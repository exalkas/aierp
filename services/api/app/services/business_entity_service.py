"""
Business Entity Service
Comprehensive service for managing business entities (customers, suppliers, partners)
with Greek business compliance and multi-tenant support
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.exc import IntegrityError

from ..models.business_entity import (
    BusinessEntity, BusinessEntityType, BusinessEntityStatus, 
    BusinessEntityRole, PaymentTerms, business_entity_roles
)
from ..models.contact import Contact, ContactType, ContactStatus
from ..models.user import User
from ..utils.greek_validation import (
    validate_afm, validate_doy, validate_greek_address, 
    validate_greek_phone, get_doy_list, search_doy
)

logger = logging.getLogger(__name__)


class BusinessEntityService:
    """Service for managing business entities with Greek compliance"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_business_entity(
        self, 
        entity_data: Dict[str, Any], 
        requesting_user: User,
        validate_greek_fields: bool = True
    ) -> BusinessEntity:
        """
        Create a new business entity with validation
        
        Args:
            entity_data: Business entity data
            requesting_user: User creating the entity
            validate_greek_fields: Whether to validate Greek-specific fields
            
        Returns:
            Created BusinessEntity
        """
        try:
            # Validate user permissions
            if not self._can_create_entity(requesting_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to create business entities"
                )
            
            # Company isolation - ensure entity belongs to user's company
            entity_data["company_id"] = str(requesting_user.company_id)
            entity_data["created_by"] = str(requesting_user.id)
            
            # Generate entity code if not provided
            if "entity_code" not in entity_data or not entity_data["entity_code"]:
                entity_data["entity_code"] = await self._generate_entity_code(requesting_user.company_id)
            
            # Validate Greek business fields if enabled
            if validate_greek_fields:
                validation_result = self._validate_greek_business_data(entity_data)
                if not validation_result["is_valid"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Greek validation failed: {validation_result['errors']}"
                    )
            
            # Validate required fields
            self._validate_required_fields(entity_data)
            
            # Set default values
            entity_data.setdefault("entity_type", BusinessEntityType.BUSINESS)
            entity_data.setdefault("status", BusinessEntityStatus.ACTIVE)
            entity_data.setdefault("language", "el")
            entity_data.setdefault("address_country", "GR")
            
            # Extract roles before creating entity (roles are handled separately)
            roles = entity_data.pop("roles", [])
            
            # Create business entity
            business_entity = BusinessEntity(**entity_data)
            self.db.add(business_entity)
            self.db.flush()  # Get ID without committing
            
            # Assign default roles if specified
            if roles:
                await self._assign_roles(business_entity.id, roles, requesting_user.id)
            
            self.db.commit()
            self.db.refresh(business_entity)
            
            logger.info(f"Business entity {business_entity.entity_code} created by {requesting_user.username}")
            return business_entity
            
        except HTTPException:
            self.db.rollback()
            raise
        except IntegrityError as e:
            self.db.rollback()
            if "entity_code" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Entity code already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity error"
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating business entity: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create business entity"
            )
    
    async def get_business_entity(
        self, 
        entity_id: UUID, 
        requesting_user: User,
        include_contacts: bool = False
    ) -> Optional[BusinessEntity]:
        """Get business entity by ID with company isolation"""
        
        query = self.db.query(BusinessEntity).filter(BusinessEntity.id == entity_id)
        
        # Company isolation
        if not requesting_user.is_super_user:
            query = query.filter(BusinessEntity.company_id == requesting_user.company_id)
        
        entity = query.first()
        
        if not entity:
            return None
        
        # Load contacts if requested
        if include_contacts:
            entity.contacts = self.db.query(Contact).filter(
                Contact.business_entity_id == entity_id
            ).all()
        
        return entity
    
    async def update_business_entity(
        self, 
        entity_id: UUID, 
        update_data: Dict[str, Any], 
        requesting_user: User,
        validate_greek_fields: bool = True
    ) -> BusinessEntity:
        """Update business entity with validation"""
        
        try:
            # Get existing entity
            entity = await self.get_business_entity(entity_id, requesting_user)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business entity not found"
                )
            
            # Check permissions
            if not self._can_update_entity(requesting_user, entity):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to update this business entity"
                )
            
            # Validate Greek business fields if enabled
            if validate_greek_fields and any(key in update_data for key in ["afm", "doy", "address_postal_code"]):
                # Merge with existing data for validation
                merged_data = {**entity.to_dict(include_sensitive=True), **update_data}
                validation_result = self._validate_greek_business_data(merged_data)
                if not validation_result["is_valid"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Greek validation failed: {validation_result['errors']}"
                    )
            
            # Update entity
            for key, value in update_data.items():
                if hasattr(entity, key) and key not in ["id", "company_id", "created_at", "created_by"]:
                    setattr(entity, key, value)
            
            entity.updated_at = datetime.utcnow()
            entity.updated_by = requesting_user.id
            
            # Handle role updates
            if "roles" in update_data:
                await self._update_roles(entity_id, update_data["roles"], requesting_user.id)
            
            self.db.commit()
            self.db.refresh(entity)
            
            logger.info(f"Business entity {entity.entity_code} updated by {requesting_user.username}")
            return entity
            
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating business entity: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update business entity"
            )
    
    async def delete_business_entity(
        self, 
        entity_id: UUID, 
        requesting_user: User,
        soft_delete: bool = True
    ) -> bool:
        """Delete business entity (soft delete by default)"""
        
        try:
            entity = await self.get_business_entity(entity_id, requesting_user)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business entity not found"
                )
            
            # Check permissions
            if not self._can_delete_entity(requesting_user, entity):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to delete this business entity"
                )
            
            # Check if entity has dependencies (invoices, orders, etc.)
            if await self._has_dependencies(entity_id):
                if not soft_delete:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot delete business entity with existing transactions"
                    )
            
            if soft_delete:
                # Soft delete - deactivate entity
                entity.status = BusinessEntityStatus.INACTIVE
                entity.updated_at = datetime.utcnow()
                entity.updated_by = requesting_user.id
                
                # Deactivate associated contacts
                self.db.query(Contact).filter(
                    Contact.business_entity_id == entity_id
                ).update({"status": ContactStatus.INACTIVE})
                
            else:
                # Hard delete - remove from database
                self.db.delete(entity)
            
            self.db.commit()
            
            delete_type = "soft" if soft_delete else "hard"
            logger.info(f"Business entity {entity.entity_code} {delete_type} deleted by {requesting_user.username}")
            return True
            
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting business entity: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete business entity"
            )
    
    async def list_business_entities(
        self,
        requesting_user: User,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        entity_type: Optional[BusinessEntityType] = None,
        status: Optional[BusinessEntityStatus] = None,
        role_filter: Optional[BusinessEntityRole] = None,
        sort_by: str = "display_name",
        sort_order: str = "asc"
    ) -> Tuple[List[BusinessEntity], int]:
        """List business entities with filtering and pagination"""
        
        query = self.db.query(BusinessEntity)
        
        # Company isolation
        if not requesting_user.is_super_user:
            query = query.filter(BusinessEntity.company_id == requesting_user.company_id)
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    BusinessEntity.display_name.ilike(search_term),
                    BusinessEntity.business_name.ilike(search_term),
                    BusinessEntity.email.ilike(search_term),
                    BusinessEntity.afm.ilike(search_term),
                    BusinessEntity.entity_code.ilike(search_term)
                )
            )
        
        if entity_type:
            query = query.filter(BusinessEntity.entity_type == entity_type)
        
        if status:
            query = query.filter(BusinessEntity.status == status)
        
        # Role filtering would require a join with business_entity_roles table
        if role_filter:
            query = query.join(business_entity_roles).filter(
                business_entity_roles.c.role == role_filter,
                business_entity_roles.c.is_active == True
            )
        
        # Get total count
        total_count = query.count()
        
        # Apply sorting
        if hasattr(BusinessEntity, sort_by):
            sort_column = getattr(BusinessEntity, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(asc(BusinessEntity.display_name))
        
        # Apply pagination
        entities = query.offset(skip).limit(limit).all()
        
        return entities, total_count
    
    async def assign_role(
        self, 
        entity_id: UUID, 
        role: BusinessEntityRole, 
        requesting_user: User,
        notes: Optional[str] = None
    ) -> bool:
        """Assign a role to a business entity"""
        
        try:
            entity = await self.get_business_entity(entity_id, requesting_user)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business entity not found"
                )
            
            # Check if role already exists
            existing_role = self.db.execute(
                business_entity_roles.select().where(
                    and_(
                        business_entity_roles.c.business_entity_id == entity_id,
                        business_entity_roles.c.role == role,
                        business_entity_roles.c.is_active == True
                    )
                )
            ).first()
            
            if existing_role:
                return True  # Role already assigned
            
            # Insert new role
            self.db.execute(
                business_entity_roles.insert().values(
                    business_entity_id=entity_id,
                    role=role,
                    assigned_by=requesting_user.id,
                    notes=notes
                )
            )
            
            self.db.commit()
            
            logger.info(f"Role {role.value} assigned to entity {entity.entity_code} by {requesting_user.username}")
            return True
            
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error assigning role: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to assign role"
            )
    
    async def remove_role(
        self, 
        entity_id: UUID, 
        role: BusinessEntityRole, 
        requesting_user: User
    ) -> bool:
        """Remove a role from a business entity"""
        
        try:
            entity = await self.get_business_entity(entity_id, requesting_user)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business entity not found"
                )
            
            # Deactivate role
            self.db.execute(
                business_entity_roles.update().where(
                    and_(
                        business_entity_roles.c.business_entity_id == entity_id,
                        business_entity_roles.c.role == role,
                        business_entity_roles.c.is_active == True
                    )
                ).values(is_active=False)
            )
            
            self.db.commit()
            
            logger.info(f"Role {role.value} removed from entity {entity.entity_code} by {requesting_user.username}")
            return True
            
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing role: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove role"
            )
    
    async def get_entity_roles(self, entity_id: UUID, requesting_user: User) -> List[Dict[str, Any]]:
        """Get all active roles for a business entity"""
        
        entity = await self.get_business_entity(entity_id, requesting_user)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business entity not found"
            )
        
        roles = self.db.execute(
            business_entity_roles.select().where(
                and_(
                    business_entity_roles.c.business_entity_id == entity_id,
                    business_entity_roles.c.is_active == True
                )
            )
        ).fetchall()
        
        return [
            {
                "role": role.role.value,
                "assigned_at": role.assigned_at.isoformat(),
                "notes": role.notes
            }
            for role in roles
        ]
    
    def validate_afm(self, afm: str) -> Dict[str, Any]:
        """Validate Greek AFM"""
        return validate_afm(afm)
    
    def validate_doy(self, doy: str) -> Dict[str, Any]:
        """Validate Greek DOY"""
        return validate_doy(doy)
    
    def get_doy_list(self) -> List[Dict[str, str]]:
        """Get list of all DOY offices"""
        return get_doy_list()
    
    def search_doy(self, query: str) -> List[Dict[str, str]]:
        """Search DOY offices"""
        return search_doy(query)
    
    # Private helper methods
    
    def _can_create_entity(self, user: User) -> bool:
        """Check if user can create business entities"""
        return user.has_permission("business_entities:create") if hasattr(user, 'has_permission') else True
    
    def _can_update_entity(self, user: User, entity: BusinessEntity) -> bool:
        """Check if user can update business entity"""
        return user.has_permission("business_entities:update") if hasattr(user, 'has_permission') else True
    
    def _can_delete_entity(self, user: User, entity: BusinessEntity) -> bool:
        """Check if user can delete business entity"""
        return user.has_permission("business_entities:delete") if hasattr(user, 'has_permission') else True
    
    async def _generate_entity_code(self, company_id: UUID) -> str:
        """Generate unique entity code for company"""
        
        # Get last entity code for company
        last_entity = self.db.query(BusinessEntity).filter(
            BusinessEntity.company_id == company_id
        ).order_by(desc(BusinessEntity.created_at)).first()
        
        if last_entity and last_entity.entity_code:
            # Extract number from last code and increment
            try:
                last_number = int(last_entity.entity_code.split('-')[-1])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        return f"BE-{new_number:06d}"
    
    def _validate_greek_business_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Greek business fields"""
        
        result = {"is_valid": True, "errors": [], "warnings": []}
        
        # Validate AFM if present
        if data.get("afm"):
            afm_result = validate_afm(data["afm"])
            if not afm_result["is_valid"]:
                result["is_valid"] = False
                result["errors"].append(f"AFM: {afm_result['error']}")
        
        # Validate DOY if present
        if data.get("doy"):
            doy_result = validate_doy(data["doy"])
            if not doy_result["is_valid"]:
                result["is_valid"] = False
                result["errors"].append(f"DOY: {doy_result['error']}")
        
        # Validate address if present
        address_fields = ["address_street", "address_city", "address_postal_code"]
        if any(field in data for field in address_fields):
            address_data = {
                field: data.get(field) for field in address_fields
            }
            address_result = validate_greek_address(address_data)
            if not address_result["is_valid"]:
                result["is_valid"] = False
                result["errors"].extend(address_result["errors"])
            result["warnings"].extend(address_result.get("warnings", []))
        
        # Validate phone if present
        if data.get("phone"):
            phone_result = validate_greek_phone(data["phone"])
            if not phone_result["is_valid"]:
                result["warnings"].append(f"Phone: {phone_result['error']}")
        
        return result
    
    def _validate_required_fields(self, data: Dict[str, Any]) -> None:
        """Validate required fields"""
        
        required_fields = ["display_name"]
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Required field '{field}' is missing"
                )
    
    async def _assign_roles(self, entity_id: UUID, roles: List[str], assigned_by: UUID) -> None:
        """Assign multiple roles to entity"""
        
        for role_str in roles:
            try:
                role = BusinessEntityRole(role_str)
                self.db.execute(
                    business_entity_roles.insert().values(
                        business_entity_id=entity_id,
                        role=role,
                        assigned_by=assigned_by
                    )
                )
            except ValueError:
                logger.warning(f"Invalid role: {role_str}")
    
    async def _update_roles(self, entity_id: UUID, new_roles: List[str], assigned_by: UUID) -> None:
        """Update entity roles (replace existing with new)"""
        
        # Deactivate all existing roles
        self.db.execute(
            business_entity_roles.update().where(
                and_(
                    business_entity_roles.c.business_entity_id == entity_id,
                    business_entity_roles.c.is_active == True
                )
            ).values(is_active=False)
        )
        
        # Assign new roles
        await self._assign_roles(entity_id, new_roles, assigned_by)
    
    async def _has_dependencies(self, entity_id: UUID) -> bool:
        """Check if entity has dependencies (invoices, orders, etc.)"""
        
        # Check for invoices
        invoice_count = self.db.query(func.count()).select_from(
            self.db.query(BusinessEntity).join("invoices").filter(
                BusinessEntity.id == entity_id
            ).subquery()
        ).scalar()
        
        return invoice_count > 0 