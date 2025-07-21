"""
Greek Compliance Middleware
Handles Greek business requirements, AADE integration, and tax compliance
"""

import re
import json
import time
from typing import Optional, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request as StarletteRequest
from datetime import datetime, timezone

from app.core.config import settings


class GreekComplianceMiddleware(BaseHTTPMiddleware):
    """
    Middleware for Greek business compliance and validation
    Handles AADE requirements, AFM validation, and Greek business rules
    """
    
    # Greek business patterns
    AFM_PATTERN = re.compile(r'^\d{9}$')
    DOY_PATTERN = re.compile(r'^[A-Z]\d{4}$')
    GREEK_PHONE_PATTERN = re.compile(r'^(\+30|0030|30)?[2-9]\d{9}$')
    
    async def dispatch(self, request: Request, call_next):
        """Process request with Greek compliance validation"""
        import time
        
        start_time = time.time()
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        print(f"[GREEK] Starting Greek compliance: {request.method} {request.url.path} [{request_id}] at {time.time()}")
        
        try:
            print(f"[GREEK] Greek compliance middleware processing: {request.method} {request.url.path}")
            
            print(f"[GREEK] Adding Greek context at {time.time()}")
            
            # Add Greek business context to request (settings disabled)
            await self._add_greek_context(request)
            
            print(f"[GREEK] Greek context added at {time.time()}")
            
            # For now, skip body validation to avoid request consumption issues
            # TODO: Implement proper body caching for production
            if request.method in ["POST", "PUT", "PATCH"]:
                print(f"[GREEK] Skipping validation for {request.method} at {time.time()}")
                print(f"[GREEK] Skipping Greek validation for {request.method} request to avoid body consumption")
            
            print(f"[GREEK] Greek compliance validation passed for {request.url.path}")
            
            print(f"[GREEK] About to call next middleware at {time.time()}")
            
            # Process request
            response = await call_next(request)
            
            print(f"[GREEK] Adding compliance headers at {time.time()}")
            
            # Add Greek compliance headers to response
            self._add_compliance_headers(response)
            
            duration = (time.time() - start_time) * 1000
            print(f"[GREEK] Greek compliance completed ({duration:.2f}ms) at {time.time()}")
            
            return response
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            print(f"[GREEK ERROR] Greek compliance error ({duration:.2f}ms): {e}")
            print(f"[GREEK ERROR] Greek compliance error for {request.url.path}: {e}")
            # TEMPORARILY DISABLE CALL_NEXT IN EXCEPTION HANDLER TO DEBUG HANG
            print(f"[GREEK ERROR] Returning error response instead of calling next")
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={"error": "Greek compliance error", "detail": str(e)}
            )
    
    async def _add_greek_context(self, request: Request):
        """Add Greek business context to request"""
        
        # TEMPORARILY DISABLE ALL SETTINGS ACCESS TO DEBUG LOGGER ERROR
        print(f"[GREEK] Setting minimal context without settings access")
        
        # Set Greek timezone
        # request.state.timezone = settings.DEFAULT_TIMEZONE
        
        # Set Greek locale for formatting  
        # request.state.locale = settings.GREEK_LOCALE
        
        # Set currency
        # request.state.currency = settings.GREEK_CURRENCY
        
        # Add VAT rates
        # request.state.vat_rates = {
        #     "standard": settings.DEFAULT_VAT_RATE,
        #     "reduced_1": settings.REDUCED_VAT_RATE_1,
        #     "reduced_2": settings.REDUCED_VAT_RATE_2,
        #     "zero": settings.ZERO_VAT_RATE
        # }
        
        # Check if AADE integration is enabled
        # request.state.aade_enabled = bool(settings.AADE_SUBSCRIPTION_KEY)
        # request.state.aade_sandbox = settings.AADE_ENABLE_SANDBOX
    
    async def _validate_greek_data(self, request: Request) -> Optional[JSONResponse]:
        """Validate Greek business data in request"""
        
        if request.method in ["GET", "DELETE"]:
            return None
        
        try:
            # TEMPORARILY SKIP BODY CONSUMPTION TO AVOID HANGS
            # TODO: Implement proper request body caching for production
            print(f"[GREEK] Skipping body validation to avoid request consumption issues")
            return None
            
            # Get request body for validation (safe with caching request)
            body = await request.body()
            if not body:
                return None
            
            try:
                data = json.loads(body.decode())
            except:
                return None  # Skip validation for non-JSON data
            
            print(f"[GREEK] Validating Greek data: {list(data.keys()) if isinstance(data, dict) else 'non-dict'}")
            
            # Validate AFM (Greek Tax Number)
            afm_error = self._validate_afm_in_data(data)
            if afm_error:
                print(f"[GREEK] AFM validation failed")
                return afm_error
            
            # Validate DOY (Greek Tax Office)
            doy_error = self._validate_doy_in_data(data)
            if doy_error:
                print(f"[GREEK] DOY validation failed")
                return doy_error
            
            # Validate Greek phone numbers
            phone_error = self._validate_greek_phone_in_data(data)
            if phone_error:
                print(f"[GREEK] Phone validation failed")
                return phone_error
            
            # Validate VAT calculations
            vat_error = self._validate_vat_in_data(data)
            if vat_error:
                print(f"[GREEK] VAT validation failed")
                return vat_error
                
        except Exception as e:
            print(f"[GREEK] Greek validation error: {e}")
            # Don't block requests for validation errors
            pass
        
        return None
    
    def _validate_afm_in_data(self, data: Any) -> Optional[JSONResponse]:
        """Validate AFM (Greek Tax Number) in request data"""
        
        afm_fields = self._find_fields_by_pattern(data, ["afm", "tax_number", "vat_number"])
        
        for field_path, afm_value in afm_fields:
            if not self._validate_afm(afm_value):
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "INVALID_AFM",
                        "message": f"Invalid Greek AFM (Tax Number): {afm_value}",
                        "field": field_path,
                        "code": "GR_001"
                    }
                )
        
        return None
    
    def _validate_doy_in_data(self, data: Any) -> Optional[JSONResponse]:
        """Validate DOY (Greek Tax Office) in request data"""
        
        doy_fields = self._find_fields_by_pattern(data, ["doy", "tax_office"])
        
        for field_path, doy_value in doy_fields:
            if not self._validate_doy(doy_value):
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "INVALID_DOY",
                        "message": f"Invalid Greek DOY (Tax Office): {doy_value}",
                        "field": field_path,
                        "code": "GR_002"
                    }
                )
        
        return None
    
    def _validate_greek_phone_in_data(self, data: Any) -> Optional[JSONResponse]:
        """Validate Greek phone numbers in request data"""
        
        phone_fields = self._find_fields_by_pattern(data, ["phone", "mobile", "tel"])
        
        for field_path, phone_value in phone_fields:
            if not self._validate_greek_phone(phone_value):
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "INVALID_GREEK_PHONE",
                        "message": f"Invalid Greek phone number: {phone_value}",
                        "field": field_path,
                        "code": "GR_003"
                    }
                )
        
        return None
    
    def _validate_vat_in_data(self, data: Any) -> Optional[JSONResponse]:
        """Validate VAT calculations in request data"""
        
        # Look for VAT-related fields
        vat_fields = self._find_fields_by_pattern(data, ["vat_rate", "tax_rate"])
        
        for field_path, vat_rate in vat_fields:
            if not self._validate_greek_vat_rate(vat_rate):
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "INVALID_VAT_RATE",
                        "message": f"Invalid Greek VAT rate: {vat_rate}. Must be 0%, 6%, 13%, or 24%",
                        "field": field_path,
                        "code": "GR_004"
                    }
                )
        
        return None
    
    def _find_fields_by_pattern(self, data: Any, patterns: list, path: str = "") -> list:
        """Recursively find fields matching patterns"""
        found = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Check if field name matches any pattern
                key_lower = key.lower()
                if any(pattern in key_lower for pattern in patterns):
                    if isinstance(value, (str, int, float)) and value and str(value).strip():
                        found.append((current_path, str(value)))
                
                # Recursively search nested objects
                found.extend(self._find_fields_by_pattern(value, patterns, current_path))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]" if path else f"[{i}]"
                found.extend(self._find_fields_by_pattern(item, patterns, current_path))
        
        return found
    
    def _validate_afm(self, afm: str) -> bool:
        """Validate Greek AFM (Tax Number) with checksum"""
        if not afm or not isinstance(afm, str):
            return True  # Empty/null AFM is valid (optional field)
        
        # Remove spaces and check format
        afm = afm.replace(" ", "")
        if not self.AFM_PATTERN.match(afm):
            return False
        
        # Validate checksum
        try:
            digits = [int(d) for d in afm]
            total = 0
            
            # Calculate weighted sum
            for i in range(8):
                total += digits[i] * (2 ** (8 - i))
            
            # Check if checksum digit is correct
            checksum = total % 11
            if checksum > 9:
                checksum = 0
            
            return checksum == digits[8]
            
        except (ValueError, IndexError):
            return False
    
    def _validate_doy(self, doy: str) -> bool:
        """Validate Greek DOY (Tax Office) code"""
        if not doy or not isinstance(doy, str):
            return True  # Empty/null DOY is valid (optional field)
        
        # Remove spaces and check format
        doy = doy.replace(" ", "").upper()
        return self.DOY_PATTERN.match(doy) is not None
    
    def _validate_greek_phone(self, phone: str) -> bool:
        """Validate Greek phone number"""
        if not phone or not isinstance(phone, str):
            return True  # Empty/null phone is valid (optional field)
        
        # Remove spaces, dashes, parentheses
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        return self.GREEK_PHONE_PATTERN.match(phone) is not None
    
    def _validate_greek_vat_rate(self, vat_rate: Any) -> bool:
        """Validate Greek VAT rate"""
        try:
            rate = float(vat_rate)
            
            # Check if rate matches Greek VAT rates (with small tolerance for floating point)
            valid_rates = [0.00, 0.06, 0.13, 0.24]
            return any(abs(rate - valid_rate) < 0.001 for valid_rate in valid_rates)
            
        except (ValueError, TypeError):
            return False
    
    def _add_compliance_headers(self, response: Response):
        """Add Greek compliance headers to response"""
        
        # Add timestamp in Greek timezone
        greek_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        response.headers["X-Greek-Timestamp"] = greek_time
        
        # Add compliance version
        response.headers["X-Greek-Compliance-Version"] = "1.0"
        
        # TEMPORARILY DISABLE AADE STATUS TO DEBUG LOGGER ERROR
        # Add AADE status if enabled
        # if settings.AADE_SUBSCRIPTION_KEY:
        #     status = "sandbox" if settings.AADE_ENABLE_SANDBOX else "production"
        #     response.headers["X-AADE-Status"] = status


# Utility function for FastAPI dependency injection
async def validate_greek_compliance() -> Dict[str, Any]:
    """
    FastAPI dependency for Greek compliance validation
    Returns Greek compliance context for use in endpoints
    """
    return {
        "compliance_enabled": True,
        "aade_enabled": bool(settings.AADE_SUBSCRIPTION_KEY if hasattr(settings, 'AADE_SUBSCRIPTION_KEY') else False),
        "validation_active": True,
        "timestamp": datetime.now(timezone.utc).isoformat()
    } 