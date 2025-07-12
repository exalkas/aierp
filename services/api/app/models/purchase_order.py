"""
Purchase Order models for Greek ERP/CRM System
Supplier ordering, procurement, and purchasing management
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


class PurchaseOrderStatus(enum.Enum):
    """Purchase order status"""
    DRAFT = "draft"                     # Προσχέδιο
    PENDING_APPROVAL = "pending_approval"  # Εκκρεμής έγκριση
    APPROVED = "approved"               # Εγκεκριμένη
    SENT = "sent"                       # Αποστάληκε
    ACKNOWLEDGED = "acknowledged"       # Επιβεβαιώθηκε από προμηθευτή
    IN_PRODUCTION = "in_production"     # Σε παραγωγή
    PARTIALLY_RECEIVED = "partially_received"  # Μερικώς παραλήφθηκε
    FULLY_RECEIVED = "fully_received"   # Πλήρως παραλήφθηκε
    CLOSED = "closed"                   # Κλείσιμο
    CANCELLED = "cancelled"             # Ακυρώθηκε


class PurchaseOrderType(enum.Enum):
    """Purchase order type"""
    STANDARD = "standard"               # Κανονική
    BLANKET = "blanket"                 # Γενική (για πολλαπλές παραδόσεις)
    CONTRACT = "contract"               # Συμβόλαιο
    PLANNED = "planned"                 # Προγραμματισμένη
    EMERGENCY = "emergency"             # Επείγουσα
    CONSIGNMENT = "consignment"         # Εμπορικό απόθεμα
    DROP_SHIP = "drop_ship"             # Άμεση αποστολή στον πελάτη


class PurchaseOrderPriority(enum.Enum):
    """Purchase order priority"""
    LOW = "low"           # Χαμηλή
    MEDIUM = "medium"     # Μεσαία
    HIGH = "high"         # Υψηλή
    URGENT = "urgent"     # Επείγον
    CRITICAL = "critical" # Κρίσιμη


class DeliveryTerm(enum.Enum):
    """Delivery terms (Incoterms)"""
    EXW = "exw"           # Ex Works
    FCA = "fca"           # Free Carrier
    CPT = "cpt"           # Carriage Paid To
    CIP = "cip"           # Carriage and Insurance Paid To
    DAP = "dap"           # Delivered at Place
    DPU = "dpu"           # Delivered at Place Unloaded
    DDP = "ddp"           # Delivered Duty Paid
    FAS = "fas"           # Free Alongside Ship
    FOB = "fob"           # Free on Board
    CFR = "cfr"           # Cost and Freight
    CIF = "cif"           # Cost, Insurance and Freight


class PurchaseOrder(Base):
    """
    Purchase Order model for Greek ERP/CRM system
    Represents orders to suppliers for products/services
    """
    __tablename__ = "purchase_orders"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Purchase order identification
    po_number = Column(String(50), nullable=False, unique=True, index=True)
    reference_number = Column(String(100))  # Internal reference
    requisition_number = Column(String(100))  # Originating requisition
    
    # Purchase order classification
    po_type = Column(Enum(PurchaseOrderType), nullable=False, default=PurchaseOrderType.STANDARD)
    status = Column(Enum(PurchaseOrderStatus), nullable=False, default=PurchaseOrderStatus.DRAFT)
    priority = Column(Enum(PurchaseOrderPriority), nullable=False, default=PurchaseOrderPriority.MEDIUM)
    
    # Supplier information (BusinessEntity with supplier role)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    supplier_contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'), index=True)
    
    # Dates
    order_date = Column(DateTime, nullable=False, default=func.now())
    requested_delivery_date = Column(DateTime)
    promised_delivery_date = Column(DateTime)
    expected_delivery_date = Column(DateTime)
    actual_delivery_date = Column(DateTime)
    
    # Financial information
    subtotal = Column(Numeric(15, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(15, 2), nullable=False, default=0)
    total_amount = Column(Numeric(15, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    discount_percentage = Column(Numeric(5, 2), default=0)
    
    # Currency and exchange
    currency = Column(String(3), nullable=False, default="EUR")
    exchange_rate = Column(Numeric(10, 6), default=1.0)
    
    # Delivery and shipping
    delivery_terms = Column(Enum(DeliveryTerm), default=DeliveryTerm.DDP)
    delivery_address = Column(Text)
    delivery_location_id = Column(UUID(as_uuid=True))  # Reference to warehouse/location
    shipping_method = Column(String(100))
    freight_terms = Column(String(100))
    
    # Payment terms
    payment_terms = Column(String(100))
    payment_due_days = Column(Integer, default=30)
    payment_method = Column(String(100))
    
    # Greek business compliance
    requires_invoice = Column(Boolean, default=True)
    requires_delivery_note = Column(Boolean, default=True)
    supplier_afm = Column(String(9))  # Cached from supplier
    supplier_vat_number = Column(String(20))
    
    # Approval workflow
    requires_approval = Column(Boolean, default=True)
    approval_limit = Column(Numeric(15, 2))
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approved_at = Column(DateTime)
    approval_notes = Column(Text)
    
    # Assignment and ownership
    buyer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    department = Column(String(100))
    cost_center = Column(String(100))
    project_id = Column(UUID(as_uuid=True))  # For project-based purchasing
    
    # Document tracking
    quote_reference = Column(String(100))  # Reference to supplier quote
    contract_reference = Column(String(100))  # Reference to contract
    
    # Quality and inspection
    requires_inspection = Column(Boolean, default=False)
    inspection_notes = Column(Text)
    quality_requirements = Column(Text)
    
    # Special instructions
    special_instructions = Column(Text)
    internal_notes = Column(Text)
    supplier_notes = Column(Text)  # Notes to be sent to supplier
    
    # Tracking and logistics
    tracking_number = Column(String(100))
    carrier = Column(String(100))
    expected_lead_time_days = Column(Integer)
    
    # Performance metrics
    on_time_delivery = Column(Boolean)
    delivery_performance_score = Column(Integer)  # 1-100
    quality_score = Column(Integer)  # 1-100
    supplier_rating = Column(Integer)  # 1-5
    
    # Receiving information
    goods_received_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    goods_received_date = Column(DateTime)
    receiving_notes = Column(Text)
    
    # Invoice matching
    invoice_received = Column(Boolean, default=False)
    invoice_matched = Column(Boolean, default=False)
    three_way_match_status = Column(String(50))  # PO + Receipt + Invoice matching
    
    # Closure information
    closed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    closed_date = Column(DateTime)
    closure_reason = Column(String(100))
    
    # Greek market specific
    emergency_procurement = Column(Boolean, default=False)
    single_source_justification = Column(Text)
    environmental_requirements = Column(Text)
    
    # Tags and custom fields
    tags = Column(JSON, default=list)
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    supplier = relationship("BusinessEntity", foreign_keys=[supplier_id])
    supplier_contact = relationship("Contact", foreign_keys=[supplier_contact_id])
    buyer = relationship("User", foreign_keys=[buyer_id])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    goods_received_by_user = relationship("User", foreign_keys=[goods_received_by])
    closed_by_user = relationship("User", foreign_keys=[closed_by])
    po_items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_po_company', 'company_id'),
        Index('idx_po_number', 'po_number'),
        Index('idx_po_supplier', 'supplier_id'),
        Index('idx_po_type', 'po_type'),
        Index('idx_po_status', 'status'),
        Index('idx_po_priority', 'priority'),
        Index('idx_po_buyer', 'buyer_id'),
        Index('idx_po_order_date', 'order_date'),
        Index('idx_po_delivery_date', 'requested_delivery_date'),
        Index('idx_po_total_amount', 'total_amount'),
        Index('idx_po_approved_by', 'approved_by'),
        Index('idx_po_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<PurchaseOrder(id={self.id}, po_number='{self.po_number}', supplier='{self.supplier_id}', status='{self.status.value}')>"
    
    @property
    def is_open(self) -> bool:
        """Check if PO is still open"""
        return self.status not in [PurchaseOrderStatus.FULLY_RECEIVED, PurchaseOrderStatus.CLOSED, PurchaseOrderStatus.CANCELLED]
    
    @property
    def is_overdue(self) -> bool:
        """Check if PO delivery is overdue"""
        if not self.expected_delivery_date or not self.is_open:
            return False
        return datetime.utcnow() > self.expected_delivery_date.replace(tzinfo=None)
    
    @property
    def days_until_delivery(self) -> Optional[int]:
        """Get days until expected delivery"""
        if not self.expected_delivery_date:
            return None
        delta = self.expected_delivery_date.replace(tzinfo=None) - datetime.utcnow()
        return delta.days
    
    @property
    def age_days(self) -> int:
        """Get PO age in days"""
        return (datetime.utcnow() - self.order_date.replace(tzinfo=None)).days
    
    @property
    def received_percentage(self) -> float:
        """Get percentage of items received"""
        if not self.po_items:
            return 0.0
        
        total_ordered = sum(item.quantity for item in self.po_items)
        total_received = sum(item.quantity_received or 0 for item in self.po_items)
        
        if total_ordered == 0:
            return 0.0
        
        return (total_received / total_ordered) * 100
    
    @property
    def needs_approval(self) -> bool:
        """Check if PO needs approval"""
        return (
            self.requires_approval and 
            not self.approved_by and 
            self.status == PurchaseOrderStatus.PENDING_APPROVAL
        )
    
    def approve(self, approved_by_user_id: str, notes: str = None) -> None:
        """Approve the purchase order"""
        self.approved_by = approved_by_user_id
        self.approved_at = func.now()
        self.status = PurchaseOrderStatus.APPROVED
        if notes:
            self.approval_notes = notes
    
    def send_to_supplier(self) -> None:
        """Mark PO as sent to supplier"""
        if self.status == PurchaseOrderStatus.APPROVED:
            self.status = PurchaseOrderStatus.SENT
    
    def acknowledge_by_supplier(self, promised_date: datetime = None) -> None:
        """Mark PO as acknowledged by supplier"""
        if self.status == PurchaseOrderStatus.SENT:
            self.status = PurchaseOrderStatus.ACKNOWLEDGED
            if promised_date:
                self.promised_delivery_date = promised_date
    
    def start_production(self) -> None:
        """Mark items as in production"""
        if self.status == PurchaseOrderStatus.ACKNOWLEDGED:
            self.status = PurchaseOrderStatus.IN_PRODUCTION
    
    def receive_items(self, received_by_user_id: str, notes: str = None) -> None:
        """Mark items as received"""
        self.goods_received_by = received_by_user_id
        self.goods_received_date = func.now()
        if notes:
            self.receiving_notes = notes
        
        # Update status based on received percentage
        received_pct = self.received_percentage
        if received_pct >= 100:
            self.status = PurchaseOrderStatus.FULLY_RECEIVED
            self.actual_delivery_date = func.now()
        elif received_pct > 0:
            self.status = PurchaseOrderStatus.PARTIALLY_RECEIVED
        
        # Calculate delivery performance
        if self.expected_delivery_date and self.actual_delivery_date:
            self.on_time_delivery = self.actual_delivery_date <= self.expected_delivery_date
    
    def close_po(self, closed_by_user_id: str, reason: str = None) -> None:
        """Close the purchase order"""
        self.status = PurchaseOrderStatus.CLOSED
        self.closed_by = closed_by_user_id
        self.closed_date = func.now()
        if reason:
            self.closure_reason = reason
    
    def cancel_po(self, reason: str = None) -> None:
        """Cancel the purchase order"""
        self.status = PurchaseOrderStatus.CANCELLED
        if reason:
            self.closure_reason = reason
    
    def calculate_totals(self) -> None:
        """Calculate PO totals from line items"""
        if not self.po_items:
            self.subtotal = Decimal('0.00')
            self.tax_amount = Decimal('0.00')
            self.total_amount = Decimal('0.00')
            return
        
        self.subtotal = sum(item.line_total for item in self.po_items)
        self.tax_amount = sum(item.tax_amount for item in self.po_items)
        self.total_amount = self.subtotal + self.tax_amount - (self.discount_amount or Decimal('0.00'))
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to PO"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from PO"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if PO has specific tag"""
        return bool(self.tags and tag in self.tags)


class PurchaseOrderItem(Base):
    """
    Purchase Order line items
    """
    __tablename__ = "purchase_order_items"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Purchase order association
    purchase_order_id = Column(UUID(as_uuid=True), ForeignKey('purchase_orders.id'), nullable=False, index=True)
    
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
    quantity_received = Column(Numeric(10, 3), default=0)
    quantity_invoiced = Column(Numeric(10, 3), default=0)
    quantity_returned = Column(Numeric(10, 3), default=0)
    
    # Pricing
    unit_price = Column(Numeric(15, 4), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    line_total = Column(Numeric(15, 2), nullable=False)
    
    # Tax information
    tax_code = Column(String(20))
    tax_rate = Column(Numeric(5, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(15, 2), nullable=False, default=0)
    
    # Delivery information
    requested_delivery_date = Column(DateTime)
    promised_delivery_date = Column(DateTime)
    delivery_location = Column(String(255))
    
    # Quality and inspection
    requires_inspection = Column(Boolean, default=False)
    inspection_status = Column(String(50))
    quality_notes = Column(Text)
    
    # Receiving details
    received_condition = Column(String(100))  # "good", "damaged", "partial"
    rejection_reason = Column(Text)
    
    # Greek compliance
    greek_product_classification = Column(String(100))
    
    # Special instructions
    line_notes = Column(Text)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="po_items")
    product = relationship("Product")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_po_item_po', 'purchase_order_id'),
        Index('idx_po_item_product', 'product_id'),
        Index('idx_po_item_line_number', 'line_number'),
    )
    
    def __repr__(self):
        return f"<PurchaseOrderItem(id={self.id}, po='{self.purchase_order_id}', product='{self.product_name}')>"
    
    @property
    def is_fully_received(self) -> bool:
        """Check if item is fully received"""
        return self.quantity_received >= self.quantity
    
    @property
    def outstanding_quantity(self) -> Decimal:
        """Get outstanding quantity to receive"""
        return self.quantity - (self.quantity_received or Decimal('0'))
    
    @property
    def received_percentage(self) -> float:
        """Get percentage received"""
        if self.quantity == 0:
            return 0.0
        return float((self.quantity_received or 0) / self.quantity * 100)
    
    def receive_quantity(self, received_qty: Decimal, condition: str = "good", notes: str = None) -> None:
        """Receive a quantity of this item"""
        if received_qty <= 0:
            return
        
        # Don't receive more than ordered
        max_receivable = self.quantity - (self.quantity_received or Decimal('0'))
        actual_received = min(received_qty, max_receivable)
        
        self.quantity_received = (self.quantity_received or Decimal('0')) + actual_received
        self.received_condition = condition
        if notes:
            self.line_notes = (self.line_notes or "") + f"\nReceived {actual_received} on {datetime.now()}: {notes}"
    
    def calculate_line_total(self) -> None:
        """Calculate line total including discounts"""
        gross_amount = self.quantity * self.unit_price
        discount = self.discount_amount or (gross_amount * (self.discount_percentage or 0) / 100)
        self.line_total = gross_amount - discount
        self.tax_amount = self.line_total * (self.tax_rate or 0) / 100


class PurchaseRequisition(Base):
    """
    Purchase requisitions (requests for purchases)
    """
    __tablename__ = "purchase_requisitions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Requisition identification
    requisition_number = Column(String(50), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Status and priority
    status = Column(String(50), nullable=False, default="draft")  # draft, submitted, approved, converted, rejected
    priority = Column(Enum(PurchaseOrderPriority), nullable=False, default=PurchaseOrderPriority.MEDIUM)
    
    # Requester information
    requested_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    department = Column(String(100))
    cost_center = Column(String(100))
    budget_code = Column(String(100))
    
    # Dates
    request_date = Column(DateTime, nullable=False, default=func.now())
    required_by_date = Column(DateTime)
    approved_date = Column(DateTime)
    
    # Budget information
    estimated_total = Column(Numeric(15, 2))
    budget_available = Column(Numeric(15, 2))
    
    # Approval workflow
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approval_notes = Column(Text)
    
    # Conversion to PO
    converted_to_po = Column(Boolean, default=False)
    po_id = Column(UUID(as_uuid=True), ForeignKey('purchase_orders.id'))
    
    # Business justification
    business_justification = Column(Text)
    urgency_reason = Column(Text)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    requested_by_user = relationship("User", foreign_keys=[requested_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    converted_purchase_order = relationship("PurchaseOrder", foreign_keys=[po_id])
    
    __table_args__ = (
        Index('idx_requisition_company', 'company_id'),
        Index('idx_requisition_number', 'requisition_number'),
        Index('idx_requisition_requested_by', 'requested_by'),
        Index('idx_requisition_status', 'status'),
        Index('idx_requisition_required_date', 'required_by_date'),
    ) 