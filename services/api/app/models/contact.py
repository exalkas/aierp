"""
Contact model for Greek ERP/CRM System
Represents individual people within BusinessEntity (CRM contacts concept)
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class ContactType(enum.Enum):
    """Contact type classification"""
    PRIMARY = "primary"        # Main contact for the business entity
    SECONDARY = "secondary"    # Additional contact
    BILLING = "billing"        # Billing contact
    TECHNICAL = "technical"    # Technical contact
    SALES = "sales"            # Sales contact
    SUPPORT = "support"        # Support contact
    DECISION_MAKER = "decision_maker"  # Decision maker
    INFLUENCER = "influencer"  # Influencer in decision process


class ContactStatus(enum.Enum):
    """Contact status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BOUNCED = "bounced"        # Email bounced
    UNSUBSCRIBED = "unsubscribed"  # Unsubscribed from communications
    DO_NOT_CONTACT = "do_not_contact"  # Do not contact


class Contact(Base):
    """
    Contact model for Greek ERP/CRM system
    Represents individual people within BusinessEntity
    """
    __tablename__ = "contacts"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (stored in company's database)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Business entity association
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    
    # Contact identification
    contact_code = Column(String(20), unique=True, index=True)
    contact_type = Column(Enum(ContactType), nullable=False, default=ContactType.PRIMARY)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    display_name = Column(String(255), index=True)
    
    # Greek personal information
    father_name = Column(String(100))     # Greek requirement
    mother_name = Column(String(100))     # Greek requirement
    amka = Column(String(11), unique=True, index=True)  # Greek Social Security Number
    id_card_number = Column(String(20))   # Greek ID card
    
    # Professional information
    job_title = Column(String(100))
    department = Column(String(100))
    reports_to_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'))  # Manager
    
    # Contact information
    email = Column(String(255), index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    fax = Column(String(20))
    
    # Address (if different from business entity)
    address_street = Column(String(255))
    address_number = Column(String(10))
    address_city = Column(String(100))
    address_postal_code = Column(String(10))
    address_region = Column(String(100))
    address_country = Column(String(2), default="GR")
    
    # Contact status and preferences
    status = Column(Enum(ContactStatus), nullable=False, default=ContactStatus.ACTIVE)
    is_primary_contact = Column(Boolean, default=False)
    is_decision_maker = Column(Boolean, default=False)
    
    # Communication preferences
    preferred_contact_method = Column(String(20), default="email")
    language = Column(String(2), default="el")  # Greek by default
    timezone = Column(String(50), default="Europe/Athens")
    
    # Marketing preferences
    marketing_consent = Column(Boolean, default=False)
    newsletter_subscription = Column(Boolean, default=False)
    email_opt_in = Column(Boolean, default=True)
    sms_opt_in = Column(Boolean, default=False)
    
    # Professional details
    linkedin_url = Column(String(255))
    twitter_handle = Column(String(100))
    other_social_media = Column(JSON, default=dict)
    
    # CRM information
    lead_source = Column(String(100))
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Account manager
    notes = Column(Text)
    tags = Column(JSON, default=list)
    
    # Interaction tracking
    last_contact_date = Column(DateTime)
    last_email_date = Column(DateTime)
    last_call_date = Column(DateTime)
    last_meeting_date = Column(DateTime)
    total_interactions = Column(Integer, default=0)
    
    # Engagement metrics
    email_opens = Column(Integer, default=0)
    email_clicks = Column(Integer, default=0)
    email_bounces = Column(Integer, default=0)
    
    # Personal dates
    birth_date = Column(DateTime)
    anniversary_date = Column(DateTime)
    
    # Custom fields for extensibility
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    business_entity = relationship("BusinessEntity", back_populates="contacts")
    contact_methods = relationship("ContactMethod", foreign_keys="ContactMethod.contact_id", back_populates="contact")
    contact_company_history = relationship("ContactCompanyHistory", foreign_keys="ContactCompanyHistory.contact_id", back_populates="contact")
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    reports_to = relationship("Contact", remote_side=[id], foreign_keys=[reports_to_id])
    direct_reports = relationship("Contact", foreign_keys=[reports_to_id], overlaps="reports_to")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_contact_company', 'company_id'),
        Index('idx_contact_business_entity', 'business_entity_id'),
        Index('idx_contact_code', 'contact_code'),
        Index('idx_contact_type', 'contact_type'),
        Index('idx_contact_status', 'status'),
        Index('idx_contact_email', 'email'),
        Index('idx_contact_phone', 'phone'),
        Index('idx_contact_mobile', 'mobile'),
        Index('idx_contact_assigned_user', 'assigned_user_id'),
        Index('idx_contact_is_primary', 'is_primary_contact'),
        Index('idx_contact_is_decision_maker', 'is_decision_maker'),
        Index('idx_contact_name', 'first_name', 'last_name'),
        Index('idx_contact_display_name', 'display_name'),
    )
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.full_name}', email='{self.email}')>"
    
    @property
    def full_name(self) -> str:
        """Get contact's full name"""
        if self.display_name:
            return self.display_name
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self) -> str:
        """Get formatted address"""
        if not self.address_street:
            return ""
        return f"{self.address_street} {self.address_number}, {self.address_postal_code} {self.address_city}, {self.address_region}"
    
    @property
    def has_valid_amka(self) -> bool:
        """Check if contact has valid Greek AMKA"""
        return bool(self.amka and len(self.amka) == 11 and self.amka.isdigit())
    
    @property
    def age(self) -> Optional[int]:
        """Calculate age from birth date"""
        if not self.birth_date:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    @property
    def days_since_last_contact(self) -> Optional[int]:
        """Calculate days since last contact"""
        if not self.last_contact_date:
            return None
        from datetime import datetime
        return (datetime.now() - self.last_contact_date).days
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to contact"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from contact"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if contact has specific tag"""
        return bool(self.tags and tag in self.tags)
    
    def update_interaction_count(self) -> None:
        """Update interaction count"""
        self.total_interactions = (self.total_interactions or 0) + 1
        self.last_contact_date = func.now()
    
    def record_email_interaction(self) -> None:
        """Record email interaction"""
        self.last_email_date = func.now()
        self.update_interaction_count()
    
    def record_call_interaction(self) -> None:
        """Record call interaction"""
        self.last_call_date = func.now()
        self.update_interaction_count()
    
    def record_meeting_interaction(self) -> None:
        """Record meeting interaction"""
        self.last_meeting_date = func.now()
        self.update_interaction_count()
    
    def record_email_open(self) -> None:
        """Record email open"""
        self.email_opens = (self.email_opens or 0) + 1
    
    def record_email_click(self) -> None:
        """Record email click"""
        self.email_clicks = (self.email_clicks or 0) + 1
    
    def record_email_bounce(self) -> None:
        """Record email bounce"""
        self.email_bounces = (self.email_bounces or 0) + 1
        if self.email_bounces > 3:  # Auto-mark as bounced after 3 bounces
            self.status = ContactStatus.BOUNCED
    
    def get_custom_field(self, field_name: str, default: Any = None) -> Any:
        """Get custom field value"""
        return self.custom_fields.get(field_name, default) if self.custom_fields else default
    
    def set_custom_field(self, field_name: str, value: Any) -> None:
        """Set custom field value"""
        if not self.custom_fields:
            self.custom_fields = {}
        self.custom_fields[field_name] = value
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert contact to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "business_entity_id": str(self.business_entity_id),
            "contact_code": self.contact_code,
            "contact_type": self.contact_type.value,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "display_name": self.display_name,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "department": self.department,
            "reports_to_id": str(self.reports_to_id) if self.reports_to_id else None,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "fax": self.fax,
            "address": {
                "street": self.address_street,
                "number": self.address_number,
                "city": self.address_city,
                "postal_code": self.address_postal_code,
                "region": self.address_region,
                "country": self.address_country,
                "full_address": self.full_address
            },
            "status": self.status.value,
            "is_primary_contact": self.is_primary_contact,
            "is_decision_maker": self.is_decision_maker,
            "preferred_contact_method": self.preferred_contact_method,
            "language": self.language,
            "timezone": self.timezone,
            "marketing_consent": self.marketing_consent,
            "newsletter_subscription": self.newsletter_subscription,
            "email_opt_in": self.email_opt_in,
            "sms_opt_in": self.sms_opt_in,
            "linkedin_url": self.linkedin_url,
            "twitter_handle": self.twitter_handle,
            "other_social_media": self.other_social_media,
            "lead_source": self.lead_source,
            "assigned_user_id": str(self.assigned_user_id) if self.assigned_user_id else None,
            "tags": self.tags,
            "last_contact_date": self.last_contact_date.isoformat() if self.last_contact_date else None,
            "last_email_date": self.last_email_date.isoformat() if self.last_email_date else None,
            "last_call_date": self.last_call_date.isoformat() if self.last_call_date else None,
            "last_meeting_date": self.last_meeting_date.isoformat() if self.last_meeting_date else None,
            "total_interactions": self.total_interactions,
            "email_opens": self.email_opens,
            "email_clicks": self.email_clicks,
            "email_bounces": self.email_bounces,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "anniversary_date": self.anniversary_date.isoformat() if self.anniversary_date else None,
            "age": self.age,
            "days_since_last_contact": self.days_since_last_contact,
            "has_valid_amka": self.has_valid_amka,
            "custom_fields": self.custom_fields,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Include sensitive data only if requested
        if include_sensitive:
            data.update({
                "father_name": self.father_name,
                "mother_name": self.mother_name,
                "amka": self.amka,
                "id_card_number": self.id_card_number,
                "notes": self.notes
            })
        
        return data 