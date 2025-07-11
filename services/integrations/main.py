"""
Greek ERP/CRM Integrations Service
AADE integration and Greek business external service connections
"""

from fastapi import FastAPI, HTTPException
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
    logger.info("Starting Greek ERP/CRM Integrations Service...")
    yield
    logger.info("Shutting down Integrations Service...")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM Integrations Service",
    description="AADE integration and Greek business external services",
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
        "service": "integrations-service",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Greek ERP/CRM Integrations Service",
        "integrations": [
            "AADE MyDATA (Greek Tax Authority)",
            "Greek Banking APIs",
            "Greek Postal Services",
            "Payment Gateways",
            "SMS/Email providers"
        ]
    }


@app.post("/aade/submit-invoice")
async def submit_invoice_to_aade():
    """Submit invoice to AADE (placeholder)"""
    return {
        "message": "AADE invoice submission endpoint",
        "status": "pending_implementation",
        "features": [
            "XML invoice generation",
            "AADE API authentication",
            "QR code generation",
            "Status tracking"
        ]
    }


@app.get("/aade/status")
async def get_aade_status():
    """Get AADE connection status"""
    return {
        "connected": False,
        "environment": "sandbox",
        "last_sync": None,
        "message": "AADE integration to be implemented"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    ) 