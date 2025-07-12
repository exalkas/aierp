"""
System Configuration and Subscription Models for Master Database
These models manage system-wide settings and subscription management
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


class ConfigurationType(enum.Enum):
    """System configuration types"""
    SYSTEM = "system"
    FEATURE = "feature"
    INTEGRATION = "integration"
    NOTIFICATION = "notification"
    SECURITY = "security"


class SubscriptionPlan(enum.Enum):
    """Subscription plan types"""
    STARTER = "starter"
    BUSINESS = "business"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class SubscriptionStatus(enum.Enum):
    """Subscription status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"


class SystemConfiguration(Base):
    """
    System-wide configuration settings
    Master database table for global system settings
    """
    __tablename__ = "system_configurations"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Configuration identification
    config_key = Column(String(255), nullable=False, unique=True, index=True)
    config_name = Column(String(255), nullable=False)
    config_type = Column(Enum(ConfigurationType), nullable=False, default=ConfigurationType.SYSTEM)
    
    # Configuration value
    config_value = Column(JSON, nullable=False)
    default_value = Column(JSON)
    
    # Metadata
    description = Column(Text)
    is_encrypted = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)  # Can be read by companies
    
    # Validation
    validation_rules = Column(JSON, default=dict)
    allowed_values = Column(JSON, default=list)
    
    # Status and version
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Indexes
    __table_args__ = (
        Index('idx_config_type', 'config_type'),
        Index('idx_config_active', 'is_active'),
        Index('idx_config_public', 'is_public'),
    )


class SubscriptionPlanDefinition(Base):
    """
    Subscription plan definitions
    Master database table for available subscription plans
    """
    __tablename__ = "subscription_plan_definitions"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Plan identification
    plan_code = Column(String(50), nullable=False, unique=True, index=True)
    plan_name = Column(String(255), nullable=False)
    plan_type = Column(Enum(SubscriptionPlan), nullable=False)
    
    # Plan description
    description = Column(Text)
    marketing_description = Column(Text)
    
    # Pricing
    monthly_price = Column(Numeric(10, 2), nullable=False)
    annual_price = Column(Numeric(10, 2))
    setup_fee = Column(Numeric(10, 2), default=0)
    
    # Limits and features
    max_users = Column(Integer, default=5)
    max_companies = Column(Integer, default=1)
    max_customers = Column(Integer, default=1000)
    max_products = Column(Integer, default=1000)
    max_invoices_per_month = Column(Integer, default=100)
    max_storage_gb = Column(Integer, default=1)
    
    # Feature flags
    features = Column(JSON, default=dict)
    
    # Greek-specific features
    aade_integration = Column(Boolean, default=False)
    greek_tax_reports = Column(Boolean, default=False)
    greek_payroll = Column(Boolean, default=False)
    voice_commands = Column(Boolean, default=False)
    
    # API and integration limits
    api_calls_per_month = Column(Integer, default=1000)
    webhook_endpoints = Column(Integer, default=1)
    integrations_allowed = Column(JSON, default=list)
    
    # Support features
    support_level = Column(String(50), default="basic")  # basic, priority, premium
    support_channels = Column(JSON, default=list)  # email, chat, phone
    
    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)  # Visible to customers
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))


class CompanySubscription(Base):
    """
    Company subscription management
    Master database table for tracking company subscriptions
    """
    __tablename__ = "company_subscriptions"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    
    # Subscription plan
    plan_id = Column(UUID(as_uuid=True), ForeignKey('subscription_plan_definitions.id'), nullable=False, index=True)
    
    # Subscription details
    subscription_status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.ACTIVE)
    
    # Timeline
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    trial_end_date = Column(DateTime)
    
    # Billing
    billing_cycle = Column(String(20), default="monthly")  # monthly, annual
    next_billing_date = Column(DateTime)
    last_billing_date = Column(DateTime)
    
    # Pricing (can override plan defaults)
    monthly_price = Column(Numeric(10, 2))
    annual_price = Column(Numeric(10, 2))
    custom_pricing = Column(JSON, default=dict)
    
    # Usage limits (can override plan defaults)
    max_users = Column(Integer)
    max_customers = Column(Integer)
    max_products = Column(Integer)
    max_invoices_per_month = Column(Integer)
    max_storage_gb = Column(Integer)
    
    # Custom features (can override plan defaults)
    custom_features = Column(JSON, default=dict)
    
    # Billing information
    billing_contact_name = Column(String(255))
    billing_contact_email = Column(String(255))
    billing_address = Column(JSON, default=dict)
    
    # Payment information
    payment_method = Column(String(50))
    payment_provider = Column(String(50))
    payment_reference = Column(String(255))
    
    # Cancellation
    cancellation_date = Column(DateTime)
    cancellation_reason = Column(Text)
    cancelled_by = Column(UUID(as_uuid=True))
    
    # Notes
    notes = Column(Text)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    company = relationship("Company", back_populates="subscriptions")
    plan = relationship("SubscriptionPlanDefinition")
    
    # Indexes
    __table_args__ = (
        Index('idx_subscription_company', 'company_id'),
        Index('idx_subscription_plan', 'plan_id'),
        Index('idx_subscription_status', 'subscription_status'),
        Index('idx_subscription_billing', 'next_billing_date'),
        Index('idx_subscription_trial', 'trial_end_date'),
    )


class UsageMetric(Base):
    """
    Usage metrics tracking for companies
    Master database table for tracking usage across all companies
    """
    __tablename__ = "usage_metrics"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    
    # Metric information
    metric_name = Column(String(255), nullable=False, index=True)
    metric_category = Column(String(100), nullable=False)  # users, customers, invoices, etc.
    
    # Metric value
    metric_value = Column(Numeric(15, 2), nullable=False)
    metric_unit = Column(String(50))  # count, gb, hours, etc.
    
    # Time period
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly, annual
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Metadata
    usage_metadata = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    company = relationship("Company")
    
    # Indexes
    __table_args__ = (
        Index('idx_usage_company', 'company_id'),
        Index('idx_usage_metric', 'metric_name'),
        Index('idx_usage_period', 'period_start', 'period_end'),
        Index('idx_usage_category', 'metric_category'),
    )


class SystemNotification(Base):
    """
    System-wide notifications
    Master database table for system notifications to companies
    """
    __tablename__ = "system_notifications"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Notification details
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # info, warning, error, success
    
    # Targeting
    target_companies = Column(JSON, default=list)  # Specific company IDs, empty = all
    target_plans = Column(JSON, default=list)  # Specific plan types, empty = all
    target_users = Column(JSON, default=list)  # Specific user roles, empty = all
    
    # Delivery
    delivery_method = Column(String(50), default="in_app")  # in_app, email, sms
    is_urgent = Column(Boolean, default=False)
    
    # Scheduling
    scheduled_for = Column(DateTime)
    sent_at = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_sent = Column(Boolean, default=False)
    
    # Metadata
    action_url = Column(String(500))
    action_text = Column(String(100))
    expires_at = Column(DateTime)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Indexes
    __table_args__ = (
        Index('idx_notification_type', 'notification_type'),
        Index('idx_notification_scheduled', 'scheduled_for'),
        Index('idx_notification_active', 'is_active'),
        Index('idx_notification_sent', 'is_sent'),
    )


class ApiKey(Base):
    """
    API keys for system integrations
    Master database table for managing API keys
    """
    __tablename__ = "api_keys"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Key information
    key_name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    key_prefix = Column(String(20), nullable=False)  # First few characters for identification
    
    # Service association
    service_name = Column(String(255), nullable=False)
    service_type = Column(String(100), nullable=False)  # aade, banking, email, etc.
    
    # Scope and permissions
    allowed_scopes = Column(JSON, default=list)
    rate_limit_per_hour = Column(Integer, default=1000)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime)
    usage_count = Column(Integer, default=0)
    
    # Expiration
    expires_at = Column(DateTime)
    
    # IP restrictions
    allowed_ips = Column(JSON, default=list)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Indexes
    __table_args__ = (
        Index('idx_api_key_service', 'service_name'),
        Index('idx_api_key_type', 'service_type'),
        Index('idx_api_key_active', 'is_active'),
        Index('idx_api_key_expires', 'expires_at'),
    ) 