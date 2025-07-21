"""
Authentication Service
Comprehensive authentication service with all authentication endpoints
Enhanced with structured logging and comprehensive error handling
"""

from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import secrets
import time
from uuid import uuid4

from database import get_db
from models import User, Company, UserStatus
from jwt_utils import jwt_manager
from schemas import (
    LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse,
    LogoutRequest, TokenValidationResponse, PasswordResetRequest, 
    PasswordResetConfirm, PasswordChangeRequest, EmailVerificationRequest,
    EmailVerificationConfirm, UserRegistrationRequest, UserRegistrationResponse,
    MessageResponse
)
from config import settings
from email_service import send_password_reset_email, send_verification_email
from structured_logger import auth_logger, LogLevel

# Use auth_logger for all logging operations 
logger = auth_logger


class AuthenticationService:
    """Authentication service business logic"""
    
    def __init__(self):
        self.jwt_manager = jwt_manager
    
    async def login(self, login_data: LoginRequest, db: AsyncSession) -> LoginResponse:
        """
        Authenticate user and return JWT tokens with comprehensive logging and error handling
        """
        start_time = time.time()
        request_id = auth_logger.request_started(
            "POST", "/auth/login",
            {"email": login_data.email, "remember_me": login_data.remember_me}
        )
        
        try:
            with auth_logger.time_operation("Database user lookup", {"email": login_data.email}):
                # Find user by email
                query = select(User).where(
                    and_(
                        User.email == login_data.email.lower(),
                        User.is_active == True
                    )
                )
                result = await db.execute(query)
                user = result.scalar_one_or_none()
            
            if not user:
                auth_logger.auth_failure(
                    login_data.email, 
                    "User not found or inactive",
                    {"request_id": request_id, "ip": getattr(login_data, 'ip_address', 'unknown')}
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                    headers={"X-Error-Code": "AUTH_USER_NOT_FOUND"}
                )
            
            # Verify password
            if not user.verify_password(login_data.password):
                auth_logger.auth_failure(
                    login_data.email,
                    "Invalid password",
                    {"request_id": request_id, "user_id": str(user.id)}
                )
                
                # Increment failed login attempts
                user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
                
                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    auth_logger.warning(
                        f"Account locked due to multiple failed attempts: {user.email}",
                        {"user_id": str(user.id), "attempts": user.failed_login_attempts}
                    )
                
                await db.commit()
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                    headers={"X-Error-Code": "AUTH_INVALID_CREDENTIALS"}
                )
            
            # Check if account is locked
            if user.locked_until and user.locked_until > datetime.utcnow():
                auth_logger.auth_failure(
                    login_data.email,
                    "Account is locked",
                    {"user_id": str(user.id), "locked_until": user.locked_until.isoformat()}
                )
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Account is temporarily locked due to multiple failed login attempts",
                    headers={"X-Error-Code": "AUTH_ACCOUNT_LOCKED"}
                )

            # Get company information
            with auth_logger.time_operation("Database company lookup", {"company_id": str(user.company_id)}):
                company_query = select(Company).where(Company.id == user.company_id)
                company_result = await db.execute(company_query)
                company = company_result.scalar_one_or_none()

            if not company or not company.is_active:
                auth_logger.auth_failure(
                    login_data.email,
                    "Company inactive or not found",
                    {"user_id": str(user.id), "company_id": str(user.company_id)}
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Company account is inactive",
                    headers={"X-Error-Code": "AUTH_COMPANY_INACTIVE"}
                )
            
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.locked_until = None
            user.last_login = datetime.utcnow()
            
            # Generate tokens
            with auth_logger.time_operation("Token generation", {"user_id": str(user.id)}):
                access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                if login_data.remember_me:
                    access_token_expires = timedelta(days=1)  # Extended session
                
                access_token = self.jwt_manager.create_access_token(
                    user=user, 
                    company=company,
                    expires_delta=access_token_expires
                )
                refresh_token = self.jwt_manager.create_refresh_token(user=user)
            
            # Create user dict BEFORE commit to avoid session issues
            user_dict = user.to_dict()
            company_dict = {
                "id": str(company.id),
                "name": company.name,
                "afm": company.afm,
                "doy": company.doy,
                "is_active": company.is_active,
            }
            
            await db.commit()
            
            logger.info(f"Successful login for user: {user.email}")
            
            return LoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=int(access_token_expires.total_seconds()),
                user=user_dict,
                company=company_dict
            )
            
        except HTTPException:
            raise
        except Exception as e:
            auth_logger.error(f"Login error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during login"
            )
    
    async def refresh_token(self, refresh_data: RefreshTokenRequest, db: AsyncSession) -> RefreshTokenResponse:
        """
        Refresh access token using refresh token
        """
        try:
            # Validate refresh token
            payload = self.jwt_manager.validate_refresh_token(refresh_data.refresh_token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            # Get user and company
            user_id = payload.get("user_id")
            user = await db.execute(select(User).where(
                and_(
                    User.id == user_id,
                    User.is_active == True
                )
            ))
            user = user.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )
            
            company = await db.execute(select(Company).where(Company.id == user.company_id))
            company = company.scalar_one_or_none()
            
            if not company or not company.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Company not found or inactive"
                )
            
            # Update last activity
            user.last_activity = datetime.utcnow()
            await db.commit()
            
            # Generate new access token
            access_token = self.jwt_manager.create_access_token(user=user, company=company)
            
            logger.info(f"Token refreshed for user: {user.email}")
            
            return RefreshTokenResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during token refresh"
            )
    
    async def logout(self, logout_data: LogoutRequest, current_user_id: str, db: AsyncSession) -> MessageResponse:
        """
        Logout user and invalidate tokens
        """
        try:
            user = await db.execute(select(User).where(User.id == current_user_id))
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Clear session token
            user.session_token = None
            user.last_activity = datetime.utcnow()
            
            if logout_data.logout_all_devices:
                # TODO: Implement blacklisting of all user tokens
                # This could be done by updating a "tokens_valid_after" timestamp
                # or by maintaining a blacklist in Redis
                pass
            
            await db.commit()
            
            logger.info(f"User logged out: {user.email}")
            
            return MessageResponse(
                success=True,
                message="Successfully logged out"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Logout error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during logout"
            )
    
    async def validate_token(self, token: str) -> TokenValidationResponse:
        """
        Validate JWT token and return user information
        """
        try:
            payload = self.jwt_manager.validate_access_token(token)
            if not payload:
                return TokenValidationResponse(
                    valid=False,
                    user_id=None,
                    company_id=None,
                    role=None,
                    permissions=None,
                    expires_at=None
                )
            
            return TokenValidationResponse(
                valid=True,
                user_id=payload.get("user_id"),
                company_id=payload.get("company_id"),
                role=payload.get("role"),
                permissions=payload.get("permissions", []),
                expires_at=datetime.fromtimestamp(payload.get("exp", 0))
            )
            
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return TokenValidationResponse(
                valid=False,
                user_id=None,
                company_id=None,
                role=None,
                permissions=None,
                expires_at=None
            )
    
    async def request_password_reset(self, reset_data: PasswordResetRequest, db: AsyncSession) -> MessageResponse:
        """
        Send password reset email
        """
        try:
            user = await db.execute(select(User).where(User.email == reset_data.email.lower()))
            user = user.scalar_one_or_none()
            
            # Always return success for security (don't reveal if email exists)
            if not user:
                logger.warning(f"Password reset requested for non-existent email: {reset_data.email}")
                return MessageResponse(
                    success=True,
                    message="If the email exists, a password reset link has been sent"
                )
            
            # Generate password reset token
            reset_token = self.jwt_manager.create_password_reset_token(user)
            
            # Store token in database
            user.password_reset_token = reset_token
            user.password_reset_expires = datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_EXPIRE_HOURS)
            await db.commit()
            
            # Send reset email
            await send_password_reset_email(user.email, user.full_name, reset_token)
            
            logger.info(f"Password reset email sent to: {user.email}")
            
            return MessageResponse(
                success=True,
                message="If the email exists, a password reset link has been sent"
            )
            
        except Exception as e:
            logger.error(f"Password reset request error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during password reset request"
            )
    
    async def confirm_password_reset(self, reset_data: PasswordResetConfirm, db: AsyncSession) -> MessageResponse:
        """
        Confirm password reset with token
        """
        try:
            # Validate password reset token
            payload = self.jwt_manager.validate_password_reset_token(reset_data.token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired password reset token"
                )
            
            # Get user
            user_id = payload.get("user_id")
            user = await db.execute(select(User).where(User.id == user_id))
            user = user.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Check if token matches stored token
            if user.password_reset_token != reset_data.token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid password reset token"
                )
            
            # Check token expiration
            if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password reset token has expired"
                )
            
            # Update password
            user.set_password(reset_data.new_password)
            user.password_reset_token = None
            user.password_reset_expires = None
            user.failed_login_attempts = 0
            user.locked_until = None
            
            await db.commit()
            
            logger.info(f"Password reset completed for user: {user.email}")
            
            return MessageResponse(
                success=True,
                message="Password has been reset successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Password reset confirmation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during password reset"
            )
    
    async def change_password(self, change_data: PasswordChangeRequest, current_user_id: str, db: AsyncSession) -> MessageResponse:
        """
        Change user password (authenticated)
        """
        try:
            user = await db.execute(select(User).where(User.id == current_user_id))
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Verify current password
            if not user.verify_password(change_data.current_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
            
            # Update password
            user.set_password(change_data.new_password)
            await db.commit()
            
            logger.info(f"Password changed for user: {user.email}")
            
            return MessageResponse(
                success=True,
                message="Password has been changed successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Password change error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during password change"
            )
    
    async def register_user(self, registration_data: UserRegistrationRequest, db: AsyncSession) -> UserRegistrationResponse:
        """
        Register new user and company
        """
        try:
            # Check if email already exists
            existing_user = await db.execute(select(User).where(User.email == registration_data.email.lower()))
            existing_user = existing_user.scalar_one_or_none()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email address is already registered"
                )
            
            # Check if AFM already exists
            existing_company = await db.execute(select(Company).where(Company.afm == registration_data.company_afm))
            existing_company = existing_company.scalar_one_or_none()
            if existing_company:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="AFM is already registered"
                )
            
            # Create company
            company = Company(
                id=uuid4(),
                name=registration_data.company_name,
                display_name=registration_data.company_name,
                afm=registration_data.company_afm,
                doy=registration_data.company_doy,
                business_activity=registration_data.business_activity,
                legal_form=registration_data.legal_form,
                email=registration_data.email,
                address_street=registration_data.address_street,
                address_number=registration_data.address_number,
                address_city=registration_data.address_city,
                address_postal_code=registration_data.address_postal_code,
                address_region=registration_data.address_region,
                address_country="GR",
                vat_number=f"EL{registration_data.company_afm}",
                accounting_start_date=datetime.utcnow(),
                database_name=f"company_{registration_data.company_afm}",
                is_active=True,
                is_verified=False,
                setup_completed=False
            )
            
            db.add(company)
            await db.flush()  # Get company ID
            
            # Create user (company admin)
            user = User(
                id=uuid4(),
                company_id=company.id,
                username=registration_data.email.split('@')[0],  # Use email prefix as username
                email=registration_data.email.lower(),
                first_name=registration_data.first_name,
                last_name=registration_data.last_name,
                display_name=f"{registration_data.first_name} {registration_data.last_name}",
                phone=registration_data.phone,
                role=UserRole.COMPANY_ADMIN,
                status=UserStatus.PENDING_VERIFICATION,
                language=registration_data.language,
                timezone=registration_data.timezone,
                is_active=True,
                is_verified=False
            )
            
            # Set password
            user.set_password(registration_data.password)
            
            # Generate email verification token
            verification_token = self.jwt_manager.create_email_verification_token(user)
            user.email_verification_token = verification_token
            user.email_verification_expires = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
            
            db.add(user)
            await db.commit()
            
            # Send verification email
            await send_verification_email(user.email, user.full_name, verification_token)
            
            logger.info(f"New user registered: {user.email} for company: {company.name}")
            
            return UserRegistrationResponse(
                success=True,
                message="Registration successful. Please check your email for verification.",
                user_id=str(user.id),
                company_id=str(company.id),
                verification_required=True
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"User registration error: {e}")
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during registration"
            )
    
    async def verify_email(self, verification_data: EmailVerificationConfirm, db: AsyncSession) -> MessageResponse:
        """
        Verify user email address
        """
        try:
            # Validate email verification token
            payload = self.jwt_manager.validate_email_verification_token(verification_data.token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired email verification token"
                )
            
            # Get user
            user_id = payload.get("user_id")
            user = await db.execute(select(User).where(User.id == user_id))
            user = user.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Check if token matches stored token
            if user.email_verification_token != verification_data.token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email verification token"
                )
            
            # Check token expiration
            if user.email_verification_expires and user.email_verification_expires < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email verification token has expired"
                )
            
            # Verify email and activate user
            user.is_verified = True
            user.status = UserStatus.ACTIVE
            user.email_verified_at = datetime.utcnow()
            user.email_verification_token = None
            user.email_verification_expires = None
            
            await db.commit()
            
            logger.info(f"Email verified for user: {user.email}")
            
            return MessageResponse(
                success=True,
                message="Email has been verified successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Email verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during email verification"
            )
    
    async def request_email_verification(self, verification_data: EmailVerificationRequest, db: AsyncSession) -> MessageResponse:
        """
        Request email verification
        """
        try:
            user = await db.execute(select(User).where(User.email == verification_data.email.lower()))
            user = user.scalar_one_or_none()
            
            if not user:
                # Don't reveal if email exists
                return MessageResponse(
                    success=True,
                    message="If the email exists, a verification link has been sent"
                )
            
            if user.is_verified:
                return MessageResponse(
                    success=True,
                    message="Email is already verified"
                )
            
            # Generate new verification token
            verification_token = self.jwt_manager.create_email_verification_token(user)
            user.email_verification_token = verification_token
            user.email_verification_expires = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
            
            await db.commit()
            
            # Send verification email
            await send_verification_email(user.email, user.full_name, verification_token)
            
            logger.info(f"Email verification requested for: {user.email}")
            
            return MessageResponse(
                success=True,
                message="Verification email has been sent"
            )
            
        except Exception as e:
            logger.error(f"Email verification request error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during email verification request"
            )
    
    async def confirm_email_verification(self, verification_data: EmailVerificationConfirm, db: AsyncSession) -> MessageResponse:
        """
        Confirm email verification
        """
        return await self.verify_email(verification_data, db)
    
    async def get_current_user(self, current_user_id: str, db: AsyncSession) -> Dict[str, Any]:
        """
        Get current user information
        """
        try:
            user = await db.execute(select(User).where(User.id == current_user_id))
            user = user.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Get company information
            company = await db.execute(select(Company).where(Company.id == user.company_id))
            company = company.scalar_one_or_none()
            
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
            
            return {
                "user": user.to_dict(),
                "company": {
                    "id": str(company.id),
                    "name": company.name,
                    "display_name": company.display_name,
                    "afm": company.afm,
                    "doy": company.doy,
                    "is_active": company.is_active,
                    "is_verified": company.is_verified
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get current user error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error getting user information"
            )


# Global authentication service instance
auth_service = AuthenticationService() 