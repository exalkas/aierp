"""
Company model for Greek ERP/CRM System
Supports multi-tenant architecture with Greek business compliance
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from typing import Optional, Dict, Any

from ..core.database import Base


class Company(Base):
    """
    Company model for multi-tenant Greek ERP/CRM system
    Each company gets its own database for data isolation
    """
    __tablename__ = "companies"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic company information
    name = Column(String(255), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Greek business compliance fields
    afm = Column(String(9), nullable=False, unique=True, index=True)  # Greek Tax Number
    doy = Column(String(10), nullable=False, index=True)  # Tax Office Code
    business_activity = Column(String(255), nullable=False)  # Primary business activity
    legal_form = Column(String(50), nullable=False)  # ΑΕ, ΕΠΕ, ΟΕ, ΕΕ, etc.
    
    # Contact information
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    fax = Column(String(20))
    website = Column(String(255))
    
    # Greek address fields
    address_street = Column(String(255), nullable=False)
    address_number = Column(String(10), nullable=False)
    address_city = Column(String(100), nullable=False)
    address_postal_code = Column(String(10), nullable=False)
    address_region = Column(String(100), nullable=False)  # Greek region
    address_country = Column(String(2), nullable=False, default="GR")  # ISO country code
    
    # Business settings
    default_currency = Column(String(3), nullable=False, default="EUR")
    default_language = Column(String(2), nullable=False, default="el")  # Greek
    timezone = Column(String(50), nullable=False, default="Europe/Athens")
    
    # AADE (Greek Tax Authority) integration
    aade_enabled = Column(Boolean, default=True)
    aade_subscription_key = Column(String(255))
    aade_test_mode = Column(Boolean, default=True)
    
    # VAT settings
    vat_number = Column(String(20), nullable=False, unique=True)  # EU VAT number
    vat_regime = Column(String(20), nullable=False, default="standard")  # standard, reduced, exempt
    
    # Accounting settings
    accounting_start_date = Column(DateTime, nullable=False)
    fiscal_year_start = Column(String(5), nullable=False, default="01-01")  # MM-DD format
    
    # Subscription and billing
    subscription_plan = Column(String(50), nullable=False, default="starter")
    subscription_status = Column(String(20), nullable=False, default="active")
    billing_email = Column(String(255))
    
    # Company status and settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    setup_completed = Column(Boolean, default=False, nullable=False)
    
    # Database isolation settings
    database_name = Column(String(255), nullable=False, unique=True)
    database_created = Column(Boolean, default=False, nullable=False)
    
    # Feature flags and configuration
    features_enabled = Column(JSON, default=dict)  # Feature toggles
    company_settings = Column(JSON, default=dict)  # Company-specific settings
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    users = relationship("User", back_populates="company")
    subscriptions = relationship("CompanySubscription", back_populates="company")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_company_afm', 'afm'),
        Index('idx_company_vat', 'vat_number'),
        Index('idx_company_active', 'is_active'),
        Index('idx_company_subscription', 'subscription_status'),
        Index('idx_company_database', 'database_name'),
    )
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', afm='{self.afm}')>"
    
    @property
    def full_address(self) -> str:
        """Get formatted Greek address"""
        return f"{self.address_street} {self.address_number}, {self.address_postal_code} {self.address_city}, {self.address_region}"
    
    def get_database_name(self) -> str:
        """Get the database name for this company"""
        return self.database_name or f"erp_company_{str(self.id).replace('-', '_')}"
    
    def get_feature_setting(self, feature_name: str, default: Any = None) -> Any:
        """Get a specific feature setting"""
        return self.features_enabled.get(feature_name, default) if self.features_enabled else default
    
    def set_feature_setting(self, feature_name: str, value: Any) -> None:
        """Set a specific feature setting"""
        if not self.features_enabled:
            self.features_enabled = {}
        self.features_enabled[feature_name] = value
    
    def get_company_setting(self, setting_name: str, default: Any = None) -> Any:
        """Get a specific company setting"""
        return self.company_settings.get(setting_name, default) if self.company_settings else default
    
    def set_company_setting(self, setting_name: str, value: Any) -> None:
        """Set a specific company setting"""
        if not self.company_settings:
            self.company_settings = {}
        self.company_settings[setting_name] = value
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled for this company"""
        return bool(self.get_feature_setting(feature_name, False))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert company to dictionary for API responses"""
        return {
            "id": str(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "afm": self.afm,
            "doy": self.doy,
            "business_activity": self.business_activity,
            "legal_form": self.legal_form,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "website": self.website,
            "address": {
                "street": self.address_street,
                "number": self.address_number,
                "city": self.address_city,
                "postal_code": self.address_postal_code,
                "region": self.address_region,
                "country": self.address_country,
                "full_address": self.full_address
            },
            "vat_number": self.vat_number,
            "default_currency": self.default_currency,
            "default_language": self.default_language,
            "timezone": self.timezone,
            "subscription_plan": self.subscription_plan,
            "subscription_status": self.subscription_status,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "setup_completed": self.setup_completed,
            "aade_enabled": self.aade_enabled,
            "aade_test_mode": self.aade_test_mode,
            "features_enabled": self.features_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 