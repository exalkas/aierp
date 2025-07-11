"""
Greek ERP/CRM Authentication Service
JWT authentication with company isolation and Greek business support
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Greek ERP/CRM Authentication Service...")
    yield
    logger.info("Shutting down Authentication Service...")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM Authentication Service",
    description="JWT authentication with company isolation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Greek ERP/CRM Authentication Service",
        "endpoints": {
            "health": "/health",
            "login": "/auth/login",
            "register": "/auth/register",
            "validate": "/auth/validate"
        }
    }


@app.post("/auth/login")
async def login():
    """User login endpoint (placeholder)"""
    return {
        "message": "Login endpoint to be implemented",
        "features": [
            "JWT token generation",
            "Company context inclusion",
            "Multi-factor authentication",
            "Greek business user support"
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    ) 