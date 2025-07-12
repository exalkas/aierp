"""
Product Service Template Service
Admin service for managing pre-configured product/service templates
"""

from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func

from ..models.product_vat_config import (
    ProductServiceTemplate, VATSuggestionConfidence
)

logger = logging.getLogger(__name__)


class ProductServiceTemplateService:
    """
    Service for managing product/service templates
    Used by admins to create and manage pre-configured VAT templates
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_templates(
        self, 
        category: Optional[str] = None,
        is_active: bool = True,
        popular_only: bool = False,
        limit: int = 100
    ) -> List[ProductServiceTemplate]:
        """
        Get product/service templates with filtering options
        """
        query = self.db.query(ProductServiceTemplate)
        
        if is_active is not None:
            query = query.filter(ProductServiceTemplate.is_active == is_active)
        
        if category:
            query = query.filter(ProductServiceTemplate.category == category)
        
        if popular_only:
            query = query.filter(ProductServiceTemplate.is_popular == True)
        
        return query.order_by(
            desc(ProductServiceTemplate.is_popular),
            desc(ProductServiceTemplate.usage_count),
            ProductServiceTemplate.display_order,
            ProductServiceTemplate.name
        ).limit(limit).all()
    
    def get_templates_grouped_by_category(
        self, 
        is_active: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get templates grouped by category for UI display
        """
        templates = self.get_templates(is_active=is_active)
        
        grouped = {}
        for template in templates:
            category = template.category
            if category not in grouped:
                grouped[category] = []
            
            grouped[category].append(template.to_dict())
        
        return grouped
    
    def get_popular_templates(self, limit: int = 10) -> List[ProductServiceTemplate]:
        """
        Get most popular templates for quick selection
        """
        return self.db.query(ProductServiceTemplate).filter(
            ProductServiceTemplate.is_active == True
        ).order_by(
            desc(ProductServiceTemplate.is_popular),
            desc(ProductServiceTemplate.usage_count)
        ).limit(limit).all()
    
    def search_templates(
        self, 
        search_term: str,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[ProductServiceTemplate]:
        """
        Search templates by name, description, or keywords
        """
        search_term_lower = search_term.lower()
        
        query = self.db.query(ProductServiceTemplate).filter(
            ProductServiceTemplate.is_active == True
        )
        
        if category:
            query = query.filter(ProductServiceTemplate.category == category)
        
        # Search in name, description, and keywords
        query = query.filter(
            or_(
                ProductServiceTemplate.name.ilike(f"%{search_term}%"),
                ProductServiceTemplate.display_name.ilike(f"%{search_term}%"),
                ProductServiceTemplate.description.ilike(f"%{search_term}%"),
                ProductServiceTemplate.keywords.op("@>")(f'["{search_term_lower}"]')
            )
        )
        
        return query.order_by(
            desc(ProductServiceTemplate.usage_count),
            ProductServiceTemplate.name
        ).limit(limit).all()
    
    def get_template_by_id(self, template_id: str) -> Optional[ProductServiceTemplate]:
        """
        Get specific template by ID
        """
        return self.db.query(ProductServiceTemplate).filter(
            ProductServiceTemplate.id == template_id
        ).first()
    
    def create_template(
        self,
        name: str,
        display_name: str,
        category: str,
        vat_rate: Decimal,
        vat_reasoning: str,
        description: Optional[str] = None,
        vat_exemption_type: Optional[str] = None,
        legal_reference: Optional[str] = None,
        business_types: List[str] = None,
        keywords: List[str] = None,
        applies_to_mainland: bool = True,
        applies_to_islands: bool = True,
        island_vat_rate: Optional[Decimal] = None,
        is_popular: bool = False,
        display_order: int = 0,
        admin_notes: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> ProductServiceTemplate:
        """
        Create a new product/service template
        """
        # Auto-calculate island VAT rate if not provided
        if not island_vat_rate and applies_to_islands and vat_rate > 0:
            island_vat_rate = vat_rate * Decimal('0.70')  # 30% reduction
        
        template = ProductServiceTemplate(
            name=name,
            display_name=display_name,
            description=description,
            category=category,
            vat_rate=vat_rate,
            vat_exemption_type=vat_exemption_type,
            vat_reasoning=vat_reasoning,
            legal_reference=legal_reference,
            business_types=business_types or [],
            keywords=keywords or [],
            applies_to_mainland=applies_to_mainland,
            applies_to_islands=applies_to_islands,
            island_vat_rate=island_vat_rate,
            is_popular=is_popular,
            display_order=display_order,
            admin_notes=admin_notes,
            created_by=created_by,
            created_by_system=False
        )
        
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        
        logger.info(f"Created new template: {name} ({category}) - {vat_rate}% VAT")
        return template
    
    def update_template(
        self,
        template_id: str,
        updates: Dict[str, Any],
        updated_by: Optional[str] = None
    ) -> Optional[ProductServiceTemplate]:
        """
        Update an existing template
        """
        template = self.get_template_by_id(template_id)
        if not template:
            return None
        
        # Update fields
        for key, value in updates.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        if updated_by:
            template.updated_by = updated_by
        
        # Auto-calculate island VAT rate if main rate changed
        if 'vat_rate' in updates and template.applies_to_islands and not template.island_vat_rate:
            if template.vat_rate > 0:
                template.island_vat_rate = template.vat_rate * Decimal('0.70')
        
        self.db.commit()
        
        logger.info(f"Updated template: {template.name} - {template_id}")
        return template
    
    def increment_usage_count(self, template_id: str) -> bool:
        """
        Increment usage count when template is selected
        """
        template = self.get_template_by_id(template_id)
        if not template:
            return False
        
        template.usage_count += 1
        self.db.commit()
        
        return True
    
    def mark_as_popular(self, template_id: str, is_popular: bool = True) -> bool:
        """
        Mark template as popular for quick access
        """
        template = self.get_template_by_id(template_id)
        if not template:
            return False
        
        template.is_popular = is_popular
        self.db.commit()
        
        return True
    
    def get_template_statistics(self) -> Dict[str, Any]:
        """
        Get template usage statistics
        """
        total_templates = self.db.query(ProductServiceTemplate).count()
        active_templates = self.db.query(ProductServiceTemplate).filter(
            ProductServiceTemplate.is_active == True
        ).count()
        popular_templates = self.db.query(ProductServiceTemplate).filter(
            ProductServiceTemplate.is_popular == True
        ).count()
        
        # Category distribution
        category_stats = self.db.query(
            ProductServiceTemplate.category,
            func.count(ProductServiceTemplate.id).label('count')
        ).filter(
            ProductServiceTemplate.is_active == True
        ).group_by(ProductServiceTemplate.category).all()
        
        # Most used templates
        most_used = self.db.query(ProductServiceTemplate).filter(
            ProductServiceTemplate.is_active == True
        ).order_by(desc(ProductServiceTemplate.usage_count)).limit(5).all()
        
        return {
            "total_templates": total_templates,
            "active_templates": active_templates,
            "popular_templates": popular_templates,
            "category_distribution": [
                {"category": cat, "count": count} for cat, count in category_stats
            ],
            "most_used_templates": [
                {
                    "id": str(t.id),
                    "name": t.name,
                    "usage_count": t.usage_count,
                    "category": t.category
                } for t in most_used
            ]
        }
    
    def bulk_create_default_templates(self, created_by: Optional[str] = None) -> int:
        """
        Create default templates for common Greek business scenarios
        """
        default_templates = [
            {
                "name": "Coffee Shop - Takeaway",
                "display_name": "☕ Coffee Shop - Takeaway",
                "description": "Takeaway coffee, tea, and beverages",
                "category": "food_service",
                "vat_rate": Decimal('13.00'),
                "vat_reasoning": "Takeaway beverages have reduced VAT rate of 13% (permanent since July 2024)",
                "legal_reference": "Greek VAT Law - Permanent Reduced Rate for Takeaway Beverages",
                "business_types": ["food_service", "cafe"],
                "keywords": ["coffee", "tea", "takeaway", "beverage", "espresso", "cappuccino"],
                "is_popular": True,
                "display_order": 10
            },
            {
                "name": "Coffee Shop - Dine-in",
                "display_name": "☕ Coffee Shop - Dine-in",
                "description": "Dine-in coffee, tea, and beverages with table service",
                "category": "food_service",
                "vat_rate": Decimal('24.00'),
                "vat_reasoning": "Dine-in food and beverages have standard VAT rate of 24%",
                "legal_reference": "Greek VAT Law - Standard Rate for Catering Services",
                "business_types": ["food_service", "restaurant", "cafe"],
                "keywords": ["coffee", "tea", "dine-in", "restaurant", "table service"],
                "is_popular": True,
                "display_order": 20
            },
            {
                "name": "Medical Consultation",
                "display_name": "🏥 Medical Consultation",
                "description": "Medical consultations and healthcare services",
                "category": "healthcare",
                "vat_rate": Decimal('0.00'),
                "vat_exemption_type": "exempt",
                "vat_reasoning": "Healthcare services are VAT exempt in Greece",
                "legal_reference": "Greek VAT Law Article 22 - Healthcare Exemption",
                "business_types": ["healthcare", "medical"],
                "keywords": ["medical", "doctor", "consultation", "healthcare", "examination"],
                "is_popular": True,
                "display_order": 30
            },
            {
                "name": "Legal Services",
                "display_name": "⚖️ Legal Services",
                "description": "Legal consultations and professional legal services",
                "category": "legal",
                "vat_rate": Decimal('0.00'),
                "vat_exemption_type": "exempt",
                "vat_reasoning": "Legal services are VAT exempt in Greece",
                "legal_reference": "Greek VAT Law Article 22 - Legal Services Exemption",
                "business_types": ["legal"],
                "keywords": ["legal", "lawyer", "attorney", "consultation", "law"],
                "is_popular": True,
                "display_order": 40
            },
            {
                "name": "Restaurant Food Service",
                "display_name": "🍽️ Restaurant Food Service",
                "description": "Restaurant meals and food service",
                "category": "food_service",
                "vat_rate": Decimal('24.00'),
                "vat_reasoning": "Restaurant food service has standard VAT rate of 24%",
                "legal_reference": "Greek VAT Law - Standard Rate for Catering Services",
                "business_types": ["food_service", "restaurant"],
                "keywords": ["restaurant", "food", "meal", "dining", "catering"],
                "is_popular": True,
                "display_order": 50
            },
            {
                "name": "Food Products (Retail)",
                "display_name": "🛒 Food Products (Retail)",
                "description": "Retail food products and groceries",
                "category": "retail",
                "vat_rate": Decimal('13.00'),
                "vat_reasoning": "Food products have reduced VAT rate of 13%",
                "legal_reference": "Greek VAT Law - Reduced Rate 1",
                "business_types": ["retail", "grocery"],
                "keywords": ["food", "grocery", "retail", "products", "supermarket"],
                "is_popular": True,
                "display_order": 60
            },
            {
                "name": "Construction Services",
                "display_name": "🏗️ Construction Services",
                "description": "Construction and building services",
                "category": "construction",
                "vat_rate": Decimal('24.00'),
                "vat_reasoning": "Construction services have standard VAT rate of 24%",
                "legal_reference": "Greek VAT Law - Standard Rate",
                "business_types": ["construction", "building"],
                "keywords": ["construction", "building", "renovation", "contractor"],
                "display_order": 70
            },
            {
                "name": "Professional Services",
                "display_name": "💼 Professional Services",
                "description": "General professional services (accounting, consulting, etc.)",
                "category": "professional",
                "vat_rate": Decimal('24.00'),
                "vat_reasoning": "Professional services have standard VAT rate of 24%",
                "legal_reference": "Greek VAT Law - Standard Rate",
                "business_types": ["professional", "consulting"],
                "keywords": ["professional", "consulting", "accounting", "services"],
                "display_order": 80
            }
        ]
        
        created_count = 0
        for template_data in default_templates:
            # Check if template already exists
            existing = self.db.query(ProductServiceTemplate).filter(
                ProductServiceTemplate.name == template_data["name"]
            ).first()
            
            if not existing:
                template_data["created_by"] = created_by
                template_data["created_by_system"] = True
                self.create_template(**template_data)
                created_count += 1
        
        logger.info(f"Created {created_count} default templates")
        return created_count 