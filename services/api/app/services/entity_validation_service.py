"""
Entity Validation Service for Greek ERP/CRM System
Provides validation for dynamic entities and fields with Greek compliance
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
import re
import json
from decimal import Decimal, InvalidOperation
from sqlalchemy.orm import Session

from ..models.dynamic_entity import DynamicEntity
from ..models.dynamic_field import DynamicField, FieldType
from ..utils.greek_validation import validate_afm, validate_amka, validate_greek_phone
from ..models.greek_reference_data import GreekTaxOffice, GreekRegion


class ValidationError:
    """Represents a validation error"""
    def __init__(self, field: str, message: str, code: str = "VALIDATION_ERROR"):
        self.field = field
        self.message = message
        self.code = code
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "field": self.field,
            "message": self.message,
            "code": self.code
        }


class EntityValidationService:
    """Service for validating dynamic entities and their field values"""

    def __init__(self, db: Session):
        self.db = db

    def validate_entity_data(
        self, 
        entity: DynamicEntity, 
        data: Dict[str, Any],
        is_create: bool = True
    ) -> Tuple[bool, List[ValidationError]]:
        """
        Validate data against entity field definitions
        
        Args:
            entity: The dynamic entity
            data: Data to validate
            is_create: Whether this is a create operation (affects required field validation)
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        # Get all fields for this entity
        fields = self.db.query(DynamicField).filter(
            DynamicField.entity_id == entity.id,
            DynamicField.is_visible == True
        ).all()
        
        # Validate each field
        for field in fields:
            field_errors = self._validate_field(field, data.get(field.name), is_create)
            errors.extend(field_errors)
        
        # Check for unknown fields
        field_names = {field.name for field in fields}
        for key in data.keys():
            if key not in field_names and not key.startswith('_'):  # Allow metadata fields
                errors.append(ValidationError(
                    field=key,
                    message=f"Unknown field '{key}' for entity '{entity.name}'",
                    code="UNKNOWN_FIELD"
                ))
        
        return len(errors) == 0, errors

    def _validate_field(
        self, 
        field: DynamicField, 
        value: Any, 
        is_create: bool = True
    ) -> List[ValidationError]:
        """Validate a single field value"""
        errors = []
        
        # Handle null/empty values
        if value is None or (isinstance(value, str) and value.strip() == ""):
            if field.is_required and (is_create or not field.is_readonly):
                errors.append(ValidationError(
                    field=field.name,
                    message=f"Field '{field.display_name}' is required",
                    code="REQUIRED_FIELD"
                ))
            return errors  # No further validation for empty values
        
        # Convert value to string for validation
        str_value = str(value).strip() if value is not None else ""
        
        # Type-specific validation
        try:
            if field.field_type == FieldType.TEXT:
                errors.extend(self._validate_text(field, str_value))
            elif field.field_type == FieldType.NUMBER:
                errors.extend(self._validate_number(field, value))
            elif field.field_type == FieldType.EMAIL:
                errors.extend(self._validate_email(field, str_value))
            elif field.field_type == FieldType.URL:
                errors.extend(self._validate_url(field, str_value))
            elif field.field_type == FieldType.PHONE:
                errors.extend(self._validate_phone(field, str_value))
            elif field.field_type == FieldType.DATE:
                errors.extend(self._validate_date(field, value))
            elif field.field_type == FieldType.DATETIME:
                errors.extend(self._validate_datetime(field, value))
            elif field.field_type == FieldType.SELECT:
                errors.extend(self._validate_select(field, str_value))
            elif field.field_type == FieldType.MULTISELECT:
                errors.extend(self._validate_multiselect(field, value))
            elif field.field_type == FieldType.AFM:
                errors.extend(self._validate_afm(field, str_value))
            elif field.field_type == FieldType.AMKA:
                errors.extend(self._validate_amka(field, str_value))
            elif field.field_type == FieldType.GREEK_PHONE:
                errors.extend(self._validate_greek_phone(field, str_value))
            elif field.field_type == FieldType.DOY_SELECTOR:
                errors.extend(self._validate_doy(field, str_value))
            elif field.field_type == FieldType.REGION_SELECTOR:
                errors.extend(self._validate_region(field, str_value))
            
            # Custom regex validation
            if field.regex_pattern and str_value:
                if not re.match(field.regex_pattern, str_value):
                    message = field.validation_message or f"Value does not match required pattern"
                    errors.append(ValidationError(
                        field=field.name,
                        message=message,
                        code="PATTERN_MISMATCH"
                    ))
                    
        except Exception as e:
            errors.append(ValidationError(
                field=field.name,
                message=f"Validation error: {str(e)}",
                code="VALIDATION_EXCEPTION"
            ))
        
        return errors

    def _validate_text(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate text field"""
        errors = []
        
        if field.min_length and len(value) < field.min_length:
            errors.append(ValidationError(
                field=field.name,
                message=f"Minimum length is {field.min_length} characters",
                code="MIN_LENGTH"
            ))
        
        if field.max_length and len(value) > field.max_length:
            errors.append(ValidationError(
                field=field.name,
                message=f"Maximum length is {field.max_length} characters",
                code="MAX_LENGTH"
            ))
        
        return errors

    def _validate_number(self, field: DynamicField, value: Any) -> List[ValidationError]:
        """Validate number field"""
        errors = []
        
        try:
            if isinstance(value, str):
                num_value = Decimal(value)
            elif isinstance(value, (int, float)):
                num_value = Decimal(str(value))
            else:
                num_value = Decimal(value)
                
            if field.min_value is not None and num_value < field.min_value:
                errors.append(ValidationError(
                    field=field.name,
                    message=f"Minimum value is {field.min_value}",
                    code="MIN_VALUE"
                ))
            
            if field.max_value is not None and num_value > field.max_value:
                errors.append(ValidationError(
                    field=field.name,
                    message=f"Maximum value is {field.max_value}",
                    code="MAX_VALUE"
                ))
                
        except (InvalidOperation, ValueError, TypeError):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid number format",
                code="INVALID_NUMBER"
            ))
        
        return errors

    def _validate_email(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate email field"""
        errors = []
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid email format",
                code="INVALID_EMAIL"
            ))
        
        return errors

    def _validate_url(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate URL field"""
        errors = []
        
        url_pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        if not re.match(url_pattern, value):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid URL format",
                code="INVALID_URL"
            ))
        
        return errors

    def _validate_phone(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate phone field"""
        errors = []
        
        # Basic phone validation - can be enhanced
        phone_pattern = r'^\+?[\d\s\-\(\)]{7,15}$'
        if not re.match(phone_pattern, value):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid phone number format",
                code="INVALID_PHONE"
            ))
        
        return errors

    def _validate_date(self, field: DynamicField, value: Any) -> List[ValidationError]:
        """Validate date field"""
        errors = []
        
        try:
            if isinstance(value, str):
                # Try to parse ISO date format
                datetime.fromisoformat(value.replace('Z', '+00:00'))
            elif not isinstance(value, (date, datetime)):
                raise ValueError("Invalid date type")
        except (ValueError, TypeError):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid date format",
                code="INVALID_DATE"
            ))
        
        return errors

    def _validate_datetime(self, field: DynamicField, value: Any) -> List[ValidationError]:
        """Validate datetime field"""
        errors = []
        
        try:
            if isinstance(value, str):
                # Try to parse ISO datetime format
                datetime.fromisoformat(value.replace('Z', '+00:00'))
            elif not isinstance(value, datetime):
                raise ValueError("Invalid datetime type")
        except (ValueError, TypeError):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid datetime format",
                code="INVALID_DATETIME"
            ))
        
        return errors

    def _validate_select(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate select field"""
        errors = []
        
        if field.options:
            valid_values = [opt.get('value') for opt in field.options if isinstance(opt, dict)]
            if value not in valid_values:
                errors.append(ValidationError(
                    field=field.name,
                    message=f"Invalid selection. Valid options: {', '.join(valid_values)}",
                    code="INVALID_SELECTION"
                ))
        
        return errors

    def _validate_multiselect(self, field: DynamicField, value: Any) -> List[ValidationError]:
        """Validate multiselect field"""
        errors = []
        
        if not isinstance(value, list):
            errors.append(ValidationError(
                field=field.name,
                message="Multiselect value must be a list",
                code="INVALID_TYPE"
            ))
            return errors
        
        if field.options:
            valid_values = [opt.get('value') for opt in field.options if isinstance(opt, dict)]
            for item in value:
                if item not in valid_values:
                    errors.append(ValidationError(
                        field=field.name,
                        message=f"Invalid selection '{item}'. Valid options: {', '.join(valid_values)}",
                        code="INVALID_SELECTION"
                    ))
        
        return errors

    def _validate_afm(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate Greek AFM (Tax Number)"""
        errors = []
        
        if not validate_afm(value):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid Greek AFM (Tax Number)",
                code="INVALID_AFM"
            ))
        
        return errors

    def _validate_amka(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate Greek AMKA (Social Security Number)"""
        errors = []
        
        if not validate_amka(value):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid Greek AMKA (Social Security Number)",
                code="INVALID_AMKA"
            ))
        
        return errors

    def _validate_greek_phone(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate Greek phone number"""
        errors = []
        
        if not validate_greek_phone(value):
            errors.append(ValidationError(
                field=field.name,
                message="Invalid Greek phone number",
                code="INVALID_GREEK_PHONE"
            ))
        
        return errors

    def _validate_doy(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate Greek DOY (Tax Office)"""
        errors = []
        
        # Check if DOY exists in reference data
        doy = self.db.query(GreekTaxOffice).filter(
            GreekTaxOffice.code == value
        ).first()
        
        if not doy:
            errors.append(ValidationError(
                field=field.name,
                message="Invalid Greek Tax Office code",
                code="INVALID_DOY"
            ))
        
        return errors

    def _validate_region(self, field: DynamicField, value: str) -> List[ValidationError]:
        """Validate Greek region"""
        errors = []
        
        # Check if region exists in reference data
        region = self.db.query(GreekRegion).filter(
            GreekRegion.code == value
        ).first()
        
        if not region:
            errors.append(ValidationError(
                field=field.name,
                message="Invalid Greek region code",
                code="INVALID_REGION"
            ))
        
        return errors

    def validate_entity_schema(self, entity: DynamicEntity) -> Tuple[bool, List[ValidationError]]:
        """Validate entity schema definition"""
        errors = []
        
        # Validate entity name
        if not entity.name or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', entity.name):
            errors.append(ValidationError(
                field="name",
                message="Entity name must be a valid identifier (letters, numbers, underscore)",
                code="INVALID_ENTITY_NAME"
            ))
        
        # Validate API name
        if not entity.api_name or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_-]*$', entity.api_name):
            errors.append(ValidationError(
                field="api_name",
                message="API name must be a valid identifier",
                code="INVALID_API_NAME"
            ))
        
        # Validate table name
        if not entity.table_name or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', entity.table_name):
            errors.append(ValidationError(
                field="table_name",
                message="Table name must be a valid database identifier",
                code="INVALID_TABLE_NAME"
            ))
        
        return len(errors) == 0, errors

    def validate_field_schema(self, field: DynamicField) -> Tuple[bool, List[ValidationError]]:
        """Validate field schema definition"""
        errors = []
        
        # Validate field name
        if not field.name or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', field.name):
            errors.append(ValidationError(
                field="name",
                message="Field name must be a valid identifier",
                code="INVALID_FIELD_NAME"
            ))
        
        # Validate options for select fields
        if field.field_type in [FieldType.SELECT, FieldType.MULTISELECT, FieldType.RADIO]:
            if not field.options or len(field.options) == 0:
                errors.append(ValidationError(
                    field="options",
                    message="Select fields must have at least one option",
                    code="MISSING_OPTIONS"
                ))
        
        # Validate numeric constraints
        if field.min_length is not None and field.min_length < 0:
            errors.append(ValidationError(
                field="min_length",
                message="Minimum length cannot be negative",
                code="INVALID_MIN_LENGTH"
            ))
        
        if (field.min_length is not None and field.max_length is not None 
            and field.min_length > field.max_length):
            errors.append(ValidationError(
                field="max_length",
                message="Maximum length must be greater than minimum length",
                code="INVALID_LENGTH_RANGE"
            ))
        
        return len(errors) == 0, errors 