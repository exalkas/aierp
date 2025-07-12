"""
Greek Document Workflow Service
Handles state transitions, validation, and automation for Greek παραστατικά (business documents)
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.document_state_machine import (
    DocumentState, DocumentAction, StateTransitionRule, DocumentWorkflowInstance,
    DocumentStateHistory, DocumentAutomationRule, GreekDocumentWorkflowTemplate,
    GREEK_DOCUMENT_WORKFLOWS
)
from ..models.invoice import Invoice, InvoiceType, InvoiceStatus
from ..models.business_entity import BusinessEntity
from ..core.database import get_db
from .aade_integration_service import AADEIntegrationService

logger = logging.getLogger(__name__)


class DocumentWorkflowService:
    """
    Service for managing Greek document workflow state transitions
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.aade_service = AADEIntegrationService()
    
    def initialize_workflow(self, document_id: str, document_type: str) -> DocumentWorkflowInstance:
        """
        Initialize workflow for a new document
        
        Args:
            document_id: UUID of the document
            document_type: Type of document (from InvoiceType enum)
            
        Returns:
            DocumentWorkflowInstance: Created workflow instance
        """
        try:
            # Get workflow template for document type
            template = self.get_workflow_template(document_type)
            
            # Create workflow instance
            workflow = DocumentWorkflowInstance(
                document_id=document_id,
                document_type=document_type,
                current_state=template.get('initial_state', DocumentState.DRAFT),
                workflow_context={
                    'template_used': template.get('template_code'),
                    'created_at': datetime.now().isoformat(),
                    'greek_business_rules': template.get('greek_business_rules', {}),
                    'aade_integration_points': template.get('aade_integration_points', {})
                }
            )
            
            # Calculate next actions
            workflow.next_actions = self.calculate_next_actions(
                document_type, workflow.current_state
            )
            
            self.db.add(workflow)
            self.db.commit()
            
            # Create initial state history entry
            self.create_state_history(
                workflow.id,
                None,
                workflow.current_state,
                DocumentAction.CREATE,
                triggered_by='system',
                notes='Workflow initialized'
            )
            
            logger.info(f"Workflow initialized for document {document_id} of type {document_type}")
            return workflow
            
        except Exception as e:
            logger.error(f"Error initializing workflow: {str(e)}")
            self.db.rollback()
            raise
    
    def execute_action(
        self,
        document_id: str,
        action: DocumentAction,
        user_id: Optional[str] = None,
        notes: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Execute an action on a document, triggering state transition
        
        Args:
            document_id: UUID of the document
            action: Action to execute
            user_id: User performing the action
            notes: Optional notes for the action
            additional_data: Additional data for the action
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Get workflow instance
            workflow = self.get_workflow_instance(document_id)
            if not workflow:
                return False, "Workflow not found"
            
            # Get document
            document = self.db.query(Invoice).filter(Invoice.id == document_id).first()
            if not document:
                return False, "Document not found"
            
            # Validate action
            is_valid, error_message = self.validate_action(
                workflow.document_type, workflow.current_state, action
            )
            if not is_valid:
                return False, error_message
            
            # Get transition rule
            transition_rule = self.get_transition_rule(
                workflow.document_type, workflow.current_state, action
            )
            if not transition_rule:
                return False, f"No transition rule found for action {action.value}"
            
            # Check business rules
            business_rules_valid, business_error = self.validate_business_rules(
                document, workflow, action, transition_rule
            )
            if not business_rules_valid:
                return False, business_error
            
            # Execute pre-action hooks
            self.execute_pre_action_hooks(document, workflow, action, additional_data)
            
            # Perform state transition
            old_state = workflow.current_state
            new_state = transition_rule.to_state
            
            # Update workflow instance
            workflow.previous_state = old_state
            workflow.current_state = new_state
            workflow.next_actions = self.calculate_next_actions(
                workflow.document_type, new_state
            )
            
            # Update document status if needed
            self.update_document_status(document, new_state, action)
            
            # Create state history entry
            self.create_state_history(
                workflow.id,
                old_state,
                new_state,
                action,
                triggered_by='user' if user_id else 'system',
                user_id=user_id,
                notes=notes,
                transition_data=additional_data or {}
            )
            
            # Execute post-action hooks
            self.execute_post_action_hooks(document, workflow, action, additional_data)
            
            # Check if workflow is completed
            if self.is_final_state(workflow.document_type, new_state):
                workflow.is_completed = True
                workflow.workflow_completed_at = datetime.now()
            
            self.db.commit()
            
            logger.info(f"Action {action.value} executed successfully for document {document_id}")
            return True, f"Action {action.value} executed successfully"
            
        except Exception as e:
            logger.error(f"Error executing action {action.value}: {str(e)}")
            self.db.rollback()
            return False, f"Error executing action: {str(e)}"
    
    def get_workflow_instance(self, document_id: str) -> Optional[DocumentWorkflowInstance]:
        """Get workflow instance for a document"""
        return self.db.query(DocumentWorkflowInstance).filter(
            DocumentWorkflowInstance.document_id == document_id
        ).first()
    
    def get_workflow_template(self, document_type: str) -> Dict[str, Any]:
        """Get workflow template for document type"""
        # First try to get from database
        template = self.db.query(GreekDocumentWorkflowTemplate).filter(
            GreekDocumentWorkflowTemplate.document_type == document_type,
            GreekDocumentWorkflowTemplate.is_active == True
        ).first()
        
        if template:
            return template.workflow_definition
        
        # Fall back to predefined workflows
        return GREEK_DOCUMENT_WORKFLOWS.get(document_type, {
            'initial_state': DocumentState.DRAFT,
            'final_states': [DocumentState.COMPLETED, DocumentState.CANCELLED],
            'transitions': []
        })
    
    def get_transition_rule(
        self, document_type: str, from_state: DocumentState, action: DocumentAction
    ) -> Optional[StateTransitionRule]:
        """Get transition rule for document type, state, and action"""
        return self.db.query(StateTransitionRule).filter(
            StateTransitionRule.document_type == document_type,
            StateTransitionRule.from_state == from_state,
            StateTransitionRule.action == action,
            StateTransitionRule.is_active == True
        ).first()
    
    def validate_action(
        self, document_type: str, current_state: DocumentState, action: DocumentAction
    ) -> Tuple[bool, str]:
        """
        Validate if an action is allowed from current state
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # Check if transition rule exists
        transition_rule = self.get_transition_rule(document_type, current_state, action)
        if not transition_rule:
            return False, f"Action {action.value} not allowed from state {current_state.value}"
        
        # Check if rule is active
        if not transition_rule.is_active:
            return False, f"Transition rule is inactive"
        
        return True, ""
    
    def validate_business_rules(
        self,
        document: Invoice,
        workflow: DocumentWorkflowInstance,
        action: DocumentAction,
        transition_rule: StateTransitionRule
    ) -> Tuple[bool, str]:
        """
        Validate Greek business rules for the transition
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Get business rules from transition rule
            business_rules = transition_rule.greek_business_rules or {}
            
            # Document-specific validations
            if action == DocumentAction.ISSUE:
                # Check if document is complete
                if not self.is_document_complete(document):
                    return False, "Document must be complete before issuing"
                
                # Check AADE requirements for legal documents
                if document.is_legal_document and not self.validate_aade_requirements(document):
                    return False, "AADE requirements not met"
            
            elif action == DocumentAction.RECORD_PAYMENT:
                # Validate payment amount
                if not self.validate_payment_amount(document):
                    return False, "Invalid payment amount"
            
            elif action == DocumentAction.CONVERT_TO_INVOICE:
                # Check if conversion is allowed
                if not self.can_convert_to_invoice(document):
                    return False, "Document cannot be converted to invoice"
            
            # Greek-specific business rule validations
            if business_rules.get('require_customer_vat_check'):
                if not self.validate_customer_vat(document):
                    return False, "Customer VAT validation failed"
            
            if business_rules.get('require_greek_address'):
                if not self.validate_greek_address(document):
                    return False, "Valid Greek address required"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Error validating business rules: {str(e)}")
            return False, f"Business rule validation error: {str(e)}"
    
    def calculate_next_actions(
        self, document_type: str, current_state: DocumentState
    ) -> List[str]:
        """Calculate next available actions for current state"""
        try:
            # Get all valid transitions from current state
            transitions = self.db.query(StateTransitionRule).filter(
                StateTransitionRule.document_type == document_type,
                StateTransitionRule.from_state == current_state,
                StateTransitionRule.is_active == True
            ).all()
            
            return [t.action.value for t in transitions]
            
        except Exception as e:
            logger.error(f"Error calculating next actions: {str(e)}")
            return []
    
    def create_state_history(
        self,
        workflow_instance_id: str,
        from_state: Optional[DocumentState],
        to_state: DocumentState,
        action: DocumentAction,
        triggered_by: str = 'user',
        user_id: Optional[str] = None,
        notes: Optional[str] = None,
        transition_data: Optional[Dict[str, Any]] = None
    ) -> DocumentStateHistory:
        """Create state history entry"""
        try:
            history = DocumentStateHistory(
                workflow_instance_id=workflow_instance_id,
                from_state=from_state,
                to_state=to_state,
                action=action,
                triggered_by=triggered_by,
                user_id=user_id,
                notes=notes,
                transition_data=transition_data or {}
            )
            
            self.db.add(history)
            self.db.flush()  # Get ID without committing
            
            return history
            
        except Exception as e:
            logger.error(f"Error creating state history: {str(e)}")
            raise
    
    def execute_pre_action_hooks(
        self,
        document: Invoice,
        workflow: DocumentWorkflowInstance,
        action: DocumentAction,
        additional_data: Optional[Dict[str, Any]]
    ):
        """Execute pre-action hooks"""
        try:
            if action == DocumentAction.ISSUE and document.is_legal_document:
                # Generate invoice number if not set
                if not document.invoice_number:
                    document.invoice_number = self.generate_invoice_number(document)
                
                # Set issue date
                if not document.issue_date:
                    document.issue_date = datetime.now()
                
                # Calculate due date
                if not document.due_date:
                    document.due_date = self.calculate_due_date(document)
            
            elif action == DocumentAction.CONVERT_TO_INVOICE:
                # Prepare for invoice conversion
                self.prepare_invoice_conversion(document, additional_data)
            
            elif action == DocumentAction.SEND:
                # Prepare for sending
                self.prepare_document_send(document, additional_data)
            
        except Exception as e:
            logger.error(f"Error in pre-action hooks: {str(e)}")
            raise
    
    def execute_post_action_hooks(
        self,
        document: Invoice,
        workflow: DocumentWorkflowInstance,
        action: DocumentAction,
        additional_data: Optional[Dict[str, Any]]
    ):
        """Execute post-action hooks"""
        try:
            if action == DocumentAction.ISSUE and document.is_legal_document:
                # Submit to AADE if required
                if document.aade_status == 'not_submitted':
                    self.schedule_aade_submission(document)
            
            elif action == DocumentAction.RECORD_PAYMENT:
                # Update payment status
                self.update_payment_status(document, additional_data)
            
            elif action == DocumentAction.CONVERT_TO_INVOICE:
                # Create the actual invoice
                self.create_converted_invoice(document, additional_data)
            
            # Trigger any automation rules
            self.trigger_automation_rules(document, workflow, action)
            
        except Exception as e:
            logger.error(f"Error in post-action hooks: {str(e)}")
            raise
    
    def is_document_complete(self, document: Invoice) -> bool:
        """Check if document is complete for issuing"""
        # Check required fields
        if not document.business_entity_id:
            return False
        
        if not document.invoice_items:
            return False
        
        # Check if all line items are valid
        for item in document.invoice_items:
            if not item.product_name or item.quantity <= 0 or item.unit_price < 0:
                return False
        
        return True
    
    def validate_aade_requirements(self, document: Invoice) -> bool:
        """Validate AADE requirements for legal documents"""
        # Check if business entity has valid AFM
        if document.business_entity and not document.business_entity.afm:
            return False
        
        # Check if VAT calculations are correct
        if document.affects_vat and not self.validate_vat_calculations(document):
            return False
        
        return True
    
    def validate_vat_calculations(self, document: Invoice) -> bool:
        """Validate VAT calculations"""
        # This would implement VAT validation logic
        # For now, return True (implement based on Greek VAT rules)
        return True
    
    def validate_customer_vat(self, document: Invoice) -> bool:
        """Validate customer VAT information"""
        if document.business_entity and document.business_entity.vat_number:
            # This would validate VAT number against EU VIES system
            return True
        return True
    
    def validate_greek_address(self, document: Invoice) -> bool:
        """Validate Greek address requirements"""
        if document.business_entity:
            return bool(
                document.business_entity.address_street and
                document.business_entity.address_city and
                document.business_entity.address_postal_code
            )
        return False
    
    def is_final_state(self, document_type: str, state: DocumentState) -> bool:
        """Check if state is a final state for document type"""
        workflow = self.get_workflow_template(document_type)
        final_states = workflow.get('final_states', [])
        return state in final_states
    
    def update_document_status(self, document: Invoice, new_state: DocumentState, action: DocumentAction):
        """Update document status based on new state"""
        # Map workflow states to document statuses
        status_mapping = {
            DocumentState.DRAFT: InvoiceStatus.DRAFT,
            DocumentState.OPEN: InvoiceStatus.SENT,
            DocumentState.PAID: InvoiceStatus.PAID,
            DocumentState.PARTIALLY_PAID: InvoiceStatus.PARTIALLY_PAID,
            DocumentState.OVERDUE: InvoiceStatus.OVERDUE,
            DocumentState.CANCELLED: InvoiceStatus.CANCELLED,
            DocumentState.COMPLETED: InvoiceStatus.COMPLETED,
        }
        
        if new_state in status_mapping:
            document.status = status_mapping[new_state]
    
    def generate_invoice_number(self, document: Invoice) -> str:
        """Generate invoice number"""
        # This would implement invoice number generation logic
        # For now, return a simple format
        return f"INV-{datetime.now().strftime('%Y%m%d')}-{document.id.hex[:8].upper()}"
    
    def calculate_due_date(self, document: Invoice) -> datetime:
        """Calculate due date based on payment terms"""
        # Default to 30 days from issue date
        return document.issue_date + timedelta(days=30)
    
    def schedule_aade_submission(self, document: Invoice):
        """Schedule AADE submission for legal documents"""
        # This would schedule AADE submission
        logger.info(f"Scheduling AADE submission for document {document.id}")
    
    def update_payment_status(self, document: Invoice, payment_data: Optional[Dict[str, Any]]):
        """Update payment status and amounts"""
        if payment_data and 'amount' in payment_data:
            document.paid_amount = (document.paid_amount or 0) + payment_data['amount']
            document.outstanding_amount = document.total_amount - document.paid_amount
    
    def trigger_automation_rules(self, document: Invoice, workflow: DocumentWorkflowInstance, action: DocumentAction):
        """Trigger any applicable automation rules"""
        # Get automation rules for this document type and action
        rules = self.db.query(DocumentAutomationRule).filter(
            DocumentAutomationRule.is_active == True,
            DocumentAutomationRule.trigger_type == 'event_based'
        ).all()
        
        for rule in rules:
            if self.should_trigger_rule(rule, document, workflow, action):
                self.execute_automation_rule(rule, document, workflow)
    
    def should_trigger_rule(
        self, rule: DocumentAutomationRule, document: Invoice, workflow: DocumentWorkflowInstance, action: DocumentAction
    ) -> bool:
        """Check if automation rule should be triggered"""
        # Check if document type matches
        if rule.document_types and document.invoice_type.value not in rule.document_types:
            return False
        
        # Check trigger conditions
        conditions = rule.trigger_conditions or {}
        if 'actions' in conditions and action.value not in conditions['actions']:
            return False
        
        return True
    
    def execute_automation_rule(self, rule: DocumentAutomationRule, document: Invoice, workflow: DocumentWorkflowInstance):
        """Execute automation rule"""
        try:
            logger.info(f"Executing automation rule {rule.rule_code} for document {document.id}")
            
            # Update execution tracking
            rule.last_executed_at = datetime.now()
            rule.execution_count += 1
            
            # Execute the rule action
            if rule.action == DocumentAction.SEND:
                # Send document automatically
                self.send_document_automatically(document, rule.action_parameters)
            elif rule.action == DocumentAction.RECORD_PAYMENT:
                # Auto-record payment
                self.auto_record_payment(document, rule.action_parameters)
            
            rule.success_count += 1
            
        except Exception as e:
            logger.error(f"Error executing automation rule {rule.rule_code}: {str(e)}")
            rule.error_count += 1
    
    def send_document_automatically(self, document: Invoice, parameters: Dict[str, Any]):
        """Send document automatically"""
        # This would implement automatic document sending
        logger.info(f"Sending document {document.id} automatically")
    
    def auto_record_payment(self, document: Invoice, parameters: Dict[str, Any]):
        """Auto-record payment"""
        # This would implement automatic payment recording
        logger.info(f"Auto-recording payment for document {document.id}")
    
    def get_document_workflow_status(self, document_id: str) -> Dict[str, Any]:
        """Get complete workflow status for a document"""
        try:
            workflow = self.get_workflow_instance(document_id)
            if not workflow:
                return {'error': 'Workflow not found'}
            
            # Get state history
            history = self.db.query(DocumentStateHistory).filter(
                DocumentStateHistory.workflow_instance_id == workflow.id
            ).order_by(DocumentStateHistory.transition_date.desc()).all()
            
            return {
                'workflow_id': workflow.id,
                'document_id': document_id,
                'document_type': workflow.document_type,
                'current_state': workflow.current_state.value,
                'is_completed': workflow.is_completed,
                'next_actions': workflow.next_actions,
                'workflow_started_at': workflow.workflow_started_at.isoformat(),
                'workflow_completed_at': workflow.workflow_completed_at.isoformat() if workflow.workflow_completed_at else None,
                'state_history': [
                    {
                        'from_state': h.from_state.value if h.from_state else None,
                        'to_state': h.to_state.value,
                        'action': h.action.value,
                        'transition_date': h.transition_date.isoformat(),
                        'triggered_by': h.triggered_by,
                        'notes': h.notes
                    } for h in history
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting workflow status: {str(e)}")
            return {'error': str(e)}
    
    def prepare_invoice_conversion(self, document: Invoice, additional_data: Optional[Dict[str, Any]]):
        """Prepare document for invoice conversion"""
        # Implementation depends on specific conversion logic
        pass
    
    def prepare_document_send(self, document: Invoice, additional_data: Optional[Dict[str, Any]]):
        """Prepare document for sending"""
        # Implementation depends on specific sending logic
        pass
    
    def create_converted_invoice(self, document: Invoice, additional_data: Optional[Dict[str, Any]]):
        """Create converted invoice"""
        # Implementation depends on specific conversion logic
        pass
    
    def validate_payment_amount(self, document: Invoice) -> bool:
        """Validate payment amount"""
        # Implementation depends on specific payment validation logic
        return True
    
    def can_convert_to_invoice(self, document: Invoice) -> bool:
        """Check if document can be converted to invoice"""
        # Implementation depends on specific conversion rules
        return True 