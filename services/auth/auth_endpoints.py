"""
Authentication Endpoints
FastAPI endpoints for all authentication functionality
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from database import get_db
from auth_service import auth_service
from schemas import (
    LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse,
    LogoutRequest, TokenValidationResponse, PasswordResetRequest, 
    PasswordResetConfirm, PasswordChangeRequest, EmailVerificationRequest,
    EmailVerificationConfirm, UserRegistrationRequest, UserRegistrationResponse,
    MessageResponse
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract current user ID from JWT token
    """
    try:
        token = credentials.credentials
        validation_result = await auth_service.validate_token(token)
        
        if not validation_result.valid or not validation_result.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return validation_result.user_id
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens
    
    **Greek Business Features:**
    - Multi-tenant company isolation
    - Greek tax number (AFM) validation
    - Role-based permissions
    - Greek localization support
    """
    return await auth_service.login(login_data, db)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    **Security Features:**
    - Validates refresh token
    - Generates new access token
    - Updates user activity
    """
    return await auth_service.refresh_token(refresh_data, db)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    logout_data: LogoutRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout user and invalidate tokens
    
    **Features:**
    - Invalidates current session
    - Optional logout from all devices
    - Updates user activity
    """
    return await auth_service.logout(logout_data, current_user_id, db)


@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(
    authorization: Optional[str] = Header(None)
):
    """
    Validate JWT token and return user information
    
    **Use Cases:**
    - API gateway token validation
    - Microservice authentication
    - Frontend token verification
    """
    if not authorization:
        return TokenValidationResponse(
            valid=False,
            user_id=None,
            company_id=None,
            role=None,
            permissions=None,
            expires_at=None
        )
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authorization scheme")
    except ValueError:
        return TokenValidationResponse(
            valid=False,
            user_id=None,
            company_id=None,
            role=None,
            permissions=None,
            expires_at=None
        )
    
    return await auth_service.validate_token(token)


@router.post("/password/reset/request", response_model=MessageResponse)
async def request_password_reset(
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset email
    
    **Security Features:**
    - Always returns success (doesn't reveal if email exists)
    - Generates secure reset token
    - Sends Greek language email
    - Token expires in 24 hours
    """
    return await auth_service.request_password_reset(reset_data, db)


@router.post("/password/reset/confirm", response_model=MessageResponse)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """
    Confirm password reset with token
    
    **Security Features:**
    - Validates reset token
    - Enforces strong password requirements
    - Invalidates reset token after use
    - Resets login attempt counters
    """
    return await auth_service.confirm_password_reset(reset_data, db)


@router.post("/password/change", response_model=MessageResponse)
async def change_password(
    change_data: PasswordChangeRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Change user password (authenticated)
    
    **Security Features:**
    - Requires current password verification
    - Enforces strong password requirements
    - Updates password change timestamp
    """
    return await auth_service.change_password(change_data, current_user_id, db)


@router.post("/register", response_model=UserRegistrationResponse)
async def register_user(
    registration_data: UserRegistrationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register new user with company setup
    
    **Greek Business Features:**
    - AFM (Tax Number) validation
    - DOY (Tax Office) validation
    - Company legal form validation
    - Greek address formatting
    - Greek localization setup
    """
    return await auth_service.register_user(registration_data, db)


@router.post("/email/verification/request", response_model=MessageResponse)
async def request_email_verification(
    verification_data: EmailVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Request email verification
    
    **Features:**
    - Sends verification email
    - Greek language support
    - Token expires in 24 hours
    """
    return await auth_service.request_email_verification(verification_data, db)


@router.post("/email/verification/confirm", response_model=MessageResponse)
async def confirm_email_verification(
    verification_data: EmailVerificationConfirm,
    db: AsyncSession = Depends(get_db)
):
    """
    Confirm email verification
    
    **Features:**
    - Validates verification token
    - Activates user account
    - Sends welcome email
    """
    return await auth_service.confirm_email_verification(verification_data, db)


@router.get("/me", response_model=dict)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user information
    
    **Features:**
    - Returns user profile
    - Company information
    - Role and permissions
    - Greek localization data
    """
    return await auth_service.get_current_user(current_user_id, db)


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the authentication service
    """
    return {
        "status": "healthy",
        "service": "greek-erp-auth",
        "version": "1.0.0",
        "features": [
            "JWT Authentication",
            "Password Management",
            "Email Verification", 
            "User Registration",
            "Greek Business Compliance",
            "Multi-tenant Support"
        ]
    } 