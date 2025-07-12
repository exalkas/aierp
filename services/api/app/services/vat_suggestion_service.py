"""
VAT Suggestion Service
Intelligent VAT rate suggestions for users based on product characteristics,
business context, and admin-configurable rules
"""

from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
from datetime import datetime
import logging
import re

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func

from ..models.product_vat_config import (
    ProductVATConfig, VATSuggestionRule, VATSuggestionConfidence, 
    SupplierInvoiceVATValidation
)
from ..models.product import Product, ProductCategory
from ..models.business_entity import BusinessEntity
from ..models.company import Company

logger = logging.getLogger(__name__)


class VATSuggestionRequest:
    """Request for VAT rate suggestion"""
    
    def __init__(
        self,
        company_id: str,
        product_name: str,
        product_category: str = None,
        business_type: str = None,
        location_type: str = "mainland",
        context_hints: List[str] = None,
        product_description: str = None,
        existing_vat_rate: Decimal = None
    ):
        self.company_id = company_id
        self.product_name = product_name
        self.product_category = product_category
        self.business_type = business_type
        self.location_type = location_type
        self.context_hints = context_hints or []
        self.product_description = product_description
        self.existing_vat_rate = existing_vat_rate


class VATSuggestionResult:
    """Result of VAT rate suggestion"""
    
    def __init__(
        self,
        suggested_rate: Decimal,
        confidence: VATSuggestionConfidence,
        reasoning: str,
        legal_reference: str = None,
        alternative_rates: List[Tuple[Decimal, str]] = None,
        matched_rules: List[str] = None
    ):
        self.suggested_rate = suggested_rate
        self.confidence = confidence
        self.reasoning = reasoning
        self.legal_reference = legal_reference
        self.alternative_rates = alternative_rates or []
        self.matched_rules = matched_rules or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "suggested_rate": float(self.suggested_rate),
            "confidence": self.confidence.value,
            "reasoning": self.reasoning,
            "legal_reference": self.legal_reference,
            "alternative_rates": [
                {"rate": float(rate), "reason": reason} 
                for rate, reason in self.alternative_rates
            ],
            "matched_rules": self.matched_rules
        }


class VATSuggestionService:
    """
    VAT Suggestion Service
    Provides intelligent VAT rate suggestions based on configurable rules
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.default_suggestions = self._load_default_suggestions()
    
    def suggest_vat_rate(self, request: VATSuggestionRequest) -> VATSuggestionResult:
        """
        Suggest VAT rate based on product characteristics and context
        """
        try:
            # Get applicable rules
            rules = self._get_applicable_rules(request)
            
            if not rules:
                return self._get_fallback_suggestion(request)
            
            # Find best matching rule
            best_rule = self._select_best_rule(rules, request)
            
            # Apply geographical adjustments
            final_rate = self._apply_geographical_adjustments(
                best_rule.suggested_rate, 
                request.location_type
            )
            
            # Generate alternative suggestions
            alternatives = self._generate_alternatives(rules, request, final_rate)
            
            return VATSuggestionResult(
                suggested_rate=final_rate,
                confidence=best_rule.confidence_level,
                reasoning=best_rule.reasoning,
                legal_reference=best_rule.legal_reference,
                alternative_rates=alternatives,
                matched_rules=[best_rule.rule_code]
            )
            
        except Exception as e:
            logger.error(f"Error in VAT suggestion: {str(e)}")
            return self._get_fallback_suggestion(request)
    
    def _get_applicable_rules(self, request: VATSuggestionRequest) -> List[VATSuggestionRule]:
        """Find rules that match the request criteria"""
        
        query = self.db.query(VATSuggestionRule).filter(
            VATSuggestionRule.is_active == True,
            VATSuggestionRule.effective_from <= datetime.now(),
            or_(
                VATSuggestionRule.effective_to.is_(None),
                VATSuggestionRule.effective_to >= datetime.now()
            )
        )
        
        # Apply filters
        conditions = []
        
        # Business type matching
        if request.business_type:
            conditions.append(
                or_(
                    VATSuggestionRule.business_type.is_(None),
                    VATSuggestionRule.business_type == request.business_type
                )
            )
        
        # Product category matching
        if request.product_category:
            conditions.append(
                or_(
                    VATSuggestionRule.product_category.is_(None),
                    VATSuggestionRule.product_category == request.product_category
                )
            )
        
        # Location type matching
        conditions.append(
            or_(
                VATSuggestionRule.location_type.is_(None),
                VATSuggestionRule.location_type == request.location_type
            )
        )
        
        if conditions:
            query = query.filter(and_(*conditions))
        
        # Get all potential rules
        rules = query.all()
        
        # Filter by keyword matching
        matching_rules = []
        for rule in rules:
            if self._matches_keywords(rule, request):
                matching_rules.append(rule)
        
        return sorted(matching_rules, key=lambda r: r.priority, reverse=True)
    
    def _matches_keywords(self, rule: VATSuggestionRule, request: VATSuggestionRequest) -> bool:
        """Check if rule keywords match the product"""
        
        if not rule.product_keywords:
            return True  # No keywords = matches all
        
        # Combine product name and description for matching
        text_to_match = f"{request.product_name} {request.product_description or ''}".lower()
        
        # Check if any keyword matches
        for keyword in rule.product_keywords:
            if keyword.lower() in text_to_match:
                return True
        
        # Check context hints
        for hint in request.context_hints:
            if hint.lower() in rule.context_hints:
                return True
        
        return False
    
    def _select_best_rule(self, rules: List[VATSuggestionRule], request: VATSuggestionRequest) -> VATSuggestionRule:
        """Select the best rule based on specificity and priority"""
        
        # Score rules based on specificity
        scored_rules = []
        for rule in rules:
            score = self._calculate_rule_score(rule, request)
            scored_rules.append((rule, score))
        
        # Sort by score (descending) then by priority (descending)
        scored_rules.sort(key=lambda x: (x[1], x[0].priority), reverse=True)
        
        return scored_rules[0][0]
    
    def _calculate_rule_score(self, rule: VATSuggestionRule, request: VATSuggestionRequest) -> int:
        """Calculate specificity score for a rule"""
        
        score = 0
        
        # More specific rules get higher scores
        if rule.business_type and rule.business_type == request.business_type:
            score += 10
        
        if rule.product_category and rule.product_category == request.product_category:
            score += 8
        
        if rule.location_type and rule.location_type == request.location_type:
            score += 6
        
        # Keyword matching bonus
        if rule.product_keywords:
            text_to_match = f"{request.product_name} {request.product_description or ''}".lower()
            for keyword in rule.product_keywords:
                if keyword.lower() in text_to_match:
                    score += 5
        
        # Context hints bonus
        for hint in request.context_hints:
            if hint.lower() in rule.context_hints:
                score += 3
        
        return score
    
    def _apply_geographical_adjustments(self, base_rate: Decimal, location_type: str) -> Decimal:
        """Apply geographical adjustments (e.g., Aegean Islands reduction)"""
        
        if location_type == "aegean_islands":
            # 30% reduction for Aegean Islands
            return base_rate * Decimal('0.70')
        
        return base_rate
    
    def _generate_alternatives(
        self, 
        rules: List[VATSuggestionRule], 
        request: VATSuggestionRequest,
        selected_rate: Decimal
    ) -> List[Tuple[Decimal, str]]:
        """Generate alternative VAT rate suggestions"""
        
        alternatives = []
        
        # Include other high-scoring rules
        for rule in rules[:3]:  # Top 3 rules
            adjusted_rate = self._apply_geographical_adjustments(
                rule.suggested_rate, 
                request.location_type
            )
            if adjusted_rate != selected_rate:
                alternatives.append((adjusted_rate, rule.reasoning))
        
        # Add common Greek VAT rates if not already included
        common_rates = [
            (Decimal('24.00'), "Standard VAT rate"),
            (Decimal('13.00'), "Reduced VAT rate for food/hospitality"),
            (Decimal('6.00'), "Reduced VAT rate for books/pharmaceuticals"),
            (Decimal('0.00'), "Zero-rated or exempt")
        ]
        
        for rate, reason in common_rates:
            adjusted_rate = self._apply_geographical_adjustments(rate, request.location_type)
            if adjusted_rate not in [alt[0] for alt in alternatives] and adjusted_rate != selected_rate:
                alternatives.append((adjusted_rate, reason))
        
        return alternatives[:3]  # Limit to 3 alternatives
    
    def _get_fallback_suggestion(self, request: VATSuggestionRequest) -> VATSuggestionResult:
        """Provide fallback suggestion when no rules match"""
        
        # Business type based fallback
        if request.business_type in ["healthcare", "legal", "education"]:
            rate = Decimal('0.00')
            reasoning = f"{request.business_type} services are typically VAT exempt in Greece"
            confidence = VATSuggestionConfidence.MEDIUM
        else:
            # Default to standard rate
            rate = Decimal('24.00')
            reasoning = "Standard VAT rate (24%) - please verify based on your specific business context"
            confidence = VATSuggestionConfidence.LOW
        
        # Apply geographical adjustments
        final_rate = self._apply_geographical_adjustments(rate, request.location_type)
        
        return VATSuggestionResult(
            suggested_rate=final_rate,
            confidence=confidence,
            reasoning=reasoning,
            legal_reference="Greek VAT Law",
            alternative_rates=[]
        )
    
    def _load_default_suggestions(self) -> Dict[str, Any]:
        """Load default VAT suggestions for common scenarios"""
        
        return {
            "healthcare": {
                "rate": Decimal('0.00'),
                "reasoning": "Healthcare services are VAT exempt",
                "confidence": VATSuggestionConfidence.HIGH
            },
            "legal": {
                "rate": Decimal('0.00'),
                "reasoning": "Legal services are VAT exempt",
                "confidence": VATSuggestionConfidence.HIGH
            },
            "education": {
                "rate": Decimal('0.00'),
                "reasoning": "Educational services are VAT exempt",
                "confidence": VATSuggestionConfidence.HIGH
            },
            "food_takeaway": {
                "rate": Decimal('13.00'),
                "reasoning": "Takeaway food and beverages have reduced VAT rate",
                "confidence": VATSuggestionConfidence.HIGH
            },
            "food_dine_in": {
                "rate": Decimal('24.00'),
                "reasoning": "Dine-in food and beverages have standard VAT rate",
                "confidence": VATSuggestionConfidence.HIGH
            },
            "default": {
                "rate": Decimal('24.00'),
                "reasoning": "Standard VAT rate",
                "confidence": VATSuggestionConfidence.MEDIUM
            }
        }
    
    def create_suggestion_rule(
        self,
        rule_name: str,
        rule_code: str,
        suggested_rate: Decimal,
        confidence: VATSuggestionConfidence,
        reasoning: str,
        business_type: str = None,
        product_category: str = None,
        product_keywords: List[str] = None,
        location_type: str = None,
        context_hints: List[str] = None,
        priority: int = 100,
        legal_reference: str = None
    ) -> VATSuggestionRule:
        """Create a new VAT suggestion rule"""
        
        rule = VATSuggestionRule(
            rule_name=rule_name,
            rule_code=rule_code,
            suggested_rate=suggested_rate,
            confidence_level=confidence,
            reasoning=reasoning,
            business_type=business_type,
            product_category=product_category,
            product_keywords=product_keywords or [],
            location_type=location_type,
            context_hints=context_hints or [],
            priority=priority,
            legal_reference=legal_reference
        )
        
        self.db.add(rule)
        self.db.commit()
        
        return rule
    
    def update_suggestion_rule(
        self,
        rule_id: str,
        updates: Dict[str, Any]
    ) -> Optional[VATSuggestionRule]:
        """Update an existing VAT suggestion rule"""
        
        rule = self.db.query(VATSuggestionRule).filter(
            VATSuggestionRule.id == rule_id
        ).first()
        
        if not rule:
            return None
        
        for key, value in updates.items():
            if hasattr(rule, key):
                setattr(rule, key, value)
        
        self.db.commit()
        return rule
    
    def get_suggestion_rules(self, is_active: bool = True) -> List[VATSuggestionRule]:
        """Get all VAT suggestion rules"""
        
        query = self.db.query(VATSuggestionRule)
        
        if is_active is not None:
            query = query.filter(VATSuggestionRule.is_active == is_active)
        
        return query.order_by(desc(VATSuggestionRule.priority)).all()


def create_default_suggestion_rules(db: Session) -> None:
    """Create default VAT suggestion rules for the system"""
    
    service = VATSuggestionService(db)
    
    default_rules = [
        # Healthcare exemption
        {
            "rule_name": "Healthcare Services VAT Exempt",
            "rule_code": "GR_HEALTHCARE_EXEMPT",
            "suggested_rate": Decimal('0.00'),
            "confidence": VATSuggestionConfidence.HIGH,
            "reasoning": "Healthcare services are VAT exempt in Greece",
            "business_type": "healthcare",
            "priority": 500,
            "legal_reference": "Greek VAT Law Article 22"
        },
        
        # Legal services exemption
        {
            "rule_name": "Legal Services VAT Exempt",
            "rule_code": "GR_LEGAL_EXEMPT",
            "suggested_rate": Decimal('0.00'),
            "confidence": VATSuggestionConfidence.HIGH,
            "reasoning": "Legal services are VAT exempt in Greece",
            "business_type": "legal",
            "priority": 500,
            "legal_reference": "Greek VAT Law Article 22"
        },
        
        # Takeaway coffee
        {
            "rule_name": "Takeaway Coffee/Beverages Reduced VAT",
            "rule_code": "GR_TAKEAWAY_COFFEE",
            "suggested_rate": Decimal('13.00'),
            "confidence": VATSuggestionConfidence.HIGH,
            "reasoning": "Takeaway coffee and beverages have 13% VAT (permanent since July 2024)",
            "business_type": "food_service",
            "product_keywords": ["coffee", "tea", "beverage", "drink"],
            "context_hints": ["takeaway", "delivery", "pickup"],
            "priority": 400,
            "legal_reference": "Greek VAT Law - Permanent Reduced Rate for Takeaway Beverages"
        },
        
        # Dine-in food service
        {
            "rule_name": "Dine-in Food Service Standard VAT",
            "rule_code": "GR_DINEIN_FOOD",
            "suggested_rate": Decimal('24.00'),
            "confidence": VATSuggestionConfidence.HIGH,
            "reasoning": "Dine-in food and beverages have standard 24% VAT",
            "business_type": "food_service",
            "context_hints": ["dine_in", "restaurant", "table_service"],
            "priority": 300,
            "legal_reference": "Greek VAT Law - Standard Rate for Catering Services"
        },
        
        # General food products
        {
            "rule_name": "Food Products Reduced VAT",
            "rule_code": "GR_FOOD_REDUCED",
            "suggested_rate": Decimal('13.00'),
            "confidence": VATSuggestionConfidence.MEDIUM,
            "reasoning": "Food products typically have 13% reduced VAT rate",
            "product_category": "food",
            "priority": 200,
            "legal_reference": "Greek VAT Law - Reduced Rate 1"
        },
        
        # Standard rate fallback
        {
            "rule_name": "Standard VAT Rate",
            "rule_code": "GR_STANDARD",
            "suggested_rate": Decimal('24.00'),
            "confidence": VATSuggestionConfidence.MEDIUM,
            "reasoning": "Standard VAT rate for most goods and services",
            "priority": 100,
            "legal_reference": "Greek VAT Law - Standard Rate"
        }
    ]
    
    for rule_data in default_rules:
        # Check if rule already exists
        existing = db.query(VATSuggestionRule).filter(
            VATSuggestionRule.rule_code == rule_data["rule_code"]
        ).first()
        
        if not existing:
            service.create_suggestion_rule(**rule_data)
            logger.info(f"Created default VAT suggestion rule: {rule_data['rule_name']}") 