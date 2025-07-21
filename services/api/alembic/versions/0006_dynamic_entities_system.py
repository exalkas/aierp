"""Dynamic Entities System

Revision ID: 0006_dynamic_entities_system
Revises: 0005_master_database_models
Create Date: 2024-01-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0006_dynamic_entities_system'
down_revision = '0005_master_database_models'
branch_labels = None
depends_on = None


def upgrade():
    """Create tables for Dynamic Entities System"""
    
    # Create entity_scope enum
    entity_scope_enum = postgresql.ENUM('global', 'company', 'user', name='entityscope')
    entity_scope_enum.create(op.get_bind())
    
    # Create entity_status enum
    entity_status_enum = postgresql.ENUM('active', 'draft', 'archived', 'deprecated', name='entitystatus')
    entity_status_enum.create(op.get_bind())
    
    # Create field_type enum
    field_type_enum = postgresql.ENUM(
        'text', 'number', 'email', 'url', 'password', 'textarea', 'rich_text', 
        'phone', 'date', 'datetime', 'time', 'select', 'multiselect', 'radio', 
        'checkbox', 'switch', 'file', 'image', 'afm', 'amka', 'greek_phone', 
        'greek_address', 'doy_selector', 'region_selector', 'json', 'formula', 
        'lookup', 'relationship', name='fieldtype'
    )
    field_type_enum.create(op.get_bind())
    
    # Create field_widget_type enum
    field_widget_type_enum = postgresql.ENUM(
        'input', 'textarea', 'select', 'checkbox', 'radio', 'date_picker', 
        'time_picker', 'file_upload', 'color_picker', 'slider', 'toggle', 
        'rating', 'tags', 'editor', 'custom', name='fieldwidgettype'
    )
    field_widget_type_enum.create(op.get_bind())
    
    # Create layout_type enum
    layout_type_enum = postgresql.ENUM(
        'form', 'list', 'detail', 'search', 'dashboard', 'report', 'mobile', 'print', 
        name='layouttype'
    )
    layout_type_enum.create(op.get_bind())
    
    # Create layout_status enum
    layout_status_enum = postgresql.ENUM('active', 'draft', 'archived', 'deprecated', name='layoutstatus')
    layout_status_enum.create(op.get_bind())
    
    # Create responsive_breakpoint enum
    responsive_breakpoint_enum = postgresql.ENUM('xs', 'sm', 'md', 'lg', 'xl', name='responsivebreakpoint')
    responsive_breakpoint_enum.create(op.get_bind())
    
    # Create dynamic_entities table
    op.create_table('dynamic_entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_name_greek', sa.String(length=255), nullable=True),
        sa.Column('description_greek', sa.Text(), nullable=True),
        sa.Column('scope', entity_scope_enum, nullable=False),
        sa.Column('status', entity_status_enum, nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('schema_version', sa.Integer(), nullable=False),
        sa.Column('is_system_entity', sa.Boolean(), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('singular_label', sa.String(length=100), nullable=False),
        sa.Column('plural_label', sa.String(length=100), nullable=False),
        sa.Column('singular_label_greek', sa.String(length=100), nullable=True),
        sa.Column('plural_label_greek', sa.String(length=100), nullable=True),
        sa.Column('is_auditable', sa.Boolean(), nullable=False),
        sa.Column('supports_workflow', sa.Boolean(), nullable=False),
        sa.Column('supports_attachments', sa.Boolean(), nullable=False),
        sa.Column('supports_comments', sa.Boolean(), nullable=False),
        sa.Column('supports_tags', sa.Boolean(), nullable=False),
        sa.Column('api_name', sa.String(length=100), nullable=False),
        sa.Column('endpoint_prefix', sa.String(length=50), nullable=False),
        sa.Column('table_name', sa.String(length=100), nullable=False),
        sa.Column('primary_key_field', sa.String(length=50), nullable=True),
        sa.Column('default_sort_field', sa.String(length=100), nullable=True),
        sa.Column('default_sort_direction', sa.String(length=4), nullable=True),
        sa.Column('records_per_page', sa.Integer(), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('requires_greek_validation', sa.Boolean(), nullable=False),
        sa.Column('aade_integration', sa.Boolean(), nullable=False),
        sa.Column('vat_applicable', sa.Boolean(), nullable=False),
        sa.Column('parent_entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('related_entities', sa.JSON(), nullable=True),
        sa.Column('email_notifications', sa.Boolean(), nullable=False),
        sa.Column('webhook_url', sa.String(length=500), nullable=True),
        sa.Column('notification_settings', sa.JSON(), nullable=True),
        sa.Column('custom_properties', sa.JSON(), nullable=True),
        sa.Column('business_rules', sa.JSON(), nullable=True),
        sa.Column('validation_rules', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['parent_entity_id'], ['dynamic_entities.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('api_name')
    )
    
    # Create indexes for dynamic_entities
    op.create_index('idx_dynamic_entity_company', 'dynamic_entities', ['company_id'])
    op.create_index('idx_dynamic_entity_name', 'dynamic_entities', ['name'])
    op.create_index('idx_dynamic_entity_status', 'dynamic_entities', ['status'])
    op.create_index('idx_dynamic_entity_scope', 'dynamic_entities', ['scope'])
    op.create_index('idx_dynamic_entity_api_name', 'dynamic_entities', ['api_name'])
    op.create_index('idx_dynamic_entity_table_name', 'dynamic_entities', ['table_name'])
    op.create_index('idx_dynamic_entity_parent', 'dynamic_entities', ['parent_entity_id'])
    op.create_index('idx_dynamic_entity_system', 'dynamic_entities', ['is_system_entity'])
    op.create_index('idx_dynamic_entity_created', 'dynamic_entities', ['created_at'])
    op.create_index('idx_dynamic_entity_updated', 'dynamic_entities', ['updated_at'])
    
    # Create dynamic_fields table
    op.create_table('dynamic_fields',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_name_greek', sa.String(length=255), nullable=True),
        sa.Column('description_greek', sa.Text(), nullable=True),
        sa.Column('placeholder_greek', sa.String(length=255), nullable=True),
        sa.Column('field_type', field_type_enum, nullable=False),
        sa.Column('widget_type', field_widget_type_enum, nullable=False),
        sa.Column('data_type', sa.String(length=50), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False),
        sa.Column('is_unique', sa.Boolean(), nullable=False),
        sa.Column('is_indexed', sa.Boolean(), nullable=False),
        sa.Column('is_searchable', sa.Boolean(), nullable=False),
        sa.Column('is_sortable', sa.Boolean(), nullable=False),
        sa.Column('is_filterable', sa.Boolean(), nullable=False),
        sa.Column('is_exportable', sa.Boolean(), nullable=False),
        sa.Column('placeholder', sa.String(length=255), nullable=True),
        sa.Column('help_text', sa.Text(), nullable=True),
        sa.Column('help_text_greek', sa.Text(), nullable=True),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('min_length', sa.Integer(), nullable=True),
        sa.Column('max_length', sa.Integer(), nullable=True),
        sa.Column('min_value', sa.Numeric(precision=15, scale=4), nullable=True),
        sa.Column('max_value', sa.Numeric(precision=15, scale=4), nullable=True),
        sa.Column('regex_pattern', sa.String(length=500), nullable=True),
        sa.Column('validation_message', sa.String(length=255), nullable=True),
        sa.Column('validation_message_greek', sa.String(length=255), nullable=True),
        sa.Column('options', sa.JSON(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('grid_column_span', sa.Integer(), nullable=True),
        sa.Column('section', sa.String(length=100), nullable=True),
        sa.Column('is_visible', sa.Boolean(), nullable=False),
        sa.Column('is_editable', sa.Boolean(), nullable=False),
        sa.Column('is_readonly', sa.Boolean(), nullable=False),
        sa.Column('show_in_list', sa.Boolean(), nullable=False),
        sa.Column('show_in_detail', sa.Boolean(), nullable=False),
        sa.Column('show_in_search', sa.Boolean(), nullable=False),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('requires_greek_validation', sa.Boolean(), nullable=False),
        sa.Column('aade_field_mapping', sa.String(length=100), nullable=True),
        sa.Column('lookup_entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('lookup_display_field', sa.String(length=100), nullable=True),
        sa.Column('lookup_filter', sa.JSON(), nullable=True),
        sa.Column('formula_expression', sa.Text(), nullable=True),
        sa.Column('formula_dependencies', sa.JSON(), nullable=True),
        sa.Column('conditional_logic', sa.JSON(), nullable=True),
        sa.Column('custom_properties', sa.JSON(), nullable=True),
        sa.Column('css_classes', sa.String(length=255), nullable=True),
        sa.Column('custom_validation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['entity_id'], ['dynamic_entities.id'], ),
        sa.ForeignKeyConstraint(['lookup_entity_id'], ['dynamic_entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for dynamic_fields
    op.create_index('idx_dynamic_field_entity', 'dynamic_fields', ['entity_id'])
    op.create_index('idx_dynamic_field_name', 'dynamic_fields', ['name'])
    op.create_index('idx_dynamic_field_type', 'dynamic_fields', ['field_type'])
    op.create_index('idx_dynamic_field_widget', 'dynamic_fields', ['widget_type'])
    op.create_index('idx_dynamic_field_required', 'dynamic_fields', ['is_required'])
    op.create_index('idx_dynamic_field_unique', 'dynamic_fields', ['is_unique'])
    op.create_index('idx_dynamic_field_indexed', 'dynamic_fields', ['is_indexed'])
    op.create_index('idx_dynamic_field_searchable', 'dynamic_fields', ['is_searchable'])
    op.create_index('idx_dynamic_field_visible', 'dynamic_fields', ['is_visible'])
    op.create_index('idx_dynamic_field_order', 'dynamic_fields', ['display_order'])
    op.create_index('idx_dynamic_field_section', 'dynamic_fields', ['section'])
    op.create_index('idx_dynamic_field_lookup', 'dynamic_fields', ['lookup_entity_id'])
    op.create_index('idx_dynamic_field_created', 'dynamic_fields', ['created_at'])
    op.create_index('idx_dynamic_field_updated', 'dynamic_fields', ['updated_at'])
    op.create_index('idx_dynamic_field_entity_order', 'dynamic_fields', ['entity_id', 'display_order'])
    op.create_index('idx_dynamic_field_entity_section', 'dynamic_fields', ['entity_id', 'section'])
    op.create_index('idx_dynamic_field_entity_visible', 'dynamic_fields', ['entity_id', 'is_visible'])
    
    # Create entity_layouts table
    op.create_table('entity_layouts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_name_greek', sa.String(length=255), nullable=True),
        sa.Column('description_greek', sa.Text(), nullable=True),
        sa.Column('layout_type', layout_type_enum, nullable=False),
        sa.Column('status', layout_status_enum, nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=False),
        sa.Column('is_system_layout', sa.Boolean(), nullable=False),
        sa.Column('is_responsive', sa.Boolean(), nullable=False),
        sa.Column('grid_columns', sa.Integer(), nullable=False),
        sa.Column('grid_gap', sa.String(length=20), nullable=True),
        sa.Column('max_width', sa.String(length=20), nullable=True),
        sa.Column('form_sections', sa.JSON(), nullable=True),
        sa.Column('form_validation', sa.JSON(), nullable=True),
        sa.Column('submit_behavior', sa.JSON(), nullable=True),
        sa.Column('list_columns', sa.JSON(), nullable=True),
        sa.Column('list_filters', sa.JSON(), nullable=True),
        sa.Column('list_sorting', sa.JSON(), nullable=True),
        sa.Column('list_pagination', sa.JSON(), nullable=True),
        sa.Column('list_actions', sa.JSON(), nullable=True),
        sa.Column('detail_sections', sa.JSON(), nullable=True),
        sa.Column('detail_tabs', sa.JSON(), nullable=True),
        sa.Column('related_entities', sa.JSON(), nullable=True),
        sa.Column('search_fields', sa.JSON(), nullable=True),
        sa.Column('search_filters', sa.JSON(), nullable=True),
        sa.Column('search_sorting', sa.JSON(), nullable=True),
        sa.Column('dashboard_widgets', sa.JSON(), nullable=True),
        sa.Column('dashboard_filters', sa.JSON(), nullable=True),
        sa.Column('dashboard_refresh', sa.Integer(), nullable=True),
        sa.Column('responsive_config', sa.JSON(), nullable=True),
        sa.Column('mobile_optimizations', sa.JSON(), nullable=True),
        sa.Column('theme', sa.String(length=50), nullable=True),
        sa.Column('color_scheme', sa.String(length=50), nullable=True),
        sa.Column('custom_css', sa.Text(), nullable=True),
        sa.Column('css_classes', sa.String(length=500), nullable=True),
        sa.Column('greek_layout_features', sa.JSON(), nullable=True),
        sa.Column('rtl_support', sa.Boolean(), nullable=False),
        sa.Column('greek_formatting', sa.JSON(), nullable=True),
        sa.Column('visibility_rules', sa.JSON(), nullable=True),
        sa.Column('permission_rules', sa.JSON(), nullable=True),
        sa.Column('loading_states', sa.JSON(), nullable=True),
        sa.Column('error_handling', sa.JSON(), nullable=True),
        sa.Column('tooltips_enabled', sa.Boolean(), nullable=False),
        sa.Column('animations_enabled', sa.Boolean(), nullable=False),
        sa.Column('lazy_loading', sa.Boolean(), nullable=False),
        sa.Column('virtual_scrolling', sa.Boolean(), nullable=False),
        sa.Column('cache_strategy', sa.String(length=50), nullable=True),
        sa.Column('parent_layout_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('template_id', sa.String(length=100), nullable=True),
        sa.Column('custom_properties', sa.JSON(), nullable=True),
        sa.Column('header_config', sa.JSON(), nullable=True),
        sa.Column('footer_config', sa.JSON(), nullable=True),
        sa.Column('breadcrumb_config', sa.JSON(), nullable=True),
        sa.Column('primary_actions', sa.JSON(), nullable=True),
        sa.Column('secondary_actions', sa.JSON(), nullable=True),
        sa.Column('context_menu', sa.JSON(), nullable=True),
        sa.Column('export_formats', sa.JSON(), nullable=True),
        sa.Column('print_layout', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['entity_id'], ['dynamic_entities.id'], ),
        sa.ForeignKeyConstraint(['parent_layout_id'], ['entity_layouts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for entity_layouts
    op.create_index('idx_entity_layout_entity', 'entity_layouts', ['entity_id'])
    op.create_index('idx_entity_layout_name', 'entity_layouts', ['name'])
    op.create_index('idx_entity_layout_type', 'entity_layouts', ['layout_type'])
    op.create_index('idx_entity_layout_status', 'entity_layouts', ['status'])
    op.create_index('idx_entity_layout_default', 'entity_layouts', ['is_default'])
    op.create_index('idx_entity_layout_system', 'entity_layouts', ['is_system_layout'])
    op.create_index('idx_entity_layout_parent', 'entity_layouts', ['parent_layout_id'])
    op.create_index('idx_entity_layout_template', 'entity_layouts', ['template_id'])
    op.create_index('idx_entity_layout_created', 'entity_layouts', ['created_at'])
    op.create_index('idx_entity_layout_updated', 'entity_layouts', ['updated_at'])
    op.create_index('idx_entity_layout_entity_type', 'entity_layouts', ['entity_id', 'layout_type'])
    op.create_index('idx_entity_layout_entity_default', 'entity_layouts', ['entity_id', 'is_default'])
    op.create_index('idx_entity_layout_entity_status', 'entity_layouts', ['entity_id', 'status'])


def downgrade():
    """Drop Dynamic Entities System tables and enums"""
    
    # Drop indexes
    op.drop_index('idx_entity_layout_entity_status', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_entity_default', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_entity_type', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_updated', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_created', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_template', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_parent', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_system', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_default', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_status', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_type', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_name', table_name='entity_layouts')
    op.drop_index('idx_entity_layout_entity', table_name='entity_layouts')
    
    op.drop_index('idx_dynamic_field_entity_visible', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_entity_section', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_entity_order', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_updated', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_created', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_lookup', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_section', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_order', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_visible', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_searchable', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_indexed', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_unique', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_required', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_widget', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_type', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_name', table_name='dynamic_fields')
    op.drop_index('idx_dynamic_field_entity', table_name='dynamic_fields')
    
    op.drop_index('idx_dynamic_entity_updated', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_created', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_system', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_parent', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_table_name', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_api_name', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_scope', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_status', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_name', table_name='dynamic_entities')
    op.drop_index('idx_dynamic_entity_company', table_name='dynamic_entities')
    
    # Drop tables
    op.drop_table('entity_layouts')
    op.drop_table('dynamic_fields')
    op.drop_table('dynamic_entities')
    
    # Drop enums
    responsive_breakpoint_enum = postgresql.ENUM(name='responsivebreakpoint')
    responsive_breakpoint_enum.drop(op.get_bind())
    
    layout_status_enum = postgresql.ENUM(name='layoutstatus')
    layout_status_enum.drop(op.get_bind())
    
    layout_type_enum = postgresql.ENUM(name='layouttype')
    layout_type_enum.drop(op.get_bind())
    
    field_widget_type_enum = postgresql.ENUM(name='fieldwidgettype')
    field_widget_type_enum.drop(op.get_bind())
    
    field_type_enum = postgresql.ENUM(name='fieldtype')
    field_type_enum.drop(op.get_bind())
    
    entity_status_enum = postgresql.ENUM(name='entitystatus')
    entity_status_enum.drop(op.get_bind())
    
    entity_scope_enum = postgresql.ENUM(name='entityscope')
    entity_scope_enum.drop(op.get_bind()) 