"""
Inventory models for Greek ERP/CRM System
Stock management, inventory tracking, and warehouse operations
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal
from datetime import datetime

from ..core.database import Base


class StockMovementType(enum.Enum):
    """Stock movement type classification"""
    # Inbound movements
    PURCHASE_RECEIPT = "purchase_receipt"       # Παραλαβή αγοράς
    RETURN_FROM_CUSTOMER = "return_from_customer"  # Επιστροφή από πελάτη
    TRANSFER_IN = "transfer_in"                 # Μεταφορά εισόδου
    PRODUCTION_RECEIPT = "production_receipt"   # Παραλαβή παραγωγής
    ADJUSTMENT_IN = "adjustment_in"             # Προσαρμογή εισόδου
    OPENING_BALANCE = "opening_balance"         # Αρχικό υπόλοιπο
    
    # Outbound movements
    SALES_SHIPMENT = "sales_shipment"           # Αποστολή πώλησης
    RETURN_TO_SUPPLIER = "return_to_supplier"   # Επιστροφή σε προμηθευτή
    TRANSFER_OUT = "transfer_out"               # Μεταφορά εξόδου
    PRODUCTION_ISSUE = "production_issue"       # Έκδοση παραγωγής
    ADJUSTMENT_OUT = "adjustment_out"           # Προσαρμογή εξόδου
    SHRINKAGE = "shrinkage"                     # Απώλεια
    DAMAGE = "damage"                           # Φθορά
    EXPIRY = "expiry"                           # Λήξη
    SCRAP = "scrap"                            # Απόρριψη


class InventoryStatus(enum.Enum):
    """Inventory status"""
    AVAILABLE = "available"         # Διαθέσιμο
    RESERVED = "reserved"           # Δεσμευμένο
    ON_HOLD = "on_hold"            # Σε αναμονή
    QUARANTINE = "quarantine"       # Καραντίνα
    DAMAGED = "damaged"             # Κατεστραμμένο
    EXPIRED = "expired"             # Ληγμένο
    ALLOCATED = "allocated"         # Κατανεμημένο


class LocationType(enum.Enum):
    """Warehouse location type"""
    WAREHOUSE = "warehouse"         # Αποθήκη
    STORE = "store"                # Κατάστημα
    PRODUCTION = "production"       # Παραγωγή
    TRANSIT = "transit"            # Διαμετακόμιση
    CONSIGNMENT = "consignment"     # Εμπορικό απόθεμα
    VIRTUAL = "virtual"            # Εικονική τοποθεσία


class CountType(enum.Enum):
    """Physical count type"""
    FULL_COUNT = "full_count"       # Πλήρης καταμέτρηση
    CYCLE_COUNT = "cycle_count"     # Κυκλική καταμέτρηση
    SPOT_COUNT = "spot_count"       # Τυχαία καταμέτρηση
    ABC_COUNT = "abc_count"         # ABC καταμέτρηση


class Location(Base):
    """
    Warehouse/Storage location model
    """
    __tablename__ = "locations"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Location identification
    location_code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Location classification
    location_type = Column(Enum(LocationType), nullable=False, default=LocationType.WAREHOUSE)
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Physical address
    address_street = Column(String(255))
    address_number = Column(String(10))
    address_city = Column(String(100))
    address_postal_code = Column(String(10))
    address_region = Column(String(100))
    address_country = Column(String(2), default="GR")
    
    # Location hierarchy
    parent_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), index=True)
    location_path = Column(String(500))  # Full path like "MAIN/ZONE-A/AISLE-1/SHELF-A"
    
    # Physical properties
    capacity_cubic_meters = Column(Numeric(10, 3))
    max_weight_kg = Column(Numeric(10, 3))
    temperature_controlled = Column(Boolean, default=False)
    min_temperature = Column(Numeric(5, 2))
    max_temperature = Column(Numeric(5, 2))
    
    # Operational settings
    allow_negative_stock = Column(Boolean, default=False)
    require_lot_tracking = Column(Boolean, default=False)
    require_serial_tracking = Column(Boolean, default=False)
    
    # Manager and contact
    location_manager_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    contact_phone = Column(String(20))
    contact_email = Column(String(255))
    
    # Operating hours
    operating_hours = Column(JSON, default=dict)  # Daily operating hours
    
    # Custom fields
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    parent_location = relationship("Location", remote_side=[id], foreign_keys=[parent_location_id])
    child_locations = relationship("Location", foreign_keys=[parent_location_id])
    location_manager = relationship("User", foreign_keys=[location_manager_id])
    inventory_items = relationship("InventoryItem", back_populates="location")
    
    # Indexes
    __table_args__ = (
        Index('idx_location_company', 'company_id'),
        Index('idx_location_code', 'location_code'),
        Index('idx_location_type', 'location_type'),
        Index('idx_location_active', 'is_active'),
        Index('idx_location_parent', 'parent_location_id'),
    )
    
    def __repr__(self):
        return f"<Location(id={self.id}, code='{self.location_code}', name='{self.name}')>"


class InventoryItem(Base):
    """
    Inventory item model - tracks stock levels by product and location
    """
    __tablename__ = "inventory_items"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Product and location
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), nullable=False, index=True)
    
    # Stock quantities
    quantity_on_hand = Column(Numeric(10, 3), nullable=False, default=0)
    quantity_available = Column(Numeric(10, 3), nullable=False, default=0)  # On hand - reserved
    quantity_reserved = Column(Numeric(10, 3), nullable=False, default=0)
    quantity_on_order = Column(Numeric(10, 3), nullable=False, default=0)
    quantity_allocated = Column(Numeric(10, 3), nullable=False, default=0)
    
    # Inventory status
    status = Column(Enum(InventoryStatus), nullable=False, default=InventoryStatus.AVAILABLE)
    
    # Stock level management
    minimum_stock = Column(Numeric(10, 3), default=0)
    maximum_stock = Column(Numeric(10, 3))
    reorder_point = Column(Numeric(10, 3), default=0)
    reorder_quantity = Column(Numeric(10, 3), default=0)
    safety_stock = Column(Numeric(10, 3), default=0)
    
    # Costing
    last_cost = Column(Numeric(15, 4))
    average_cost = Column(Numeric(15, 4))
    standard_cost = Column(Numeric(15, 4))
    total_value = Column(Numeric(15, 2))  # quantity * cost
    
    # Lot and serial tracking
    lot_controlled = Column(Boolean, default=False)
    serial_controlled = Column(Boolean, default=False)
    
    # Dates
    last_received_date = Column(DateTime)
    last_issued_date = Column(DateTime)
    last_count_date = Column(DateTime)
    last_movement_date = Column(DateTime)
    
    # ABC analysis
    abc_class = Column(String(1))  # A, B, or C
    abc_value = Column(Numeric(15, 2))
    
    # Cycle counting
    cycle_count_frequency = Column(Integer)  # Days between counts
    next_count_date = Column(DateTime)
    count_variance_threshold = Column(Numeric(5, 2), default=5.0)  # %
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    product = relationship("Product")
    location = relationship("Location", back_populates="inventory_items")
    stock_movements = relationship("StockMovement", back_populates="inventory_item")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('product_id', 'location_id', name='uq_inventory_product_location'),
        Index('idx_inventory_company', 'company_id'),
        Index('idx_inventory_product', 'product_id'),
        Index('idx_inventory_location', 'location_id'),
        Index('idx_inventory_status', 'status'),
        Index('idx_inventory_reorder', 'reorder_point'),
        Index('idx_inventory_abc', 'abc_class'),
        Index('idx_inventory_next_count', 'next_count_date'),
    )
    
    def __repr__(self):
        return f"<InventoryItem(id={self.id}, product='{self.product_id}', location='{self.location_id}', qty={self.quantity_on_hand})>"
    
    @property
    def is_below_minimum(self) -> bool:
        """Check if stock is below minimum level"""
        return self.quantity_available < (self.minimum_stock or 0)
    
    @property
    def is_at_reorder_point(self) -> bool:
        """Check if stock is at or below reorder point"""
        return self.quantity_available <= (self.reorder_point or 0)
    
    @property
    def is_out_of_stock(self) -> bool:
        """Check if item is out of stock"""
        return self.quantity_available <= 0
    
    @property
    def stock_coverage_days(self) -> Optional[float]:
        """Calculate days of stock coverage based on average usage"""
        # This would typically calculate based on historical movement data
        # For now, return a placeholder
        return None
    
    def update_quantities(self, quantity_change: Decimal, movement_type: StockMovementType) -> None:
        """Update inventory quantities based on stock movement"""
        if movement_type in [
            StockMovementType.PURCHASE_RECEIPT,
            StockMovementType.RETURN_FROM_CUSTOMER,
            StockMovementType.TRANSFER_IN,
            StockMovementType.PRODUCTION_RECEIPT,
            StockMovementType.ADJUSTMENT_IN,
            StockMovementType.OPENING_BALANCE
        ]:
            # Inbound movements
            self.quantity_on_hand += quantity_change
            self.quantity_available += quantity_change
        else:
            # Outbound movements
            self.quantity_on_hand -= quantity_change
            self.quantity_available -= quantity_change
        
        # Update last movement date
        self.last_movement_date = func.now()
        
        # Update dates based on movement type
        if "RECEIPT" in movement_type.value or "RETURN_FROM_CUSTOMER" in movement_type.value:
            self.last_received_date = func.now()
        elif "SHIPMENT" in movement_type.value or "ISSUE" in movement_type.value:
            self.last_issued_date = func.now()
    
    def reserve_quantity(self, quantity: Decimal) -> bool:
        """Reserve a quantity for allocation"""
        if self.quantity_available >= quantity:
            self.quantity_reserved += quantity
            self.quantity_available -= quantity
            return True
        return False
    
    def release_reservation(self, quantity: Decimal) -> None:
        """Release a reserved quantity"""
        release_qty = min(quantity, self.quantity_reserved)
        self.quantity_reserved -= release_qty
        self.quantity_available += release_qty
    
    def calculate_total_value(self) -> None:
        """Calculate total inventory value"""
        cost = self.average_cost or self.last_cost or self.standard_cost
        if cost:
            self.total_value = self.quantity_on_hand * cost


class StockMovement(Base):
    """
    Stock movement transactions
    """
    __tablename__ = "stock_movements"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Movement identification
    movement_number = Column(String(50), nullable=False, unique=True, index=True)
    movement_type = Column(Enum(StockMovementType), nullable=False)
    
    # Product and location
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), nullable=False, index=True)
    inventory_item_id = Column(UUID(as_uuid=True), ForeignKey('inventory_items.id'), nullable=False, index=True)
    
    # Transfer movements (location to location)
    from_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), index=True)
    to_location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), index=True)
    
    # Movement details
    quantity = Column(Numeric(10, 3), nullable=False)
    unit_of_measure = Column(String(20))
    unit_cost = Column(Numeric(15, 4))
    total_cost = Column(Numeric(15, 2))
    
    # Reference document
    reference_type = Column(String(50))  # "purchase_order", "sales_order", "adjustment", etc.
    reference_id = Column(UUID(as_uuid=True))
    reference_number = Column(String(100))
    
    # Lot and serial tracking
    lot_number = Column(String(100))
    serial_number = Column(String(100))
    expiry_date = Column(DateTime)
    
    # Movement timing
    movement_date = Column(DateTime, nullable=False, default=func.now())
    transaction_date = Column(DateTime, nullable=False, default=func.now())
    
    # User and reason
    moved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    reason_code = Column(String(50))
    notes = Column(Text)
    
    # Approval (for adjustments)
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approved_at = Column(DateTime)
    
    # Quality information
    quality_status = Column(String(50))  # "passed", "failed", "pending"
    inspection_notes = Column(Text)
    
    # Costing impact
    affects_costing = Column(Boolean, default=True)
    cost_impact = Column(Numeric(15, 2))
    
    # Greek business compliance
    customs_declaration = Column(String(100))
    import_license = Column(String(100))
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    product = relationship("Product")
    location = relationship("Location", foreign_keys=[location_id])
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])
    inventory_item = relationship("InventoryItem", back_populates="stock_movements")
    moved_by_user = relationship("User", foreign_keys=[moved_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_stock_movement_company', 'company_id'),
        Index('idx_stock_movement_number', 'movement_number'),
        Index('idx_stock_movement_type', 'movement_type'),
        Index('idx_stock_movement_product', 'product_id'),
        Index('idx_stock_movement_location', 'location_id'),
        Index('idx_stock_movement_inventory', 'inventory_item_id'),
        Index('idx_stock_movement_date', 'movement_date'),
        Index('idx_stock_movement_moved_by', 'moved_by'),
        Index('idx_stock_movement_reference', 'reference_type', 'reference_id'),
        Index('idx_stock_movement_lot', 'lot_number'),
        Index('idx_stock_movement_serial', 'serial_number'),
    )
    
    def __repr__(self):
        return f"<StockMovement(id={self.id}, number='{self.movement_number}', type='{self.movement_type.value}', qty={self.quantity})>"


class PhysicalCount(Base):
    """
    Physical inventory counts
    """
    __tablename__ = "physical_counts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Count identification
    count_number = Column(String(50), nullable=False, unique=True, index=True)
    count_name = Column(String(255), nullable=False)
    count_type = Column(Enum(CountType), nullable=False)
    
    # Count scope
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), index=True)
    product_categories = Column(JSON, default=list)  # List of category IDs to count
    abc_classes = Column(JSON, default=list)  # A, B, C classes to count
    
    # Count status
    status = Column(String(50), nullable=False, default="planned")  # planned, in_progress, completed, cancelled
    
    # Count scheduling
    scheduled_date = Column(DateTime)
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    
    # Count team
    count_manager = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    count_team = Column(JSON, default=list)  # List of user IDs
    
    # Count configuration
    allow_negative_adjustments = Column(Boolean, default=True)
    variance_threshold_percentage = Column(Numeric(5, 2), default=5.0)
    require_recount_over_threshold = Column(Boolean, default=True)
    
    # Count results
    items_counted = Column(Integer, default=0)
    items_with_variance = Column(Integer, default=0)
    total_variance_value = Column(Numeric(15, 2), default=0)
    adjustments_created = Column(Boolean, default=False)
    
    # Notes and instructions
    count_instructions = Column(Text)
    completion_notes = Column(Text)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    
    # Relationships
    location = relationship("Location")
    count_manager_user = relationship("User", foreign_keys=[count_manager])
    count_lines = relationship("PhysicalCountLine", back_populates="physical_count", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_physical_count_company', 'company_id'),
        Index('idx_physical_count_number', 'count_number'),
        Index('idx_physical_count_type', 'count_type'),
        Index('idx_physical_count_location', 'location_id'),
        Index('idx_physical_count_status', 'status'),
        Index('idx_physical_count_scheduled', 'scheduled_date'),
    )


class PhysicalCountLine(Base):
    """
    Physical count line items
    """
    __tablename__ = "physical_count_lines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    physical_count_id = Column(UUID(as_uuid=True), ForeignKey('physical_counts.id'), nullable=False, index=True)
    
    # Product and location
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), nullable=False, index=True)
    
    # Count quantities
    system_quantity = Column(Numeric(10, 3), nullable=False)  # Quantity per system
    counted_quantity = Column(Numeric(10, 3))  # Actual counted quantity
    variance_quantity = Column(Numeric(10, 3))  # Difference
    variance_percentage = Column(Numeric(5, 2))  # Variance %
    
    # Count details
    counted_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    count_date = Column(DateTime)
    recount_required = Column(Boolean, default=False)
    recount_completed = Column(Boolean, default=False)
    
    # Lot and serial
    lot_number = Column(String(100))
    serial_number = Column(String(100))
    
    # Count notes
    count_notes = Column(Text)
    variance_reason = Column(Text)
    
    # Adjustment tracking
    adjustment_created = Column(Boolean, default=False)
    adjustment_movement_id = Column(UUID(as_uuid=True), ForeignKey('stock_movements.id'))
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    physical_count = relationship("PhysicalCount", back_populates="count_lines")
    product = relationship("Product")
    location = relationship("Location")
    counted_by_user = relationship("User", foreign_keys=[counted_by])
    adjustment_movement = relationship("StockMovement", foreign_keys=[adjustment_movement_id])
    
    __table_args__ = (
        Index('idx_count_line_count', 'physical_count_id'),
        Index('idx_count_line_product', 'product_id'),
        Index('idx_count_line_location', 'location_id'),
        Index('idx_count_line_variance', 'variance_quantity'),
    ) 