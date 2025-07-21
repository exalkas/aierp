"""
Company Isolation Middleware
Ensures strict data isolation between companies in multi-tenant architecture
"""

import time
from typing import Optional, Tuple
from fastapi import Request, Response, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt
from jwt.exceptions import InvalidSignatureError

from app.core.config import settings

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
        "/api/v1/auth/forgot-password",
        "/api/v1/greek-reference-data",
        "/api/v1/doy-offices",
        "/api/v1/doy-offices/search"
    }

    def _is_public_route(self, path: str) -> bool:
        """Check if the path is a public route that doesn't require company isolation"""
        # Check exact matches
        if path in self.EXCLUDED_PATHS:
            return True
        
        # Check if it's a non-API path
        if not path.startswith("/api/"):
            return True
            
        # Check for static files and docs
        if any(static_path in path for static_path in ["/static/", "/docs", "/redoc", "/openapi"]):
            return True
            
        return False
    
    async def dispatch(self, request: Request, call_next):
        """Process request with company isolation"""
        import time
        
        start_time = time.time()
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        print(f"[COMPANY] Starting company isolation: {request.method} {request.url.path} [{request_id}] at {time.time()}")
        
        try:
            # Skip isolation for public routes
            if self._is_public_route(request.url.path):
                print(f"[COMPANY] Public route, skipping isolation at {time.time()}")
                response = await call_next(request)
                duration = (time.time() - start_time) * 1000
                print(f"[COMPANY] Public route completed ({duration:.2f}ms) at {time.time()}")
                return response
            
            print(f"[COMPANY] Getting user and company at {time.time()}")
            
            # Get current user and company
            user, company = await get_current_user_and_company(request)
            
            print(f"[COMPANY] User/company retrieved at {time.time()}: user={user.id if user else None}, company={company if company else None}")
            
            # Store in request state
            request.state.current_user = user
            request.state.current_company = company
            
            # Set company context for database queries
            if company:
                print(f"[COMPANY] Setting company context: {company} at {time.time()}")
                request.state.company_id = company
            else:
                print(f"[COMPANY] No company context set at {time.time()}")
                
            print(f"[COMPANY] About to call next middleware at {time.time()}")
            
            # Process request with company context
            response = await call_next(request)
            
            duration = (time.time() - start_time) * 1000
            print(f"[COMPANY] Company isolation completed ({duration:.2f}ms) at {time.time()}")
            
            return response
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            print(f"[COMPANY ERROR] Company isolation error ({duration:.2f}ms): {e}")
            print(f"[COMPANY ERROR] Company isolation error for {request.url.path}: {e}")
            raise
    
    async def _extract_company_context(self, request: Request) -> Optional[str]:
        """Extract company ID from JWT token or request headers"""
        
        # Try to get company ID from JWT token first
        company_id = await self._extract_from_jwt(request)
        if company_id:
            return company_id
        
        # Fallback: Try to get from headers (for service-to-service calls)
        company_id = request.headers.get("X-Company-ID")
        if company_id:
            print(f"[COMPANY DEBUG] Company ID from header: {company_id}")
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
                    return str(company_id)
                
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )
            except jwt.InvalidTokenError as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
                
        except Exception as e:
            print(f"[COMPANY ERROR] Error extracting company from JWT: {e}")
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
        print(f"[COMPANY WARNING] Company isolation violation: {company_id} != {resource_company_id}")
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
    import time
    
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    print(f"[JWT] Starting JWT validation [{request_id}] at {time.time()}")
    
    try:
        # Get authorization header
        print(f"[JWT] Getting auth header at {time.time()}")
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            print(f"[JWT ERROR] Missing/invalid auth header at {time.time()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        # Extract token
        print(f"[JWT] Extracting token at {time.time()}")
        token = auth_header.replace("Bearer ", "")
        if not token:
            print(f"[JWT ERROR] Missing token at {time.time()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token"
            )
        
        # Decode JWT token
        print(f"[JWT] About to decode JWT at {time.time()}")
        print(f"[JWT DEBUG] Token details:", {
            "token_length": len(token),
            "token_start": token[:20] + "...",
            "token_end": "..." + token[-20:],
            "has_dots": token.count('.'),
            "algorithm": settings.JWT_ALGORITHM,
            "secret_key_length": len(settings.JWT_SECRET_KEY) if settings.JWT_SECRET_KEY else 0,
            "secret_key_start": settings.JWT_SECRET_KEY[:10] + "..." if settings.JWT_SECRET_KEY else "NO_KEY",
        })
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            print(f"[JWT] JWT decoded successfully at {time.time()}")
            print(f"[JWT DEBUG] Decoded payload keys: {list(payload.keys())}")
            
            # Extract user info
            user_id = payload.get("user_id")
            username = payload.get("username") or payload.get("sub")
            email = payload.get("email")
            company_id = payload.get("company_id")
            full_name = payload.get("full_name")
            role = payload.get("role")
            is_active = payload.get("is_active", True)
            is_superuser = payload.get("is_superuser", False)
            permissions = payload.get("permissions", [])
            
            print(f"[JWT] Extracted user info at {time.time()}: user_id={user_id}, company_id={company_id}")
            
            if not user_id or not company_id:
                print(f"[JWT ERROR] Missing user_id or company_id at {time.time()}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user_id or company_id"
                )
            
            # Create user-like object with all necessary attributes for services
            class UserFromToken:
                def __init__(self, data):
                    self.id = data["id"]
                    self.username = data["username"]
                    self.email = data["email"]
                    self.company_id = data["company_id"]
                    self.full_name = data.get("full_name")
                    self.role = data.get("role")
                    self.is_active = data.get("is_active", True)
                    self.is_super_user = data.get("is_super_user", False)  # Consistent naming
                    self.permissions = data.get("permissions", [])
            
            print(f"[JWT] Creating user object at {time.time()}")
            
            user = UserFromToken({
                "id": user_id,
                "username": username,
                "email": email,
                "company_id": company_id,
                "full_name": full_name,
                "role": role,
                "is_active": is_active,
                "is_super_user": is_superuser,
                "permissions": permissions
            })
            
            duration = (time.time() - start_time) * 1000
            print(f"[JWT] JWT validation completed ({duration:.2f}ms) at {time.time()}")
            
            return user, str(company_id)
            
        except jwt.ExpiredSignatureError as e:
            print(f"[JWT] Token expired at {time.time()}")
            print(f"[JWT DEBUG] Expired token details:", {
                "error": str(e),
                "token_start": token[:20] + "...",
            })
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidSignatureError as e:
            print(f"[JWT] Invalid signature at {time.time()}: {e}")
            print(f"[JWT DEBUG] Signature verification failed:", {
                "error": str(e),
                "token_parts": len(token.split('.')),
                "secret_length": len(settings.JWT_SECRET_KEY) if settings.JWT_SECRET_KEY else 0,
                "algorithm": settings.JWT_ALGORITHM,
                "config_file": "services/api/.env",
            })
            
            # Try to decode without verification to see the header and payload
            try:
                unverified_header = jwt.get_unverified_header(token)
                unverified_payload = jwt.decode(token, options={"verify_signature": False})
                print(f"[JWT DEBUG] Unverified token contents:", {
                    "header": unverified_header,
                    "payload_keys": list(unverified_payload.keys()),
                    "payload_iss": unverified_payload.get("iss"),
                    "payload_exp": unverified_payload.get("exp"),
                    "payload_user_id": unverified_payload.get("user_id"),
                })
            except Exception as decode_error:
                print(f"[JWT DEBUG] Could not decode unverified token: {decode_error}")
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token signature: {str(e)}"
            )
        except jwt.InvalidTokenError as e:
            print(f"[JWT] Invalid token at {time.time()}: {e}")
            print(f"[JWT DEBUG] General token error:", {
                "error_type": type(e).__name__,
                "error": str(e),
                "token_start": token[:20] + "...",
            })
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
            
    except HTTPException:
        print(f"[JWT] HTTP exception at {time.time()}")
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        print(f"[JWT] Unexpected error ({duration:.2f}ms) at {time.time()}: {e}")
        print(f"[JWT ERROR] Error getting user and company: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate user"
        ) 