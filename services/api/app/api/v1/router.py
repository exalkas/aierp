"""
Main API Router for Greek ERP/CRM System
Version 1 API endpoints with Greek business features
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.core.config import settings
from app.api.v1.vat_simplified import vat_router
from app.api.v1.document_workflow import router as workflow_router
from app.api.v1.voice_commands import router as voice_router
from app.api.v1.business_entities import router as business_entities_router
from app.api.v1.contacts import router as contacts_router
from app.api.v1.contact_methods import router as contact_methods_router
from app.api.v1.contact_method_subtypes import router as contact_method_subtypes_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.greek_reference import router as greek_reference_router
from app.api.v1.dynamic_entities import router as dynamic_entities_router

# Security
security = HTTPBearer()

# Create main API router
api_router = APIRouter()

# Include simplified VAT router
api_router.include_router(vat_router)

# Include document workflow router
api_router.include_router(workflow_router)

# Include voice commands router
api_router.include_router(voice_router, prefix="/voice", tags=["voice-commands"])

# Include business entity router
api_router.include_router(business_entities_router, tags=["business-entities"])

# Include contacts router
api_router.include_router(contacts_router, tags=["contacts"])

# Include contact methods router
api_router.include_router(contact_methods_router, tags=["contact-methods"])

# Include contact method subtypes router
api_router.include_router(contact_method_subtypes_router, tags=["contact-method-subtypes"])

# Include dashboard router
api_router.include_router(dashboard_router, tags=["dashboard"])

# Include Greek reference data router
api_router.include_router(greek_reference_router, tags=["greek-reference"])

# Include dynamic entities router
api_router.include_router(dynamic_entities_router, tags=["dynamic-entities"])

# Legacy/compatibility endpoints for frontend
from fastapi import Request
from fastapi.responses import RedirectResponse

@api_router.get("/customers")
async def redirect_customers():
    """Redirect customers to business-entities with customer role filter"""
    return RedirectResponse(url="/api/v1/business-entities/?role_filter=customer", status_code=301)

@api_router.get("/suppliers")
async def redirect_suppliers():
    """Redirect suppliers to business-entities with supplier role filter"""
    return RedirectResponse(url="/api/v1/business-entities/?role_filter=supplier", status_code=301)

# Health check endpoint
@api_router.get("/health")
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "service": "greek-erp-api",
        "version": "1.0.0",
        "greek_compliance": True,
        "aade_enabled": bool(settings.AADE_SUBSCRIPTION_KEY)
    }

# Company management endpoints
@api_router.get("/companies")
async def list_companies():
    """List all companies"""
    return {
        "companies": [
            {
                "id": "1",
                "name": "Sample Company",
                "afm": "9",
                "doy": "Athens",
                "address": "Sample Address",
                "phone": "+30 210 1234567",
                "email": "info@sample.com",
                "status": "active"
            }
        ]
    }

@api_router.get("/companies/{company_id}")
async def get_company(company_id: str):
    """Get company details"""
    return {
        "id": company_id,
        "name": "Sample Company",
        "afm": "9",
        "doy": "Athens",
        "address": "Sample Address",
        "phone": "+30 210 1234567",
        "email": "info@sample.com",
        "status": "active"
    }

@api_router.post("/companies")
async def create_company(company_data: dict):
    """Create a new company"""
    return {
        "id": "new-company-id",
        "message": "Company created successfully",
        "company": company_data
    }

@api_router.put("/companies/{company_id}")
async def update_company(company_id: str, company_data: dict):
    """Update company details"""
    return {
        "id": company_id,
        "message": "Company updated successfully",
        "company": company_data
    }

@api_router.delete("/companies/{company_id}")
async def delete_company(company_id: str):
    """Delete a company"""
    return {
        "id": company_id,
        "message": "Company deleted successfully"
    } 