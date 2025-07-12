"""
Business Entity model for Greek ERP/CRM System
Unified model for all external business entities (customers, suppliers, partners)
This replaces the Customer model and adds Supplier functionality
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal

from ..core.database import Base


class BusinessEntityType(enum.Enum):
    """Business entity type classification"""
    BUSINESS = "business"      # B2B entity
    INDIVIDUAL = "individual"  # B2C entity
    GOVERNMENT = "government"  # Government entity
    NON_PROFIT = "non_profit"  # Non-profit organization


class BusinessEntityStatus(enum.Enum):
    """Business entity status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PROSPECT = "prospect"      # Potential business partner
    BLOCKED = "blocked"        # Blocked entity


class BusinessEntityRole(enum.Enum):
    """Roles that a business entity can have"""
    CUSTOMER = "customer"      # Buys from us
    SUPPLIER = "supplier"      # Sells to us
    PARTNER = "partner"        # Business partner
    COMPETITOR = "competitor"  # Competitor
    PROSPECT = "prospect"      # Potential customer/supplier
    LEAD = "lead"              # Sales lead


class PaymentTerms(enum.Enum):
    """Payment terms for business entities"""
    NET_0 = "net_0"        # Cash on delivery
    NET_15 = "net_15"      # 15 days
    NET_30 = "net_30"      # 30 days
    NET_60 = "net_60"      # 60 days
    NET_90 = "net_90"      # 90 days
    PREPAID = "prepaid"    # Prepayment required


# Many-to-many relationship table for business entity roles
business_entity_roles = Table(
    'business_entity_roles',
    Base.metadata,
    Column('business_entity_id', UUID(as_uuid=True), ForeignKey('business_entities.id'), primary_key=True),
    Column('role', Enum(BusinessEntityRole), primary_key=True),
    Column('assigned_at', DateTime, server_default=func.now(), nullable=False),
    Column('assigned_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('notes', Text),
    Index('idx_business_entity_roles_entity', 'business_entity_id'),
    Index('idx_business_entity_roles_role', 'role'),
    Index('idx_business_entity_roles_active', 'is_active'),
)


class BusinessEntity(Base):
    """
    Unified Business Entity model for Greek ERP/CRM system
    Represents all external business entities (customers, suppliers, partners)
    Replaces the Customer model and adds Supplier functionality
    """
    __tablename__ = "business_entities"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (stored in company's database)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Business entity identification
    entity_code = Column(String(20), nullable=False, unique=True, index=True)
    entity_type = Column(Enum(BusinessEntityType), nullable=False, default=BusinessEntityType.BUSINESS)
    
    # Basic information
    business_name = Column(String(255))  # For business entities
    first_name = Column(String(100))     # For individual entities
    last_name = Column(String(100))      # For individual entities
    display_name = Column(String(255), nullable=False, index=True)
    
    # Greek business compliance (for business entities)
    afm = Column(String(9), index=True)  # Greek Tax Number
    doy = Column(String(10), index=True)  # Tax Office Code
    business_activity = Column(String(255))  # Business activity
    legal_form = Column(String(50))      # ΑΕ, ΕΠΕ, ΟΕ, ΕΕ, etc.
    
    # EU VAT compliance
    vat_number = Column(String(20), index=True)  # EU VAT number
    vat_exempt = Column(Boolean, default=False)
    
    # Contact information
    email = Column(String(255), index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    fax = Column(String(20))
    website = Column(String(255))
    
    # Greek address fields
    address_street = Column(String(255))
    address_number = Column(String(10))
    address_city = Column(String(100))
    address_postal_code = Column(String(10))
    address_region = Column(String(100))  # Greek region
    address_country = Column(String(2), default="GR")  # ISO country code
    
    # Billing address (if different)
    billing_address_street = Column(String(255))
    billing_address_number = Column(String(10))
    billing_address_city = Column(String(100))
    billing_address_postal_code = Column(String(10))
    billing_address_region = Column(String(100))
    billing_address_country = Column(String(2), default="GR")
    
    # Status and classification
    status = Column(Enum(BusinessEntityStatus), nullable=False, default=BusinessEntityStatus.ACTIVE)
    entity_category = Column(String(50))  # A, B, C classification
    entity_segment = Column(String(50))   # Market segment
    
    # Financial information (for customer relationships)
    credit_limit = Column(Numeric(15, 2), default=0)
    payment_terms = Column(Enum(PaymentTerms), default=PaymentTerms.NET_30)
    discount_percentage = Column(Numeric(5, 2), default=0)
    
    # Supplier information (for supplier relationships)
    supplier_rating = Column(Integer)  # 1-5 rating
    supplier_category = Column(String(100))  # Preferred, Standard, etc.
    lead_time_days = Column(Integer, default=0)
    minimum_order_amount = Column(Numeric(15, 2))
    
    # CRM information
    lead_source = Column(String(100))      # How entity was acquired
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Account manager
    notes = Column(Text)
    tags = Column(JSON, default=list)      # Entity tags
    
    # Business metrics
    total_sales = Column(Numeric(15, 2), default=0)  # Total sales to this entity
    total_purchases = Column(Numeric(15, 2), default=0)  # Total purchases from this entity
    total_orders = Column(Integer, default=0)
    total_purchase_orders = Column(Integer, default=0)
    last_order_date = Column(DateTime)
    last_purchase_date = Column(DateTime)
    first_order_date = Column(DateTime)
    first_purchase_date = Column(DateTime)
    
    # Language and preferences
    language = Column(String(2), default="el")  # Greek by default
    preferred_contact_method = Column(String(20), default="email")
    
    # Marketing preferences
    marketing_consent = Column(Boolean, default=False)
    newsletter_subscription = Column(Boolean, default=False)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    contacts = relationship("Contact", back_populates="business_entity")
    invoices = relationship("Invoice", back_populates="business_entity")
    
    # Many-to-many relationship for roles
    # This will be populated via the business_entity_roles table
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_business_entity_company', 'company_id'),
        Index('idx_business_entity_code', 'entity_code'),
        Index('idx_business_entity_type', 'entity_type'),
        Index('idx_business_entity_status', 'status'),
        Index('idx_business_entity_afm', 'afm'),
        Index('idx_business_entity_vat', 'vat_number'),
        Index('idx_business_entity_email', 'email'),
        Index('idx_business_entity_display_name', 'display_name'),
        Index('idx_business_entity_assigned_user', 'assigned_user_id'),
        Index('idx_business_entity_category', 'entity_category'),
    )
    
    def __repr__(self):
        return f"<BusinessEntity(id={self.id}, code='{self.entity_code}', name='{self.display_name}')>"
    
    @property
    def full_name(self) -> str:
        """Get entity's full name"""
        if self.entity_type == BusinessEntityType.INDIVIDUAL:
            return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.display_name
        return self.business_name or self.display_name
    
    @property
    def primary_address(self) -> str:
        """Get formatted primary address"""
        if not self.address_street:
            return ""
        return f"{self.address_street} {self.address_number}, {self.address_postal_code} {self.address_city}, {self.address_region}"
    
    @property
    def billing_address(self) -> str:
        """Get formatted billing address"""
        if not self.billing_address_street:
            return self.primary_address
        return f"{self.billing_address_street} {self.billing_address_number}, {self.billing_address_postal_code} {self.billing_address_city}, {self.billing_address_region}"
    
    @property
    def is_business(self) -> bool:
        """Check if entity is a business"""
        return self.entity_type == BusinessEntityType.BUSINESS
    
    @property
    def is_individual(self) -> bool:
        """Check if entity is an individual"""
        return self.entity_type == BusinessEntityType.INDIVIDUAL
    
    @property
    def has_valid_afm(self) -> bool:
        """Check if entity has valid Greek AFM"""
        return bool(self.afm and len(self.afm) == 9 and self.afm.isdigit())
    
    @property
    def has_valid_vat(self) -> bool:
        """Check if entity has valid EU VAT number"""
        return bool(self.vat_number and len(self.vat_number) >= 8)
    
    def get_roles(self) -> List[BusinessEntityRole]:
        """Get all active roles for this entity"""
        # This would typically query the business_entity_roles table
        # For now, return empty list as placeholder
        return []
    
    def has_role(self, role: BusinessEntityRole) -> bool:
        """Check if entity has specific role"""
        return role in self.get_roles()
    
    def add_role(self, role: BusinessEntityRole, assigned_by: str = None, notes: str = None) -> None:
        """Add a role to this entity"""
        # This would typically insert into business_entity_roles table
        pass
    
    def remove_role(self, role: BusinessEntityRole) -> None:
        """Remove a role from this entity"""
        # This would typically update business_entity_roles table
        pass
    
    @property
    def is_customer(self) -> bool:
        """Check if entity is a customer"""
        return self.has_role(BusinessEntityRole.CUSTOMER)
    
    @property
    def is_supplier(self) -> bool:
        """Check if entity is a supplier"""
        return self.has_role(BusinessEntityRole.SUPPLIER)
    
    @property
    def is_partner(self) -> bool:
        """Check if entity is a partner"""
        return self.has_role(BusinessEntityRole.PARTNER)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to entity"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from entity"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if entity has specific tag"""
        return bool(self.tags and tag in self.tags)
    
    def calculate_outstanding_balance(self) -> Decimal:
        """Calculate outstanding balance from unpaid invoices"""
        # This would typically query related invoices
        # For now, return 0 as placeholder
        return Decimal('0.00')
    
    def get_credit_available(self) -> Decimal:
        """Get available credit limit"""
        outstanding = self.calculate_outstanding_balance()
        return max(Decimal('0.00'), self.credit_limit - outstanding)
    
    def is_credit_limit_exceeded(self) -> bool:
        """Check if credit limit is exceeded"""
        return self.calculate_outstanding_balance() > self.credit_limit
    
    def update_sales_metrics(self, order_amount: Decimal) -> None:
        """Update entity sales metrics"""
        self.total_sales = (self.total_sales or Decimal('0.00')) + order_amount
        self.total_orders = (self.total_orders or 0) + 1
        self.last_order_date = func.now()
        if not self.first_order_date:
            self.first_order_date = func.now()
    
    def update_purchase_metrics(self, purchase_amount: Decimal) -> None:
        """Update entity purchase metrics"""
        self.total_purchases = (self.total_purchases or Decimal('0.00')) + purchase_amount
        self.total_purchase_orders = (self.total_purchase_orders or 0) + 1
        self.last_purchase_date = func.now()
        if not self.first_purchase_date:
            self.first_purchase_date = func.now()
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert business entity to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "entity_code": self.entity_code,
            "entity_type": self.entity_type.value,
            "business_name": self.business_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "display_name": self.display_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "website": self.website,
            "address": {
                "street": self.address_street,
                "number": self.address_number,
                "city": self.address_city,
                "postal_code": self.address_postal_code,
                "region": self.address_region,
                "country": self.address_country,
                "full_address": self.primary_address
            },
            "billing_address": {
                "street": self.billing_address_street,
                "number": self.billing_address_number,
                "city": self.billing_address_city,
                "postal_code": self.billing_address_postal_code,
                "region": self.billing_address_region,
                "country": self.billing_address_country,
                "full_address": self.billing_address
            },
            "status": self.status.value,
            "entity_category": self.entity_category,
            "entity_segment": self.entity_segment,
            "credit_limit": float(self.credit_limit) if self.credit_limit else 0,
            "payment_terms": self.payment_terms.value if self.payment_terms else None,
            "discount_percentage": float(self.discount_percentage) if self.discount_percentage else 0,
            "supplier_rating": self.supplier_rating,
            "supplier_category": self.supplier_category,
            "lead_time_days": self.lead_time_days,
            "minimum_order_amount": float(self.minimum_order_amount) if self.minimum_order_amount else None,
            "lead_source": self.lead_source,
            "assigned_user_id": str(self.assigned_user_id) if self.assigned_user_id else None,
            "tags": self.tags,
            "total_sales": float(self.total_sales) if self.total_sales else 0,
            "total_purchases": float(self.total_purchases) if self.total_purchases else 0,
            "total_orders": self.total_orders,
            "total_purchase_orders": self.total_purchase_orders,
            "last_order_date": self.last_order_date.isoformat() if self.last_order_date else None,
            "last_purchase_date": self.last_purchase_date.isoformat() if self.last_purchase_date else None,
            "language": self.language,
            "preferred_contact_method": self.preferred_contact_method,
            "marketing_consent": self.marketing_consent,
            "newsletter_subscription": self.newsletter_subscription,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "roles": [role.value for role in self.get_roles()],
            "is_customer": self.is_customer,
            "is_supplier": self.is_supplier,
            "is_partner": self.is_partner,
            "has_valid_afm": self.has_valid_afm,
            "has_valid_vat": self.has_valid_vat,
            "outstanding_balance": float(self.calculate_outstanding_balance()),
            "credit_available": float(self.get_credit_available()),
            "is_credit_limit_exceeded": self.is_credit_limit_exceeded()
        }
        
        # Include sensitive data only if requested
        if include_sensitive:
            data.update({
                "afm": self.afm,
                "doy": self.doy,
                "business_activity": self.business_activity,
                "legal_form": self.legal_form,
                "vat_number": self.vat_number,
                "vat_exempt": self.vat_exempt,
                "notes": self.notes
            })
        
        return data 