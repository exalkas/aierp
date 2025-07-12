"""
Simplified VAT API
User-friendly VAT management with product configuration, suggestions, and supplier invoice validation
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.product_vat_config import (
    ProductVATConfig, VATSuggestionRule, SupplierInvoiceVATValidation,
    VATConfigStatus, VATSuggestionConfidence, ProductServiceTemplate
)
from app.models.product import Product
from app.models.business_entity import BusinessEntity
from app.models.invoice import Invoice
from app.services.vat_suggestion_service import (
    VATSuggestionService, VATSuggestionRequest, VATSuggestionResult
)
from app.services.supplier_invoice_vat_validation_service import (
    SupplierInvoiceVATValidationService, SupplierInvoiceVATValidationRequest
)
from app.services.product_service_template_service import ProductServiceTemplateService

# Create router
vat_router = APIRouter(prefix="/vat", tags=["VAT Management"])

# Pydantic models
class VATSuggestionRequestModel(BaseModel):
    product_name: str = Field(..., description="Product or service name")
    product_category: Optional[str] = Field(None, description="Product category")
    business_type: Optional[str] = Field(None, description="Business type")
    location_type: str = Field("mainland", description="Location type")
    context_hints: List[str] = Field(default=[], description="Context hints")
    product_description: Optional[str] = Field(None, description="Product description")

class VATSuggestionResponseModel(BaseModel):
    suggested_rate: float
    confidence: str
    reasoning: str
    legal_reference: Optional[str] = None
    alternative_rates: List[Dict[str, Any]] = []
    matched_rules: List[str] = []

class ProductVATConfigModel(BaseModel):
    product_id: str
    vat_rate: float
    vat_exemption_type: Optional[str] = None
    user_notes: Optional[str] = None
    template_id: Optional[str] = None  # If created from template

class ProductVATConfigUpdateModel(BaseModel):
    vat_rate: Optional[float] = None
    vat_exemption_type: Optional[str] = None
    user_notes: Optional[str] = None

class SupplierInvoiceLineItem(BaseModel):
    product_name: str
    product_category: Optional[str] = None
    vat_rate: float
    line_amount: float

class SupplierInvoiceValidationRequestModel(BaseModel):
    supplier_id: str
    invoice_number: str
    line_items: List[SupplierInvoiceLineItem]
    validation_context: Dict[str, Any] = {}

class UserDecisionModel(BaseModel):
    action: str = Field(..., description="accept_supplier_rate, flag_for_review, or correct_rate")
    user_notes: Optional[str] = None

class ProductServiceTemplateCreateModel(BaseModel):
    name: str = Field(..., description="Template name")
    display_name: str = Field(..., description="Display name with emoji")
    description: Optional[str] = Field(None, description="Template description")
    category: str = Field(..., description="Template category")
    vat_rate: float = Field(..., description="VAT rate")
    vat_exemption_type: Optional[str] = Field(None, description="Exemption type")
    vat_reasoning: str = Field(..., description="Why this VAT rate applies")
    legal_reference: Optional[str] = Field(None, description="Legal reference")
    business_types: List[str] = Field(default=[], description="Applicable business types")
    keywords: List[str] = Field(default=[], description="Search keywords")
    is_popular: bool = Field(False, description="Mark as popular template")

class ProductServiceTemplateUpdateModel(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    vat_rate: Optional[float] = None
    vat_exemption_type: Optional[str] = None
    vat_reasoning: Optional[str] = None
    legal_reference: Optional[str] = None
    business_types: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    is_popular: Optional[bool] = None
    is_active: Optional[bool] = None


# Helper functions
def get_vat_suggestion_service(db: Session = Depends(get_db)) -> VATSuggestionService:
    return VATSuggestionService(db)

def get_supplier_validation_service(db: Session = Depends(get_db)) -> SupplierInvoiceVATValidationService:
    return SupplierInvoiceVATValidationService(db)

def get_template_service(db: Session = Depends(get_db)) -> ProductServiceTemplateService:
    return ProductServiceTemplateService(db)


# Product/Service Template Endpoints
@vat_router.get("/templates")
async def get_product_service_templates(
    category: Optional[str] = Query(None, description="Filter by category"),
    popular_only: bool = Query(False, description="Show only popular templates"),
    search: Optional[str] = Query(None, description="Search templates"),
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Get product/service templates for dropdown selection
    """
    try:
        if search:
            templates = template_service.search_templates(search, category)
        elif popular_only:
            templates = template_service.get_popular_templates()
        else:
            templates = template_service.get_templates(category=category)
        
        return {
            "templates": [template.to_dict() for template in templates]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting templates: {str(e)}"
        )


@vat_router.get("/templates/grouped")
async def get_templates_grouped_by_category(
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Get templates grouped by category for organized UI display
    """
    try:
        grouped_templates = template_service.get_templates_grouped_by_category()
        
        return {
            "categories": grouped_templates,
            "category_order": ["food_service", "healthcare", "legal", "retail", "construction", "professional"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting grouped templates: {str(e)}"
        )


@vat_router.post("/templates/{template_id}/select")
async def select_template_for_product(
    template_id: str,
    product_id: str,
    company_id: str = Query(..., description="Company ID"),
    user_id: str = Query(..., description="User ID"),
    location_type: str = Query("mainland", description="Location type"),
    template_service: ProductServiceTemplateService = Depends(get_template_service),
    db: Session = Depends(get_db)
):
    """
    Select a template and create VAT configuration for a product
    """
    try:
        # Get template
        template = template_service.get_template_by_id(template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        # Check if product exists
        product = db.query(Product).filter(
            Product.id == product_id,
            Product.company_id == company_id
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Check if VAT config already exists
        existing_config = db.query(ProductVATConfig).filter(
            ProductVATConfig.product_id == product_id
        ).first()
        
        if existing_config:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="VAT configuration already exists for this product"
            )
        
        # Calculate VAT rate based on location
        vat_rate = template.vat_rate
        if location_type == "aegean_islands" and template.island_vat_rate:
            vat_rate = template.island_vat_rate
        
        # Create VAT configuration from template
        vat_config = ProductVATConfig(
            company_id=company_id,
            product_id=product_id,
            template_id=template_id,
            vat_rate=vat_rate,
            vat_exemption_type=template.vat_exemption_type,
            user_notes=f"Created from template: {template.name}",
            suggested_vat_rate=vat_rate,
            suggestion_confidence=VATSuggestionConfidence.HIGH,
            suggestion_reasoning=template.vat_reasoning,
            selected_from_template=True,
            template_modified=False,
            created_by=user_id,
            updated_by=user_id
        )
        
        db.add(vat_config)
        
        # Increment template usage count
        template_service.increment_usage_count(template_id)
        
        db.commit()
        db.refresh(vat_config)
        
        return {
            "id": str(vat_config.id),
            "message": "VAT configuration created from template",
            "template_name": template.name,
            "vat_rate": float(vat_rate),
            "vat_reasoning": template.vat_reasoning
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error selecting template: {str(e)}"
        )


# Admin Template Management Endpoints
@vat_router.get("/admin/templates")
async def get_admin_templates(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Get templates for admin management (Admin endpoint)
    """
    try:
        templates = template_service.get_templates(
            category=category,
            is_active=is_active,
            limit=500
        )
        
        return {
            "templates": [template.to_dict() for template in templates],
            "statistics": template_service.get_template_statistics()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting admin templates: {str(e)}"
        )


@vat_router.post("/admin/templates")
async def create_product_service_template(
    template: ProductServiceTemplateCreateModel,
    admin_id: str = Query(..., description="Admin user ID"),
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Create new product/service template (Admin endpoint)
    """
    try:
        new_template = template_service.create_template(
            name=template.name,
            display_name=template.display_name,
            description=template.description,
            category=template.category,
            vat_rate=Decimal(str(template.vat_rate)),
            vat_reasoning=template.vat_reasoning,
            vat_exemption_type=template.vat_exemption_type,
            legal_reference=template.legal_reference,
            business_types=template.business_types,
            keywords=template.keywords,
            is_popular=template.is_popular,
            created_by=admin_id
        )
        
        return {
            "id": str(new_template.id),
            "message": "Template created successfully",
            "template": new_template.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating template: {str(e)}"
        )


@vat_router.put("/admin/templates/{template_id}")
async def update_product_service_template(
    template_id: str,
    template_update: ProductServiceTemplateUpdateModel,
    admin_id: str = Query(..., description="Admin user ID"),
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Update product/service template (Admin endpoint)
    """
    try:
        updates = template_update.dict(exclude_unset=True)
        
        # Convert vat_rate to Decimal if provided
        if 'vat_rate' in updates:
            updates['vat_rate'] = Decimal(str(updates['vat_rate']))
        
        updated_template = template_service.update_template(
            template_id=template_id,
            updates=updates,
            updated_by=admin_id
        )
        
        if not updated_template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        return {
            "message": "Template updated successfully",
            "template": updated_template.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating template: {str(e)}"
        )


@vat_router.post("/admin/templates/bulk-create-defaults")
async def bulk_create_default_templates(
    admin_id: str = Query(..., description="Admin user ID"),
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Create default templates for common Greek business scenarios (Admin endpoint)
    """
    try:
        created_count = template_service.bulk_create_default_templates(created_by=admin_id)
        
        return {
            "message": f"Created {created_count} default templates",
            "created_count": created_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating default templates: {str(e)}"
        )


@vat_router.get("/admin/templates/statistics")
async def get_template_statistics(
    template_service: ProductServiceTemplateService = Depends(get_template_service)
):
    """
    Get template usage statistics (Admin endpoint)
    """
    try:
        stats = template_service.get_template_statistics()
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting template statistics: {str(e)}"
        )


# Existing VAT Suggestion Endpoints
@vat_router.post("/suggest", response_model=VATSuggestionResponseModel)
async def suggest_vat_rate(
    request: VATSuggestionRequestModel,
    company_id: str = Query(..., description="Company ID"),
    suggestion_service: VATSuggestionService = Depends(get_vat_suggestion_service)
):
    """
    Get VAT rate suggestion for a product/service
    """
    try:
        suggestion_request = VATSuggestionRequest(
            company_id=company_id,
            product_name=request.product_name,
            product_category=request.product_category,
            business_type=request.business_type,
            location_type=request.location_type,
            context_hints=request.context_hints,
            product_description=request.product_description
        )
        
        result = suggestion_service.suggest_vat_rate(suggestion_request)
        
        return VATSuggestionResponseModel(
            suggested_rate=float(result.suggested_rate),
            confidence=result.confidence.value,
            reasoning=result.reasoning,
            legal_reference=result.legal_reference,
            alternative_rates=result.alternative_rates,
            matched_rules=result.matched_rules
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating VAT suggestion: {str(e)}"
        )


# Product VAT Configuration Endpoints
@vat_router.get("/products/{product_id}/config")
async def get_product_vat_config(
    product_id: str,
    db: Session = Depends(get_db)
):
    """
    Get VAT configuration for a product
    """
    config = db.query(ProductVATConfig).filter(
        ProductVATConfig.product_id == product_id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product VAT configuration not found"
        )
    
    result = {
        "id": str(config.id),
        "product_id": str(config.product_id),
        "vat_rate": float(config.vat_rate),
        "vat_exemption_type": config.vat_exemption_type,
        "user_notes": config.user_notes,
        "suggested_vat_rate": float(config.suggested_vat_rate) if config.suggested_vat_rate else None,
        "suggestion_confidence": config.suggestion_confidence.value if config.suggestion_confidence else None,
        "suggestion_reasoning": config.suggestion_reasoning,
        "user_override": config.user_override,
        "selected_from_template": config.selected_from_template,
        "template_modified": config.template_modified,
        "status": config.status.value,
        "created_at": config.created_at.isoformat(),
        "updated_at": config.updated_at.isoformat()
    }
    
    # Include template info if available
    if config.template:
        result["template"] = {
            "id": str(config.template.id),
            "name": config.template.name,
            "display_name": config.template.display_name,
            "category": config.template.category
        }
    
    return result


@vat_router.post("/products/{product_id}/config", response_model=Dict[str, Any])
async def create_product_vat_config(
    product_id: str,
    config: ProductVATConfigModel,
    company_id: str = Query(..., description="Company ID"),
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db),
    suggestion_service: VATSuggestionService = Depends(get_vat_suggestion_service)
):
    """
    Create VAT configuration for a product
    """
    # Check if product exists
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == company_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if config already exists
    existing_config = db.query(ProductVATConfig).filter(
        ProductVATConfig.product_id == product_id
    ).first()
    
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="VAT configuration already exists for this product"
        )
    
    # Get suggestion for comparison
    suggestion_request = VATSuggestionRequest(
        company_id=company_id,
        product_name=product.name,
        product_category=product.category.name if product.category else None,
        business_type=None,  # Could be inferred from company
        location_type="mainland"  # Could be inferred from company
    )
    
    suggestion_result = suggestion_service.suggest_vat_rate(suggestion_request)
    
    # Create configuration
    vat_config = ProductVATConfig(
        company_id=company_id,
        product_id=product_id,
        template_id=config.template_id,
        vat_rate=Decimal(str(config.vat_rate)),
        vat_exemption_type=config.vat_exemption_type,
        user_notes=config.user_notes,
        suggested_vat_rate=suggestion_result.suggested_rate,
        suggestion_confidence=suggestion_result.confidence,
        suggestion_reasoning=suggestion_result.reasoning,
        user_override=abs(Decimal(str(config.vat_rate)) - suggestion_result.suggested_rate) > Decimal('0.01'),
        selected_from_template=bool(config.template_id),
        created_by=user_id,
        updated_by=user_id
    )
    
    db.add(vat_config)
    db.commit()
    db.refresh(vat_config)
    
    return {
        "id": str(vat_config.id),
        "message": "VAT configuration created successfully",
        "suggestion_used": not vat_config.user_override,
        "selected_from_template": vat_config.selected_from_template
    }


@vat_router.put("/products/{product_id}/config")
async def update_product_vat_config(
    product_id: str,
    config_update: ProductVATConfigUpdateModel,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Update VAT configuration for a product
    """
    vat_config = db.query(ProductVATConfig).filter(
        ProductVATConfig.product_id == product_id
    ).first()
    
    if not vat_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="VAT configuration not found"
        )
    
    # Update fields
    if config_update.vat_rate is not None:
        old_rate = vat_config.vat_rate
        vat_config.vat_rate = Decimal(str(config_update.vat_rate))
        
        # Check if this is an override
        if vat_config.suggested_vat_rate:
            vat_config.user_override = abs(vat_config.vat_rate - vat_config.suggested_vat_rate) > Decimal('0.01')
        
        # Mark as template modified if created from template
        if vat_config.selected_from_template and old_rate != vat_config.vat_rate:
            vat_config.template_modified = True
    
    if config_update.vat_exemption_type is not None:
        vat_config.vat_exemption_type = config_update.vat_exemption_type
    
    if config_update.user_notes is not None:
        vat_config.user_notes = config_update.user_notes
    
    vat_config.updated_by = user_id
    
    db.commit()
    
    return {
        "message": "VAT configuration updated successfully",
        "user_override": vat_config.user_override,
        "template_modified": vat_config.template_modified
    }


# Supplier Invoice Validation Endpoints
@vat_router.post("/supplier-invoices/validate")
async def validate_supplier_invoice(
    request: SupplierInvoiceValidationRequestModel,
    company_id: str = Query(..., description="Company ID"),
    validation_service: SupplierInvoiceVATValidationService = Depends(get_supplier_validation_service)
):
    """
    Validate supplier invoice VAT rates
    """
    try:
        # Convert line items to expected format
        line_items = []
        for item in request.line_items:
            line_items.append({
                "product_name": item.product_name,
                "product_category": item.product_category,
                "vat_rate": item.vat_rate,
                "line_amount": item.line_amount
            })
        
        validation_request = SupplierInvoiceVATValidationRequest(
            company_id=company_id,
            invoice_id=str(UUID()),  # Generate temp ID for now
            supplier_id=request.supplier_id,
            line_items=line_items,
            validation_context=request.validation_context
        )
        
        result = validation_service.validate_supplier_invoice(validation_request)
        
        return result.to_dict()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating supplier invoice: {str(e)}"
        )


@vat_router.post("/supplier-invoices/validations/{validation_id}/decisions/{line_number}")
async def record_user_decision(
    validation_id: str,
    line_number: int,
    decision: UserDecisionModel,
    user_id: str = Query(..., description="User ID"),
    validation_service: SupplierInvoiceVATValidationService = Depends(get_supplier_validation_service)
):
    """
    Record user decision about VAT inconsistency
    """
    try:
        success = validation_service.record_user_decision(
            validation_id=validation_id,
            line_number=line_number,
            action=decision.action,
            user_notes=decision.user_notes or "",
            decided_by=user_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Validation record not found"
            )
        
        return {"message": "User decision recorded successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error recording user decision: {str(e)}"
        )


@vat_router.get("/supplier-invoices/validations/history")
async def get_validation_history(
    company_id: str = Query(..., description="Company ID"),
    supplier_id: Optional[str] = Query(None, description="Supplier ID"),
    limit: int = Query(50, description="Limit results"),
    validation_service: SupplierInvoiceVATValidationService = Depends(get_supplier_validation_service)
):
    """
    Get validation history for a company
    """
    try:
        history = validation_service.get_validation_history(
            company_id=company_id,
            supplier_id=supplier_id,
            limit=limit
        )
        
        return {
            "validations": [
                {
                    "id": str(validation.id),
                    "supplier_id": str(validation.supplier_id),
                    "validation_status": validation.validation_status,
                    "total_inconsistencies": validation.total_inconsistencies,
                    "total_items_checked": validation.total_items_checked,
                    "created_at": validation.created_at.isoformat()
                }
                for validation in history
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting validation history: {str(e)}"
        )


@vat_router.get("/supplier-invoices/validations/statistics")
async def get_validation_statistics(
    company_id: str = Query(..., description="Company ID"),
    validation_service: SupplierInvoiceVATValidationService = Depends(get_supplier_validation_service)
):
    """
    Get validation statistics for a company
    """
    try:
        stats = validation_service.get_validation_statistics(company_id)
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting validation statistics: {str(e)}"
        )


# VAT Suggestion Rules Management (Admin)
@vat_router.get("/admin/suggestion-rules")
async def get_suggestion_rules(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    suggestion_service: VATSuggestionService = Depends(get_vat_suggestion_service)
):
    """
    Get VAT suggestion rules (Admin endpoint)
    """
    try:
        rules = suggestion_service.get_suggestion_rules(is_active)
        
        return {
            "rules": [
                {
                    "id": str(rule.id),
                    "rule_name": rule.rule_name,
                    "rule_code": rule.rule_code,
                    "description": rule.description,
                    "business_type": rule.business_type,
                    "product_category": rule.product_category,
                    "suggested_rate": float(rule.suggested_rate),
                    "confidence_level": rule.confidence_level.value,
                    "reasoning": rule.reasoning,
                    "priority": rule.priority,
                    "is_active": rule.is_active,
                    "created_at": rule.created_at.isoformat()
                }
                for rule in rules
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting suggestion rules: {str(e)}"
        )


@vat_router.post("/admin/suggestion-rules")
async def create_suggestion_rule(
    rule_name: str,
    rule_code: str,
    suggested_rate: float,
    confidence: str,
    reasoning: str,
    business_type: Optional[str] = None,
    product_category: Optional[str] = None,
    product_keywords: Optional[List[str]] = None,
    location_type: Optional[str] = None,
    context_hints: Optional[List[str]] = None,
    priority: int = 100,
    legal_reference: Optional[str] = None,
    suggestion_service: VATSuggestionService = Depends(get_vat_suggestion_service)
):
    """
    Create VAT suggestion rule (Admin endpoint)
    """
    try:
        confidence_enum = VATSuggestionConfidence(confidence)
        
        rule = suggestion_service.create_suggestion_rule(
            rule_name=rule_name,
            rule_code=rule_code,
            suggested_rate=Decimal(str(suggested_rate)),
            confidence=confidence_enum,
            reasoning=reasoning,
            business_type=business_type,
            product_category=product_category,
            product_keywords=product_keywords,
            location_type=location_type,
            context_hints=context_hints,
            priority=priority,
            legal_reference=legal_reference
        )
        
        return {
            "id": str(rule.id),
            "message": "VAT suggestion rule created successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating suggestion rule: {str(e)}"
        ) 