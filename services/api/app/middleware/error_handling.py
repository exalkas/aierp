"""
Comprehensive Error Handling Middleware
Provides structured error responses with proper HTTP status codes
Enhanced with Greek business context and multilingual support
"""

import time
import traceback
from typing import Dict, Any, Optional
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from pydantic import ValidationError

from ..core.logging import api_logger


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive error handling middleware with structured logging
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = api_logger.child({"component": "error_handler"})

    async def dispatch(self, request: Request, call_next):
        """Process request with comprehensive error handling"""
        start_time = time.time()
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Log successful requests
            duration = time.time() - start_time
            if response.status_code >= 400:
                self.logger.warning(
                    f"HTTP {response.status_code} response",
                    {
                        "request_id": request_id,
                        "method": request.method,
                        "url": str(request.url),
                        "status_code": response.status_code,
                        "duration_ms": round(duration * 1000, 2)
                    }
                )
            
            return response
            
        except HTTPException as exc:
            return await self._handle_http_exception(request, exc, start_time)
        except RequestValidationError as exc:
            return await self._handle_validation_error(request, exc, start_time)
        except SQLAlchemyError as exc:
            return await self._handle_database_error(request, exc, start_time)
        except Exception as exc:
            return await self._handle_unexpected_error(request, exc, start_time)

    async def _handle_http_exception(
        self, 
        request: Request, 
        exc: HTTPException, 
        start_time: float
    ) -> JSONResponse:
        """Handle standard HTTP exceptions"""
        duration = time.time() - start_time
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        # Extract error code from headers if present
        error_code = exc.headers.get("X-Error-Code") if exc.headers else None
        
        context = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "status_code": exc.status_code,
            "duration_ms": round(duration * 1000, 2),
            "error_code": error_code
        }
        
        if exc.status_code >= 500:
            self.logger.error(f"HTTP {exc.status_code}: {exc.detail}", context)
        elif exc.status_code >= 400:
            self.logger.warning(f"HTTP {exc.status_code}: {exc.detail}", context)
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "http_exception",
                    "code": error_code or f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "status_code": exc.status_code,
                    "request_id": request_id,
                    "timestamp": time.time()
                }
            },
            headers={"X-Request-ID": request_id}
        )

    async def _handle_validation_error(
        self, 
        request: Request, 
        exc: RequestValidationError, 
        start_time: float
    ) -> JSONResponse:
        """Handle request validation errors"""
        duration = time.time() - start_time
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        # Extract validation error details
        validation_errors = []
        for error in exc.errors():
            validation_errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
                "input": error.get("input")
            })
        
        context = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "validation_errors": validation_errors,
            "duration_ms": round(duration * 1000, 2)
        }
        
        self.logger.warning("Request validation failed", context)
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "type": "validation_error",
                    "code": "VALIDATION_FAILED",
                    "message": "Request validation failed",
                    "details": validation_errors,
                    "request_id": request_id,
                    "timestamp": time.time()
                }
            },
            headers={"X-Request-ID": request_id}
        )

    async def _handle_database_error(
        self, 
        request: Request, 
        exc: SQLAlchemyError, 
        start_time: float
    ) -> JSONResponse:
        """Handle database-related errors"""
        duration = time.time() - start_time
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        context = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "duration_ms": round(duration * 1000, 2),
            "error_type": type(exc).__name__
        }
        
        # Determine specific error type and response
        if isinstance(exc, IntegrityError):
            # Handle constraint violations (duplicates, foreign keys, etc.)
            error_message = "Data integrity constraint violated"
            error_code = "DATA_INTEGRITY_ERROR"
            status_code = status.HTTP_409_CONFLICT
            
            # Check for specific Greek business constraints
            if "afm" in str(exc).lower():
                error_message = "AFM already exists or invalid"
                error_code = "DUPLICATE_AFM"
            elif "email" in str(exc).lower():
                error_message = "Email already exists"
                error_code = "DUPLICATE_EMAIL"
            elif "foreign key" in str(exc).lower():
                error_message = "Referenced record does not exist"
                error_code = "FOREIGN_KEY_VIOLATION"
                
            self.logger.warning(f"Database integrity error: {error_message}", context, exc)
            
        elif isinstance(exc, DataError):
            # Handle data type/format errors
            error_message = "Invalid data format"
            error_code = "INVALID_DATA_FORMAT"
            status_code = status.HTTP_400_BAD_REQUEST
            
            self.logger.warning("Database data error", context, exc)
            
        else:
            # Generic database error
            error_message = "Database service temporarily unavailable"
            error_code = "DATABASE_ERROR"
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            
            self.logger.error("Database error", context, exc)
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": "database_error",
                    "code": error_code,
                    "message": error_message,
                    "request_id": request_id,
                    "timestamp": time.time()
                }
            },
            headers={"X-Request-ID": request_id}
        )

    async def _handle_unexpected_error(
        self, 
        request: Request, 
        exc: Exception, 
        start_time: float
    ) -> JSONResponse:
        """Handle unexpected errors"""
        duration = time.time() - start_time
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        context = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "duration_ms": round(duration * 1000, 2),
            "error_type": type(exc).__name__,
            "traceback": traceback.format_exc()
        }
        
        self.logger.critical("Unexpected error", context, exc)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "internal_error",
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "request_id": request_id,
                    "timestamp": time.time()
                }
            },
            headers={"X-Request-ID": request_id}
        )


class GreekBusinessErrorHandler:
    """
    Specialized error handler for Greek business logic
    """
    
    @staticmethod
    def afm_validation_error(afm: str) -> HTTPException:
        """Handle AFM validation errors"""
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid Greek AFM: {afm}",
            headers={"X-Error-Code": "INVALID_AFM"}
        )
    
    @staticmethod
    def vat_calculation_error(context: str) -> HTTPException:
        """Handle VAT calculation errors"""
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"VAT calculation error: {context}",
            headers={"X-Error-Code": "VAT_CALCULATION_ERROR"}
        )
    
    @staticmethod
    def aade_integration_error(operation: str, message: str) -> HTTPException:
        """Handle AADE integration errors"""
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AADE {operation} failed: {message}",
            headers={"X-Error-Code": "AADE_INTEGRATION_ERROR"}
        )
    
    @staticmethod
    def greek_compliance_error(requirement: str) -> HTTPException:
        """Handle Greek compliance requirement errors"""
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Greek compliance requirement not met: {requirement}",
            headers={"X-Error-Code": "GREEK_COMPLIANCE_ERROR"}
        )


# Exception classes for specific business logic
class GreekBusinessException(Exception):
    """Base exception for Greek business logic errors"""
    def __init__(self, message: str, error_code: str, status_code: int = 422):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class AFMValidationException(GreekBusinessException):
    """Exception for AFM validation errors"""
    def __init__(self, afm: str, message: str = None):
        super().__init__(
            message or f"Invalid AFM: {afm}",
            "INVALID_AFM",
            422
        )


class VATCalculationException(GreekBusinessException):
    """Exception for VAT calculation errors"""
    def __init__(self, context: str):
        super().__init__(
            f"VAT calculation error: {context}",
            "VAT_CALCULATION_ERROR",
            422
        )


class AADEIntegrationException(GreekBusinessException):
    """Exception for AADE integration errors"""
    def __init__(self, operation: str, message: str):
        super().__init__(
            f"AADE {operation} failed: {message}",
            "AADE_INTEGRATION_ERROR",
            503
        )


# Utility functions for error responses
def create_error_response(
    error_code: str,
    message: str,
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> JSONResponse:
    """Create standardized error response"""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": "business_error",
                "code": error_code,
                "message": message,
                "details": details,
                "request_id": request_id or "unknown",
                "timestamp": time.time()
            }
        },
        headers={"X-Request-ID": request_id or "unknown"}
    )


def create_success_response(
    data: Any,
    message: str = "Operation completed successfully",
    request_id: Optional[str] = None
) -> JSONResponse:
    """Create standardized success response"""
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data,
            "request_id": request_id or "unknown",
            "timestamp": time.time()
        },
        headers={"X-Request-ID": request_id or "unknown"}
    ) 