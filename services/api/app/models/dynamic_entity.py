"""
Dynamic Entity model for Greek ERP/CRM System
Represents user-defined entities with flexible schema and Greek compliance
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List

from ..core.database import Base


class EntityScope(enum.Enum):
    """Entity scope classification"""
    GLOBAL = "global"      # Available to all companies
    COMPANY = "company"    # Company-specific
    USER = "user"         # User-specific


class EntityStatus(enum.Enum):
    """Entity status"""
    ACTIVE = "active"
    DRAFT = "draft"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class DynamicEntity(Base):
    """
    Dynamic Entity model for Greek ERP/CRM system
    Allows users to create custom entities with flexible schemas
    """
    __tablename__ = "dynamic_entities"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Entity definition
    name = Column(String(100), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Greek translations
    display_name_greek = Column(String(255))
    description_greek = Column(Text)
    
    # Entity configuration
    scope = Column(Enum(EntityScope), nullable=False, default=EntityScope.COMPANY)
    status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.DRAFT)
    
    # Schema management
    version = Column(String(20), nullable=False, default="1.0.0")
    schema_version = Column(Integer, nullable=False, default=1)
    is_system_entity = Column(Boolean, default=False, nullable=False)
    
    # Entity properties
    icon = Column(String(50))  # Lucide icon name
    color = Column(String(7))  # Hex color
    singular_label = Column(String(100), nullable=False)
    plural_label = Column(String(100), nullable=False)
    
    # Greek labels
    singular_label_greek = Column(String(100))
    plural_label_greek = Column(String(100))
    
    # Entity behavior
    is_auditable = Column(Boolean, default=True, nullable=False)
    supports_workflow = Column(Boolean, default=False, nullable=False)
    supports_attachments = Column(Boolean, default=True, nullable=False)
    supports_comments = Column(Boolean, default=True, nullable=False)
    supports_tags = Column(Boolean, default=True, nullable=False)
    
    # API configuration
    api_name = Column(String(100), nullable=False, unique=True, index=True)
    endpoint_prefix = Column(String(50), nullable=False)
    
    # Database configuration
    table_name = Column(String(100), nullable=False)
    primary_key_field = Column(String(50), default="id")
    
    # Display configuration
    default_sort_field = Column(String(100))
    default_sort_direction = Column(String(4), default="asc")  # asc/desc
    records_per_page = Column(Integer, default=25)
    
    # Permissions
    permissions = Column(JSON, default=dict)  # Role-based permissions
    
    # Greek compliance
    requires_greek_validation = Column(Boolean, default=False, nullable=False)
    aade_integration = Column(Boolean, default=False, nullable=False)
    vat_applicable = Column(Boolean, default=False, nullable=False)
    
    # Relationships and references
    parent_entity_id = Column(UUID(as_uuid=True), ForeignKey('dynamic_entities.id'), index=True)
    related_entities = Column(JSON, default=list)  # List of related entity IDs
    
    # Notification settings
    email_notifications = Column(Boolean, default=False, nullable=False)
    webhook_url = Column(String(500))
    notification_settings = Column(JSON, default=dict)
    
    # Custom configuration
    custom_properties = Column(JSON, default=dict)
    business_rules = Column(JSON, default=list)
    validation_rules = Column(JSON, default=list)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    parent_entity = relationship("DynamicEntity", remote_side=[id], foreign_keys=[parent_entity_id])
    child_entities = relationship("DynamicEntity", foreign_keys=[parent_entity_id], overlaps="parent_entity")
    fields = relationship("DynamicField", back_populates="entity", foreign_keys="DynamicField.entity_id", cascade="all, delete-orphan")
    layouts = relationship("EntityLayout", back_populates="entity", cascade="all, delete-orphan")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_dynamic_entity_company', 'company_id'),
        Index('idx_dynamic_entity_name', 'name'),
        Index('idx_dynamic_entity_status', 'status'),
        Index('idx_dynamic_entity_scope', 'scope'),
        Index('idx_dynamic_entity_api_name', 'api_name'),
        Index('idx_dynamic_entity_table_name', 'table_name'),
        Index('idx_dynamic_entity_parent', 'parent_entity_id'),
        Index('idx_dynamic_entity_system', 'is_system_entity'),
        Index('idx_dynamic_entity_created', 'created_at'),
        Index('idx_dynamic_entity_updated', 'updated_at'),
    )

    def __repr__(self):
        return f"<DynamicEntity(id={self.id}, name={self.name}, display_name={self.display_name})>" 