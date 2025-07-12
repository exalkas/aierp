"""
Greek Document State Machine Models
Comprehensive state machine system for Greek παραστατικά (business documents)
Supports all 16 Greek document types with proper state transitions and workflow automation
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

from ..core.database import Base


class DocumentState(enum.Enum):
    """
    Document states for Greek παραστατικά
    Based on Greek business practices and legal requirements
    """
    # Draft states
    DRAFT = "draft"                          # Προσχέδιο
    PENDING_APPROVAL = "pending_approval"    # Εκκρεμής έγκριση
    
    # Active states
    APPROVED = "approved"                    # Εγκεκριμένο
    ISSUED = "issued"                       # Εκδόθηκε
    SENT = "sent"                           # Αποστάληκε
    OPEN = "open"                           # Ανοιχτό
    CONFIRMED = "confirmed"                 # Επιβεβαιωμένο
    ACCEPTED = "accepted"                   # Αποδεκτό
    
    # In-process states
    IN_TRANSIT = "in_transit"               # Σε μεταφορά
    SHIPPED = "shipped"                     # Αποσταλμένο
    PARTIALLY_RECEIVED = "partially_received" # Μερικώς παραλήφθηκε
    FULLY_RECEIVED = "fully_received"       # Πλήρως παραλήφθηκε
    QUOTED = "quoted"                       # Προσφέρθηκε
    
    # Payment states
    PARTIALLY_PAID = "partially_paid"       # Μερικώς πληρωμένο
    PAID = "paid"                           # Πληρωμένο
    OVERDUE = "overdue"                     # Ληξιπρόθεσμο
    
    # Completion states
    COMPLETED = "completed"                 # Ολοκληρωμένο
    DELIVERED = "delivered"                 # Παραδόθηκε
    APPLIED = "applied"                     # Εφαρμόσθηκε
    CREDITED = "credited"                   # Πιστώθηκε
    DEBITED = "debited"                     # Χρεώθηκε
    
    # Closure states
    CLOSED = "closed"                       # Κλείσιμο
    CANCELLED = "cancelled"                 # Ακυρώθηκε
    REJECTED = "rejected"                   # Απορρίφθηκε
    EXPIRED = "expired"                     # Έληξε
    DECLINED = "declined"                   # Απορρίφθηκε
    REFUNDED = "refunded"                   # Επιστράφηκε


class DocumentAction(enum.Enum):
    """
    Actions that can be performed on Greek παραστατικά
    Each action triggers a state transition
    """
    # Creation actions
    CREATE = "create"                       # Δημιουργία
    FINALIZE = "finalize"                   # Οριστικοποίηση
    APPROVE = "approve"                     # Έγκριση
    
    # Workflow actions
    ISSUE = "issue"                         # Έκδοση
    SEND = "send"                          # Αποστολή
    CONFIRM = "confirm"                     # Επιβεβαίωση
    ACCEPT = "accept"                       # Αποδοχή
    REJECT = "reject"                       # Απόρριψη
    
    # Fulfillment actions
    SHIP = "ship"                          # Αποστολή
    RECEIVE = "receive"                     # Παραλαβή
    DELIVER = "deliver"                     # Παράδοση
    
    # Payment actions
    RECORD_PAYMENT = "record_payment"       # Καταγραφή πληρωμής
    MARK_OVERDUE = "mark_overdue"          # Σήμανση ληξιπρόθεσμου
    
    # Conversion actions
    CONVERT_TO_INVOICE = "convert_to_invoice"         # Μετατροπή σε τιμολόγιο
    CONVERT_TO_CREDIT_NOTE = "convert_to_credit_note" # Μετατροπή σε πιστωτικό
    CONVERT_TO_DEBIT_NOTE = "convert_to_debit_note"   # Μετατροπή σε χρεωστικό
    CREATE_DELIVERY_NOTE = "create_delivery_note"     # Δημιουργία δελτίου αποστολής
    CREATE_SALES_ORDER = "create_sales_order"         # Δημιουργία παραγγελίας
    
    # Closure actions
    CANCEL = "cancel"                       # Ακύρωση
    CLOSE = "close"                         # Κλείσιμο
    EXPIRE = "expire"                       # Λήξη
    DECLINE = "decline"                     # Απόρριψη
    REFUND = "refund"                       # Επιστροφή
    
    # Correction actions
    APPLY_TO_INVOICE = "apply_to_invoice"   # Εφαρμογή σε τιμολόγιο
    CORRECT = "correct"                     # Διόρθωση


class StateTransitionRule(Base):
    """
    Rules defining valid state transitions for each document type
    Based on Greek business practices and legal requirements
    """
    __tablename__ = "state_transition_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document type and state transition
    document_type = Column(String(50), nullable=False, index=True)  # From InvoiceType enum
    from_state = Column(Enum(DocumentState), nullable=False, index=True)
    to_state = Column(Enum(DocumentState), nullable=False, index=True)
    action = Column(Enum(DocumentAction), nullable=False, index=True)
    
    # Rule configuration
    is_active = Column(Boolean, default=True, nullable=False)
    is_automatic = Column(Boolean, default=False, nullable=False)  # Can be triggered automatically
    requires_approval = Column(Boolean, default=False, nullable=False)
    
    # Conditions for transition
    conditions = Column(JSON, default=dict)  # Business rules and conditions
    
    # Greek business rules
    greek_business_rules = Column(JSON, default=dict)
    aade_requirements = Column(JSON, default=dict)
    
    # Metadata
    description = Column(Text)
    greek_description = Column(Text)
    legal_reference = Column(String(500))
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Ensure unique transitions
    __table_args__ = (
        UniqueConstraint('document_type', 'from_state', 'to_state', 'action', name='uq_transition_rule'),
        Index('idx_transition_document_type', 'document_type'),
        Index('idx_transition_from_state', 'from_state'),
        Index('idx_transition_to_state', 'to_state'),
        Index('idx_transition_action', 'action'),
    )


class DocumentWorkflowInstance(Base):
    """
    Tracks the current state and workflow progress for each document
    """
    __tablename__ = "document_workflow_instances"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document reference
    document_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), nullable=False, index=True)
    document_type = Column(String(50), nullable=False, index=True)
    
    # Current state
    current_state = Column(Enum(DocumentState), nullable=False, index=True)
    previous_state = Column(Enum(DocumentState), index=True)
    
    # Workflow metadata
    workflow_started_at = Column(DateTime, server_default=func.now(), nullable=False)
    workflow_completed_at = Column(DateTime)
    is_completed = Column(Boolean, default=False, nullable=False)
    
    # Next allowed actions (computed)
    next_actions = Column(JSON, default=list)  # List of allowed actions
    
    # Workflow context
    workflow_context = Column(JSON, default=dict)  # Additional context data
    
    # Relationships
    document = relationship("Invoice", back_populates="workflow_instance")
    state_history = relationship("DocumentStateHistory", back_populates="workflow_instance", cascade="all, delete-orphan")
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_workflow_document', 'document_id'),
        Index('idx_workflow_current_state', 'current_state'),
        Index('idx_workflow_type', 'document_type'),
        Index('idx_workflow_completed', 'is_completed'),
    )


class DocumentStateHistory(Base):
    """
    Audit trail of all state transitions for each document
    Complete history of document lifecycle
    """
    __tablename__ = "document_state_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Workflow reference
    workflow_instance_id = Column(UUID(as_uuid=True), ForeignKey('document_workflow_instances.id'), nullable=False, index=True)
    
    # State transition details
    from_state = Column(Enum(DocumentState), index=True)
    to_state = Column(Enum(DocumentState), nullable=False, index=True)
    action = Column(Enum(DocumentAction), nullable=False, index=True)
    
    # Transition metadata
    transition_date = Column(DateTime, server_default=func.now(), nullable=False)
    triggered_by = Column(String(50))  # 'user', 'system', 'automatic'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    
    # Transition context
    transition_data = Column(JSON, default=dict)  # Additional data for the transition
    notes = Column(Text)
    greek_notes = Column(Text)
    
    # Validation results
    validation_passed = Column(Boolean, default=True, nullable=False)
    validation_errors = Column(JSON, default=list)
    
    # Greek compliance
    aade_submission_triggered = Column(Boolean, default=False, nullable=False)
    aade_submission_id = Column(String(100))
    
    # Relationships
    workflow_instance = relationship("DocumentWorkflowInstance", back_populates="state_history")
    user = relationship("User", foreign_keys=[user_id])
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_state_history_workflow', 'workflow_instance_id'),
        Index('idx_state_history_date', 'transition_date'),
        Index('idx_state_history_action', 'action'),
        Index('idx_state_history_user', 'user_id'),
    )


class DocumentAutomationRule(Base):
    """
    Rules for automatic state transitions and workflow automation
    Greek business-specific automation rules
    """
    __tablename__ = "document_automation_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Rule identification
    rule_name = Column(String(200), nullable=False)
    rule_code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    greek_description = Column(Text)
    
    # Rule scope
    document_types = Column(JSON, default=list)  # List of document types this rule applies to
    business_entity_types = Column(JSON, default=list)  # Business entity types
    
    # Trigger conditions
    trigger_type = Column(String(50), nullable=False)  # 'time_based', 'event_based', 'condition_based'
    trigger_conditions = Column(JSON, default=dict)
    
    # Action to perform
    action = Column(Enum(DocumentAction), nullable=False)
    action_parameters = Column(JSON, default=dict)
    
    # Greek business rules
    greek_business_rules = Column(JSON, default=dict)
    aade_integration = Column(JSON, default=dict)
    
    # Rule status
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=100)  # Higher number = higher priority
    
    # Execution tracking
    last_executed_at = Column(DateTime)
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Indexes
    __table_args__ = (
        Index('idx_automation_rule_active', 'is_active'),
        Index('idx_automation_rule_trigger_type', 'trigger_type'),
        Index('idx_automation_rule_priority', 'priority'),
    )


class GreekDocumentWorkflowTemplate(Base):
    """
    Pre-configured workflow templates for different Greek document types
    Based on Greek business practices and legal requirements
    """
    __tablename__ = "greek_document_workflow_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template identification
    template_name = Column(String(200), nullable=False)
    template_code = Column(String(50), nullable=False, unique=True)
    document_type = Column(String(50), nullable=False, index=True)
    
    # Template description
    description = Column(Text)
    greek_description = Column(Text)
    
    # Workflow configuration
    workflow_definition = Column(JSON, nullable=False)  # Complete workflow definition
    initial_state = Column(Enum(DocumentState), nullable=False)
    final_states = Column(JSON, nullable=False)  # List of possible final states
    
    # Greek business configuration
    greek_business_rules = Column(JSON, default=dict)
    aade_integration_points = Column(JSON, default=dict)
    
    # Template metadata
    is_system_template = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    usage_count = Column(Integer, default=0)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_workflow_template_document_type', 'document_type'),
        Index('idx_workflow_template_active', 'is_active'),
    )


# Greek Document Type Workflow Definitions
GREEK_DOCUMENT_WORKFLOWS = {
    # 1. Προτιμολόγιο (Proforma Invoice)
    "proforma": {
        "states": [DocumentState.DRAFT, DocumentState.ISSUED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.ISSUED, "action": DocumentAction.FINALIZE},
            {"from": DocumentState.ISSUED, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ],
        "conversions": [
            {"action": DocumentAction.CONVERT_TO_INVOICE, "target_type": "sales_invoice"}
        ]
    },
    
    # 2. Sales Order (Δελτίο Παραγγελίας)
    "sales_order": {
        "states": [DocumentState.DRAFT, DocumentState.CONFIRMED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.CONFIRMED, "action": DocumentAction.CONFIRM},
            {"from": DocumentState.CONFIRMED, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
            {"from": DocumentState.DRAFT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ],
        "conversions": [
            {"action": DocumentAction.CREATE_DELIVERY_NOTE, "target_type": "delivery_note"}
        ]
    },
    
    # 3. Order Confirmation (Επιβεβαίωση Παραγγελίας)
    "order_confirmation": {
        "states": [DocumentState.DRAFT, DocumentState.SENT, DocumentState.CONFIRMED, DocumentState.EXPIRED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.SENT, "action": DocumentAction.SEND},
            {"from": DocumentState.SENT, "to": DocumentState.CONFIRMED, "action": DocumentAction.CONFIRM},
            {"from": DocumentState.SENT, "to": DocumentState.EXPIRED, "action": DocumentAction.EXPIRE},
            {"from": DocumentState.SENT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 4. Purchase Order (Παραγγελία Προμηθευτή)
    "purchase_order": {
        "states": [DocumentState.DRAFT, DocumentState.SENT, DocumentState.PARTIALLY_RECEIVED, DocumentState.FULLY_RECEIVED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.SENT, "action": DocumentAction.SEND},
            {"from": DocumentState.SENT, "to": DocumentState.PARTIALLY_RECEIVED, "action": DocumentAction.RECEIVE},
            {"from": DocumentState.SENT, "to": DocumentState.FULLY_RECEIVED, "action": DocumentAction.RECEIVE},
            {"from": DocumentState.PARTIALLY_RECEIVED, "to": DocumentState.FULLY_RECEIVED, "action": DocumentAction.RECEIVE},
            {"from": DocumentState.SENT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 5. Delivery Note (Δελτίο Αποστολής)
    "delivery_note": {
        "states": [DocumentState.DRAFT, DocumentState.SHIPPED, DocumentState.DELIVERED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.SHIPPED, "action": DocumentAction.FINALIZE},
            {"from": DocumentState.SHIPPED, "to": DocumentState.DELIVERED, "action": DocumentAction.DELIVER},
            {"from": DocumentState.SHIPPED, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ],
        "conversions": [
            {"action": DocumentAction.CONVERT_TO_INVOICE, "target_type": "sales_invoice"}
        ]
    },
    
    # 6. Sales Invoice (Τιμολόγιο Πώλησης)
    "sales_invoice": {
        "states": [DocumentState.DRAFT, DocumentState.OPEN, DocumentState.PARTIALLY_PAID, DocumentState.PAID, DocumentState.OVERDUE, DocumentState.CREDITED, DocumentState.DEBITED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.OPEN, "action": DocumentAction.ISSUE},
            {"from": DocumentState.OPEN, "to": DocumentState.PARTIALLY_PAID, "action": DocumentAction.RECORD_PAYMENT},
            {"from": DocumentState.OPEN, "to": DocumentState.PAID, "action": DocumentAction.RECORD_PAYMENT},
            {"from": DocumentState.PARTIALLY_PAID, "to": DocumentState.PAID, "action": DocumentAction.RECORD_PAYMENT},
            {"from": DocumentState.OPEN, "to": DocumentState.OVERDUE, "action": DocumentAction.MARK_OVERDUE},
            {"from": DocumentState.OPEN, "to": DocumentState.CREDITED, "action": DocumentAction.CONVERT_TO_CREDIT_NOTE},
            {"from": DocumentState.OPEN, "to": DocumentState.DEBITED, "action": DocumentAction.CONVERT_TO_DEBIT_NOTE},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 7. Simplified Invoice (Απλοποιημένο Τιμολόγιο)
    "simplified_invoice": {
        "states": [DocumentState.DRAFT, DocumentState.PAID, DocumentState.OPEN, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.PAID, "action": DocumentAction.ISSUE},
            {"from": DocumentState.DRAFT, "to": DocumentState.OPEN, "action": DocumentAction.ISSUE},
            {"from": DocumentState.OPEN, "to": DocumentState.PAID, "action": DocumentAction.RECORD_PAYMENT},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 8. Receipt (Απόδειξη Λιανικής Πώλησης)
    "receipt": {
        "states": [DocumentState.DRAFT, DocumentState.CLOSED, DocumentState.REFUNDED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.CLOSED, "action": DocumentAction.ISSUE},
            {"from": DocumentState.CLOSED, "to": DocumentState.REFUNDED, "action": DocumentAction.REFUND},
            {"from": DocumentState.CLOSED, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 9. Credit Note (Πιστωτικό Τιμολόγιο)
    "credit_note": {
        "states": [DocumentState.DRAFT, DocumentState.OPEN, DocumentState.APPLIED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.OPEN, "action": DocumentAction.ISSUE},
            {"from": DocumentState.OPEN, "to": DocumentState.APPLIED, "action": DocumentAction.APPLY_TO_INVOICE},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 10. Debit Note (Χρεωστικό Τιμολόγιο)
    "debit_note": {
        "states": [DocumentState.DRAFT, DocumentState.OPEN, DocumentState.APPLIED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.OPEN, "action": DocumentAction.ISSUE},
            {"from": DocumentState.OPEN, "to": DocumentState.APPLIED, "action": DocumentAction.APPLY_TO_INVOICE},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 11. Return Note (Δελτίο Επιστροφής Εμπορευμάτων)
    "return_note": {
        "states": [DocumentState.DRAFT, DocumentState.FULLY_RECEIVED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.FULLY_RECEIVED, "action": DocumentAction.ISSUE},
            {"from": DocumentState.FULLY_RECEIVED, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
            {"from": DocumentState.DRAFT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ],
        "conversions": [
            {"action": DocumentAction.CONVERT_TO_CREDIT_NOTE, "target_type": "credit_note"}
        ]
    },
    
    # 12. Request for Quotation (RFQ)
    "request_for_quotation": {
        "states": [DocumentState.DRAFT, DocumentState.SENT, DocumentState.QUOTED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.SENT, "action": DocumentAction.SEND},
            {"from": DocumentState.SENT, "to": DocumentState.QUOTED, "action": DocumentAction.CONFIRM},
            {"from": DocumentState.DRAFT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
            {"from": DocumentState.SENT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
            {"from": DocumentState.QUOTED, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 13. Quotation (Προσφορά)
    "sales_quotation": {
        "states": [DocumentState.DRAFT, DocumentState.OPEN, DocumentState.ACCEPTED, DocumentState.DECLINED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.OPEN, "action": DocumentAction.ISSUE},
            {"from": DocumentState.OPEN, "to": DocumentState.ACCEPTED, "action": DocumentAction.ACCEPT},
            {"from": DocumentState.OPEN, "to": DocumentState.DECLINED, "action": DocumentAction.DECLINE},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ],
        "conversions": [
            {"action": DocumentAction.CREATE_SALES_ORDER, "target_type": "sales_order"}
        ]
    },
    
    # 14. Internal Transfer Note (Παραστατικό Εσωτερικής Μετακίνησης)
    "internal_transfer": {
        "states": [DocumentState.DRAFT, DocumentState.IN_TRANSIT, DocumentState.COMPLETED, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.DRAFT, "to": DocumentState.IN_TRANSIT, "action": DocumentAction.ISSUE},
            {"from": DocumentState.IN_TRANSIT, "to": DocumentState.COMPLETED, "action": DocumentAction.RECEIVE},
            {"from": DocumentState.DRAFT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
            {"from": DocumentState.IN_TRANSIT, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 15. Self-billing Invoice (Αυτοτιμολόγηση)
    "self_billing": {
        "states": [DocumentState.OPEN, DocumentState.PAID, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.OPEN, "to": DocumentState.PAID, "action": DocumentAction.RECORD_PAYMENT},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    },
    
    # 16. E-Invoice (Ηλεκτρονικό Τιμολόγιο)
    "e_invoice": {
        "states": [DocumentState.OPEN, DocumentState.PAID, DocumentState.CANCELLED],
        "transitions": [
            {"from": DocumentState.OPEN, "to": DocumentState.PAID, "action": DocumentAction.RECORD_PAYMENT},
            {"from": DocumentState.OPEN, "to": DocumentState.CANCELLED, "action": DocumentAction.CANCEL},
        ]
    }
} 