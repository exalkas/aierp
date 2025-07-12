"""
Activity models for Greek ERP/CRM System
Tasks, calls, meetings, notes, and activity management
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from decimal import Decimal

from ..core.database import Base


class ActivityType(enum.Enum):
    """Activity type classification"""
    TASK = "task"               # Εργασία
    PHONE_CALL = "phone_call"   # Τηλεφωνική κλήση
    EMAIL = "email"             # Email
    MEETING = "meeting"         # Συνάντηση
    NOTE = "note"               # Σημείωση
    APPOINTMENT = "appointment" # Ραντεβού
    FOLLOW_UP = "follow_up"     # Παρακολούθηση
    DEMO = "demo"               # Demo/Παρουσίαση
    PRESENTATION = "presentation" # Παρουσίαση
    SITE_VISIT = "site_visit"   # Επίσκεψη


class ActivityStatus(enum.Enum):
    """Activity status"""
    PLANNED = "planned"         # Προγραμματισμένο
    IN_PROGRESS = "in_progress" # Σε εξέλιξη
    COMPLETED = "completed"     # Ολοκληρώθηκε
    CANCELLED = "cancelled"     # Ακυρώθηκε
    POSTPONED = "postponed"     # Αναβλήθηκε
    NO_SHOW = "no_show"        # Δεν εμφανίστηκε


class ActivityPriority(enum.Enum):
    """Activity priority levels"""
    LOW = "low"           # Χαμηλή
    MEDIUM = "medium"     # Μεσαία
    HIGH = "high"         # Υψηλή
    URGENT = "urgent"     # Επείγον


class CallDirection(enum.Enum):
    """Call direction for phone calls"""
    INBOUND = "inbound"   # Εισερχόμενη
    OUTBOUND = "outbound" # Εξερχόμενη


class CallOutcome(enum.Enum):
    """Call outcome"""
    CONNECTED = "connected"         # Συνδέθηκε
    NO_ANSWER = "no_answer"        # Δεν απάντησε
    BUSY = "busy"                  # Κατειλημμένο
    VOICEMAIL = "voicemail"        # Αυτόματος τηλεφωνητής
    WRONG_NUMBER = "wrong_number"   # Λάθος νούμερο
    INTERESTED = "interested"       # Ενδιαφέρεται
    NOT_INTERESTED = "not_interested" # Δεν ενδιαφέρεται
    CALLBACK_REQUESTED = "callback_requested" # Ζήτησε επανάκληση


class MeetingType(enum.Enum):
    """Meeting type classification"""
    SALES_MEETING = "sales_meeting"       # Συνάντηση πωλήσεων
    DISCOVERY_CALL = "discovery_call"     # Κλήση εξερεύνησης
    DEMO = "demo"                         # Demo
    PROPOSAL_PRESENTATION = "proposal_presentation" # Παρουσίαση προσφοράς
    NEGOTIATION = "negotiation"           # Διαπραγμάτευση
    CLOSING_MEETING = "closing_meeting"   # Συνάντηση κλεισίματος
    FOLLOW_UP = "follow_up"               # Παρακολούθηση
    CUSTOMER_SUPPORT = "customer_support" # Υποστήριξη πελάτη
    TRAINING = "training"                 # Εκπαίδευση
    CONSULTATION = "consultation"         # Συμβουλευτική


class Activity(Base):
    """
    Activity model for Greek ERP/CRM system
    Represents all types of activities: tasks, calls, meetings, notes
    """
    __tablename__ = "activities"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Activity identification
    activity_number = Column(String(50), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Activity classification
    activity_type = Column(Enum(ActivityType), nullable=False)
    status = Column(Enum(ActivityStatus), nullable=False, default=ActivityStatus.PLANNED)
    priority = Column(Enum(ActivityPriority), nullable=False, default=ActivityPriority.MEDIUM)
    
    # Related entities (polymorphic relationships)
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id'), index=True)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('leads.id'), index=True)
    opportunity_id = Column(UUID(as_uuid=True), ForeignKey('opportunities.id'), index=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), index=True)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id'), index=True)
    
    # Assignment and ownership
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Timing
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    due_date = Column(DateTime)
    completed_date = Column(DateTime)
    duration_minutes = Column(Integer)  # Planned or actual duration
    
    # Recurrence (for recurring activities)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50))  # "daily", "weekly", "monthly", etc.
    recurrence_interval = Column(Integer, default=1)  # Every X days/weeks/months
    recurrence_end_date = Column(DateTime)
    parent_activity_id = Column(UUID(as_uuid=True), ForeignKey('activities.id'), index=True)
    
    # Call-specific fields
    call_direction = Column(Enum(CallDirection))
    call_outcome = Column(Enum(CallOutcome))
    phone_number = Column(String(20))
    call_duration_seconds = Column(Integer)
    
    # Meeting-specific fields
    meeting_type = Column(Enum(MeetingType))
    location = Column(String(255))
    meeting_url = Column(String(500))  # For online meetings
    attendees = Column(JSON, default=list)  # List of attendee contact IDs
    meeting_agenda = Column(Text)
    meeting_minutes = Column(Text)
    
    # Email-specific fields
    email_subject = Column(String(255))
    email_to = Column(JSON, default=list)      # List of email addresses
    email_cc = Column(JSON, default=list)      # List of CC email addresses
    email_bcc = Column(JSON, default=list)     # List of BCC email addresses
    email_message_id = Column(String(255))     # Email message ID for tracking
    email_thread_id = Column(String(255))      # Email thread ID
    
    # Task-specific fields
    completion_percentage = Column(Integer, default=0)  # 0-100%
    checklist = Column(JSON, default=list)     # List of checklist items
    dependencies = Column(JSON, default=list)   # List of dependent activity IDs
    
    # Results and outcomes
    outcome_description = Column(Text)
    next_action = Column(String(255))
    next_action_date = Column(DateTime)
    follow_up_required = Column(Boolean, default=False)
    
    # Communication tracking
    communication_channel = Column(String(50))  # "phone", "email", "in_person", "video", "chat"
    response_received = Column(Boolean, default=False)
    response_date = Column(DateTime)
    
    # Greek business context
    involves_contract = Column(Boolean, default=False)
    contract_reference = Column(String(100))
    requires_documentation = Column(Boolean, default=False)
    documentation_completed = Column(Boolean, default=False)
    
    # Reminder and notification settings
    reminder_enabled = Column(Boolean, default=True)
    reminder_minutes_before = Column(Integer, default=15)  # Minutes before start_date
    reminder_sent = Column(Boolean, default=False)
    notification_settings = Column(JSON, default=dict)
    
    # Location and travel
    requires_travel = Column(Boolean, default=False)
    travel_time_minutes = Column(Integer)
    address = Column(String(500))
    city = Column(String(100))
    postal_code = Column(String(10))
    
    # Cost and billing
    estimated_cost = Column(Numeric(10, 2))
    actual_cost = Column(Numeric(10, 2))
    is_billable = Column(Boolean, default=False)
    billable_hours = Column(Numeric(5, 2))
    hourly_rate = Column(Numeric(10, 2))
    
    # Performance and satisfaction
    satisfaction_rating = Column(Integer)  # 1-5 rating
    quality_score = Column(Integer)       # 1-100 quality score
    
    # Tags and categorization
    tags = Column(JSON, default=list)
    category = Column(String(100))
    project_name = Column(String(255))
    
    # Custom fields for flexibility
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    business_entity = relationship("BusinessEntity", foreign_keys=[business_entity_id])
    contact = relationship("Contact", foreign_keys=[contact_id])
    lead = relationship("Lead", back_populates="activities", foreign_keys=[lead_id])
    opportunity = relationship("Opportunity", back_populates="activities", foreign_keys=[opportunity_id])
    case = relationship("Case", back_populates="activities", foreign_keys=[case_id])
    invoice = relationship("Invoice", foreign_keys=[invoice_id])
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
    parent_activity = relationship("Activity", remote_side=[id], foreign_keys=[parent_activity_id])
    child_activities = relationship("Activity", foreign_keys=[parent_activity_id])
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_activity_company', 'company_id'),
        Index('idx_activity_number', 'activity_number'),
        Index('idx_activity_type', 'activity_type'),
        Index('idx_activity_status', 'status'),
        Index('idx_activity_priority', 'priority'),
        Index('idx_activity_business_entity', 'business_entity_id'),
        Index('idx_activity_contact', 'contact_id'),
        Index('idx_activity_lead', 'lead_id'),
        Index('idx_activity_opportunity', 'opportunity_id'),
        Index('idx_activity_case', 'case_id'),
        Index('idx_activity_assigned_user', 'assigned_user_id'),
        Index('idx_activity_created_by', 'created_by_user_id'),
        Index('idx_activity_start_date', 'start_date'),
        Index('idx_activity_due_date', 'due_date'),
        Index('idx_activity_end_date', 'end_date'),
        Index('idx_activity_completed_date', 'completed_date'),
        Index('idx_activity_recurring', 'is_recurring'),
        Index('idx_activity_parent', 'parent_activity_id'),
        Index('idx_activity_follow_up', 'follow_up_required'),
        Index('idx_activity_billable', 'is_billable'),
        Index('idx_activity_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Activity(id={self.id}, number='{self.activity_number}', title='{self.title}', type='{self.activity_type.value}')>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if activity is overdue"""
        if self.status == ActivityStatus.COMPLETED or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date.replace(tzinfo=None)
    
    @property
    def is_due_today(self) -> bool:
        """Check if activity is due today"""
        if not self.due_date:
            return False
        today = datetime.utcnow().date()
        return self.due_date.date() == today
    
    @property
    def is_due_tomorrow(self) -> bool:
        """Check if activity is due tomorrow"""
        if not self.due_date:
            return False
        tomorrow = (datetime.utcnow() + timedelta(days=1)).date()
        return self.due_date.date() == tomorrow
    
    @property
    def days_until_due(self) -> Optional[int]:
        """Get days until due date"""
        if not self.due_date:
            return None
        delta = self.due_date.replace(tzinfo=None) - datetime.utcnow()
        return delta.days
    
    @property
    def is_meeting(self) -> bool:
        """Check if activity is a meeting or appointment"""
        return self.activity_type in [ActivityType.MEETING, ActivityType.APPOINTMENT, ActivityType.DEMO, ActivityType.PRESENTATION]
    
    @property
    def is_call(self) -> bool:
        """Check if activity is a phone call"""
        return self.activity_type == ActivityType.PHONE_CALL
    
    @property
    def is_task(self) -> bool:
        """Check if activity is a task"""
        return self.activity_type == ActivityType.TASK
    
    @property
    def is_communication(self) -> bool:
        """Check if activity is communication-related"""
        return self.activity_type in [ActivityType.PHONE_CALL, ActivityType.EMAIL, ActivityType.MEETING]
    
    @property
    def formatted_duration(self) -> str:
        """Get formatted duration string"""
        if not self.duration_minutes:
            return "Not set"
        
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
        return f"{minutes}m"
    
    @property
    def billable_amount(self) -> Optional[Decimal]:
        """Calculate billable amount"""
        if not self.is_billable or not self.billable_hours or not self.hourly_rate:
            return None
        return self.billable_hours * self.hourly_rate
    
    def complete_activity(self, outcome: str = None, next_action: str = None, 
                         satisfaction_rating: int = None) -> None:
        """Mark activity as completed"""
        self.status = ActivityStatus.COMPLETED
        self.completed_date = func.now()
        self.completion_percentage = 100
        
        if outcome:
            self.outcome_description = outcome
        if next_action:
            self.next_action = next_action
        if satisfaction_rating:
            self.satisfaction_rating = satisfaction_rating
    
    def cancel_activity(self, reason: str = None) -> None:
        """Cancel the activity"""
        self.status = ActivityStatus.CANCELLED
        if reason:
            self.outcome_description = f"Cancelled: {reason}"
    
    def postpone_activity(self, new_date: datetime, reason: str = None) -> None:
        """Postpone the activity to a new date"""
        self.status = ActivityStatus.POSTPONED
        self.start_date = new_date
        if self.due_date:
            # Maintain the same duration if due date exists
            duration = self.due_date - self.start_date
            self.due_date = new_date + duration
        
        if reason:
            self.outcome_description = f"Postponed: {reason}"
    
    def add_attendee(self, contact_id: str) -> None:
        """Add an attendee to a meeting"""
        if not self.is_meeting:
            return
        
        if not self.attendees:
            self.attendees = []
        if contact_id not in self.attendees:
            self.attendees.append(contact_id)
    
    def remove_attendee(self, contact_id: str) -> None:
        """Remove an attendee from a meeting"""
        if self.attendees and contact_id in self.attendees:
            self.attendees.remove(contact_id)
    
    def add_checklist_item(self, item: str, completed: bool = False) -> None:
        """Add an item to the task checklist"""
        if not self.is_task:
            return
        
        if not self.checklist:
            self.checklist = []
        
        checklist_item = {
            "id": str(uuid.uuid4()),
            "item": item,
            "completed": completed,
            "created_at": datetime.utcnow().isoformat()
        }
        self.checklist.append(checklist_item)
        
        # Update completion percentage
        self.update_completion_percentage()
    
    def complete_checklist_item(self, item_id: str) -> None:
        """Mark a checklist item as completed"""
        if not self.checklist:
            return
        
        for item in self.checklist:
            if item.get("id") == item_id:
                item["completed"] = True
                item["completed_at"] = datetime.utcnow().isoformat()
                break
        
        self.update_completion_percentage()
    
    def update_completion_percentage(self) -> None:
        """Update task completion percentage based on checklist"""
        if not self.checklist or not self.is_task:
            return
        
        total_items = len(self.checklist)
        completed_items = sum(1 for item in self.checklist if item.get("completed", False))
        
        self.completion_percentage = int((completed_items / total_items) * 100)
        
        # Auto-complete if all items are done
        if self.completion_percentage == 100 and self.status != ActivityStatus.COMPLETED:
            self.complete_activity("All checklist items completed")
    
    def set_reminder(self, minutes_before: int = 15) -> None:
        """Set reminder for the activity"""
        self.reminder_enabled = True
        self.reminder_minutes_before = minutes_before
        self.reminder_sent = False
    
    def mark_reminder_sent(self) -> None:
        """Mark reminder as sent"""
        self.reminder_sent = True
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to activity"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from activity"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if activity has specific tag"""
        return bool(self.tags and tag in self.tags)
    
    def calculate_quality_score(self) -> int:
        """Calculate quality score based on various factors"""
        score = 50  # Base score
        
        # Completion score
        if self.status == ActivityStatus.COMPLETED:
            score += 30
            
            # Bonus for timely completion
            if self.completed_date and self.due_date:
                if self.completed_date <= self.due_date:
                    score += 10
                else:
                    score -= 5  # Penalty for late completion
        
        # Outcome quality
        if self.outcome_description:
            score += 10
        
        # Follow-up planning
        if self.next_action and self.next_action_date:
            score += 5
        
        # Satisfaction rating
        if self.satisfaction_rating:
            score += self.satisfaction_rating * 2  # 2-10 points based on rating
        
        return max(0, min(score, 100))


class ActivityTemplate(Base):
    """
    Activity templates for common recurring activities
    """
    __tablename__ = "activity_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Template identification
    name = Column(String(255), nullable=False)
    description = Column(Text)
    activity_type = Column(Enum(ActivityType), nullable=False)
    
    # Default values
    default_duration_minutes = Column(Integer)
    default_priority = Column(Enum(ActivityPriority), default=ActivityPriority.MEDIUM)
    default_reminder_minutes = Column(Integer, default=15)
    
    # Template configuration
    template_fields = Column(JSON, default=dict)  # Field values to apply
    required_fields = Column(JSON, default=list)  # Required fields when using template
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime)
    
    # Template settings
    is_active = Column(Boolean, default=True)
    is_system_template = Column(Boolean, default=False)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    
    __table_args__ = (
        Index('idx_activity_template_company', 'company_id'),
        Index('idx_activity_template_type', 'activity_type'),
        Index('idx_activity_template_active', 'is_active'),
    ) 