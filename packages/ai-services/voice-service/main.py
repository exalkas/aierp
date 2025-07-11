"""
Greek ERP/CRM Voice AI Service
Voice recognition and synthesis with Greek language support
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
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
    logger.info("Starting Greek ERP/CRM Voice AI Service...")
    yield
    logger.info("Shutting down Voice AI Service...")


# Create FastAPI application
app = FastAPI(
    title="Greek ERP/CRM Voice AI Service",
    description="Voice recognition and synthesis with Greek language support",
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
        "service": "voice-ai-service",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Greek ERP/CRM Voice AI Service",
        "features": [
            "Greek speech recognition",
            "Text-to-speech synthesis",
            "Voice commands for ERP operations",
            "Multi-language support (Greek/English)"
        ]
    }


@app.post("/voice/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe audio to text (placeholder)"""
    return {
        "message": f"Audio transcription - received {audio.filename}",
        "size": audio.size if hasattr(audio, 'size') else "unknown",
        "content_type": audio.content_type,
        "transcription": "Transcription to be implemented with Greek language support"
    }


@app.post("/voice/synthesize")
async def synthesize_speech(data: dict):
    """Convert text to speech (placeholder)"""
    text = data.get("text", "")
    language = data.get("language", "el-GR")  # Default to Greek
    
    return {
        "message": "Text-to-speech synthesis",
        "text": text,
        "language": language,
        "status": "to_be_implemented"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=True
    ) 