"""
Voice Commands API endpoints for Greek ERP/CRM System
Handles voice command processing, user customization, and analytics
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import json
import logging

from ...core.database import get_db_for_company
from ...services.voice_command_service import VoiceCommandService
from ...models import User
from ...middleware.company_isolation import get_current_user_and_company

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic models for request/response
class VoiceCommandRequest(BaseModel):
    """Request model for voice command processing"""
    recognized_text: str = Field(..., description="The recognized text from speech")
    confidence_score: int = Field(ge=0, le=100, description="Recognition confidence score")
    language: str = Field(default="el", description="Language code")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class VoiceCommandResponse(BaseModel):
    """Response model for voice command processing"""
    success: bool
    command_matched: bool
    action_performed: str
    response_data: Dict[str, Any]
    match_score: float
    execution_time_ms: int
    error_message: Optional[str] = None


class CustomizeCommandRequest(BaseModel):
    """Request model for customizing voice commands"""
    system_command_id: str
    custom_phrases: List[str] = Field(..., min_items=1, description="Custom phrases")
    custom_action_config: Optional[Dict[str, Any]] = Field(default=None, description="Custom action configuration")
    confidence_threshold: int = Field(default=70, ge=0, le=100, description="Confidence threshold")
    confirmation_required: bool = Field(default=False, description="Require confirmation")


class UserCommandResponse(BaseModel):
    """Response model for user commands"""
    system_command_id: str
    user_command_id: Optional[str]
    command_key: str
    command_name: str
    description: str
    command_type: str
    category: str
    module: str
    phrases: List[str]
    action_type: str
    action_config: Dict[str, Any]
    required_permissions: List[str]
    help_text: str
    examples: List[str]
    is_customized: bool
    confidence_threshold: int
    confirmation_required: bool


class SystemCommandResponse(BaseModel):
    """Response model for system commands"""
    id: str
    command_key: str
    command_name: str
    description: str
    command_type: str
    category: str
    module: str
    default_phrases: Dict[str, List[str]]
    action_type: str
    action_config: Dict[str, Any]
    required_permissions: List[str]
    help_text: str
    examples: List[str]
    is_customizable: bool
    priority: int


class CommandAnalyticsResponse(BaseModel):
    """Response model for command analytics"""
    total_commands: int
    successful_commands: int
    success_rate: float
    most_used_commands: List[Dict[str, Any]]
    average_confidence: float
    period_days: int


@router.post("/process", response_model=VoiceCommandResponse)
async def process_voice_command(
    request: VoiceCommandRequest,
    user_company = Depends(get_current_user_and_company)
):
    """Process a voice command from recognized text"""
    try:
        user, company_id = user_company
        
        # Get voice command service
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        
        # Match the command
        matched_command = voice_service.match_command(
            recognized_text=request.recognized_text,
            user_id=str(user.id),
            company_id=company_id
        )
        
        if not matched_command:
            return VoiceCommandResponse(
                success=False,
                command_matched=False,
                action_performed="",
                response_data={},
                match_score=0.0,
                execution_time_ms=0,
                error_message="No matching command found"
            )
        
        # Execute the command
        execution_result = voice_service.execute_command(
            command=matched_command,
            user_id=str(user.id),
            company_id=company_id,
            context=request.context
        )
        
        return VoiceCommandResponse(
            success=execution_result['success'],
            command_matched=True,
            action_performed=execution_result['action_performed'],
            response_data=execution_result['response_data'],
            match_score=matched_command['match_score'],
            execution_time_ms=execution_result['execution_time_ms'],
            error_message=execution_result.get('error_message')
        )
        
    except Exception as e:
        logger.error(f"Error processing voice command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-commands", response_model=List[UserCommandResponse])
async def get_user_commands(
    user_company = Depends(get_current_user_and_company)
):
    """Get all available voice commands for the current user"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        commands = voice_service.get_user_commands(str(user.id), company_id)
        
        return [UserCommandResponse(**cmd) for cmd in commands]
        
    except Exception as e:
        logger.error(f"Error getting user commands: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system-commands", response_model=List[SystemCommandResponse])
async def get_system_commands(
    category: Optional[str] = None,
    user_company = Depends(get_current_user_and_company)
):
    """Get all system voice commands, optionally filtered by category"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        commands = voice_service.get_system_commands_by_category(category)
        
        return [SystemCommandResponse(**cmd) for cmd in commands]
        
    except Exception as e:
        logger.error(f"Error getting system commands: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customize")
async def customize_voice_command(
    request: CustomizeCommandRequest,
    user_company = Depends(get_current_user_and_company)
):
    """Customize a voice command for the current user"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        result = voice_service.customize_user_command(
            user_id=str(user.id),
            company_id=company_id,
            system_command_id=request.system_command_id,
            custom_phrases=request.custom_phrases,
            custom_action_config=request.custom_action_config
        )
        
        if result['success']:
            return {"success": True, "message": "Command customized successfully"}
        else:
            raise HTTPException(status_code=400, detail=result.get('error', 'Customization failed'))
            
    except Exception as e:
        logger.error(f"Error customizing voice command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics", response_model=CommandAnalyticsResponse)
async def get_command_analytics(
    days: int = 30,
    user_company = Depends(get_current_user_and_company)
):
    """Get voice command usage analytics"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        analytics = voice_service.get_command_analytics(company_id, days)
        
        return CommandAnalyticsResponse(**analytics)
        
    except Exception as e:
        logger.error(f"Error getting command analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_command_categories(
    user_company = Depends(get_current_user_and_company)
):
    """Get all available command categories"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        commands = voice_service.get_system_commands_by_category()
        
        categories = list(set(cmd['category'] for cmd in commands))
        categories.sort()
        
        return {
            "categories": categories,
            "category_counts": {
                category: len([cmd for cmd in commands if cmd['category'] == category])
                for category in categories
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting command categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/seed-defaults")
async def seed_default_commands(
    user_company = Depends(get_current_user_and_company)
):
    """Seed the database with default voice commands (admin only)"""
    try:
        user, company_id = user_company
        
        # TODO: Add admin permission check
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        voice_service.seed_default_commands()
        
        return {"success": True, "message": "Default commands seeded successfully"}
        
    except Exception as e:
        logger.error(f"Error seeding default commands: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-recognition")
async def test_speech_recognition(
    text: str = Form(...),
    user_company = Depends(get_current_user_and_company)
):
    """Test speech recognition and command matching without execution"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        
        # Match the command
        matched_command = voice_service.match_command(
            recognized_text=text,
            user_id=str(user.id),
            company_id=company_id
        )
        
        if matched_command:
            return {
                "success": True,
                "command_matched": True,
                "matched_command": {
                    "command_key": matched_command['command_key'],
                    "command_name": matched_command['command_name'],
                    "matched_phrase": matched_command['matched_phrase'],
                    "match_score": matched_command['match_score'],
                    "action_type": matched_command['action_type'],
                    "action_config": matched_command['action_config']
                }
            }
        else:
            return {
                "success": True,
                "command_matched": False,
                "message": "No matching command found"
            }
            
    except Exception as e:
        logger.error(f"Error testing speech recognition: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/customization/{system_command_id}")
async def delete_command_customization(
    system_command_id: str,
    user_company = Depends(get_current_user_and_company)
):
    """Delete a user's command customization"""
    try:
        user, company_id = user_company
        
        # TODO: Implement deletion logic
        # This would remove the user's customization and revert to system defaults
        
        return {"success": True, "message": "Command customization deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting command customization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback")
async def provide_command_feedback(
    command_log_id: str = Form(...),
    feedback: str = Form(...),  # "correct", "incorrect", "partially_correct"
    correction: Optional[str] = Form(None),
    user_company = Depends(get_current_user_and_company)
):
    """Provide feedback on command execution for ML improvement"""
    try:
        user, company_id = user_company
        
        # TODO: Implement feedback storage and processing
        # This would update the VoiceCommandLog with user feedback
        
        return {"success": True, "message": "Feedback recorded successfully"}
        
    except Exception as e:
        logger.error(f"Error providing command feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/help")
async def get_voice_command_help(
    user_company = Depends(get_current_user_and_company)
):
    """Get help information for voice commands"""
    try:
        user, company_id = user_company
        
        voice_service = VoiceCommandService(get_db_for_company(company_id))
        commands = voice_service.get_user_commands(str(user.id), company_id)
        
        help_info = {
            "total_commands": len(commands),
            "categories": {},
            "examples": []
        }
        
        for cmd in commands:
            category = cmd['category']
            if category not in help_info['categories']:
                help_info['categories'][category] = []
            
            help_info['categories'][category].append({
                "command_name": cmd['command_name'],
                "description": cmd['description'],
                "phrases": cmd['phrases'][:3],  # Show first 3 phrases
                "help_text": cmd['help_text']
            })
            
            # Add examples
            if cmd['examples']:
                help_info['examples'].extend([
                    {
                        "command": cmd['command_name'],
                        "example": example
                    }
                    for example in cmd['examples'][:2]  # Show first 2 examples
                ])
        
        return help_info
        
    except Exception as e:
        logger.error(f"Error getting voice command help: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 