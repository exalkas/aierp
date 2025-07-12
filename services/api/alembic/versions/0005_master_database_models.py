"""Add master database models for Greek reference data and system configuration

Revision ID: 0005
Revises: 0004
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create Greek reference data tables
    
    # Greek regions table
    op.create_table('greek_regions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('region_code', sa.String(length=10), nullable=False),
        sa.Column('region_name_el', sa.String(length=100), nullable=False),
        sa.Column('region_name_en', sa.String(length=100), nullable=False),
        sa.Column('prefecture_code', sa.String(length=10), nullable=False),
        sa.Column('prefecture_name_el', sa.String(length=100), nullable=False),
        sa.Column('prefecture_name_en', sa.String(length=100), nullable=False),
        sa.Column('location_type', sa.Enum('MAINLAND', 'AEGEAN_ISLANDS', 'IONIAN_ISLANDS', 'CRETE', 'SPECIAL_ZONE', name='locationtype'), nullable=False),
        sa.Column('vat_zone', sa.Enum('STANDARD', 'REDUCED_ISLAND', 'SPECIAL_ZONE', 'VAT_EXEMPT', name='vatzone'), nullable=False),
        sa.Column('island_group', sa.String(length=50), nullable=True),
        sa.Column('is_tourist_area', sa.Boolean(), nullable=True),
        sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=True),
        sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_region_code', 'greek_regions', ['region_code'], unique=True)
    op.create_index('idx_prefecture_code', 'greek_regions', ['prefecture_code'])
    
    # Greek tax offices table
    op.create_table('greek_tax_offices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('doy_code', sa.String(length=10), nullable=False),
        sa.Column('doy_name_el', sa.String(length=255), nullable=False),
        sa.Column('doy_name_en', sa.String(length=255), nullable=False),
        sa.Column('region_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('postal_code', sa.String(length=10), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('fax', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('operating_hours', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['region_id'], ['greek_regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_doy_code', 'greek_tax_offices', ['doy_code'], unique=True)
    op.create_index('idx_doy_region', 'greek_tax_offices', ['region_id'])
    
    # Greek VAT rates table
    op.create_table('greek_vat_rates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('rate_code', sa.String(length=20), nullable=False),
        sa.Column('rate_name_el', sa.String(length=255), nullable=False),
        sa.Column('rate_name_en', sa.String(length=255), nullable=False),
        sa.Column('rate_percentage', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('business_type', sa.String(length=100), nullable=True),
        sa.Column('product_category', sa.String(length=100), nullable=True),
        sa.Column('location_type', sa.Enum('MAINLAND', 'AEGEAN_ISLANDS', 'IONIAN_ISLANDS', 'CRETE', 'SPECIAL_ZONE', name='locationtype'), nullable=True),
        sa.Column('vat_zone', sa.Enum('STANDARD', 'REDUCED_ISLAND', 'SPECIAL_ZONE', 'VAT_EXEMPT', name='vatzone'), nullable=False),
        sa.Column('context_conditions', sa.JSON(), nullable=True),
        sa.Column('legal_reference', sa.String(length=500), nullable=True),
        sa.Column('description_el', sa.Text(), nullable=True),
        sa.Column('description_en', sa.Text(), nullable=True),
        sa.Column('effective_from', sa.DateTime(), nullable=False),
        sa.Column('effective_to', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_vat_rate_code', 'greek_vat_rates', ['rate_code'], unique=True)
    op.create_index('idx_vat_rate_business_type', 'greek_vat_rates', ['business_type'])
    op.create_index('idx_vat_rate_location_type', 'greek_vat_rates', ['location_type'])
    op.create_index('idx_vat_rate_vat_zone', 'greek_vat_rates', ['vat_zone'])
    op.create_index('idx_vat_rate_effective', 'greek_vat_rates', ['effective_from', 'effective_to'])
    op.create_index('idx_vat_rate_active', 'greek_vat_rates', ['is_active'])
    
    # Greek business activities table
    op.create_table('greek_business_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('kad_code', sa.String(length=10), nullable=False),
        sa.Column('kad_name_el', sa.String(length=500), nullable=False),
        sa.Column('kad_name_en', sa.String(length=500), nullable=False),
        sa.Column('parent_kod_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('activity_level', sa.Integer(), nullable=True),
        sa.Column('section_code', sa.String(length=2), nullable=True),
        sa.Column('division_code', sa.String(length=2), nullable=True),
        sa.Column('group_code', sa.String(length=3), nullable=True),
        sa.Column('class_code', sa.String(length=5), nullable=True),
        sa.Column('vat_implications', sa.JSON(), nullable=True),
        sa.Column('tax_implications', sa.JSON(), nullable=True),
        sa.Column('license_requirements', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['parent_kod_id'], ['greek_business_activities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_kad_code', 'greek_business_activities', ['kad_code'], unique=True)
    op.create_index('idx_kad_parent', 'greek_business_activities', ['parent_kod_id'])
    
    # Greek legal forms table
    op.create_table('greek_legal_forms',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('legal_form_code', sa.String(length=10), nullable=False),
        sa.Column('legal_form_name_el', sa.String(length=255), nullable=False),
        sa.Column('legal_form_name_en', sa.String(length=255), nullable=False),
        sa.Column('description_el', sa.Text(), nullable=True),
        sa.Column('description_en', sa.Text(), nullable=True),
        sa.Column('min_capital', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('min_shareholders', sa.Integer(), nullable=True),
        sa.Column('max_shareholders', sa.Integer(), nullable=True),
        sa.Column('liability_type', sa.String(length=50), nullable=True),
        sa.Column('tax_rate', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('dividend_tax_rate', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('requires_board', sa.Boolean(), nullable=True),
        sa.Column('requires_auditor', sa.Boolean(), nullable=True),
        sa.Column('requires_publication', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_legal_form_code', 'greek_legal_forms', ['legal_form_code'], unique=True)
    
    # Greek banks table
    op.create_table('greek_banks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bank_code', sa.String(length=10), nullable=False),
        sa.Column('bank_name_el', sa.String(length=255), nullable=False),
        sa.Column('bank_name_en', sa.String(length=255), nullable=False),
        sa.Column('swift_bic', sa.String(length=11), nullable=True),
        sa.Column('country_code', sa.String(length=2), nullable=True),
        sa.Column('bank_type', sa.String(length=50), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('supports_sepa', sa.Boolean(), nullable=True),
        sa.Column('supports_instant_payments', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_bank_code', 'greek_banks', ['bank_code'], unique=True)
    op.create_index('idx_bank_swift', 'greek_banks', ['swift_bic'])
    
    # Postal codes table
    op.create_table('postal_codes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('postal_code', sa.String(length=10), nullable=False),
        sa.Column('area_name_el', sa.String(length=255), nullable=False),
        sa.Column('area_name_en', sa.String(length=255), nullable=False),
        sa.Column('region_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('municipality', sa.String(length=100), nullable=True),
        sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=True),
        sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['region_id'], ['greek_regions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_postal_code', 'postal_codes', ['postal_code'])
    op.create_index('idx_postal_code_region', 'postal_codes', ['region_id'])
    op.create_index('idx_postal_code_municipality', 'postal_codes', ['municipality'])
    
    # System configuration tables
    
    # System configurations table
    op.create_table('system_configurations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('config_key', sa.String(length=255), nullable=False),
        sa.Column('config_name', sa.String(length=255), nullable=False),
        sa.Column('config_type', sa.Enum('SYSTEM', 'FEATURE', 'INTEGRATION', 'NOTIFICATION', 'SECURITY', name='configurationtype'), nullable=False),
        sa.Column('config_value', sa.JSON(), nullable=False),
        sa.Column('default_value', sa.JSON(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_encrypted', sa.Boolean(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('validation_rules', sa.JSON(), nullable=True),
        sa.Column('allowed_values', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_config_key', 'system_configurations', ['config_key'], unique=True)
    op.create_index('idx_config_type', 'system_configurations', ['config_type'])
    op.create_index('idx_config_active', 'system_configurations', ['is_active'])
    op.create_index('idx_config_public', 'system_configurations', ['is_public'])
    
    # Subscription plan definitions table
    op.create_table('subscription_plan_definitions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_code', sa.String(length=50), nullable=False),
        sa.Column('plan_name', sa.String(length=255), nullable=False),
        sa.Column('plan_type', sa.Enum('STARTER', 'BUSINESS', 'PROFESSIONAL', 'ENTERPRISE', 'CUSTOM', name='subscriptionplan'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('marketing_description', sa.Text(), nullable=True),
        sa.Column('monthly_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('annual_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('setup_fee', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('max_users', sa.Integer(), nullable=True),
        sa.Column('max_companies', sa.Integer(), nullable=True),
        sa.Column('max_customers', sa.Integer(), nullable=True),
        sa.Column('max_products', sa.Integer(), nullable=True),
        sa.Column('max_invoices_per_month', sa.Integer(), nullable=True),
        sa.Column('max_storage_gb', sa.Integer(), nullable=True),
        sa.Column('features', sa.JSON(), nullable=True),
        sa.Column('aade_integration', sa.Boolean(), nullable=True),
        sa.Column('greek_tax_reports', sa.Boolean(), nullable=True),
        sa.Column('greek_payroll', sa.Boolean(), nullable=True),
        sa.Column('voice_commands', sa.Boolean(), nullable=True),
        sa.Column('api_calls_per_month', sa.Integer(), nullable=True),
        sa.Column('webhook_endpoints', sa.Integer(), nullable=True),
        sa.Column('integrations_allowed', sa.JSON(), nullable=True),
        sa.Column('support_level', sa.String(length=50), nullable=True),
        sa.Column('support_channels', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_plan_code', 'subscription_plan_definitions', ['plan_code'], unique=True)
    
    # Company subscriptions table
    op.create_table('company_subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('subscription_status', sa.Enum('ACTIVE', 'INACTIVE', 'SUSPENDED', 'CANCELLED', 'EXPIRED', 'TRIAL', name='subscriptionstatus'), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('trial_end_date', sa.DateTime(), nullable=True),
        sa.Column('billing_cycle', sa.String(length=20), nullable=True),
        sa.Column('next_billing_date', sa.DateTime(), nullable=True),
        sa.Column('last_billing_date', sa.DateTime(), nullable=True),
        sa.Column('monthly_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('annual_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('custom_pricing', sa.JSON(), nullable=True),
        sa.Column('max_users', sa.Integer(), nullable=True),
        sa.Column('max_customers', sa.Integer(), nullable=True),
        sa.Column('max_products', sa.Integer(), nullable=True),
        sa.Column('max_invoices_per_month', sa.Integer(), nullable=True),
        sa.Column('max_storage_gb', sa.Integer(), nullable=True),
        sa.Column('custom_features', sa.JSON(), nullable=True),
        sa.Column('billing_contact_name', sa.String(length=255), nullable=True),
        sa.Column('billing_contact_email', sa.String(length=255), nullable=True),
        sa.Column('billing_address', sa.JSON(), nullable=True),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('payment_provider', sa.String(length=50), nullable=True),
        sa.Column('payment_reference', sa.String(length=255), nullable=True),
        sa.Column('cancellation_date', sa.DateTime(), nullable=True),
        sa.Column('cancellation_reason', sa.Text(), nullable=True),
        sa.Column('cancelled_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['plan_id'], ['subscription_plan_definitions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_subscription_company', 'company_subscriptions', ['company_id'])
    op.create_index('idx_subscription_plan', 'company_subscriptions', ['plan_id'])
    op.create_index('idx_subscription_status', 'company_subscriptions', ['subscription_status'])
    op.create_index('idx_subscription_billing', 'company_subscriptions', ['next_billing_date'])
    op.create_index('idx_subscription_trial', 'company_subscriptions', ['trial_end_date'])
    
    # Usage metrics table
    op.create_table('usage_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metric_name', sa.String(length=255), nullable=False),
        sa.Column('metric_category', sa.String(length=100), nullable=False),
        sa.Column('metric_value', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('metric_unit', sa.String(length=50), nullable=True),
        sa.Column('period_type', sa.String(length=20), nullable=False),
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('period_end', sa.DateTime(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_usage_company', 'usage_metrics', ['company_id'])
    op.create_index('idx_usage_metric', 'usage_metrics', ['metric_name'])
    op.create_index('idx_usage_period', 'usage_metrics', ['period_start', 'period_end'])
    op.create_index('idx_usage_category', 'usage_metrics', ['metric_category'])
    
    # System notifications table
    op.create_table('system_notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('target_companies', sa.JSON(), nullable=True),
        sa.Column('target_plans', sa.JSON(), nullable=True),
        sa.Column('target_users', sa.JSON(), nullable=True),
        sa.Column('delivery_method', sa.String(length=50), nullable=True),
        sa.Column('is_urgent', sa.Boolean(), nullable=True),
        sa.Column('scheduled_for', sa.DateTime(), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_sent', sa.Boolean(), nullable=True),
        sa.Column('action_url', sa.String(length=500), nullable=True),
        sa.Column('action_text', sa.String(length=100), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_notification_type', 'system_notifications', ['notification_type'])
    op.create_index('idx_notification_scheduled', 'system_notifications', ['scheduled_for'])
    op.create_index('idx_notification_active', 'system_notifications', ['is_active'])
    op.create_index('idx_notification_sent', 'system_notifications', ['is_sent'])
    
    # API keys table
    op.create_table('api_keys',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('key_name', sa.String(length=255), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('key_prefix', sa.String(length=20), nullable=False),
        sa.Column('service_name', sa.String(length=255), nullable=False),
        sa.Column('service_type', sa.String(length=100), nullable=False),
        sa.Column('allowed_scopes', sa.JSON(), nullable=True),
        sa.Column('rate_limit_per_hour', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('allowed_ips', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_api_key_hash', 'api_keys', ['key_hash'], unique=True)
    op.create_index('idx_api_key_service', 'api_keys', ['service_name'])
    op.create_index('idx_api_key_type', 'api_keys', ['service_type'])
    op.create_index('idx_api_key_active', 'api_keys', ['is_active'])
    op.create_index('idx_api_key_expires', 'api_keys', ['expires_at'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('api_keys')
    op.drop_table('system_notifications')
    op.drop_table('usage_metrics')
    op.drop_table('company_subscriptions')
    op.drop_table('subscription_plan_definitions')
    op.drop_table('system_configurations')
    op.drop_table('postal_codes')
    op.drop_table('greek_banks')
    op.drop_table('greek_legal_forms')
    op.drop_table('greek_business_activities')
    op.drop_table('greek_vat_rates')
    op.drop_table('greek_tax_offices')
    op.drop_table('greek_regions')
    
    # Drop enums
    op.execute("DROP TYPE IF EXISTS subscriptionstatus")
    op.execute("DROP TYPE IF EXISTS subscriptionplan")
    op.execute("DROP TYPE IF EXISTS configurationtype")
    op.execute("DROP TYPE IF EXISTS vatzone")
    op.execute("DROP TYPE IF EXISTS locationtype") 