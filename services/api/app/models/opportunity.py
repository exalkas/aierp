"""
Opportunity models for Greek ERP/CRM System
Sales pipeline, deals, and opportunity management
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


class OpportunityStage(enum.Enum):
    """Sales pipeline stages"""
    PROSPECTING = "prospecting"         # Εξερεύνηση
    QUALIFICATION = "qualification"     # Αξιολόγηση
    NEEDS_ANALYSIS = "needs_analysis"   # Ανάλυση αναγκών
    PROPOSAL = "proposal"               # Προσφορά
    NEGOTIATION = "negotiation"         # Διαπραγμάτευση
    DECISION = "decision"               # Απόφαση
    CLOSED_WON = "closed_won"           # Κλείσιμο - Κέρδος
    CLOSED_LOST = "closed_lost"         # Κλείσιμο - Απώλεια
    ON_HOLD = "on_hold"                 # Σε αναμονή


class OpportunityType(enum.Enum):
    """Opportunity type classification"""
    NEW_BUSINESS = "new_business"       # Νέα δουλειά
    EXISTING_BUSINESS = "existing_business"  # Υπάρχουσα δουλειά
    UPSELL = "upsell"                   # Αναβάθμιση
    CROSS_SELL = "cross_sell"           # Διασταυρούμενη πώληση
    RENEWAL = "renewal"                 # Ανανέωση
    REPLACEMENT = "replacement"         # Αντικατάσταση


class OpportunityPriority(enum.Enum):
    """Opportunity priority levels"""
    LOW = "low"           # Χαμηλή
    MEDIUM = "medium"     # Μεσαία
    HIGH = "high"         # Υψηλή
    CRITICAL = "critical" # Κρίσιμη


class OpportunitySource(enum.Enum):
    """Source of the opportunity"""
    LEAD_CONVERSION = "lead_conversion"    # Μετατροπή lead
    REFERRAL = "referral"                  # Παραπομπή
    WEBSITE = "website"                    # Website
    COLD_OUTREACH = "cold_outreach"        # Ψυχρή προσέγγιση
    MARKETING_CAMPAIGN = "marketing_campaign"  # Καμπάνια μάρκετινγκ
    PARTNER = "partner"                    # Συνεργάτης
    TRADE_SHOW = "trade_show"              # Έκθεση
    EXISTING_CUSTOMER = "existing_customer" # Υπάρχων πελάτης
    OTHER = "other"                        # Άλλο


class CompetitorAction(enum.Enum):
    """Competitor action types"""
    PROPOSAL_SUBMITTED = "proposal_submitted"  # Κατέθεσε προσφορά
    PRICE_REDUCTION = "price_reduction"        # Μείωση τιμής
    FEATURE_ENHANCEMENT = "feature_enhancement" # Βελτίωση χαρακτηριστικών
    SERVICE_UPGRADE = "service_upgrade"        # Αναβάθμιση υπηρεσίας
    RELATIONSHIP_LEVERAGE = "relationship_leverage"  # Αξιοποίηση σχέσης


class Opportunity(Base):
    """
    Opportunity model for Greek ERP/CRM system
    Represents sales opportunities in the pipeline
    """
    __tablename__ = "opportunities"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Opportunity identification
    opportunity_number = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Business entity (customer) association
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'), index=True)  # Primary contact
    
    # Opportunity classification
    stage = Column(Enum(OpportunityStage), nullable=False, default=OpportunityStage.PROSPECTING)
    opportunity_type = Column(Enum(OpportunityType), nullable=False, default=OpportunityType.NEW_BUSINESS)
    priority = Column(Enum(OpportunityPriority), nullable=False, default=OpportunityPriority.MEDIUM)
    source = Column(Enum(OpportunitySource), nullable=False)
    
    # Financial information
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="EUR")
    expected_revenue = Column(Numeric(15, 2))  # After discounts, probability
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    # Probability and forecasting
    probability = Column(Integer, nullable=False, default=50)  # 0-100%
    weighted_amount = Column(Numeric(15, 2))  # amount * probability
    
    # Timeline information
    expected_close_date = Column(DateTime, nullable=False)
    actual_close_date = Column(DateTime)
    sales_cycle_days = Column(Integer)  # Calculated sales cycle length
    
    # Greek business specific
    requires_tender = Column(Boolean, default=False)  # Απαιτείται διαγωνισμός
    tender_deadline = Column(DateTime)
    tender_number = Column(String(100))
    is_government_opportunity = Column(Boolean, default=False)
    government_procurement_type = Column(String(100))  # Type of government procurement
    
    # Assignment and ownership
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    sales_team_members = Column(JSON, default=list)  # List of user IDs
    
    # Source tracking
    lead_id = Column(UUID(as_uuid=True), ForeignKey('leads.id'), index=True)  # If converted from lead
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id'), index=True)
    referral_source = Column(String(255))
    
    # Competitor analysis
    competitors = Column(JSON, default=list)  # List of competing companies
    competitive_advantages = Column(Text)
    competitive_threats = Column(Text)
    
    # Solution and products
    solution_description = Column(Text)
    key_requirements = Column(Text)
    decision_criteria = Column(Text)
    
    # Stakeholder analysis
    decision_makers = Column(JSON, default=list)  # List of contact IDs
    influencers = Column(JSON, default=list)       # List of contact IDs
    technical_evaluators = Column(JSON, default=list)  # List of contact IDs
    budget_approvers = Column(JSON, default=list)      # List of contact IDs
    
    # Sales process tracking
    next_step = Column(String(255))
    next_step_date = Column(DateTime)
    last_activity_date = Column(DateTime)
    
    # Proposal and contract information
    proposal_sent_date = Column(DateTime)
    proposal_deadline = Column(DateTime)
    contract_terms = Column(Text)
    payment_terms = Column(String(100))
    delivery_timeline = Column(String(100))
    
    # Win/Loss analysis
    won_reason = Column(Text)
    lost_reason = Column(Text)
    competitor_won = Column(String(255))  # Which competitor won
    lessons_learned = Column(Text)
    
    # Follow-up and renewal
    follow_up_date = Column(DateTime)
    renewal_date = Column(DateTime)
    renewal_probability = Column(Integer)  # For existing customers
    
    # Communication preferences
    preferred_communication_method = Column(String(50))
    meeting_frequency = Column(String(50))  # "weekly", "bi-weekly", etc.
    
    # Tags and classification
    tags = Column(JSON, default=list)
    industry_focus = Column(String(100))
    vertical_market = Column(String(100))
    
    # Risk assessment
    risk_factors = Column(Text)
    risk_mitigation = Column(Text)
    confidence_level = Column(Integer, default=50)  # 0-100%
    
    # Greek market specific fields
    public_sector = Column(Boolean, default=False)
    requires_certification = Column(String(255))  # Required certifications
    local_partner_required = Column(Boolean, default=False)
    language_requirements = Column(String(100))  # Greek, English, etc.
    
    # Performance metrics
    engagement_score = Column(Integer, default=0)  # Based on interactions
    response_time_hours = Column(Numeric(5, 2))   # Average response time
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    business_entity = relationship("BusinessEntity", foreign_keys=[business_entity_id])
    contact = relationship("Contact", foreign_keys=[contact_id])
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    lead = relationship("Lead", foreign_keys=[lead_id])
    campaign = relationship("Campaign", foreign_keys=[campaign_id])
    activities = relationship("Activity", back_populates="opportunity")
    quotes = relationship("Invoice", primaryjoin="and_(Invoice.original_document_id==Opportunity.id, Invoice.invoice_type=='sales_quotation')")
    orders = relationship("Invoice", primaryjoin="and_(Invoice.original_document_id==Opportunity.id, Invoice.invoice_type=='sales_order')")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_opportunity_company', 'company_id'),
        Index('idx_opportunity_number', 'opportunity_number'),
        Index('idx_opportunity_business_entity', 'business_entity_id'),
        Index('idx_opportunity_contact', 'contact_id'),
        Index('idx_opportunity_stage', 'stage'),
        Index('idx_opportunity_type', 'opportunity_type'),
        Index('idx_opportunity_priority', 'priority'),
        Index('idx_opportunity_assigned_user', 'assigned_user_id'),
        Index('idx_opportunity_lead', 'lead_id'),
        Index('idx_opportunity_campaign', 'campaign_id'),
        Index('idx_opportunity_expected_close', 'expected_close_date'),
        Index('idx_opportunity_amount', 'amount'),
        Index('idx_opportunity_probability', 'probability'),
        Index('idx_opportunity_source', 'source'),
        Index('idx_opportunity_tender', 'requires_tender'),
        Index('idx_opportunity_government', 'is_government_opportunity'),
        Index('idx_opportunity_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Opportunity(id={self.id}, number='{self.opportunity_number}', name='{self.name}', stage='{self.stage.value}')>"
    
    @property
    def is_open(self) -> bool:
        """Check if opportunity is still open"""
        return self.stage not in [OpportunityStage.CLOSED_WON, OpportunityStage.CLOSED_LOST]
    
    @property
    def is_won(self) -> bool:
        """Check if opportunity was won"""
        return self.stage == OpportunityStage.CLOSED_WON
    
    @property
    def is_lost(self) -> bool:
        """Check if opportunity was lost"""
        return self.stage == OpportunityStage.CLOSED_LOST
    
    @property
    def days_in_stage(self) -> int:
        """Get number of days in current stage"""
        # This would typically be calculated from stage history
        # For now, use updated_at as approximation
        return (datetime.utcnow() - self.updated_at.replace(tzinfo=None)).days
    
    @property
    def days_until_close(self) -> Optional[int]:
        """Get days until expected close date"""
        if not self.expected_close_date:
            return None
        delta = self.expected_close_date.replace(tzinfo=None) - datetime.utcnow()
        return delta.days
    
    @property
    def is_overdue(self) -> bool:
        """Check if opportunity is past expected close date"""
        if not self.expected_close_date or not self.is_open:
            return False
        return datetime.utcnow() > self.expected_close_date.replace(tzinfo=None)
    
    @property
    def stage_probability_mapping(self) -> int:
        """Get default probability based on stage"""
        mapping = {
            OpportunityStage.PROSPECTING: 10,
            OpportunityStage.QUALIFICATION: 20,
            OpportunityStage.NEEDS_ANALYSIS: 30,
            OpportunityStage.PROPOSAL: 50,
            OpportunityStage.NEGOTIATION: 70,
            OpportunityStage.DECISION: 80,
            OpportunityStage.CLOSED_WON: 100,
            OpportunityStage.CLOSED_LOST: 0,
            OpportunityStage.ON_HOLD: self.probability,  # Keep current
        }
        return mapping.get(self.stage, 50)
    
    def calculate_weighted_amount(self) -> Decimal:
        """Calculate weighted amount based on probability"""
        if not self.amount:
            return Decimal('0.00')
        return self.amount * (Decimal(str(self.probability)) / 100)
    
    def update_stage(self, new_stage: OpportunityStage, notes: str = None, user_id: str = None) -> None:
        """Update opportunity stage and related fields"""
        old_stage = self.stage
        self.stage = new_stage
        
        # Auto-update probability based on stage
        self.probability = self.stage_probability_mapping
        
        # Update weighted amount
        self.weighted_amount = self.calculate_weighted_amount()
        
        # Set close date if closing
        if new_stage in [OpportunityStage.CLOSED_WON, OpportunityStage.CLOSED_LOST]:
            self.actual_close_date = func.now()
            
            # Calculate sales cycle length
            if self.created_at:
                cycle_days = (datetime.utcnow() - self.created_at.replace(tzinfo=None)).days
                self.sales_cycle_days = cycle_days
        
        # TODO: Create stage history record
        # This would typically create an OpportunityStageHistory record
    
    def add_competitor(self, competitor_name: str, strengths: str = None, weaknesses: str = None) -> None:
        """Add a competitor to the opportunity"""
        if not self.competitors:
            self.competitors = []
        
        competitor = {
            "name": competitor_name,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "added_date": datetime.utcnow().isoformat()
        }
        
        # Check if competitor already exists
        existing = next((c for c in self.competitors if c.get("name") == competitor_name), None)
        if existing:
            existing.update(competitor)
        else:
            self.competitors.append(competitor)
    
    def remove_competitor(self, competitor_name: str) -> None:
        """Remove a competitor from the opportunity"""
        if self.competitors:
            self.competitors = [c for c in self.competitors if c.get("name") != competitor_name]
    
    def add_stakeholder(self, contact_id: str, role: str) -> None:
        """Add a stakeholder to the opportunity"""
        role_mapping = {
            "decision_maker": "decision_makers",
            "influencer": "influencers", 
            "technical_evaluator": "technical_evaluators",
            "budget_approver": "budget_approvers"
        }
        
        field_name = role_mapping.get(role)
        if not field_name:
            return
            
        stakeholder_list = getattr(self, field_name) or []
        if contact_id not in stakeholder_list:
            stakeholder_list.append(contact_id)
            setattr(self, field_name, stakeholder_list)
    
    def remove_stakeholder(self, contact_id: str, role: str = None) -> None:
        """Remove a stakeholder from the opportunity"""
        if role:
            role_mapping = {
                "decision_maker": "decision_makers",
                "influencer": "influencers", 
                "technical_evaluator": "technical_evaluators",
                "budget_approver": "budget_approvers"
            }
            field_name = role_mapping.get(role)
            if field_name:
                stakeholder_list = getattr(self, field_name) or []
                if contact_id in stakeholder_list:
                    stakeholder_list.remove(contact_id)
                    setattr(self, field_name, stakeholder_list)
        else:
            # Remove from all roles
            for field_name in ["decision_makers", "influencers", "technical_evaluators", "budget_approvers"]:
                stakeholder_list = getattr(self, field_name) or []
                if contact_id in stakeholder_list:
                    stakeholder_list.remove(contact_id)
                    setattr(self, field_name, stakeholder_list)
    
    def add_team_member(self, user_id: str) -> None:
        """Add a team member to the opportunity"""
        if not self.sales_team_members:
            self.sales_team_members = []
        if user_id not in self.sales_team_members:
            self.sales_team_members.append(user_id)
    
    def remove_team_member(self, user_id: str) -> None:
        """Remove a team member from the opportunity"""
        if self.sales_team_members and user_id in self.sales_team_members:
            self.sales_team_members.remove(user_id)
    
    def calculate_engagement_score(self) -> int:
        """Calculate engagement score based on activities and interactions"""
        # This would typically analyze related activities
        # For now, return a placeholder calculation
        score = 0
        
        # Base score from stage
        stage_scores = {
            OpportunityStage.PROSPECTING: 10,
            OpportunityStage.QUALIFICATION: 20,
            OpportunityStage.NEEDS_ANALYSIS: 40,
            OpportunityStage.PROPOSAL: 60,
            OpportunityStage.NEGOTIATION: 80,
            OpportunityStage.DECISION: 90,
        }
        score += stage_scores.get(self.stage, 0)
        
        # Bonus for stakeholder engagement
        total_stakeholders = len(self.decision_makers or []) + len(self.influencers or [])
        score += min(total_stakeholders * 5, 20)
        
        # Penalty for time in stage
        if self.days_in_stage > 30:
            score -= 10
        
        return max(0, min(score, 100))
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to opportunity"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from opportunity"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if opportunity has specific tag"""
        return bool(self.tags and tag in self.tags)


class OpportunityStageHistory(Base):
    """
    Track opportunity stage changes over time
    """
    __tablename__ = "opportunity_stage_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id = Column(UUID(as_uuid=True), ForeignKey('opportunities.id'), nullable=False, index=True)
    
    # Stage change information
    from_stage = Column(Enum(OpportunityStage))
    to_stage = Column(Enum(OpportunityStage), nullable=False)
    stage_duration_days = Column(Integer)  # Days in previous stage
    
    # Probability and amount at time of change
    probability_at_change = Column(Integer)
    amount_at_change = Column(Numeric(15, 2))
    
    # Reason and notes
    change_reason = Column(Text)
    notes = Column(Text)
    changed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Timestamp
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    opportunity = relationship("Opportunity")
    changed_by_user = relationship("User")
    
    __table_args__ = (
        Index('idx_opportunity_stage_history_opportunity', 'opportunity_id'),
        Index('idx_opportunity_stage_history_created', 'created_at'),
        Index('idx_opportunity_stage_history_to_stage', 'to_stage'),
    )


class OpportunityProduct(Base):
    """
    Products/services associated with opportunities
    """
    __tablename__ = "opportunity_products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id = Column(UUID(as_uuid=True), ForeignKey('opportunities.id'), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)
    
    # Quantity and pricing
    quantity = Column(Numeric(10, 3), nullable=False, default=1)
    unit_price = Column(Numeric(15, 4), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0)
    total_amount = Column(Numeric(15, 2), nullable=False)
    
    # Additional details
    notes = Column(Text)
    is_primary_product = Column(Boolean, default=False)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    opportunity = relationship("Opportunity")
    product = relationship("Product")
    
    __table_args__ = (
        Index('idx_opportunity_product_opportunity', 'opportunity_id'),
        Index('idx_opportunity_product_product', 'product_id'),
    ) 