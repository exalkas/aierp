"""
Supplier Invoice VAT Validation Service
Validates supplier invoices for VAT inconsistencies and provides suggestions
"""

from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func

from ..models.product_vat_config import (
    ProductVATConfig, VATSuggestionRule, VATSuggestionConfidence, 
    SupplierInvoiceVATValidation
)
from ..models.product import Product
from ..models.business_entity import BusinessEntity
from ..models.invoice import Invoice, InvoiceItem
from ..models.company import Company
from .vat_suggestion_service import VATSuggestionService, VATSuggestionRequest

logger = logging.getLogger(__name__)


class SupplierInvoiceVATValidationRequest:
    """Request for supplier invoice VAT validation"""
    
    def __init__(
        self,
        company_id: str,
        invoice_id: str,
        supplier_id: str,
        line_items: List[Dict[str, Any]],
        validation_context: Dict[str, Any] = None
    ):
        self.company_id = company_id
        self.invoice_id = invoice_id
        self.supplier_id = supplier_id
        self.line_items = line_items
        self.validation_context = validation_context or {}


class SupplierInvoiceVATValidationResult:
    """Result of supplier invoice VAT validation"""
    
    def __init__(
        self,
        validation_status: str,
        total_inconsistencies: int,
        total_items_checked: int,
        validation_details: Dict[str, Any],
        suggestions: List[Dict[str, Any]] = None
    ):
        self.validation_status = validation_status
        self.total_inconsistencies = total_inconsistencies
        self.total_items_checked = total_items_checked
        self.validation_details = validation_details
        self.suggestions = suggestions or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "validation_status": self.validation_status,
            "total_inconsistencies": self.total_inconsistencies,
            "total_items_checked": self.total_items_checked,
            "validation_details": self.validation_details,
            "suggestions": self.suggestions
        }


class SupplierInvoiceVATValidationService:
    """
    Supplier Invoice VAT Validation Service
    Validates supplier invoices for VAT inconsistencies and provides suggestions
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.vat_suggestion_service = VATSuggestionService(db)
        self.tolerance_threshold = Decimal('0.01')  # 1% tolerance for VAT rate differences
    
    def validate_supplier_invoice(
        self, 
        request: SupplierInvoiceVATValidationRequest
    ) -> SupplierInvoiceVATValidationResult:
        """
        Validate supplier invoice VAT rates against expected rates
        """
        try:
            validation_details = {
                "line_items": [],
                "summary": {},
                "timestamp": datetime.now().isoformat()
            }
            
            inconsistencies = 0
            total_items = len(request.line_items)
            
            # Validate each line item
            for i, line_item in enumerate(request.line_items):
                item_result = self._validate_line_item(line_item, request, i + 1)
                validation_details["line_items"].append(item_result)
                
                if item_result.get("inconsistency_detected", False):
                    inconsistencies += 1
            
            # Determine overall validation status
            validation_status = self._determine_validation_status(inconsistencies, total_items)
            
            # Generate summary
            validation_details["summary"] = {
                "total_items": total_items,
                "inconsistencies": inconsistencies,
                "accuracy_percentage": ((total_items - inconsistencies) / total_items * 100) if total_items > 0 else 0,
                "validation_date": datetime.now().isoformat()
            }
            
            # Generate suggestions
            suggestions = self._generate_validation_suggestions(validation_details)
            
            result = SupplierInvoiceVATValidationResult(
                validation_status=validation_status,
                total_inconsistencies=inconsistencies,
                total_items_checked=total_items,
                validation_details=validation_details,
                suggestions=suggestions
            )
            
            # Save validation result
            self._save_validation_result(request, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in supplier invoice VAT validation: {str(e)}")
            return self._get_error_result(str(e))
    
    def _validate_line_item(
        self, 
        line_item: Dict[str, Any], 
        request: SupplierInvoiceVATValidationRequest,
        line_number: int
    ) -> Dict[str, Any]:
        """Validate a single line item"""
        
        product_name = line_item.get("product_name", "")
        product_category = line_item.get("product_category", "")
        supplier_vat_rate = Decimal(str(line_item.get("vat_rate", 0)))
        
        # Get expected VAT rate
        expected_vat_result = self._get_expected_vat_rate(
            product_name, product_category, request
        )
        
        expected_vat_rate = expected_vat_result["rate"]
        
        # Check for inconsistency
        rate_difference = abs(supplier_vat_rate - expected_vat_rate)
        inconsistency_detected = rate_difference > self.tolerance_threshold
        
        # Generate suggestion if inconsistent
        suggestion = ""
        confidence = "medium"
        
        if inconsistency_detected:
            suggestion = self._generate_inconsistency_suggestion(
                supplier_vat_rate, expected_vat_rate, expected_vat_result
            )
            confidence = expected_vat_result.get("confidence", "medium")
        
        return {
            "line_number": line_number,
            "product_name": product_name,
            "product_category": product_category,
            "supplier_vat_rate": float(supplier_vat_rate),
            "expected_vat_rate": float(expected_vat_rate),
            "rate_difference": float(rate_difference),
            "inconsistency_detected": inconsistency_detected,
            "suggestion": suggestion,
            "confidence": confidence,
            "expected_vat_reasoning": expected_vat_result.get("reasoning", ""),
            "legal_reference": expected_vat_result.get("legal_reference", "")
        }
    
    def _get_expected_vat_rate(
        self, 
        product_name: str, 
        product_category: str, 
        request: SupplierInvoiceVATValidationRequest
    ) -> Dict[str, Any]:
        """Get expected VAT rate for a product"""
        
        # First check if we have a configured VAT rate for this product
        existing_config = self._get_product_vat_config(product_name, request.company_id)
        if existing_config:
            return {
                "rate": existing_config.vat_rate,
                "reasoning": f"Based on your configured VAT rate for {product_name}",
                "confidence": "high",
                "source": "user_configuration"
            }
        
        # Get suggestion from VAT suggestion service
        suggestion_request = VATSuggestionRequest(
            company_id=request.company_id,
            product_name=product_name,
            product_category=product_category,
            business_type=request.validation_context.get("business_type"),
            location_type=request.validation_context.get("location_type", "mainland"),
            context_hints=request.validation_context.get("context_hints", [])
        )
        
        suggestion_result = self.vat_suggestion_service.suggest_vat_rate(suggestion_request)
        
        return {
            "rate": suggestion_result.suggested_rate,
            "reasoning": suggestion_result.reasoning,
            "confidence": suggestion_result.confidence.value,
            "legal_reference": suggestion_result.legal_reference,
            "source": "system_suggestion"
        }
    
    def _get_product_vat_config(self, product_name: str, company_id: str) -> Optional[ProductVATConfig]:
        """Get existing product VAT configuration"""
        
        # Try to find by exact product match
        product = self.db.query(Product).filter(
            Product.company_id == company_id,
            Product.name == product_name
        ).first()
        
        if product:
            return self.db.query(ProductVATConfig).filter(
                ProductVATConfig.product_id == product.id
            ).first()
        
        return None
    
    def _generate_inconsistency_suggestion(
        self, 
        supplier_rate: Decimal, 
        expected_rate: Decimal, 
        expected_vat_result: Dict[str, Any]
    ) -> str:
        """Generate suggestion for VAT inconsistency"""
        
        if supplier_rate > expected_rate:
            return f"Supplier charged {supplier_rate}% VAT but we expect {expected_rate}% based on {expected_vat_result['reasoning']}. Consider checking if this is correct."
        else:
            return f"Supplier charged {supplier_rate}% VAT but we expect {expected_rate}% based on {expected_vat_result['reasoning']}. This might be a supplier error."
    
    def _determine_validation_status(self, inconsistencies: int, total_items: int) -> str:
        """Determine overall validation status"""
        
        if inconsistencies == 0:
            return "clean"
        elif inconsistencies / total_items <= 0.2:  # 20% threshold
            return "has_inconsistencies"
        else:
            return "needs_review"
    
    def _generate_validation_suggestions(
        self, 
        validation_details: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate general validation suggestions"""
        
        suggestions = []
        
        inconsistent_items = [
            item for item in validation_details["line_items"] 
            if item["inconsistency_detected"]
        ]
        
        if not inconsistent_items:
            suggestions.append({
                "type": "success",
                "message": "All VAT rates match expected values",
                "action": "no_action_required"
            })
        else:
            # Group by common issues
            high_confidence_issues = [
                item for item in inconsistent_items 
                if item["confidence"] == "high"
            ]
            
            if high_confidence_issues:
                suggestions.append({
                    "type": "warning",
                    "message": f"{len(high_confidence_issues)} items have high-confidence VAT inconsistencies",
                    "action": "review_high_confidence_items",
                    "items": [item["line_number"] for item in high_confidence_issues]
                })
            
            # Common rate patterns
            rate_patterns = {}
            for item in inconsistent_items:
                supplier_rate = item["supplier_vat_rate"]
                if supplier_rate not in rate_patterns:
                    rate_patterns[supplier_rate] = []
                rate_patterns[supplier_rate].append(item["line_number"])
            
            for rate, lines in rate_patterns.items():
                if len(lines) > 1:
                    suggestions.append({
                        "type": "info",
                        "message": f"Multiple items ({len(lines)}) have {rate}% VAT from supplier",
                        "action": "check_supplier_vat_policy",
                        "items": lines
                    })
        
        return suggestions
    
    def _save_validation_result(
        self, 
        request: SupplierInvoiceVATValidationRequest,
        result: SupplierInvoiceVATValidationResult
    ):
        """Save validation result to database"""
        
        try:
            validation_record = SupplierInvoiceVATValidation(
                company_id=request.company_id,
                invoice_id=request.invoice_id,
                supplier_id=request.supplier_id,
                validation_status=result.validation_status,
                total_inconsistencies=result.total_inconsistencies,
                total_items_checked=result.total_items_checked,
                validation_details=result.validation_details,
                user_decisions={}
            )
            
            self.db.add(validation_record)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error saving validation result: {str(e)}")
            self.db.rollback()
    
    def _get_error_result(self, error_message: str) -> SupplierInvoiceVATValidationResult:
        """Return error result"""
        
        return SupplierInvoiceVATValidationResult(
            validation_status="error",
            total_inconsistencies=0,
            total_items_checked=0,
            validation_details={
                "error": error_message,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def record_user_decision(
        self,
        validation_id: str,
        line_number: int,
        action: str,
        user_notes: str = "",
        decided_by: str = ""
    ) -> bool:
        """Record user decision about VAT inconsistency"""
        
        try:
            validation = self.db.query(SupplierInvoiceVATValidation).filter(
                SupplierInvoiceVATValidation.id == validation_id
            ).first()
            
            if not validation:
                return False
            
            # Update user decisions
            if not validation.user_decisions:
                validation.user_decisions = {}
            
            validation.user_decisions[f"line_{line_number}"] = {
                "action": action,
                "user_notes": user_notes,
                "decided_at": datetime.now().isoformat(),
                "decided_by": decided_by
            }
            
            # Check if this decision can improve suggestions
            self._learn_from_user_decision(validation, line_number, action, user_notes)
            
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error recording user decision: {str(e)}")
            self.db.rollback()
            return False
    
    def _learn_from_user_decision(
        self,
        validation: SupplierInvoiceVATValidation,
        line_number: int,
        action: str,
        user_notes: str
    ):
        """Learn from user decision to improve future suggestions"""
        
        # Find the specific line item
        line_item = None
        for item in validation.validation_details.get("line_items", []):
            if item["line_number"] == line_number:
                line_item = item
                break
        
        if not line_item:
            return
        
        # Extract learning data
        learning_data = {
            "product_name": line_item["product_name"],
            "product_category": line_item.get("product_category", ""),
            "supplier_vat_rate": line_item["supplier_vat_rate"],
            "expected_vat_rate": line_item["expected_vat_rate"],
            "user_action": action,
            "user_notes": user_notes,
            "decision_date": datetime.now().isoformat()
        }
        
        # Update learning data
        if not validation.learning_data:
            validation.learning_data = {}
        
        validation.learning_data[f"line_{line_number}"] = learning_data
        
        # Mark as improving suggestions if user provided useful feedback
        if action in ["accept_supplier_rate", "correct_rate"] and user_notes:
            validation.improves_suggestions = True
    
    def get_validation_history(
        self, 
        company_id: str, 
        supplier_id: str = None,
        limit: int = 50
    ) -> List[SupplierInvoiceVATValidation]:
        """Get validation history for a company"""
        
        query = self.db.query(SupplierInvoiceVATValidation).filter(
            SupplierInvoiceVATValidation.company_id == company_id
        )
        
        if supplier_id:
            query = query.filter(SupplierInvoiceVATValidation.supplier_id == supplier_id)
        
        return query.order_by(desc(SupplierInvoiceVATValidation.created_at)).limit(limit).all()
    
    def get_validation_statistics(self, company_id: str) -> Dict[str, Any]:
        """Get validation statistics for a company"""
        
        total_validations = self.db.query(SupplierInvoiceVATValidation).filter(
            SupplierInvoiceVATValidation.company_id == company_id
        ).count()
        
        clean_validations = self.db.query(SupplierInvoiceVATValidation).filter(
            SupplierInvoiceVATValidation.company_id == company_id,
            SupplierInvoiceVATValidation.validation_status == "clean"
        ).count()
        
        inconsistent_validations = self.db.query(SupplierInvoiceVATValidation).filter(
            SupplierInvoiceVATValidation.company_id == company_id,
            SupplierInvoiceVATValidation.validation_status == "has_inconsistencies"
        ).count()
        
        needs_review_validations = self.db.query(SupplierInvoiceVATValidation).filter(
            SupplierInvoiceVATValidation.company_id == company_id,
            SupplierInvoiceVATValidation.validation_status == "needs_review"
        ).count()
        
        return {
            "total_validations": total_validations,
            "clean_validations": clean_validations,
            "inconsistent_validations": inconsistent_validations,
            "needs_review_validations": needs_review_validations,
            "accuracy_percentage": (clean_validations / total_validations * 100) if total_validations > 0 else 0
        } 