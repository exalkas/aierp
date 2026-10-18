"""
Pydantic schemas for Authentication Service
Request and response models for authentication endpoints
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    remember_me: bool = Field(False, description="Remember me for extended session")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "",
                "remember_me": False
            }
        }


class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    
    # User information
    user: Dict[str, Any] = Field(..., description="User information")
    company: Dict[str, Any] = Field(..., description="Company information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "",
                "refresh_token": "",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "john.doe",
                    "email": "john@example.com",
                    "full_name": "John Doe",
                    "role": "employee"
                },
                "company": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Example Maritime Ltd",
                    "afm": "9"
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str = Field(..., description="Valid refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": ""
            }
        }


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema"""
    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class LogoutRequest(BaseModel):
    """Logout request schema"""
    refresh_token: Optional[str] = Field(None, description="Refresh token to invalidate")
    logout_all_devices: bool = Field(False, description="Logout from all devices")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "",
                "logout_all_devices": False
            }
        }


class TokenValidationResponse(BaseModel):
    """Token validation response schema"""
    valid: bool = Field(..., description="Whether token is valid")
    user_id: Optional[str] = Field(None, description="User ID if token is valid")
    company_id: Optional[str] = Field(None, description="Company ID if token is valid")
    role: Optional[str] = Field(None, description="User role if token is valid")
    permissions: Optional[List[str]] = Field(None, description="User permissions if token is valid")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "employee",
                "permissions": ["businesses:read", "products:read"],
                "expires_at": "2024-01-15T10:30:00Z"
            }
        }


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr = Field(..., description="User email address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "",
                "new_password": "New",
                "confirm_password": "New"
            }
        }


class PasswordChangeRequest(BaseModel):
    """Password change request schema"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "New",
                "confirm_password": "New"
            }
        }


class EmailVerificationRequest(BaseModel):
    """Email verification request schema"""
    email: EmailStr = Field(..., description="User email address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class EmailVerificationConfirm(BaseModel):
    """Email verification confirmation schema"""
    token: str = Field(..., description="Email verification token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": ""
            }
        }


class UserRegistrationRequest(BaseModel):
    """User registration request schema"""
    # Company information
    company_name: str = Field(..., min_length=2, max_length=255, description="Company name")
    company_afm: str = Field(..., min_length=9, max_length=9, description="Greek Tax Number (AFM)")
    company_doy: str = Field(..., description="Tax Office Code (DOY)")
    business_activity: str = Field(..., description="Primary business activity")
    legal_form: str = Field(..., description="Legal form (AE, EPE, OE, etc.)")
    
    # User information
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Confirm password")
    
    # Address information
    address_street: str = Field(..., description="Street address")
    address_number: str = Field(..., description="Street number")
    address_city: str = Field(..., description="City")
    address_postal_code: str = Field(..., description="Postal code")
    address_region: str = Field(..., description="Greek region")
    
    # Preferences
    language: str = Field("el", description="Preferred language")
    timezone: str = Field("Europe/Athens", description="Timezone")
    
    # Terms and conditions
    accept_terms: bool = Field(..., description="Accept terms and conditions")
    accept_privacy: bool = Field(..., description="Accept privacy policy")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('company_afm')
    def validate_afm(cls, v):
        if not re.match(r'^\d{9}$', v):
            raise ValueError('AFM must be exactly 9 digits')
        return v
    
    @validator('accept_terms')
    def terms_must_be_accepted(cls, v):
        if not v:
            raise ValueError('Terms and conditions must be accepted')
        return v
    
    @validator('accept_privacy')
    def privacy_must_be_accepted(cls, v):
        if not v:
            raise ValueError('Privacy policy must be accepted')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Maritime Solutions Ltd",
                "company_afm": "9",
                "company_doy": "A001",
                "business_activity": "Maritime Services",
                "legal_form": "AE",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@maritime-solutions.gr",
                "phone": "+30 210 1234567",
                "password": "",
                "confirm_password": "",
                "address_street": "Akti Miaouli",
                "address_number": "85",
                "address_city": "Piraeus",
                "address_postal_code": "18538",
                "address_region": "Attica",
                "language": "el",
                "timezone": "Europe/Athens",
                "accept_terms": True,
                "accept_privacy": True
            }
        }


class UserRegistrationResponse(BaseModel):
    """User registration response schema"""
    success: bool = Field(..., description="Registration success status")
    message: str = Field(..., description="Registration message")
    user_id: Optional[str] = Field(None, description="Created user ID")
    company_id: Optional[str] = Field(None, description="Created company ID")
    verification_required: bool = Field(..., description="Whether email verification is required")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Registration successful. Please check your email for verification.",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "verification_required": True
            }
        }


class MessageResponse(BaseModel):
    """Generic message response schema"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully"
            }
        } 