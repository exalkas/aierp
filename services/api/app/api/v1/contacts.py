"""
Contact API endpoints for Greek ERP/CRM System
CRUD operations for contacts within business entities
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...core.database import get_db
from ...models.contact import Contact, ContactType, ContactStatus
from ...models.business_entity import BusinessEntity
from ...models.user import User
from ...middleware.company_isolation import get_current_user_and_company

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# Pydantic models for request/response

class ContactCreateRequest(BaseModel):
    """Request model for creating contact"""
    business_entity_id: UUID = Field(..., description="ID of the business entity this contact belongs to")
    contact_type: ContactType = ContactType.PRIMARY
    
    # Personal information
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=255)
    
    # Greek personal information
    father_name: Optional[str] = Field(None, max_length=100)
    mother_name: Optional[str] = Field(None, max_length=100)
    amka: Optional[str] = Field(None, min_length=11, max_length=11)
    id_card_number: Optional[str] = Field(None, max_length=20)
    
    # Professional information
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    reports_to_id: Optional[UUID] = None
    
    # Contact information
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, max_length=20)
    mobile: Optional[str] = Field(None, max_length=20)
    fax: Optional[str] = Field(None, max_length=20)
    
    # Address (if different from business entity)
    address_street: Optional[str] = Field(None, max_length=255)
    address_number: Optional[str] = Field(None, max_length=10)
    address_city: Optional[str] = Field(None, max_length=100)
    address_postal_code: Optional[str] = Field(None, min_length=5, max_length=5)
    address_region: Optional[str] = Field(None, max_length=100)
    
    # Contact status and preferences
    is_primary_contact: bool = False
    is_decision_maker: bool = False
    preferred_contact_method: str = "email"
    language: str = "el"
    
    # Marketing preferences
    marketing_consent: bool = False
    newsletter_subscription: bool = False
    email_opt_in: bool = True
    sms_opt_in: bool = False
    
    # Social media
    linkedin_url: Optional[str] = Field(None, max_length=255)
    twitter_handle: Optional[str] = Field(None, max_length=100)
    
    # CRM information
    lead_source: Optional[str] = Field(None, max_length=100)
    assigned_user_id: Optional[UUID] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = []
    
    # Personal dates
    birth_date: Optional[datetime] = None
    anniversary_date: Optional[datetime] = None
    
    @validator('amka')
    def validate_amka_format(cls, v):
        if v and not v.isdigit():
            raise ValueError('AMKA must contain only digits')
        return v

class ContactUpdateRequest(BaseModel):
    """Request model for updating contact"""
    contact_type: Optional[ContactType] = None
    
    # Personal information
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=255)
    
    # Greek personal information
    father_name: Optional[str] = Field(None, max_length=100)
    mother_name: Optional[str] = Field(None, max_length=100)
    amka: Optional[str] = Field(None, min_length=11, max_length=11)
    id_card_number: Optional[str] = Field(None, max_length=20)
    
    # Professional information
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    reports_to_id: Optional[UUID] = None
    
    # Contact information
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, max_length=20)
    mobile: Optional[str] = Field(None, max_length=20)
    fax: Optional[str] = Field(None, max_length=20)
    
    # Address
    address_street: Optional[str] = Field(None, max_length=255)
    address_number: Optional[str] = Field(None, max_length=10)
    address_city: Optional[str] = Field(None, max_length=100)
    address_postal_code: Optional[str] = Field(None, min_length=5, max_length=5)
    address_region: Optional[str] = Field(None, max_length=100)
    
    # Contact status and preferences
    status: Optional[ContactStatus] = None
    is_primary_contact: Optional[bool] = None
    is_decision_maker: Optional[bool] = None
    preferred_contact_method: Optional[str] = None
    language: Optional[str] = None
    
    # Marketing preferences
    marketing_consent: Optional[bool] = None
    newsletter_subscription: Optional[bool] = None
    email_opt_in: Optional[bool] = None
    sms_opt_in: Optional[bool] = None
    
    # Social media
    linkedin_url: Optional[str] = Field(None, max_length=255)
    twitter_handle: Optional[str] = Field(None, max_length=100)
    
    # CRM information
    lead_source: Optional[str] = Field(None, max_length=100)
    assigned_user_id: Optional[UUID] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # Personal dates
    birth_date: Optional[datetime] = None
    anniversary_date: Optional[datetime] = None

class ContactResponse(BaseModel):
    """Response model for contact"""
    id: UUID
    company_id: UUID
    business_entity_id: UUID
    contact_code: Optional[str]
    contact_type: ContactType
    status: ContactStatus
    
    # Personal information
    first_name: str
    last_name: str
    middle_name: Optional[str]
    display_name: Optional[str]
    full_name: str
    
    # Greek personal information
    father_name: Optional[str]
    mother_name: Optional[str]
    amka: Optional[str]
    id_card_number: Optional[str]
    
    # Professional information
    job_title: Optional[str]
    department: Optional[str]
    reports_to_id: Optional[UUID]
    
    # Contact information
    email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    fax: Optional[str]
    
    # Address
    address_street: Optional[str]
    address_number: Optional[str]
    address_city: Optional[str]
    address_postal_code: Optional[str]
    address_region: Optional[str]
    full_address: str
    
    # Contact status and preferences
    is_primary_contact: bool
    is_decision_maker: bool
    preferred_contact_method: str
    language: str
    
    # Marketing preferences
    marketing_consent: bool
    newsletter_subscription: bool
    email_opt_in: bool
    sms_opt_in: bool
    
    # Social media
    linkedin_url: Optional[str]
    twitter_handle: Optional[str]
    
    # CRM information
    lead_source: Optional[str]
    assigned_user_id: Optional[UUID]
    notes: Optional[str]
    tags: Optional[List[str]]
    
    # Interaction tracking
    last_contact_date: Optional[datetime]
    total_interactions: int
    
    # Personal dates
    birth_date: Optional[datetime]
    anniversary_date: Optional[datetime]
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContactListResponse(BaseModel):
    """Response model for contact list"""
    contacts: List[ContactResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class ContactSummaryResponse(BaseModel):
    """Simplified contact response for lists"""
    id: UUID
    full_name: str
    job_title: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    contact_type: ContactType
    is_primary_contact: bool
    is_decision_maker: bool
    status: ContactStatus

# Helper functions
def get_current_user(user_company = Depends(get_current_user_and_company)) -> User:
    """Get current authenticated user"""
    user, company_id = user_company
    return user

# API Endpoints

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: ContactCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new contact"""
    
    try:
        # Verify business entity exists and user has access
        business_entity = db.query(BusinessEntity).filter(
            BusinessEntity.id == contact_data.business_entity_id,
            BusinessEntity.company_id == current_user.company_id
        ).first()
        
        if not business_entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business entity not found"
            )
        
        # Generate contact code
        last_contact = db.query(Contact).filter(
            Contact.company_id == current_user.company_id
        ).order_by(Contact.created_at.desc()).first()
        
        if last_contact and last_contact.contact_code:
            try:
                last_number = int(last_contact.contact_code.split('-')[-1])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        contact_code = f"CNT-{new_number:06d}"
        
        # Prepare contact data
        contact_dict = contact_data.dict(exclude_unset=True)
        contact_dict["company_id"] = str(current_user.company_id)
        contact_dict["contact_code"] = contact_code
        contact_dict["created_by"] = str(current_user.id)
        
        # Set display name if not provided
        if not contact_dict.get("display_name"):
            contact_dict["display_name"] = f"{contact_dict['first_name']} {contact_dict['last_name']}"
        
        # If this is set as primary contact, unset other primary contacts
        if contact_dict.get("is_primary_contact"):
            db.query(Contact).filter(
                Contact.business_entity_id == contact_data.business_entity_id,
                Contact.is_primary_contact == True
            ).update({"is_primary_contact": False})
        
        # Create contact
        contact = Contact(**contact_dict)
        db.add(contact)
        db.commit()
        db.refresh(contact)
        
        return ContactResponse.from_orm(contact)
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create contact: {str(e)}"
        )

@router.get("/", response_model=ContactListResponse)
async def list_contacts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name, email, or phone"),
    business_entity_id: Optional[UUID] = Query(None, description="Filter by business entity"),
    contact_type: Optional[ContactType] = Query(None, description="Filter by contact type"),
    status: Optional[ContactStatus] = Query(None, description="Filter by status"),
    is_primary_only: bool = Query(False, description="Show only primary contacts"),
    is_decision_maker_only: bool = Query(False, description="Show only decision makers"),
    sort_by: str = Query("full_name", description="Field to sort by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List contacts with filtering and pagination"""
    
    query = db.query(Contact).filter(Contact.company_id == current_user.company_id)
    
    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Contact.display_name.ilike(search_term) |
            Contact.email.ilike(search_term) |
            Contact.phone.ilike(search_term) |
            Contact.mobile.ilike(search_term) |
            (Contact.first_name + ' ' + Contact.last_name).ilike(search_term)
        )
    
    if business_entity_id:
        query = query.filter(Contact.business_entity_id == business_entity_id)
    
    if contact_type:
        query = query.filter(Contact.contact_type == contact_type)
    
    if status:
        query = query.filter(Contact.status == status)
    
    if is_primary_only:
        query = query.filter(Contact.is_primary_contact == True)
    
    if is_decision_maker_only:
        query = query.filter(Contact.is_decision_maker == True)
    
    # Get total count
    total_count = query.count()
    
    # Apply sorting
    if hasattr(Contact, sort_by):
        sort_column = getattr(Contact, sort_by)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(Contact.display_name.asc())
    
    # Apply pagination
    contacts = query.offset(skip).limit(limit).all()
    
    page = (skip // limit) + 1
    total_pages = (total_count + limit - 1) // limit
    
    return ContactListResponse(
        contacts=[ContactResponse.from_orm(contact) for contact in contacts],
        total_count=total_count,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: UUID = Path(..., description="Contact ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contact by ID"""
    
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.company_id == current_user.company_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    return ContactResponse.from_orm(contact)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: UUID = Path(..., description="Contact ID"),
    contact_data: ContactUpdateRequest = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update contact"""
    
    try:
        # Get existing contact
        contact = db.query(Contact).filter(
            Contact.id == contact_id,
            Contact.company_id == current_user.company_id
        ).first()
        
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        
        # Prepare update data
        update_dict = contact_data.dict(exclude_unset=True)
        
        # If setting as primary contact, unset other primary contacts
        if update_dict.get("is_primary_contact"):
            db.query(Contact).filter(
                Contact.business_entity_id == contact.business_entity_id,
                Contact.id != contact_id,
                Contact.is_primary_contact == True
            ).update({"is_primary_contact": False})
        
        # Update contact
        for key, value in update_dict.items():
            if hasattr(contact, key):
                setattr(contact, key, value)
        
        contact.updated_at = datetime.utcnow()
        contact.updated_by = current_user.id
        
        db.commit()
        db.refresh(contact)
        
        return ContactResponse.from_orm(contact)
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update contact: {str(e)}"
        )

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: UUID = Path(..., description="Contact ID"),
    soft_delete: bool = Query(True, description="Perform soft delete (deactivate) instead of hard delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete contact"""
    
    try:
        contact = db.query(Contact).filter(
            Contact.id == contact_id,
            Contact.company_id == current_user.company_id
        ).first()
        
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        
        if soft_delete:
            # Soft delete - deactivate contact
            contact.status = ContactStatus.INACTIVE
            contact.updated_at = datetime.utcnow()
            contact.updated_by = current_user.id
        else:
            # Hard delete - remove from database
            db.delete(contact)
        
        db.commit()
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete contact: {str(e)}"
        )

# Business entity specific endpoints

@router.get("/business-entity/{business_entity_id}", response_model=List[ContactSummaryResponse])
async def get_contacts_for_business_entity(
    business_entity_id: UUID = Path(..., description="Business entity ID"),
    include_inactive: bool = Query(False, description="Include inactive contacts"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all contacts for a specific business entity"""
    
    # Verify business entity access
    business_entity = db.query(BusinessEntity).filter(
        BusinessEntity.id == business_entity_id,
        BusinessEntity.company_id == current_user.company_id
    ).first()
    
    if not business_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business entity not found"
        )
    
    query = db.query(Contact).filter(Contact.business_entity_id == business_entity_id)
    
    if not include_inactive:
        query = query.filter(Contact.status == ContactStatus.ACTIVE)
    
    contacts = query.order_by(
        Contact.is_primary_contact.desc(),
        Contact.display_name.asc()
    ).all()
    
    return [ContactSummaryResponse.from_orm(contact) for contact in contacts]

@router.put("/{contact_id}/set-primary")
async def set_primary_contact(
    contact_id: UUID = Path(..., description="Contact ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Set contact as primary contact for their business entity"""
    
    try:
        contact = db.query(Contact).filter(
            Contact.id == contact_id,
            Contact.company_id == current_user.company_id
        ).first()
        
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        
        # Unset other primary contacts for the same business entity
        db.query(Contact).filter(
            Contact.business_entity_id == contact.business_entity_id,
            Contact.id != contact_id,
            Contact.is_primary_contact == True
        ).update({"is_primary_contact": False})
        
        # Set this contact as primary
        contact.is_primary_contact = True
        contact.updated_at = datetime.utcnow()
        contact.updated_by = current_user.id
        
        db.commit()
        
        return {"message": "Contact set as primary successfully"}
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set primary contact: {str(e)}"
        )

# Statistics endpoints

@router.get("/stats/summary")
async def get_contact_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contact statistics summary"""
    
    total_contacts = db.query(Contact).filter(
        Contact.company_id == current_user.company_id
    ).count()
    
    active_contacts = db.query(Contact).filter(
        Contact.company_id == current_user.company_id,
        Contact.status == ContactStatus.ACTIVE
    ).count()
    
    primary_contacts = db.query(Contact).filter(
        Contact.company_id == current_user.company_id,
        Contact.is_primary_contact == True
    ).count()
    
    decision_makers = db.query(Contact).filter(
        Contact.company_id == current_user.company_id,
        Contact.is_decision_maker == True
    ).count()
    
    return {
        "total_contacts": total_contacts,
        "active_contacts": active_contacts,
        "primary_contacts": primary_contacts,
        "decision_makers": decision_makers,
        "last_updated": datetime.utcnow().isoformat()
    } 