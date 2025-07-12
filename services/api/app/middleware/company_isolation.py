"""
Company Isolation Middleware
Ensures strict data isolation between companies in multi-tenant architecture
"""

import logging
from typing import Optional, Tuple
from fastapi import Request, Response, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt

from app.core.config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()


class CompanyIsolationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce company isolation for all API requests
    Ensures users can only access data from their assigned company
    """
    
    # Endpoints that don't require company isolation
    EXCLUDED_PATHS = {
        "/health",
        "/",
        "/api/docs",
        "/api/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/auth/forgot-password"
    }
    
    async def dispatch(self, request: Request, call_next):
        """Process request and enforce company isolation"""
        
        # Skip excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Skip non-API paths
        if not request.url.path.startswith("/api/"):
            return await call_next(request)
        
        try:
            # Extract and validate company context
            company_id = await self._extract_company_context(request)
            
            if not company_id and settings.REQUIRE_COMPANY_IN_JWT:
                logger.warning(f"Missing company context for request: {request.url.path}")
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "error": "COMPANY_REQUIRED",
                        "message": "Company context is required for this request",
                        "code": "COMP_001"
                    }
                )
            
            # Add company context to request state
            if company_id:
                request.state.company_id = company_id
                logger.debug(f"Request bound to company: {company_id}")
            
            # Process request
            response = await call_next(request)
            
            # Add company context to response headers (for debugging)
            if hasattr(request.state, "company_id") and settings.DEBUG:
                response.headers["X-Company-ID"] = request.state.company_id
            
            return response
            
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail}
            )
        except Exception as e:
            logger.error(f"Company isolation error: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "ISOLATION_ERROR",
                    "message": "Failed to enforce company isolation",
                    "code": "COMP_002"
                }
            )
    
    async def _extract_company_context(self, request: Request) -> Optional[str]:
        """Extract company ID from JWT token or request headers"""
        
        # Try to get company ID from JWT token first
        company_id = await self._extract_from_jwt(request)
        if company_id:
            return company_id
        
        # Fallback: Try to get from headers (for service-to-service calls)
        company_id = request.headers.get("X-Company-ID")
        if company_id:
            logger.debug(f"Company ID from header: {company_id}")
            return company_id
        
        return None
    
    async def _extract_from_jwt(self, request: Request) -> Optional[str]:
        """Extract company ID from JWT token"""
        try:
            # Get authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            # Extract token
            token = auth_header.replace("Bearer ", "")
            if not token:
                return None
            
            # Decode JWT token (without verification for company extraction)
            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.JWT_ALGORITHM]
                )
                
                company_id = payload.get("company_id")
                if company_id:
                    logger.debug(f"Company ID from JWT: {company_id}")
                    return str(company_id)
                
            except jwt.ExpiredSignatureError:
                logger.warning("JWT token expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid JWT token: {e}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
                
        except Exception as e:
            logger.error(f"Error extracting company from JWT: {e}")
            return None
        
        return None
    
    def _validate_company_access(self, user_id: str, company_id: str) -> bool:
        """Validate if user has access to the specified company"""
        # This would typically check against a database
        # For now, we assume the JWT token contains valid company context
        return True


def get_current_company(request: Request) -> str:
    """Helper function to get current company ID from request"""
    if hasattr(request.state, "company_id"):
        return request.state.company_id
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Company context not available"
    )


def ensure_company_isolation(company_id: str, resource_company_id: str):
    """Ensure resource belongs to the current company"""
    if company_id != resource_company_id:
        logger.warning(f"Company isolation violation: {company_id} != {resource_company_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Resource belongs to different company"
        )


async def get_current_user_and_company(request: Request) -> Tuple[dict, str]:
    """
    FastAPI dependency to get current user and company from JWT token
    
    Returns:
        Tuple[dict, str]: (user_data, company_id)
    """
    try:
        # Get authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        # Extract token
        token = auth_header.replace("Bearer ", "")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token"
            )
        
        # Decode JWT token
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # Extract user info
            user_id = payload.get("user_id")
            username = payload.get("username") or payload.get("sub")
            email = payload.get("email")
            company_id = payload.get("company_id")
            
            if not user_id or not company_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user_id or company_id"
                )
            
            # Create user object (simplified for dependency injection)
            user = {
                "id": user_id,
                "username": username,
                "email": email,
                "company_id": company_id
            }
            
            return user, str(company_id)
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user and company: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate user"
        ) 