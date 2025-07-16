"""
User Management Service with Super User Protection
Handles user CRUD operations with proper authorization and super user protection
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import datetime

from ..models.user import User, UserRole, UserStatus
from ..models.company import Company
from ..core.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)


class UserManagementService:
    """Service for managing users with super user protection"""
    
    async def create_user(
        self,
        db: AsyncSession,
        requesting_user: User,
        user_data: Dict[str, Any]
    ) -> User:
        """Create a new user with proper authorization"""
        
        # Check if requesting user can create users
        if not requesting_user.has_permission("users:create"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create users"
            )
        
        # Prevent creating super users unless requester is super user
        if user_data.get("is_super_user", False) and not requesting_user.is_protected_super_user():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only super users can create other super users"
            )
        
        # Hash password
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))
        
        # Set company context for multi-tenant isolation
        user_data["company_id"] = requesting_user.company_id
        user_data["created_by"] = requesting_user.id
        
        # Create user
        new_user = User(**user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"User {new_user.username} created by {requesting_user.username}")
        return new_user
    
    async def update_user(
        self,
        db: AsyncSession,
        requesting_user: User,
        user_id: UUID,
        update_data: Dict[str, Any]
    ) -> User:
        """Update user with proper authorization"""
        
        # Get target user
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        target_user = result.scalar_one_or_none()
        
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if requesting user can update this user
        if not self._can_update_user(requesting_user, target_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to update this user"
            )
        
        # Handle password changes
        if "password" in update_data:
            if not target_user.can_change_password_by(requesting_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot change password for this user"
                )
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
            update_data["password_changed_at"] = datetime.utcnow()
        
        # Prevent role changes to/from super user unless requester is super user
        if "role" in update_data or "is_super_user" in update_data:
            if target_user.is_protected_super_user() and not requesting_user.is_protected_super_user():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only super users can modify super user roles"
                )
        
        # Update user
        for key, value in update_data.items():
            if hasattr(target_user, key):
                setattr(target_user, key, value)
        
        target_user.updated_at = datetime.utcnow()
        target_user.updated_by = requesting_user.id
        
        await db.commit()
        await db.refresh(target_user)
        
        logger.info(f"User {target_user.username} updated by {requesting_user.username}")
        return target_user
    
    async def delete_user(
        self,
        db: AsyncSession,
        requesting_user: User,
        user_id: UUID
    ) -> bool:
        """Delete user with proper authorization"""
        
        # Get target user
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        target_user = result.scalar_one_or_none()
        
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user can be deleted
        if not target_user.can_be_deleted_by(requesting_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This user cannot be deleted"
            )
        
        # Super users cannot be deleted (extra protection)
        if target_user.is_protected_super_user():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Super users cannot be deleted"
            )
        
        # Soft delete - deactivate instead of hard delete
        target_user.is_active = False
        target_user.status = UserStatus.INACTIVE
        target_user.updated_at = datetime.utcnow()
        target_user.updated_by = requesting_user.id
        
        await db.commit()
        
        logger.info(f"User {target_user.username} deleted by {requesting_user.username}")
        return True
    
    async def get_user_by_id(
        self,
        db: AsyncSession,
        requesting_user: User,
        user_id: UUID
    ) -> Optional[User]:
        """Get user by ID with proper authorization"""
        
        query = select(User).where(User.id == user_id)
        
        # Company isolation - users can only see users in their company
        if not requesting_user.is_protected_super_user():
            query = query.where(User.company_id == requesting_user.company_id)
        
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if user and not self._can_view_user(requesting_user, user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view this user"
            )
        
        return user
    
    async def list_users(
        self,
        db: AsyncSession,
        requesting_user: User,
        skip: int = 0,
        limit: int = 100,
        app_filter: Optional[str] = None
    ) -> List[User]:
        """List users with proper authorization"""
        
        query = select(User)
        
        # Company isolation - users can only see users in their company
        if not requesting_user.is_protected_super_user():
            query = query.where(User.company_id == requesting_user.company_id)
        
        # Filter by app access if specified
        if app_filter:
            # This would need to be implemented based on the app access logic
            pass
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        users = result.scalars().all()
        
        # Filter users based on permissions
        filtered_users = []
        for user in users:
            if self._can_view_user(requesting_user, user):
                filtered_users.append(user)
        
        return filtered_users
    
    async def change_user_password(
        self,
        db: AsyncSession,
        requesting_user: User,
        user_id: UUID,
        new_password: str,
        current_password: Optional[str] = None
    ) -> bool:
        """Change user password with proper authorization"""
        
        # Get target user
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        target_user = result.scalar_one_or_none()
        
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if password can be changed
        if not target_user.can_change_password_by(requesting_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot change password for this user"
            )
        
        # If changing own password, verify current password
        if requesting_user.id == target_user.id and current_password:
            if not verify_password(current_password, target_user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
        
        # Update password
        target_user.password_hash = get_password_hash(new_password)
        target_user.password_changed_at = datetime.utcnow()
        target_user.updated_at = datetime.utcnow()
        target_user.updated_by = requesting_user.id
        
        await db.commit()
        
        logger.info(f"Password changed for user {target_user.username} by {requesting_user.username}")
        return True
    
    def _can_view_user(self, requesting_user: User, target_user: User) -> bool:
        """Check if requesting user can view target user"""
        
        # Super users can view anyone
        if requesting_user.is_protected_super_user():
            return True
        
        # Users can view themselves
        if requesting_user.id == target_user.id:
            return True
        
        # Company admins can view users in their company
        if (requesting_user.role == UserRole.COMPANY_ADMIN and 
            requesting_user.company_id == target_user.company_id):
            return True
        
        # Managers can view employees in their company
        if (requesting_user.role == UserRole.MANAGER and 
            requesting_user.company_id == target_user.company_id and
            target_user.role in [UserRole.EMPLOYEE, UserRole.VIEWER]):
            return True
        
        return False
    
    def _can_update_user(self, requesting_user: User, target_user: User) -> bool:
        """Check if requesting user can update target user"""
        
        # Super users can update anyone (except other super users unless they're updating themselves)
        if requesting_user.is_protected_super_user():
            if target_user.is_protected_super_user():
                return requesting_user.id == target_user.id
            return True
        
        # Users can update themselves (limited fields)
        if requesting_user.id == target_user.id:
            return True
        
        # Company admins can update users in their company (except super users)
        if (requesting_user.role == UserRole.COMPANY_ADMIN and 
            requesting_user.company_id == target_user.company_id and
            not target_user.is_protected_super_user()):
            return True
        
        return False


# Create singleton instance
user_management_service = UserManagementService() 