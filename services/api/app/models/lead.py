"""
Lead models for Greek ERP/CRM System
Lead capture, qualification, and conversion tracking
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal
from datetime import datetime

from ..core.database import Base


class LeadStatus(enum.Enum):
    """Lead status classification"""
    NEW = "new"                     # Νέο lead
    CONTACTED = "contacted"         # Επικοινωνήσαμε
    QUALIFIED = "qualified"         # Εγκεκριμένο
    PROPOSAL_SENT = "proposal_sent" # Προσφορά στάλθηκε
    NEGOTIATION = "negotiation"     # Διαπραγμάτευση
    WON = "won"                     # Κέρδος (μετατράπηκε)
    LOST = "lost"                   # Χάθηκε
    NURTURING = "nurturing"         # Ανάπτυξη σχέσης
    DISQUALIFIED = "disqualified"   # Απορρίφθηκε


class LeadSource(enum.Enum):
    """Lead source classification"""
    WEBSITE = "website"                 # Website
    REFERRAL = "referral"              # Παραπομπή
    EMAIL_CAMPAIGN = "email_campaign"   # Email καμπάνια
    SOCIAL_MEDIA = "social_media"      # Social media
    PHONE_CALL = "phone_call"          # Τηλεφωνική επαφή
    TRADE_SHOW = "trade_show"          # Έκθεση
    ADVERTISING = "advertising"         # Διαφήμιση
    PARTNER = "partner"                # Συνεργάτης
    COLD_OUTREACH = "cold_outreach"    # Ψυχρή προσέγγιση
    WALK_IN = "walk_in"                # Επίσκεψη στο κατάστημα
    OTHER = "other"                    # Άλλο


class LeadRating(enum.Enum):
    """Lead quality rating"""
    HOT = "hot"         # Καυτό (άμεση ενδιαφέρον)
    WARM = "warm"       # Ζεστό (μέτριο ενδιαφέρον)
    COLD = "cold"       # Κρύο (χαμηλό ενδιαφέρον)


class LeadQualificationCriteria(enum.Enum):
    """BANT qualification criteria"""
    BUDGET = "budget"       # Προϋπολογισμός
    AUTHORITY = "authority" # Εξουσία αγοράς
    NEED = "need"          # Ανάγκη
    TIMELINE = "timeline"   # Χρονοδιάγραμμα


class Lead(Base):
    """
    Lead model for Greek ERP/CRM system
    Represents potential customers before they become BusinessEntity records
    """
    __tablename__ = "leads"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Lead identification
    lead_number = Column(String(50), nullable=False, unique=True, index=True)
    
    # Personal/Business information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    business_name = Column(String(255))  # For B2B leads
    title = Column(String(100))          # Job title
    department = Column(String(100))
    
    # Contact information
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    website = Column(String(255))
    
    # Greek address fields
    address_street = Column(String(255))
    address_number = Column(String(10))
    address_city = Column(String(100))
    address_postal_code = Column(String(10))
    address_region = Column(String(100))
    address_country = Column(String(2), default="GR")
    
    # Lead classification
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    source = Column(Enum(LeadSource), nullable=False)
    rating = Column(Enum(LeadRating), default=LeadRating.COLD)
    
    # Greek business information (for B2B leads)
    afm = Column(String(9), index=True)    # Greek Tax Number
    doy = Column(String(10))               # Tax Office
    vat_number = Column(String(20))        # EU VAT number
    business_activity = Column(String(255))
    
    # Lead scoring and qualification
    lead_score = Column(Integer, default=0)  # 0-100 scoring
    qualification_score = Column(Integer, default=0)  # BANT score
    qualified_date = Column(DateTime)
    
    # Sales information
    estimated_value = Column(Numeric(15, 2))  # Potential deal value
    estimated_close_date = Column(DateTime)
    probability = Column(Integer, default=0)  # 0-100%
    
    # Assignment and ownership
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    assigned_date = Column(DateTime)
    
    # Lead lifecycle tracking
    first_contact_date = Column(DateTime)
    last_contact_date = Column(DateTime)
    next_follow_up_date = Column(DateTime)
    
    # Campaign tracking
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id'), index=True)
    utm_source = Column(String(100))       # UTM tracking
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_content = Column(String(100))
    utm_term = Column(String(100))
    
    # Conversion tracking
    converted = Column(Boolean, default=False)
    converted_date = Column(DateTime)
    converted_to_business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'))
    converted_to_opportunity_id = Column(UUID(as_uuid=True), ForeignKey('opportunities.id'))
    
    # Lead details
    industry = Column(String(100))
    company_size = Column(String(50))      # "1-10", "11-50", "51-200", etc.
    annual_revenue = Column(String(50))    # Revenue range
    
    # Communication preferences
    preferred_contact_method = Column(String(20), default="email")
    preferred_contact_time = Column(String(50))  # "morning", "afternoon", etc.
    language = Column(String(2), default="el")   # Greek by default
    
    # Marketing compliance
    marketing_consent = Column(Boolean, default=False)
    newsletter_subscription = Column(Boolean, default=False)
    gdpr_consent = Column(Boolean, default=False)
    gdpr_consent_date = Column(DateTime)
    
    # Lead description and notes
    description = Column(Text)
    notes = Column(Text)
    pain_points = Column(Text)           # Identified problems
    solution_interest = Column(Text)      # What solutions they're interested in
    budget_range = Column(String(50))    # Budget information
    decision_timeframe = Column(String(50))  # When they plan to decide
    
    # Qualification criteria (BANT)
    has_budget = Column(Boolean)         # Budget qualification
    has_authority = Column(Boolean)      # Authority qualification
    has_need = Column(Boolean)          # Need qualification
    has_timeline = Column(Boolean)       # Timeline qualification
    
    # Lead lifecycle automation
    auto_follow_up_enabled = Column(Boolean, default=True)
    last_email_sent = Column(DateTime)
    email_open_count = Column(Integer, default=0)
    email_click_count = Column(Integer, default=0)
    
    # Social media information
    linkedin_profile = Column(String(255))
    twitter_handle = Column(String(100))
    facebook_profile = Column(String(255))
    
    # Greek market specific
    referral_source = Column(String(255))  # Who referred them
    competitor_currently_using = Column(String(255))
    
    # Tags and classification
    tags = Column(JSON, default=list)
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    campaign = relationship("Campaign", back_populates="leads")
    converted_business_entity = relationship("BusinessEntity", foreign_keys=[converted_to_business_entity_id])
    converted_opportunity = relationship("Opportunity", foreign_keys=[converted_to_opportunity_id])
    activities = relationship("Activity", back_populates="lead")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_lead_company', 'company_id'),
        Index('idx_lead_number', 'lead_number'),
        Index('idx_lead_email', 'email'),
        Index('idx_lead_status', 'status'),
        Index('idx_lead_source', 'source'),
        Index('idx_lead_rating', 'rating'),
        Index('idx_lead_assigned_user', 'assigned_user_id'),
        Index('idx_lead_campaign', 'campaign_id'),
        Index('idx_lead_afm', 'afm'),
        Index('idx_lead_converted', 'converted'),
        Index('idx_lead_score', 'lead_score'),
        Index('idx_lead_next_follow_up', 'next_follow_up_date'),
        Index('idx_lead_business_name', 'business_name'),
        Index('idx_lead_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Lead(id={self.id}, number='{self.lead_number}', name='{self.first_name} {self.last_name}', status='{self.status.value}')>"
    
    @property
    def full_name(self) -> str:
        """Get lead's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def display_name(self) -> str:
        """Get display name (business name or full name)"""
        return self.business_name or self.full_name
    
    @property
    def is_qualified(self) -> bool:
        """Check if lead meets BANT qualification criteria"""
        return all([
            self.has_budget,
            self.has_authority,
            self.has_need,
            self.has_timeline
        ])
    
    @property
    def qualification_percentage(self) -> int:
        """Get qualification percentage based on BANT criteria"""
        criteria = [self.has_budget, self.has_authority, self.has_need, self.has_timeline]
        qualified_count = sum(1 for criterion in criteria if criterion)
        return int((qualified_count / len(criteria)) * 100)
    
    @property
    def is_hot_lead(self) -> bool:
        """Check if lead is hot (high priority)"""
        return (
            self.rating == LeadRating.HOT or
            self.lead_score >= 80 or
            self.is_qualified
        )
    
    @property
    def days_since_created(self) -> int:
        """Get days since lead was created"""
        if not self.created_at:
            return 0
        return (datetime.utcnow() - self.created_at.replace(tzinfo=None)).days
    
    @property
    def days_since_last_contact(self) -> Optional[int]:
        """Get days since last contact"""
        if not self.last_contact_date:
            return None
        return (datetime.utcnow() - self.last_contact_date.replace(tzinfo=None)).days
    
    @property
    def is_overdue_follow_up(self) -> bool:
        """Check if follow-up is overdue"""
        if not self.next_follow_up_date:
            return False
        return datetime.utcnow() > self.next_follow_up_date.replace(tzinfo=None)
    
    def calculate_lead_score(self) -> int:
        """Calculate lead score based on various factors"""
        score = 0
        
        # Source scoring
        if self.source == LeadSource.REFERRAL:
            score += 20
        elif self.source == LeadSource.WEBSITE:
            score += 15
        elif self.source == LeadSource.EMAIL_CAMPAIGN:
            score += 10
        
        # Qualification scoring
        score += self.qualification_percentage * 0.4  # Up to 40 points
        
        # Engagement scoring
        score += min(self.email_open_count * 2, 20)  # Up to 20 points
        score += min(self.email_click_count * 5, 20)  # Up to 20 points
        
        # Business information scoring
        if self.business_name:
            score += 10
        if self.afm:
            score += 10
        if self.estimated_value and self.estimated_value > 1000:
            score += 15
        
        return min(int(score), 100)  # Cap at 100
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to lead"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from lead"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if lead has specific tag"""
        return bool(self.tags and tag in self.tags)
    
    def mark_as_contacted(self) -> None:
        """Mark lead as contacted and update timestamps"""
        if self.status == LeadStatus.NEW:
            self.status = LeadStatus.CONTACTED
        
        if not self.first_contact_date:
            self.first_contact_date = func.now()
        
        self.last_contact_date = func.now()
    
    def qualify_lead(self, budget: bool = False, authority: bool = False, 
                    need: bool = False, timeline: bool = False) -> None:
        """Qualify lead using BANT criteria"""
        self.has_budget = budget
        self.has_authority = authority
        self.has_need = need
        self.has_timeline = timeline
        
        if self.is_qualified and self.status in [LeadStatus.NEW, LeadStatus.CONTACTED]:
            self.status = LeadStatus.QUALIFIED
            self.qualified_date = func.now()
        
        # Update qualification score
        self.qualification_score = self.qualification_percentage
        
        # Update overall lead score
        self.lead_score = self.calculate_lead_score()
    
    def convert_to_opportunity(self, opportunity_id: str) -> None:
        """Convert lead to opportunity"""
        self.converted = True
        self.converted_date = func.now()
        self.converted_to_opportunity_id = opportunity_id
        self.status = LeadStatus.WON
    
    def convert_to_business_entity(self, business_entity_id: str) -> None:
        """Convert lead to business entity"""
        self.converted = True
        self.converted_date = func.now()
        self.converted_to_business_entity_id = business_entity_id
        self.status = LeadStatus.WON


class LeadQualificationHistory(Base):
    """
    Track lead qualification changes over time
    """
    __tablename__ = "lead_qualification_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('leads.id'), nullable=False, index=True)
    
    # Qualification criteria at this point in time
    has_budget = Column(Boolean)
    has_authority = Column(Boolean)
    has_need = Column(Boolean)
    has_timeline = Column(Boolean)
    
    # Scores at this point
    qualification_score = Column(Integer)
    lead_score = Column(Integer)
    
    # Notes and reason for change
    notes = Column(Text)
    changed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Timestamp
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    lead = relationship("Lead")
    changed_by_user = relationship("User")
    
    __table_args__ = (
        Index('idx_lead_qualification_history_lead', 'lead_id'),
        Index('idx_lead_qualification_history_created', 'created_at'),
    ) 