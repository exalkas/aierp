"""
Database Models for Authentication Service
References the same models as API service for consistency
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from passlib.context import CryptContext
from datetime import datetime

from database import Base

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserStatus(enum.Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING_VERIFICATION = "pending_verification"
    SUSPENDED = "suspended"


class Company(Base):
    """
    Company model for multi-tenant support
    """
    __tablename__ = "companies"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic company information
    name = Column(String(255), nullable=False)
    afm = Column(String(9), unique=True, nullable=False)  # Greek Tax Number
    doy = Column(String(10), nullable=False)  # Tax Office Code
    
    # Contact information
    address = Column(Text)
    city = Column(String(100))
    postal_code = Column(String(10))
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    
    # Business details
    vat_number = Column(String(20))
    legal_form = Column(String(50))
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', afm='{self.afm}')>"


class User(Base):
    """
    User model for authentication
    """
    __tablename__ = "users"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    
    # Authentication fields
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal information
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    
    # Role and permissions
    role = Column(String(50), nullable=False, default='user')
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Session management
    last_login = Column(DateTime)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def display_name(self) -> str:
        """Get display name (fallback to username if no full name)"""
        return self.full_name
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self.role in ['admin', 'super_admin']
    
    def set_password(self, password: str) -> None:
        """Hash and set user password"""
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        return pwd_context.verify(password, self.password_hash)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        # Admin users have all permissions
        if self.is_admin:
            return True
        
        # For now, basic role-based permissions
        role_permissions = self.get_role_permissions()
        return permission in role_permissions
    
    def get_role_permissions(self) -> List[str]:
        """Get permissions based on role"""
        role_perms = {
            'admin': ['*'],  # All permissions
            'manager': ['customers:*', 'products:*', 'invoices:*', 'reports:view'],
            'user': ['customers:view', 'products:view', 'invoices:view'],
            'accountant': ['invoices:*', 'customers:view', 'products:view', 'reports:view'],
            'sales': ['customers:*', 'invoices:create', 'invoices:update', 'products:view']
        }
        return role_perms.get(self.role, ['customers:view'])
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user to dictionary for API responses"""
        data = {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "phone": self.phone,
            "role": self.role,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "permissions": self.get_role_permissions(),
            "can_be_deleted": not self.is_superuser,
            "can_change_password": True
        }
        
        return data 