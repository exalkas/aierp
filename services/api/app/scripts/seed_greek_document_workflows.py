"""
Database seed script for Greek Document Workflow State Machine
Populates transition rules and workflow templates for all 16 Greek document types (παραστατικά)

Usage:
    python -m app.scripts.seed_greek_document_workflows
    
    Or with company filter:
    python -m app.scripts.seed_greek_document_workflows --company-id <uuid>
"""

import asyncio
import logging
import argparse
from uuid import UUID
from typing import Dict, List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from ..core.database import async_session
from ..models.document_state_machine import (
    DocumentState, DocumentAction, StateTransitionRule, GreekDocumentWorkflowTemplate,
    GREEK_DOCUMENT_WORKFLOWS
)
from ..models.company import Company

logger = logging.getLogger(__name__)


async def seed_greek_document_workflows(company_id: Optional[UUID] = None):
    """
    Seed Greek document workflow transition rules and templates
    
    Args:
        company_id: Optional company ID to seed for specific company
    """
    logger.info("Starting Greek document workflow seeding...")
    
    async with async_session() as db:
        try:
            # Get companies to seed for
            if company_id:
                result = await db.execute(select(Company).where(Company.id == company_id))
                companies = result.scalars().all()
                if not companies:
                    logger.error(f"Company with ID {company_id} not found")
                    return
            else:
                result = await db.execute(select(Company))
                companies = result.scalars().all()
            
            if not companies:
                logger.warning("No companies found. Creating system-wide templates...")
                companies = [None]  # Create system-wide templates
            
            # Clear existing rules and templates for the companies
            for company in companies:
                if company:
                    await db.execute(delete(StateTransitionRule).where(StateTransitionRule.company_id == company.id))
                    await db.execute(delete(GreekDocumentWorkflowTemplate).where(GreekDocumentWorkflowTemplate.company_id == company.id))
                else:
                    # Clear system-wide templates
                    await db.execute(delete(GreekDocumentWorkflowTemplate).where(GreekDocumentWorkflowTemplate.company_id.is_(None)))
            
            await db.commit()
            
            # Seed transition rules and templates for each company
            for company in companies:
                for doc_type, workflow_def in GREEK_DOCUMENT_WORKFLOWS.items():
                    await seed_document_type_rules(db, doc_type, workflow_def, company)
                    await create_workflow_template(db, doc_type, workflow_def, company)
            
            await db.commit()
            logger.info("Greek document workflow seeding completed successfully")
            
        except Exception as e:
            logger.error(f"Error seeding Greek document workflows: {str(e)}")
            await db.rollback()
            raise


async def seed_document_type_rules(db: AsyncSession, doc_type: str, workflow_def: Dict[str, Any], company: Optional[Company]):
    """
    Seed transition rules for a specific document type
    
    Args:
        db: Database session
        doc_type: Document type (e.g., 'sales_invoice')
        workflow_def: Workflow definition from GREEK_DOCUMENT_WORKFLOWS
        company: Company instance or None for system-wide
    """
    logger.info(f"Seeding rules for document type: {doc_type}, company: {company.name if company else 'system-wide'}")
    
    # Get Greek document type info
    doc_info = get_document_type_info(doc_type)
    
    # Create transition rules
    transitions = workflow_def.get('transitions', [])
    for transition in transitions:
        rule = StateTransitionRule(
            company_id=company.id if company else None,
            document_type=doc_type,
            from_state=transition['from'],
            to_state=transition['to'],
            action=transition['action'],
            is_active=True,
            is_automatic=transition.get('is_automatic', False),
            conditions=transition.get('conditions', {}),
            required_role=transition.get('required_role'),
            greek_business_rules=get_greek_business_rules(doc_type, transition['action']),
            aade_requirements=get_aade_requirements(doc_type, transition['action']),
            validation_rules=get_validation_rules(doc_type, transition['action'])
        )
        db.add(rule)
    
    # Create conversion rules
    conversions = workflow_def.get('conversions', [])
    for conversion in conversions:
        rule = StateTransitionRule(
            company_id=company.id if company else None,
            document_type=doc_type,
            from_state=DocumentState.ISSUED.value,  # Most conversions happen from issued state
            to_state=DocumentState.COMPLETED.value,  # Conversion completes the original document
            action=conversion['action'],
            is_active=True,
            is_automatic=False,
            conditions=conversion.get('conditions', {}),
            required_role='manager',  # Conversions usually require manager role
            greek_business_rules=get_conversion_business_rules(doc_type, conversion['target_type']),
            aade_requirements=get_conversion_aade_requirements(doc_type, conversion['target_type']),
            validation_rules=get_conversion_validation_rules(doc_type, conversion['target_type'])
        )
        db.add(rule)


async def create_workflow_template(db: AsyncSession, doc_type: str, workflow_def: Dict[str, Any], company: Optional[Company]):
    """
    Create workflow template for a document type
    
    Args:
        db: Database session
        doc_type: Document type
        workflow_def: Workflow definition
        company: Company instance or None for system-wide
    """
    # Get Greek document type info
    doc_info = get_document_type_info(doc_type)
    
    template = GreekDocumentWorkflowTemplate(
        company_id=company.id if company else None,
        document_type=doc_type,
        name=doc_info.get('greek_name', doc_type),
        description=f"Workflow template for {doc_type}",
        initial_state=DocumentState.DRAFT.value,
        final_states=get_final_states(workflow_def),
        state_config=get_state_config(workflow_def),
        action_config=get_action_config(workflow_def),
        greek_legal_refs=get_greek_legal_refs(doc_type),
        aade_mydata_mapping=get_aade_mydata_mapping(doc_type),
        is_default=True,
        is_active=True
    )
    
    db.add(template)


def get_document_type_info(doc_type: str) -> Dict[str, Any]:
    """Get Greek document type information"""
    document_info = {
        'proforma': {
            'greek_name': 'Προτιμολόγιο',
            'legal_reference': 'Ν. 4308/2014 - Προσφορά χωρίς φορολογικές επιπτώσεις',
            'is_legal': False,
            'affects_vat': False,
            'requires_aade': False
        },
        'sales_order': {
            'greek_name': 'Δελτίο Παραγγελίας',
            'legal_reference': 'Εσωτερικό έγγραφο - Καταγραφή παραγγελιών',
            'is_legal': False,
            'affects_vat': False,
            'requires_aade': False
        },
        'order_confirmation': {
            'greek_name': 'Επιβεβαίωση Παραγγελίας',
            'legal_reference': 'Εσωτερικό έγγραφο - Επιβεβαίωση παραγγελίας',
            'is_legal': False,
            'affects_vat': False,
            'requires_aade': False
        },
        'purchase_order': {
            'greek_name': 'Παραγγελία Προμηθευτή',
            'legal_reference': 'Εσωτερικό έγγραφο - Παραγγελία προμηθειών',
            'is_legal': False,
            'affects_vat': False,
            'requires_aade': False
        },
        'delivery_note': {
            'greek_name': 'Δελτίο Αποστολής',
            'legal_reference': 'Ν. 4308/2014 - Συνοδεύει μεταφορά αγαθών',
            'is_legal': True,
            'affects_vat': False,
            'requires_aade': True
        },
        'sales_invoice': {
            'greek_name': 'Τιμολόγιο Πώλησης',
            'legal_reference': 'Ν. 4308/2014 - Βασικό φορολογικό έγγραφο',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'simplified_invoice': {
            'greek_name': 'Απλοποιημένο Τιμολόγιο',
            'legal_reference': 'Ν. 4308/2014 - Έως €1.500',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'receipt': {
            'greek_name': 'Απόδειξη Λιανικής Πώλησης',
            'legal_reference': 'Ν. 4308/2014 - Λιανικές πωλήσεις έως €500',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'credit_note': {
            'greek_name': 'Πιστωτικό Τιμολόγιο',
            'legal_reference': 'Ν. 4308/2014 - Διόρθωση/μείωση τιμολογίου',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'debit_note': {
            'greek_name': 'Χρεωστικό Τιμολόγιο',
            'legal_reference': 'Ν. 4308/2014 - Πρόσθετη χρέωση',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'purchase_invoice': {
            'greek_name': 'Τιμολόγιο Αγοράς',
            'legal_reference': 'Ν. 4308/2014 - Καταγραφή αγορών',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'expense_report': {
            'greek_name': 'Αναφορά Δαπανών',
            'legal_reference': 'Εσωτερικό έγγραφο - Δαπάνες υπαλλήλων',
            'is_legal': False,
            'affects_vat': False,
            'requires_aade': False
        },
        'contract': {
            'greek_name': 'Σύμβαση',
            'legal_reference': 'Αστικός Κώδικας - Συμβατικές υποχρεώσεις',
            'is_legal': True,
            'affects_vat': False,
            'requires_aade': False
        },
        'self_invoice': {
            'greek_name': 'Αυτοτιμολόγιο',
            'legal_reference': 'Ν. 4308/2014 - Αυτοτιμολόγηση',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        },
        'payment_voucher': {
            'greek_name': 'Παραστατικό Πληρωμής',
            'legal_reference': 'Εσωτερικό έγγραφο - Καταγραφή πληρωμών',
            'is_legal': False,
            'affects_vat': False,
            'requires_aade': False
        },
        'cash_register_receipt': {
            'greek_name': 'Απόδειξη Ταμείου',
            'legal_reference': 'Ν. 4308/2014 - Λιανικές πωλήσεις',
            'is_legal': True,
            'affects_vat': True,
            'requires_aade': True
        }
    }
    
    return document_info.get(doc_type, {
        'greek_name': doc_type,
        'legal_reference': 'Εσωτερικό έγγραφο',
        'is_legal': False,
        'affects_vat': False,
        'requires_aade': False
    })


def get_validation_rules(doc_type: str, action: str) -> Dict[str, Any]:
    """Get validation rules for document type and action"""
    base_rules = {
        'required_fields': [],
        'business_rules': [],
        'greek_specific': []
    }
    
    if action == DocumentAction.FINALIZE.value:
        base_rules['required_fields'] = ['customer_id', 'total_amount']
        base_rules['business_rules'] = ['must_have_line_items', 'vat_calculation_valid']
        
        doc_info = get_document_type_info(doc_type)
        if doc_info.get('requires_aade'):
            base_rules['greek_specific'] = ['aade_submission_required']
    
    return base_rules


def get_greek_business_rules(doc_type: str, action: str) -> Dict[str, Any]:
    """Get Greek-specific business rules"""
    rules = {
        'vat_validation': True,
        'customer_validation': True,
        'series_validation': True
    }
    
    doc_info = get_document_type_info(doc_type)
    
    if doc_info.get('requires_aade'):
        rules['aade_submission'] = True
        rules['mydata_format'] = True
    
    if action == DocumentAction.ISSUE.value:
        rules['numbering_sequence'] = True
        rules['issue_date_validation'] = True
    
    return rules


def get_aade_requirements(doc_type: str, action: str) -> Dict[str, Any]:
    """Get AADE requirements for document type and action"""
    requirements = {}
    
    doc_info = get_document_type_info(doc_type)
    
    if doc_info.get('requires_aade'):
        requirements = {
            'mydata_submission': True,
            'invoice_type': get_mydata_invoice_type(doc_type),
            'required_fields': ['mark', 'uid', 'auth_code', 'qr_url']
        }
        
        if action == DocumentAction.ISSUE.value:
            requirements['submit_immediately'] = True
        elif action == DocumentAction.CANCEL.value:
            requirements['cancellation_submission'] = True
    
    return requirements


def get_conversion_business_rules(source_type: str, target_type: str) -> Dict[str, Any]:
    """Get business rules for document conversion"""
    return {
        'preserve_customer': True,
        'preserve_line_items': True,
        'update_references': True,
        'validate_conversion_allowed': True
    }


def get_conversion_aade_requirements(source_type: str, target_type: str) -> Dict[str, Any]:
    """Get AADE requirements for document conversion"""
    source_info = get_document_type_info(source_type)
    target_info = get_document_type_info(target_type)
    
    requirements = {}
    
    if source_info.get('requires_aade') and target_info.get('requires_aade'):
        requirements = {
            'update_related_documents': True,
            'submit_conversion': True
        }
    
    return requirements


def get_conversion_validation_rules(source_type: str, target_type: str) -> Dict[str, Any]:
    """Get validation rules for document conversion"""
    return {
        'source_must_be_issued': True,
        'target_fields_valid': True,
        'no_duplicate_conversion': True
    }


def get_final_states(workflow_def: Dict[str, Any]) -> List[str]:
    """Get final states from workflow definition"""
    final_states = []
    
    # Standard final states
    states_in_transitions = set()
    for transition in workflow_def.get('transitions', []):
        states_in_transitions.add(transition['from'])
        states_in_transitions.add(transition['to'])
    
    # States that are destinations but not sources are final
    destination_states = set()
    source_states = set()
    
    for transition in workflow_def.get('transitions', []):
        destination_states.add(transition['to'])
        source_states.add(transition['from'])
    
    # Final states are those that are destinations but not sources
    potential_final = destination_states - source_states
    
    # Add common final states
    common_final = ['COMPLETED', 'CANCELLED', 'CLOSED', 'DELIVERED']
    for state in common_final:
        if state in states_in_transitions:
            potential_final.add(state)
    
    return list(potential_final)


def get_state_config(workflow_def: Dict[str, Any]) -> Dict[str, Any]:
    """Get state configuration from workflow definition"""
    return {
        'states': workflow_def.get('states', {}),
        'initial_state': DocumentState.DRAFT.value,
        'validation_rules': workflow_def.get('validation_rules', {})
    }


def get_action_config(workflow_def: Dict[str, Any]) -> Dict[str, Any]:
    """Get action configuration from workflow definition"""
    return {
        'actions': workflow_def.get('actions', {}),
        'transitions': workflow_def.get('transitions', []),
        'conversions': workflow_def.get('conversions', [])
    }


def get_greek_legal_refs(doc_type: str) -> Dict[str, Any]:
    """Get Greek legal references for document type"""
    doc_info = get_document_type_info(doc_type)
    return {
        'primary_law': doc_info.get('legal_reference', ''),
        'secondary_regulations': [],
        'aade_guidelines': []
    }


def get_aade_mydata_mapping(doc_type: str) -> Dict[str, Any]:
    """Get AADE MyDATA mapping for document type"""
    return {
        'invoice_type': get_mydata_invoice_type(doc_type),
        'classification_category': get_classification_category(doc_type),
        'vat_category': get_vat_category(doc_type)
    }


def get_mydata_invoice_type(doc_type: str) -> str:
    """Get MyDATA invoice type for document type"""
    mapping = {
        'sales_invoice': '1.1',
        'simplified_invoice': '1.2',
        'receipt': '1.3',
        'credit_note': '1.4',
        'debit_note': '1.5',
        'purchase_invoice': '2.1',
        'self_invoice': '2.2',
        'delivery_note': '8.1',
        'cash_register_receipt': '1.3'
    }
    return mapping.get(doc_type, '1.1')


def get_classification_category(doc_type: str) -> str:
    """Get classification category for document type"""
    if doc_type in ['sales_invoice', 'simplified_invoice', 'receipt']:
        return 'category1_3'
    elif doc_type in ['purchase_invoice']:
        return 'category2_1'
    return 'category1_95'


def get_vat_category(doc_type: str) -> str:
    """Get VAT category for document type"""
    doc_info = get_document_type_info(doc_type)
    if doc_info.get('affects_vat'):
        return '1'  # Standard VAT
    return '8'  # No VAT


async def main():
    """Main function to run the seed script"""
    parser = argparse.ArgumentParser(description='Seed Greek document workflows')
    parser.add_argument('--company-id', type=str, help='Company ID to seed for')
    args = parser.parse_args()
    
    company_id = None
    if args.company_id:
        try:
            company_id = UUID(args.company_id)
        except ValueError:
            logger.error(f"Invalid company ID format: {args.company_id}")
            return
    
    await seed_greek_document_workflows(company_id)


if __name__ == "__main__":
    asyncio.run(main()) 