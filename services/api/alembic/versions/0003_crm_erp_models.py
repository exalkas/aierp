"""Add CRM and ERP models

Revision ID: 0003
Revises: 0002
Create Date: 2024-01-01 02:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create campaigns table
    op.create_table('campaigns',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('campaign_number', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('campaign_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('objective', sa.String(length=50), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime()),
        sa.Column('planned_duration_days', sa.Integer()),
        sa.Column('actual_duration_days', sa.Integer()),
        sa.Column('budget', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('actual_cost', sa.Numeric(precision=15, scale=2), server_default='0'),
        sa.Column('cost_per_lead', sa.Numeric(precision=10, scale=2)),
        sa.Column('cost_per_acquisition', sa.Numeric(precision=10, scale=2)),
        sa.Column('roi_percentage', sa.Numeric(precision=5, scale=2)),
        sa.Column('target_audience_description', sa.Text()),
        sa.Column('target_demographics', sa.JSON(), server_default='{}'),
        sa.Column('target_geography', sa.JSON(), server_default='[]'),
        sa.Column('target_industries', sa.JSON(), server_default='[]'),
        sa.Column('target_company_sizes', sa.JSON(), server_default='[]'),
        sa.Column('primary_message', sa.Text()),
        sa.Column('value_proposition', sa.Text()),
        sa.Column('call_to_action', sa.String(length=255)),
        sa.Column('landing_page_url', sa.String(length=500)),
        sa.Column('channels', sa.JSON(), server_default='[]'),
        sa.Column('channel_budget_allocation', sa.JSON(), server_default='{}'),
        sa.Column('email_subject_line', sa.String(length=255)),
        sa.Column('email_template_id', sa.String(length=100)),
        sa.Column('sender_name', sa.String(length=100)),
        sa.Column('sender_email', sa.String(length=255)),
        sa.Column('social_platforms', sa.JSON(), server_default='[]'),
        sa.Column('hashtags', sa.JSON(), server_default='[]'),
        sa.Column('advertising_platforms', sa.JSON(), server_default='[]'),
        sa.Column('keywords', sa.JSON(), server_default='[]'),
        sa.Column('ad_copy', sa.Text()),
        sa.Column('event_name', sa.String(length=255)),
        sa.Column('event_location', sa.String(length=255)),
        sa.Column('booth_number', sa.String(length=50)),
        sa.Column('event_url', sa.String(length=500)),
        sa.Column('greek_regions_targeted', sa.JSON(), server_default='[]'),
        sa.Column('greek_business_types', sa.JSON(), server_default='[]'),
        sa.Column('requires_greek_content', sa.Boolean(), server_default='true'),
        sa.Column('gdpr_compliant', sa.Boolean(), server_default='true'),
        sa.Column('target_leads', sa.Integer(), server_default='0'),
        sa.Column('target_opportunities', sa.Integer(), server_default='0'),
        sa.Column('target_customers', sa.Integer(), server_default='0'),
        sa.Column('target_revenue', sa.Numeric(precision=15, scale=2), server_default='0'),
        sa.Column('leads_generated', sa.Integer(), server_default='0'),
        sa.Column('opportunities_created', sa.Integer(), server_default='0'),
        sa.Column('customers_acquired', sa.Integer(), server_default='0'),
        sa.Column('revenue_generated', sa.Numeric(precision=15, scale=2), server_default='0'),
        sa.Column('impressions', sa.Integer(), server_default='0'),
        sa.Column('clicks', sa.Integer(), server_default='0'),
        sa.Column('click_through_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('conversion_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('open_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('bounce_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('unsubscribe_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('qualified_leads', sa.Integer(), server_default='0'),
        sa.Column('lead_qualification_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('sales_qualified_leads', sa.Integer(), server_default='0'),
        sa.Column('lead_to_opportunity_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('opportunity_to_customer_rate', sa.Numeric(precision=5, scale=4)),
        sa.Column('campaign_manager_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('team_members', sa.JSON(), server_default='[]'),
        sa.Column('approval_required', sa.Boolean(), server_default='false'),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True)),
        sa.Column('approved_at', sa.DateTime()),
        sa.Column('approval_notes', sa.Text()),
        sa.Column('launch_checklist', sa.JSON(), server_default='[]'),
        sa.Column('launch_checklist_completed', sa.Boolean(), server_default='false'),
        sa.Column('execution_notes', sa.Text()),
        sa.Column('utm_source', sa.String(length=100)),
        sa.Column('utm_medium', sa.String(length=100)),
        sa.Column('utm_campaign', sa.String(length=100)),
        sa.Column('utm_content', sa.String(length=100)),
        sa.Column('utm_term', sa.String(length=100)),
        sa.Column('google_analytics_campaign', sa.String(length=100)),
        sa.Column('facebook_campaign_id', sa.String(length=100)),
        sa.Column('linkedin_campaign_id', sa.String(length=100)),
        sa.Column('mailchimp_campaign_id', sa.String(length=100)),
        sa.Column('creative_assets', sa.JSON(), server_default='[]'),
        sa.Column('document_assets', sa.JSON(), server_default='[]'),
        sa.Column('competitor_campaigns', sa.JSON(), server_default='[]'),
        sa.Column('competitive_advantages', sa.Text()),
        sa.Column('lessons_learned', sa.Text()),
        sa.Column('success_factors', sa.Text()),
        sa.Column('improvement_areas', sa.Text()),
        sa.Column('follow_up_actions', sa.Text()),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('campaign_theme', sa.String(length=100)),
        sa.Column('seasonal_campaign', sa.Boolean(), server_default='false'),
        sa.Column('custom_fields', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['campaign_manager_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('campaign_number')
    )
    op.create_index('idx_campaign_company', 'campaigns', ['company_id'])
    op.create_index('idx_campaign_number', 'campaigns', ['campaign_number'])
    op.create_index('idx_campaign_name', 'campaigns', ['name'])
    op.create_index('idx_campaign_type', 'campaigns', ['campaign_type'])
    op.create_index('idx_campaign_status', 'campaigns', ['status'])
    op.create_index('idx_campaign_priority', 'campaigns', ['priority'])
    op.create_index('idx_campaign_objective', 'campaigns', ['objective'])
    op.create_index('idx_campaign_manager', 'campaigns', ['campaign_manager_id'])
    op.create_index('idx_campaign_start_date', 'campaigns', ['start_date'])
    op.create_index('idx_campaign_end_date', 'campaigns', ['end_date'])
    op.create_index('idx_campaign_budget', 'campaigns', ['budget'])
    op.create_index('idx_campaign_leads_generated', 'campaigns', ['leads_generated'])
    op.create_index('idx_campaign_created_at', 'campaigns', ['created_at'])

    # Create leads table
    op.create_table('leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lead_number', sa.String(length=50), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('business_name', sa.String(length=255)),
        sa.Column('title', sa.String(length=100)),
        sa.Column('department', sa.String(length=100)),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('mobile', sa.String(length=20)),
        sa.Column('website', sa.String(length=255)),
        sa.Column('address_street', sa.String(length=255)),
        sa.Column('address_number', sa.String(length=10)),
        sa.Column('address_city', sa.String(length=100)),
        sa.Column('address_postal_code', sa.String(length=10)),
        sa.Column('address_region', sa.String(length=100)),
        sa.Column('address_country', sa.String(length=2), server_default='GR'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='new'),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('rating', sa.String(length=50), server_default='cold'),
        sa.Column('afm', sa.String(length=9)),
        sa.Column('doy', sa.String(length=10)),
        sa.Column('vat_number', sa.String(length=20)),
        sa.Column('business_activity', sa.String(length=255)),
        sa.Column('lead_score', sa.Integer(), server_default='0'),
        sa.Column('qualification_score', sa.Integer(), server_default='0'),
        sa.Column('qualified_date', sa.DateTime()),
        sa.Column('estimated_value', sa.Numeric(precision=15, scale=2)),
        sa.Column('estimated_close_date', sa.DateTime()),
        sa.Column('probability', sa.Integer(), server_default='0'),
        sa.Column('assigned_user_id', postgresql.UUID(as_uuid=True)),
        sa.Column('assigned_date', sa.DateTime()),
        sa.Column('first_contact_date', sa.DateTime()),
        sa.Column('last_contact_date', sa.DateTime()),
        sa.Column('next_follow_up_date', sa.DateTime()),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True)),
        sa.Column('utm_source', sa.String(length=100)),
        sa.Column('utm_medium', sa.String(length=100)),
        sa.Column('utm_campaign', sa.String(length=100)),
        sa.Column('utm_content', sa.String(length=100)),
        sa.Column('utm_term', sa.String(length=100)),
        sa.Column('converted', sa.Boolean(), server_default='false'),
        sa.Column('converted_date', sa.DateTime()),
        sa.Column('converted_to_business_entity_id', postgresql.UUID(as_uuid=True)),
        sa.Column('converted_to_opportunity_id', postgresql.UUID(as_uuid=True)),
        sa.Column('industry', sa.String(length=100)),
        sa.Column('company_size', sa.String(length=50)),
        sa.Column('annual_revenue', sa.String(length=50)),
        sa.Column('preferred_contact_method', sa.String(length=20), server_default='email'),
        sa.Column('preferred_contact_time', sa.String(length=50)),
        sa.Column('language', sa.String(length=2), server_default='el'),
        sa.Column('marketing_consent', sa.Boolean(), server_default='false'),
        sa.Column('newsletter_subscription', sa.Boolean(), server_default='false'),
        sa.Column('gdpr_consent', sa.Boolean(), server_default='false'),
        sa.Column('gdpr_consent_date', sa.DateTime()),
        sa.Column('description', sa.Text()),
        sa.Column('notes', sa.Text()),
        sa.Column('pain_points', sa.Text()),
        sa.Column('solution_interest', sa.Text()),
        sa.Column('budget_range', sa.String(length=50)),
        sa.Column('decision_timeframe', sa.String(length=50)),
        sa.Column('has_budget', sa.Boolean()),
        sa.Column('has_authority', sa.Boolean()),
        sa.Column('has_need', sa.Boolean()),
        sa.Column('has_timeline', sa.Boolean()),
        sa.Column('auto_follow_up_enabled', sa.Boolean(), server_default='true'),
        sa.Column('last_email_sent', sa.DateTime()),
        sa.Column('email_open_count', sa.Integer(), server_default='0'),
        sa.Column('email_click_count', sa.Integer(), server_default='0'),
        sa.Column('linkedin_profile', sa.String(length=255)),
        sa.Column('twitter_handle', sa.String(length=100)),
        sa.Column('facebook_profile', sa.String(length=255)),
        sa.Column('referral_source', sa.String(length=255)),
        sa.Column('competitor_currently_using', sa.String(length=255)),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('custom_fields', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['assigned_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ),
        sa.ForeignKeyConstraint(['converted_to_business_entity_id'], ['business_entities.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('lead_number')
    )
    op.create_index('idx_lead_company', 'leads', ['company_id'])
    op.create_index('idx_lead_number', 'leads', ['lead_number'])
    op.create_index('idx_lead_email', 'leads', ['email'])
    op.create_index('idx_lead_status', 'leads', ['status'])
    op.create_index('idx_lead_source', 'leads', ['source'])
    op.create_index('idx_lead_rating', 'leads', ['rating'])
    op.create_index('idx_lead_assigned_user', 'leads', ['assigned_user_id'])
    op.create_index('idx_lead_campaign', 'leads', ['campaign_id'])
    op.create_index('idx_lead_afm', 'leads', ['afm'])
    op.create_index('idx_lead_converted', 'leads', ['converted'])
    op.create_index('idx_lead_score', 'leads', ['lead_score'])
    op.create_index('idx_lead_next_follow_up', 'leads', ['next_follow_up_date'])
    op.create_index('idx_lead_business_name', 'leads', ['business_name'])
    op.create_index('idx_lead_created_at', 'leads', ['created_at'])

    # Create opportunities table
    op.create_table('opportunities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('opportunity_number', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('business_entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contact_id', postgresql.UUID(as_uuid=True)),
        sa.Column('stage', sa.String(length=50), nullable=False, server_default='prospecting'),
        sa.Column('opportunity_type', sa.String(length=50), nullable=False, server_default='new_business'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='EUR'),
        sa.Column('expected_revenue', sa.Numeric(precision=15, scale=2)),
        sa.Column('discount_percentage', sa.Numeric(precision=5, scale=2), server_default='0'),
        sa.Column('discount_amount', sa.Numeric(precision=15, scale=2), server_default='0'),
        sa.Column('probability', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('weighted_amount', sa.Numeric(precision=15, scale=2)),
        sa.Column('expected_close_date', sa.DateTime(), nullable=False),
        sa.Column('actual_close_date', sa.DateTime()),
        sa.Column('sales_cycle_days', sa.Integer()),
        sa.Column('requires_tender', sa.Boolean(), server_default='false'),
        sa.Column('tender_deadline', sa.DateTime()),
        sa.Column('tender_number', sa.String(length=100)),
        sa.Column('is_government_opportunity', sa.Boolean(), server_default='false'),
        sa.Column('government_procurement_type', sa.String(length=100)),
        sa.Column('assigned_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sales_team_members', sa.JSON(), server_default='[]'),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True)),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True)),
        sa.Column('referral_source', sa.String(length=255)),
        sa.Column('competitors', sa.JSON(), server_default='[]'),
        sa.Column('competitive_advantages', sa.Text()),
        sa.Column('competitive_threats', sa.Text()),
        sa.Column('solution_description', sa.Text()),
        sa.Column('key_requirements', sa.Text()),
        sa.Column('decision_criteria', sa.Text()),
        sa.Column('decision_makers', sa.JSON(), server_default='[]'),
        sa.Column('influencers', sa.JSON(), server_default='[]'),
        sa.Column('technical_evaluators', sa.JSON(), server_default='[]'),
        sa.Column('budget_approvers', sa.JSON(), server_default='[]'),
        sa.Column('next_step', sa.String(length=255)),
        sa.Column('next_step_date', sa.DateTime()),
        sa.Column('last_activity_date', sa.DateTime()),
        sa.Column('proposal_sent_date', sa.DateTime()),
        sa.Column('proposal_deadline', sa.DateTime()),
        sa.Column('contract_terms', sa.Text()),
        sa.Column('payment_terms', sa.String(length=100)),
        sa.Column('delivery_timeline', sa.String(length=100)),
        sa.Column('won_reason', sa.Text()),
        sa.Column('lost_reason', sa.Text()),
        sa.Column('competitor_won', sa.String(length=255)),
        sa.Column('lessons_learned', sa.Text()),
        sa.Column('follow_up_date', sa.DateTime()),
        sa.Column('renewal_date', sa.DateTime()),
        sa.Column('renewal_probability', sa.Integer()),
        sa.Column('preferred_communication_method', sa.String(length=50)),
        sa.Column('meeting_frequency', sa.String(length=50)),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('industry_focus', sa.String(length=100)),
        sa.Column('vertical_market', sa.String(length=100)),
        sa.Column('risk_factors', sa.Text()),
        sa.Column('risk_mitigation', sa.Text()),
        sa.Column('confidence_level', sa.Integer(), server_default='50'),
        sa.Column('public_sector', sa.Boolean(), server_default='false'),
        sa.Column('requires_certification', sa.String(length=255)),
        sa.Column('local_partner_required', sa.Boolean(), server_default='false'),
        sa.Column('language_requirements', sa.String(length=100)),
        sa.Column('engagement_score', sa.Integer(), server_default='0'),
        sa.Column('response_time_hours', sa.Numeric(precision=5, scale=2)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['business_entity_id'], ['business_entities.id'], ),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
        sa.ForeignKeyConstraint(['assigned_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('opportunity_number')
    )
    op.create_index('idx_opportunity_company', 'opportunities', ['company_id'])
    op.create_index('idx_opportunity_number', 'opportunities', ['opportunity_number'])
    op.create_index('idx_opportunity_business_entity', 'opportunities', ['business_entity_id'])
    op.create_index('idx_opportunity_contact', 'opportunities', ['contact_id'])
    op.create_index('idx_opportunity_stage', 'opportunities', ['stage'])
    op.create_index('idx_opportunity_type', 'opportunities', ['opportunity_type'])
    op.create_index('idx_opportunity_priority', 'opportunities', ['priority'])
    op.create_index('idx_opportunity_assigned_user', 'opportunities', ['assigned_user_id'])
    op.create_index('idx_opportunity_lead', 'opportunities', ['lead_id'])
    op.create_index('idx_opportunity_campaign', 'opportunities', ['campaign_id'])
    op.create_index('idx_opportunity_expected_close', 'opportunities', ['expected_close_date'])
    op.create_index('idx_opportunity_amount', 'opportunities', ['amount'])
    op.create_index('idx_opportunity_probability', 'opportunities', ['probability'])
    op.create_index('idx_opportunity_source', 'opportunities', ['source'])
    op.create_index('idx_opportunity_tender', 'opportunities', ['requires_tender'])
    op.create_index('idx_opportunity_government', 'opportunities', ['is_government_opportunity'])
    op.create_index('idx_opportunity_created_at', 'opportunities', ['created_at'])

    # Add foreign key to leads.converted_to_opportunity_id
    op.create_foreign_key('fk_lead_converted_opportunity', 'leads', 'opportunities', ['converted_to_opportunity_id'], ['id'])

    # Create activities table
    op.create_table('activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_number', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('activity_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='planned'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('business_entity_id', postgresql.UUID(as_uuid=True)),
        sa.Column('contact_id', postgresql.UUID(as_uuid=True)),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True)),
        sa.Column('opportunity_id', postgresql.UUID(as_uuid=True)),
        sa.Column('case_id', postgresql.UUID(as_uuid=True)),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True)),
        sa.Column('assigned_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime()),
        sa.Column('due_date', sa.DateTime()),
        sa.Column('completed_date', sa.DateTime()),
        sa.Column('duration_minutes', sa.Integer()),
        sa.Column('is_recurring', sa.Boolean(), server_default='false'),
        sa.Column('recurrence_pattern', sa.String(length=50)),
        sa.Column('recurrence_interval', sa.Integer(), server_default='1'),
        sa.Column('recurrence_end_date', sa.DateTime()),
        sa.Column('parent_activity_id', postgresql.UUID(as_uuid=True)),
        sa.Column('call_direction', sa.String(length=50)),
        sa.Column('call_outcome', sa.String(length=50)),
        sa.Column('phone_number', sa.String(length=20)),
        sa.Column('call_duration_seconds', sa.Integer()),
        sa.Column('meeting_type', sa.String(length=50)),
        sa.Column('location', sa.String(length=255)),
        sa.Column('meeting_url', sa.String(length=500)),
        sa.Column('attendees', sa.JSON(), server_default='[]'),
        sa.Column('meeting_agenda', sa.Text()),
        sa.Column('meeting_minutes', sa.Text()),
        sa.Column('email_subject', sa.String(length=255)),
        sa.Column('email_to', sa.JSON(), server_default='[]'),
        sa.Column('email_cc', sa.JSON(), server_default='[]'),
        sa.Column('email_bcc', sa.JSON(), server_default='[]'),
        sa.Column('email_message_id', sa.String(length=255)),
        sa.Column('email_thread_id', sa.String(length=255)),
        sa.Column('completion_percentage', sa.Integer(), server_default='0'),
        sa.Column('checklist', sa.JSON(), server_default='[]'),
        sa.Column('dependencies', sa.JSON(), server_default='[]'),
        sa.Column('outcome_description', sa.Text()),
        sa.Column('next_action', sa.String(length=255)),
        sa.Column('next_action_date', sa.DateTime()),
        sa.Column('follow_up_required', sa.Boolean(), server_default='false'),
        sa.Column('communication_channel', sa.String(length=50)),
        sa.Column('response_received', sa.Boolean(), server_default='false'),
        sa.Column('response_date', sa.DateTime()),
        sa.Column('involves_contract', sa.Boolean(), server_default='false'),
        sa.Column('contract_reference', sa.String(length=100)),
        sa.Column('requires_documentation', sa.Boolean(), server_default='false'),
        sa.Column('documentation_completed', sa.Boolean(), server_default='false'),
        sa.Column('reminder_enabled', sa.Boolean(), server_default='true'),
        sa.Column('reminder_minutes_before', sa.Integer(), server_default='15'),
        sa.Column('reminder_sent', sa.Boolean(), server_default='false'),
        sa.Column('notification_settings', sa.JSON(), server_default='{}'),
        sa.Column('requires_travel', sa.Boolean(), server_default='false'),
        sa.Column('travel_time_minutes', sa.Integer()),
        sa.Column('address', sa.String(length=500)),
        sa.Column('city', sa.String(length=100)),
        sa.Column('postal_code', sa.String(length=10)),
        sa.Column('estimated_cost', sa.Numeric(precision=10, scale=2)),
        sa.Column('actual_cost', sa.Numeric(precision=10, scale=2)),
        sa.Column('is_billable', sa.Boolean(), server_default='false'),
        sa.Column('billable_hours', sa.Numeric(precision=5, scale=2)),
        sa.Column('hourly_rate', sa.Numeric(precision=10, scale=2)),
        sa.Column('satisfaction_rating', sa.Integer()),
        sa.Column('quality_score', sa.Integer()),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('category', sa.String(length=100)),
        sa.Column('project_name', sa.String(length=255)),
        sa.Column('custom_fields', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['business_entity_id'], ['business_entities.id'], ),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.ForeignKeyConstraint(['opportunity_id'], ['opportunities.id'], ),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.ForeignKeyConstraint(['assigned_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['parent_activity_id'], ['activities.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('activity_number')
    )
    op.create_index('idx_activity_company', 'activities', ['company_id'])
    op.create_index('idx_activity_number', 'activities', ['activity_number'])
    op.create_index('idx_activity_type', 'activities', ['activity_type'])
    op.create_index('idx_activity_status', 'activities', ['status'])
    op.create_index('idx_activity_priority', 'activities', ['priority'])
    op.create_index('idx_activity_business_entity', 'activities', ['business_entity_id'])
    op.create_index('idx_activity_contact', 'activities', ['contact_id'])
    op.create_index('idx_activity_lead', 'activities', ['lead_id'])
    op.create_index('idx_activity_opportunity', 'activities', ['opportunity_id'])
    op.create_index('idx_activity_case', 'activities', ['case_id'])
    op.create_index('idx_activity_assigned_user', 'activities', ['assigned_user_id'])
    op.create_index('idx_activity_created_by', 'activities', ['created_by_user_id'])
    op.create_index('idx_activity_start_date', 'activities', ['start_date'])
    op.create_index('idx_activity_due_date', 'activities', ['due_date'])
    op.create_index('idx_activity_end_date', 'activities', ['end_date'])
    op.create_index('idx_activity_completed_date', 'activities', ['completed_date'])
    op.create_index('idx_activity_recurring', 'activities', ['is_recurring'])
    op.create_index('idx_activity_parent', 'activities', ['parent_activity_id'])
    op.create_index('idx_activity_follow_up', 'activities', ['follow_up_required'])
    op.create_index('idx_activity_billable', 'activities', ['is_billable'])
    op.create_index('idx_activity_created_at', 'activities', ['created_at'])

    # Create cases table
    op.create_table('cases',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('case_number', sa.String(length=50), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('case_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='new'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='moderate'),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('business_entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contact_id', postgresql.UUID(as_uuid=True)),
        sa.Column('product_id', postgresql.UUID(as_uuid=True)),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True)),
        sa.Column('order_number', sa.String(length=100)),
        sa.Column('assigned_user_id', postgresql.UUID(as_uuid=True)),
        sa.Column('assigned_team', sa.String(length=100)),
        sa.Column('escalated_to_user_id', postgresql.UUID(as_uuid=True)),
        sa.Column('created_date', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('first_response_date', sa.DateTime()),
        sa.Column('last_response_date', sa.DateTime()),
        sa.Column('resolution_date', sa.DateTime()),
        sa.Column('closed_date', sa.DateTime()),
        sa.Column('first_response_sla_hours', sa.Integer(), server_default='24'),
        sa.Column('resolution_sla_hours', sa.Integer(), server_default='72'),
        sa.Column('first_response_breached', sa.Boolean(), server_default='false'),
        sa.Column('resolution_sla_breached', sa.Boolean(), server_default='false'),
        sa.Column('resolution_type', sa.String(length=50)),
        sa.Column('resolution_description', sa.Text()),
        sa.Column('resolution_time_hours', sa.Numeric(precision=5, scale=2)),
        sa.Column('work_time_hours', sa.Numeric(precision=5, scale=2)),
        sa.Column('satisfaction_rating', sa.Integer()),
        sa.Column('satisfaction_feedback', sa.Text()),
        sa.Column('satisfaction_survey_sent', sa.Boolean(), server_default='false'),
        sa.Column('satisfaction_survey_completed', sa.Boolean(), server_default='false'),
        sa.Column('customer_email', sa.String(length=255)),
        sa.Column('customer_phone', sa.String(length=20)),
        sa.Column('preferred_contact_method', sa.String(length=50)),
        sa.Column('follow_up_required', sa.Boolean(), server_default='false'),
        sa.Column('follow_up_date', sa.DateTime()),
        sa.Column('category', sa.String(length=100)),
        sa.Column('subcategory', sa.String(length=100)),
        sa.Column('root_cause', sa.String(length=255)),
        sa.Column('environment', sa.String(length=100)),
        sa.Column('browser_version', sa.String(length=100)),
        sa.Column('operating_system', sa.String(length=100)),
        sa.Column('error_message', sa.Text()),
        sa.Column('steps_to_reproduce', sa.Text()),
        sa.Column('affects_compliance', sa.Boolean(), server_default='false'),
        sa.Column('affects_aade_integration', sa.Boolean(), server_default='false'),
        sa.Column('requires_legal_review', sa.Boolean(), server_default='false'),
        sa.Column('greek_regulation_reference', sa.String(length=255)),
        sa.Column('escalation_level', sa.Integer(), server_default='0'),
        sa.Column('escalation_reason', sa.Text()),
        sa.Column('escalation_date', sa.DateTime()),
        sa.Column('previous_assignee_id', postgresql.UUID(as_uuid=True)),
        sa.Column('knowledge_article_id', sa.String(length=100)),
        sa.Column('solution_article_created', sa.Boolean(), server_default='false'),
        sa.Column('estimated_cost', sa.Numeric(precision=10, scale=2)),
        sa.Column('actual_cost', sa.Numeric(precision=10, scale=2)),
        sa.Column('billable_to_customer', sa.Boolean(), server_default='false'),
        sa.Column('parent_case_id', postgresql.UUID(as_uuid=True)),
        sa.Column('is_master_case', sa.Boolean(), server_default='false'),
        sa.Column('reopen_count', sa.Integer(), server_default='0'),
        sa.Column('last_reopened_date', sa.DateTime()),
        sa.Column('reopen_reason', sa.Text()),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('custom_fields', sa.JSON(), server_default='{}'),
        sa.Column('internal_notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['business_entity_id'], ['business_entities.id'], ),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.ForeignKeyConstraint(['assigned_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['escalated_to_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['previous_assignee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['parent_case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('case_number')
    )
    op.create_index('idx_case_company', 'cases', ['company_id'])
    op.create_index('idx_case_number', 'cases', ['case_number'])
    op.create_index('idx_case_subject', 'cases', ['subject'])
    op.create_index('idx_case_type', 'cases', ['case_type'])
    op.create_index('idx_case_status', 'cases', ['status'])
    op.create_index('idx_case_priority', 'cases', ['priority'])
    op.create_index('idx_case_severity', 'cases', ['severity'])
    op.create_index('idx_case_source', 'cases', ['source'])
    op.create_index('idx_case_business_entity', 'cases', ['business_entity_id'])
    op.create_index('idx_case_contact', 'cases', ['contact_id'])
    op.create_index('idx_case_product', 'cases', ['product_id'])
    op.create_index('idx_case_assigned_user', 'cases', ['assigned_user_id'])
    op.create_index('idx_case_escalated_to', 'cases', ['escalated_to_user_id'])
    op.create_index('idx_case_created_date', 'cases', ['created_date'])
    op.create_index('idx_case_resolution_date', 'cases', ['resolution_date'])
    op.create_index('idx_case_closed_date', 'cases', ['closed_date'])
    op.create_index('idx_case_first_response_breached', 'cases', ['first_response_breached'])
    op.create_index('idx_case_resolution_sla_breached', 'cases', ['resolution_sla_breached'])
    op.create_index('idx_case_parent', 'cases', ['parent_case_id'])
    op.create_index('idx_case_follow_up', 'cases', ['follow_up_required'])
    op.create_index('idx_case_satisfaction', 'cases', ['satisfaction_rating'])
    op.create_index('idx_case_escalation_level', 'cases', ['escalation_level'])
    op.create_index('idx_case_created_at', 'cases', ['created_at'])

    # Add foreign key to activities.case_id
    op.create_foreign_key('fk_activity_case', 'activities', 'cases', ['case_id'], ['id'])

    # Create ERP tables (Purchase Orders, Inventory, Accounting)
    
    # Create locations table
    op.create_table('locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('location_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('location_type', sa.String(length=50), nullable=False, server_default='warehouse'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('is_default', sa.Boolean(), server_default='false'),
        sa.Column('address_street', sa.String(length=255)),
        sa.Column('address_number', sa.String(length=10)),
        sa.Column('address_city', sa.String(length=100)),
        sa.Column('address_postal_code', sa.String(length=10)),
        sa.Column('address_region', sa.String(length=100)),
        sa.Column('address_country', sa.String(length=2), server_default='GR'),
        sa.Column('parent_location_id', postgresql.UUID(as_uuid=True)),
        sa.Column('location_path', sa.String(length=500)),
        sa.Column('capacity_cubic_meters', sa.Numeric(precision=10, scale=3)),
        sa.Column('max_weight_kg', sa.Numeric(precision=10, scale=3)),
        sa.Column('temperature_controlled', sa.Boolean(), server_default='false'),
        sa.Column('min_temperature', sa.Numeric(precision=5, scale=2)),
        sa.Column('max_temperature', sa.Numeric(precision=5, scale=2)),
        sa.Column('allow_negative_stock', sa.Boolean(), server_default='false'),
        sa.Column('require_lot_tracking', sa.Boolean(), server_default='false'),
        sa.Column('require_serial_tracking', sa.Boolean(), server_default='false'),
        sa.Column('location_manager_id', postgresql.UUID(as_uuid=True)),
        sa.Column('contact_phone', sa.String(length=20)),
        sa.Column('contact_email', sa.String(length=255)),
        sa.Column('operating_hours', sa.JSON(), server_default='{}'),
        sa.Column('custom_fields', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['parent_location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['location_manager_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('location_code')
    )
    op.create_index('idx_location_company', 'locations', ['company_id'])
    op.create_index('idx_location_code', 'locations', ['location_code'])
    op.create_index('idx_location_type', 'locations', ['location_type'])
    op.create_index('idx_location_active', 'locations', ['is_active'])
    op.create_index('idx_location_parent', 'locations', ['parent_location_id'])

    # Create purchase_orders table
    op.create_table('purchase_orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('po_number', sa.String(length=50), nullable=False),
        sa.Column('reference_number', sa.String(length=100)),
        sa.Column('requisition_number', sa.String(length=100)),
        sa.Column('po_type', sa.String(length=50), nullable=False, server_default='standard'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('supplier_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('supplier_contact_id', postgresql.UUID(as_uuid=True)),
        sa.Column('order_date', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('requested_delivery_date', sa.DateTime()),
        sa.Column('promised_delivery_date', sa.DateTime()),
        sa.Column('expected_delivery_date', sa.DateTime()),
        sa.Column('actual_delivery_date', sa.DateTime()),
        sa.Column('subtotal', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('tax_amount', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('discount_amount', sa.Numeric(precision=15, scale=2), server_default='0'),
        sa.Column('discount_percentage', sa.Numeric(precision=5, scale=2), server_default='0'),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='EUR'),
        sa.Column('exchange_rate', sa.Numeric(precision=10, scale=6), server_default='1.0'),
        sa.Column('delivery_terms', sa.String(length=50), server_default='ddp'),
        sa.Column('delivery_address', sa.Text()),
        sa.Column('delivery_location_id', postgresql.UUID(as_uuid=True)),
        sa.Column('shipping_method', sa.String(length=100)),
        sa.Column('freight_terms', sa.String(length=100)),
        sa.Column('payment_terms', sa.String(length=100)),
        sa.Column('payment_due_days', sa.Integer(), server_default='30'),
        sa.Column('payment_method', sa.String(length=100)),
        sa.Column('requires_invoice', sa.Boolean(), server_default='true'),
        sa.Column('requires_delivery_note', sa.Boolean(), server_default='true'),
        sa.Column('supplier_afm', sa.String(length=9)),
        sa.Column('supplier_vat_number', sa.String(length=20)),
        sa.Column('requires_approval', sa.Boolean(), server_default='true'),
        sa.Column('approval_limit', sa.Numeric(precision=15, scale=2)),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True)),
        sa.Column('approved_at', sa.DateTime()),
        sa.Column('approval_notes', sa.Text()),
        sa.Column('buyer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('department', sa.String(length=100)),
        sa.Column('cost_center', sa.String(length=100)),
        sa.Column('project_id', postgresql.UUID(as_uuid=True)),
        sa.Column('quote_reference', sa.String(length=100)),
        sa.Column('contract_reference', sa.String(length=100)),
        sa.Column('requires_inspection', sa.Boolean(), server_default='false'),
        sa.Column('inspection_notes', sa.Text()),
        sa.Column('quality_requirements', sa.Text()),
        sa.Column('special_instructions', sa.Text()),
        sa.Column('internal_notes', sa.Text()),
        sa.Column('supplier_notes', sa.Text()),
        sa.Column('tracking_number', sa.String(length=100)),
        sa.Column('carrier', sa.String(length=100)),
        sa.Column('expected_lead_time_days', sa.Integer()),
        sa.Column('on_time_delivery', sa.Boolean()),
        sa.Column('delivery_performance_score', sa.Integer()),
        sa.Column('quality_score', sa.Integer()),
        sa.Column('supplier_rating', sa.Integer()),
        sa.Column('goods_received_by', postgresql.UUID(as_uuid=True)),
        sa.Column('goods_received_date', sa.DateTime()),
        sa.Column('receiving_notes', sa.Text()),
        sa.Column('invoice_received', sa.Boolean(), server_default='false'),
        sa.Column('invoice_matched', sa.Boolean(), server_default='false'),
        sa.Column('three_way_match_status', sa.String(length=50)),
        sa.Column('closed_by', postgresql.UUID(as_uuid=True)),
        sa.Column('closed_date', sa.DateTime()),
        sa.Column('closure_reason', sa.String(length=100)),
        sa.Column('emergency_procurement', sa.Boolean(), server_default='false'),
        sa.Column('single_source_justification', sa.Text()),
        sa.Column('environmental_requirements', sa.Text()),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('custom_fields', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['supplier_id'], ['business_entities.id'], ),
        sa.ForeignKeyConstraint(['supplier_contact_id'], ['contacts.id'], ),
        sa.ForeignKeyConstraint(['buyer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['goods_received_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['closed_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('po_number')
    )
    op.create_index('idx_po_company', 'purchase_orders', ['company_id'])
    op.create_index('idx_po_number', 'purchase_orders', ['po_number'])
    op.create_index('idx_po_supplier', 'purchase_orders', ['supplier_id'])
    op.create_index('idx_po_type', 'purchase_orders', ['po_type'])
    op.create_index('idx_po_status', 'purchase_orders', ['status'])
    op.create_index('idx_po_priority', 'purchase_orders', ['priority'])
    op.create_index('idx_po_buyer', 'purchase_orders', ['buyer_id'])
    op.create_index('idx_po_order_date', 'purchase_orders', ['order_date'])
    op.create_index('idx_po_delivery_date', 'purchase_orders', ['requested_delivery_date'])
    op.create_index('idx_po_total_amount', 'purchase_orders', ['total_amount'])
    op.create_index('idx_po_approved_by', 'purchase_orders', ['approved_by'])
    op.create_index('idx_po_created_at', 'purchase_orders', ['created_at'])

    # Create additional CRM/ERP support tables as needed
    # (This migration is already quite large, so we'll keep core tables for now)
    
    print("CRM and ERP models migration completed successfully!")


def downgrade() -> None:
    # Drop tables in reverse order to handle foreign key constraints
    op.drop_table('purchase_orders')
    op.drop_table('locations')
    op.drop_table('cases')
    op.drop_table('activities')
    op.drop_table('opportunities')
    op.drop_table('leads')
    op.drop_table('campaigns')
    
    print("CRM and ERP models migration downgraded successfully!") 