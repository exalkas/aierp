"""
JWT Token Utilities for Authentication Service
Handles token generation, validation, refresh, and company context
"""

import jwt
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from uuid import UUID
import logging

from config import settings
from models import User, Company

logger = logging.getLogger(__name__)


class JWTManager:
    """JWT token management class"""
    
    def __init__(self):
        # Require JWT_SECRET_KEY from environment - no fallbacks
        if not settings.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set in environment variables")
        
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(
        self, 
        user: User, 
        company: Company,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token with user and company context
        """
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            # Standard JWT claims
            "sub": str(user.id),  # Subject (user ID)
            "iat": datetime.now(timezone.utc),  # Issued at
            "exp": expire,  # Expiration
            "jti": secrets.token_urlsafe(16),  # JWT ID (unique identifier)
            
            # User information
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            
            # Company context (essential for multi-tenant)
            "company_id": str(company.id),
            "company_name": company.name,
            "company_afm": company.afm,
            "company_active": company.is_active,
            
            # Permissions
            "permissions": user.get_role_permissions(),
            
            # Default localization
            "language": "el",
            "timezone": "Europe/Athens",
            
            # Token type
            "token_type": "access"
        }
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Access token created for user {user.username} ({user.email})")
            return token
        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise
    
    def create_refresh_token(
        self, 
        user: User,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT refresh token (minimal payload for security)
        """
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        
        payload = {
            # Standard JWT claims
            "sub": str(user.id),
            "iat": datetime.now(timezone.utc),
            "exp": expire,
            "jti": secrets.token_urlsafe(16),
            
            # Minimal information for refresh
            "user_id": str(user.id),
            "company_id": str(user.company_id),
            "token_type": "refresh"
        }
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Refresh token created for user {user.username}")
            return token
        except Exception as e:
            logger.error(f"Failed to create refresh token: {e}")
            raise
    
    def create_password_reset_token(self, user: User) -> str:
        """
        Create JWT token for password reset (short-lived)
        """
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.PASSWORD_RESET_EXPIRE_HOURS)
        
        payload = {
            "sub": str(user.id),
            "iat": datetime.now(timezone.utc),
            "exp": expire,
            "jti": secrets.token_urlsafe(16),
            "user_id": str(user.id),
            "email": user.email,
            "token_type": "password_reset"
        }
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Password reset token created for user {user.email}")
            return token
        except Exception as e:
            logger.error(f"Failed to create password reset token: {e}")
            raise
    
    def create_email_verification_token(self, user: User) -> str:
        """
        Create JWT token for email verification
        """
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
        
        payload = {
            "sub": str(user.id),
            "iat": datetime.now(timezone.utc),
            "exp": expire,
            "jti": secrets.token_urlsafe(16),
            "user_id": str(user.id),
            "email": user.email,
            "token_type": "email_verification"
        }
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Email verification token created for user {user.email}")
            return token
        except Exception as e:
            logger.error(f"Failed to create email verification token: {e}")
            raise
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token
        """
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={"verify_exp": True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            raise ValueError("Invalid token")
        except Exception as e:
            logger.error(f"Token decode error: {e}")
            raise ValueError("Token decode failed")
    
    def validate_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate access token and return payload
        """
        try:
            payload = self.decode_token(token)
            
            # Verify token type
            if payload.get("token_type") != "access":
                logger.warning("Invalid token type for access token")
                return None
            
            # Verify required fields
            required_fields = ["user_id", "company_id", "username", "email", "role"]
            for field in required_fields:
                if field not in payload:
                    logger.warning(f"Missing required field in token: {field}")
                    return None
            
            return payload
        except Exception as e:
            logger.error(f"Access token validation failed: {e}")
            return None
    
    def validate_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate refresh token and return payload
        """
        try:
            payload = self.decode_token(token)
            
            # Verify token type
            if payload.get("token_type") != "refresh":
                logger.warning("Invalid token type for refresh token")
                return None
            
            # Verify required fields
            required_fields = ["user_id", "company_id"]
            for field in required_fields:
                if field not in payload:
                    logger.warning(f"Missing required field in refresh token: {field}")
                    return None
            
            return payload
        except Exception as e:
            logger.error(f"Refresh token validation failed: {e}")
            return None
    
    def validate_password_reset_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate password reset token and return payload
        """
        try:
            payload = self.decode_token(token)
            
            # Verify token type
            if payload.get("token_type") != "password_reset":
                logger.warning("Invalid token type for password reset token")
                return None
            
            # Verify required fields
            required_fields = ["user_id", "email"]
            for field in required_fields:
                if field not in payload:
                    logger.warning(f"Missing required field in password reset token: {field}")
                    return None
            
            return payload
        except Exception as e:
            logger.error(f"Password reset token validation failed: {e}")
            return None
    
    def validate_email_verification_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate email verification token and return payload
        """
        try:
            payload = self.decode_token(token)
            
            # Verify token type
            if payload.get("token_type") != "email_verification":
                logger.warning("Invalid token type for email verification token")
                return None
            
            # Verify required fields
            required_fields = ["user_id", "email"]
            for field in required_fields:
                if field not in payload:
                    logger.warning(f"Missing required field in email verification token: {field}")
                    return None
            
            return payload
        except Exception as e:
            logger.error(f"Email verification token validation failed: {e}")
            return None
    
    def extract_user_id(self, token: str) -> Optional[str]:
        """
        Extract user ID from token without full validation
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": False}  # Don't verify expiration
            )
            return payload.get("user_id")
        except Exception as e:
            logger.error(f"Failed to extract user ID from token: {e}")
            return None
    
    def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if token is blacklisted (placeholder for future implementation)
        Could be implemented with Redis or database storage
        """
        # TODO: Implement token blacklisting
        return False


# Global JWT manager instance
jwt_manager = JWTManager() 