"""
Contact Method Subtype model for Greek ERP/CRM System
Configurable subtypes for contact methods (replacing hardcoded enum)
Enables ultimate flexibility for contact categorization
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base
from .contact_method import ContactMethodType


class ContactMethodSubType(Base):
    """
    Contact Method SubType model for Greek ERP/CRM system
    Configurable subtypes for flexible contact method classification
    """
    __tablename__ = "contact_method_subtypes"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (for company-specific customization)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Type association
    method_type = Column(Enum(ContactMethodType), nullable=False, index=True)
    
    # Subtype definition
    code = Column(String(50), nullable=False, index=True)  # "work", "ceo_direct", "emergency"
    name = Column(String(100), nullable=False)  # "Work", "CEO Direct Line", "Emergency"
    name_greek = Column(String(100))  # "Εργασίας", "Άμεση Γραμμή CEO", "Έκτακτης Ανάγκης"
    description = Column(String(255))
    description_greek = Column(String(255))
    
    # Visual properties
    icon = Column(String(50))  # Lucide icon name: "phone", "mail", "user", "crown"
    color = Column(String(7))  # Hex color: "#3B82F6"
    
    # System properties
    is_system = Column(Boolean, default=False, nullable=False)  # System vs user-created
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)  # Default for this type
    display_order = Column(Integer, default=0)  # Sort order in UI
    
    # Usage tracking
    usage_count = Column(Integer, default=0)  # How many times used
    last_used = Column(DateTime)  # When last used
    
    # Rules and validation
    validation_rules = Column(JSON, default=dict)  # Custom validation rules
    format_template = Column(String(255))  # Display format template
    auto_suggestions = Column(JSON, default=list)  # Auto-complete suggestions
    
    # Business rules
    requires_verification = Column(Boolean, default=False)  # Requires verification
    allows_marketing = Column(Boolean, default=True)  # Can be used for marketing
    business_hours_only = Column(Boolean, default=False)  # Only during business hours
    
    # Greek-specific properties
    greek_compliance_required = Column(Boolean, default=False)
    aade_field_mapping = Column(String(100))  # AADE XML field mapping
    
    # Custom properties
    custom_properties = Column(JSON, default=dict)
    tags = Column(JSON, default=list)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    contact_methods = relationship("ContactMethod", back_populates="subtype")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_contact_method_subtype_company', 'company_id'),
        Index('idx_contact_method_subtype_type', 'method_type'),
        Index('idx_contact_method_subtype_code', 'code'),
        Index('idx_contact_method_subtype_active', 'is_active'),
        Index('idx_contact_method_subtype_system', 'is_system'),
        Index('idx_contact_method_subtype_default', 'is_default'),
        Index('idx_contact_method_subtype_order', 'display_order'),
        # Composite indexes
        Index('idx_contact_method_subtype_company_type', 'company_id', 'method_type'),
        Index('idx_contact_method_subtype_company_code', 'company_id', 'code'),
        Index('idx_contact_method_subtype_type_active', 'method_type', 'is_active'),
        # Unique constraint
        Index('idx_contact_method_subtype_unique', 'company_id', 'method_type', 'code', unique=True),
    )

    def __repr__(self):
        return f"<ContactMethodSubType(id={self.id}, type={self.method_type.value}, code={self.code}, name='{self.name}')>"
    
    @property
    def display_name(self) -> str:
        """Get display name based on language preference"""
        # This would be enhanced with proper i18n context
        return self.name_greek if self.name_greek else self.name
    
    def mark_as_used(self) -> None:
        """Mark this subtype as recently used"""
        self.last_used = func.now()
        self.usage_count = (self.usage_count or 0) + 1
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert subtype to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "method_type": self.method_type.value,
            "code": self.code,
            "name": self.name,
            "name_greek": self.name_greek,
            "display_name": self.display_name,
            "description": self.description,
            "description_greek": self.description_greek,
            "icon": self.icon,
            "color": self.color,
            "is_system": self.is_system,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "display_order": self.display_order,
            "usage_count": self.usage_count,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "validation_rules": self.validation_rules,
            "format_template": self.format_template,
            "auto_suggestions": self.auto_suggestions,
            "requires_verification": self.requires_verification,
            "allows_marketing": self.allows_marketing,
            "business_hours_only": self.business_hours_only,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                "custom_properties": self.custom_properties,
                "greek_compliance_required": self.greek_compliance_required,
                "aade_field_mapping": self.aade_field_mapping,
                "created_by": str(self.created_by) if self.created_by else None,
                "updated_by": str(self.updated_by) if self.updated_by else None
            })
        
        return data


# System default subtypes for migration and new companies
SYSTEM_DEFAULT_SUBTYPES = [
    # Phone/Mobile subtypes
    {
        "method_type": ContactMethodType.PHONE,
        "code": "work",
        "name": "Work",
        "name_greek": "Εργασίας",
        "icon": "phone",
        "color": "#3B82F6",
        "is_system": True,
        "is_default": True,
        "display_order": 1
    },
    {
        "method_type": ContactMethodType.PHONE,
        "code": "direct",
        "name": "Direct Line", 
        "name_greek": "Άμεση Γραμμή",
        "icon": "phone-call",
        "color": "#10B981",
        "is_system": True,
        "display_order": 2
    },
    {
        "method_type": ContactMethodType.PHONE,
        "code": "reception",
        "name": "Reception",
        "name_greek": "Υποδοχή",
        "icon": "phone-incoming",
        "color": "#8B5CF6",
        "is_system": True,
        "display_order": 3
    },
    {
        "method_type": ContactMethodType.MOBILE,
        "code": "work",
        "name": "Work Mobile",
        "name_greek": "Κινητό Εργασίας",
        "icon": "smartphone",
        "color": "#3B82F6",
        "is_system": True,
        "is_default": True,
        "display_order": 1
    },
    {
        "method_type": ContactMethodType.MOBILE,
        "code": "personal",
        "name": "Personal Mobile",
        "name_greek": "Προσωπικό Κινητό",
        "icon": "smartphone",
        "color": "#F59E0B",
        "is_system": True,
        "display_order": 2
    },
    
    # Email subtypes
    {
        "method_type": ContactMethodType.EMAIL,
        "code": "work",
        "name": "Work Email",
        "name_greek": "Email Εργασίας",
        "icon": "mail",
        "color": "#3B82F6",
        "is_system": True,
        "is_default": True,
        "display_order": 1
    },
    {
        "method_type": ContactMethodType.EMAIL,
        "code": "billing",
        "name": "Billing Email",
        "name_greek": "Email Τιμολόγησης",
        "icon": "receipt",
        "color": "#10B981",
        "is_system": True,
        "display_order": 2
    },
    {
        "method_type": ContactMethodType.EMAIL,
        "code": "support",
        "name": "Support Email",
        "name_greek": "Email Υποστήριξης",
        "icon": "help-circle",
        "color": "#EF4444",
        "is_system": True,
        "display_order": 3
    },
    {
        "method_type": ContactMethodType.EMAIL,
        "code": "sales",
        "name": "Sales Email",
        "name_greek": "Email Πωλήσεων",
        "icon": "trending-up",
        "color": "#F59E0B",
        "is_system": True,
        "display_order": 4
    },
    
    # Address subtypes
    {
        "method_type": ContactMethodType.ADDRESS,
        "code": "main_office",
        "name": "Main Office",
        "name_greek": "Κεντρικά Γραφεία",
        "icon": "building",
        "color": "#3B82F6",
        "is_system": True,
        "is_default": True,
        "display_order": 1
    },
    {
        "method_type": ContactMethodType.ADDRESS,
        "code": "billing",
        "name": "Billing Address",
        "name_greek": "Διεύθυνση Τιμολόγησης",
        "icon": "receipt",
        "color": "#10B981",
        "is_system": True,
        "display_order": 2
    },
    {
        "method_type": ContactMethodType.ADDRESS,
        "code": "shipping",
        "name": "Shipping Address",
        "name_greek": "Διεύθυνση Αποστολής",
        "icon": "truck",
        "color": "#F59E0B",
        "is_system": True,
        "display_order": 3
    },
    {
        "method_type": ContactMethodType.ADDRESS,
        "code": "warehouse",
        "name": "Warehouse",
        "name_greek": "Αποθήκη",
        "icon": "package",
        "color": "#8B5CF6",
        "is_system": True,
        "display_order": 4
    },
    
    # Website/Social subtypes
    {
        "method_type": ContactMethodType.WEBSITE,
        "code": "main_website",
        "name": "Main Website",
        "name_greek": "Κύρια Ιστοσελίδα",
        "icon": "globe",
        "color": "#3B82F6",
        "is_system": True,
        "is_default": True,
        "display_order": 1
    },
    {
        "method_type": ContactMethodType.SOCIAL_MEDIA,
        "code": "linkedin",
        "name": "LinkedIn",
        "name_greek": "LinkedIn",
        "icon": "linkedin",
        "color": "#0077B5",
        "is_system": True,
        "display_order": 1
    },
    {
        "method_type": ContactMethodType.SOCIAL_MEDIA,
        "code": "facebook",
        "name": "Facebook",
        "name_greek": "Facebook",
        "icon": "facebook",
        "color": "#1877F2",
        "is_system": True,
        "display_order": 2
    }
] 