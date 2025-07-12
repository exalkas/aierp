"""
Audit Log Model for Greek ERP/CRM System
Tracks all changes to VAT rules, locations, and other critical system data
"""

import enum
from datetime import datetime
from typing import Dict, Optional, Any, List
from sqlalchemy import Column, String, DateTime, Text, JSON, Index, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..core.database import Base


class AuditAction(enum.Enum):
    """Types of audit actions"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"
    IMPORT = "import"
    EXPORT = "export"
    BULK_UPDATE = "bulk_update"
    APPROVE = "approve"
    REJECT = "reject"


class AuditEntityType(enum.Enum):
    """Types of entities being audited"""
    VAT_RULE = "vat_rule"
    GREEK_LOCATION = "greek_location"
    COMPANY = "company"
    USER = "user"
    BUSINESS_ENTITY = "business_entity"
    PRODUCT = "product"
    INVOICE = "invoice"
    SYSTEM_CONFIG = "system_config"


class AuditLog(Base):
    """
    Audit log model for tracking all system changes
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # What was changed
    entity_type = Column(Enum(AuditEntityType), nullable=False, index=True)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    action = Column(Enum(AuditAction), nullable=False, index=True)
    
    # Who made the change
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255))
    
    # When the change was made
    timestamp = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    
    # Change details
    description = Column(Text)
    change_reason = Column(Text)
    
    # Data changes
    old_values = Column(JSON)  # Previous values
    new_values = Column(JSON)  # New values
    changed_fields = Column(JSON)  # List of fields that changed
    
    # Context information
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))
    session_id = Column(String(255))
    request_id = Column(String(255))
    
    # Company context (for multi-tenant)
    company_id = Column(UUID(as_uuid=True), index=True)
    
    # Additional metadata
    additional_metadata = Column(JSON, default=dict)
    
    # Audit trail integrity
    checksum = Column(String(255))  # For audit trail integrity
    
    __table_args__ = (
        Index('idx_audit_entity', 'entity_type', 'entity_id'),
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_company', 'company_id'),
        Index('idx_audit_search', 'entity_type', 'timestamp', 'user_id'),
    )
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, entity_type={self.entity_type}, action={self.action}, user={self.user_name})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary"""
        return {
            "id": str(self.id),
            "entity_type": self.entity_type.value,
            "entity_id": str(self.entity_id),
            "action": self.action.value,
            "user_id": str(self.user_id),
            "user_name": self.user_name,
            "user_email": self.user_email,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "change_reason": self.change_reason,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "changed_fields": self.changed_fields,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "company_id": str(self.company_id) if self.company_id else None,
            "additional_metadata": self.additional_metadata,
            "checksum": self.checksum
        }


class AuditService:
    """
    Service for creating and managing audit logs
    """
    
    def __init__(self, db_session):
        self.db = db_session
    
    def create_audit_log(
        self,
        entity_type: AuditEntityType,
        entity_id: UUID,
        action: AuditAction,
        user_id: UUID,
        user_name: str,
        description: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        change_reason: Optional[str] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        company_id: Optional[UUID] = None,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Create a new audit log entry
        """
        # Calculate changed fields
        changed_fields = []
        if old_values and new_values:
            for key, new_value in new_values.items():
                old_value = old_values.get(key)
                if old_value != new_value:
                    changed_fields.append({
                        "field": key,
                        "old_value": old_value,
                        "new_value": new_value
                    })
        
        audit_log = AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            description=description,
            change_reason=change_reason,
            old_values=old_values,
            new_values=new_values,
            changed_fields=changed_fields,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            request_id=request_id,
            company_id=company_id,
            additional_metadata=additional_metadata or {}
        )
        
        # Generate checksum for integrity
        audit_log.checksum = self._generate_checksum(audit_log)
        
        self.db.add(audit_log)
        self.db.commit()
        
        return audit_log
    
    def get_audit_trail(
        self,
        entity_type: Optional[AuditEntityType] = None,
        entity_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        action: Optional[AuditAction] = None,
        company_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get audit trail with filtering
        """
        query = self.db.query(AuditLog)
        
        # Apply filters
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if company_id:
            query = query.filter(AuditLog.company_id == company_id)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination and ordering
        audit_logs = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
        
        return {
            "audit_logs": [log.to_dict() for log in audit_logs],
            "pagination": {
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
                "has_next": offset + limit < total_count
            }
        }
    
    def get_entity_history(
        self,
        entity_type: AuditEntityType,
        entity_id: UUID,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get complete history for a specific entity
        """
        audit_logs = self.db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
        
        return [log.to_dict() for log in audit_logs]
    
    def _generate_checksum(self, audit_log: AuditLog) -> str:
        """
        Generate checksum for audit log integrity
        """
        import hashlib
        
        # Create a string representation of key fields
        checksum_data = f"{audit_log.entity_type.value}{audit_log.entity_id}{audit_log.action.value}{audit_log.user_id}{audit_log.timestamp}"
        
        # Generate MD5 hash
        return hashlib.md5(checksum_data.encode()).hexdigest()
    
    def verify_audit_integrity(self, audit_log_id: UUID) -> bool:
        """
        Verify audit log integrity using checksum
        """
        audit_log = self.db.query(AuditLog).filter(AuditLog.id == audit_log_id).first()
        if not audit_log:
            return False
        
        expected_checksum = self._generate_checksum(audit_log)
        return audit_log.checksum == expected_checksum 