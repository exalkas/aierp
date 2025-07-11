"""
Greek ERP/CRM File Storage Service
Secure file management with Greek business document support
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
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
    logger.info("Starting Greek ERP/CRM File Storage Service...")
    yield
    logger.info("Shutting down File Storage Service...")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM File Storage Service",
    description="Secure file management with Greek business document support",
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
        "service": "files-service",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Greek ERP/CRM File Storage Service",
        "features": [
            "Secure file upload/download",
            "Greek document processing",
            "PDF generation for invoices",
            "Image processing",
            "Company-isolated storage"
        ]
    }


@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """File upload endpoint (placeholder)"""
    return {
        "message": f"File upload endpoint - received {file.filename}",
        "size": file.size if hasattr(file, 'size') else "unknown",
        "content_type": file.content_type
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    ) 