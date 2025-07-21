"""
Entity Layout model for Greek ERP/CRM System
Represents layout configurations for dynamic entities
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class LayoutType(enum.Enum):
    """Layout type classification"""
    FORM = "form"              # Form layout for create/edit
    LIST = "list"              # List/table layout
    DETAIL = "detail"          # Detail view layout
    SEARCH = "search"          # Search interface layout
    DASHBOARD = "dashboard"    # Dashboard widget layout
    REPORT = "report"          # Report layout
    MOBILE = "mobile"          # Mobile-optimized layout
    PRINT = "print"           # Print-friendly layout


class LayoutStatus(enum.Enum):
    """Layout status"""
    ACTIVE = "active"
    DRAFT = "draft"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class ResponsiveBreakpoint(enum.Enum):
    """Responsive breakpoint"""
    XS = "xs"     # Extra small (mobile)
    SM = "sm"     # Small (mobile landscape)
    MD = "md"     # Medium (tablet)
    LG = "lg"     # Large (desktop)
    XL = "xl"     # Extra large (wide desktop)


class EntityLayout(Base):
    """
    Entity Layout model for Greek ERP/CRM system
    Defines how dynamic entities are displayed and interacted with
    """
    __tablename__ = "entity_layouts"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Entity association
    entity_id = Column(UUID(as_uuid=True), ForeignKey('dynamic_entities.id'), nullable=False, index=True)
    
    # Layout definition
    name = Column(String(100), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Greek translations
    display_name_greek = Column(String(255))
    description_greek = Column(Text)
    
    # Layout configuration
    layout_type = Column(Enum(LayoutType), nullable=False)
    status = Column(Enum(LayoutStatus), nullable=False, default=LayoutStatus.DRAFT)
    version = Column(String(20), nullable=False, default="1.0.0")
    
    # Layout properties
    is_default = Column(Boolean, default=False, nullable=False)
    is_system_layout = Column(Boolean, default=False, nullable=False)
    is_responsive = Column(Boolean, default=True, nullable=False)
    
    # Grid configuration
    grid_columns = Column(Integer, default=12, nullable=False)  # Grid system (12-column by default)
    grid_gap = Column(String(20), default="4")  # Tailwind spacing
    max_width = Column(String(20), default="7xl")  # Container max width
    
    # Form-specific configuration
    form_sections = Column(JSON, default=list)  # Form sections and their fields
    form_validation = Column(JSON, default=dict)  # Form-level validation rules
    submit_behavior = Column(JSON, default=dict)  # Submit button configuration
    
    # List-specific configuration
    list_columns = Column(JSON, default=list)  # Columns to display in list
    list_filters = Column(JSON, default=list)  # Available filters
    list_sorting = Column(JSON, default=dict)  # Default sorting
    list_pagination = Column(JSON, default=dict)  # Pagination configuration
    list_actions = Column(JSON, default=list)  # Bulk actions
    
    # Detail-specific configuration
    detail_sections = Column(JSON, default=list)  # Detail view sections
    detail_tabs = Column(JSON, default=list)  # Tab configuration
    related_entities = Column(JSON, default=list)  # Related entity displays
    
    # Search-specific configuration
    search_fields = Column(JSON, default=list)  # Searchable fields
    search_filters = Column(JSON, default=list)  # Search filters
    search_sorting = Column(JSON, default=list)  # Search result sorting
    
    # Dashboard-specific configuration
    dashboard_widgets = Column(JSON, default=list)  # Widget configuration
    dashboard_filters = Column(JSON, default=dict)  # Dashboard filters
    dashboard_refresh = Column(Integer, default=0)  # Auto-refresh interval (seconds)
    
    # Responsive configuration
    responsive_config = Column(JSON, default=dict)  # Breakpoint-specific configurations
    mobile_optimizations = Column(JSON, default=dict)  # Mobile-specific settings
    
    # Styling and theming
    theme = Column(String(50), default="default")
    color_scheme = Column(String(50), default="blue")
    custom_css = Column(Text)
    css_classes = Column(String(500))
    
    # Greek-specific layout features
    greek_layout_features = Column(JSON, default=dict)  # Greek-specific UI elements
    rtl_support = Column(Boolean, default=False, nullable=False)  # Right-to-left support
    greek_formatting = Column(JSON, default=dict)  # Greek date/number formatting
    
    # Conditional display
    visibility_rules = Column(JSON, default=dict)  # Show/hide based on conditions
    permission_rules = Column(JSON, default=dict)  # Role-based layout permissions
    
    # User experience
    loading_states = Column(JSON, default=dict)  # Loading indicators
    error_handling = Column(JSON, default=dict)  # Error display configuration
    tooltips_enabled = Column(Boolean, default=True, nullable=False)
    animations_enabled = Column(Boolean, default=True, nullable=False)
    
    # Performance optimization
    lazy_loading = Column(Boolean, default=True, nullable=False)
    virtual_scrolling = Column(Boolean, default=False, nullable=False)
    cache_strategy = Column(String(50), default="default")
    
    # Layout templates and inheritance
    parent_layout_id = Column(UUID(as_uuid=True), ForeignKey('entity_layouts.id'), index=True)
    template_id = Column(String(100))  # Predefined template reference
    custom_properties = Column(JSON, default=dict)
    
    # Header and footer configuration
    header_config = Column(JSON, default=dict)  # Page header settings
    footer_config = Column(JSON, default=dict)  # Page footer settings
    breadcrumb_config = Column(JSON, default=dict)  # Breadcrumb navigation
    
    # Action configuration
    primary_actions = Column(JSON, default=list)  # Primary action buttons
    secondary_actions = Column(JSON, default=list)  # Secondary actions
    context_menu = Column(JSON, default=list)  # Context menu items
    
    # Export and print configuration
    export_formats = Column(JSON, default=list)  # Available export formats
    print_layout = Column(JSON, default=dict)  # Print-specific layout
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    entity = relationship("DynamicEntity", back_populates="layouts", foreign_keys=[entity_id])
    parent_layout = relationship("EntityLayout", remote_side=[id], foreign_keys=[parent_layout_id])
    child_layouts = relationship("EntityLayout", foreign_keys=[parent_layout_id], overlaps="parent_layout")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_entity_layout_entity', 'entity_id'),
        Index('idx_entity_layout_name', 'name'),
        Index('idx_entity_layout_type', 'layout_type'),
        Index('idx_entity_layout_status', 'status'),
        Index('idx_entity_layout_default', 'is_default'),
        Index('idx_entity_layout_system', 'is_system_layout'),
        Index('idx_entity_layout_parent', 'parent_layout_id'),
        Index('idx_entity_layout_template', 'template_id'),
        Index('idx_entity_layout_created', 'created_at'),
        Index('idx_entity_layout_updated', 'updated_at'),
        # Composite indexes for common queries
        Index('idx_entity_layout_entity_type', 'entity_id', 'layout_type'),
        Index('idx_entity_layout_entity_default', 'entity_id', 'is_default'),
        Index('idx_entity_layout_entity_status', 'entity_id', 'status'),
    )

    def __repr__(self):
        return f"<EntityLayout(id={self.id}, name={self.name}, type={self.layout_type}, entity_id={self.entity_id})>" 