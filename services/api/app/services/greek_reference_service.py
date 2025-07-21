"""
Greek Reference Service for Greek ERP/CRM System
Provides access to Greek reference data (DOY, regions, VAT rates, etc.)
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.greek_reference_data import (
    GreekRegion, GreekTaxOffice, GreekVATRate, GreekBusinessActivity,
    GreekLegalForm, GreekBank, PostalCode, VATZone, LocationType
)


class GreekReferenceService:
    """Service for accessing Greek reference data"""

    def __init__(self, db: Session):
        self.db = db

    # Greek Regions
    def get_all_regions(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all Greek regions"""
        query = self.db.query(GreekRegion)
        if not include_inactive:
            query = query.filter(GreekRegion.is_active == True)
        
        regions = query.order_by(GreekRegion.name_en).all()
        return [self._region_to_dict(region) for region in regions]

    def get_region_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get region by code"""
        region = self.db.query(GreekRegion).filter(
            GreekRegion.code == code,
            GreekRegion.is_active == True
        ).first()
        return self._region_to_dict(region) if region else None

    def search_regions(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search regions by name"""
        regions = self.db.query(GreekRegion).filter(
            and_(
                GreekRegion.is_active == True,
                or_(
                    GreekRegion.name_en.ilike(f"%{query}%"),
                    GreekRegion.name_el.ilike(f"%{query}%")
                )
            )
        ).limit(limit).all()
        return [self._region_to_dict(region) for region in regions]

    def _region_to_dict(self, region: GreekRegion) -> Dict[str, Any]:
        """Convert region model to dict"""
        return {
            "code": region.code,
            "name_en": region.name_en,
            "name_el": region.name_el,
            "capital": region.capital,
            "vat_zone": region.vat_zone,
            "island_discount": region.island_discount,
            "is_active": region.is_active
        }

    # Greek Tax Offices (DOY)
    def get_all_tax_offices(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all Greek tax offices"""
        query = self.db.query(GreekTaxOffice)
        if not include_inactive:
            query = query.filter(GreekTaxOffice.is_active == True)
        
        offices = query.order_by(GreekTaxOffice.name_en).all()
        return [self._tax_office_to_dict(office) for office in offices]

    def get_tax_office_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get tax office by code"""
        office = self.db.query(GreekTaxOffice).filter(
            GreekTaxOffice.code == code,
            GreekTaxOffice.is_active == True
        ).first()
        return self._tax_office_to_dict(office) if office else None

    def search_tax_offices(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search tax offices by name or code"""
        offices = self.db.query(GreekTaxOffice).filter(
            and_(
                GreekTaxOffice.is_active == True,
                or_(
                    GreekTaxOffice.code.ilike(f"%{query}%"),
                    GreekTaxOffice.name_en.ilike(f"%{query}%"),
                    GreekTaxOffice.name_el.ilike(f"%{query}%"),
                    GreekTaxOffice.city.ilike(f"%{query}%")
                )
            )
        ).limit(limit).all()
        return [self._tax_office_to_dict(office) for office in offices]

    def get_tax_offices_by_region(self, region_code: str) -> List[Dict[str, Any]]:
        """Get tax offices by region"""
        offices = self.db.query(GreekTaxOffice).filter(
            GreekTaxOffice.region_code == region_code,
            GreekTaxOffice.is_active == True
        ).order_by(GreekTaxOffice.name_en).all()
        return [self._tax_office_to_dict(office) for office in offices]

    def _tax_office_to_dict(self, office: GreekTaxOffice) -> Dict[str, Any]:
        """Convert tax office model to dict"""
        return {
            "code": office.code,
            "name_en": office.name_en,
            "name_el": office.name_el,
            "city": office.city,
            "region_code": office.region_code,
            "postal_code": office.postal_code,
            "address": office.address,
            "phone": office.phone,
            "fax": office.fax,
            "email": office.email,
            "is_active": office.is_active
        }

    # Greek VAT Rates
    def get_current_vat_rates(self) -> List[Dict[str, Any]]:
        """Get current VAT rates"""
        rates = self.db.query(GreekVATRate).filter(
            GreekVATRate.is_active == True
        ).order_by(GreekVATRate.rate.desc()).all()
        return [self._vat_rate_to_dict(rate) for rate in rates]

    def get_vat_rate_by_category(self, category: str) -> Optional[Dict[str, Any]]:
        """Get VAT rate by category"""
        rate = self.db.query(GreekVATRate).filter(
            GreekVATRate.category == category,
            GreekVATRate.is_active == True
        ).first()
        return self._vat_rate_to_dict(rate) if rate else None

    def _vat_rate_to_dict(self, rate: GreekVATRate) -> Dict[str, Any]:
        """Convert VAT rate model to dict"""
        return {
            "category": rate.category,
            "rate": float(rate.rate),
            "description_en": rate.description_en,
            "description_el": rate.description_el,
            "effective_date": rate.effective_date.isoformat() if rate.effective_date else None,
            "island_rate": float(rate.island_rate) if rate.island_rate else None,
            "is_active": rate.is_active
        }

    # Greek Business Activities
    def get_all_business_activities(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all business activities"""
        query = self.db.query(GreekBusinessActivity)
        if not include_inactive:
            query = query.filter(GreekBusinessActivity.is_active == True)
        
        activities = query.order_by(
            GreekBusinessActivity.section_code,
            GreekBusinessActivity.code
        ).all()
        return [self._business_activity_to_dict(activity) for activity in activities]

    def get_business_activity_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get business activity by code"""
        activity = self.db.query(GreekBusinessActivity).filter(
            GreekBusinessActivity.code == code,
            GreekBusinessActivity.is_active == True
        ).first()
        return self._business_activity_to_dict(activity) if activity else None

    def search_business_activities(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search business activities"""
        activities = self.db.query(GreekBusinessActivity).filter(
            and_(
                GreekBusinessActivity.is_active == True,
                or_(
                    GreekBusinessActivity.code.ilike(f"%{query}%"),
                    GreekBusinessActivity.description_en.ilike(f"%{query}%"),
                    GreekBusinessActivity.description_el.ilike(f"%{query}%")
                )
            )
        ).limit(limit).all()
        return [self._business_activity_to_dict(activity) for activity in activities]

    def get_business_activities_by_section(self, section_code: str) -> List[Dict[str, Any]]:
        """Get business activities by section"""
        activities = self.db.query(GreekBusinessActivity).filter(
            GreekBusinessActivity.section_code == section_code,
            GreekBusinessActivity.is_active == True
        ).order_by(GreekBusinessActivity.code).all()
        return [self._business_activity_to_dict(activity) for activity in activities]

    def _business_activity_to_dict(self, activity: GreekBusinessActivity) -> Dict[str, Any]:
        """Convert business activity model to dict"""
        return {
            "code": activity.code,
            "description_en": activity.description_en,
            "description_el": activity.description_el,
            "section_code": activity.section_code,
            "section_description": activity.section_description,
            "level": activity.level,
            "parent_code": activity.parent_code,
            "is_active": activity.is_active
        }

    # Greek Legal Forms
    def get_all_legal_forms(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all legal forms"""
        query = self.db.query(GreekLegalForm)
        if not include_inactive:
            query = query.filter(GreekLegalForm.is_active == True)
        
        forms = query.order_by(GreekLegalForm.abbreviation_el).all()
        return [self._legal_form_to_dict(form) for form in forms]

    def get_legal_form_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get legal form by code"""
        form = self.db.query(GreekLegalForm).filter(
            GreekLegalForm.code == code,
            GreekLegalForm.is_active == True
        ).first()
        return self._legal_form_to_dict(form) if form else None

    def _legal_form_to_dict(self, form: GreekLegalForm) -> Dict[str, Any]:
        """Convert legal form model to dict"""
        return {
            "code": form.code,
            "name_en": form.name_en,
            "name_el": form.name_el,
            "abbreviation_en": form.abbreviation_en,
            "abbreviation_el": form.abbreviation_el,
            "type": form.type,
            "min_shareholders": form.min_shareholders,
            "max_shareholders": form.max_shareholders,
            "min_capital": float(form.min_capital) if form.min_capital else None,
            "is_active": form.is_active
        }

    # Greek Banks
    def get_all_banks(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all Greek banks"""
        query = self.db.query(GreekBank)
        if not include_inactive:
            query = query.filter(GreekBank.is_active == True)
        
        banks = query.order_by(GreekBank.name_en).all()
        return [self._bank_to_dict(bank) for bank in banks]

    def get_bank_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get bank by code"""
        bank = self.db.query(GreekBank).filter(
            GreekBank.code == code,
            GreekBank.is_active == True
        ).first()
        return self._bank_to_dict(bank) if bank else None

    def search_banks(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search banks by name"""
        banks = self.db.query(GreekBank).filter(
            and_(
                GreekBank.is_active == True,
                or_(
                    GreekBank.name_en.ilike(f"%{query}%"),
                    GreekBank.name_el.ilike(f"%{query}%"),
                    GreekBank.code.ilike(f"%{query}%")
                )
            )
        ).limit(limit).all()
        return [self._bank_to_dict(bank) for bank in banks]

    def _bank_to_dict(self, bank: GreekBank) -> Dict[str, Any]:
        """Convert bank model to dict"""
        return {
            "code": bank.code,
            "name_en": bank.name_en,
            "name_el": bank.name_el,
            "swift_code": bank.swift_code,
            "website": bank.website,
            "is_active": bank.is_active
        }

    # Postal Codes
    def get_postal_codes_by_city(self, city: str) -> List[Dict[str, Any]]:
        """Get postal codes by city"""
        codes = self.db.query(PostalCode).filter(
            PostalCode.city.ilike(f"%{city}%"),
            PostalCode.is_active == True
        ).order_by(PostalCode.postal_code).all()
        return [self._postal_code_to_dict(code) for code in codes]

    def get_postal_code_info(self, postal_code: str) -> Optional[Dict[str, Any]]:
        """Get postal code information"""
        code = self.db.query(PostalCode).filter(
            PostalCode.postal_code == postal_code,
            PostalCode.is_active == True
        ).first()
        return self._postal_code_to_dict(code) if code else None

    def search_postal_codes(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search postal codes"""
        codes = self.db.query(PostalCode).filter(
            and_(
                PostalCode.is_active == True,
                or_(
                    PostalCode.postal_code.ilike(f"%{query}%"),
                    PostalCode.city.ilike(f"%{query}%"),
                    PostalCode.area.ilike(f"%{query}%")
                )
            )
        ).limit(limit).all()
        return [self._postal_code_to_dict(code) for code in codes]

    def _postal_code_to_dict(self, code: PostalCode) -> Dict[str, Any]:
        """Convert postal code model to dict"""
        return {
            "postal_code": code.postal_code,
            "city": code.city,
            "area": code.area,
            "region_code": code.region_code,
            "prefecture": code.prefecture,
            "latitude": float(code.latitude) if code.latitude else None,
            "longitude": float(code.longitude) if code.longitude else None,
            "is_active": code.is_active
        }

    # Utility methods
    def validate_afm_doy_combination(self, afm: str, doy_code: str) -> bool:
        """Validate that AFM and DOY combination is valid"""
        # Check if DOY exists
        doy = self.db.query(GreekTaxOffice).filter(
            GreekTaxOffice.code == doy_code,
            GreekTaxOffice.is_active == True
        ).first()
        
        if not doy:
            return False
        
        # Additional validation logic can be added here
        # For now, we just check that the DOY exists
        return True

    def get_vat_zone_by_location(self, region_code: str, postal_code: str = None) -> str:
        """Get VAT zone by location"""
        # First try to get from region
        region = self.db.query(GreekRegion).filter(
            GreekRegion.code == region_code,
            GreekRegion.is_active == True
        ).first()
        
        if region and region.vat_zone:
            return region.vat_zone
        
        # Default to mainland VAT zone
        return "mainland"

    def get_suggested_vat_rate(self, business_activity_code: str, location: str = "mainland") -> Optional[float]:
        """Get suggested VAT rate based on business activity and location"""
        # This is a simplified implementation
        # In practice, this would involve complex business rules
        
        activity = self.db.query(GreekBusinessActivity).filter(
            GreekBusinessActivity.code == business_activity_code,
            GreekBusinessActivity.is_active == True
        ).first()
        
        if not activity:
            return None
        
        # Default to standard VAT rate
        standard_rate = self.db.query(GreekVATRate).filter(
            GreekVATRate.category == "standard",
            GreekVATRate.is_active == True
        ).first()
        
        if standard_rate:
            # Check if island discount applies
            if location in ["island", "reduced_vat_zone"] and standard_rate.island_rate:
                return float(standard_rate.island_rate)
            return float(standard_rate.rate)
        
        return 24.0  # Default Greek VAT rate 