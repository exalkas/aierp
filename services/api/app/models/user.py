"""
User model for Greek ERP/CRM System
Supports role-based access control and multi-tenant architecture
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from passlib.context import CryptContext
from datetime import timedelta

from ..core.database import Base

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    """User roles with hierarchical permissions"""
    SUPER_ADMIN = "super_admin"      # System administrator
    COMPANY_ADMIN = "company_admin"  # Company administrator
    MANAGER = "manager"              # Department manager
    EMPLOYEE = "employee"            # Regular employee
    VIEWER = "viewer"                # Read-only access
    CLIENT = "client"                # External client access


class UserStatus(enum.Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"
    LOCKED = "locked"


class User(Base):
    """
    User model for multi-tenant Greek ERP/CRM system
    Each user belongs to a specific company
    """
    __tablename__ = "users"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association (foreign key to master companies table)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    
    # Authentication fields
    username = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    display_name = Column(String(200))
    phone = Column(String(20))
    mobile = Column(String(20))
    
    # Role and permissions
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    permissions = Column(JSON, default=list)  # Specific permissions list
    department = Column(String(100))
    position = Column(String(100))
    
    # Account status
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.PENDING_VERIFICATION)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Language and localization
    language = Column(String(2), default="el")  # Greek by default
    timezone = Column(String(50), default="Europe/Athens")
    
    # Security settings
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255))
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    
    # Session management
    last_login = Column(DateTime)
    last_activity = Column(DateTime)
    session_token = Column(String(255), unique=True, index=True)
    
    # Password management
    password_changed_at = Column(DateTime)
    password_reset_token = Column(String(255), unique=True, index=True)
    password_reset_expires = Column(DateTime)
    
    # Email verification
    email_verification_token = Column(String(255), unique=True, index=True)
    email_verification_expires = Column(DateTime)
    email_verified_at = Column(DateTime)
    
    # User preferences
    notification_preferences = Column(JSON, default=dict)
    ui_preferences = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    company = relationship("Company", back_populates="users")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_user_company', 'company_id'),
        Index('idx_user_username_company', 'username', 'company_id', unique=True),
        Index('idx_user_email_company', 'email', 'company_id', unique=True),
        Index('idx_user_role', 'role'),
        Index('idx_user_status', 'status'),
        Index('idx_user_active', 'is_active'),
        Index('idx_user_session', 'session_token'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role.value}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.COMPANY_ADMIN]
    
    @property
    def is_manager(self) -> bool:
        """Check if user has manager role or higher"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.COMPANY_ADMIN, UserRole.MANAGER]
    
    def set_password(self, password: str) -> None:
        """Hash and set user password"""
        self.password_hash = pwd_context.hash(password)
        self.password_changed_at = func.now()
    
    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        return pwd_context.verify(password, self.password_hash)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        # Super admin has all permissions
        if self.role == UserRole.SUPER_ADMIN:
            return True
        
        # Check role-based permissions
        role_permissions = self.get_role_permissions()
        if permission in role_permissions:
            return True
        
        # Check specific permissions
        if self.permissions and permission in self.permissions:
            return True
        
        return False
    
    def get_role_permissions(self) -> List[str]:
        """Get permissions based on user role"""
        role_permissions = {
            UserRole.SUPER_ADMIN: ["*"],  # All permissions
            UserRole.COMPANY_ADMIN: [
                "company:manage", "users:manage", "settings:manage",
                "businesses:manage", "products:manage", "invoices:manage",
                "reports:view", "analytics:view", "audit:view"
            ],
            UserRole.MANAGER: [
                "businesses:manage", "products:manage", "invoices:manage",
                "reports:view", "analytics:view", "users:view"
            ],
            UserRole.EMPLOYEE: [
                "businesses:read", "businesses:write", "products:read", "products:write",
                "invoices:read", "invoices:write", "reports:view"
            ],
            UserRole.VIEWER: [
                "businesses:read", "products:read", "invoices:read", "reports:view"
            ],
            UserRole.CLIENT: [
                "invoices:read", "profile:read", "profile:write"
            ]
        }
        return role_permissions.get(self.role, [])
    
    def add_permission(self, permission: str) -> None:
        """Add specific permission to user"""
        if not self.permissions:
            self.permissions = []
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: str) -> None:
        """Remove specific permission from user"""
        if self.permissions and permission in self.permissions:
            self.permissions.remove(permission)
    
    def get_notification_preference(self, key: str, default: Any = None) -> Any:
        """Get notification preference"""
        return self.notification_preferences.get(key, default) if self.notification_preferences else default
    
    def set_notification_preference(self, key: str, value: Any) -> None:
        """Set notification preference"""
        if not self.notification_preferences:
            self.notification_preferences = {}
        self.notification_preferences[key] = value
    
    def get_ui_preference(self, key: str, default: Any = None) -> Any:
        """Get UI preference"""
        return self.ui_preferences.get(key, default) if self.ui_preferences else default
    
    def set_ui_preference(self, key: str, value: Any) -> None:
        """Set UI preference"""
        if not self.ui_preferences:
            self.ui_preferences = {}
        self.ui_preferences[key] = value
    
    def is_account_locked(self) -> bool:
        """Check if account is locked"""
        if self.status == UserStatus.LOCKED:
            return True
        if self.locked_until and self.locked_until > func.now():
            return True
        return False
    
    def lock_account(self, duration_minutes: int = 30) -> None:
        """Lock account for specified duration"""
        self.status = UserStatus.LOCKED
        self.locked_until = func.now() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts = 0
    
    def unlock_account(self) -> None:
        """Unlock account"""
        self.status = UserStatus.ACTIVE
        self.locked_until = None
        self.failed_login_attempts = 0
    
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
            "mobile": self.mobile,
            "role": self.role.value,
            "department": self.department,
            "position": self.position,
            "status": self.status.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "language": self.language,
            "timezone": self.timezone,
            "two_factor_enabled": self.two_factor_enabled,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                "permissions": self.permissions,
                "notification_preferences": self.notification_preferences,
                "ui_preferences": self.ui_preferences,
                "failed_login_attempts": self.failed_login_attempts,
                "password_changed_at": self.password_changed_at.isoformat() if self.password_changed_at else None
            })
        
        return data 