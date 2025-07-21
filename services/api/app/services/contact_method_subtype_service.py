"""
Contact Method Subtype Service for Greek ERP/CRM System
Handles business logic for contact method subtypes including default seeding
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from ..models.contact_method_subtype import ContactMethodSubType, SYSTEM_DEFAULT_SUBTYPES
from ..models.contact_method import ContactMethodType
from ..models.company import Company
from ..models.user import User
from ..core.database import get_db


class ContactMethodSubtypeService:
    """Service for managing contact method subtypes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def seed_default_subtypes_for_company(
        self, 
        company_id: UUID, 
        created_by_user_id: UUID,
        force_recreate: bool = False
    ) -> Dict[str, Any]:
        """
        Seed default contact method subtypes for a company
        
        Args:
            company_id: Company to seed subtypes for
            created_by_user_id: User creating the subtypes
            force_recreate: Whether to recreate existing subtypes
            
        Returns:
            Dict with creation statistics
        """
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for default_subtype in SYSTEM_DEFAULT_SUBTYPES:
            existing = self.db.query(ContactMethodSubType).filter(
                and_(
                    ContactMethodSubType.company_id == company_id,
                    ContactMethodSubType.method_type == default_subtype["method_type"],
                    ContactMethodSubType.code == default_subtype["code"]
                )
            ).first()
            
            if existing and not force_recreate:
                skipped_count += 1
                continue
            
            if existing and force_recreate:
                # Update existing
                for key, value in default_subtype.items():
                    if key not in ["method_type"]:  # Don't update the type
                        setattr(existing, key, value)
                existing.updated_by = created_by_user_id
                existing.updated_at = datetime.utcnow()
                updated_count += 1
            else:
                # Create new
                subtype = ContactMethodSubType(
                    company_id=company_id,
                    created_by=created_by_user_id,
                    **default_subtype
                )
                self.db.add(subtype)
                created_count += 1
        
        self.db.commit()
        
        return {
            "message": "Default subtypes seeded successfully",
            "created_count": created_count,
            "updated_count": updated_count,
            "skipped_count": skipped_count,
            "total_defaults": len(SYSTEM_DEFAULT_SUBTYPES)
        }
    
    def get_subtypes_for_company(
        self, 
        company_id: UUID,
        method_type: Optional[ContactMethodType] = None,
        is_active: Optional[bool] = None,
        include_system: bool = True,
        include_custom: bool = True
    ) -> List[ContactMethodSubType]:
        """
        Get contact method subtypes for a company with filtering
        
        Args:
            company_id: Company ID
            method_type: Filter by method type
            is_active: Filter by active status
            include_system: Include system subtypes
            include_custom: Include custom subtypes
            
        Returns:
            List of ContactMethodSubType objects
        """
        query = self.db.query(ContactMethodSubType).filter(
            ContactMethodSubType.company_id == company_id
        )
        
        if method_type:
            query = query.filter(ContactMethodSubType.method_type == method_type)
        
        if is_active is not None:
            query = query.filter(ContactMethodSubType.is_active == is_active)
        
        if not include_system:
            query = query.filter(ContactMethodSubType.is_system == False)
        
        if not include_custom:
            query = query.filter(ContactMethodSubType.is_system == True)
        
        # Order by method type, then display order, then name
        query = query.order_by(
            ContactMethodSubType.method_type,
            ContactMethodSubType.display_order,
            ContactMethodSubType.name
        )
        
        return query.all()
    
    def get_default_subtype_for_method_type(
        self, 
        company_id: UUID, 
        method_type: ContactMethodType
    ) -> Optional[ContactMethodSubType]:
        """
        Get the default subtype for a specific method type and company
        
        Args:
            company_id: Company ID
            method_type: Contact method type
            
        Returns:
            Default ContactMethodSubType or None
        """
        return self.db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.company_id == company_id,
                ContactMethodSubType.method_type == method_type,
                ContactMethodSubType.is_default == True,
                ContactMethodSubType.is_active == True
            )
        ).first()
    
    def create_custom_subtype(
        self,
        company_id: UUID,
        created_by_user_id: UUID,
        method_type: ContactMethodType,
        code: str,
        name: str,
        **kwargs
    ) -> ContactMethodSubType:
        """
        Create a custom contact method subtype
        
        Args:
            company_id: Company ID
            created_by_user_id: User creating the subtype
            method_type: Contact method type
            code: Unique code for the subtype
            name: Display name
            **kwargs: Additional subtype properties
            
        Returns:
            Created ContactMethodSubType
            
        Raises:
            ValueError: If code already exists for this company and method type
        """
        # Check if code already exists
        existing = self.db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.company_id == company_id,
                ContactMethodSubType.method_type == method_type,
                ContactMethodSubType.code == code.lower()
            )
        ).first()
        
        if existing:
            raise ValueError(f"Subtype with code '{code}' already exists for {method_type.value}")
        
        # If this is set as default, unset other defaults for this method type
        if kwargs.get('is_default', False):
            self.db.query(ContactMethodSubType).filter(
                and_(
                    ContactMethodSubType.company_id == company_id,
                    ContactMethodSubType.method_type == method_type,
                    ContactMethodSubType.is_default == True
                )
            ).update({"is_default": False})
        
        # Create the subtype
        subtype = ContactMethodSubType(
            company_id=company_id,
            method_type=method_type,
            code=code.lower(),
            name=name,
            is_system=False,  # Custom subtypes are never system subtypes
            created_by=created_by_user_id,
            **kwargs
        )
        
        self.db.add(subtype)
        self.db.commit()
        self.db.refresh(subtype)
        
        return subtype
    
    def update_subtype(
        self,
        subtype_id: UUID,
        company_id: UUID,
        updated_by_user_id: UUID,
        **updates
    ) -> ContactMethodSubType:
        """
        Update a contact method subtype
        
        Args:
            subtype_id: Subtype ID
            company_id: Company ID (for security)
            updated_by_user_id: User updating the subtype
            **updates: Fields to update
            
        Returns:
            Updated ContactMethodSubType
            
        Raises:
            ValueError: If subtype not found or cannot be updated
        """
        subtype = self.db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.id == subtype_id,
                ContactMethodSubType.company_id == company_id
            )
        ).first()
        
        if not subtype:
            raise ValueError("Contact method subtype not found")
        
        # Prevent editing core properties of system subtypes
        if subtype.is_system and any(key in updates for key in [
            'name', 'name_greek', 'description', 'description_greek', 
            'icon', 'color', 'code'
        ]):
            raise ValueError("Cannot modify core properties of system subtypes")
        
        # If setting as default, unset other defaults
        if updates.get('is_default'):
            self.db.query(ContactMethodSubType).filter(
                and_(
                    ContactMethodSubType.company_id == company_id,
                    ContactMethodSubType.method_type == subtype.method_type,
                    ContactMethodSubType.is_default == True,
                    ContactMethodSubType.id != subtype_id
                )
            ).update({"is_default": False})
        
        # Update fields
        for field, value in updates.items():
            if hasattr(subtype, field):
                setattr(subtype, field, value)
        
        subtype.updated_by = updated_by_user_id
        subtype.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(subtype)
        
        return subtype
    
    def deactivate_subtype(
        self,
        subtype_id: UUID,
        company_id: UUID,
        updated_by_user_id: UUID
    ) -> ContactMethodSubType:
        """
        Deactivate a contact method subtype (soft delete)
        
        Args:
            subtype_id: Subtype ID
            company_id: Company ID (for security)
            updated_by_user_id: User deactivating the subtype
            
        Returns:
            Deactivated ContactMethodSubType
            
        Raises:
            ValueError: If subtype not found or cannot be deactivated
        """
        subtype = self.db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.id == subtype_id,
                ContactMethodSubType.company_id == company_id
            )
        ).first()
        
        if not subtype:
            raise ValueError("Contact method subtype not found")
        
        # Check if subtype is in use
        from ..models.contact_method import ContactMethod
        usage_count = self.db.query(ContactMethod).filter(
            ContactMethod.subtype_id == subtype_id
        ).count()
        
        if usage_count > 0:
            # Soft delete - deactivate instead of removing
            subtype.is_active = False
            subtype.updated_by = updated_by_user_id
            subtype.updated_at = datetime.utcnow()
            self.db.commit()
            
            raise ValueError(
                f"Cannot delete subtype in use by {usage_count} contact methods. "
                f"Subtype has been deactivated instead."
            )
        
        # Deactivate the subtype
        subtype.is_active = False
        subtype.updated_by = updated_by_user_id
        subtype.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(subtype)
        
        return subtype
    
    def get_subtype_usage_stats(
        self, 
        company_id: UUID, 
        subtype_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Get usage statistics for subtypes
        
        Args:
            company_id: Company ID
            subtype_id: Specific subtype ID (optional)
            
        Returns:
            Dict with usage statistics
        """
        from ..models.contact_method import ContactMethod
        
        if subtype_id:
            # Stats for specific subtype
            subtype = self.db.query(ContactMethodSubType).filter(
                and_(
                    ContactMethodSubType.id == subtype_id,
                    ContactMethodSubType.company_id == company_id
                )
            ).first()
            
            if not subtype:
                raise ValueError("Contact method subtype not found")
            
            usage_count = self.db.query(ContactMethod).filter(
                ContactMethod.subtype_id == subtype_id
            ).count()
            
            return {
                "subtype_id": subtype_id,
                "subtype_name": subtype.display_name,
                "usage_count": usage_count,
                "last_used": subtype.last_used.isoformat() if subtype.last_used else None
            }
        else:
            # Stats for all subtypes
            subtypes = self.db.query(ContactMethodSubType).filter(
                ContactMethodSubType.company_id == company_id
            ).all()
            
            stats = []
            total_usage = 0
            
            for subtype in subtypes:
                usage_count = self.db.query(ContactMethod).filter(
                    ContactMethod.subtype_id == subtype.id
                ).count()
                
                total_usage += usage_count
                
                stats.append({
                    "subtype_id": str(subtype.id),
                    "subtype_name": subtype.display_name,
                    "method_type": subtype.method_type.value,
                    "usage_count": usage_count,
                    "is_system": subtype.is_system,
                    "is_active": subtype.is_active,
                    "last_used": subtype.last_used.isoformat() if subtype.last_used else None
                })
            
            return {
                "total_subtypes": len(subtypes),
                "total_usage": total_usage,
                "subtypes": stats
            }


def get_contact_method_subtype_service(db: Session = None) -> ContactMethodSubtypeService:
    """Get a ContactMethodSubtypeService instance"""
    if db is None:
        db = next(get_db())
    return ContactMethodSubtypeService(db) 