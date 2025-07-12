"""
Invoice models for Greek ERP/CRM System
Supports AADE compliance and comprehensive Greek business document types (parastatika) support
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal
from datetime import datetime, timedelta

from ..core.database import Base


class InvoiceType(enum.Enum):
    """Document types (parastatika) according to Greek business practices"""
    # Legal documents (νόμιμα παραστατικά)
    SALES_INVOICE = "sales_invoice"           # Τιμολόγιο Πώλησης
    RECEIPT = "receipt"                       # Απόδειξη Λιανικής Πώλησης
    CREDIT_NOTE = "credit_note"              # Πιστωτικό Τιμολόγιο
    DEBIT_NOTE = "debit_note"                # Χρεωστικό Τιμολόγιο
    PROFORMA = "proforma"                    # Προτιμολόγιο
    DELIVERY_NOTE = "delivery_note"          # Δελτίο Αποστολής
    SIMPLIFIED_INVOICE = "simplified_invoice" # Απλοποιημένο Τιμολόγιο
    SELF_BILLING = "self_billing"            # Αυτο-τιμολόγηση
    E_INVOICE = "e_invoice"                  # Ηλεκτρονικό Τιμολόγιο (UBL)
    
    # Business workflow documents (εσωτερικά έγγραφα)
    SALES_ORDER = "sales_order"             # Δελτίο Παραγγελίας / Παραγγελιοληψία
    ORDER_CONFIRMATION = "order_confirmation" # Επιβεβαίωση Παραγγελίας
    PURCHASE_ORDER = "purchase_order"        # Παραγγελία Προμηθευτή
    REQUEST_FOR_QUOTATION = "request_for_quotation" # Αίτημα Προσφοράς
    SALES_QUOTATION = "sales_quotation"     # Προσφορά / Προσυμφωνητική Τιμολόγηση
    RETURN_NOTE = "return_note"             # Δελτίο Επιστροφής Εμπορευμάτων
    INTERNAL_TRANSFER = "internal_transfer"  # Παραστατικό Εσωτερικής Μετακίνησης


class InvoiceStatus(enum.Enum):
    """Document status"""
    DRAFT = "draft"                          # Προσχέδιο
    PENDING = "pending"                      # Εκκρεμές
    APPROVED = "approved"                    # Εγκεκριμένο
    SENT = "sent"                           # Αποσταλμένο
    ACCEPTED = "accepted"                   # Αποδεκτό
    REJECTED = "rejected"                   # Απορριφθέν
    PAID = "paid"                           # Πληρωμένο
    PARTIALLY_PAID = "partially_paid"        # Μερικώς Πληρωμένο
    OVERDUE = "overdue"                     # Ληξιπρόθεσμο
    CANCELLED = "cancelled"                  # Ακυρωμένο
    REFUNDED = "refunded"                   # Επιστραμμένο
    COMPLETED = "completed"                  # Ολοκληρωμένο
    DELIVERED = "delivered"                  # Παραδόθηκε


class PaymentMethod(enum.Enum):
    """Payment methods according to Greek tax law"""
    CASH = "cash"                           # Μετρητά
    CARD = "card"                           # Κάρτα
    BANK_TRANSFER = "bank_transfer"         # Τραπεζική Μεταφορά
    CHECK = "check"                         # Επιταγή
    CREDIT = "credit"                       # Πίστωση
    PAYPAL = "paypal"                       # PayPal
    CRYPTO = "crypto"                       # Κρυπτονόμισμα
    OTHER = "other"                         # Άλλο


class AADEStatus(enum.Enum):
    """AADE submission status"""
    NOT_SUBMITTED = "not_submitted"          # Δεν έχει υποβληθεί
    PENDING = "pending"                      # Εκκρεμής υποβολή
    SUBMITTED = "submitted"                  # Υποβλήθηκε
    ACCEPTED = "accepted"                    # Εγκρίθηκε
    REJECTED = "rejected"                    # Απορρίφθηκε
    ERROR = "error"                          # Σφάλμα υποβολής


class Invoice(Base):
    """
    Invoice model for Greek ERP/CRM system
    Supports AADE compliance and comprehensive Greek business document types (parastatika)
    """
    __tablename__ = "invoices"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (stored in company's database)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Document identification
    invoice_number = Column(String(50), nullable=False, unique=True, index=True)
    series = Column(String(20), nullable=False, default="INV")
    sequence_number = Column(Integer, nullable=False)
    
    # Document type and status
    invoice_type = Column(Enum(InvoiceType), nullable=False, default=InvoiceType.SALES_INVOICE)
    status = Column(Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.DRAFT)
    
    # Greek business compliance
    is_legal_document = Column(Boolean, nullable=False, default=True)  # Νόμιμο παραστατικό
    affects_vat = Column(Boolean, nullable=False, default=True)        # Επηρεάζει ΦΠΑ
    affects_inventory = Column(Boolean, nullable=False, default=True)  # Επηρεάζει απόθεμα
    
    # Business entity information (customer, client, etc.)
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    
    # Document dates
    issue_date = Column(DateTime, nullable=False, default=func.now())
    due_date = Column(DateTime, nullable=False)
    service_date = Column(DateTime)  # Date of service delivery
    delivery_date = Column(DateTime)  # Actual delivery date
    
    # Document workflow - related documents
    parent_document_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), index=True)  # Parent document
    original_document_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), index=True)  # Original document for corrections
    
    # Financial information
    subtotal = Column(Numeric(15, 2), nullable=False, default=0)
    total_vat = Column(Numeric(15, 2), nullable=False, default=0)
    total_amount = Column(Numeric(15, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    discount_percentage = Column(Numeric(5, 2), default=0)
    
    # Payment information
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.BANK_TRANSFER)
    payment_terms = Column(String(100))
    paid_amount = Column(Numeric(15, 2), default=0)
    outstanding_amount = Column(Numeric(15, 2), default=0)
    
    # Currency
    currency = Column(String(3), nullable=False, default="EUR")
    exchange_rate = Column(Numeric(10, 6), default=1.0)
    
    # Notes and references
    notes = Column(Text)
    internal_notes = Column(Text)
    reference_number = Column(String(100))
    purchase_order = Column(String(100))
    project_number = Column(String(100))
    
    # Approval workflow
    approved_by = Column(UUID(as_uuid=True))
    approved_at = Column(DateTime)
    approval_notes = Column(Text)
    
    # AADE (Greek Tax Authority) integration
    aade_status = Column(Enum(AADEStatus), default=AADEStatus.NOT_SUBMITTED)
    aade_submission_date = Column(DateTime)
    aade_response = Column(JSON)
    aade_mark = Column(String(100))  # AADE unique identifier
    aade_qr_code = Column(String(500))  # QR code for validation
    aade_cancellation_mark = Column(String(100))
    
    # Greek compliance fields
    mydata_invoice_type = Column(String(20))  # MyDATA invoice type code
    vat_exemption_reason = Column(String(255))
    reverse_charge = Column(Boolean, default=False)
    
    # UBL/XML support for e-invoicing
    ubl_version = Column(String(10))  # UBL version (e.g., "2.1")
    xml_content = Column(Text)        # Generated XML content
    digital_signature = Column(Text)  # Digital signature for e-invoices
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    business_entity = relationship("BusinessEntity", back_populates="invoices")
    invoice_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    parent_document = relationship("Invoice", remote_side=[id], foreign_keys=[parent_document_id])
    original_document = relationship("Invoice", remote_side=[id], foreign_keys=[original_document_id])
    child_documents = relationship("Invoice", foreign_keys=[parent_document_id])
    workflow_instance = relationship("DocumentWorkflowInstance", back_populates="document", uselist=False)
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_invoice_company', 'company_id'),
        Index('idx_invoice_number', 'invoice_number'),
        Index('idx_invoice_business_entity', 'business_entity_id'),
        Index('idx_invoice_type', 'invoice_type'),
        Index('idx_invoice_status', 'status'),
        Index('idx_invoice_issue_date', 'issue_date'),
        Index('idx_invoice_due_date', 'due_date'),
        Index('idx_invoice_aade_status', 'aade_status'),
        Index('idx_invoice_series_sequence', 'series', 'sequence_number'),
        Index('idx_invoice_parent', 'parent_document_id'),
        Index('idx_invoice_original', 'original_document_id'),
        Index('idx_invoice_legal', 'is_legal_document'),
        Index('idx_invoice_affects_vat', 'affects_vat'),
        Index('idx_invoice_affects_inventory', 'affects_inventory'),
    )
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.invoice_number}', type='{self.invoice_type.value}', amount={self.total_amount})>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue"""
        return self.due_date < datetime.now() and self.status not in [InvoiceStatus.PAID, InvoiceStatus.CANCELLED]
    
    @property
    def is_paid(self) -> bool:
        """Check if invoice is fully paid"""
        return self.status == InvoiceStatus.PAID or self.paid_amount >= self.total_amount
    
    @property
    def is_partially_paid(self) -> bool:
        """Check if invoice is partially paid"""
        return self.paid_amount > 0 and self.paid_amount < self.total_amount
    
    @property
    def days_overdue(self) -> int:
        """Calculate days overdue"""
        if not self.is_overdue:
            return 0
        return (datetime.now() - self.due_date).days
    
    @property
    def payment_status(self) -> str:
        """Get payment status string"""
        if self.is_paid:
            return "paid"
        elif self.is_partially_paid:
            return "partially_paid"
        elif self.is_overdue:
            return "overdue"
        else:
            return "unpaid"
    
    @property
    def document_type_info(self) -> Dict[str, Any]:
        """Get document type information"""
        type_info = {
            InvoiceType.SALES_INVOICE: {
                "greek_name": "Τιμολόγιο Πώλησης",
                "legal_reference": "Ν. Δ. 186/1992",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.RECEIPT: {
                "greek_name": "Απόδειξη Λιανικής Πώλησης",
                "legal_reference": "Ν. 4492/2017 (up to €500 retail)",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.CREDIT_NOTE: {
                "greek_name": "Πιστωτικό Τιμολόγιο",
                "legal_reference": "Διορθώνει/μειώνει τιμολόγιο πώλησης",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.DEBIT_NOTE: {
                "greek_name": "Χρεωστικό Τιμολόγιο",
                "legal_reference": "Προσθέτει χρέωση σε υπάρχον τιμολόγιο",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": False,
                "requires_aade": True
            },
            InvoiceType.PROFORMA: {
                "greek_name": "Προτιμολόγιο",
                "legal_reference": "Προσφορά, δεν εκπίπτει ΦΠΑ",
                "is_legal": False,
                "affects_vat": False,
                "affects_inventory": False,
                "requires_aade": False
            },
            InvoiceType.DELIVERY_NOTE: {
                "greek_name": "Δελτίο Αποστολής",
                "legal_reference": "Συνοδεύει παράδοση αγαθών",
                "is_legal": True,
                "affects_vat": False,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.SIMPLIFIED_INVOICE: {
                "greek_name": "Απλοποιημένο Τιμολόγιο",
                "legal_reference": "Έως €1.500 ή €500 (ανάλογα είδος υπηρεσίας)",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.SALES_ORDER: {
                "greek_name": "Δελτίο Παραγγελίας / Παραγγελιοληψία",
                "legal_reference": "Πιστοποιεί την παραγγελία πελάτη (προ-παραστατικό)",
                "is_legal": False,
                "affects_vat": False,
                "affects_inventory": False,
                "requires_aade": False
            },
            InvoiceType.ORDER_CONFIRMATION: {
                "greek_name": "Επιβεβαίωση Παραγγελίας",
                "legal_reference": "Επιβεβαιώνει εκ μέρους προμηθευτή",
                "is_legal": False,
                "affects_vat": False,
                "affects_inventory": False,
                "requires_aade": False
            },
            InvoiceType.PURCHASE_ORDER: {
                "greek_name": "Παραγγελία Προμηθευτή",
                "legal_reference": "Έγγραφο αγοραστή· δεν επιβάλλεται από νόμο",
                "is_legal": False,
                "affects_vat": False,
                "affects_inventory": False,
                "requires_aade": False
            },
            InvoiceType.REQUEST_FOR_QUOTATION: {
                "greek_name": "Αίτημα Προσφοράς",
                "legal_reference": "Αρχικό στάδιο διαπραγμάτευσης",
                "is_legal": False,
                "affects_vat": False,
                "affects_inventory": False,
                "requires_aade": False
            },
            InvoiceType.SALES_QUOTATION: {
                "greek_name": "Προσφορά / Προσυμφωνητική Τιμολόγηση",
                "legal_reference": "Προσφορά τιμών, δεν επιβάλλει ΦΠΑ",
                "is_legal": False,
                "affects_vat": False,
                "affects_inventory": False,
                "requires_aade": False
            },
            InvoiceType.RETURN_NOTE: {
                "greek_name": "Δελτίο Επιστροφής Εμπορευμάτων",
                "legal_reference": "Καταγραφή επιστροφής από πελάτη",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.INTERNAL_TRANSFER: {
                "greek_name": "Παραστατικό Εσωτερικής Μετακίνησης",
                "legal_reference": "Μετακίνηση αγαθών μεταξύ αποθηκών",
                "is_legal": True,
                "affects_vat": False,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.SELF_BILLING: {
                "greek_name": "Αυτο-τιμολόγηση",
                "legal_reference": "Εφαρμόζεται σε συγκεκριμένες βιομηχανίες",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            },
            InvoiceType.E_INVOICE: {
                "greek_name": "Ηλεκτρονικό Τιμολόγιο",
                "legal_reference": "e-Invoicing με UBL 2.1 (myDATA, PEPPOL κ.λπ.)",
                "is_legal": True,
                "affects_vat": True,
                "affects_inventory": True,
                "requires_aade": True
            }
        }
        return type_info.get(self.invoice_type, {})
    
    def calculate_totals(self) -> None:
        """Calculate invoice totals from line items"""
        subtotal = Decimal('0.00')
        total_vat = Decimal('0.00')
        
        for item in self.invoice_items:
            subtotal += item.line_total
            total_vat += item.vat_amount
        
        # Apply discount
        if self.discount_percentage > 0:
            discount = subtotal * (self.discount_percentage / 100)
            subtotal -= discount
            self.discount_amount = discount
        elif self.discount_amount > 0:
            subtotal -= self.discount_amount
        
        self.subtotal = subtotal
        self.total_vat = total_vat
        self.total_amount = subtotal + total_vat
        self.outstanding_amount = self.total_amount - self.paid_amount
    
    def add_payment(self, amount: Decimal, payment_date: datetime = None) -> None:
        """Add payment to invoice"""
        self.paid_amount += amount
        self.outstanding_amount = self.total_amount - self.paid_amount
        
        # Update status based on payment
        if self.paid_amount >= self.total_amount:
            self.status = InvoiceStatus.PAID
        elif self.paid_amount > 0:
            self.status = InvoiceStatus.PARTIALLY_PAID
        else:
            self.status = InvoiceStatus.PENDING
    
    def can_be_edited(self) -> bool:
        """Check if document can be edited"""
        return self.status in [InvoiceStatus.DRAFT, InvoiceStatus.PENDING]
    
    def can_be_cancelled(self) -> bool:
        """Check if document can be cancelled"""
        return self.status not in [InvoiceStatus.PAID, InvoiceStatus.CANCELLED, InvoiceStatus.REFUNDED]
    
    def can_be_submitted_to_aade(self) -> bool:
        """Check if document can be submitted to AADE"""
        doc_info = self.document_type_info
        return (doc_info.get('requires_aade', False) and 
                self.aade_status == AADEStatus.NOT_SUBMITTED and 
                self.status not in [InvoiceStatus.DRAFT, InvoiceStatus.CANCELLED])
    
    def mark_as_submitted_to_aade(self, aade_mark: str, qr_code: str = None) -> None:
        """Mark document as submitted to AADE"""
        self.aade_status = AADEStatus.SUBMITTED
        self.aade_submission_date = func.now()
        self.aade_mark = aade_mark
        if qr_code:
            self.aade_qr_code = qr_code
    
    def get_workflow_next_steps(self) -> List[str]:
        """Get possible next steps in document workflow"""
        workflows = {
            InvoiceType.REQUEST_FOR_QUOTATION: [InvoiceType.SALES_QUOTATION],
            InvoiceType.SALES_QUOTATION: [InvoiceType.SALES_ORDER],
            InvoiceType.SALES_ORDER: [InvoiceType.DELIVERY_NOTE, InvoiceType.SALES_INVOICE],
            InvoiceType.DELIVERY_NOTE: [InvoiceType.SALES_INVOICE],
            InvoiceType.SALES_INVOICE: [InvoiceType.CREDIT_NOTE, InvoiceType.DEBIT_NOTE],
            InvoiceType.PURCHASE_ORDER: [InvoiceType.DELIVERY_NOTE],
        }
        return [step.value for step in workflows.get(self.invoice_type, [])]
    
    def to_dict(self, include_items: bool = True, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert invoice to dictionary for API responses"""
        doc_info = self.document_type_info
        
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "invoice_number": self.invoice_number,
            "series": self.series,
            "sequence_number": self.sequence_number,
            "invoice_type": self.invoice_type.value,
            "status": self.status.value,
            "business_entity_id": str(self.business_entity_id),
            "issue_date": self.issue_date.isoformat() if self.issue_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "service_date": self.service_date.isoformat() if self.service_date else None,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "parent_document_id": str(self.parent_document_id) if self.parent_document_id else None,
            "original_document_id": str(self.original_document_id) if self.original_document_id else None,
            "subtotal": float(self.subtotal),
            "total_vat": float(self.total_vat),
            "total_amount": float(self.total_amount),
            "discount_amount": float(self.discount_amount) if self.discount_amount else 0,
            "discount_percentage": float(self.discount_percentage) if self.discount_percentage else 0,
            "payment_method": self.payment_method.value if self.payment_method else None,
            "payment_terms": self.payment_terms,
            "paid_amount": float(self.paid_amount),
            "outstanding_amount": float(self.outstanding_amount),
            "currency": self.currency,
            "exchange_rate": float(self.exchange_rate),
            "notes": self.notes,
            "reference_number": self.reference_number,
            "purchase_order": self.purchase_order,
            "project_number": self.project_number,
            "approved_by": str(self.approved_by) if self.approved_by else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "aade_status": self.aade_status.value,
            "aade_submission_date": self.aade_submission_date.isoformat() if self.aade_submission_date else None,
            "aade_mark": self.aade_mark,
            "aade_qr_code": self.aade_qr_code,
            "is_legal_document": self.is_legal_document,
            "affects_vat": self.affects_vat,
            "affects_inventory": self.affects_inventory,
            "document_type_info": doc_info,
            "workflow_next_steps": self.get_workflow_next_steps(),
            "is_overdue": self.is_overdue,
            "is_paid": self.is_paid,
            "is_partially_paid": self.is_partially_paid,
            "days_overdue": self.days_overdue,
            "payment_status": self.payment_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_items:
            data["items"] = [item.to_dict() for item in self.invoice_items]
        
        if include_sensitive:
            data.update({
                "internal_notes": self.internal_notes,
                "approval_notes": self.approval_notes,
                "aade_response": self.aade_response,
                "aade_cancellation_mark": self.aade_cancellation_mark,
                "mydata_invoice_type": self.mydata_invoice_type,
                "vat_exemption_reason": self.vat_exemption_reason,
                "reverse_charge": self.reverse_charge,
                "ubl_version": self.ubl_version,
                "xml_content": self.xml_content,
                "digital_signature": self.digital_signature,
                "created_by": str(self.created_by) if self.created_by else None,
                "updated_by": str(self.updated_by) if self.updated_by else None
            })
        
        return data


class InvoiceItem(Base):
    """
    Invoice item model for Greek ERP/CRM system
    Represents line items in invoices with VAT compliance
    """
    __tablename__ = "invoice_items"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Invoice association
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), nullable=False, index=True)
    
    # Product association
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), index=True)
    
    # Line item details
    line_number = Column(Integer, nullable=False)
    product_code = Column(String(50))
    product_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Quantities and units
    quantity = Column(Numeric(10, 3), nullable=False)
    unit_of_measure = Column(String(20))
    
    # Pricing
    unit_price = Column(Numeric(15, 4), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    line_total = Column(Numeric(15, 2), nullable=False)
    
    # VAT information
    vat_category = Column(String(20), nullable=False)
    vat_rate = Column(Numeric(5, 2), nullable=False)
    vat_amount = Column(Numeric(15, 2), nullable=False)
    vat_exemption_reason = Column(String(255))
    
    # Greek compliance
    mydata_classification = Column(String(50))  # MyDATA classification
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="invoice_items")
    product = relationship("Product", back_populates="invoice_items")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_invoice_item_invoice', 'invoice_id'),
        Index('idx_invoice_item_product', 'product_id'),
        Index('idx_invoice_item_line_number', 'invoice_id', 'line_number'),
    )
    
    def __repr__(self):
        return f"<InvoiceItem(id={self.id}, product='{self.product_name}', quantity={self.quantity})>"
    
    def calculate_totals(self) -> None:
        """Calculate line item totals"""
        # Calculate base amount
        base_amount = self.quantity * self.unit_price
        
        # Apply discount
        if self.discount_percentage > 0:
            discount = base_amount * (self.discount_percentage / 100)
            base_amount -= discount
            self.discount_amount = discount
        elif self.discount_amount > 0:
            base_amount -= self.discount_amount
        
        # Calculate VAT
        if self.vat_rate > 0:
            self.vat_amount = base_amount * (self.vat_rate / 100)
        else:
            self.vat_amount = Decimal('0.00')
        
        # Set line total (excluding VAT as per Greek practice)
        self.line_total = base_amount
    
    @property
    def total_with_vat(self) -> Decimal:
        """Get total including VAT"""
        return self.line_total + self.vat_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert invoice item to dictionary for API responses"""
        return {
            "id": str(self.id),
            "invoice_id": str(self.invoice_id),
            "product_id": str(self.product_id) if self.product_id else None,
            "line_number": self.line_number,
            "product_code": self.product_code,
            "product_name": self.product_name,
            "description": self.description,
            "quantity": float(self.quantity),
            "unit_of_measure": self.unit_of_measure,
            "unit_price": float(self.unit_price),
            "discount_percentage": float(self.discount_percentage) if self.discount_percentage else 0,
            "discount_amount": float(self.discount_amount) if self.discount_amount else 0,
            "line_total": float(self.line_total),
            "vat_category": self.vat_category,
            "vat_rate": float(self.vat_rate),
            "vat_amount": float(self.vat_amount),
            "total_with_vat": float(self.total_with_vat),
            "vat_exemption_reason": self.vat_exemption_reason,
            "mydata_classification": self.mydata_classification,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 