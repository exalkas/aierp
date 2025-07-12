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