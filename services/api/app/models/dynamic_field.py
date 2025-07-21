"""
Dynamic Field model for Greek ERP/CRM System
Represents fields for dynamic entities with validation and Greek compliance
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class FieldType(enum.Enum):
    """Field type classification"""
    # Basic types
    TEXT = "text"
    NUMBER = "number"
    EMAIL = "email"
    URL = "url"
    PASSWORD = "password"
    
    # Specialized inputs
    TEXTAREA = "textarea"
    RICH_TEXT = "rich_text"
    PHONE = "phone"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    
    # Selection types
    SELECT = "select"
    MULTISELECT = "multiselect"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    SWITCH = "switch"
    
    # File types
    FILE = "file"
    IMAGE = "image"
    
    # Greek-specific types
    AFM = "afm"                    # Greek Tax Number
    AMKA = "amka"                  # Greek Social Security Number
    GREEK_PHONE = "greek_phone"    # Greek phone validation
    GREEK_ADDRESS = "greek_address" # Greek address components
    DOY_SELECTOR = "doy_selector"  # Greek Tax Office selector
    REGION_SELECTOR = "region_selector" # Greek region selector
    
    # Advanced types
    JSON_FIELD = "json"
    FORMULA = "formula"
    LOOKUP = "lookup"
    RELATIONSHIP = "relationship"


class FieldWidgetType(enum.Enum):
    """Field widget type for rendering"""
    INPUT = "input"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DATE_PICKER = "date_picker"
    TIME_PICKER = "time_picker"
    FILE_UPLOAD = "file_upload"
    COLOR_PICKER = "color_picker"
    SLIDER = "slider"
    TOGGLE = "toggle"
    RATING = "rating"
    TAGS = "tags"
    EDITOR = "editor"
    CUSTOM = "custom"


class DynamicField(Base):
    """
    Dynamic Field model for Greek ERP/CRM system
    Represents fields that can be added to dynamic entities
    """
    __tablename__ = "dynamic_fields"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Entity association
    entity_id = Column(UUID(as_uuid=True), ForeignKey('dynamic_entities.id'), nullable=False, index=True)
    
    # Field definition
    name = Column(String(100), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Greek translations
    display_name_greek = Column(String(255))
    description_greek = Column(Text)
    placeholder_greek = Column(String(255))
    
    # Field type and configuration
    field_type = Column(Enum(FieldType), nullable=False)
    widget_type = Column(Enum(FieldWidgetType), nullable=False)
    data_type = Column(String(50), nullable=False, default="string")  # string, number, boolean, date, etc.
    
    # Field properties
    is_required = Column(Boolean, default=False, nullable=False)
    is_unique = Column(Boolean, default=False, nullable=False)
    is_indexed = Column(Boolean, default=False, nullable=False)
    is_searchable = Column(Boolean, default=True, nullable=False)
    is_sortable = Column(Boolean, default=True, nullable=False)
    is_filterable = Column(Boolean, default=True, nullable=False)
    is_exportable = Column(Boolean, default=True, nullable=False)
    
    # Display properties
    placeholder = Column(String(255))
    help_text = Column(Text)
    help_text_greek = Column(Text)
    default_value = Column(Text)
    
    # Validation rules
    min_length = Column(Integer)
    max_length = Column(Integer)
    min_value = Column(Numeric(15, 4))
    max_value = Column(Numeric(15, 4))
    regex_pattern = Column(String(500))
    validation_message = Column(String(255))
    validation_message_greek = Column(String(255))
    
    # Options for select/radio/checkbox fields
    options = Column(JSON, default=list)  # [{"value": "...", "label": "...", "label_greek": "..."}]
    
    # Layout and positioning
    display_order = Column(Integer, nullable=False, default=0)
    grid_column_span = Column(Integer, default=1)  # 1-12 for grid layout
    section = Column(String(100), default="general")  # Form section grouping
    
    # Visibility and permissions
    is_visible = Column(Boolean, default=True, nullable=False)
    is_editable = Column(Boolean, default=True, nullable=False)
    is_readonly = Column(Boolean, default=False, nullable=False)
    
    # List display
    show_in_list = Column(Boolean, default=True, nullable=False)
    show_in_detail = Column(Boolean, default=True, nullable=False)
    show_in_search = Column(Boolean, default=False, nullable=False)
    
    # Permissions
    permissions = Column(JSON, default=dict)  # Role-based field permissions
    
    # Greek compliance
    requires_greek_validation = Column(Boolean, default=False, nullable=False)
    aade_field_mapping = Column(String(100))  # AADE XML field mapping
    
    # Relationship configuration (for lookup/relationship fields)
    lookup_entity_id = Column(UUID(as_uuid=True), ForeignKey('dynamic_entities.id'), index=True)
    lookup_display_field = Column(String(100))  # Field to display from lookup entity
    lookup_filter = Column(JSON, default=dict)  # Filter criteria for lookup
    
    # Formula configuration (for calculated fields)
    formula_expression = Column(Text)  # Mathematical or logical expression
    formula_dependencies = Column(JSON, default=list)  # Fields this formula depends on
    
    # Conditional logic
    conditional_logic = Column(JSON, default=dict)  # Show/hide based on other fields
    
    # Custom configuration
    custom_properties = Column(JSON, default=dict)
    css_classes = Column(String(255))
    custom_validation = Column(Text)  # Custom JavaScript validation
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    entity = relationship("DynamicEntity", back_populates="fields", foreign_keys=[entity_id])
    lookup_entity = relationship("DynamicEntity", foreign_keys=[lookup_entity_id])
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_dynamic_field_entity', 'entity_id'),
        Index('idx_dynamic_field_name', 'name'),
        Index('idx_dynamic_field_type', 'field_type'),
        Index('idx_dynamic_field_widget', 'widget_type'),
        Index('idx_dynamic_field_required', 'is_required'),
        Index('idx_dynamic_field_unique', 'is_unique'),
        Index('idx_dynamic_field_indexed', 'is_indexed'),
        Index('idx_dynamic_field_searchable', 'is_searchable'),
        Index('idx_dynamic_field_visible', 'is_visible'),
        Index('idx_dynamic_field_order', 'display_order'),
        Index('idx_dynamic_field_section', 'section'),
        Index('idx_dynamic_field_lookup', 'lookup_entity_id'),
        Index('idx_dynamic_field_created', 'created_at'),
        Index('idx_dynamic_field_updated', 'updated_at'),
        # Composite indexes for common queries
        Index('idx_dynamic_field_entity_order', 'entity_id', 'display_order'),
        Index('idx_dynamic_field_entity_section', 'entity_id', 'section'),
        Index('idx_dynamic_field_entity_visible', 'entity_id', 'is_visible'),
    )

    def __repr__(self):
        return f"<DynamicField(id={self.id}, name={self.name}, type={self.field_type}, entity_id={self.entity_id})>" 