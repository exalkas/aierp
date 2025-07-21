"""
Request/Response Logging Middleware
Provides comprehensive request and response logging for debugging
"""

import time
import json
import uuid
from typing import Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

from ..core.logging import api_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive request/response logging middleware
    """
    
    def __init__(self, app, log_body: bool = False, log_headers: bool = True):
        super().__init__(app)
        self.log_body = log_body
        self.log_headers = log_headers
        self.logger = api_logger.child({"component": "request_logger"})

    async def dispatch(self, request: Request, call_next):
        """Log request and response with comprehensive details"""
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start timing
        start_time = time.time()
        
        # Log request
        await self._log_request(request, request_id)
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        await self._log_response(request, response, request_id, duration)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response

    async def _log_request(self, request: Request, request_id: str):
        """Log incoming request details"""
        # Extract client information
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Extract user context if available
        user_context = {}
        if hasattr(request.state, "user"):
            user = request.state.user
            user_context = {
                "user_id": getattr(user, "id", None),
                "company_id": getattr(user, "company_id", None),
                "role": getattr(user, "role", None)
            }
        
        # Base context
        context = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": client_ip,
            "user_agent": user_agent,
            **user_context
        }
        
        # Add headers if enabled
        if self.log_headers:
            context["headers"] = dict(request.headers)
        
        # Add body if enabled and present
        if self.log_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await self._get_request_body(request)
                if body:
                    context["body"] = body
            except Exception as e:
                context["body_error"] = str(e)
        
        self.logger.info(f"Request started: {request.method} {request.url.path}", context)

    async def _log_response(
        self, 
        request: Request, 
        response: Response, 
        request_id: str, 
        duration: float
    ):
        """Log response details"""
        context = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "response_size": len(getattr(response, 'body', b''))
        }
        
        # Add response headers if enabled
        if self.log_headers:
            context["response_headers"] = dict(response.headers)
        
        # Add response body if enabled and appropriate
        if self.log_body and response.status_code >= 400:
            try:
                if hasattr(response, 'body') and response.body:
                    # Try to parse as JSON for structured logging
                    try:
                        body_str = response.body.decode('utf-8')
                        context["response_body"] = json.loads(body_str)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        context["response_body"] = body_str[:1000]  # Limit size
            except Exception as e:
                context["response_body_error"] = str(e)
        
        # Log based on status code
        if response.status_code >= 500:
            self.logger.error(f"Request failed: {response.status_code}", context)
        elif response.status_code >= 400:
            self.logger.warning(f"Request error: {response.status_code}", context)
        else:
            self.logger.info(f"Request completed: {response.status_code}", context)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address considering proxies"""
        # Check for forwarded headers (common in containerized environments)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        if request.client:
            return request.client.host
        
        return "unknown"

    async def _get_request_body(self, request: Request) -> Optional[Dict[str, Any]]:
        """Safely extract request body for logging"""
        try:
            # Check content type
            content_type = request.headers.get("content-type", "")
            
            if "application/json" in content_type:
                # Handle JSON body
                body_bytes = await request.body()
                if body_bytes:
                    body_str = body_bytes.decode('utf-8')
                    return json.loads(body_str)
            
            elif "application/x-www-form-urlencoded" in content_type:
                # Handle form data
                form_data = await request.form()
                return dict(form_data)
            
            elif "multipart/form-data" in content_type:
                # Handle multipart data (but don't log file contents)
                form_data = await request.form()
                result = {}
                for key, value in form_data.items():
                    if hasattr(value, 'filename'):
                        result[key] = f"<file: {value.filename}>"
                    else:
                        result[key] = str(value)
                return result
            
            else:
                # For other content types, just indicate presence
                body_bytes = await request.body()
                if body_bytes:
                    return {"content_type": content_type, "size": len(body_bytes)}
        
        except Exception:
            # If we can't parse the body, just indicate there was content
            return {"error": "Could not parse request body"}
        
        return None


class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    """
    Performance-focused logging middleware for monitoring slow requests
    """
    
    def __init__(self, app, slow_request_threshold: float = 1.0):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.logger = api_logger.child({"component": "performance_logger"})

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        # Log slow requests
        if duration > self.slow_request_threshold:
            context = {
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration * 1000, 2),
                "status_code": response.status_code,
                "threshold_ms": round(self.slow_request_threshold * 1000, 2)
            }
            
            self.logger.warning("Slow request detected", context)
        
        return response


class SecurityLoggingMiddleware(BaseHTTPMiddleware):
    """
    Security-focused logging middleware for tracking authentication and suspicious activity
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = api_logger.child({"component": "security_logger"})

    async def dispatch(self, request: Request, call_next):
        # Log security-relevant requests
        if self._is_security_relevant(request):
            await self._log_security_event(request)
        
        response = await call_next(request)
        
        # Log authentication failures
        if response.status_code in [401, 403]:
            await self._log_auth_failure(request, response)
        
        return response

    def _is_security_relevant(self, request: Request) -> bool:
        """Determine if request is security-relevant"""
        security_paths = [
            "/auth/",
            "/admin/",
            "/api/v1/users/",
            "/api/v1/companies/"
        ]
        
        return any(request.url.path.startswith(path) for path in security_paths)

    async def _log_security_event(self, request: Request):
        """Log security-relevant events"""
        context = {
            "method": request.method,
            "path": request.url.path,
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown"),
            "authorization_present": "authorization" in request.headers
        }
        
        self.logger.info("Security-relevant request", context)

    async def _log_auth_failure(self, request: Request, response: Response):
        """Log authentication failures"""
        context = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        self.logger.warning("Authentication failure", context)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        if request.client:
            return request.client.host
        
        return "unknown" 