"""
Contact Company History model for Greek ERP/CRM System
Tracks contact relationships with companies over time
Enables proper CRM history when contacts change companies
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class RelationshipType(enum.Enum):
    """Type of relationship between contact and company"""
    EMPLOYEE = "employee"
    CONTRACTOR = "contractor"
    CONSULTANT = "consultant"
    PARTNER = "partner"
    CUSTOMER_CONTACT = "customer_contact"
    SUPPLIER_CONTACT = "supplier_contact"
    VENDOR_CONTACT = "vendor_contact"
    DECISION_MAKER = "decision_maker"
    INFLUENCER = "influencer"
    GATEKEEPER = "gatekeeper"
    TECHNICAL_CONTACT = "technical_contact"
    BILLING_CONTACT = "billing_contact"
    SUPPORT_CONTACT = "support_contact"


class RelationshipStatus(enum.Enum):
    """Status of the relationship"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ENDED = "ended"
    SUSPENDED = "suspended"
    PENDING = "pending"


class ContactCompanyHistory(Base):
    """
    Contact Company History model for Greek ERP/CRM system
    Tracks relationships between contacts and companies over time
    Enables contact mobility and relationship history tracking
    """
    __tablename__ = "contact_company_history"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (the CRM owner's company)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Relationship participants
    contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'), nullable=False, index=True)
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    
    # Relationship details
    relationship_type = Column(Enum(RelationshipType), nullable=False, index=True)
    status = Column(Enum(RelationshipStatus), nullable=False, default=RelationshipStatus.ACTIVE)
    
    # Position and role details
    job_title = Column(String(100))
    department = Column(String(100))
    division = Column(String(100))
    seniority_level = Column(String(50))  # "junior", "mid", "senior", "executive", "c-level"
    
    # Authority and decision-making power
    is_decision_maker = Column(Boolean, default=False)
    is_budget_holder = Column(Boolean, default=False)
    is_influencer = Column(Boolean, default=False)
    is_gatekeeper = Column(Boolean, default=False)
    decision_scope = Column(String(255))  # What decisions they can make
    budget_authority = Column(String(100))  # Budget amount they control
    
    # Reporting structure
    reports_to_contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'))
    manages_team = Column(Boolean, default=False)
    team_size = Column(Integer)
    
    # Relationship timeline
    start_date = Column(DateTime, nullable=False, default=func.now())
    end_date = Column(DateTime)
    is_current = Column(Boolean, default=True, index=True)
    
    # How the relationship was established
    source = Column(String(100))  # "referral", "linkedin", "cold_outreach", "event", etc.
    introduction_method = Column(String(100))
    referrer_contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'))
    
    # Relationship quality and engagement
    relationship_strength = Column(String(20), default="unknown")  # "strong", "moderate", "weak", "unknown"
    engagement_level = Column(String(20), default="low")  # "high", "medium", "low"
    last_interaction_date = Column(DateTime)
    interaction_frequency = Column(String(50))  # "daily", "weekly", "monthly", "quarterly", "rarely"
    
    # Communication preferences specific to this relationship
    preferred_contact_method = Column(String(50))  # "email", "phone", "in_person", "chat"
    communication_style = Column(String(50))  # "formal", "casual", "brief", "detailed"
    best_contact_time = Column(String(100))  # "morning", "afternoon", "business_hours_only"
    timezone = Column(String(50), default="Europe/Athens")
    
    # Business context
    primary_interest = Column(String(255))  # What they're primarily interested in
    pain_points = Column(Text)  # Their main challenges
    goals = Column(Text)  # Their objectives
    influence_areas = Column(JSON, default=list)  # What areas they influence ["purchasing", "technology", "budget"]
    
    # Greek business context
    speaks_greek = Column(Boolean, default=True)
    speaks_english = Column(Boolean, default=False)
    preferred_language = Column(String(2), default="el")
    local_business_network = Column(Text)  # Their local connections
    
    # CRM assignment and ownership
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Account manager
    assigned_team = Column(String(100))  # Sales team responsible
    
    # Opportunity and pipeline context
    opportunity_influence = Column(String(50))  # "champion", "supporter", "neutral", "blocker"
    buying_role = Column(String(50))  # "initiator", "influencer", "decider", "buyer", "user", "gatekeeper"
    
    # Interaction and engagement metrics
    total_meetings = Column(Integer, default=0)
    total_calls = Column(Integer, default=0)
    total_emails = Column(Integer, default=0)
    total_social_interactions = Column(Integer, default=0)
    
    # Relationship events and milestones
    first_meeting_date = Column(DateTime)
    last_meeting_date = Column(DateTime)
    key_milestones = Column(JSON, default=list)  # Important events in the relationship
    
    # Notes and observations
    relationship_notes = Column(Text)
    personal_notes = Column(Text)  # Personal interests, family, hobbies
    business_intelligence = Column(Text)  # Business insights they've shared
    
    # Exit information (when relationship ends)
    termination_reason = Column(String(255))
    new_company = Column(String(255))  # Where they went if they left
    forwarding_contact = Column(String(255))  # Who replaced them
    exit_notes = Column(Text)
    
    # Relationship scoring and analytics
    relationship_score = Column(Integer, default=0)  # 0-100 relationship quality score
    engagement_score = Column(Integer, default=0)  # 0-100 engagement score
    influence_score = Column(Integer, default=0)  # 0-100 influence score
    
    # Tags and categorization
    tags = Column(JSON, default=list)
    relationship_category = Column(String(100))  # Custom categorization
    
    # Privacy and compliance
    data_sharing_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    follow_up_consent = Column(Boolean, default=True)
    
    # Custom fields for extensibility
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    contact = relationship("Contact", foreign_keys=[contact_id])
    business_entity = relationship("BusinessEntity", foreign_keys=[business_entity_id])
    reports_to = relationship("Contact", foreign_keys=[reports_to_contact_id])
    referrer = relationship("Contact", foreign_keys=[referrer_contact_id])
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_contact_company_history_company', 'company_id'),
        Index('idx_contact_company_history_contact', 'contact_id'),
        Index('idx_contact_company_history_business_entity', 'business_entity_id'),
        Index('idx_contact_company_history_current', 'is_current'),
        Index('idx_contact_company_history_status', 'status'),
        Index('idx_contact_company_history_type', 'relationship_type'),
        Index('idx_contact_company_history_dates', 'start_date', 'end_date'),
        Index('idx_contact_company_history_assigned', 'assigned_user_id'),
        # Composite indexes for common queries
        Index('idx_contact_current_relationships', 'contact_id', 'is_current'),
        Index('idx_entity_current_contacts', 'business_entity_id', 'is_current'),
        Index('idx_contact_entity_timeline', 'contact_id', 'business_entity_id', 'start_date'),
    )
    
    def __repr__(self):
        return f"<ContactCompanyHistory(id={self.id}, contact_id={self.contact_id}, entity_id={self.business_entity_id}, type={self.relationship_type.value})>"
    
    @property
    def duration_days(self) -> Optional[int]:
        """Calculate relationship duration in days"""
        if not self.start_date:
            return None
        
        end = self.end_date or func.now()
        return (end - self.start_date).days
    
    @property
    def is_active_relationship(self) -> bool:
        """Check if this is an active relationship"""
        return self.status == RelationshipStatus.ACTIVE and self.is_current
    
    @property
    def authority_level(self) -> str:
        """Calculate authority level based on various factors"""
        if self.is_decision_maker and self.is_budget_holder:
            return "high"
        elif self.is_decision_maker or self.is_budget_holder:
            return "medium"
        elif self.is_influencer:
            return "medium"
        else:
            return "low"
    
    @property
    def relationship_health(self) -> str:
        """Calculate overall relationship health"""
        if self.relationship_score >= 80:
            return "excellent"
        elif self.relationship_score >= 60:
            return "good"
        elif self.relationship_score >= 40:
            return "fair"
        elif self.relationship_score >= 20:
            return "poor"
        else:
            return "at_risk"
    
    def end_relationship(self, reason: str, end_date: Optional[DateTime] = None) -> None:
        """End the current relationship"""
        self.status = RelationshipStatus.ENDED
        self.is_current = False
        self.end_date = end_date or func.now()
        self.termination_reason = reason
    
    def update_engagement_score(self) -> None:
        """Update engagement score based on interaction metrics"""
        # Simple scoring algorithm - can be enhanced
        base_score = 0
        
        # Recent interaction bonus
        if self.last_interaction_date:
            days_since = (func.now() - self.last_interaction_date).days
            if days_since <= 7:
                base_score += 30
            elif days_since <= 30:
                base_score += 20
            elif days_since <= 90:
                base_score += 10
        
        # Interaction frequency bonus
        frequency_scores = {
            "daily": 40,
            "weekly": 30,
            "monthly": 20,
            "quarterly": 10,
            "rarely": 5
        }
        base_score += frequency_scores.get(self.interaction_frequency, 0)
        
        # Total interactions bonus
        total_interactions = (self.total_meetings or 0) + (self.total_calls or 0) + (self.total_emails or 0)
        if total_interactions >= 50:
            base_score += 20
        elif total_interactions >= 20:
            base_score += 15
        elif total_interactions >= 10:
            base_score += 10
        elif total_interactions >= 5:
            base_score += 5
        
        # Authority and influence bonus
        if self.is_decision_maker:
            base_score += 10
        if self.is_budget_holder:
            base_score += 10
        if self.is_influencer:
            base_score += 5
        
        self.engagement_score = min(100, base_score)
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert relationship to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "contact_id": str(self.contact_id),
            "business_entity_id": str(self.business_entity_id),
            "relationship_type": self.relationship_type.value,
            "status": self.status.value,
            "job_title": self.job_title,
            "department": self.department,
            "division": self.division,
            "seniority_level": self.seniority_level,
            "is_decision_maker": self.is_decision_maker,
            "is_budget_holder": self.is_budget_holder,
            "is_influencer": self.is_influencer,
            "is_gatekeeper": self.is_gatekeeper,
            "decision_scope": self.decision_scope,
            "budget_authority": self.budget_authority,
            "reports_to_contact_id": str(self.reports_to_contact_id) if self.reports_to_contact_id else None,
            "manages_team": self.manages_team,
            "team_size": self.team_size,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_current": self.is_current,
            "source": self.source,
            "introduction_method": self.introduction_method,
            "referrer_contact_id": str(self.referrer_contact_id) if self.referrer_contact_id else None,
            "relationship_strength": self.relationship_strength,
            "engagement_level": self.engagement_level,
            "last_interaction_date": self.last_interaction_date.isoformat() if self.last_interaction_date else None,
            "interaction_frequency": self.interaction_frequency,
            "preferred_contact_method": self.preferred_contact_method,
            "communication_style": self.communication_style,
            "best_contact_time": self.best_contact_time,
            "speaks_greek": self.speaks_greek,
            "speaks_english": self.speaks_english,
            "preferred_language": self.preferred_language,
            "assigned_user_id": str(self.assigned_user_id) if self.assigned_user_id else None,
            "assigned_team": self.assigned_team,
            "opportunity_influence": self.opportunity_influence,
            "buying_role": self.buying_role,
            "total_meetings": self.total_meetings,
            "total_calls": self.total_calls,
            "total_emails": self.total_emails,
            "total_social_interactions": self.total_social_interactions,
            "first_meeting_date": self.first_meeting_date.isoformat() if self.first_meeting_date else None,
            "last_meeting_date": self.last_meeting_date.isoformat() if self.last_meeting_date else None,
            "key_milestones": self.key_milestones,
            "termination_reason": self.termination_reason,
            "new_company": self.new_company,
            "forwarding_contact": self.forwarding_contact,
            "relationship_score": self.relationship_score,
            "engagement_score": self.engagement_score,
            "influence_score": self.influence_score,
            "tags": self.tags,
            "relationship_category": self.relationship_category,
            "duration_days": self.duration_days,
            "authority_level": self.authority_level,
            "relationship_health": self.relationship_health,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Include sensitive fields only if requested
        if include_sensitive:
            data.update({
                "primary_interest": self.primary_interest,
                "pain_points": self.pain_points,
                "goals": self.goals,
                "influence_areas": self.influence_areas,
                "local_business_network": self.local_business_network,
                "relationship_notes": self.relationship_notes,
                "personal_notes": self.personal_notes,
                "business_intelligence": self.business_intelligence,
                "exit_notes": self.exit_notes,
                "custom_fields": self.custom_fields,
                "data_sharing_consent": self.data_sharing_consent,
                "marketing_consent": self.marketing_consent,
                "follow_up_consent": self.follow_up_consent
            })
        
        return data 