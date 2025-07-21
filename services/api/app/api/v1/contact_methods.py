"""
Contact Method API endpoints for Greek ERP/CRM System
CRUD operations for contact methods (phones, emails, addresses)
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...core.database import get_db
from ...models.contact_method import ContactMethod, ContactMethodType, ContactMethodStatus
from ...models.contact_method_subtype import ContactMethodSubType
from ...models.business_entity import BusinessEntity
from ...models.contact import Contact
from ...models.user import User
from ...middleware.company_isolation import get_current_user_and_company

router = APIRouter(prefix="/contact-methods", tags=["Contact Methods"])

# Pydantic models for request/response

class ContactMethodCreateRequest(BaseModel):
    """Request model for creating contact method"""
    business_entity_id: Optional[UUID] = Field(None, description="Business entity ID (if for business entity)")
    contact_id: Optional[UUID] = Field(None, description="Contact ID (if for contact person)")
    method_type: ContactMethodType = Field(..., description="Type of contact method")
    subtype_id: UUID = Field(..., description="Contact method subtype ID")
    value: str = Field(..., min_length=1, max_length=500, description="Contact method value")
    label: Optional[str] = Field(None, max_length=100, description="Custom label")
    description: Optional[str] = Field(None, description="Additional notes")
    
    # Priority and preferences
    is_primary: Optional[bool] = Field(False, description="Primary method of this type")
    is_preferred: Optional[bool] = Field(False, description="User's preferred method")
    priority_order: Optional[int] = Field(0, description="1=highest, 2=second, etc.")
    
    # Phone/Mobile specific fields
    country_code: Optional[str] = Field(None, max_length=5, description="Country code (+30)")
    area_code: Optional[str] = Field(None, max_length=10, description="Area code")
    extension: Optional[str] = Field(None, max_length=10, description="Extension")
    
    # Address specific fields
    address_street: Optional[str] = Field(None, max_length=255, description="Street name")
    address_number: Optional[str] = Field(None, max_length=10, description="Street number")
    address_floor: Optional[str] = Field(None, max_length=10, description="Floor")
    address_apartment: Optional[str] = Field(None, max_length=10, description="Apartment")
    address_city: Optional[str] = Field(None, max_length=100, description="City")
    address_postal_code: Optional[str] = Field(None, max_length=10, description="Postal code")
    address_region: Optional[str] = Field(None, max_length=100, description="Region")
    address_country: Optional[str] = Field("GR", max_length=2, description="Country code")
    
    # Website/Social Media specific
    platform_name: Optional[str] = Field(None, max_length=100, description="Platform name")
    username: Optional[str] = Field(None, max_length=100, description="Username")
    url: Optional[str] = Field(None, max_length=500, description="Full URL")
    
    # Operational settings
    allow_marketing: Optional[bool] = Field(False, description="Can be used for marketing")
    allow_notifications: Optional[bool] = Field(True, description="Can be used for notifications")
    business_hours_only: Optional[bool] = Field(False, description="Only contact during business hours")
    
    # Time-based availability
    available_from: Optional[str] = Field(None, max_length=5, description="Available from (HH:MM)")
    available_until: Optional[str] = Field(None, max_length=5, description="Available until (HH:MM)")
    timezone: Optional[str] = Field("Europe/Athens", max_length=50, description="Timezone")
    
    # Custom fields
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")
    
    @validator('available_from', 'available_until')
    def validate_time_format(cls, v):
        if v:
            try:
                hour, minute = v.split(':')
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    raise ValueError('Invalid time format')
            except:
                raise ValueError('Time must be in HH:MM format')
        return v
    
    @validator('address_postal_code')
    def validate_greek_postal_code(cls, v, values):
        if v and values.get('address_country') == 'GR':
            if not v.isdigit() or len(v) != 5:
                raise ValueError('Greek postal code must be 5 digits')
        return v


class ContactMethodUpdateRequest(BaseModel):
    """Request model for updating contact method"""
    value: Optional[str] = Field(None, min_length=1, max_length=500)
    label: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    subtype_id: Optional[UUID] = None
    status: Optional[ContactMethodStatus] = None
    is_primary: Optional[bool] = None
    is_preferred: Optional[bool] = None
    priority_order: Optional[int] = None
    
    # Phone/Mobile specific fields
    country_code: Optional[str] = Field(None, max_length=5)
    area_code: Optional[str] = Field(None, max_length=10)
    extension: Optional[str] = Field(None, max_length=10)
    
    # Address specific fields
    address_street: Optional[str] = Field(None, max_length=255)
    address_number: Optional[str] = Field(None, max_length=10)
    address_floor: Optional[str] = Field(None, max_length=10)
    address_apartment: Optional[str] = Field(None, max_length=10)
    address_city: Optional[str] = Field(None, max_length=100)
    address_postal_code: Optional[str] = Field(None, max_length=10)
    address_region: Optional[str] = Field(None, max_length=100)
    address_country: Optional[str] = Field(None, max_length=2)
    
    # Website/Social Media specific
    platform_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=100)
    url: Optional[str] = Field(None, max_length=500)
    
    # Operational settings
    allow_marketing: Optional[bool] = None
    allow_notifications: Optional[bool] = None
    business_hours_only: Optional[bool] = None
    
    # Time-based availability
    available_from: Optional[str] = Field(None, max_length=5)
    available_until: Optional[str] = Field(None, max_length=5)
    timezone: Optional[str] = Field(None, max_length=50)
    
    # Custom fields
    tags: Optional[List[str]] = None


class ContactMethodResponse(BaseModel):
    """Response model for contact method"""
    id: UUID
    company_id: UUID
    business_entity_id: Optional[UUID]
    contact_id: Optional[UUID]
    method_type: ContactMethodType
    subtype_id: UUID
    subtype: Dict[str, Any]
    status: ContactMethodStatus
    value: str
    formatted_value: str
    label: Optional[str]
    display_label: str
    description: Optional[str]
    is_primary: bool
    is_preferred: bool
    priority_order: int
    is_valid: bool
    validated_date: Optional[datetime]
    quality_score: Optional[int]
    last_used: Optional[datetime]
    usage_count: int
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    # Type-specific fields will be included based on method_type
    
    class Config:
        from_attributes = True


# API Endpoints

@router.get("/", response_model=List[ContactMethodResponse])
async def list_contact_methods(
    business_entity_id: Optional[UUID] = Query(None, description="Filter by business entity"),
    contact_id: Optional[UUID] = Query(None, description="Filter by contact"),
    method_type: Optional[ContactMethodType] = Query(None, description="Filter by method type"),
    status: Optional[ContactMethodStatus] = Query(None, description="Filter by status"),
    is_primary: Optional[bool] = Query(None, description="Filter by primary status"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in value and labels"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """List contact methods with filtering"""
    user, company = current_user_and_company
    
    query = db.query(ContactMethod).filter(
        ContactMethod.company_id == company.id
    )
    
    # Apply filters
    if business_entity_id:
        query = query.filter(ContactMethod.business_entity_id == business_entity_id)
    
    if contact_id:
        query = query.filter(ContactMethod.contact_id == contact_id)
    
    if method_type:
        query = query.filter(ContactMethod.method_type == method_type)
    
    if status:
        query = query.filter(ContactMethod.status == status)
    
    if is_primary is not None:
        query = query.filter(ContactMethod.is_primary == is_primary)
    
    if is_active is not None:
        if is_active:
            query = query.filter(ContactMethod.status == ContactMethodStatus.ACTIVE)
        else:
            query = query.filter(ContactMethod.status != ContactMethodStatus.ACTIVE)
    
    if search:
        search_filter = or_(
            ContactMethod.value.ilike(f"%{search}%"),
            ContactMethod.label.ilike(f"%{search}%"),
            ContactMethod.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Order by type, primary status, preference, and priority
    query = query.order_by(
        ContactMethod.method_type,
        ContactMethod.is_primary.desc(),
        ContactMethod.is_preferred.desc(),
        ContactMethod.priority_order,
        ContactMethod.created_at
    )
    
    contact_methods = query.all()
    return [contact_method.to_dict(include_sensitive=False) for contact_method in contact_methods]


@router.get("/{contact_method_id}", response_model=ContactMethodResponse)
async def get_contact_method(
    contact_method_id: UUID = Path(..., description="Contact method ID"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Get a specific contact method"""
    user, company = current_user_and_company
    
    contact_method = db.query(ContactMethod).filter(
        and_(
            ContactMethod.id == contact_method_id,
            ContactMethod.company_id == company.id
        )
    ).first()
    
    if not contact_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method not found"
        )
    
    return contact_method.to_dict(include_sensitive=True)


@router.post("/", response_model=ContactMethodResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_method(
    contact_method_data: ContactMethodCreateRequest,
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Create a new contact method"""
    user, company = current_user_and_company
    
    # Validate that either business_entity_id OR contact_id is provided
    if not contact_method_data.business_entity_id and not contact_method_data.contact_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either business_entity_id or contact_id must be provided"
        )
    
    if contact_method_data.business_entity_id and contact_method_data.contact_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot specify both business_entity_id and contact_id"
        )
    
    # Validate subtype exists and belongs to the same company
    subtype = db.query(ContactMethodSubType).filter(
        and_(
            ContactMethodSubType.id == contact_method_data.subtype_id,
            ContactMethodSubType.company_id == company.id,
            ContactMethodSubType.method_type == contact_method_data.method_type,
            ContactMethodSubType.is_active == True
        )
    ).first()
    
    if not subtype:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subtype for this method type or company"
        )
    
    # Validate business entity or contact exists and belongs to company
    if contact_method_data.business_entity_id:
        entity = db.query(BusinessEntity).filter(
            and_(
                BusinessEntity.id == contact_method_data.business_entity_id,
                BusinessEntity.company_id == company.id
            )
        ).first()
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business entity not found or not accessible"
            )
    
    if contact_method_data.contact_id:
        contact = db.query(Contact).filter(
            and_(
                Contact.id == contact_method_data.contact_id,
                Contact.company_id == company.id
            )
        ).first()
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact not found or not accessible"
            )
    
    # If setting as primary, unset other primary methods of same type
    if contact_method_data.is_primary:
        existing_primary_query = db.query(ContactMethod).filter(
            and_(
                ContactMethod.company_id == company.id,
                ContactMethod.method_type == contact_method_data.method_type,
                ContactMethod.is_primary == True
            )
        )
        
        if contact_method_data.business_entity_id:
            existing_primary_query = existing_primary_query.filter(
                ContactMethod.business_entity_id == contact_method_data.business_entity_id
            )
        else:
            existing_primary_query = existing_primary_query.filter(
                ContactMethod.contact_id == contact_method_data.contact_id
            )
        
        existing_primary_query.update({"is_primary": False})
    
    # Create the contact method
    contact_method = ContactMethod(
        company_id=company.id,
        business_entity_id=contact_method_data.business_entity_id,
        contact_id=contact_method_data.contact_id,
        method_type=contact_method_data.method_type,
        subtype_id=contact_method_data.subtype_id,
        value=contact_method_data.value,
        label=contact_method_data.label,
        description=contact_method_data.description,
        is_primary=contact_method_data.is_primary,
        is_preferred=contact_method_data.is_preferred,
        priority_order=contact_method_data.priority_order,
        
        # Phone/Mobile fields
        country_code=contact_method_data.country_code,
        area_code=contact_method_data.area_code,
        extension=contact_method_data.extension,
        
        # Address fields
        address_street=contact_method_data.address_street,
        address_number=contact_method_data.address_number,
        address_floor=contact_method_data.address_floor,
        address_apartment=contact_method_data.address_apartment,
        address_city=contact_method_data.address_city,
        address_postal_code=contact_method_data.address_postal_code,
        address_region=contact_method_data.address_region,
        address_country=contact_method_data.address_country,
        
        # Website/Social Media fields
        platform_name=contact_method_data.platform_name,
        username=contact_method_data.username,
        url=contact_method_data.url,
        
        # Operational settings
        allow_marketing=contact_method_data.allow_marketing,
        allow_notifications=contact_method_data.allow_notifications,
        business_hours_only=contact_method_data.business_hours_only,
        available_from=contact_method_data.available_from,
        available_until=contact_method_data.available_until,
        timezone=contact_method_data.timezone,
        
        # Custom fields
        tags=contact_method_data.tags
    )
    
    # Validate the contact method value
    contact_method.is_valid = contact_method.validate_value()
    if contact_method.is_valid:
        contact_method.validated_date = datetime.utcnow()
        contact_method.validation_method = "system"
    
    db.add(contact_method)
    db.commit()
    db.refresh(contact_method)
    
    return contact_method.to_dict(include_sensitive=False)


@router.put("/{contact_method_id}", response_model=ContactMethodResponse)
async def update_contact_method(
    contact_method_id: UUID = Path(..., description="Contact method ID"),
    contact_method_data: ContactMethodUpdateRequest = ...,
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Update a contact method"""
    user, company = current_user_and_company
    
    contact_method = db.query(ContactMethod).filter(
        and_(
            ContactMethod.id == contact_method_id,
            ContactMethod.company_id == company.id
        )
    ).first()
    
    if not contact_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method not found"
        )
    
    # Validate subtype if provided
    if contact_method_data.subtype_id:
        subtype = db.query(ContactMethodSubType).filter(
            and_(
                ContactMethodSubType.id == contact_method_data.subtype_id,
                ContactMethodSubType.company_id == company.id,
                ContactMethodSubType.method_type == contact_method.method_type,
                ContactMethodSubType.is_active == True
            )
        ).first()
        
        if not subtype:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid subtype for this method type or company"
            )
    
    # If setting as primary, unset other primary methods of same type
    if contact_method_data.is_primary:
        existing_primary_query = db.query(ContactMethod).filter(
            and_(
                ContactMethod.company_id == company.id,
                ContactMethod.method_type == contact_method.method_type,
                ContactMethod.is_primary == True,
                ContactMethod.id != contact_method_id
            )
        )
        
        if contact_method.business_entity_id:
            existing_primary_query = existing_primary_query.filter(
                ContactMethod.business_entity_id == contact_method.business_entity_id
            )
        else:
            existing_primary_query = existing_primary_query.filter(
                ContactMethod.contact_id == contact_method.contact_id
            )
        
        existing_primary_query.update({"is_primary": False})
    
    # Update fields
    update_data = contact_method_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact_method, field, value)
    
    # Re-validate if value changed
    if contact_method_data.value:
        contact_method.is_valid = contact_method.validate_value()
        if contact_method.is_valid:
            contact_method.validated_date = datetime.utcnow()
            contact_method.validation_method = "system"
    
    db.commit()
    db.refresh(contact_method)
    
    return contact_method.to_dict(include_sensitive=False)


@router.delete("/{contact_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_method(
    contact_method_id: UUID = Path(..., description="Contact method ID"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Delete a contact method"""
    user, company = current_user_and_company
    
    contact_method = db.query(ContactMethod).filter(
        and_(
            ContactMethod.id == contact_method_id,
            ContactMethod.company_id == company.id
        )
    ).first()
    
    if not contact_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method not found"
        )
    
    db.delete(contact_method)
    db.commit()


@router.post("/{contact_method_id}/mark-as-used", response_model=Dict[str, Any])
async def mark_contact_method_as_used(
    contact_method_id: UUID = Path(..., description="Contact method ID"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Mark a contact method as recently used (for usage tracking)"""
    user, company = current_user_and_company
    
    contact_method = db.query(ContactMethod).filter(
        and_(
            ContactMethod.id == contact_method_id,
            ContactMethod.company_id == company.id
        )
    ).first()
    
    if not contact_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method not found"
        )
    
    contact_method.mark_as_used()
    db.commit()
    
    return {
        "message": "Contact method marked as used",
        "usage_count": contact_method.usage_count,
        "last_used": contact_method.last_used.isoformat() if contact_method.last_used else None
    }


@router.post("/{contact_method_id}/validate", response_model=Dict[str, Any])
async def validate_contact_method(
    contact_method_id: UUID = Path(..., description="Contact method ID"),
    db: Session = Depends(get_db),
    current_user_and_company = Depends(get_current_user_and_company)
):
    """Validate a contact method value"""
    user, company = current_user_and_company
    
    contact_method = db.query(ContactMethod).filter(
        and_(
            ContactMethod.id == contact_method_id,
            ContactMethod.company_id == company.id
        )
    ).first()
    
    if not contact_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact method not found"
        )
    
    is_valid = contact_method.validate_value()
    
    if is_valid:
        contact_method.is_valid = True
        contact_method.validated_date = datetime.utcnow()
        contact_method.validation_method = "manual"
        contact_method.quality_score = 100
    else:
        contact_method.is_valid = False
        contact_method.quality_score = 0
    
    db.commit()
    
    return {
        "is_valid": is_valid,
        "validated_date": contact_method.validated_date.isoformat() if contact_method.validated_date else None,
        "quality_score": contact_method.quality_score
    } 