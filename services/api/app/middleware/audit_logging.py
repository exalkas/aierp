"""
Audit Logging Middleware
Comprehensive audit trail for Greek ERP/CRM compliance requirements
"""

import logging
import json
import time
from typing import Optional, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
import uuid

from app.core.config import settings

logger = logging.getLogger(__name__)
audit_logger = logging.getLogger("audit")


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive audit logging
    Tracks all API operations for compliance and security
    """
    
    # Sensitive endpoints that require detailed logging
    SENSITIVE_ENDPOINTS = {
        "/api/v1/customers",
        "/api/v1/invoices",
        "/api/v1/payments",
        "/api/v1/users",
        "/api/v1/companies",
        "/api/v1/aade",
        "/api/v1/reports/financial"
    }
    
    # Fields to exclude from request/response logging (security)
    EXCLUDED_FIELDS = {
        "password",
        "secret",
        "token",
        "key",
        "afm",  # Greek tax number - sensitive data
        "bank_account",
        "credit_card"
    }
    
    async def dispatch(self, request: Request, call_next):
        """Process request with audit logging"""
        
        # Generate request ID for tracing
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start timing
        start_time = time.time()
        
        # Extract request data
        audit_data = await self._prepare_audit_data(request, request_id)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Log successful request
            await self._log_request_success(
                audit_data, response, processing_time
            )
            
            return response
            
        except Exception as e:
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Log failed request
            await self._log_request_error(
                audit_data, e, processing_time
            )
            
            # Re-raise exception
            raise
    
    async def _prepare_audit_data(self, request: Request, request_id: str) -> Dict[str, Any]:
        """Prepare audit data from request"""
        
        # Basic request information
        audit_data = {
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": self._sanitize_headers(dict(request.headers)),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        # Add company context if available
        if hasattr(request.state, "company_id"):
            audit_data["company_id"] = request.state.company_id
        
        # Add user context if available in JWT
        user_context = await self._extract_user_context(request)
        if user_context:
            audit_data.update(user_context)
        
        # Add request body for sensitive endpoints or POST/PUT/PATCH methods
        if (request.url.path in self.SENSITIVE_ENDPOINTS or 
            request.method in ["POST", "PUT", "PATCH", "DELETE"]):
            audit_data["request_body"] = await self._get_request_body(request)
        
        return audit_data
    
    async def _log_request_success(
        self, 
        audit_data: Dict[str, Any], 
        response: Response, 
        processing_time: float
    ):
        """Log successful request"""
        
        audit_data.update({
            "status": "SUCCESS",
            "status_code": response.status_code,
            "processing_time_ms": round(processing_time * 1000, 2),
            "response_size": len(response.body) if hasattr(response, 'body') else 0
        })
        
        # Add response body for sensitive endpoints
        if (audit_data["path"] in self.SENSITIVE_ENDPOINTS and 
            response.status_code < 400):
            # Don't log large responses
            if audit_data["response_size"] < 10000:  # 10KB limit
                try:
                    response_body = response.body.decode() if hasattr(response, 'body') else None
                    if response_body:
                        audit_data["response_body"] = self._sanitize_data(
                            json.loads(response_body)
                        )
                except:
                    pass  # Skip if can't decode response
        
        # Log audit trail
        audit_logger.info(json.dumps(audit_data, ensure_ascii=False))
        
        # Log summary for regular application logs
        logger.info(
            f"API Request: {audit_data['method']} {audit_data['path']} - "
            f"{audit_data['status_code']} ({audit_data['processing_time_ms']}ms) "
            f"[{audit_data['request_id']}]"
        )
    
    async def _log_request_error(
        self, 
        audit_data: Dict[str, Any], 
        error: Exception, 
        processing_time: float
    ):
        """Log failed request"""
        
        audit_data.update({
            "status": "ERROR",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "processing_time_ms": round(processing_time * 1000, 2)
        })
        
        # Log audit trail
        audit_logger.error(json.dumps(audit_data, ensure_ascii=False))
        
        # Log summary for regular application logs
        logger.error(
            f"API Error: {audit_data['method']} {audit_data['path']} - "
            f"{audit_data['error_type']}: {audit_data['error_message']} "
            f"({audit_data['processing_time_ms']}ms) [{audit_data['request_id']}]"
        )
    
    async def _extract_user_context(self, request: Request) -> Optional[Dict[str, Any]]:
        """Extract user context from JWT token"""
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            token = auth_header.replace("Bearer ", "")
            if not token:
                return None
            
            # For audit purposes, we decode without verification
            # (middleware runs after auth validation)
            import jwt
            payload = jwt.decode(
                token, 
                options={"verify_signature": False}
            )
            
            return {
                "user_id": payload.get("user_id"),
                "username": payload.get("username"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "company_id": payload.get("company_id")
            }
            
        except Exception:
            return None
    
    async def _get_request_body(self, request: Request) -> Optional[Dict[str, Any]]:
        """Extract and sanitize request body"""
        try:
            if request.method in ["GET", "DELETE"]:
                return None
            
            # Get request body
            body = await request.body()
            if not body:
                return None
            
            # Try to parse as JSON
            try:
                json_body = json.loads(body.decode())
                return self._sanitize_data(json_body)
            except:
                # If not JSON, return truncated string
                body_str = body.decode()[:1000]  # Limit to 1KB
                return {"raw_body": body_str}
                
        except Exception as e:
            logger.warning(f"Failed to extract request body: {e}")
            return None
    
    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Remove sensitive information from headers"""
        sanitized = {}
        
        for key, value in headers.items():
            key_lower = key.lower()
            
            if any(field in key_lower for field in self.EXCLUDED_FIELDS):
                sanitized[key] = "[REDACTED]"
            elif key_lower == "authorization":
                sanitized[key] = "Bearer [REDACTED]"
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _sanitize_data(self, data: Any) -> Any:
        """Recursively sanitize sensitive data"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                key_lower = key.lower()
                
                if any(field in key_lower for field in self.EXCLUDED_FIELDS):
                    sanitized[key] = "[REDACTED]"
                else:
                    sanitized[key] = self._sanitize_data(value)
            
            return sanitized
        
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        
        else:
            return data
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for forwarded IP (reverse proxy)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for real IP
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to client IP
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return "unknown" 