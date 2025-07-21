"""
Business Entity API endpoints for Greek ERP/CRM System
Complete CRUD operations for business entities (customers, suppliers, partners)
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...core.database import get_db
from ...services.business_entity_service import BusinessEntityService
from ...models.business_entity import (
    BusinessEntity, BusinessEntityType, BusinessEntityStatus, 
    BusinessEntityRole, PaymentTerms
)
from ...models.user import User
from ...middleware.company_isolation import get_current_user_and_company

router = APIRouter(prefix="/business-entities", tags=["Business Entities"])

# Pydantic models for request/response

class BusinessEntityCreateRequest(BaseModel):
    """Request model for creating business entity"""
    entity_type: BusinessEntityType = BusinessEntityType.BUSINESS
    business_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: str = Field(..., min_length=1, max_length=255)
    
    # Greek business fields
    afm: Optional[str] = Field(None, min_length=9, max_length=9)
    doy: Optional[str] = Field(None, min_length=4, max_length=10)
    business_activity: Optional[str] = None
    legal_form: Optional[str] = None
    vat_number: Optional[str] = None
    vat_exempt: bool = False
    
    # Contact information
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    
    # Address
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_city: Optional[str] = None
    address_postal_code: Optional[str] = Field(None, min_length=5, max_length=5)
    address_region: Optional[str] = None
    
    # Billing address (if different)
    billing_address_street: Optional[str] = None
    billing_address_number: Optional[str] = None
    billing_address_city: Optional[str] = None
    billing_address_postal_code: Optional[str] = Field(None, min_length=5, max_length=5)
    billing_address_region: Optional[str] = None
    
    # Business settings
    entity_category: Optional[str] = None
    entity_segment: Optional[str] = None
    credit_limit: Optional[float] = Field(None, ge=0)
    payment_terms: Optional[PaymentTerms] = PaymentTerms.NET_30
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    
    # Supplier settings
    supplier_rating: Optional[int] = Field(None, ge=1, le=5)
    supplier_category: Optional[str] = None
    lead_time_days: Optional[int] = Field(None, ge=0)
    minimum_order_amount: Optional[float] = Field(None, ge=0)
    
    # CRM fields
    lead_source: Optional[str] = None
    assigned_user_id: Optional[UUID] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = []
    
    # Roles to assign
    roles: Optional[List[BusinessEntityRole]] = []
    
    # Preferences
    language: str = "el"
    preferred_contact_method: str = "email"
    marketing_consent: bool = False
    newsletter_subscription: bool = False
    
    @validator('afm')
    def validate_afm_format(cls, v):
        if v and not v.isdigit():
            raise ValueError('AFM must contain only digits')
        return v

class BusinessEntityUpdateRequest(BaseModel):
    """Request model for updating business entity"""
    business_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    
    # Greek business fields
    afm: Optional[str] = Field(None, min_length=9, max_length=9)
    doy: Optional[str] = Field(None, min_length=4, max_length=10)
    business_activity: Optional[str] = None
    legal_form: Optional[str] = None
    vat_number: Optional[str] = None
    vat_exempt: Optional[bool] = None
    
    # Contact information
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    
    # Address
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_city: Optional[str] = None
    address_postal_code: Optional[str] = Field(None, min_length=5, max_length=5)
    address_region: Optional[str] = None
    
    # Billing address
    billing_address_street: Optional[str] = None
    billing_address_number: Optional[str] = None
    billing_address_city: Optional[str] = None
    billing_address_postal_code: Optional[str] = Field(None, min_length=5, max_length=5)
    billing_address_region: Optional[str] = None
    
    # Business settings
    status: Optional[BusinessEntityStatus] = None
    entity_category: Optional[str] = None
    entity_segment: Optional[str] = None
    credit_limit: Optional[float] = Field(None, ge=0)
    payment_terms: Optional[PaymentTerms] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    
    # Supplier settings
    supplier_rating: Optional[int] = Field(None, ge=1, le=5)
    supplier_category: Optional[str] = None
    lead_time_days: Optional[int] = Field(None, ge=0)
    minimum_order_amount: Optional[float] = Field(None, ge=0)
    
    # CRM fields
    lead_source: Optional[str] = None
    assigned_user_id: Optional[UUID] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # Roles to assign (replaces existing roles)
    roles: Optional[List[BusinessEntityRole]] = None
    
    # Preferences
    language: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    marketing_consent: Optional[bool] = None
    newsletter_subscription: Optional[bool] = None

class BusinessEntityResponse(BaseModel):
    """Response model for business entity"""
    id: UUID
    company_id: UUID
    entity_code: str
    entity_type: BusinessEntityType
    status: BusinessEntityStatus
    
    # Basic info
    business_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: str
    full_name: str
    
    # Greek business fields
    afm: Optional[str]
    doy: Optional[str]
    business_activity: Optional[str]
    legal_form: Optional[str]
    vat_number: Optional[str]
    vat_exempt: bool
    
    # Contact info
    email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    website: Optional[str]
    
    # Address
    address_street: Optional[str]
    address_number: Optional[str]
    address_city: Optional[str]
    address_postal_code: Optional[str]
    address_region: Optional[str]
    primary_address: str
    
    # Business metrics
    total_sales: float
    total_purchases: float
    total_orders: int
    total_purchase_orders: int
    
    # Validation status
    has_valid_afm: bool
    has_valid_vat: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BusinessEntityListResponse(BaseModel):
    """Response model for business entity list"""
    entities: List[BusinessEntityResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class RoleAssignmentRequest(BaseModel):
    """Request model for role assignment"""
    role: BusinessEntityRole
    notes: Optional[str] = None

class ValidationResponse(BaseModel):
    """Response model for validation results"""
    is_valid: bool
    error: Optional[str] = None
    normalized_value: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

# Helper functions
def get_business_entity_service(db: Session = Depends(get_db)) -> BusinessEntityService:
    """Get business entity service instance"""
    return BusinessEntityService(db)

def get_current_user(user_company = Depends(get_current_user_and_company)) -> User:
    """Get current authenticated user"""
    user, company_id = user_company
    return user

# API Endpoints

@router.post("/test", status_code=status.HTTP_200_OK)
async def test_business_entity_endpoint():
    """Test endpoint to verify routing works"""
    return {"message": "Business entity endpoint is working", "timestamp": datetime.now()}

@router.post("", response_model=BusinessEntityResponse, status_code=status.HTTP_201_CREATED)
async def create_business_entity(
    entity_data: BusinessEntityCreateRequest,
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new business entity"""
    import time
    
    start_time = time.time()
    
    print(f"[ENDPOINT] POST /business-entities/ started at {time.time()}")
    print(f"[ENDPOINT] POST /business-entities endpoint reached with data: {entity_data}")
    print(f"[ENDPOINT] Current user: {current_user.username if current_user else 'None'}")
    
    print(f"[ENDPOINT] Converting entity data at {time.time()}")
    
    entity_dict = entity_data.dict(exclude_unset=True)
    
    # Convert roles to strings for the service
    if "roles" in entity_dict:
        entity_dict["roles"] = [role.value for role in entity_dict["roles"]]
    
    print(f"[ENDPOINT] About to call service.create_business_entity at {time.time()}")
    
    entity = await service.create_business_entity(
        entity_data=entity_dict,
        requesting_user=current_user,
        validate_greek_fields=True
    )
    
    print(f"[ENDPOINT] Service call completed at {time.time()}")
    
    result = BusinessEntityResponse.from_orm(entity)
    
    duration = (time.time() - start_time) * 1000
    print(f"[ENDPOINT] POST /business-entities/ completed ({duration:.2f}ms) at {time.time()}")
    
    return result

# Helper function to avoid code duplication
async def _list_business_entities_impl(
    skip: int,
    limit: int,
    search: Optional[str],
    entity_type: Optional[BusinessEntityType],
    status: Optional[BusinessEntityStatus],
    role_filter: Optional[BusinessEntityRole],
    sort_by: str,
    sort_order: str,
    service: BusinessEntityService,
    current_user: User
):
    """Implementation for listing business entities"""
    entities, total_count = await service.list_business_entities(
        requesting_user=current_user,
        skip=skip,
        limit=limit,
        search=search,
        entity_type=entity_type,
        status=status,
        role_filter=role_filter,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    page = (skip // limit) + 1
    total_pages = (total_count + limit - 1) // limit
    
    return BusinessEntityListResponse(
        entities=[BusinessEntityResponse.from_orm(entity) for entity in entities],
        total_count=total_count,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )

@router.get("/", response_model=BusinessEntityListResponse)
async def list_business_entities_with_slash(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name, email, AFM, or entity code"),
    entity_type: Optional[BusinessEntityType] = Query(None, description="Filter by entity type"),
    status: Optional[BusinessEntityStatus] = Query(None, description="Filter by status"),
    role_filter: Optional[BusinessEntityRole] = Query(None, description="Filter by role"),
    sort_by: str = Query("display_name", description="Field to sort by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order"),
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """List business entities with filtering and pagination (with trailing slash)"""
    return await _list_business_entities_impl(
        skip, limit, search, entity_type, status, role_filter, 
        sort_by, sort_order, service, current_user
    )

@router.get("", response_model=BusinessEntityListResponse)
async def list_business_entities_without_slash(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name, email, AFM, or entity code"),
    entity_type: Optional[BusinessEntityType] = Query(None, description="Filter by entity type"),
    status: Optional[BusinessEntityStatus] = Query(None, description="Filter by status"),
    role_filter: Optional[BusinessEntityRole] = Query(None, description="Filter by role"),
    sort_by: str = Query("display_name", description="Field to sort by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order"),
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """List business entities with filtering and pagination (without trailing slash)"""
    return await _list_business_entities_impl(
        skip, limit, search, entity_type, status, role_filter, 
        sort_by, sort_order, service, current_user
    )

@router.get("/{entity_id}", response_model=BusinessEntityResponse)
async def get_business_entity(
    entity_id: UUID = Path(..., description="Business entity ID"),
    include_contacts: bool = Query(False, description="Include associated contacts"),
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Get business entity by ID"""
    
    entity = await service.get_business_entity(
        entity_id=entity_id,
        requesting_user=current_user,
        include_contacts=include_contacts
    )
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business entity not found"
        )
    
    return BusinessEntityResponse.from_orm(entity)

@router.put("/{entity_id}", response_model=BusinessEntityResponse)
async def update_business_entity(
    entity_id: UUID = Path(..., description="Business entity ID"),
    entity_data: BusinessEntityUpdateRequest = ...,
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Update business entity"""
    
    update_dict = entity_data.dict(exclude_unset=True)
    
    # Convert roles to strings for the service
    if "roles" in update_dict:
        update_dict["roles"] = [role.value for role in update_dict["roles"]]
    
    entity = await service.update_business_entity(
        entity_id=entity_id,
        update_data=update_dict,
        requesting_user=current_user,
        validate_greek_fields=True
    )
    
    return BusinessEntityResponse.from_orm(entity)

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business_entity(
    entity_id: UUID = Path(..., description="Business entity ID"),
    soft_delete: bool = Query(True, description="Perform soft delete (deactivate) instead of hard delete"),
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Delete business entity"""
    
    success = await service.delete_business_entity(
        entity_id=entity_id,
        requesting_user=current_user,
        soft_delete=soft_delete
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete business entity"
        )

# Role management endpoints

@router.post("/{entity_id}/roles", status_code=status.HTTP_201_CREATED)
async def assign_role(
    entity_id: UUID = Path(..., description="Business entity ID"),
    role_data: RoleAssignmentRequest = ...,
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Assign a role to business entity"""
    
    success = await service.assign_role(
        entity_id=entity_id,
        role=role_data.role,
        requesting_user=current_user,
        notes=role_data.notes
    )
    
    return {"message": f"Role {role_data.role.value} assigned successfully"}

@router.delete("/{entity_id}/roles/{role}")
async def remove_role(
    entity_id: UUID = Path(..., description="Business entity ID"),
    role: BusinessEntityRole = Path(..., description="Role to remove"),
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Remove a role from business entity"""
    
    success = await service.remove_role(
        entity_id=entity_id,
        role=role,
        requesting_user=current_user
    )
    
    return {"message": f"Role {role.value} removed successfully"}

@router.get("/{entity_id}/roles")
async def get_entity_roles(
    entity_id: UUID = Path(..., description="Business entity ID"),
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Get all roles for business entity"""
    
    roles = await service.get_entity_roles(
        entity_id=entity_id,
        requesting_user=current_user
    )
    
    return {"roles": roles}

# Greek validation endpoints

@router.post("/validate/afm", response_model=ValidationResponse)
async def validate_afm(
    afm: str = Query(..., description="AFM to validate"),
    service: BusinessEntityService = Depends(get_business_entity_service)
):
    """Validate Greek AFM (Tax Identification Number)"""
    
    result = service.validate_afm(afm)
    
    return ValidationResponse(
        is_valid=result["is_valid"],
        error=result.get("error"),
        normalized_value=result.get("normalized_afm"),
        additional_info={"afm": result["afm"]}
    )

@router.post("/validate/doy", response_model=ValidationResponse)
async def validate_doy(
    doy: str = Query(..., description="DOY to validate"),
    service: BusinessEntityService = Depends(get_business_entity_service)
):
    """Validate Greek DOY (Tax Office) code"""
    
    result = service.validate_doy(doy)
    
    return ValidationResponse(
        is_valid=result["is_valid"],
        error=result.get("error"),
        additional_info={
            "doy": result["doy"],
            "doy_name": result.get("doy_name")
        }
    )

@router.get("/doy-list")
async def get_doy_list(
    service: BusinessEntityService = Depends(get_business_entity_service)
):
    """Get list of all Greek DOY offices"""
    
    doy_list = service.get_doy_list()
    return {"doy_offices": doy_list}

@router.get("/doy-search")
async def search_doy(
    query: str = Query(..., description="Search query for DOY office"),
    service: BusinessEntityService = Depends(get_business_entity_service)
):
    """Search Greek DOY offices"""
    
    results = service.search_doy(query)
    return {"results": results}

# Statistics endpoints

class CustomerStatsResponse(BaseModel):
    """Response model for customer statistics"""
    total_customers: int
    active_customers: int
    total_sales: float
    average_order_value: float
    last_updated: str

class SupplierStatsResponse(BaseModel):
    """Response model for supplier statistics"""
    total_suppliers: int
    active_suppliers: int
    total_purchases: float
    average_rating: float
    last_updated: str

@router.get("/stats/summary")
async def get_business_entity_stats(
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user)
):
    """Get business entity statistics summary"""
    
    # Get basic counts
    entities, total_count = await service.list_business_entities(
        requesting_user=current_user,
        skip=0,
        limit=1  # We only need the count
    )
    
    # Get counts by type
    customers, customer_count = await service.list_business_entities(
        requesting_user=current_user,
        role_filter=BusinessEntityRole.CUSTOMER,
        skip=0,
        limit=1
    )
    
    suppliers, supplier_count = await service.list_business_entities(
        requesting_user=current_user,
        role_filter=BusinessEntityRole.SUPPLIER,
        skip=0,
        limit=1
    )
    
    return {
        "total_entities": total_count,
        "customers": customer_count,
        "suppliers": supplier_count,
        "active_entities": total_count,  # Could be refined with status filter
        "last_updated": datetime.utcnow().isoformat()
    }

@router.get("/stats/customers", response_model=CustomerStatsResponse)
async def get_customer_stats(
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get customer statistics with real data"""
    from sqlalchemy import func, and_
    from ...models.business_entity import business_entity_roles
    
    try:
        # Get total customers
        customers_query = db.query(BusinessEntity).join(
            business_entity_roles,
            BusinessEntity.id == business_entity_roles.c.business_entity_id
        ).filter(
            and_(
                BusinessEntity.company_id == current_user.company_id,
                business_entity_roles.c.role == BusinessEntityRole.CUSTOMER,
                business_entity_roles.c.is_active == True
            )
        )
        
        total_customers = customers_query.count()
        
        # Get active customers
        active_customers = customers_query.filter(
            BusinessEntity.status == BusinessEntityStatus.ACTIVE
        ).count()
        
        # Get total sales and calculate average order value
        sales_data = customers_query.with_entities(
            func.sum(BusinessEntity.total_sales).label('total_sales'),
            func.sum(BusinessEntity.total_orders).label('total_orders')
        ).first()
        
        total_sales = float(sales_data.total_sales or 0)
        total_orders = int(sales_data.total_orders or 0)
        average_order_value = total_sales / total_orders if total_orders > 0 else 0
        
        return CustomerStatsResponse(
            total_customers=total_customers,
            active_customers=active_customers,
            total_sales=total_sales,
            average_order_value=average_order_value,
            last_updated=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        # Fallback to basic counts if complex query fails
        customers, customer_count = await service.list_business_entities(
            requesting_user=current_user,
            role_filter=BusinessEntityRole.CUSTOMER,
            skip=0,
            limit=1
        )
        
        active_customers, active_count = await service.list_business_entities(
            requesting_user=current_user,
            role_filter=BusinessEntityRole.CUSTOMER,
            status=BusinessEntityStatus.ACTIVE,
            skip=0,
            limit=1
        )
        
        return CustomerStatsResponse(
            total_customers=customer_count,
            active_customers=active_count,
            total_sales=0.0,
            average_order_value=0.0,
            last_updated=datetime.utcnow().isoformat()
        )

@router.get("/stats/suppliers", response_model=SupplierStatsResponse)
async def get_supplier_stats(
    service: BusinessEntityService = Depends(get_business_entity_service),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get supplier statistics with real data"""
    from sqlalchemy import func, and_
    from ...models.business_entity import business_entity_roles
    
    try:
        # Get total suppliers
        suppliers_query = db.query(BusinessEntity).join(
            business_entity_roles,
            BusinessEntity.id == business_entity_roles.c.business_entity_id
        ).filter(
            and_(
                BusinessEntity.company_id == current_user.company_id,
                business_entity_roles.c.role == BusinessEntityRole.SUPPLIER,
                business_entity_roles.c.is_active == True
            )
        )
        
        total_suppliers = suppliers_query.count()
        
        # Get active suppliers
        active_suppliers = suppliers_query.filter(
            BusinessEntity.status == BusinessEntityStatus.ACTIVE
        ).count()
        
        # Get total purchases
        purchases_data = suppliers_query.with_entities(
            func.sum(BusinessEntity.total_purchases).label('total_purchases')
        ).first()
        
        total_purchases = float(purchases_data.total_purchases or 0)
        
        # Calculate average rating from actual data 
        # Since we don't have a rating system yet, calculate based on performance metrics
        # For now, return 0.0 to indicate no ratings available
        average_rating = 0.0
        
        return SupplierStatsResponse(
            total_suppliers=total_suppliers,
            active_suppliers=active_suppliers,
            total_purchases=total_purchases,
            average_rating=average_rating,
            last_updated=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        # Fallback to basic counts if complex query fails
        suppliers, supplier_count = await service.list_business_entities(
            requesting_user=current_user,
            role_filter=BusinessEntityRole.SUPPLIER,
            skip=0,
            limit=1
        )
        
        active_suppliers, active_count = await service.list_business_entities(
            requesting_user=current_user,
            role_filter=BusinessEntityRole.SUPPLIER,
            status=BusinessEntityStatus.ACTIVE,
            skip=0,
            limit=1
        )
        
        return SupplierStatsResponse(
            total_suppliers=supplier_count,
            active_suppliers=active_count,
            total_purchases=0.0,
            average_rating=0.0,
            last_updated=datetime.utcnow().isoformat()
        ) 