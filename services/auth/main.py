"""
Greek ERP/CRM Authentication Service
Complete JWT authentication with company isolation and Greek business support
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from database import init_database, close_database
from auth_endpoints import router as auth_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Greek ERP/CRM Authentication Service...")
    
    # Initialize database connection
    if not await init_database():
        logger.error("Failed to initialize database connection")
        raise Exception("Database initialization failed")
    
    logger.info("✅ Authentication Service started successfully")
    yield
    
    # Cleanup
    await close_database()
    logger.info("Authentication Service shut down")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM Authentication Service",
    description="Complete JWT authentication with multi-tenant support and Greek business compliance",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or [
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Greek ERP/CRM Authentication Service",
        "version": "1.0.0",
        "status": "running",
        "features": {
            "authentication": [
                "JWT token generation and validation",
                "Access and refresh token support",
                "Multi-tenant company isolation",
                "Role-based access control"
            ],
            "password_management": [
                "Secure password hashing (bcrypt)",
                "Password reset via email",
                "Password strength validation",
                "Account lockout protection"
            ],
            "user_management": [
                "User registration with company setup",
                "Email verification",
                "Account status management",
                "Session management"
            ],
            "greek_business": [
                "AFM (Greek Tax Number) validation",
                "DOY (Tax Office) support", 
                "Greek localization (language/timezone)",
                "Greek company legal forms",
                "Greek address formatting"
            ],
            "security": [
                "Failed login attempt tracking",
                "Account lockout after failed attempts",
                "Secure token generation",
                "Email verification required",
                "Strong password requirements"
            ]
        },
        "endpoints": {
            "authentication": {
                "login": "POST /auth/login",
                "logout": "POST /auth/logout", 
                "refresh": "POST /auth/refresh",
                "validate": "POST /auth/validate",
                "me": "GET /auth/me"
            },
            "password_management": {
                "reset_request": "POST /auth/password/reset/request",
                "reset_confirm": "POST /auth/password/reset/confirm",
                "change": "POST /auth/password/change"
            },
            "registration": {
                "register": "POST /auth/register",
                "verify_email_request": "POST /auth/email/verification/request",
                "verify_email_confirm": "POST /auth/email/verification/confirm"
            },
            "system": {
                "health": "GET /auth/health",
                "docs": "GET /docs",
                "root": "GET /"
            }
        },
        "database": {
            "connected": True,
            "models": [
                "User (with Greek localization)",
                "Company (with AFM/DOY)",
                "Authentication tokens",
                "Session management"
            ]
        },
        "environment": settings.ENVIRONMENT,
        "cors_enabled": True,
        "documentation": {
            "openapi": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "greek-erp-auth",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "database_connected": True,
        "features_enabled": [
            "jwt_authentication",
            "password_management", 
            "user_registration",
            "email_verification",
            "greek_business_compliance",
            "multi_tenant_support"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.AUTH_SERVICE_PORT,
        reload=settings.ENVIRONMENT == "development"
    ) 