"""
Case models for Greek ERP/CRM System
Customer service tickets, support cases, and issue management
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from ..core.database import Base


class CaseType(enum.Enum):
    """Case type classification"""
    SUPPORT_REQUEST = "support_request"       # Αίτημα υποστήριξης
    BUG_REPORT = "bug_report"                 # Αναφορά σφάλματος
    FEATURE_REQUEST = "feature_request"       # Αίτημα χαρακτηριστικού
    COMPLAINT = "complaint"                   # Παράπονο
    INQUIRY = "inquiry"                       # Ερώτηση
    REFUND_REQUEST = "refund_request"         # Αίτημα επιστροφής
    BILLING_ISSUE = "billing_issue"           # Πρόβλημα χρέωσης
    TECHNICAL_ISSUE = "technical_issue"       # Τεχνικό πρόβλημα
    ACCOUNT_ISSUE = "account_issue"           # Πρόβλημα λογαριασμού
    TRAINING_REQUEST = "training_request"     # Αίτημα εκπαίδευσης
    CONSULTATION = "consultation"             # Συμβουλευτική
    INSTALLATION_SUPPORT = "installation_support"  # Υποστήριξη εγκατάστασης
    OTHER = "other"                           # Άλλο


class CaseStatus(enum.Enum):
    """Case status"""
    NEW = "new"                     # Νέο
    OPEN = "open"                   # Ανοιχτό
    IN_PROGRESS = "in_progress"     # Σε εξέλιξη
    PENDING_CUSTOMER = "pending_customer"  # Εκκρεμεί απάντηση πελάτη
    PENDING_VENDOR = "pending_vendor"      # Εκκρεμεί vendor
    ESCALATED = "escalated"         # Κλιμακώθηκε
    RESOLVED = "resolved"           # Επιλύθηκε
    CLOSED = "closed"               # Κλείσιμο
    CANCELLED = "cancelled"         # Ακυρώθηκε
    REOPENED = "reopened"           # Επανάνοιξε


class CasePriority(enum.Enum):
    """Case priority levels"""
    LOW = "low"           # Χαμηλή
    MEDIUM = "medium"     # Μεσαία
    HIGH = "high"         # Υψηλή
    URGENT = "urgent"     # Επείγον
    CRITICAL = "critical" # Κρίσιμη


class CaseSeverity(enum.Enum):
    """Case severity levels"""
    MINOR = "minor"       # Μικρή
    MODERATE = "moderate" # Μέτρια
    MAJOR = "major"       # Μεγάλη
    CRITICAL = "critical" # Κρίσιμη


class CaseSource(enum.Enum):
    """Case source/channel"""
    EMAIL = "email"           # Email
    PHONE = "phone"           # Τηλέφωνο
    WEB_FORM = "web_form"     # Web φόρμα
    CHAT = "chat"             # Live chat
    SOCIAL_MEDIA = "social_media"  # Social media
    IN_PERSON = "in_person"   # Προσωπικά
    INTERNAL = "internal"     # Εσωτερικό
    API = "api"               # API
    MOBILE_APP = "mobile_app" # Mobile εφαρμογή
    OTHER = "other"           # Άλλο


class ResolutionType(enum.Enum):
    """Resolution type classification"""
    RESOLVED = "resolved"               # Επιλύθηκε
    WORKAROUND_PROVIDED = "workaround_provided"  # Δόθηκε προσωρινή λύση
    NOT_REPRODUCIBLE = "not_reproducible"        # Δεν αναπαράγεται
    DUPLICATE = "duplicate"             # Διπλότυπο
    WONT_FIX = "wont_fix"              # Δεν θα επιδιορθωθεί
    BY_DESIGN = "by_design"            # Σύμφωνα με το σχεδιασμό
    CUSTOMER_ERROR = "customer_error"   # Λάθος χρήστη
    THIRD_PARTY_ISSUE = "third_party_issue"  # Πρόβλημα τρίτου
    FEATURE_REQUEST = "feature_request" # Αίτημα χαρακτηριστικού
    TRAINING_PROVIDED = "training_provided"  # Παρασχέθηκε εκπαίδευση


class Case(Base):
    """
    Case model for Greek ERP/CRM system
    Represents customer service tickets and support cases
    """
    __tablename__ = "cases"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Case identification
    case_number = Column(String(50), nullable=False, unique=True, index=True)
    subject = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Case classification
    case_type = Column(Enum(CaseType), nullable=False)
    status = Column(Enum(CaseStatus), nullable=False, default=CaseStatus.NEW)
    priority = Column(Enum(CasePriority), nullable=False, default=CasePriority.MEDIUM)
    severity = Column(Enum(CaseSeverity), nullable=False, default=CaseSeverity.MODERATE)
    source = Column(Enum(CaseSource), nullable=False)
    
    # Customer/Business entity association
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), nullable=False, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'), index=True)  # Primary contact
    
    # Product/Service context
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), index=True)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), index=True)  # Related invoice
    order_number = Column(String(100))  # Related order
    
    # Assignment and ownership
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    assigned_team = Column(String(100))  # Support team
    escalated_to_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    
    # Timeline tracking
    created_date = Column(DateTime, nullable=False, default=func.now())
    first_response_date = Column(DateTime)
    last_response_date = Column(DateTime)
    resolution_date = Column(DateTime)
    closed_date = Column(DateTime)
    
    # SLA tracking
    first_response_sla_hours = Column(Integer, default=24)  # SLA for first response
    resolution_sla_hours = Column(Integer, default=72)      # SLA for resolution
    first_response_breached = Column(Boolean, default=False)
    resolution_sla_breached = Column(Boolean, default=False)
    
    # Resolution information
    resolution_type = Column(Enum(ResolutionType))
    resolution_description = Column(Text)
    resolution_time_hours = Column(Numeric(5, 2))  # Actual time to resolve
    work_time_hours = Column(Numeric(5, 2))        # Actual work time spent
    
    # Customer satisfaction
    satisfaction_rating = Column(Integer)           # 1-5 rating
    satisfaction_feedback = Column(Text)
    satisfaction_survey_sent = Column(Boolean, default=False)
    satisfaction_survey_completed = Column(Boolean, default=False)
    
    # Communication tracking
    customer_email = Column(String(255))
    customer_phone = Column(String(20))
    preferred_contact_method = Column(String(50))
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime)
    
    # Issue categorization
    category = Column(String(100))              # General category
    subcategory = Column(String(100))           # Specific subcategory
    root_cause = Column(String(255))            # Root cause analysis
    
    # Technical details
    environment = Column(String(100))           # Production, staging, etc.
    browser_version = Column(String(100))       # For web issues
    operating_system = Column(String(100))      # OS information
    error_message = Column(Text)                # Error message details
    steps_to_reproduce = Column(Text)           # How to reproduce the issue
    
    # Greek business context
    affects_compliance = Column(Boolean, default=False)  # Affects regulatory compliance
    affects_aade_integration = Column(Boolean, default=False)  # Affects AADE integration
    requires_legal_review = Column(Boolean, default=False)     # Needs legal review
    greek_regulation_reference = Column(String(255))           # Related Greek regulation
    
    # Escalation tracking
    escalation_level = Column(Integer, default=0)  # 0=L1, 1=L2, 2=L3, etc.
    escalation_reason = Column(Text)
    escalation_date = Column(DateTime)
    previous_assignee_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Knowledge base integration
    knowledge_article_id = Column(String(100))     # Related KB article
    solution_article_created = Column(Boolean, default=False)
    
    # Cost tracking
    estimated_cost = Column(Numeric(10, 2))
    actual_cost = Column(Numeric(10, 2))
    billable_to_customer = Column(Boolean, default=False)
    
    # Parent/child case relationships
    parent_case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), index=True)
    is_master_case = Column(Boolean, default=False)
    
    # Reopening tracking
    reopen_count = Column(Integer, default=0)
    last_reopened_date = Column(DateTime)
    reopen_reason = Column(Text)
    
    # Tags and custom fields
    tags = Column(JSON, default=list)
    custom_fields = Column(JSON, default=dict)
    
    # Internal notes (not visible to customer)
    internal_notes = Column(Text)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    business_entity = relationship("BusinessEntity", foreign_keys=[business_entity_id])
    contact = relationship("Contact", foreign_keys=[contact_id])
    product = relationship("Product", foreign_keys=[product_id])
    invoice = relationship("Invoice", foreign_keys=[invoice_id])
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    escalated_to_user = relationship("User", foreign_keys=[escalated_to_user_id])
    previous_assignee = relationship("User", foreign_keys=[previous_assignee_id])
    parent_case = relationship("Case", remote_side=[id], foreign_keys=[parent_case_id])
    child_cases = relationship("Case", foreign_keys=[parent_case_id], overlaps="parent_case")
    activities = relationship("Activity", back_populates="case")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_case_company', 'company_id'),
        Index('idx_case_number', 'case_number'),
        Index('idx_case_subject', 'subject'),
        Index('idx_case_type', 'case_type'),
        Index('idx_case_status', 'status'),
        Index('idx_case_priority', 'priority'),
        Index('idx_case_severity', 'severity'),
        Index('idx_case_source', 'source'),
        Index('idx_case_business_entity', 'business_entity_id'),
        Index('idx_case_contact', 'contact_id'),
        Index('idx_case_product', 'product_id'),
        Index('idx_case_assigned_user', 'assigned_user_id'),
        Index('idx_case_escalated_to', 'escalated_to_user_id'),
        Index('idx_case_created_date', 'created_date'),
        Index('idx_case_resolution_date', 'resolution_date'),
        Index('idx_case_closed_date', 'closed_date'),
        Index('idx_case_first_response_breached', 'first_response_breached'),
        Index('idx_case_resolution_sla_breached', 'resolution_sla_breached'),
        Index('idx_case_parent', 'parent_case_id'),
        Index('idx_case_follow_up', 'follow_up_required'),
        Index('idx_case_satisfaction', 'satisfaction_rating'),
        Index('idx_case_escalation_level', 'escalation_level'),
        Index('idx_case_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Case(id={self.id}, number='{self.case_number}', subject='{self.subject}', status='{self.status.value}')>"
    
    @property
    def is_open(self) -> bool:
        """Check if case is still open"""
        return self.status not in [CaseStatus.RESOLVED, CaseStatus.CLOSED, CaseStatus.CANCELLED]
    
    @property
    def is_resolved(self) -> bool:
        """Check if case is resolved"""
        return self.status in [CaseStatus.RESOLVED, CaseStatus.CLOSED]
    
    @property
    def age_hours(self) -> float:
        """Get case age in hours"""
        end_time = self.closed_date or datetime.utcnow()
        return (end_time.replace(tzinfo=None) - self.created_date.replace(tzinfo=None)).total_seconds() / 3600
    
    @property
    def age_business_hours(self) -> float:
        """Get case age in business hours (8 hours/day, 5 days/week)"""
        # Simplified calculation - in real implementation, this would account for weekends and holidays
        return self.age_hours * (5/7) * (8/24)
    
    @property
    def first_response_time_hours(self) -> Optional[float]:
        """Get first response time in hours"""
        if not self.first_response_date:
            return None
        return (self.first_response_date.replace(tzinfo=None) - self.created_date.replace(tzinfo=None)).total_seconds() / 3600
    
    @property
    def is_first_response_overdue(self) -> bool:
        """Check if first response is overdue"""
        if self.first_response_date or not self.first_response_sla_hours:
            return False
        hours_since_creation = (datetime.utcnow() - self.created_date.replace(tzinfo=None)).total_seconds() / 3600
        return hours_since_creation > self.first_response_sla_hours
    
    @property
    def is_resolution_overdue(self) -> bool:
        """Check if resolution is overdue"""
        if self.resolution_date or not self.resolution_sla_hours:
            return False
        hours_since_creation = (datetime.utcnow() - self.created_date.replace(tzinfo=None)).total_seconds() / 3600
        return hours_since_creation > self.resolution_sla_hours
    
    @property
    def time_until_first_response_breach(self) -> Optional[timedelta]:
        """Get time until first response SLA breach"""
        if self.first_response_date or not self.first_response_sla_hours:
            return None
        
        sla_deadline = self.created_date + timedelta(hours=self.first_response_sla_hours)
        remaining = sla_deadline.replace(tzinfo=None) - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    @property
    def time_until_resolution_breach(self) -> Optional[timedelta]:
        """Get time until resolution SLA breach"""
        if self.resolution_date or not self.resolution_sla_hours:
            return None
        
        sla_deadline = self.created_date + timedelta(hours=self.resolution_sla_hours)
        remaining = sla_deadline.replace(tzinfo=None) - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    @property
    def needs_attention(self) -> bool:
        """Check if case needs immediate attention"""
        return (
            self.priority in [CasePriority.URGENT, CasePriority.CRITICAL] or
            self.is_first_response_overdue or
            self.is_resolution_overdue or
            self.status == CaseStatus.ESCALATED
        )
    
    def escalate(self, escalated_to_user_id: str, reason: str, escalation_level: int = None) -> None:
        """Escalate the case to another user or team"""
        self.previous_assignee_id = self.assigned_user_id
        self.escalated_to_user_id = escalated_to_user_id
        self.escalation_reason = reason
        self.escalation_date = func.now()
        self.status = CaseStatus.ESCALATED
        
        if escalation_level is not None:
            self.escalation_level = escalation_level
        else:
            self.escalation_level = (self.escalation_level or 0) + 1
    
    def assign_to(self, user_id: str, team: str = None) -> None:
        """Assign case to a user"""
        self.assigned_user_id = user_id
        if team:
            self.assigned_team = team
        
        # Reset escalation if case was escalated
        if self.status == CaseStatus.ESCALATED:
            self.status = CaseStatus.IN_PROGRESS
    
    def mark_first_response(self) -> None:
        """Mark the first response as sent"""
        if not self.first_response_date:
            self.first_response_date = func.now()
            
            # Check if SLA was breached
            if self.first_response_sla_hours:
                response_time = self.first_response_time_hours
                if response_time and response_time > self.first_response_sla_hours:
                    self.first_response_breached = True
    
    def resolve_case(self, resolution_type: ResolutionType, resolution_description: str, 
                    work_hours: float = None) -> None:
        """Resolve the case"""
        self.status = CaseStatus.RESOLVED
        self.resolution_date = func.now()
        self.resolution_type = resolution_type
        self.resolution_description = resolution_description
        
        if work_hours:
            self.work_time_hours = work_hours
        
        # Calculate resolution time
        self.resolution_time_hours = self.age_hours
        
        # Check if resolution SLA was breached
        if self.resolution_sla_hours and self.resolution_time_hours > self.resolution_sla_hours:
            self.resolution_sla_breached = True
    
    def close_case(self, closing_notes: str = None) -> None:
        """Close the case"""
        self.status = CaseStatus.CLOSED
        self.closed_date = func.now()
        
        if closing_notes:
            self.internal_notes = (self.internal_notes or "") + f"\nClosed: {closing_notes}"
    
    def reopen_case(self, reason: str) -> None:
        """Reopen a closed case"""
        self.status = CaseStatus.REOPENED
        self.reopen_count = (self.reopen_count or 0) + 1
        self.last_reopened_date = func.now()
        self.reopen_reason = reason
        
        # Clear resolution information
        self.resolution_date = None
        self.closed_date = None
        self.resolution_type = None
    
    def add_child_case(self, child_case_id: str) -> None:
        """Add a child case (for case splitting)"""
        # This would typically update the child case's parent_case_id
        # Implementation depends on how you handle the relationship
        pass
    
    def calculate_satisfaction_score(self) -> Optional[int]:
        """Calculate satisfaction score (1-100)"""
        if not self.satisfaction_rating:
            return None
        
        # Convert 1-5 rating to 1-100 scale
        return int(self.satisfaction_rating * 20)
    
    def send_satisfaction_survey(self) -> None:
        """Mark satisfaction survey as sent"""
        self.satisfaction_survey_sent = True
    
    def record_satisfaction(self, rating: int, feedback: str = None) -> None:
        """Record customer satisfaction"""
        self.satisfaction_rating = rating
        if feedback:
            self.satisfaction_feedback = feedback
        self.satisfaction_survey_completed = True
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to case"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from case"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if case has specific tag"""
        return bool(self.tags and tag in self.tags)
    
    def update_sla_settings(self, first_response_hours: int = None, resolution_hours: int = None) -> None:
        """Update SLA settings based on priority/severity"""
        if first_response_hours:
            self.first_response_sla_hours = first_response_hours
        if resolution_hours:
            self.resolution_sla_hours = resolution_hours


class CaseComment(Base):
    """
    Comments/updates on cases
    """
    __tablename__ = "case_comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False, index=True)
    
    # Comment content
    comment_text = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # Internal comment not visible to customer
    is_solution = Column(Boolean, default=False)  # This comment contains the solution
    
    # Author information
    author_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    author_name = Column(String(255))  # For external comments (customers)
    author_email = Column(String(255))
    
    # Comment metadata
    comment_type = Column(String(50), default="comment")  # "comment", "status_change", "assignment", etc.
    visibility = Column(String(50), default="all")       # "all", "internal", "customer"
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    case = relationship("Case")
    author_user = relationship("User")
    
    __table_args__ = (
        Index('idx_case_comment_case', 'case_id'),
        Index('idx_case_comment_author', 'author_user_id'),
        Index('idx_case_comment_created', 'created_at'),
        Index('idx_case_comment_internal', 'is_internal'),
    )


class CaseAttachment(Base):
    """
    File attachments for cases
    """
    __tablename__ = "case_attachments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False, index=True)
    
    # File information
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # Size in bytes
    file_type = Column(String(100))  # MIME type
    
    # Upload information
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Metadata
    description = Column(Text)
    is_public = Column(Boolean, default=True)  # Visible to customer
    
    # Relationships
    case = relationship("Case")
    uploaded_by_user = relationship("User")
    
    __table_args__ = (
        Index('idx_case_attachment_case', 'case_id'),
        Index('idx_case_attachment_uploaded_by', 'uploaded_by'),
    ) 