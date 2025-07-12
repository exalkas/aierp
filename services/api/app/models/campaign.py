"""
Campaign models for Greek ERP/CRM System
Marketing campaigns, lead generation, and campaign management
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


class CampaignType(enum.Enum):
    """Campaign type classification"""
    EMAIL = "email"                   # Email καμπάνια
    SOCIAL_MEDIA = "social_media"     # Social media καμπάνια
    CONTENT_MARKETING = "content_marketing"  # Content marketing
    PAID_ADVERTISING = "paid_advertising"    # Πληρωμένη διαφήμιση
    TRADE_SHOW = "trade_show"         # Έκθεση/Συνέδριο
    WEBINAR = "webinar"               # Webinar
    DIRECT_MAIL = "direct_mail"       # Άμεσο ταχυδρομείο
    TELEMARKETING = "telemarketing"   # Τηλεμάρκετινγκ
    REFERRAL = "referral"             # Παραπομπές
    PARTNERSHIP = "partnership"       # Συνεργασίες
    EVENT = "event"                   # Εκδήλωση
    PR = "pr"                         # Public Relations
    RETARGETING = "retargeting"       # Retargeting
    OTHER = "other"                   # Άλλο


class CampaignStatus(enum.Enum):
    """Campaign status"""
    DRAFT = "draft"           # Προσχέδιο
    PLANNED = "planned"       # Προγραμματισμένη
    ACTIVE = "active"         # Ενεργή
    PAUSED = "paused"         # Σε παύση
    COMPLETED = "completed"   # Ολοκληρώθηκε
    CANCELLED = "cancelled"   # Ακυρώθηκε


class CampaignPriority(enum.Enum):
    """Campaign priority levels"""
    LOW = "low"           # Χαμηλή
    MEDIUM = "medium"     # Μεσαία
    HIGH = "high"         # Υψηλή
    CRITICAL = "critical" # Κρίσιμη


class CampaignObjective(enum.Enum):
    """Campaign objectives"""
    LEAD_GENERATION = "lead_generation"         # Δημιουργία leads
    BRAND_AWARENESS = "brand_awareness"         # Αναγνωρισιμότητα μάρκας
    CUSTOMER_ACQUISITION = "customer_acquisition"  # Απόκτηση πελατών
    CUSTOMER_RETENTION = "customer_retention"   # Διατήρηση πελατών
    UPSELL_CROSSSELL = "upsell_crosssell"      # Upsell/Cross-sell
    PRODUCT_LAUNCH = "product_launch"           # Λανσάρισμα προϊόντος
    EVENT_PROMOTION = "event_promotion"         # Προώθηση εκδήλωσης
    THOUGHT_LEADERSHIP = "thought_leadership"   # Thought leadership
    MARKET_RESEARCH = "market_research"         # Έρευνα αγοράς
    OTHER = "other"                             # Άλλο


class Campaign(Base):
    """
    Campaign model for Greek ERP/CRM system
    Represents marketing campaigns and lead generation activities
    """
    __tablename__ = "campaigns"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Campaign identification
    campaign_number = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Campaign classification
    campaign_type = Column(Enum(CampaignType), nullable=False)
    status = Column(Enum(CampaignStatus), nullable=False, default=CampaignStatus.DRAFT)
    priority = Column(Enum(CampaignPriority), nullable=False, default=CampaignPriority.MEDIUM)
    objective = Column(Enum(CampaignObjective), nullable=False)
    
    # Campaign timeline
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    planned_duration_days = Column(Integer)
    actual_duration_days = Column(Integer)
    
    # Budget and costs
    budget = Column(Numeric(15, 2), nullable=False, default=0)
    actual_cost = Column(Numeric(15, 2), default=0)
    cost_per_lead = Column(Numeric(10, 2))
    cost_per_acquisition = Column(Numeric(10, 2))
    roi_percentage = Column(Numeric(5, 2))
    
    # Target audience
    target_audience_description = Column(Text)
    target_demographics = Column(JSON, default=dict)
    target_geography = Column(JSON, default=list)  # List of cities/regions
    target_industries = Column(JSON, default=list)
    target_company_sizes = Column(JSON, default=list)
    
    # Campaign content and messaging
    primary_message = Column(Text)
    value_proposition = Column(Text)
    call_to_action = Column(String(255))
    landing_page_url = Column(String(500))
    
    # Channel configuration
    channels = Column(JSON, default=list)  # List of marketing channels
    channel_budget_allocation = Column(JSON, default=dict)  # Budget per channel
    
    # Email campaign specific
    email_subject_line = Column(String(255))
    email_template_id = Column(String(100))
    sender_name = Column(String(100))
    sender_email = Column(String(255))
    
    # Social media campaign specific
    social_platforms = Column(JSON, default=list)  # List of platforms
    hashtags = Column(JSON, default=list)
    
    # Paid advertising specific
    advertising_platforms = Column(JSON, default=list)  # Google Ads, Facebook, etc.
    keywords = Column(JSON, default=list)
    ad_copy = Column(Text)
    
    # Event/Trade show specific
    event_name = Column(String(255))
    event_location = Column(String(255))
    booth_number = Column(String(50))
    event_url = Column(String(500))
    
    # Greek market specific
    greek_regions_targeted = Column(JSON, default=list)  # Greek regions
    greek_business_types = Column(JSON, default=list)    # ΑΕ, ΕΠΕ, etc.
    requires_greek_content = Column(Boolean, default=True)
    gdpr_compliant = Column(Boolean, default=True)
    
    # Performance metrics and KPIs
    target_leads = Column(Integer, default=0)
    target_opportunities = Column(Integer, default=0)
    target_customers = Column(Integer, default=0)
    target_revenue = Column(Numeric(15, 2), default=0)
    
    # Actual results
    leads_generated = Column(Integer, default=0)
    opportunities_created = Column(Integer, default=0)
    customers_acquired = Column(Integer, default=0)
    revenue_generated = Column(Numeric(15, 2), default=0)
    
    # Engagement metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    click_through_rate = Column(Numeric(5, 4))  # CTR percentage
    conversion_rate = Column(Numeric(5, 4))     # Conversion percentage
    open_rate = Column(Numeric(5, 4))           # Email open rate
    bounce_rate = Column(Numeric(5, 4))         # Email bounce rate
    unsubscribe_rate = Column(Numeric(5, 4))    # Email unsubscribe rate
    
    # Lead quality metrics
    qualified_leads = Column(Integer, default=0)
    lead_qualification_rate = Column(Numeric(5, 4))
    sales_qualified_leads = Column(Integer, default=0)
    lead_to_opportunity_rate = Column(Numeric(5, 4))
    opportunity_to_customer_rate = Column(Numeric(5, 4))
    
    # Assignment and ownership
    campaign_manager_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    team_members = Column(JSON, default=list)  # List of user IDs
    
    # Approval workflow
    approval_required = Column(Boolean, default=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approved_at = Column(DateTime)
    approval_notes = Column(Text)
    
    # Campaign execution tracking
    launch_checklist = Column(JSON, default=list)
    launch_checklist_completed = Column(Boolean, default=False)
    execution_notes = Column(Text)
    
    # Integration tracking
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_content = Column(String(100))
    utm_term = Column(String(100))
    
    # External platform integration
    google_analytics_campaign = Column(String(100))
    facebook_campaign_id = Column(String(100))
    linkedin_campaign_id = Column(String(100))
    mailchimp_campaign_id = Column(String(100))
    
    # Assets and resources
    creative_assets = Column(JSON, default=list)  # URLs to images, videos, etc.
    document_assets = Column(JSON, default=list)  # URLs to PDFs, presentations
    
    # Competitor analysis
    competitor_campaigns = Column(JSON, default=list)
    competitive_advantages = Column(Text)
    
    # Post-campaign analysis
    lessons_learned = Column(Text)
    success_factors = Column(Text)
    improvement_areas = Column(Text)
    follow_up_actions = Column(Text)
    
    # Tags and categorization
    tags = Column(JSON, default=list)
    campaign_theme = Column(String(100))
    seasonal_campaign = Column(Boolean, default=False)
    
    # Custom fields
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    campaign_manager = relationship("User", foreign_keys=[campaign_manager_id])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    leads = relationship("Lead", back_populates="campaign")
    opportunities = relationship("Opportunity", back_populates="campaign")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_campaign_company', 'company_id'),
        Index('idx_campaign_number', 'campaign_number'),
        Index('idx_campaign_name', 'name'),
        Index('idx_campaign_type', 'campaign_type'),
        Index('idx_campaign_status', 'status'),
        Index('idx_campaign_priority', 'priority'),
        Index('idx_campaign_objective', 'objective'),
        Index('idx_campaign_manager', 'campaign_manager_id'),
        Index('idx_campaign_start_date', 'start_date'),
        Index('idx_campaign_end_date', 'end_date'),
        Index('idx_campaign_budget', 'budget'),
        Index('idx_campaign_leads_generated', 'leads_generated'),
        Index('idx_campaign_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Campaign(id={self.id}, number='{self.campaign_number}', name='{self.name}', type='{self.campaign_type.value}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if campaign is currently active"""
        return self.status == CampaignStatus.ACTIVE
    
    @property
    def is_completed(self) -> bool:
        """Check if campaign is completed"""
        return self.status == CampaignStatus.COMPLETED
    
    @property
    def days_running(self) -> int:
        """Get number of days campaign has been running"""
        if not self.start_date:
            return 0
        
        end = self.end_date.replace(tzinfo=None) if self.end_date else datetime.utcnow()
        return (end - self.start_date.replace(tzinfo=None)).days
    
    @property
    def days_remaining(self) -> Optional[int]:
        """Get days remaining in campaign"""
        if not self.end_date:
            return None
        
        delta = self.end_date.replace(tzinfo=None) - datetime.utcnow()
        return max(0, delta.days)
    
    @property
    def is_over_budget(self) -> bool:
        """Check if campaign is over budget"""
        return self.actual_cost > self.budget if self.budget > 0 else False
    
    @property
    def budget_utilization_percentage(self) -> float:
        """Get budget utilization percentage"""
        if not self.budget or self.budget == 0:
            return 0.0
        return float((self.actual_cost or 0) / self.budget * 100)
    
    @property
    def lead_conversion_rate(self) -> float:
        """Get lead conversion rate percentage"""
        if not self.leads_generated or self.leads_generated == 0:
            return 0.0
        return float(self.customers_acquired / self.leads_generated * 100)
    
    @property
    def opportunity_conversion_rate(self) -> float:
        """Get opportunity conversion rate percentage"""
        if not self.opportunities_created or self.opportunities_created == 0:
            return 0.0
        return float(self.customers_acquired / self.opportunities_created * 100)
    
    @property
    def effectiveness_score(self) -> int:
        """Calculate campaign effectiveness score (0-100)"""
        score = 0
        
        # Lead generation effectiveness (30 points)
        if self.target_leads > 0:
            lead_achievement = min(self.leads_generated / self.target_leads, 1.0)
            score += int(lead_achievement * 30)
        
        # Revenue effectiveness (30 points)
        if self.target_revenue > 0:
            revenue_achievement = min(float(self.revenue_generated / self.target_revenue), 1.0)
            score += int(revenue_achievement * 30)
        
        # Budget efficiency (20 points)
        if self.budget > 0:
            if self.actual_cost <= self.budget:
                score += 20
            else:
                # Penalty for going over budget
                over_budget_penalty = min((self.actual_cost - self.budget) / self.budget * 20, 20)
                score += max(0, 20 - int(over_budget_penalty))
        
        # Quality metrics (20 points)
        quality_score = 0
        if self.conversion_rate:
            quality_score += min(float(self.conversion_rate) * 100, 10)
        if self.lead_qualification_rate:
            quality_score += min(float(self.lead_qualification_rate) * 100, 10)
        score += int(quality_score)
        
        return min(score, 100)
    
    def calculate_roi(self) -> Optional[float]:
        """Calculate return on investment percentage"""
        if not self.actual_cost or self.actual_cost == 0:
            return None
        
        profit = self.revenue_generated - self.actual_cost
        return float(profit / self.actual_cost * 100)
    
    def calculate_cost_per_lead(self) -> Optional[Decimal]:
        """Calculate cost per lead"""
        if not self.leads_generated or self.leads_generated == 0:
            return None
        return self.actual_cost / self.leads_generated
    
    def calculate_cost_per_acquisition(self) -> Optional[Decimal]:
        """Calculate cost per customer acquisition"""
        if not self.customers_acquired or self.customers_acquired == 0:
            return None
        return self.actual_cost / self.customers_acquired
    
    def update_metrics(self) -> None:
        """Update calculated metrics"""
        self.cost_per_lead = self.calculate_cost_per_lead()
        self.cost_per_acquisition = self.calculate_cost_per_acquisition()
        
        roi = self.calculate_roi()
        if roi is not None:
            self.roi_percentage = Decimal(str(roi))
        
        # Update conversion rates
        if self.leads_generated > 0:
            self.lead_qualification_rate = Decimal(str(self.qualified_leads / self.leads_generated))
            self.lead_to_opportunity_rate = Decimal(str(self.opportunities_created / self.leads_generated))
        
        if self.opportunities_created > 0:
            self.opportunity_to_customer_rate = Decimal(str(self.customers_acquired / self.opportunities_created))
        
        # Update click-through rate
        if self.impressions > 0:
            self.click_through_rate = Decimal(str(self.clicks / self.impressions))
        
        # Update conversion rate
        if self.clicks > 0:
            self.conversion_rate = Decimal(str(self.leads_generated / self.clicks))
    
    def add_team_member(self, user_id: str) -> None:
        """Add a team member to the campaign"""
        if not self.team_members:
            self.team_members = []
        if user_id not in self.team_members:
            self.team_members.append(user_id)
    
    def remove_team_member(self, user_id: str) -> None:
        """Remove a team member from the campaign"""
        if self.team_members and user_id in self.team_members:
            self.team_members.remove(user_id)
    
    def add_creative_asset(self, asset_url: str, asset_type: str, description: str = None) -> None:
        """Add a creative asset to the campaign"""
        if not self.creative_assets:
            self.creative_assets = []
        
        asset = {
            "url": asset_url,
            "type": asset_type,
            "description": description,
            "added_at": datetime.utcnow().isoformat()
        }
        self.creative_assets.append(asset)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to campaign"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from campaign"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if campaign has specific tag"""
        return bool(self.tags and tag in self.tags)
    
    def complete_campaign(self, completion_notes: str = None) -> None:
        """Mark campaign as completed"""
        self.status = CampaignStatus.COMPLETED
        self.end_date = func.now()
        self.actual_duration_days = self.days_running
        
        if completion_notes:
            self.execution_notes = completion_notes
        
        # Update final metrics
        self.update_metrics()
    
    def pause_campaign(self, pause_reason: str = None) -> None:
        """Pause the campaign"""
        self.status = CampaignStatus.PAUSED
        if pause_reason:
            self.execution_notes = f"Paused: {pause_reason}"
    
    def resume_campaign(self) -> None:
        """Resume paused campaign"""
        if self.status == CampaignStatus.PAUSED:
            self.status = CampaignStatus.ACTIVE


class CampaignMetrics(Base):
    """
    Daily metrics tracking for campaigns
    """
    __tablename__ = "campaign_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=False, index=True)
    
    # Date for these metrics
    metric_date = Column(DateTime, nullable=False)
    
    # Daily metrics
    daily_impressions = Column(Integer, default=0)
    daily_clicks = Column(Integer, default=0)
    daily_leads = Column(Integer, default=0)
    daily_opportunities = Column(Integer, default=0)
    daily_customers = Column(Integer, default=0)
    daily_revenue = Column(Numeric(15, 2), default=0)
    daily_cost = Column(Numeric(15, 2), default=0)
    
    # Email specific metrics
    emails_sent = Column(Integer, default=0)
    emails_opened = Column(Integer, default=0)
    emails_clicked = Column(Integer, default=0)
    emails_bounced = Column(Integer, default=0)
    emails_unsubscribed = Column(Integer, default=0)
    
    # Social media metrics
    social_shares = Column(Integer, default=0)
    social_likes = Column(Integer, default=0)
    social_comments = Column(Integer, default=0)
    social_followers_gained = Column(Integer, default=0)
    
    # Website metrics
    website_visits = Column(Integer, default=0)
    page_views = Column(Integer, default=0)
    time_on_page_seconds = Column(Integer, default=0)
    bounce_rate_percentage = Column(Numeric(5, 2), default=0)
    
    # Conversion metrics
    form_submissions = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    demo_requests = Column(Integer, default=0)
    phone_calls = Column(Integer, default=0)
    
    # Quality metrics
    qualified_leads_daily = Column(Integer, default=0)
    sales_accepted_leads = Column(Integer, default=0)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    campaign = relationship("Campaign")
    
    __table_args__ = (
        Index('idx_campaign_metrics_campaign', 'campaign_id'),
        Index('idx_campaign_metrics_date', 'metric_date'),
        Index('idx_campaign_metrics_campaign_date', 'campaign_id', 'metric_date', unique=True),
    ) 