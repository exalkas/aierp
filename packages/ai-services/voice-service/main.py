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
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = "el-GR"
):
    """Transcribe audio to text with Greek language support"""
    try:
        import speech_recognition as sr
        import io
        from pydub import AudioSegment
        import tempfile
        import os
        
        # Read audio file
        audio_bytes = await audio.read()
        
        # Convert to wav format if needed
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Create temporary wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            audio_segment.export(temp_file.name, format="wav")
            temp_path = temp_file.name
        
        try:
            # Initialize speech recognition
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_path) as source:
                # Record the audio data
                audio_data = recognizer.record(source)
                
                # Try Google Speech Recognition with Greek support
                try:
                    text = recognizer.recognize_google(
                        audio_data, 
                        language=language
                    )
                    confidence = 85  # Google doesn't provide confidence, use default
                except sr.UnknownValueError:
                    # Fallback to Whisper if available
                    try:
                        text = recognizer.recognize_whisper(audio_data, language="el")
                        confidence = 80
                    except:
                        return {
                            "success": False,
                            "error": "Could not understand audio",
                            "transcription": "",
                            "confidence": 0
                        }
                except sr.RequestError as e:
                    return {
                        "success": False,
                        "error": f"Speech recognition service error: {e}",
                        "transcription": "",
                        "confidence": 0
                    }
            
            return {
                "success": True,
                "transcription": text,
                "confidence": confidence,
                "language": language,
                "duration": len(audio_segment) / 1000.0  # in seconds
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logger.error(f"Error in audio transcription: {e}")
        return {
            "success": False,
            "error": str(e),
            "transcription": "",
            "confidence": 0
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


@app.post("/voice/process-command")
async def process_voice_command(
    audio: UploadFile = File(...),
    language: str = "el-GR",
    main_api_url: str = "http://localhost:8000"
):
    """Complete voice command processing: audio -> text -> command execution"""
    import httpx
    
    try:
        # Step 1: Transcribe audio to text
        transcription_result = await transcribe_audio(audio, language)
        
        if not transcription_result["success"]:
            return transcription_result
        
        recognized_text = transcription_result["transcription"]
        confidence = transcription_result["confidence"]
        
        # Step 2: Send to main API for command processing
        async with httpx.AsyncClient() as client:
            command_response = await client.post(
                f"{main_api_url}/api/v1/voice/process",
                json={
                    "recognized_text": recognized_text,
                    "confidence_score": confidence,
                    "language": "el",
                    "context": {
                        "voice_service": True,
                        "transcription_confidence": confidence
                    }
                },
                headers={"Content-Type": "application/json"}
            )
            
            if command_response.status_code == 200:
                command_result = command_response.json()
                
                return {
                    "success": True,
                    "transcription": {
                        "text": recognized_text,
                        "confidence": confidence,
                        "language": language
                    },
                    "command": command_result
                }
            else:
                return {
                    "success": False,
                    "transcription": {
                        "text": recognized_text,
                        "confidence": confidence,
                        "language": language
                    },
                    "error": f"Command processing failed: {command_response.status_code}"
                }
                
    except Exception as e:
        logger.error(f"Error in voice command processing: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/voice/test-text")
async def test_text_command(
    data: dict,
    main_api_url: str = "http://localhost:8000"
):
    """Test command processing with direct text input"""
    import httpx
    
    try:
        text = data.get("text", "")
        language = data.get("language", "el")
        
        if not text:
            return {"success": False, "error": "No text provided"}
        
        # Send to main API for command processing
        async with httpx.AsyncClient() as client:
            command_response = await client.post(
                f"{main_api_url}/api/v1/voice/process",
                json={
                    "recognized_text": text,
                    "confidence_score": 95,  # High confidence for text input
                    "language": language,
                    "context": {
                        "voice_service": True,
                        "test_mode": True
                    }
                },
                headers={"Content-Type": "application/json"}
            )
            
            if command_response.status_code == 200:
                command_result = command_response.json()
                
                return {
                    "success": True,
                    "input_text": text,
                    "command": command_result
                }
            else:
                return {
                    "success": False,
                    "input_text": text,
                    "error": f"Command processing failed: {command_response.status_code}"
                }
                
    except Exception as e:
        logger.error(f"Error in text command testing: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=True
    ) 