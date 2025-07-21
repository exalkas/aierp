"""
Dynamic Entities API Endpoints
Provides REST API for creating and managing dynamic entities, fields, and layouts
Includes Greek compliance and validation features
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from pydantic import BaseModel, Field, validator
import uuid
import json

from ...core.database import get_db
from ...middleware.company_isolation import get_current_company
from ...middleware.greek_compliance import validate_greek_compliance
from ...models.dynamic_entity import DynamicEntity as DynamicEntityModel
from ...models.dynamic_field import DynamicField as DynamicFieldModel
from ...models.entity_layout import EntityLayout as EntityLayoutModel
from ...services.entity_validation_service import EntityValidationService
from ...services.greek_reference_service import GreekReferenceService
from ...utils.greek_validation import validate_afm, validate_amka, validate_greek_phone

# Initialize router
router = APIRouter(prefix="/dynamic-entities", tags=["Dynamic Entities"])

# ============================================================================
# PYDANTIC MODELS (REQUEST/RESPONSE SCHEMAS)
# ============================================================================

class FieldOptionCreate(BaseModel):
    value: str
    label: str
    label_greek: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    is_default: bool = False
    is_active: bool = True

class FieldValidationRule(BaseModel):
    type: str = Field(..., description="Validation rule type")
    value: Optional[Any] = None
    message: Optional[str] = None
    message_greek: Optional[str] = None

class FieldValidation(BaseModel):
    rules: List[FieldValidationRule] = []
    custom_validation: Optional[str] = None
    error_message: Optional[str] = None
    error_message_greek: Optional[str] = None

class GreekFieldValidation(BaseModel):
    afm_validation: Optional[Dict[str, Any]] = None
    amka_validation: Optional[Dict[str, Any]] = None
    iban_validation: Optional[Dict[str, Any]] = None
    phone_format: Optional[str] = None
    address_validation: Optional[Dict[str, Any]] = None

class FieldPermissions(BaseModel):
    create: List[str] = ["admin", "manager"]
    read: List[str] = ["admin", "manager", "user"]
    update: List[str] = ["admin", "manager"]
    delete: List[str] = ["admin"]

class DynamicFieldCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=200)
    label_greek: Optional[str] = Field(None, max_length=200)
    type: str = Field(..., description="Field type")
    description: Optional[str] = None
    description_greek: Optional[str] = None
    help_text: Optional[str] = None
    help_text_greek: Optional[str] = None
    
    # Field Configuration
    required: bool = False
    unique: bool = False
    indexed: bool = False
    searchable: bool = True
    sortable: bool = True
    filterable: bool = True
    exportable: bool = True
    
    # Data Properties
    default_value: Optional[Any] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    options: Optional[List[FieldOptionCreate]] = None
    
    # Validation
    validation: Optional[FieldValidation] = None
    greek_validation: Optional[GreekFieldValidation] = None
    
    # Display Properties
    display_order: int = 1
    grid_column: bool = True
    grid_width: Optional[int] = None
    detail_section: str = "general"
    is_inline_editable: bool = False
    show_in_list: bool = True
    show_in_detail: bool = True
    show_in_search: bool = True
    
    # Permissions
    permissions: Optional[FieldPermissions] = None

    @validator('name')
    def validate_name(cls, v):
        if not v.islower():
            raise ValueError('Field name must be lowercase')
        if not v.replace('_', '').isalnum():
            raise ValueError('Field name must contain only letters, numbers, and underscores')
        if v.startswith('_') or v.endswith('_'):
            raise ValueError('Field name cannot start or end with underscore')
        return v

    @validator('type')
    def validate_type(cls, v):
        valid_types = [
            # Basic Types
            'text', 'textarea', 'email', 'phone', 'url', 'number', 'decimal', 
            'currency', 'percentage', 'date', 'datetime', 'time', 'boolean', 'checkbox',
            # Selection Types
            'dropdown', 'multiselect', 'radio', 'tags', 'lookup', 'multilookup',
            # Rich Content
            'richtext', 'markdown', 'code', 'file', 'image', 'document',
            # Greek-Specific Types
            'greek_afm', 'greek_amka', 'greek_iban', 'greek_phone', 'greek_postal_code',
            'greek_doy_selector', 'greek_municipality', 'greek_address',
            # Advanced Types
            'json', 'array', 'composite', 'calculated', 'formula', 'aggregation',
            'signature', 'location', 'barcode', 'rating', 'progress', 'status_indicator'
        ]
        if v not in valid_types:
            raise ValueError(f'Invalid field type: {v}')
        return v

class DynamicFieldUpdate(BaseModel):
    label: Optional[str] = None
    label_greek: Optional[str] = None
    description: Optional[str] = None
    description_greek: Optional[str] = None
    help_text: Optional[str] = None
    help_text_greek: Optional[str] = None
    required: Optional[bool] = None
    unique: Optional[bool] = None
    indexed: Optional[bool] = None
    searchable: Optional[bool] = None
    default_value: Optional[Any] = None
    options: Optional[List[FieldOptionCreate]] = None
    validation: Optional[FieldValidation] = None
    permissions: Optional[FieldPermissions] = None
    is_active: Optional[bool] = None

class DynamicFieldResponse(BaseModel):
    id: str
    entity_id: str
    name: str
    label: str
    label_greek: Optional[str]
    type: str
    description: Optional[str]
    description_greek: Optional[str]
    help_text: Optional[str]
    help_text_greek: Optional[str]
    required: bool
    unique: bool
    indexed: bool
    searchable: bool
    sortable: bool
    filterable: bool
    exportable: bool
    default_value: Optional[Any]
    options: Optional[List[Dict[str, Any]]]
    validation: Optional[Dict[str, Any]]
    greek_validation: Optional[Dict[str, Any]]
    display_order: int
    grid_column: bool
    detail_section: str
    show_in_list: bool
    show_in_detail: bool
    show_in_search: bool
    permissions: Dict[str, List[str]]
    version: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    is_active: bool

    class Config:
        from_attributes = True

class GreekComplianceConfig(BaseModel):
    aade_reporting: bool = False
    tax_relevant: bool = False
    personal_data: bool = False
    professional_certification: Optional[str] = None
    required_documents: List[str] = []
    compliance_level: str = "basic"
    audit_trail: bool = True
    digital_signature: bool = False

class EntityPermissions(BaseModel):
    create: List[str] = ["admin", "manager"]
    read: List[str] = ["admin", "manager", "user"]
    update: List[str] = ["admin", "manager"]
    delete: List[str] = ["admin"]
    export: List[str] = ["admin", "manager"]
    import_data: List[str] = ["admin"]
    customize_fields: List[str] = ["admin"]
    customize_layouts: List[str] = ["admin"]
    create_workflows: List[str] = ["admin"]

class DynamicEntityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    plural_name: str = Field(..., min_length=1, max_length=100)
    label_singular: str = Field(..., min_length=1, max_length=200)
    label_plural: str = Field(..., min_length=1, max_length=200)
    label_singular_greek: Optional[str] = Field(None, max_length=200)
    label_plural_greek: Optional[str] = Field(None, max_length=200)
    icon: str = "building2"
    color: str = "#3B82F6"
    description: Optional[str] = None
    description_greek: Optional[str] = None
    
    # Module Configuration
    module: str = "custom"
    category: str = "custom"
    customization_level: str = "custom"
    
    # Greek Compliance
    greek_compliance: Optional[GreekComplianceConfig] = None
    aade_integration: bool = False
    tax_relevant: bool = False
    gdpr_relevant: bool = False
    
    # Permissions
    permissions: Optional[EntityPermissions] = None

    @validator('name')
    def validate_name(cls, v):
        if not v.islower():
            raise ValueError('Entity name must be lowercase')
        if not v.replace('_', '').isalnum():
            raise ValueError('Entity name must contain only letters, numbers, and underscores')
        if v in ['user', 'company', 'role', 'permission', 'audit_log', 'system']:
            raise ValueError('Entity name is reserved')
        return v

    @validator('category')
    def validate_category(cls, v):
        valid_categories = ['core', 'crm', 'erp', 'financial', 'inventory', 'hr', 'greek', 'custom']
        if v not in valid_categories:
            raise ValueError(f'Invalid category: {v}')
        return v

class DynamicEntityUpdate(BaseModel):
    label_singular: Optional[str] = None
    label_plural: Optional[str] = None
    label_singular_greek: Optional[str] = None
    label_plural_greek: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    description_greek: Optional[str] = None
    greek_compliance: Optional[GreekComplianceConfig] = None
    permissions: Optional[EntityPermissions] = None
    is_active: Optional[bool] = None

class DynamicEntityResponse(BaseModel):
    id: str
    name: str
    plural_name: str
    label_singular: str
    label_plural: str
    label_singular_greek: Optional[str]
    label_plural_greek: Optional[str]
    icon: str
    color: str
    description: Optional[str]
    description_greek: Optional[str]
    module: str
    category: str
    customization_level: str
    greek_compliance: Dict[str, Any]
    aade_integration: bool
    tax_relevant: bool
    gdpr_relevant: bool
    permissions: Dict[str, List[str]]
    field_count: int
    layout_count: int
    record_count: int
    version: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    is_active: bool
    is_system_entity: bool

    class Config:
        from_attributes = True

class LayoutFieldConfig(BaseModel):
    field_id: str
    order: int = 1
    width: Optional[int] = None
    height: Optional[int] = None
    is_visible: bool = True
    is_readonly: bool = False
    is_required: Optional[bool] = None
    custom_label: Optional[str] = None
    custom_label_greek: Optional[str] = None
    placeholder: Optional[str] = None
    placeholder_greek: Optional[str] = None

class LayoutSectionConfig(BaseModel):
    id: Optional[str] = None
    name: str
    name_greek: Optional[str] = None
    order: int = 1
    columns: int = 2
    is_collapsible: bool = True
    is_collapsed: bool = False
    icon: Optional[str] = None
    description: Optional[str] = None
    description_greek: Optional[str] = None
    fields: List[LayoutFieldConfig] = []

class EntityLayoutCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    name_greek: Optional[str] = Field(None, max_length=200)
    type: str = "form"
    is_default: bool = False
    is_greek_optimized: bool = False
    
    # Layout Configuration
    columns: int = 2
    spacing: str = "normal"
    show_section_headers: bool = True
    show_field_labels: bool = True
    enable_drag_and_drop: bool = True
    enable_inline_editing: bool = False
    theme: str = "light"
    
    # Sections
    sections: List[LayoutSectionConfig] = []
    
    # Custom Settings
    custom_settings: Optional[Dict[str, Any]] = None
    custom_css: Optional[str] = None

    @validator('type')
    def validate_type(cls, v):
        valid_types = [
            'form', 'list', 'detail', 'search', 'print', 'mobile', 
            'kanban', 'calendar', 'timeline', 'greek_invoice', 'greek_report'
        ]
        if v not in valid_types:
            raise ValueError(f'Invalid layout type: {v}')
        return v

class EntityLayoutUpdate(BaseModel):
    name: Optional[str] = None
    name_greek: Optional[str] = None
    is_default: Optional[bool] = None
    is_greek_optimized: Optional[bool] = None
    columns: Optional[int] = None
    spacing: Optional[str] = None
    show_section_headers: Optional[bool] = None
    show_field_labels: Optional[bool] = None
    theme: Optional[str] = None
    sections: Optional[List[LayoutSectionConfig]] = None
    custom_settings: Optional[Dict[str, Any]] = None

class EntityLayoutResponse(BaseModel):
    id: str
    entity_id: str
    name: str
    name_greek: Optional[str]
    type: str
    is_default: bool
    is_greek_optimized: bool
    configuration: Dict[str, Any]
    sections: List[Dict[str, Any]]
    permissions: List[Dict[str, Any]]
    responsive_settings: Dict[str, Any]
    custom_settings: Dict[str, Any]
    version: str
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True

# Bulk operations
class BulkFieldOperation(BaseModel):
    operation: str = Field(..., description="Operation type: create, update, delete")
    field_ids: Optional[List[str]] = None
    field_data: Optional[List[Union[DynamicFieldCreate, DynamicFieldUpdate]]] = None

class EntityExportRequest(BaseModel):
    include_fields: bool = True
    include_layouts: bool = True
    include_data: bool = False
    include_workflows: bool = False
    format: str = "json"

# ============================================================================
# DEPENDENCY FUNCTIONS
# ============================================================================

async def get_entity_or_404(
    entity_id: str = Path(..., description="Entity ID"),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
) -> DynamicEntityModel:
    """Get entity by ID or raise 404"""
    entity = db.query(DynamicEntityModel).filter(
        and_(
            DynamicEntityModel.id == entity_id,
            DynamicEntityModel.company_id == company_id,
            DynamicEntityModel.is_active == True
        )
    ).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return entity

async def get_field_or_404(
    field_id: str = Path(..., description="Field ID"),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
) -> DynamicFieldModel:
    """Get field by ID or raise 404"""
    field = db.query(DynamicFieldModel).filter(
        and_(
            DynamicFieldModel.id == field_id,
            DynamicFieldModel.company_id == company_id,
            DynamicFieldModel.is_active == True
        )
    ).first()
    
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    
    return field

async def get_layout_or_404(
    layout_id: str = Path(..., description="Layout ID"),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
) -> EntityLayoutModel:
    """Get layout by ID or raise 404"""
    layout = db.query(EntityLayoutModel).filter(
        and_(
            EntityLayoutModel.id == layout_id,
            EntityLayoutModel.company_id == company_id
        )
    ).first()
    
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    return layout

# ============================================================================
# ENTITY MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/", response_model=List[DynamicEntityResponse])
async def list_entities(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    module: Optional[str] = Query(None, description="Filter by module"),
    search: Optional[str] = Query(None, description="Search in name and labels"),
    active_only: bool = Query(True, description="Show only active entities"),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
):
    """List all dynamic entities with optional filtering"""
    print(f"Listing entities for company {company_id}")
    
    query = db.query(DynamicEntityModel).filter(
        DynamicEntityModel.company_id == company_id
    )
    
    if active_only:
        query = query.filter(DynamicEntityModel.is_active == True)
    
    if category:
        query = query.filter(DynamicEntityModel.category == category)
    
    if module:
        query = query.filter(DynamicEntityModel.module == module)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                DynamicEntityModel.name.ilike(search_term),
                DynamicEntityModel.label_singular.ilike(search_term),
                DynamicEntityModel.label_plural.ilike(search_term),
                DynamicEntityModel.label_singular_greek.ilike(search_term),
                DynamicEntityModel.label_plural_greek.ilike(search_term),
                DynamicEntityModel.description.ilike(search_term)
            )
        )
    
    entities = query.order_by(DynamicEntityModel.created_at.desc()).offset(skip).limit(limit).all()
    
    # Add computed fields
    for entity in entities:
        entity.field_count = len(entity.fields) if hasattr(entity, 'fields') else 0
        entity.layout_count = len(entity.layouts) if hasattr(entity, 'layouts') else 0
        entity.record_count = 0  # TODO: Implement record counting
    
    return entities

@router.post("/", response_model=DynamicEntityResponse, status_code=201)
async def create_entity(
    entity_data: DynamicEntityCreate,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
):
    """Create a new dynamic entity"""
    print(f"Creating entity {entity_data.name} for company {company_id}")
    
    # Check if entity with same name exists
    existing = db.query(DynamicEntityModel).filter(
        and_(
            DynamicEntityModel.name == entity_data.name,
            DynamicEntityModel.company_id == company_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Entity with this name already exists")
    
    # Greek compliance validation
    if entity_data.greek_compliance and entity_data.greek_compliance.aade_reporting:
        await validate_greek_compliance(entity_data.dict())
    
    # Create entity
    entity = DynamicEntityModel(
        id=str(uuid.uuid4()),
        company_id=company_id,
        name=entity_data.name,
        plural_name=entity_data.plural_name,
        label_singular=entity_data.label_singular,
        label_plural=entity_data.label_plural,
        label_singular_greek=entity_data.label_singular_greek,
        label_plural_greek=entity_data.label_plural_greek,
        icon=entity_data.icon,
        color=entity_data.color,
        description=entity_data.description,
        description_greek=entity_data.description_greek,
        module=entity_data.module,
        category=entity_data.category,
        customization_level=entity_data.customization_level,
        greek_compliance=entity_data.greek_compliance.dict() if entity_data.greek_compliance else {},
        aade_integration=entity_data.aade_integration,
        tax_relevant=entity_data.tax_relevant,
        gdpr_relevant=entity_data.gdpr_relevant,
        permissions=entity_data.permissions.dict() if entity_data.permissions else {},
        version="1.0.0",
        created_by="system",  # TODO: Get from auth context
        is_active=True,
        is_system_entity=False
    )
    
    db.add(entity)
    db.commit()
    db.refresh(entity)
    
    # Add computed fields
    entity.field_count = 0
    entity.layout_count = 0
    entity.record_count = 0
    
    print(f"Entity created successfully: {entity.name} ({entity.id})")
    return entity

@router.get("/{entity_id}", response_model=DynamicEntityResponse)
async def get_entity(entity: DynamicEntityModel = Depends(get_entity_or_404)):
    """Get a specific dynamic entity by ID"""
    print(f"Retrieved entity: {entity.name} ({entity.id})")
    
    # Add computed fields
    entity.field_count = len(entity.fields) if hasattr(entity, 'fields') else 0
    entity.layout_count = len(entity.layouts) if hasattr(entity, 'layouts') else 0
    entity.record_count = 0  # TODO: Implement record counting
    
    return entity

@router.put("/{entity_id}", response_model=DynamicEntityResponse)
async def update_entity(
    entity_data: DynamicEntityUpdate,
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Update a dynamic entity"""
    print(f"Updating entity: {entity.name} ({entity.id})")
    
    # Update fields
    update_data = entity_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(entity, field):
            setattr(entity, field, value)
    
    entity.updated_at = datetime.utcnow()
    entity.version = "1.0.1"  # TODO: Implement proper versioning
    
    db.commit()
    db.refresh(entity)
    
    # Add computed fields
    entity.field_count = len(entity.fields) if hasattr(entity, 'fields') else 0
    entity.layout_count = len(entity.layouts) if hasattr(entity, 'layouts') else 0
    entity.record_count = 0
    
    return entity

@router.delete("/{entity_id}", status_code=204)
async def delete_entity(
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Soft delete a dynamic entity"""
    print(f"Deleting entity: {entity.name} ({entity.id})")
    
    entity.is_active = False
    entity.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Entity deleted successfully"}

# ============================================================================
# FIELD MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/{entity_id}/fields", response_model=List[DynamicFieldResponse])
async def list_entity_fields(
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    active_only: bool = Query(True, description="Show only active fields"),
    include_system: bool = Query(False, description="Include system fields"),
    db: Session = Depends(get_db)
):
    """List all fields for a specific entity"""
    print(f"Listing fields for entity: {entity.name}")
    
    query = db.query(DynamicFieldModel).filter(
        DynamicFieldModel.entity_id == entity.id
    )
    
    if active_only:
        query = query.filter(DynamicFieldModel.is_active == True)
    
    if not include_system:
        query = query.filter(DynamicFieldModel.is_system_field == False)
    
    fields = query.order_by(DynamicFieldModel.display_order).all()
    return fields

@router.post("/{entity_id}/fields", response_model=DynamicFieldResponse, status_code=201)
async def create_entity_field(
    field_data: DynamicFieldCreate,
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
):
    """Create a new field for an entity"""
    print(f"Creating field {field_data.name} for entity {entity.name}")
    
    # Check if field with same name exists
    existing = db.query(DynamicFieldModel).filter(
        and_(
            DynamicFieldModel.entity_id == entity.id,
            DynamicFieldModel.name == field_data.name
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Field with this name already exists")
    
    # Greek field validation
    if field_data.type.startswith('greek_'):
        await validate_greek_field_data(field_data)
    
    # Create field
    field = DynamicFieldModel(
        id=str(uuid.uuid4()),
        entity_id=entity.id,
        company_id=company_id,
        name=field_data.name,
        label=field_data.label,
        label_greek=field_data.label_greek,
        type=field_data.type,
        description=field_data.description,
        description_greek=field_data.description_greek,
        help_text=field_data.help_text,
        help_text_greek=field_data.help_text_greek,
        required=field_data.required,
        unique=field_data.unique,
        indexed=field_data.indexed,
        searchable=field_data.searchable,
        sortable=field_data.sortable,
        filterable=field_data.filterable,
        exportable=field_data.exportable,
        default_value=field_data.default_value,
        min_value=field_data.min_value,
        max_value=field_data.max_value,
        min_length=field_data.min_length,
        max_length=field_data.max_length,
        pattern=field_data.pattern,
        options=json.dumps(field_data.options) if field_data.options else None,
        validation=field_data.validation.dict() if field_data.validation else {},
        greek_validation=field_data.greek_validation.dict() if field_data.greek_validation else {},
        display_order=field_data.display_order,
        grid_column=field_data.grid_column,
        grid_width=field_data.grid_width,
        detail_section=field_data.detail_section,
        is_inline_editable=field_data.is_inline_editable,
        show_in_list=field_data.show_in_list,
        show_in_detail=field_data.show_in_detail,
        show_in_search=field_data.show_in_search,
        permissions=field_data.permissions.dict() if field_data.permissions else {},
        version="1.0.0",
        created_by="system",
        is_active=True,
        is_system_field=False
    )
    
    db.add(field)
    db.commit()
    db.refresh(field)
    
    print(f"Field created successfully: {field.name} ({field.id})")
    return field

@router.get("/{entity_id}/fields/{field_id}", response_model=DynamicFieldResponse)
async def get_entity_field(
    field: DynamicFieldModel = Depends(get_field_or_404),
    entity: DynamicEntityModel = Depends(get_entity_or_404)
):
    """Get a specific field by ID"""
    if field.entity_id != entity.id:
        raise HTTPException(status_code=404, detail="Field not found in this entity")
    
    print(f"Retrieved field: {field.name} ({field.id})")
    return field

@router.put("/{entity_id}/fields/{field_id}", response_model=DynamicFieldResponse)
async def update_entity_field(
    field_data: DynamicFieldUpdate,
    field: DynamicFieldModel = Depends(get_field_or_404),
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Update a field"""
    if field.entity_id != entity.id:
        raise HTTPException(status_code=404, detail="Field not found in this entity")
    
    print(f"Updating field: {field.name} ({field.id})")
    
    # Update fields
    update_data = field_data.dict(exclude_unset=True)
    for field_name, value in update_data.items():
        if hasattr(field, field_name):
            setattr(field, field_name, value)
    
    field.updated_at = datetime.utcnow()
    field.version = "1.0.1"
    
    db.commit()
    db.refresh(field)
    
    return field

@router.delete("/{entity_id}/fields/{field_id}", status_code=204)
async def delete_entity_field(
    field: DynamicFieldModel = Depends(get_field_or_404),
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Soft delete a field"""
    if field.entity_id != entity.id:
        raise HTTPException(status_code=404, detail="Field not found in this entity")
    
    print(f"Deleting field: {field.name} ({field.id})")
    
    field.is_active = False
    field.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Field deleted successfully"}

# ============================================================================
# LAYOUT MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/{entity_id}/layouts", response_model=List[EntityLayoutResponse])
async def list_entity_layouts(
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    layout_type: Optional[str] = Query(None, description="Filter by layout type"),
    db: Session = Depends(get_db)
):
    """List all layouts for a specific entity"""
    print(f"Listing layouts for entity: {entity.name}")
    
    query = db.query(EntityLayoutModel).filter(
        EntityLayoutModel.entity_id == entity.id
    )
    
    if layout_type:
        query = query.filter(EntityLayoutModel.type == layout_type)
    
    layouts = query.order_by(EntityLayoutModel.created_at.desc()).all()
    return layouts

@router.post("/{entity_id}/layouts", response_model=EntityLayoutResponse, status_code=201)
async def create_entity_layout(
    layout_data: EntityLayoutCreate,
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
):
    """Create a new layout for an entity"""
    print(f"Creating layout {layout_data.name} for entity {entity.name}")
    
    # Create layout
    layout = EntityLayoutModel(
        id=str(uuid.uuid4()),
        entity_id=entity.id,
        company_id=company_id,
        name=layout_data.name,
        name_greek=layout_data.name_greek,
        type=layout_data.type,
        is_default=layout_data.is_default,
        is_greek_optimized=layout_data.is_greek_optimized,
        configuration={
            "columns": layout_data.columns,
            "spacing": layout_data.spacing,
            "show_section_headers": layout_data.show_section_headers,
            "show_field_labels": layout_data.show_field_labels,
            "enable_drag_and_drop": layout_data.enable_drag_and_drop,
            "enable_inline_editing": layout_data.enable_inline_editing,
            "theme": layout_data.theme,
        },
        sections=[section.dict() for section in layout_data.sections],
        permissions=[{
            "role": "admin",
            "can_view": True,
            "can_edit": True,
            "can_customize": True,
        }],
        responsive_settings={
            "mobile": {"columns_per_row": 1, "hide_fields": [], "collapses_sections": []},
            "tablet": {"columns_per_row": 2, "hide_fields": [], "collapses_sections": []},
            "desktop": {"columns_per_row": layout_data.columns, "hide_fields": [], "collapses_sections": []},
            "large_desktop": {"columns_per_row": layout_data.columns, "hide_fields": [], "collapses_sections": []},
        },
        custom_settings=layout_data.custom_settings or {},
        custom_css=layout_data.custom_css,
        version="1.0.0",
        created_by="system"
    )
    
    db.add(layout)
    db.commit()
    db.refresh(layout)
    
    print(f"Layout created successfully: {layout.name} ({layout.id})")
    return layout

@router.get("/{entity_id}/layouts/{layout_id}", response_model=EntityLayoutResponse)
async def get_entity_layout(
    layout: EntityLayoutModel = Depends(get_layout_or_404),
    entity: DynamicEntityModel = Depends(get_entity_or_404)
):
    """Get a specific layout by ID"""
    if layout.entity_id != entity.id:
        raise HTTPException(status_code=404, detail="Layout not found in this entity")
    
    print(f"Retrieved layout: {layout.name} ({layout.id})")
    return layout

@router.put("/{entity_id}/layouts/{layout_id}", response_model=EntityLayoutResponse)
async def update_entity_layout(
    layout_data: EntityLayoutUpdate,
    layout: EntityLayoutModel = Depends(get_layout_or_404),
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Update a layout"""
    if layout.entity_id != entity.id:
        raise HTTPException(status_code=404, detail="Layout not found in this entity")
    
    print(f"Updating layout: {layout.name} ({layout.id})")
    
    # Update fields
    update_data = layout_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == 'sections' and value:
            layout.sections = [section.dict() if hasattr(section, 'dict') else section for section in value]
        elif hasattr(layout, field):
            setattr(layout, field, value)
    
    layout.updated_at = datetime.utcnow()
    layout.version = "1.0.1"
    
    db.commit()
    db.refresh(layout)
    
    return layout

@router.delete("/{entity_id}/layouts/{layout_id}", status_code=204)
async def delete_entity_layout(
    layout: EntityLayoutModel = Depends(get_layout_or_404),
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Delete a layout"""
    if layout.entity_id != entity.id:
        raise HTTPException(status_code=404, detail="Layout not found in this entity")
    
    print(f"Deleting layout: {layout.name} ({layout.id})")
    
    db.delete(layout)
    db.commit()
    
    return {"message": "Layout deleted successfully"}

# ============================================================================
# BULK OPERATIONS
# ============================================================================

@router.post("/{entity_id}/fields/bulk", response_model=Dict[str, Any])
async def bulk_field_operations(
    operation: BulkFieldOperation,
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
):
    """Perform bulk operations on fields"""
    print(f"Performing bulk {operation.operation} operation on entity {entity.name}")
    
    results = {"success": [], "errors": []}
    
    if operation.operation == "delete" and operation.field_ids:
        for field_id in operation.field_ids:
            try:
                field = db.query(DynamicFieldModel).filter(
                    and_(
                        DynamicFieldModel.id == field_id,
                        DynamicFieldModel.entity_id == entity.id,
                        DynamicFieldModel.company_id == company_id
                    )
                ).first()
                
                if field:
                    field.is_active = False
                    field.updated_at = datetime.utcnow()
                    results["success"].append(field_id)
                else:
                    results["errors"].append({"field_id": field_id, "error": "Field not found"})
            except Exception as e:
                results["errors"].append({"field_id": field_id, "error": str(e)})
    
    db.commit()
    
    return results

# ============================================================================
# IMPORT/EXPORT ENDPOINTS
# ============================================================================

@router.post("/{entity_id}/export")
async def export_entity(
    export_request: EntityExportRequest,
    entity: DynamicEntityModel = Depends(get_entity_or_404),
    db: Session = Depends(get_db)
):
    """Export entity definition and data"""
    print(f"Exporting entity: {entity.name}")
    
    export_data = {
        "entity": {
            "id": entity.id,
            "name": entity.name,
            "plural_name": entity.plural_name,
            "label_singular": entity.label_singular,
            "label_plural": entity.label_plural,
            "label_singular_greek": entity.label_singular_greek,
            "label_plural_greek": entity.label_plural_greek,
            "icon": entity.icon,
            "color": entity.color,
            "description": entity.description,
            "description_greek": entity.description_greek,
            "module": entity.module,
            "category": entity.category,
            "greek_compliance": entity.greek_compliance,
            "version": entity.version,
            "exported_at": datetime.utcnow().isoformat()
        }
    }
    
    if export_request.include_fields:
        fields = db.query(DynamicFieldModel).filter(
            DynamicFieldModel.entity_id == entity.id
        ).all()
        export_data["fields"] = [
            {
                "name": field.name,
                "label": field.label,
                "label_greek": field.label_greek,
                "type": field.type,
                "required": field.required,
                "unique": field.unique,
                "validation": field.validation,
                # Add other field properties
            }
            for field in fields
        ]
    
    if export_request.include_layouts:
        layouts = db.query(EntityLayoutModel).filter(
            EntityLayoutModel.entity_id == entity.id
        ).all()
        export_data["layouts"] = [
            {
                "name": layout.name,
                "name_greek": layout.name_greek,
                "type": layout.type,
                "configuration": layout.configuration,
                "sections": layout.sections,
                # Add other layout properties
            }
            for layout in layouts
        ]
    
    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": f"attachment; filename={entity.name}_export.json"
        }
    )

@router.get("/categories", response_model=List[Dict[str, str]])
async def get_entity_categories():
    """Get list of available entity categories"""
    return [
        {"value": "core", "label": "Core Business", "label_greek": "Βασική Επιχείρηση"},
        {"value": "crm", "label": "CRM", "label_greek": "CRM"},
        {"value": "erp", "label": "ERP", "label_greek": "ERP"},
        {"value": "financial", "label": "Financial", "label_greek": "Οικονομικά"},
        {"value": "inventory", "label": "Inventory", "label_greek": "Αποθέματα"},
        {"value": "hr", "label": "Human Resources", "label_greek": "Ανθρώπινο Δυναμικό"},
        {"value": "greek", "label": "Greek Specific", "label_greek": "Ελληνικά Ειδικά"},
        {"value": "custom", "label": "Custom", "label_greek": "Προσαρμοσμένα"},
    ]

@router.get("/field-types", response_model=List[Dict[str, Any]])
async def get_field_types():
    """Get list of available field types with metadata"""
    return [
        # Basic Types
        {"value": "text", "label": "Text", "label_greek": "Κείμενο", "category": "basic"},
        {"value": "textarea", "label": "Long Text", "label_greek": "Μεγάλο Κείμενο", "category": "basic"},
        {"value": "email", "label": "Email", "label_greek": "Email", "category": "basic"},
        {"value": "phone", "label": "Phone", "label_greek": "Τηλέφωνο", "category": "basic"},
        {"value": "url", "label": "Website URL", "label_greek": "Ιστοσελίδα", "category": "basic"},
        
        # Numeric Types
        {"value": "number", "label": "Number", "label_greek": "Αριθμός", "category": "numeric"},
        {"value": "decimal", "label": "Decimal", "label_greek": "Δεκαδικός", "category": "numeric"},
        {"value": "currency", "label": "Currency", "label_greek": "Νόμισμα", "category": "numeric"},
        {"value": "percentage", "label": "Percentage", "label_greek": "Ποσοστό", "category": "numeric"},
        
        # Date & Time
        {"value": "date", "label": "Date", "label_greek": "Ημερομηνία", "category": "datetime"},
        {"value": "datetime", "label": "Date & Time", "label_greek": "Ημερομηνία & Ώρα", "category": "datetime"},
        {"value": "time", "label": "Time", "label_greek": "Ώρα", "category": "datetime"},
        
        # Selection Types
        {"value": "boolean", "label": "Yes/No", "label_greek": "Ναι/Όχι", "category": "selection"},
        {"value": "dropdown", "label": "Dropdown", "label_greek": "Λίστα Επιλογών", "category": "selection"},
        {"value": "multiselect", "label": "Multi-Select", "label_greek": "Πολλαπλή Επιλογή", "category": "selection"},
        {"value": "radio", "label": "Radio Buttons", "label_greek": "Κουμπιά Επιλογής", "category": "selection"},
        
        # Greek-Specific Types
        {"value": "greek_afm", "label": "Greek AFM", "label_greek": "ΑΦΜ", "category": "greek"},
        {"value": "greek_amka", "label": "Greek AMKA", "label_greek": "ΑΜΚΑ", "category": "greek"},
        {"value": "greek_iban", "label": "Greek IBAN", "label_greek": "Ελληνικό IBAN", "category": "greek"},
        {"value": "greek_phone", "label": "Greek Phone", "label_greek": "Ελληνικό Τηλέφωνο", "category": "greek"},
        {"value": "greek_doy_selector", "label": "Greek DOY", "label_greek": "ΔΟΥ", "category": "greek"},
        
        # Advanced Types
        {"value": "calculated", "label": "Calculated", "label_greek": "Υπολογιζόμενο", "category": "advanced"},
        {"value": "formula", "label": "Formula", "label_greek": "Φόρμουλα", "category": "advanced"},
        {"value": "signature", "label": "Digital Signature", "label_greek": "Ψηφιακή Υπογραφή", "category": "advanced"},
    ]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def validate_greek_field_data(field_data: DynamicFieldCreate):
    """Validate Greek-specific field data"""
    if field_data.type == "greek_afm":
        if field_data.default_value and not validate_afm(field_data.default_value):
            raise HTTPException(status_code=400, detail="Invalid default AFM value")
    
    elif field_data.type == "greek_amka":
        if field_data.default_value and not validate_amka(field_data.default_value):
            raise HTTPException(status_code=400, detail="Invalid default AMKA value")
    
    elif field_data.type == "greek_phone":
        if field_data.default_value and not validate_greek_phone(field_data.default_value):
            raise HTTPException(status_code=400, detail="Invalid default Greek phone number")

# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/stats/overview")
async def get_entities_overview(
    db: Session = Depends(get_db),
    company_id: str = Depends(get_current_company)
):
    """Get overview statistics for dynamic entities"""
    total_entities = db.query(DynamicEntityModel).filter(
        and_(
            DynamicEntityModel.company_id == company_id,
            DynamicEntityModel.is_active == True
        )
    ).count()
    
    total_fields = db.query(DynamicFieldModel).filter(
        and_(
            DynamicFieldModel.company_id == company_id,
            DynamicFieldModel.is_active == True
        )
    ).count()
    
    total_layouts = db.query(EntityLayoutModel).filter(
        EntityLayoutModel.company_id == company_id
    ).count()
    
    # Category breakdown
    category_stats = db.query(
        DynamicEntityModel.category,
        db.func.count(DynamicEntityModel.id).label('count')
    ).filter(
        and_(
            DynamicEntityModel.company_id == company_id,
            DynamicEntityModel.is_active == True
        )
    ).group_by(DynamicEntityModel.category).all()
    
    return {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "total_layouts": total_layouts,
        "categories": [{"category": cat, "count": count} for cat, count in category_stats],
        "generated_at": datetime.utcnow().isoformat()
    } 