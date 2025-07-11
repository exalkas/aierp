"""
Greek ERP/CRM AI Support Service
Intelligent customer support with Greek language understanding
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
    logger.info("Starting Greek ERP/CRM AI Support Service...")
    yield
    logger.info("Shutting down AI Support Service...")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM AI Support Service",
    description="Intelligent customer support with Greek language understanding",
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
        "service": "ai-support-service",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Greek ERP/CRM AI Support Service",
        "capabilities": [
            "Greek language chatbot",
            "ERP/CRM knowledge base",
            "Intelligent ticket routing",
            "Greek business context understanding",
            "Multi-language support"
        ]
    }


@app.post("/chat/message")
async def process_chat_message(data: dict):
    """Process chat message (placeholder)"""
    message = data.get("message", "")
    language = data.get("language", "el")  # Default to Greek
    
    return {
        "response": "AI response to be implemented",
        "message": message,
        "language": language,
        "confidence": 0.0,
        "suggestions": []
    }


@app.post("/support/analyze-ticket")
async def analyze_support_ticket(data: dict):
    """Analyze support ticket and suggest routing"""
    ticket_content = data.get("content", "")
    
    return {
        "analysis": "Ticket analysis to be implemented",
        "suggested_department": "general",
        "priority": "medium",
        "tags": [],
        "sentiment": "neutral"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=True
    ) 