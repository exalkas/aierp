"""
Greek Compliance Middleware
Handles Greek business requirements, AADE integration, and tax compliance
"""

import logging
import re
from typing import Optional, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timezone

from app.core.config import settings

logger = logging.getLogger(__name__)


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
        
        try:
            # Add Greek business context to request
            await self._add_greek_context(request)
            
            # Validate Greek business data in request
            validation_error = await self._validate_greek_data(request)
            if validation_error:
                return validation_error
            
            # Process request
            response = await call_next(request)
            
            # Add Greek compliance headers to response
            self._add_compliance_headers(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Greek compliance error: {e}")
            # Continue processing - don't block requests for compliance errors
            return await call_next(request)
    
    async def _add_greek_context(self, request: Request):
        """Add Greek business context to request"""
        
        # Set Greek timezone
        request.state.timezone = settings.DEFAULT_TIMEZONE
        
        # Set Greek locale for formatting
        request.state.locale = settings.GREEK_LOCALE
        
        # Set currency
        request.state.currency = settings.GREEK_CURRENCY
        
        # Add VAT rates
        request.state.vat_rates = {
            "standard": settings.DEFAULT_VAT_RATE,
            "reduced_1": settings.REDUCED_VAT_RATE_1,
            "reduced_2": settings.REDUCED_VAT_RATE_2,
            "zero": settings.ZERO_VAT_RATE
        }
        
        # Check if AADE integration is enabled
        request.state.aade_enabled = bool(settings.AADE_SUBSCRIPTION_KEY)
        request.state.aade_sandbox = settings.AADE_ENABLE_SANDBOX
    
    async def _validate_greek_data(self, request: Request) -> Optional[JSONResponse]:
        """Validate Greek business data in request"""
        
        if request.method in ["GET", "DELETE"]:
            return None
        
        try:
            # Get request body for validation
            body = await request.body()
            if not body:
                return None
            
            import json
            try:
                data = json.loads(body.decode())
            except:
                return None  # Skip validation for non-JSON data
            
            # Validate AFM (Greek Tax Number)
            afm_error = self._validate_afm_in_data(data)
            if afm_error:
                return afm_error
            
            # Validate DOY (Greek Tax Office)
            doy_error = self._validate_doy_in_data(data)
            if doy_error:
                return doy_error
            
            # Validate Greek phone numbers
            phone_error = self._validate_greek_phone_in_data(data)
            if phone_error:
                return phone_error
            
            # Validate VAT calculations
            vat_error = self._validate_vat_in_data(data)
            if vat_error:
                return vat_error
                
        except Exception as e:
            logger.warning(f"Greek validation error: {e}")
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
                    if isinstance(value, (str, int, float)) and value:
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
            return False
        
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
            return False
        
        # Remove spaces and check format
        doy = doy.replace(" ", "").upper()
        return self.DOY_PATTERN.match(doy) is not None
    
    def _validate_greek_phone(self, phone: str) -> bool:
        """Validate Greek phone number"""
        if not phone or not isinstance(phone, str):
            return False
        
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
        
        # Add AADE status if enabled
        if settings.AADE_SUBSCRIPTION_KEY:
            status = "sandbox" if settings.AADE_ENABLE_SANDBOX else "production"
            response.headers["X-AADE-Status"] = status 