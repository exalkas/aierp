"""
Voice Command models for Greek ERP/CRM System
Supports customizable voice commands with Greek language support
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class VoiceCommandType(enum.Enum):
    """Voice command type classification"""
    NAVIGATION = "navigation"        # Navigate to page/section
    CREATE = "create"               # Create new record
    SEARCH = "search"               # Search for records
    ACTION = "action"               # Perform specific action
    MODAL = "modal"                 # Open modal/dialog
    WORKFLOW = "workflow"           # Execute workflow
    REPORT = "report"               # Generate report
    HELP = "help"                   # Get help/assistance


class VoiceCommandStatus(enum.Enum):
    """Voice command status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


class VoiceActionType(enum.Enum):
    """Type of action to perform"""
    NAVIGATE = "navigate"           # Navigate to URL/route
    OPEN_MODAL = "open_modal"       # Open modal dialog
    EXECUTE_FUNCTION = "execute_function"  # Execute JavaScript function
    API_CALL = "api_call"           # Make API call
    FORM_FILL = "form_fill"         # Fill form fields
    WORKFLOW = "workflow"           # Execute workflow


class SystemVoiceCommand(Base):
    """
    System-defined voice commands (defaults)
    These are the base commands that come with the system
    """
    __tablename__ = "system_voice_commands"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Command identification
    command_key = Column(String(100), nullable=False, unique=True, index=True)
    command_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Command classification
    command_type = Column(Enum(VoiceCommandType), nullable=False)
    category = Column(String(100), nullable=False)  # "crm", "erp", "general", etc.
    module = Column(String(100))  # Specific module
    
    # Default phrases (multiple languages)
    default_phrases = Column(JSON, nullable=False, default=dict)  # {"el": ["Νέο τιμολόγιο"], "en": ["New invoice"]}
    
    # Action configuration
    action_type = Column(Enum(VoiceActionType), nullable=False)
    action_config = Column(JSON, nullable=False, default=dict)  # Action-specific configuration
    
    # Examples:
    # Navigation: {"type": "navigate", "url": "/invoices/new", "target": "_self"}
    # Modal: {"type": "open_modal", "modal_id": "new-invoice-modal", "props": {}}
    # Function: {"type": "execute_function", "function": "openInvoiceModal", "params": {}}
    
    # Required parameters
    required_params = Column(JSON, default=list)  # ["customer_id", "product_id"]
    optional_params = Column(JSON, default=list)  # ["due_date", "notes"]
    
    # Permissions and access
    required_permissions = Column(JSON, default=list)  # ["invoice.create", "customer.read"]
    min_user_role = Column(String(50), default="employee")
    
    # Command settings
    status = Column(Enum(VoiceCommandStatus), nullable=False, default=VoiceCommandStatus.ACTIVE)
    is_customizable = Column(Boolean, default=True)
    priority = Column(Integer, default=100)  # Higher priority = more likely to match
    
    # Greek language support
    greek_variants = Column(JSON, default=list)  # Alternative Greek pronunciations
    phonetic_spelling = Column(JSON, default=dict)  # Phonetic spellings for better recognition
    
    # Help and documentation
    help_text = Column(Text)
    examples = Column(JSON, default=list)  # Example usage
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    version = Column(String(20), default="1.0.0")
    
    # Relationships
    user_customizations = relationship("UserVoiceCommand", back_populates="system_command")
    
    # Indexes
    __table_args__ = (
        Index('idx_system_voice_command_key', 'command_key'),
        Index('idx_system_voice_command_type', 'command_type'),
        Index('idx_system_voice_command_category', 'category'),
        Index('idx_system_voice_command_module', 'module'),
        Index('idx_system_voice_command_status', 'status'),
        Index('idx_system_voice_command_priority', 'priority'),
    )
    
    def __repr__(self):
        return f"<SystemVoiceCommand(key='{self.command_key}', name='{self.command_name}')>"


class UserVoiceCommand(Base):
    """
    User-customized voice commands
    Allows users to override system commands with their own phrases
    """
    __tablename__ = "user_voice_commands"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User and company association
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # System command reference
    system_command_id = Column(UUID(as_uuid=True), ForeignKey('system_voice_commands.id'), nullable=False, index=True)
    
    # User's custom phrases
    custom_phrases = Column(JSON, nullable=False, default=list)  # ["βγάλε νέο τιμολόγιο", "κάνε τιμολόγιο"]
    
    # Override settings
    is_enabled = Column(Boolean, default=True)
    use_system_phrases = Column(Boolean, default=True)  # Also use system phrases
    
    # Custom action (if user wants different behavior)
    custom_action_type = Column(Enum(VoiceActionType))
    custom_action_config = Column(JSON, default=dict)
    
    # Usage statistics
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime)
    accuracy_score = Column(Integer, default=0)  # How often recognition was correct
    
    # User preferences
    confidence_threshold = Column(Integer, default=70)  # Minimum confidence to trigger
    confirmation_required = Column(Boolean, default=False)  # Require confirmation
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    system_command = relationship("SystemVoiceCommand", back_populates="user_customizations")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_voice_command_user', 'user_id'),
        Index('idx_user_voice_command_company', 'company_id'),
        Index('idx_user_voice_command_system', 'system_command_id'),
        Index('idx_user_voice_command_enabled', 'is_enabled'),
        Index('idx_user_voice_command_usage', 'usage_count'),
        # Unique constraint: one customization per user per system command
        Index('idx_user_voice_command_unique', 'user_id', 'system_command_id', unique=True),
    )
    
    def __repr__(self):
        return f"<UserVoiceCommand(user_id='{self.user_id}', system_command_id='{self.system_command_id}')>"


class VoiceCommandLog(Base):
    """
    Voice command execution log for analytics and debugging
    """
    __tablename__ = "voice_command_logs"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User and company association
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Session information
    session_id = Column(String(100), index=True)
    device_info = Column(JSON, default=dict)
    
    # Voice recognition details
    original_text = Column(Text, nullable=False)  # What was actually said
    recognized_text = Column(Text, nullable=False)  # What was recognized
    confidence_score = Column(Integer, nullable=False)  # 0-100
    language_detected = Column(String(10), default="el")
    
    # Command matching
    matched_command_id = Column(UUID(as_uuid=True), ForeignKey('system_voice_commands.id'), index=True)
    user_command_id = Column(UUID(as_uuid=True), ForeignKey('user_voice_commands.id'), index=True)
    match_score = Column(Integer, default=0)  # How well the command matched
    
    # Execution details
    executed_successfully = Column(Boolean, default=False)
    execution_time_ms = Column(Integer)
    action_performed = Column(String(255))
    
    # Error information
    error_message = Column(Text)
    error_code = Column(String(50))
    
    # Context information
    page_url = Column(String(500))
    page_context = Column(JSON, default=dict)  # Additional context data
    
    # Feedback
    user_feedback = Column(String(20))  # "correct", "incorrect", "partially_correct"
    user_correction = Column(Text)  # What the user actually wanted
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    matched_command = relationship("SystemVoiceCommand", foreign_keys=[matched_command_id])
    user_command = relationship("UserVoiceCommand", foreign_keys=[user_command_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_voice_log_user', 'user_id'),
        Index('idx_voice_log_company', 'company_id'),
        Index('idx_voice_log_session', 'session_id'),
        Index('idx_voice_log_command', 'matched_command_id'),
        Index('idx_voice_log_success', 'executed_successfully'),
        Index('idx_voice_log_confidence', 'confidence_score'),
        Index('idx_voice_log_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<VoiceCommandLog(id='{self.id}', text='{self.recognized_text[:50]}...')>"


class VoiceCommandTemplate(Base):
    """
    Templates for creating voice commands
    Helps users create consistent command patterns
    """
    __tablename__ = "voice_command_templates"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template identification
    template_name = Column(String(255), nullable=False)
    template_key = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    
    # Template configuration
    category = Column(String(100), nullable=False)
    command_type = Column(Enum(VoiceCommandType), nullable=False)
    
    # Template structure
    phrase_patterns = Column(JSON, nullable=False, default=list)  # Pattern templates
    # Example: ["Νέο {entity}", "Δημιούργησε {entity}", "Κάνε {entity}"]
    
    action_template = Column(JSON, nullable=False, default=dict)  # Action configuration template
    
    # Variables and parameters
    variables = Column(JSON, default=list)  # ["entity", "action"]
    variable_examples = Column(JSON, default=dict)  # {"entity": ["τιμολόγιο", "πελάτη"]}
    
    # Usage information
    usage_count = Column(Integer, default=0)
    is_popular = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_voice_template_key', 'template_key'),
        Index('idx_voice_template_category', 'category'),
        Index('idx_voice_template_type', 'command_type'),
        Index('idx_voice_template_popular', 'is_popular'),
    )
    
    def __repr__(self):
        return f"<VoiceCommandTemplate(key='{self.template_key}', name='{self.template_name}')>"


# Default system voice commands for Greek ERP/CRM
DEFAULT_VOICE_COMMANDS = [
    {
        "command_key": "create_invoice",
        "command_name": "Create New Invoice",
        "description": "Create a new invoice",
        "command_type": VoiceCommandType.CREATE,
        "category": "erp",
        "module": "invoicing",
        "default_phrases": {
            "el": ["Νέο τιμολόγιο", "Δημιούργησε τιμολόγιο", "Κάνε τιμολόγιο"],
            "en": ["New invoice", "Create invoice", "Make invoice"]
        },
        "action_type": VoiceActionType.NAVIGATE,
        "action_config": {
            "url": "/invoices/new",
            "target": "_self"
        },
        "required_permissions": ["invoice.create"],
        "help_text": "Δημιουργεί νέο τιμολόγιο",
        "examples": ["Νέο τιμολόγιο", "Κάνε τιμολόγιο για πελάτη"]
    },
    {
        "command_key": "search_customers",
        "command_name": "Search Customers",
        "description": "Search for customers",
        "command_type": VoiceCommandType.SEARCH,
        "category": "crm",
        "module": "customers",
        "default_phrases": {
            "el": ["Βρες πελάτη", "Αναζήτηση πελάτη", "Ψάξε πελάτη"],
            "en": ["Find customer", "Search customer", "Look for customer"]
        },
        "action_type": VoiceActionType.NAVIGATE,
        "action_config": {
            "url": "/customers",
            "target": "_self",
            "focus_search": True
        },
        "required_permissions": ["customer.read"],
        "help_text": "Αναζητά πελάτες",
        "examples": ["Βρες πελάτη Παπαδόπουλος", "Αναζήτηση πελάτη"]
    },
    {
        "command_key": "open_dashboard",
        "command_name": "Open Dashboard",
        "description": "Navigate to main dashboard",
        "command_type": VoiceCommandType.NAVIGATION,
        "category": "general",
        "module": "dashboard",
        "default_phrases": {
            "el": ["Αρχική", "Ταμπλό", "Κεντρική σελίδα"],
            "en": ["Dashboard", "Home", "Main page"]
        },
        "action_type": VoiceActionType.NAVIGATE,
        "action_config": {
            "url": "/dashboard",
            "target": "_self"
        },
        "required_permissions": [],
        "help_text": "Πηγαίνει στην κεντρική σελίδα",
        "examples": ["Αρχική", "Πήγαινε στο ταμπλό"]
    },
    {
        "command_key": "create_customer",
        "command_name": "Create New Customer",
        "description": "Create a new customer",
        "command_type": VoiceCommandType.CREATE,
        "category": "crm",
        "module": "customers",
        "default_phrases": {
            "el": ["Νέος πελάτης", "Δημιούργησε πελάτη", "Κάνε πελάτη"],
            "en": ["New customer", "Create customer", "Add customer"]
        },
        "action_type": VoiceActionType.OPEN_MODAL,
        "action_config": {
            "modal_id": "new-customer-modal",
            "modal_props": {}
        },
        "required_permissions": ["customer.create"],
        "help_text": "Δημιουργεί νέον πελάτη",
        "examples": ["Νέος πελάτης", "Κάνε πελάτη"]
    },
    {
        "command_key": "show_help",
        "command_name": "Show Help",
        "description": "Show help information",
        "command_type": VoiceCommandType.HELP,
        "category": "general",
        "module": "help",
        "default_phrases": {
            "el": ["Βοήθεια", "Βοήθα με", "Τι μπορώ να κάνω"],
            "en": ["Help", "Help me", "What can I do"]
        },
        "action_type": VoiceActionType.OPEN_MODAL,
        "action_config": {
            "modal_id": "help-modal",
            "modal_props": {"section": "voice_commands"}
        },
        "required_permissions": [],
        "help_text": "Εμφανίζει πληροφορίες βοήθειας",
        "examples": ["Βοήθεια", "Τι μπορώ να πω"]
    }
] 