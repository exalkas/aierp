"""
Greek Reference Data Models for Master Database
These models contain shared reference data used across all companies
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal

from ..core.database import Base


class VATZone(enum.Enum):
    """Greek VAT zones based on geographical location"""
    STANDARD = "standard"           # 24% standard rate (mainland)
    REDUCED_ISLAND = "reduced_island"  # Reduced rates for islands
    SPECIAL_ZONE = "special_zone"   # Special economic zones
    VAT_EXEMPT = "vat_exempt"       # No VAT zones


class LocationType(enum.Enum):
    """Greek location types for VAT purposes"""
    MAINLAND = "mainland"
    AEGEAN_ISLANDS = "aegean_islands"
    IONIAN_ISLANDS = "ionian_islands"
    CRETE = "crete"
    SPECIAL_ZONE = "special_zone"


class GreekRegion(Base):
    """
    Greek regions and prefectures reference data
    Master database table shared across all companies
    """
    __tablename__ = "greek_regions"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Region information
    region_code = Column(String(10), nullable=False, unique=True, index=True)
    region_name_el = Column(String(100), nullable=False)  # Greek name
    region_name_en = Column(String(100), nullable=False)  # English name
    
    # Prefecture information
    prefecture_code = Column(String(10), nullable=False, index=True)
    prefecture_name_el = Column(String(100), nullable=False)
    prefecture_name_en = Column(String(100), nullable=False)
    
    # Geographic classification
    location_type = Column(Enum(LocationType), nullable=False, default=LocationType.MAINLAND)
    vat_zone = Column(Enum(VATZone), nullable=False, default=VATZone.STANDARD)
    
    # Island-specific information
    island_group = Column(String(50))  # cyclades, dodecanese, etc.
    is_tourist_area = Column(Boolean, default=False)
    
    # Coordinates
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class GreekTaxOffice(Base):
    """
    Greek Tax Offices (DOY) reference data
    Master database table shared across all companies
    """
    __tablename__ = "greek_tax_offices"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # DOY information
    doy_code = Column(String(10), nullable=False, unique=True, index=True)
    doy_name_el = Column(String(255), nullable=False)
    doy_name_en = Column(String(255), nullable=False)
    
    # Location information
    region_id = Column(UUID(as_uuid=True), ForeignKey('greek_regions.id'), nullable=False, index=True)
    city = Column(String(100), nullable=False)
    address = Column(String(500))
    postal_code = Column(String(10))
    
    # Contact information
    phone = Column(String(20))
    fax = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    
    # Operating information
    is_active = Column(Boolean, default=True)
    operating_hours = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    region = relationship("GreekRegion")


class GreekVATRate(Base):
    """
    Greek VAT rates by business type and location
    Master database table shared across all companies
    """
    __tablename__ = "greek_vat_rates"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # VAT rate identification
    rate_code = Column(String(20), nullable=False, unique=True, index=True)
    rate_name_el = Column(String(255), nullable=False)
    rate_name_en = Column(String(255), nullable=False)
    
    # Rate information
    rate_percentage = Column(Numeric(5, 2), nullable=False)  # VAT percentage
    
    # Applicability
    business_type = Column(String(100))  # healthcare, food_service, etc.
    product_category = Column(String(100))  # food, services, etc.
    location_type = Column(Enum(LocationType))
    vat_zone = Column(Enum(VATZone), nullable=False)
    
    # Context-specific rates
    context_conditions = Column(JSON, default=dict)  # {takeaway: true, dine_in: false}
    
    # Legal information
    legal_reference = Column(String(500))  # Greek law reference
    description_el = Column(Text)
    description_en = Column(Text)
    
    # Effective dates
    effective_from = Column(DateTime, nullable=False)
    effective_to = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_vat_rate_business_type', 'business_type'),
        Index('idx_vat_rate_location_type', 'location_type'),
        Index('idx_vat_rate_vat_zone', 'vat_zone'),
        Index('idx_vat_rate_effective', 'effective_from', 'effective_to'),
        Index('idx_vat_rate_active', 'is_active'),
    )


class GreekBusinessActivity(Base):
    """
    Greek business activity codes (KAD codes) reference data
    Master database table shared across all companies
    """
    __tablename__ = "greek_business_activities"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # KAD code information
    kad_code = Column(String(10), nullable=False, unique=True, index=True)
    kad_name_el = Column(String(500), nullable=False)
    kad_name_en = Column(String(500), nullable=False)
    
    # Hierarchy
    parent_kod_id = Column(UUID(as_uuid=True), ForeignKey('greek_business_activities.id'), index=True)
    activity_level = Column(Integer, default=1)  # 1=section, 2=division, 3=group, 4=class
    
    # Classification
    section_code = Column(String(2))  # A, B, C, etc.
    division_code = Column(String(2))  # 01, 02, etc.
    group_code = Column(String(3))    # 01.1, 01.2, etc.
    class_code = Column(String(5))    # 01.11, 01.12, etc.
    
    # Business implications
    vat_implications = Column(JSON, default=dict)
    tax_implications = Column(JSON, default=dict)
    license_requirements = Column(JSON, default=list)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    parent_activity = relationship("GreekBusinessActivity", remote_side=[id])


class GreekLegalForm(Base):
    """
    Greek legal forms reference data (AE, EPE, OE, EE, etc.)
    Master database table shared across all companies
    """
    __tablename__ = "greek_legal_forms"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Legal form information
    legal_form_code = Column(String(10), nullable=False, unique=True, index=True)
    legal_form_name_el = Column(String(255), nullable=False)
    legal_form_name_en = Column(String(255), nullable=False)
    
    # Description
    description_el = Column(Text)
    description_en = Column(Text)
    
    # Requirements
    min_capital = Column(Numeric(15, 2))  # Minimum capital requirement
    min_shareholders = Column(Integer)
    max_shareholders = Column(Integer)
    liability_type = Column(String(50))  # limited, unlimited, mixed
    
    # Tax implications
    tax_rate = Column(Numeric(5, 2))  # Corporate tax rate
    dividend_tax_rate = Column(Numeric(5, 2))
    
    # Legal requirements
    requires_board = Column(Boolean, default=False)
    requires_auditor = Column(Boolean, default=False)
    requires_publication = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class GreekBank(Base):
    """
    Greek banks and payment methods reference data
    Master database table shared across all companies
    """
    __tablename__ = "greek_banks"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Bank information
    bank_code = Column(String(10), nullable=False, unique=True, index=True)
    bank_name_el = Column(String(255), nullable=False)
    bank_name_en = Column(String(255), nullable=False)
    
    # SWIFT information
    swift_bic = Column(String(11), index=True)
    country_code = Column(String(2), default="GR")
    
    # Bank type
    bank_type = Column(String(50))  # commercial, cooperative, investment, etc.
    
    # Contact information
    website = Column(String(255))
    phone = Column(String(20))
    
    # Status
    is_active = Column(Boolean, default=True)
    supports_sepa = Column(Boolean, default=True)
    supports_instant_payments = Column(Boolean, default=False)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class PostalCode(Base):
    """
    Greek postal codes reference data
    Master database table shared across all companies
    """
    __tablename__ = "postal_codes"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Postal code information
    postal_code = Column(String(10), nullable=False, index=True)
    area_name_el = Column(String(255), nullable=False)
    area_name_en = Column(String(255), nullable=False)
    
    # Location information
    region_id = Column(UUID(as_uuid=True), ForeignKey('greek_regions.id'), nullable=False, index=True)
    municipality = Column(String(100))
    
    # Geographic coordinates
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    region = relationship("GreekRegion")
    
    # Indexes
    __table_args__ = (
        Index('idx_postal_code_region', 'region_id'),
        Index('idx_postal_code_municipality', 'municipality'),
    ) 