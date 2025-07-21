"""
Contact Method Subtype API endpoints for Greek ERP/CRM System
CRUD operations for configurable contact method subtypes
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...core.database import get_db
from ...models.contact_method_subtype import ContactMethodSubType, SYSTEM_DEFAULT_SUBTYPES
from ...models.contact_method import ContactMethodType
from ...models.user import User
from ...middleware.company_isolation import get_current_user_and_company

router = APIRouter(prefix="/contact-method-subtypes", tags=["Contact Method Subtypes"])

# Pydantic models for request/response

class ContactMethodSubTypeCreateRequest(BaseModel):
    """Request model for creating contact method subtype"""
    method_type: ContactMethodType = Field(..., description="Type of contact method")
    code: str = Field(..., min_length=1, max_length=50, description="Unique code for the subtype")
    name: str = Field(..., min_length=1, max_length=100, description="Display name")
    name_greek: Optional[str] = Field(None, max_length=100, description="Greek display name")
    description: Optional[str] = Field(None, max_length=255, description="Description")
    description_greek: Optional[str] = Field(None, max_length=255, description="Greek description")
    icon: Optional[str] = Field(None, max_length=50, description="Lucide icon name")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    is_default: Optional[bool] = Field(False, description="Is this the default subtype for this method type")
    display_order: Optional[int] = Field(0, description="Sort order for display")
    validation_rules: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom validation rules")
    format_template: Optional[str] = Field(None, max_length=255, description="Display format template")
    auto_suggestions: Optional[List[str]] = Field(default_factory=list, description="Auto-complete suggestions")
    requires_verification: Optional[bool] = Field(False, description="Requires verification")
    allows_marketing: Optional[bool] = Field(True, description="Can be used for marketing")
    business_hours_only: Optional[bool] = Field(False, description="Only during business hours")
    greek_compliance_required: Optional[bool] = Field(False, description="Greek compliance required")
    aade_field_mapping: Optional[str] = Field(None, max_length=100, description="AADE XML field mapping")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")
    
    @validator('code')
    def validate_code(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Code must contain only letters, numbers, underscores, and hyphens')
        return v.lower()
    
    @validator('color')
    def validate_color(cls, v):
        if v and not v.startswith('#'):
            raise ValueError('Color must be a hex color code starting with #')
        if v and len(v) != 7:
            raise ValueError('Color must be a 7-character hex code (e.g., #3B82F6)')
        return v


class ContactMethodSubTypeUpdateRequest(BaseModel):
    """Request model for updating contact method subtype"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_greek: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    description_greek: Optional[str] = Field(None, max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None
    validation_rules: Optional[Dict[str, Any]] = None
    format_template: Optional[str] = Field(None, max_length=255)
    auto_suggestions: Optional[List[str]] = None
    requires_verification: Optional[bool] = None
    allows_marketing: Optional[bool] = None
    business_hours_only: Optional[bool] = None
    greek_compliance_required: Optional[bool] = None
    aade_field_mapping: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    
    @validator('color')
    def validate_color(cls, v):
        if v and not v.startswith('#'):
            raise ValueError('Color must be a hex color code starting with #')
        if v and len(v) != 7:
            raise ValueError('Color must be a 7-character hex code (e.g., #3B82F6)')
        return v


class ContactMethodSubTypeResponse(BaseModel):
    """Response model for contact method subtype"""
    id: UUID
    company_id: UUID
    method_type: ContactMethodType
    code: str
    name: str
    name_greek: Optional[str]
    display_name: str
    description: Optional[str]
    description_greek: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    is_system: bool
    is_active: bool
    is_default: bool
    display_order: int
    usage_count: int
    last_used: Optional[datetime]
    validation_rules: Dict[str, Any]
    format_template: Optional[str]
    auto_suggestions: List[str]
    requires_verification: bool
    allows_marketing: bool
    business_hours_only: bool
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SubtypeSeeedingRequest(BaseModel):
    """Request model for seeding default subtypes"""
    force_recreate: Optional[bool] = Field(False, description="Force recreate all system subtypes")


# API Endpoints

@router.get("/", response_model=List[ContactMethodSubTypeResponse])
async def list_contact_method_subtypes(
    method_type: Optional[ContactMethodType] = Query(None, description="Filter by method type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    include_system: Optional[bool] = Query(True, description="Include system subtypes"),
    include_custom: Optional[bool] = Query(True, description="Include custom subtypes"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """List contact method subtypes with filtering"""
    user, company_id = current_user_and_company
    
    query = db.query(ContactMethodSubType).filter(
        ContactMethodSubType.company_id == company_id
    )
    
    # Apply filters
    if method_type:
        query = query.filter(ContactMethodSubType.method_type == method_type)
    
    if is_active is not None:
        query = query.filter(ContactMethodSubType.is_active == is_active)
    
    if not include_system:
        query = query.filter(ContactMethodSubType.is_system == False)
    
    if not include_custom:
        query = query.filter(ContactMethodSubType.is_system == True)
    
    if search:
        search_filter = or_(
            ContactMethodSubType.name.ilike(f"%{search}%"),
            ContactMethodSubType.name_greek.ilike(f"%{search}%"),
            ContactMethodSubType.description.ilike(f"%{search}%"),
            ContactMethodSubType.code.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Order by display_order, then by name
    query = query.order_by(
        ContactMethodSubType.method_type,
        ContactMethodSubType.display_order,
        ContactMethodSubType.name
    )
    
    subtypes = query.all()
    return [subtype.to_dict() for subtype in subtypes]


@router.get("/{subtype_id}", response_model=ContactMethodSubTypeResponse)
async def get_contact_method_subtype(
    subtype_id: UUID = Path(..., description="Contact method subtype ID"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Get a specific contact method subtype"""
    user, company_id = current_user_and_company
    
    subtype = db.query(ContactMethodSubType).filter(
        and_(
            ContactMethodSubType.id == subtype_id,
            ContactMethodSubType.company_id == company_id
        )
    ).first()
    
    if not subtype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method subtype not found"
        )
    
    return subtype.to_dict()


@router.post("/", response_model=ContactMethodSubTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_method_subtype(
    subtype_data: ContactMethodSubTypeCreateRequest,
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Create a new contact method subtype"""
    user, company_id = current_user_and_company
    
    # Check if code already exists for this company and method type
    existing = db.query(ContactMethodSubType).filter(
        and_(
            ContactMethodSubType.company_id == company_id,
            ContactMethodSubType.method_type == subtype_data.method_type,
            ContactMethodSubType.code == subtype_data.code
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subtype with code '{subtype_data.code}' already exists for {subtype_data.method_type.value}"
        )
    
    # If this is set as default, unset other defaults for this method type
    if subtype_data.is_default:
        db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.company_id == company_id,
                ContactMethodSubType.method_type == subtype_data.method_type,
                ContactMethodSubType.is_default == True
            )
        ).update({"is_default": False})
    
    # Create the subtype
    subtype = ContactMethodSubType(
        company_id=company_id,
        method_type=subtype_data.method_type,
        code=subtype_data.code,
        name=subtype_data.name,
        name_greek=subtype_data.name_greek,
        description=subtype_data.description,
        description_greek=subtype_data.description_greek,
        icon=subtype_data.icon,
        color=subtype_data.color,
        is_default=subtype_data.is_default,
        display_order=subtype_data.display_order,
        validation_rules=subtype_data.validation_rules,
        format_template=subtype_data.format_template,
        auto_suggestions=subtype_data.auto_suggestions,
        requires_verification=subtype_data.requires_verification,
        allows_marketing=subtype_data.allows_marketing,
        business_hours_only=subtype_data.business_hours_only,
        greek_compliance_required=subtype_data.greek_compliance_required,
        aade_field_mapping=subtype_data.aade_field_mapping,
        tags=subtype_data.tags,
        created_by=user.id
    )
    
    db.add(subtype)
    db.commit()
    db.refresh(subtype)
    
    return subtype.to_dict()


@router.put("/{subtype_id}", response_model=ContactMethodSubTypeResponse)
async def update_contact_method_subtype(
    subtype_id: UUID = Path(..., description="Contact method subtype ID"),
    subtype_data: ContactMethodSubTypeUpdateRequest = ...,
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Update a contact method subtype"""
    user, company_id = current_user_and_company
    
    subtype = db.query(ContactMethodSubType).filter(
        and_(
            ContactMethodSubType.id == subtype_id,
            ContactMethodSubType.company_id == company_id
        )
    ).first()
    
    if not subtype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method subtype not found"
        )
    
    # Prevent editing system subtypes (only activation/deactivation allowed)
    if subtype.is_system and any([
        subtype_data.name,
        subtype_data.name_greek, 
        subtype_data.description,
        subtype_data.description_greek,
        subtype_data.icon,
        subtype_data.color
    ]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify core properties of system subtypes"
        )
    
    # If setting as default, unset other defaults
    if subtype_data.is_default:
        db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.company_id == company.id,
                ContactMethodSubType.method_type == subtype.method_type,
                ContactMethodSubType.is_default == True,
                ContactMethodSubType.id != subtype_id
            )
        ).update({"is_default": False})
    
    # Update fields
    update_data = subtype_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subtype, field, value)
    
    subtype.updated_by = user.id
    
    db.commit()
    db.refresh(subtype)
    
    return subtype.to_dict()


@router.delete("/{subtype_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_method_subtype(
    subtype_id: UUID = Path(..., description="Contact method subtype ID"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Delete a contact method subtype (soft delete for system subtypes)"""
    user, company_id = current_user_and_company
    
    subtype = db.query(ContactMethodSubType).filter(
        and_(
            ContactMethodSubType.id == subtype_id,
            ContactMethodSubType.company_id == company_id
        )
    ).first()
    
    if not subtype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method subtype not found"
        )
    
    # Check if subtype is in use
    from ...models.contact_method import ContactMethod
    usage_count = db.query(ContactMethod).filter(
        ContactMethod.subtype_id == subtype_id
    ).count()
    
    if usage_count > 0:
        # Soft delete - deactivate instead of removing
        subtype.is_active = False
        subtype.updated_by = user.id
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete subtype in use by {usage_count} contact methods. Subtype has been deactivated instead."
        )
    
    # System subtypes should be deactivated, not deleted
    if subtype.is_system:
        subtype.is_active = False
        subtype.updated_by = user.id
        db.commit()
    else:
        # Custom subtypes can be deleted
        db.delete(subtype)
        db.commit()


@router.post("/seed-defaults", response_model=Dict[str, Any])
async def seed_default_subtypes(
    seed_data: SubtypeSeeedingRequest = SubtypeSeeedingRequest(),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Seed default system subtypes for the company"""
    user, company_id = current_user_and_company
    
    created_count = 0
    updated_count = 0
    
    for default_subtype in SYSTEM_DEFAULT_SUBTYPES:
        existing = db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.company_id == company_id,
                ContactMethodSubType.method_type == default_subtype["method_type"],
                ContactMethodSubType.code == default_subtype["code"]
            )
        ).first()
        
        if existing and not seed_data.force_recreate:
            continue
        
        if existing and seed_data.force_recreate:
            # Update existing
            for key, value in default_subtype.items():
                if key != "method_type":  # Don't update the type
                    setattr(existing, key, value)
            existing.updated_by = user.id
            updated_count += 1
        else:
            # Create new
            subtype = ContactMethodSubType(
                company_id=company_id,
                created_by=user.id,
                **default_subtype
            )
            db.add(subtype)
            created_count += 1
    
    db.commit()
    
    return {
        "message": "Default subtypes seeded successfully",
        "created_count": created_count,
        "updated_count": updated_count,
        "total_defaults": len(SYSTEM_DEFAULT_SUBTYPES)
    }


@router.get("/method-types/options", response_model=List[Dict[str, Any]])
async def get_method_type_options():
    """Get available contact method types for UI"""
    return [
        {
            "value": method_type.value,
            "label": method_type.value.title(),
            "icon": {
                "phone": "phone",
                "mobile": "smartphone", 
                "email": "mail",
                "address": "map-pin",
                "fax": "printer",
                "website": "globe",
                "social_media": "users"
            }.get(method_type.value, "circle")
        }
        for method_type in ContactMethodType
    ] 