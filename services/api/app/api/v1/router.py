"""
Main API Router for Greek ERP/CRM System
Version 1 API endpoints with Greek business features
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.core.config import settings

# Security
security = HTTPBearer()

# Create main API router
api_router = APIRouter()

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

# Greek business validation endpoints
@api_router.get("/greek/vat-rates")
async def get_greek_vat_rates():
    """Get current Greek VAT rates"""
    return {
        "standard": settings.DEFAULT_VAT_RATE,
        "reduced_1": settings.REDUCED_VAT_RATE_1,
        "reduced_2": settings.REDUCED_VAT_RATE_2,
        "zero": settings.ZERO_VAT_RATE,
        "currency": settings.GREEK_CURRENCY,
        "locale": settings.GREEK_LOCALE
    }

@api_router.post("/greek/validate/afm")
async def validate_afm(data: dict):
    """Validate Greek AFM (Tax Number)"""
    afm = data.get("afm")
    if not afm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AFM is required"
        )
    
    # Basic validation (will be enhanced with middleware logic)
    import re
    afm_pattern = re.compile(r'^\d{9}$')
    
    if not afm_pattern.match(str(afm)):
        return {"valid": False, "message": "Invalid AFM format"}
    
    return {"valid": True, "message": "AFM format is valid"}

# Company management placeholder
@api_router.get("/companies")
async def list_companies():
    """List companies (placeholder)"""
    return {
        "message": "Company management endpoints will be implemented",
        "features": [
            "Company registration",
            "Multi-tenant isolation",
            "Greek business compliance",
            "AADE integration"
        ]
    }

# TODO: Add more routers
# from app.api.v1.endpoints import auth, customers, invoices, aade
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
# api_router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
# api_router.include_router(aade.router, prefix="/aade", tags=["aade"]) 