"""
Greek ERP/CRM API Service
Main FastAPI application with Greek business compliance features
"""

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
from typing import Optional
import uvicorn

from app.core.config import settings
from app.core.database import engine, create_tables
from app.core.logging import api_logger
from app.api.v1.router import api_router
from app.middleware.company_isolation import CompanyIsolationMiddleware
from app.middleware.audit_logging import AuditLoggingMiddleware
from app.middleware.greek_compliance import GreekComplianceMiddleware
from app.middleware.error_handling import ErrorHandlingMiddleware
from app.middleware.request_logging import (
    RequestLoggingMiddleware, 
    PerformanceLoggingMiddleware, 
    SecurityLoggingMiddleware
)

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    api_logger.info("Starting Greek ERP/CRM API Service...", {
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    })
    
    # Create database tables
    await create_tables()
    
    api_logger.info("API Service started successfully", {
        "cors_origins": settings.CORS_ORIGINS,
        "database_url": settings.DATABASE_URL.split('@')[1] if '@' in str(settings.DATABASE_URL) else "configured"
    })
    yield
    
    api_logger.info("Shutting down Greek ERP/CRM API Service...")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM API",
    description="Comprehensive Greek business management system with AADE compliance",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Add middleware (order matters!)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for Greek business requirements - TESTING ONE BY ONE
app.add_middleware(GreekComplianceMiddleware)  # 🔥 TESTING THE SUSPECTED CULPRIT
app.add_middleware(AuditLoggingMiddleware)  # ✅ CONFIRMED WORKING
app.add_middleware(CompanyIsolationMiddleware)  # ✅ CONFIRMED WORKING

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "greek-erp-api",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Greek ERP/CRM API Service",
        "documentation": "/api/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    ) 