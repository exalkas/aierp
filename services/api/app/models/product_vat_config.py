"""
Product VAT Configuration Model
Simplified user-friendly VAT management where users configure VAT per product/service
with system suggestions and supplier invoice validation
"""

import enum
from decimal import Decimal
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..core.database import Base


class VATConfigStatus(enum.Enum):
    """Status of VAT configuration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING_REVIEW = "pending_review"


class VATSuggestionConfidence(enum.Enum):
    """Confidence level for VAT suggestions"""
    HIGH = "high"          # 90%+ confidence
    MEDIUM = "medium"      # 70-89% confidence
    LOW = "low"           # 50-69% confidence
    UNKNOWN = "unknown"    # <50% confidence


class ProductServiceTemplate(Base):
    """
    Pre-configured product/service templates for quick selection
    Admin-managed templates that users can select from dropdowns
    """
    __tablename__ = "product_service_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template identification
    name = Column(String(200), nullable=False)  # "Coffee Shop - Takeaway"
    display_name = Column(String(200), nullable=False)  # "☕ Coffee Shop - Takeaway"
    description = Column(Text)  # "Takeaway coffee and beverages"
    category = Column(String(100), nullable=False)  # "food_service", "healthcare", etc.
    
    # VAT configuration
    vat_rate = Column(Numeric(5, 2), nullable=False)
    vat_exemption_type = Column(String(50), nullable=True)
    vat_reasoning = Column(Text, nullable=False)  # Why this VAT rate applies
    legal_reference = Column(String(500), nullable=True)
    
    # Template metadata
    usage_count = Column(Integer, default=0)  # How many times selected
    business_types = Column(JSON, default=list)  # ["food_service", "hospitality"]
    keywords = Column(JSON, default=list)  # ["coffee", "takeaway", "beverage"]
    
    # Geographic applicability
    applies_to_mainland = Column(Boolean, default=True)
    applies_to_islands = Column(Boolean, default=True)
    island_vat_rate = Column(Numeric(5, 2), nullable=True)  # Auto-calculated or manual
    
    # Template status
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)  # Show in "popular" section
    display_order = Column(Integer, default=0)
    
    # Admin metadata
    created_by_system = Column(Boolean, default=True)  # System vs admin created
    admin_notes = Column(Text)  # Internal admin notes
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    __table_args__ = (
        Index('idx_product_service_template_category', 'category'),
        Index('idx_product_service_template_active', 'is_active'),
        Index('idx_product_service_template_popular', 'is_popular'),
        Index('idx_product_service_template_usage', 'usage_count'),
        Index('idx_product_service_template_name', 'name'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "category": self.category,
            "vat_rate": float(self.vat_rate),
            "vat_exemption_type": self.vat_exemption_type,
            "vat_reasoning": self.vat_reasoning,
            "legal_reference": self.legal_reference,
            "usage_count": self.usage_count,
            "business_types": self.business_types,
            "keywords": self.keywords,
            "applies_to_mainland": self.applies_to_mainland,
            "applies_to_islands": self.applies_to_islands,
            "island_vat_rate": float(self.island_vat_rate) if self.island_vat_rate else None,
            "is_popular": self.is_popular
        }


class ProductVATConfig(Base):
    """
    Product VAT configuration - user-friendly VAT management
    Users configure VAT per product/service with system suggestions
    """
    __tablename__ = "product_vat_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    
    # Template reference (if created from template)
    template_id = Column(UUID(as_uuid=True), ForeignKey('product_service_templates.id'), nullable=True, index=True)
    
    # User-configured VAT
    vat_rate = Column(Numeric(5, 2), nullable=False)  # User's chosen VAT rate
    vat_exemption_type = Column(String(50), nullable=True)  # 'exempt', 'zero_rated', null
    user_notes = Column(Text)  # User's notes about why they chose this VAT
    
    # System suggestions
    suggested_vat_rate = Column(Numeric(5, 2), nullable=True)  # System suggestion
    suggestion_confidence = Column(Enum(VATSuggestionConfidence), nullable=True)
    suggestion_reasoning = Column(Text)  # Why system suggested this rate
    user_override = Column(Boolean, default=False)  # Did user override suggestion?
    
    # Template usage tracking
    selected_from_template = Column(Boolean, default=False)  # Was created from template?
    template_modified = Column(Boolean, default=False)  # Did user modify template values?
    
    # Supplier invoice learning
    common_supplier_rates = Column(JSON, default=list)  # Rates seen from suppliers
    supplier_inconsistency_count = Column(Integer, default=0)  # How many times suppliers had different rates
    last_supplier_rate_seen = Column(Numeric(5, 2), nullable=True)
    last_supplier_date = Column(DateTime, nullable=True)
    
    # Configuration status
    status = Column(Enum(VATConfigStatus), default=VATConfigStatus.ACTIVE)
    requires_review = Column(Boolean, default=False)  # Flag for admin review
    last_reviewed = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    product = relationship("Product", back_populates="vat_config")
    template = relationship("ProductServiceTemplate")
    
    __table_args__ = (
        Index('idx_product_vat_config_company', 'company_id'),
        Index('idx_product_vat_config_product', 'product_id'),
        Index('idx_product_vat_config_template', 'template_id'),
        Index('idx_product_vat_config_status', 'status'),
        Index('idx_product_vat_config_review', 'requires_review'),
    )


class VATSuggestionRule(Base):
    """
    Admin-editable VAT suggestion rules
    Controls how the system suggests VAT rates to users
    """
    __tablename__ = "vat_suggestion_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Rule identification
    rule_name = Column(String(200), nullable=False)
    rule_code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    
    # Rule criteria (flexible matching)
    business_type = Column(String(100), nullable=True)  # 'restaurant', 'healthcare', etc.
    product_category = Column(String(100), nullable=True)  # 'food', 'services', etc.
    product_keywords = Column(JSON, default=list)  # Keywords to match in product name
    location_type = Column(String(50), nullable=True)  # 'mainland', 'aegean_islands'
    context_hints = Column(JSON, default=list)  # ['takeaway', 'dine_in', 'has_music']
    
    # Suggestion output
    suggested_rate = Column(Numeric(5, 2), nullable=False)
    confidence_level = Column(Enum(VATSuggestionConfidence), nullable=False)
    reasoning = Column(Text, nullable=False)  # Explanation for user
    legal_reference = Column(String(500), nullable=True)  # Greek law reference
    
    # Rule priority and status
    priority = Column(Integer, default=100)  # Higher number = higher priority
    is_active = Column(Boolean, default=True)
    
    # Effective dates
    effective_from = Column(DateTime, nullable=False, default=func.now())
    effective_to = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    __table_args__ = (
        Index('idx_vat_suggestion_rule_code', 'rule_code'),
        Index('idx_vat_suggestion_rule_business_type', 'business_type'),
        Index('idx_vat_suggestion_rule_category', 'product_category'),
        Index('idx_vat_suggestion_rule_active', 'is_active'),
        Index('idx_vat_suggestion_rule_priority', 'priority'),
    )


class SupplierInvoiceVATValidation(Base):
    """
    Supplier invoice VAT validation results
    Tracks inconsistencies between supplier invoices and expected VAT rates
    """
    __tablename__ = "supplier_invoice_vat_validations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), nullable=False, index=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    
    # Validation summary
    validation_status = Column(String(50), nullable=False)  # 'clean', 'has_inconsistencies', 'needs_review'
    total_inconsistencies = Column(Integer, default=0)
    total_items_checked = Column(Integer, default=0)
    
    # Validation details (JSON for flexibility)
    validation_details = Column(JSON, default=dict)
    # Structure: {
    #   "line_items": [
    #     {
    #       "line_number": 1,
    #       "product_name": "Coffee",
    #       "supplier_vat_rate": 24.0,
    #       "expected_vat_rate": 13.0,
    #       "inconsistency_detected": true,
    #       "suggestion": "Supplier charged 24% VAT but takeaway coffee typically has 13% VAT",
    #       "confidence": "high"
    #     }
    #   ]
    # }
    
    # User decisions
    user_decisions = Column(JSON, default=dict)
    # Structure: {
    #   "line_1": {
    #     "action": "accept_supplier_rate",  # 'accept_supplier_rate', 'flag_for_review', 'correct_rate'
    #     "user_notes": "Supplier is correct - this is dine-in coffee",
    #     "decided_at": "2025-01-01T10:00:00Z",
    #     "decided_by": "user_id"
    #   }
    # }
    
    # Learning feedback
    improves_suggestions = Column(Boolean, default=False)  # Will this feedback improve suggestions?
    learning_data = Column(JSON, default=dict)  # Data to improve VAT suggestions
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    invoice = relationship("Invoice")
    supplier = relationship("BusinessEntity")
    
    __table_args__ = (
        Index('idx_supplier_invoice_vat_validation_company', 'company_id'),
        Index('idx_supplier_invoice_vat_validation_invoice', 'invoice_id'),
        Index('idx_supplier_invoice_vat_validation_supplier', 'supplier_id'),
        Index('idx_supplier_invoice_vat_validation_status', 'validation_status'),
    ) 