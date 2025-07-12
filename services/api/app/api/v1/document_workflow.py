"""
Document Workflow API endpoints for Greek παραστατικά state machine management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from ...core.database import get_db
from ...services.document_workflow_service import DocumentWorkflowService
from ...models.document_state_machine import DocumentState, DocumentAction
from ...models.invoice import Invoice

router = APIRouter(prefix="/workflow", tags=["Document Workflow"])


# Pydantic models for request/response
class WorkflowStatusResponse(BaseModel):
    """Response model for workflow status"""
    workflow_id: str
    document_id: str
    document_type: str
    current_state: str
    is_completed: bool
    next_actions: List[str]
    workflow_started_at: datetime
    workflow_completed_at: Optional[datetime] = None
    state_history: List[Dict[str, Any]]


class ExecuteActionRequest(BaseModel):
    """Request model for executing workflow actions"""
    action: str = Field(..., description="Action to execute")
    notes: Optional[str] = Field(None, description="Optional notes for the action")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Additional data for the action")


class ExecuteActionResponse(BaseModel):
    """Response model for action execution"""
    success: bool
    message: str
    new_state: Optional[str] = None
    next_actions: List[str] = []


class WorkflowInitRequest(BaseModel):
    """Request model for workflow initialization"""
    document_id: str = Field(..., description="Document ID to initialize workflow for")
    document_type: str = Field(..., description="Type of document")


class WorkflowInitResponse(BaseModel):
    """Response model for workflow initialization"""
    workflow_id: str
    document_id: str
    document_type: str
    initial_state: str
    next_actions: List[str]


class StateTransitionRule(BaseModel):
    """State transition rule model"""
    from_state: str
    to_state: str
    action: str
    description: Optional[str] = None
    greek_description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None


class DocumentWorkflowTemplate(BaseModel):
    """Document workflow template model"""
    document_type: str
    template_name: str
    states: List[str]
    transitions: List[StateTransitionRule]
    initial_state: str
    final_states: List[str]


@router.post("/initialize", response_model=WorkflowInitResponse)
async def initialize_workflow(
    request: WorkflowInitRequest,
    db: Session = Depends(get_db)
):
    """
    Initialize workflow for a document
    
    Creates a new workflow instance for the specified document with the appropriate
    initial state and available actions based on the document type.
    """
    try:
        service = DocumentWorkflowService(db)
        
        # Verify document exists
        document = db.query(Invoice).filter(Invoice.id == request.document_id).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Check if workflow already exists
        existing_workflow = service.get_workflow_instance(request.document_id)
        if existing_workflow:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Workflow already exists for this document"
            )
        
        # Initialize workflow
        workflow = service.initialize_workflow(request.document_id, request.document_type)
        
        return WorkflowInitResponse(
            workflow_id=str(workflow.id),
            document_id=request.document_id,
            document_type=workflow.document_type,
            initial_state=workflow.current_state.value,
            next_actions=workflow.next_actions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing workflow: {str(e)}"
        )


@router.get("/status/{document_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get current workflow status for a document
    
    Returns the current state, available actions, and complete state history
    for the specified document.
    """
    try:
        service = DocumentWorkflowService(db)
        status_data = service.get_document_workflow_status(document_id)
        
        if 'error' in status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=status_data['error']
            )
        
        return WorkflowStatusResponse(**status_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting workflow status: {str(e)}"
        )


@router.post("/execute/{document_id}", response_model=ExecuteActionResponse)
async def execute_action(
    document_id: str,
    request: ExecuteActionRequest,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Execute an action on a document
    
    Triggers a state transition by executing the specified action on the document.
    Validates business rules and updates the document state accordingly.
    """
    try:
        service = DocumentWorkflowService(db)
        
        # Validate action
        try:
            action = DocumentAction(request.action)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid action: {request.action}"
            )
        
        # Execute action
        success, message = service.execute_action(
            document_id=document_id,
            action=action,
            user_id=user_id,
            notes=request.notes,
            additional_data=request.additional_data
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Get updated workflow status
        workflow = service.get_workflow_instance(document_id)
        
        return ExecuteActionResponse(
            success=success,
            message=message,
            new_state=workflow.current_state.value if workflow else None,
            next_actions=workflow.next_actions if workflow else []
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing action: {str(e)}"
        )


@router.get("/actions/{document_id}")
async def get_available_actions(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get available actions for a document
    
    Returns the list of actions that can be performed on the document
    in its current state.
    """
    try:
        service = DocumentWorkflowService(db)
        workflow = service.get_workflow_instance(document_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found"
            )
        
        return {
            "document_id": document_id,
            "current_state": workflow.current_state.value,
            "available_actions": workflow.next_actions,
            "is_completed": workflow.is_completed
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting available actions: {str(e)}"
        )


@router.get("/history/{document_id}")
async def get_state_history(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get complete state history for a document
    
    Returns chronological list of all state transitions for the document.
    """
    try:
        service = DocumentWorkflowService(db)
        status_data = service.get_document_workflow_status(document_id)
        
        if 'error' in status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=status_data['error']
            )
        
        return {
            "document_id": document_id,
            "document_type": status_data['document_type'],
            "current_state": status_data['current_state'],
            "state_history": status_data['state_history']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting state history: {str(e)}"
        )


@router.get("/templates/{document_type}")
async def get_workflow_template(
    document_type: str,
    db: Session = Depends(get_db)
):
    """
    Get workflow template for a document type
    
    Returns the workflow template configuration for the specified
    Greek document type (παραστατικό).
    """
    try:
        service = DocumentWorkflowService(db)
        template = service.get_workflow_template(document_type)
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No workflow template found for document type: {document_type}"
            )
        
        return {
            "document_type": document_type,
            "template": template
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting workflow template: {str(e)}"
        )


@router.get("/templates")
async def get_all_workflow_templates(
    db: Session = Depends(get_db)
):
    """
    Get all available workflow templates
    
    Returns workflow templates for all supported Greek document types.
    """
    try:
        from ...models.document_state_machine import GREEK_DOCUMENT_WORKFLOWS
        
        templates = []
        for doc_type, workflow_def in GREEK_DOCUMENT_WORKFLOWS.items():
            templates.append({
                "document_type": doc_type,
                "template": workflow_def
            })
        
        return {
            "templates": templates,
            "total_count": len(templates)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting workflow templates: {str(e)}"
        )


@router.get("/states")
async def get_all_document_states():
    """
    Get all available document states
    
    Returns complete list of document states used in the state machine.
    """
    try:
        states = [
            {
                "value": state.value,
                "name": state.name,
                "description": get_state_description(state)
            }
            for state in DocumentState
        ]
        
        return {
            "states": states,
            "total_count": len(states)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document states: {str(e)}"
        )


@router.get("/actions")
async def get_all_document_actions():
    """
    Get all available document actions
    
    Returns complete list of actions that can be performed on documents.
    """
    try:
        actions = [
            {
                "value": action.value,
                "name": action.name,
                "description": get_action_description(action)
            }
            for action in DocumentAction
        ]
        
        return {
            "actions": actions,
            "total_count": len(actions)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document actions: {str(e)}"
        )


def get_state_description(state: DocumentState) -> str:
    """Get human-readable description for document state"""
    descriptions = {
        DocumentState.DRAFT: "Προσχέδιο - Document is being prepared",
        DocumentState.PENDING_APPROVAL: "Εκκρεμής έγκριση - Waiting for approval",
        DocumentState.APPROVED: "Εγκεκριμένο - Document has been approved",
        DocumentState.ISSUED: "Εκδόθηκε - Document has been issued",
        DocumentState.SENT: "Αποστάληκε - Document has been sent",
        DocumentState.OPEN: "Ανοιχτό - Document is open for business",
        DocumentState.CONFIRMED: "Επιβεβαιωμένο - Document has been confirmed",
        DocumentState.ACCEPTED: "Αποδεκτό - Document has been accepted",
        DocumentState.IN_TRANSIT: "Σε μεταφορά - Goods are in transit",
        DocumentState.SHIPPED: "Αποσταλμένο - Goods have been shipped",
        DocumentState.PARTIALLY_RECEIVED: "Μερικώς παραλήφθηκε - Partially received",
        DocumentState.FULLY_RECEIVED: "Πλήρως παραλήφθηκε - Fully received",
        DocumentState.QUOTED: "Προσφέρθηκε - Quote has been provided",
        DocumentState.PARTIALLY_PAID: "Μερικώς πληρωμένο - Partially paid",
        DocumentState.PAID: "Πληρωμένο - Fully paid",
        DocumentState.OVERDUE: "Ληξιπρόθεσμο - Payment overdue",
        DocumentState.COMPLETED: "Ολοκληρωμένο - Process completed",
        DocumentState.DELIVERED: "Παραδόθηκε - Delivered successfully",
        DocumentState.APPLIED: "Εφαρμόσθηκε - Applied to invoice",
        DocumentState.CREDITED: "Πιστώθηκε - Credit applied",
        DocumentState.DEBITED: "Χρεώθηκε - Debit applied",
        DocumentState.CLOSED: "Κλείσιμο - Document closed",
        DocumentState.CANCELLED: "Ακυρώθηκε - Document cancelled",
        DocumentState.REJECTED: "Απορρίφθηκε - Document rejected",
        DocumentState.EXPIRED: "Έληξε - Document expired",
        DocumentState.DECLINED: "Απορρίφθηκε - Document declined",
        DocumentState.REFUNDED: "Επιστράφηκε - Payment refunded",
    }
    return descriptions.get(state, state.value)


def get_action_description(action: DocumentAction) -> str:
    """Get human-readable description for document action"""
    descriptions = {
        DocumentAction.CREATE: "Δημιουργία - Create document",
        DocumentAction.FINALIZE: "Οριστικοποίηση - Finalize document",
        DocumentAction.APPROVE: "Έγκριση - Approve document",
        DocumentAction.ISSUE: "Έκδοση - Issue document",
        DocumentAction.SEND: "Αποστολή - Send document",
        DocumentAction.CONFIRM: "Επιβεβαίωση - Confirm document",
        DocumentAction.ACCEPT: "Αποδοχή - Accept document",
        DocumentAction.REJECT: "Απόρριψη - Reject document",
        DocumentAction.SHIP: "Αποστολή - Ship goods",
        DocumentAction.RECEIVE: "Παραλαβή - Receive goods",
        DocumentAction.DELIVER: "Παράδοση - Deliver goods",
        DocumentAction.RECORD_PAYMENT: "Καταγραφή πληρωμής - Record payment",
        DocumentAction.MARK_OVERDUE: "Σήμανση ληξιπρόθεσμου - Mark as overdue",
        DocumentAction.CONVERT_TO_INVOICE: "Μετατροπή σε τιμολόγιο - Convert to invoice",
        DocumentAction.CONVERT_TO_CREDIT_NOTE: "Μετατροπή σε πιστωτικό - Convert to credit note",
        DocumentAction.CONVERT_TO_DEBIT_NOTE: "Μετατροπή σε χρεωστικό - Convert to debit note",
        DocumentAction.CREATE_DELIVERY_NOTE: "Δημιουργία δελτίου αποστολής - Create delivery note",
        DocumentAction.CREATE_SALES_ORDER: "Δημιουργία παραγγελίας - Create sales order",
        DocumentAction.CANCEL: "Ακύρωση - Cancel document",
        DocumentAction.CLOSE: "Κλείσιμο - Close document",
        DocumentAction.EXPIRE: "Λήξη - Expire document",
        DocumentAction.DECLINE: "Απόρριψη - Decline document",
        DocumentAction.REFUND: "Επιστροφή - Refund payment",
        DocumentAction.APPLY_TO_INVOICE: "Εφαρμογή σε τιμολόγιο - Apply to invoice",
        DocumentAction.CORRECT: "Διόρθωση - Correct document",
    }
    return descriptions.get(action, action.value) 