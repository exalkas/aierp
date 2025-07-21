"""
Contact Method model for Greek ERP/CRM System
Supports multiple contact methods (phones, emails, addresses) per entity
Enables top-tier CRM functionality with flexible contact management
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class ContactMethodType(enum.Enum):
    """Contact method type classification"""
    PHONE = "phone"
    MOBILE = "mobile"
    EMAIL = "email"
    ADDRESS = "address"
    FAX = "fax"
    WEBSITE = "website"
    SOCIAL_MEDIA = "social_media"


class ContactMethodStatus(enum.Enum):
    """Contact method status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    INVALID = "invalid"
    PREFERRED = "preferred"


class ContactMethod(Base):
    """
    Contact Method model for Greek ERP/CRM system
    Supports multiple contact methods per business entity or contact
    Enables flexible contact information management
    """
    __tablename__ = "contact_methods"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Entity association (can be linked to BusinessEntity OR Contact)
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'), index=True)
    
    # Contact method classification
    method_type = Column(Enum(ContactMethodType), nullable=False, index=True)
    subtype_id = Column(UUID(as_uuid=True), ForeignKey('contact_method_subtypes.id'), nullable=False, index=True)
    status = Column(Enum(ContactMethodStatus), nullable=False, default=ContactMethodStatus.ACTIVE)
    
    # Priority and preferences
    is_primary = Column(Boolean, default=False, index=True)  # Primary method of this type
    is_preferred = Column(Boolean, default=False)           # User's preferred method
    priority_order = Column(Integer, default=0)             # 1=highest, 2=second, etc.
    
    # Common fields
    value = Column(String(500), nullable=False)             # The actual contact value
    label = Column(String(100))                             # Custom label (e.g., "CEO Direct Line")
    description = Column(Text)                              # Additional notes
    
    # Phone/Mobile specific fields
    country_code = Column(String(5))                        # +30 for Greece
    area_code = Column(String(10))
    extension = Column(String(10))
    
    # Email specific fields
    verified = Column(Boolean, default=False)               # Email verification status
    bounce_count = Column(Integer, default=0)              # Email bounce tracking
    last_bounce_date = Column(DateTime)
    
    # Address specific fields (for detailed Greek addresses)
    address_street = Column(String(255))
    address_number = Column(String(10))
    address_floor = Column(String(10))                      # Greek: Όροφος
    address_apartment = Column(String(10))                  # Greek: Διαμέρισμα
    address_city = Column(String(100))
    address_postal_code = Column(String(10))
    address_region = Column(String(100))                    # Greek region
    address_country = Column(String(2), default="GR")
    address_coordinates = Column(JSON)                      # {"lat": x, "lng": y}
    
    # Website/Social Media specific
    platform_name = Column(String(100))                    # LinkedIn, Facebook, etc.
    username = Column(String(100))                         # Social media username
    url = Column(String(500))                              # Full URL
    
    # Usage tracking
    last_used = Column(DateTime)                           # When this method was last used
    usage_count = Column(Integer, default=0)              # How many times used
    
    # Validation and quality
    is_valid = Column(Boolean, default=True)              # Has been validated
    validated_date = Column(DateTime)                     # When it was validated
    validation_method = Column(String(50))                # How it was validated
    quality_score = Column(Integer)                       # 1-100 quality score
    
    # Privacy and consent (GDPR compliance)
    consent_given = Column(Boolean, default=False)        # Consent for marketing
    consent_date = Column(DateTime)                       # When consent was given
    consent_source = Column(String(100))                  # How consent was obtained
    opt_out = Column(Boolean, default=False)              # User opted out
    opt_out_date = Column(DateTime)
    
    # Operational settings
    allow_marketing = Column(Boolean, default=False)      # Can be used for marketing
    allow_notifications = Column(Boolean, default=True)   # Can be used for notifications
    business_hours_only = Column(Boolean, default=False)  # Only contact during business hours
    
    # Time-based availability (for phone numbers)
    available_from = Column(String(5))                    # "09:00"
    available_until = Column(String(5))                   # "17:00"
    timezone = Column(String(50), default="Europe/Athens")
    
    # Greek-specific validation
    is_greek_mobile = Column(Boolean, default=False)      # Greek mobile format
    mobile_provider = Column(String(50))                  # Cosmote, Vodafone, etc.
    
    # Custom fields for extensibility
    custom_fields = Column(JSON, default=dict)
    tags = Column(JSON, default=list)                     # Contact method tags
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    business_entity = relationship("BusinessEntity", foreign_keys=[business_entity_id])
    contact = relationship("Contact", foreign_keys=[contact_id])
    subtype = relationship("ContactMethodSubType", back_populates="contact_methods")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_contact_method_company', 'company_id'),
        Index('idx_contact_method_business_entity', 'business_entity_id'),
        Index('idx_contact_method_contact', 'contact_id'),
        Index('idx_contact_method_type', 'method_type'),
        Index('idx_contact_method_subtype', 'subtype_id'),
        Index('idx_contact_method_status', 'status'),
        Index('idx_contact_method_primary', 'is_primary'),
        Index('idx_contact_method_preferred', 'is_preferred'),
        Index('idx_contact_method_value', 'value'),
        Index('idx_contact_method_valid', 'is_valid'),
        # Composite indexes for common queries
        Index('idx_contact_method_entity_type', 'business_entity_id', 'method_type'),
        Index('idx_contact_method_contact_type', 'contact_id', 'method_type'),
        Index('idx_contact_method_primary_by_type', 'business_entity_id', 'method_type', 'is_primary'),
    )
    
    def __repr__(self):
        subtype_code = self.subtype.code if self.subtype else "unknown"
        return f"<ContactMethod(id={self.id}, type={self.method_type.value}, subtype={subtype_code}, value='{self.value}')>"
    
    @property
    def formatted_value(self) -> str:
        """Get formatted contact method value based on type"""
        if self.method_type == ContactMethodType.PHONE or self.method_type == ContactMethodType.MOBILE:
            if self.country_code and self.area_code:
                return f"{self.country_code} {self.area_code} {self.value}"
            return self.value
        elif self.method_type == ContactMethodType.ADDRESS:
            return self.formatted_address
        return self.value
    
    @property
    def formatted_address(self) -> str:
        """Get formatted address for Greek addresses"""
        if not self.address_street:
            return self.value
        
        parts = [f"{self.address_street} {self.address_number}"]
        if self.address_floor:
            parts.append(f"Όροφος {self.address_floor}")
        if self.address_apartment:
            parts.append(f"Διαμ. {self.address_apartment}")
        
        address_line = ", ".join(parts)
        
        if self.address_postal_code and self.address_city:
            address_line += f", {self.address_postal_code} {self.address_city}"
        
        if self.address_region:
            address_line += f", {self.address_region}"
            
        return address_line
    
    @property
    def display_label(self) -> str:
        """Get display label for UI"""
        if self.label:
            return self.label
        
        # Generate label based on type and subtype
        type_name = self.method_type.value.title()
        subtype_name = self.subtype.display_name if self.subtype else "Unknown"
        
        if self.is_primary:
            return f"Primary {subtype_name} {type_name}"
        return f"{subtype_name} {type_name}"
    
    def validate_value(self) -> bool:
        """Validate the contact method value based on type"""
        if self.method_type == ContactMethodType.EMAIL:
            # Basic email validation
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(email_pattern, self.value))
        
        elif self.method_type in [ContactMethodType.PHONE, ContactMethodType.MOBILE]:
            # Greek phone validation
            if self.value.startswith('+30'):
                # Remove country code for validation
                number = self.value[3:].replace(' ', '').replace('-', '')
                
                if self.method_type == ContactMethodType.MOBILE:
                    # Greek mobile: 69XXXXXXXX (10 digits total)
                    return len(number) == 10 and number.startswith('69')
                else:
                    # Greek landline: 2XXXXXXXXX (10 digits total) 
                    return len(number) == 10 and number.startswith('2')
            
            # International format basic validation
            return len(self.value.replace('+', '').replace(' ', '').replace('-', '')) >= 10
        
        elif self.method_type == ContactMethodType.WEBSITE:
            # Basic URL validation
            return self.value.startswith(('http://', 'https://'))
        
        return True  # Default to valid for other types
    
    def mark_as_used(self) -> None:
        """Mark this contact method as recently used"""
        self.last_used = func.now()
        self.usage_count = (self.usage_count or 0) + 1
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert contact method to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "business_entity_id": str(self.business_entity_id) if self.business_entity_id else None,
            "contact_id": str(self.contact_id) if self.contact_id else None,
            "method_type": self.method_type.value,
            "subtype_id": str(self.subtype_id) if self.subtype_id else None,
            "subtype": self.subtype.to_dict() if self.subtype else None,
            "status": self.status.value,
            "value": self.value,
            "formatted_value": self.formatted_value,
            "label": self.label,
            "display_label": self.display_label,
            "description": self.description,
            "is_primary": self.is_primary,
            "is_preferred": self.is_preferred,
            "priority_order": self.priority_order,
            "is_valid": self.is_valid,
            "validated_date": self.validated_date.isoformat() if self.validated_date else None,
            "quality_score": self.quality_score,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "usage_count": self.usage_count,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Type-specific fields
        if self.method_type in [ContactMethodType.PHONE, ContactMethodType.MOBILE]:
            data.update({
                "country_code": self.country_code,
                "area_code": self.area_code,
                "extension": self.extension,
                "available_from": self.available_from,
                "available_until": self.available_until,
                "business_hours_only": self.business_hours_only
            })
        
        elif self.method_type == ContactMethodType.EMAIL:
            data.update({
                "verified": self.verified,
                "bounce_count": self.bounce_count,
                "last_bounce_date": self.last_bounce_date.isoformat() if self.last_bounce_date else None
            })
        
        elif self.method_type == ContactMethodType.ADDRESS:
            data.update({
                "address": {
                    "street": self.address_street,
                    "number": self.address_number,
                    "floor": self.address_floor,
                    "apartment": self.address_apartment,
                    "city": self.address_city,
                    "postal_code": self.address_postal_code,
                    "region": self.address_region,
                    "country": self.address_country,
                    "formatted": self.formatted_address,
                    "coordinates": self.address_coordinates
                }
            })
        
        elif self.method_type in [ContactMethodType.WEBSITE, ContactMethodType.SOCIAL_MEDIA]:
            data.update({
                "platform_name": self.platform_name,
                "username": self.username,
                "url": self.url
            })
        
        # Include sensitive fields only if requested
        if include_sensitive:
            data.update({
                "custom_fields": self.custom_fields,
                "consent_given": self.consent_given,
                "consent_date": self.consent_date.isoformat() if self.consent_date else None,
                "opt_out": self.opt_out,
                "allow_marketing": self.allow_marketing,
                "allow_notifications": self.allow_notifications
            })
        
        return data 