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
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.middleware.company_isolation import CompanyIsolationMiddleware
from app.middleware.audit_logging import AuditLoggingMiddleware
from app.middleware.greek_compliance import GreekComplianceMiddleware

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Greek ERP/CRM API Service...")
    
    # Create database tables
    await create_tables()
    
    logger.info("API Service started successfully")
    yield
    
    logger.info("Shutting down Greek ERP/CRM API Service...")


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

# Custom middleware for Greek business requirements
app.add_middleware(GreekComplianceMiddleware)
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(CompanyIsolationMiddleware)

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