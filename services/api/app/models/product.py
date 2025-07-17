"""
Product models for Greek ERP/CRM System
Production-level flexible product system with dynamic attributes, variants, and Greek VAT compliance
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal

from ..core.database import Base


class ProductType(enum.Enum):
    """Product type classification"""
    SIMPLE = "simple"              # Simple product (no variants)
    VARIABLE = "variable"          # Variable product (has variants like color/size)
    SERVICE = "service"            # Service product
    SUBSCRIPTION = "subscription"  # Subscription service
    BUNDLE = "bundle"             # Product bundle
    DIGITAL = "digital"           # Digital product


class ProductStatus(enum.Enum):
    """Product status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    DRAFT = "draft"


class VatCategory(enum.Enum):
    """Greek VAT categories"""
    STANDARD = "standard"      # 24% (standard rate)
    REDUCED_1 = "reduced_1"    # 13% (reduced rate 1)
    REDUCED_2 = "reduced_2"    # 6% (reduced rate 2)
    ZERO = "zero"              # 0% (zero rate)
    EXEMPT = "exempt"          # VAT exempt


class UnitOfMeasure(enum.Enum):
    """Units of measure"""
    PIECE = "piece"            # Τεμάχιο
    KILOGRAM = "kilogram"      # Κιλό
    GRAM = "gram"              # Γραμμάριο
    LITER = "liter"            # Λίτρο
    MILLILITER = "milliliter"  # Χιλιοστόλιτρο
    METER = "meter"            # Μέτρο
    CENTIMETER = "centimeter"  # Εκατοστό
    SQUARE_METER = "square_meter"  # Τετραγωνικό μέτρο
    CUBIC_METER = "cubic_meter"    # Κυβικό μέτρο
    HOUR = "hour"              # Ώρα
    DAY = "day"                # Μέρα
    MONTH = "month"            # Μήνας
    YEAR = "year"              # Χρόνος


class AttributeType(enum.Enum):
    """Attribute data types"""
    TEXT = "text"              # Simple text
    NUMBER = "number"          # Numeric value
    DECIMAL = "decimal"        # Decimal number
    BOOLEAN = "boolean"        # True/False
    DATE = "date"              # Date value
    COLOR = "color"            # Color (with hex code)
    SIZE = "size"              # Size (with ordering)
    SELECT = "select"          # Single selection from list
    MULTISELECT = "multiselect" # Multiple selection from list
    RANGE = "range"            # Numeric range
    DIMENSION = "dimension"    # Physical dimension
    WEIGHT = "weight"          # Weight value
    TEMPERATURE = "temperature" # Temperature value
    FILE = "file"              # File attachment
    URL = "url"                # URL link


class Product(Base):
    """
    Base Product model for Greek ERP/CRM system
    Master product that can have multiple variants with different attributes
    """
    __tablename__ = "products"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (stored in company's database)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Product identification
    product_code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    
    # Product classification
    product_type = Column(Enum(ProductType), nullable=False, default=ProductType.SIMPLE)
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.ACTIVE)
    category_id = Column(UUID(as_uuid=True), ForeignKey('product_categories.id'), index=True)
    brand = Column(String(100))
    manufacturer = Column(String(100))
    
    # Base pricing (can be overridden by variants)
    base_cost_price = Column(Numeric(15, 4), default=0)
    base_selling_price = Column(Numeric(15, 4), nullable=False)
    base_wholesale_price = Column(Numeric(15, 4))
    
    # Greek VAT compliance (can be overridden by variants)
    vat_category = Column(Enum(VatCategory), nullable=False, default=VatCategory.STANDARD)
    vat_rate = Column(Numeric(5, 2), nullable=False, default=24.00)
    vat_exempt_reason = Column(String(255))
    
    # Base measurements (can be overridden by variants)
    unit_of_measure = Column(Enum(UnitOfMeasure), nullable=False, default=UnitOfMeasure.PIECE)
    base_weight = Column(Numeric(10, 3))  # kg
    base_length = Column(Numeric(10, 3))  # cm
    base_width = Column(Numeric(10, 3))   # cm
    base_height = Column(Numeric(10, 3))  # cm
    
    # Inventory settings
    track_inventory = Column(Boolean, default=True)
    track_by_variant = Column(Boolean, default=False)  # Track inventory per variant
    
    # Global product settings
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_digital = Column(Boolean, default=False)
    requires_shipping = Column(Boolean, default=True)
    taxable = Column(Boolean, default=True)
    
    # Service-specific fields for service-only businesses
    service_duration = Column(Integer)  # Duration in minutes
    service_buffer_time = Column(Integer, default=0)  # Buffer time between appointments
    is_bookable = Column(Boolean, default=False)  # Can be booked via calendar
    advance_booking_days = Column(Integer, default=0)  # How many days in advance can be booked
    max_bookings_per_day = Column(Integer)  # Maximum bookings per day
    requires_preparation = Column(Boolean, default=False)  # Requires preparation time
    preparation_time = Column(Integer, default=0)  # Preparation time in minutes
    
    # Professional services (doctors, lawyers, engineers)
    requires_license = Column(Boolean, default=False)  # Requires professional license
    certification_required = Column(String(255))  # Required certification
    professional_type = Column(String(100))  # Doctor, Lawyer, Engineer, etc.
    
    # Service delivery settings
    service_location = Column(String(20), default="office")  # office, client_location, remote, any
    allows_remote_delivery = Column(Boolean, default=False)  # Can be delivered remotely
    
    # Recurring service settings
    is_recurring = Column(Boolean, default=False)  # Is this a recurring service
    recurring_interval = Column(String(20))  # daily, weekly, monthly, yearly
    recurring_duration = Column(Integer)  # How many intervals
    
    # SEO and marketing
    meta_title = Column(String(255))
    meta_description = Column(Text)
    keywords = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    
    # Images and media
    primary_image_url = Column(String(500))
    image_urls = Column(JSON, default=list)
    
    # Supplier information
    primary_supplier_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), index=True)
    supplier_product_code = Column(String(100))  # Supplier's product code
    supplier_lead_time_days = Column(Integer, default=0)
    
    # Flexible data for custom fields
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    primary_supplier = relationship("BusinessEntity", foreign_keys=[primary_supplier_id])
    attributes = relationship("ProductAttribute", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    inventory_items = relationship("ProductInventory", back_populates="product", cascade="all, delete-orphan")
    invoice_items = relationship("InvoiceItem", back_populates="product")
    vat_config = relationship("ProductVATConfig", back_populates="product", uselist=False)
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_product_company', 'company_id'),
        Index('idx_product_code', 'product_code'),
        Index('idx_product_name', 'name'),
        Index('idx_product_type', 'product_type'),
        Index('idx_product_status', 'status'),
        Index('idx_product_category', 'category_id'),
        Index('idx_product_vat_category', 'vat_category'),
        Index('idx_product_active', 'is_active'),
        Index('idx_product_featured', 'is_featured'),
    )
    
    def __repr__(self):
        return f"<Product(id={self.id}, code='{self.product_code}', name='{self.name}')>"
    
    @property
    def has_variants(self) -> bool:
        """Check if product has variants"""
        return self.product_type == ProductType.VARIABLE and len(self.variants) > 0
    
    @property
    def total_stock(self) -> int:
        """Get total stock across all variants or direct inventory"""
        if self.has_variants:
            return sum(variant.stock_quantity for variant in self.variants)
        elif self.inventory_items:
            return sum(item.stock_quantity for item in self.inventory_items)
        return 0
    
    @property
    def available_stock(self) -> int:
        """Get available stock (total - reserved)"""
        if self.has_variants:
            return sum(variant.available_quantity for variant in self.variants)
        elif self.inventory_items:
            return sum(item.available_quantity for item in self.inventory_items)
        return 0
    
    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock"""
        if not self.track_inventory:
            return True
        return self.available_stock > 0
    
    @property
    def lowest_price(self) -> Decimal:
        """Get lowest price among variants or base price"""
        if self.has_variants:
            variant_prices = [v.selling_price for v in self.variants if v.selling_price]
            return min(variant_prices) if variant_prices else self.base_selling_price
        return self.base_selling_price
    
    @property
    def highest_price(self) -> Decimal:
        """Get highest price among variants or base price"""
        if self.has_variants:
            variant_prices = [v.selling_price for v in self.variants if v.selling_price]
            return max(variant_prices) if variant_prices else self.base_selling_price
        return self.base_selling_price
    
    def get_attribute_definitions(self) -> List[Dict[str, Any]]:
        """Get all attribute definitions for this product"""
        return [attr.to_dict() for attr in self.attributes]
    
    def get_variant_by_attributes(self, attributes: Dict[str, str]) -> Optional['ProductVariant']:
        """Find variant by attribute combination"""
        for variant in self.variants:
            if variant.matches_attributes(attributes):
                return variant
        return None
    
    def add_attribute(self, attribute_name: str, attribute_type: AttributeType, 
                     values: List[str], required: bool = False) -> 'ProductAttribute':
        """Add a new attribute to the product"""
        attribute = ProductAttribute(
            product_id=self.id,
            name=attribute_name,
            attribute_type=attribute_type,
            required=required
        )
        
        for i, value in enumerate(values):
            attr_value = ProductAttributeValue(
                attribute=attribute,
                value=value,
                display_order=i
            )
            attribute.values.append(attr_value)
        
        self.attributes.append(attribute)
        return attribute
    
    def to_dict(self, include_variants: bool = True, include_inventory: bool = False) -> Dict[str, Any]:
        """Convert product to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "product_code": self.product_code,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "product_type": self.product_type.value,
            "status": self.status.value,
            "category_id": str(self.category_id) if self.category_id else None,
            "brand": self.brand,
            "manufacturer": self.manufacturer,
            "base_cost_price": float(self.base_cost_price) if self.base_cost_price else 0,
            "base_selling_price": float(self.base_selling_price),
            "base_wholesale_price": float(self.base_wholesale_price) if self.base_wholesale_price else None,
            "vat_category": self.vat_category.value,
            "vat_rate": float(self.vat_rate),
            "unit_of_measure": self.unit_of_measure.value,
            "base_weight": float(self.base_weight) if self.base_weight else None,
            "base_length": float(self.base_length) if self.base_length else None,
            "base_width": float(self.base_width) if self.base_width else None,
            "base_height": float(self.base_height) if self.base_height else None,
            "track_inventory": self.track_inventory,
            "track_by_variant": self.track_by_variant,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "is_digital": self.is_digital,
            "requires_shipping": self.requires_shipping,
            "taxable": self.taxable,
            # Service-specific fields
            "service_duration": self.service_duration,
            "service_buffer_time": self.service_buffer_time,
            "is_bookable": self.is_bookable,
            "advance_booking_days": self.advance_booking_days,
            "max_bookings_per_day": self.max_bookings_per_day,
            "requires_preparation": self.requires_preparation,
            "preparation_time": self.preparation_time,
            "requires_license": self.requires_license,
            "certification_required": self.certification_required,
            "professional_type": self.professional_type,
            "service_location": self.service_location,
            "allows_remote_delivery": self.allows_remote_delivery,
            "is_recurring": self.is_recurring,
            "recurring_interval": self.recurring_interval,
            "recurring_duration": self.recurring_duration,
            "primary_image_url": self.primary_image_url,
            "image_urls": self.image_urls,
            "tags": self.tags,
            "keywords": self.keywords,
            "custom_fields": self.custom_fields,
            "has_variants": self.has_variants,
            "total_stock": self.total_stock,
            "available_stock": self.available_stock,
            "is_in_stock": self.is_in_stock,
            "lowest_price": float(self.lowest_price),
            "highest_price": float(self.highest_price),
            "attributes": self.get_attribute_definitions(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_variants and self.has_variants:
            data["variants"] = [variant.to_dict() for variant in self.variants]
        
        if include_inventory:
            data["inventory"] = [item.to_dict() for item in self.inventory_items]
        
        return data


class ProductCategory(Base):
    """
    Product category model for hierarchical product organization
    """
    __tablename__ = "product_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('product_categories.id'), index=True)
    
    # Category-level defaults
    default_vat_category = Column(Enum(VatCategory), default=VatCategory.STANDARD)
    default_vat_rate = Column(Numeric(5, 2), default=24.00)
    default_unit_of_measure = Column(Enum(UnitOfMeasure), default=UnitOfMeasure.PIECE)
    
    # Display settings
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    parent = relationship("ProductCategory", remote_side=[id], foreign_keys=[parent_id])
    children = relationship("ProductCategory", foreign_keys=[parent_id], overlaps="parent")
    products = relationship("Product", back_populates="category")
    
    __table_args__ = (
        Index('idx_product_category_company', 'company_id'),
        Index('idx_product_category_parent', 'parent_id'),
        Index('idx_product_category_name', 'name'),
    )


class ProductAttribute(Base):
    """
    Product attribute definition (e.g., Color, Size, Material)
    Defines what attributes a product can have
    """
    __tablename__ = "product_attributes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    
    # Attribute definition
    name = Column(String(100), nullable=False)  # "Color", "Size", "Material"
    display_name = Column(String(200))  # User-friendly name
    attribute_type = Column(Enum(AttributeType), nullable=False)
    
    # Attribute settings
    required = Column(Boolean, default=False)
    affects_price = Column(Boolean, default=False)
    affects_inventory = Column(Boolean, default=True)
    affects_shipping = Column(Boolean, default=False)
    
    # Display settings
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Validation rules
    validation_rules = Column(JSON, default=dict)  # Min/max values, regex patterns, etc.
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="attributes")
    values = relationship("ProductAttributeValue", back_populates="attribute", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_product_attribute_product', 'product_id'),
        Index('idx_product_attribute_name', 'name'),
        UniqueConstraint('product_id', 'name', name='uq_product_attribute_name'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert attribute to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "attribute_type": self.attribute_type.value,
            "required": self.required,
            "affects_price": self.affects_price,
            "affects_inventory": self.affects_inventory,
            "affects_shipping": self.affects_shipping,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "validation_rules": self.validation_rules,
            "values": [value.to_dict() for value in self.values]
        }


class ProductAttributeValue(Base):
    """
    Possible values for product attributes (e.g., Red, Blue, Green for Color)
    """
    __tablename__ = "product_attribute_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey('product_attributes.id'), nullable=False, index=True)
    
    # Value definition
    value = Column(String(200), nullable=False)  # "Red", "Large", "Cotton"
    display_name = Column(String(200))  # User-friendly display name
    
    # Type-specific data
    color_code = Column(String(7))      # Hex color code for color attributes
    numeric_value = Column(Numeric(15, 4))  # Numeric value for size/weight attributes
    file_url = Column(String(500))      # File URL for file attributes
    
    # Display and ordering
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    attribute = relationship("ProductAttribute", back_populates="values")
    
    __table_args__ = (
        Index('idx_product_attribute_value_attribute', 'attribute_id'),
        Index('idx_product_attribute_value_value', 'value'),
        UniqueConstraint('attribute_id', 'value', name='uq_attribute_value'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert attribute value to dictionary"""
        return {
            "id": str(self.id),
            "value": self.value,
            "display_name": self.display_name or self.value,
            "color_code": self.color_code,
            "numeric_value": float(self.numeric_value) if self.numeric_value else None,
            "file_url": self.file_url,
            "display_order": self.display_order,
            "is_active": self.is_active
        }


class ProductVariant(Base):
    """
    Product variant model - specific combinations of attributes
    (e.g., Red T-shirt Size Large, Blue Shoes Size 42)
    """
    __tablename__ = "product_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    
    # Variant identification
    variant_code = Column(String(100), unique=True, index=True)
    sku = Column(String(100), unique=True, index=True)
    barcode = Column(String(50), unique=True, index=True)
    
    # Variant name and description
    name = Column(String(255))  # Auto-generated from attributes
    description = Column(Text)
    
    # Variant-specific pricing (overrides base product pricing)
    cost_price = Column(Numeric(15, 4))
    selling_price = Column(Numeric(15, 4))
    wholesale_price = Column(Numeric(15, 4))
    
    # Variant-specific measurements
    weight = Column(Numeric(10, 3))  # kg
    length = Column(Numeric(10, 3))  # cm
    width = Column(Numeric(10, 3))   # cm
    height = Column(Numeric(10, 3))  # cm
    
    # Inventory tracking
    stock_quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    minimum_stock_level = Column(Integer, default=0)
    
    # Variant-specific settings
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)  # Default variant for the product
    
    # Images and media specific to this variant
    primary_image_url = Column(String(500))
    image_urls = Column(JSON, default=list)
    
    # Attribute combination for this variant
    attribute_values = Column(JSON, nullable=False)  # {"color": "red", "size": "large"}
    
    # Supplier information
    supplier_code = Column(String(50))
    lead_time_days = Column(Integer, default=0)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="variants")
    
    __table_args__ = (
        Index('idx_product_variant_product', 'product_id'),
        Index('idx_product_variant_code', 'variant_code'),
        Index('idx_product_variant_sku', 'sku'),
        Index('idx_product_variant_active', 'is_active'),
        # GIN index for efficient JSON queries (supports @>, ?, ?&, ?| operators)
        Index('idx_product_variant_attributes', 'attribute_values', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<ProductVariant(id={self.id}, code='{self.variant_code}', name='{self.name}')>"
    
    @property
    def available_quantity(self) -> int:
        """Get available stock quantity"""
        return max(0, self.stock_quantity - self.reserved_quantity)
    
    @property
    def is_in_stock(self) -> bool:
        """Check if variant is in stock"""
        return self.available_quantity > 0
    
    @property
    def is_low_stock(self) -> bool:
        """Check if variant is below minimum stock level"""
        return self.stock_quantity <= self.minimum_stock_level
    
    @property
    def effective_selling_price(self) -> Decimal:
        """Get effective selling price (variant price or base product price)"""
        return self.selling_price or self.product.base_selling_price
    
    @property
    def effective_cost_price(self) -> Decimal:
        """Get effective cost price (variant price or base product price)"""
        return self.cost_price or self.product.base_cost_price
    
    @property
    def effective_weight(self) -> Optional[Decimal]:
        """Get effective weight (variant weight or base product weight)"""
        return self.weight or self.product.base_weight
    
    def matches_attributes(self, attributes: Dict[str, str]) -> bool:
        """Check if this variant matches the given attribute combination"""
        if not self.attribute_values:
            return not attributes
        
        for key, value in attributes.items():
            if self.attribute_values.get(key) != value:
                return False
        
        return True
    
    def get_attribute_display_name(self) -> str:
        """Get human-readable attribute combination"""
        if not self.attribute_values:
            return ""
        
        parts = []
        for key, value in self.attribute_values.items():
            parts.append(f"{key.title()}: {value}")
        
        return ", ".join(parts)
    
    def generate_name(self) -> str:
        """Auto-generate variant name from product name and attributes"""
        base_name = self.product.name
        attr_display = self.get_attribute_display_name()
        
        if attr_display:
            return f"{base_name} ({attr_display})"
        return base_name
    
    def generate_variant_code(self) -> str:
        """Auto-generate variant code from product code and attributes"""
        base_code = self.product.product_code
        if not self.attribute_values:
            return base_code
        
        suffix_parts = []
        for value in self.attribute_values.values():
            # Take first 3 chars of each attribute value
            suffix_parts.append(value[:3].upper())
        
        suffix = "-".join(suffix_parts)
        return f"{base_code}-{suffix}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert variant to dictionary for API responses"""
        return {
            "id": str(self.id),
            "product_id": str(self.product_id),
            "variant_code": self.variant_code,
            "sku": self.sku,
            "barcode": self.barcode,
            "name": self.name,
            "description": self.description,
            "cost_price": float(self.cost_price) if self.cost_price else None,
            "selling_price": float(self.selling_price) if self.selling_price else None,
            "wholesale_price": float(self.wholesale_price) if self.wholesale_price else None,
            "effective_selling_price": float(self.effective_selling_price),
            "effective_cost_price": float(self.effective_cost_price),
            "weight": float(self.weight) if self.weight else None,
            "length": float(self.length) if self.length else None,
            "width": float(self.width) if self.width else None,
            "height": float(self.height) if self.height else None,
            "effective_weight": float(self.effective_weight) if self.effective_weight else None,
            "stock_quantity": self.stock_quantity,
            "reserved_quantity": self.reserved_quantity,
            "available_quantity": self.available_quantity,
            "minimum_stock_level": self.minimum_stock_level,
            "is_in_stock": self.is_in_stock,
            "is_low_stock": self.is_low_stock,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "primary_image_url": self.primary_image_url,
            "image_urls": self.image_urls,
            "attribute_values": self.attribute_values,
            "attribute_display_name": self.get_attribute_display_name(),
            "supplier_code": self.supplier_code,
            "lead_time_days": self.lead_time_days,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ProductInventory(Base):
    """
    Product inventory tracking model
    For simple products (non-variant) inventory tracking
    """
    __tablename__ = "product_inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    
    # Location/warehouse information
    location_id = Column(UUID(as_uuid=True))  # Warehouse/location ID
    location_name = Column(String(200))
    
    # Inventory quantities
    stock_quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    minimum_stock_level = Column(Integer, default=0)
    maximum_stock_level = Column(Integer)
    reorder_quantity = Column(Integer, default=0)
    
    # Inventory values
    average_cost = Column(Numeric(15, 4), default=0)
    last_cost = Column(Numeric(15, 4), default=0)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    
    __table_args__ = (
        Index('idx_product_inventory_product', 'product_id'),
        Index('idx_product_inventory_location', 'location_id'),
        UniqueConstraint('product_id', 'location_id', name='uq_product_inventory_location'),
    )
    
    @property
    def available_quantity(self) -> int:
        """Get available stock quantity"""
        return max(0, self.stock_quantity - self.reserved_quantity)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert inventory to dictionary"""
        return {
            "id": str(self.id),
            "product_id": str(self.product_id),
            "location_id": str(self.location_id) if self.location_id else None,
            "location_name": self.location_name,
            "stock_quantity": self.stock_quantity,
            "reserved_quantity": self.reserved_quantity,
            "available_quantity": self.available_quantity,
            "minimum_stock_level": self.minimum_stock_level,
            "maximum_stock_level": self.maximum_stock_level,
            "reorder_quantity": self.reorder_quantity,
            "average_cost": float(self.average_cost),
            "last_cost": float(self.last_cost)
        } 