"""
Voice Command Service for Greek ERP/CRM System
Handles speech recognition, command matching, and action execution
"""

import logging
import re
import uuid
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from difflib import SequenceMatcher
import unicodedata

from ..models import (
    SystemVoiceCommand, UserVoiceCommand, VoiceCommandLog, 
    VoiceCommandTemplate, VoiceCommandType, VoiceCommandStatus, 
    VoiceActionType, DEFAULT_VOICE_COMMANDS, User
)
from ..core.database import get_db_for_company

logger = logging.getLogger(__name__)


class VoiceCommandService:
    """Service for handling voice commands and user customizations"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def normalize_greek_text(self, text: str) -> str:
        """Normalize Greek text for better matching"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove accents from Greek characters
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        # Replace common Greek variations
        replacements = {
            'ή': 'η', 'ί': 'ι', 'ό': 'ο', 'ύ': 'υ', 'ώ': 'ω',
            'ά': 'α', 'έ': 'ε', 'ές': 'ες', 'ός': 'ος',
            'κ': 'κ', 'γ': 'γ', 'χ': 'χ'  # Normalize similar sounding letters
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        
        # Normalize both texts
        norm_text1 = self.normalize_greek_text(text1)
        norm_text2 = self.normalize_greek_text(text2)
        
        # Calculate basic similarity
        similarity = SequenceMatcher(None, norm_text1, norm_text2).ratio()
        
        # Boost similarity for exact word matches
        words1 = set(norm_text1.split())
        words2 = set(norm_text2.split())
        
        if words1 and words2:
            word_match_ratio = len(words1 & words2) / len(words1 | words2)
            similarity = max(similarity, word_match_ratio)
        
        # Check for substring matches
        if norm_text1 in norm_text2 or norm_text2 in norm_text1:
            similarity = max(similarity, 0.8)
        
        return similarity
    
    def seed_default_commands(self) -> None:
        """Seed the database with default voice commands"""
        try:
            for cmd_data in DEFAULT_VOICE_COMMANDS:
                existing = self.db.query(SystemVoiceCommand).filter(
                    SystemVoiceCommand.command_key == cmd_data["command_key"]
                ).first()
                
                if not existing:
                    command = SystemVoiceCommand(
                        command_key=cmd_data["command_key"],
                        command_name=cmd_data["command_name"],
                        description=cmd_data["description"],
                        command_type=cmd_data["command_type"],
                        category=cmd_data["category"],
                        module=cmd_data["module"],
                        default_phrases=cmd_data["default_phrases"],
                        action_type=cmd_data["action_type"],
                        action_config=cmd_data["action_config"],
                        required_permissions=cmd_data.get("required_permissions", []),
                        help_text=cmd_data.get("help_text", ""),
                        examples=cmd_data.get("examples", [])
                    )
                    self.db.add(command)
            
            self.db.commit()
            logger.info(f"Seeded {len(DEFAULT_VOICE_COMMANDS)} default voice commands")
            
        except Exception as e:
            logger.error(f"Failed to seed default voice commands: {e}")
            self.db.rollback()
    
    def get_user_commands(self, user_id: str, company_id: str) -> List[Dict[str, Any]]:
        """Get all available commands for a user"""
        try:
            # Get system commands
            system_commands = self.db.query(SystemVoiceCommand).filter(
                SystemVoiceCommand.status == VoiceCommandStatus.ACTIVE
            ).all()
            
            # Get user customizations
            user_customizations = self.db.query(UserVoiceCommand).filter(
                and_(
                    UserVoiceCommand.user_id == user_id,
                    UserVoiceCommand.company_id == company_id,
                    UserVoiceCommand.is_enabled == True
                )
            ).all()
            
            # Create lookup for user customizations
            user_custom_lookup = {uc.system_command_id: uc for uc in user_customizations}
            
            commands = []
            for sys_cmd in system_commands:
                user_custom = user_custom_lookup.get(sys_cmd.id)
                
                # Build phrases list
                phrases = []
                if user_custom:
                    phrases.extend(user_custom.custom_phrases)
                    if user_custom.use_system_phrases:
                        phrases.extend(sys_cmd.default_phrases.get('el', []))
                        phrases.extend(sys_cmd.default_phrases.get('en', []))
                else:
                    phrases.extend(sys_cmd.default_phrases.get('el', []))
                    phrases.extend(sys_cmd.default_phrases.get('en', []))
                
                # Build action configuration
                action_config = sys_cmd.action_config
                if user_custom and user_custom.custom_action_config:
                    action_config = user_custom.custom_action_config
                
                commands.append({
                    'system_command_id': str(sys_cmd.id),
                    'user_command_id': str(user_custom.id) if user_custom else None,
                    'command_key': sys_cmd.command_key,
                    'command_name': sys_cmd.command_name,
                    'description': sys_cmd.description,
                    'command_type': sys_cmd.command_type.value,
                    'category': sys_cmd.category,
                    'module': sys_cmd.module,
                    'phrases': phrases,
                    'action_type': sys_cmd.action_type.value,
                    'action_config': action_config,
                    'required_permissions': sys_cmd.required_permissions,
                    'help_text': sys_cmd.help_text,
                    'examples': sys_cmd.examples,
                    'is_customized': user_custom is not None,
                    'confidence_threshold': user_custom.confidence_threshold if user_custom else 70,
                    'confirmation_required': user_custom.confirmation_required if user_custom else False
                })
            
            return commands
            
        except Exception as e:
            logger.error(f"Failed to get user commands: {e}")
            return []
    
    def match_command(self, recognized_text: str, user_id: str, company_id: str) -> Optional[Dict[str, Any]]:
        """Match recognized text to a voice command"""
        try:
            user_commands = self.get_user_commands(user_id, company_id)
            
            best_match = None
            best_score = 0.0
            
            for command in user_commands:
                for phrase in command['phrases']:
                    similarity = self.calculate_similarity(recognized_text, phrase)
                    
                    if similarity > best_score and similarity >= (command['confidence_threshold'] / 100):
                        best_score = similarity
                        best_match = {
                            **command,
                            'matched_phrase': phrase,
                            'match_score': similarity * 100,
                            'original_text': recognized_text
                        }
            
            return best_match
            
        except Exception as e:
            logger.error(f"Failed to match command: {e}")
            return None
    
    def execute_command(self, command: Dict[str, Any], user_id: str, company_id: str, 
                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a matched voice command"""
        try:
            execution_result = {
                'success': False,
                'action_performed': '',
                'error_message': '',
                'response_data': {},
                'execution_time_ms': 0
            }
            
            start_time = datetime.now()
            
            # Check permissions
            # TODO: Implement permission checking
            
            action_type = command['action_type']
            action_config = command['action_config']
            
            if action_type == VoiceActionType.NAVIGATE.value:
                execution_result.update({
                    'success': True,
                    'action_performed': 'navigate',
                    'response_data': {
                        'action': 'navigate',
                        'url': action_config.get('url', '/'),
                        'target': action_config.get('target', '_self'),
                        'focus_search': action_config.get('focus_search', False)
                    }
                })
                
            elif action_type == VoiceActionType.OPEN_MODAL.value:
                execution_result.update({
                    'success': True,
                    'action_performed': 'open_modal',
                    'response_data': {
                        'action': 'open_modal',
                        'modal_id': action_config.get('modal_id', ''),
                        'modal_props': action_config.get('modal_props', {})
                    }
                })
                
            elif action_type == VoiceActionType.EXECUTE_FUNCTION.value:
                execution_result.update({
                    'success': True,
                    'action_performed': 'execute_function',
                    'response_data': {
                        'action': 'execute_function',
                        'function': action_config.get('function', ''),
                        'params': action_config.get('params', {})
                    }
                })
                
            elif action_type == VoiceActionType.API_CALL.value:
                # TODO: Implement API call execution
                execution_result.update({
                    'success': True,
                    'action_performed': 'api_call',
                    'response_data': {
                        'action': 'api_call',
                        'endpoint': action_config.get('endpoint', ''),
                        'method': action_config.get('method', 'GET'),
                        'params': action_config.get('params', {})
                    }
                })
                
            else:
                execution_result.update({
                    'success': False,
                    'error_message': f'Unsupported action type: {action_type}'
                })
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            execution_result['execution_time_ms'] = int(execution_time)
            
            # Log the command execution
            self.log_command_execution(
                user_id=user_id,
                company_id=company_id,
                command=command,
                execution_result=execution_result,
                context=context
            )
            
            # Update usage statistics
            if command.get('user_command_id'):
                self.update_usage_statistics(command['user_command_id'], execution_result['success'])
            
            return execution_result
            
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return {
                'success': False,
                'action_performed': '',
                'error_message': str(e),
                'response_data': {},
                'execution_time_ms': 0
            }
    
    def log_command_execution(self, user_id: str, company_id: str, command: Dict[str, Any], 
                            execution_result: Dict[str, Any], context: Dict[str, Any] = None):
        """Log voice command execution for analytics"""
        try:
            log_entry = VoiceCommandLog(
                user_id=user_id,
                company_id=company_id,
                session_id=context.get('session_id', '') if context else '',
                device_info=context.get('device_info', {}) if context else {},
                original_text=command.get('original_text', ''),
                recognized_text=command.get('original_text', ''),
                confidence_score=int(command.get('match_score', 0)),
                language_detected=context.get('language', 'el') if context else 'el',
                matched_command_id=command.get('system_command_id'),
                user_command_id=command.get('user_command_id'),
                match_score=int(command.get('match_score', 0)),
                executed_successfully=execution_result['success'],
                execution_time_ms=execution_result['execution_time_ms'],
                action_performed=execution_result['action_performed'],
                error_message=execution_result.get('error_message', ''),
                page_url=context.get('page_url', '') if context else '',
                page_context=context.get('page_context', {}) if context else {}
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Failed to log command execution: {e}")
            self.db.rollback()
    
    def update_usage_statistics(self, user_command_id: str, success: bool):
        """Update usage statistics for a user command"""
        try:
            user_command = self.db.query(UserVoiceCommand).filter(
                UserVoiceCommand.id == user_command_id
            ).first()
            
            if user_command:
                user_command.usage_count += 1
                user_command.last_used = datetime.now()
                
                if success:
                    # Improve accuracy score
                    user_command.accuracy_score = min(100, user_command.accuracy_score + 1)
                else:
                    # Decrease accuracy score
                    user_command.accuracy_score = max(0, user_command.accuracy_score - 2)
                
                self.db.commit()
                
        except Exception as e:
            logger.error(f"Failed to update usage statistics: {e}")
            self.db.rollback()
    
    def customize_user_command(self, user_id: str, company_id: str, 
                             system_command_id: str, custom_phrases: List[str],
                             custom_action_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create or update user command customization"""
        try:
            # Check if customization already exists
            existing = self.db.query(UserVoiceCommand).filter(
                and_(
                    UserVoiceCommand.user_id == user_id,
                    UserVoiceCommand.company_id == company_id,
                    UserVoiceCommand.system_command_id == system_command_id
                )
            ).first()
            
            if existing:
                # Update existing customization
                existing.custom_phrases = custom_phrases
                if custom_action_config:
                    existing.custom_action_config = custom_action_config
                existing.updated_at = datetime.now()
                
                self.db.commit()
                return {'success': True, 'user_command_id': str(existing.id)}
            else:
                # Create new customization
                user_command = UserVoiceCommand(
                    user_id=user_id,
                    company_id=company_id,
                    system_command_id=system_command_id,
                    custom_phrases=custom_phrases,
                    custom_action_config=custom_action_config or {}
                )
                
                self.db.add(user_command)
                self.db.commit()
                
                return {'success': True, 'user_command_id': str(user_command.id)}
                
        except Exception as e:
            logger.error(f"Failed to customize user command: {e}")
            self.db.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_command_analytics(self, company_id: str, days: int = 30) -> Dict[str, Any]:
        """Get voice command usage analytics"""
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            # Total commands executed
            total_commands = self.db.query(func.count(VoiceCommandLog.id)).filter(
                and_(
                    VoiceCommandLog.company_id == company_id,
                    VoiceCommandLog.created_at >= since_date
                )
            ).scalar()
            
            # Success rate
            successful_commands = self.db.query(func.count(VoiceCommandLog.id)).filter(
                and_(
                    VoiceCommandLog.company_id == company_id,
                    VoiceCommandLog.created_at >= since_date,
                    VoiceCommandLog.executed_successfully == True
                )
            ).scalar()
            
            success_rate = (successful_commands / total_commands * 100) if total_commands > 0 else 0
            
            # Most used commands
            most_used = self.db.query(
                SystemVoiceCommand.command_name,
                func.count(VoiceCommandLog.id).label('usage_count')
            ).join(
                VoiceCommandLog, SystemVoiceCommand.id == VoiceCommandLog.matched_command_id
            ).filter(
                and_(
                    VoiceCommandLog.company_id == company_id,
                    VoiceCommandLog.created_at >= since_date
                )
            ).group_by(SystemVoiceCommand.command_name).order_by(
                func.count(VoiceCommandLog.id).desc()
            ).limit(10).all()
            
            # Average confidence score
            avg_confidence = self.db.query(func.avg(VoiceCommandLog.confidence_score)).filter(
                and_(
                    VoiceCommandLog.company_id == company_id,
                    VoiceCommandLog.created_at >= since_date
                )
            ).scalar()
            
            return {
                'total_commands': total_commands,
                'successful_commands': successful_commands,
                'success_rate': round(success_rate, 2),
                'most_used_commands': [
                    {'command': cmd[0], 'usage_count': cmd[1]} 
                    for cmd in most_used
                ],
                'average_confidence': round(avg_confidence or 0, 2),
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Failed to get command analytics: {e}")
            return {
                'total_commands': 0,
                'successful_commands': 0,
                'success_rate': 0.0,
                'most_used_commands': [],
                'average_confidence': 0.0,
                'period_days': days
            }
    
    def get_system_commands_by_category(self, category: str = None) -> List[Dict[str, Any]]:
        """Get system commands, optionally filtered by category"""
        try:
            query = self.db.query(SystemVoiceCommand).filter(
                SystemVoiceCommand.status == VoiceCommandStatus.ACTIVE
            )
            
            if category:
                query = query.filter(SystemVoiceCommand.category == category)
            
            commands = query.all()
            
            return [
                {
                    'id': str(cmd.id),
                    'command_key': cmd.command_key,
                    'command_name': cmd.command_name,
                    'description': cmd.description,
                    'command_type': cmd.command_type.value,
                    'category': cmd.category,
                    'module': cmd.module,
                    'default_phrases': cmd.default_phrases,
                    'action_type': cmd.action_type.value,
                    'action_config': cmd.action_config,
                    'required_permissions': cmd.required_permissions,
                    'help_text': cmd.help_text,
                    'examples': cmd.examples,
                    'is_customizable': cmd.is_customizable,
                    'priority': cmd.priority
                }
                for cmd in commands
            ]
            
        except Exception as e:
            logger.error(f"Failed to get system commands: {e}")
            return []


def get_voice_command_service(company_id: str) -> VoiceCommandService:
    """Get voice command service for a specific company"""
    with get_db_for_company(company_id) as db:
        return VoiceCommandService(db) 