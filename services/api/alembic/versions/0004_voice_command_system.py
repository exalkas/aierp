"""Voice Command System

Revision ID: 0004_voice_command_system
Revises: 0003_crm_erp_models
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0004_voice_command_system'
down_revision = '0003_crm_erp_models'
branch_labels = None
depends_on = None


def upgrade():
    # Create voice command enums
    voicecommandtype_enum = sa.Enum('NAVIGATION', 'CREATE', 'SEARCH', 'ACTION', 'MODAL', 'WORKFLOW', 'REPORT', 'HELP', name='voicecommandtype')
    voicecommandtype_enum.create(op.get_bind())
    
    voicecommandstatus_enum = sa.Enum('ACTIVE', 'INACTIVE', 'DEPRECATED', name='voicecommandstatus')
    voicecommandstatus_enum.create(op.get_bind())
    
    voiceactiontype_enum = sa.Enum('NAVIGATE', 'OPEN_MODAL', 'EXECUTE_FUNCTION', 'API_CALL', 'FORM_FILL', 'WORKFLOW', name='voiceactiontype')
    voiceactiontype_enum.create(op.get_bind())
    
    # Create system_voice_commands table
    op.create_table('system_voice_commands',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('command_key', sa.String(length=100), nullable=False),
        sa.Column('command_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('command_type', voicecommandtype_enum, nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('module', sa.String(length=100), nullable=True),
        sa.Column('default_phrases', sa.JSON(), nullable=False),
        sa.Column('action_type', voiceactiontype_enum, nullable=False),
        sa.Column('action_config', sa.JSON(), nullable=False),
        sa.Column('required_params', sa.JSON(), nullable=True),
        sa.Column('optional_params', sa.JSON(), nullable=True),
        sa.Column('required_permissions', sa.JSON(), nullable=True),
        sa.Column('min_user_role', sa.String(length=50), nullable=True),
        sa.Column('status', voicecommandstatus_enum, nullable=False),
        sa.Column('is_customizable', sa.Boolean(), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('greek_variants', sa.JSON(), nullable=True),
        sa.Column('phonetic_spelling', sa.JSON(), nullable=True),
        sa.Column('help_text', sa.Text(), nullable=True),
        sa.Column('examples', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('command_key')
    )
    
    # Create indexes for system_voice_commands
    op.create_index('idx_system_voice_command_key', 'system_voice_commands', ['command_key'])
    op.create_index('idx_system_voice_command_type', 'system_voice_commands', ['command_type'])
    op.create_index('idx_system_voice_command_category', 'system_voice_commands', ['category'])
    op.create_index('idx_system_voice_command_module', 'system_voice_commands', ['module'])
    op.create_index('idx_system_voice_command_status', 'system_voice_commands', ['status'])
    op.create_index('idx_system_voice_command_priority', 'system_voice_commands', ['priority'])
    
    # Create user_voice_commands table
    op.create_table('user_voice_commands',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('system_command_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('custom_phrases', sa.JSON(), nullable=False),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('use_system_phrases', sa.Boolean(), nullable=True),
        sa.Column('custom_action_type', voiceactiontype_enum, nullable=True),
        sa.Column('custom_action_config', sa.JSON(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.Column('last_used', sa.DateTime(), nullable=True),
        sa.Column('accuracy_score', sa.Integer(), nullable=True),
        sa.Column('confidence_threshold', sa.Integer(), nullable=True),
        sa.Column('confirmation_required', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['system_command_id'], ['system_voice_commands.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for user_voice_commands
    op.create_index('idx_user_voice_command_user', 'user_voice_commands', ['user_id'])
    op.create_index('idx_user_voice_command_company', 'user_voice_commands', ['company_id'])
    op.create_index('idx_user_voice_command_system', 'user_voice_commands', ['system_command_id'])
    op.create_index('idx_user_voice_command_enabled', 'user_voice_commands', ['is_enabled'])
    op.create_index('idx_user_voice_command_usage', 'user_voice_commands', ['usage_count'])
    op.create_index('idx_user_voice_command_unique', 'user_voice_commands', ['user_id', 'system_command_id'], unique=True)
    
    # Create voice_command_logs table
    op.create_table('voice_command_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', sa.String(length=100), nullable=True),
        sa.Column('device_info', sa.JSON(), nullable=True),
        sa.Column('original_text', sa.Text(), nullable=False),
        sa.Column('recognized_text', sa.Text(), nullable=False),
        sa.Column('confidence_score', sa.Integer(), nullable=False),
        sa.Column('language_detected', sa.String(length=10), nullable=True),
        sa.Column('matched_command_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_command_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('match_score', sa.Integer(), nullable=True),
        sa.Column('executed_successfully', sa.Boolean(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('action_performed', sa.String(length=255), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('error_code', sa.String(length=50), nullable=True),
        sa.Column('page_url', sa.String(length=500), nullable=True),
        sa.Column('page_context', sa.JSON(), nullable=True),
        sa.Column('user_feedback', sa.String(length=20), nullable=True),
        sa.Column('user_correction', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['matched_command_id'], ['system_voice_commands.id'], ),
        sa.ForeignKeyConstraint(['user_command_id'], ['user_voice_commands.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for voice_command_logs
    op.create_index('idx_voice_log_user', 'voice_command_logs', ['user_id'])
    op.create_index('idx_voice_log_company', 'voice_command_logs', ['company_id'])
    op.create_index('idx_voice_log_session', 'voice_command_logs', ['session_id'])
    op.create_index('idx_voice_log_command', 'voice_command_logs', ['matched_command_id'])
    op.create_index('idx_voice_log_success', 'voice_command_logs', ['executed_successfully'])
    op.create_index('idx_voice_log_confidence', 'voice_command_logs', ['confidence_score'])
    op.create_index('idx_voice_log_created', 'voice_command_logs', ['created_at'])
    
    # Create voice_command_templates table
    op.create_table('voice_command_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('template_name', sa.String(length=255), nullable=False),
        sa.Column('template_key', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('command_type', voicecommandtype_enum, nullable=False),
        sa.Column('phrase_patterns', sa.JSON(), nullable=False),
        sa.Column('action_template', sa.JSON(), nullable=False),
        sa.Column('variables', sa.JSON(), nullable=True),
        sa.Column('variable_examples', sa.JSON(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.Column('is_popular', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('template_key')
    )
    
    # Create indexes for voice_command_templates
    op.create_index('idx_voice_template_key', 'voice_command_templates', ['template_key'])
    op.create_index('idx_voice_template_category', 'voice_command_templates', ['category'])
    op.create_index('idx_voice_template_type', 'voice_command_templates', ['command_type'])
    op.create_index('idx_voice_template_popular', 'voice_command_templates', ['is_popular'])


def downgrade():
    # Drop tables
    op.drop_table('voice_command_templates')
    op.drop_table('voice_command_logs')
    op.drop_table('user_voice_commands')
    op.drop_table('system_voice_commands')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS voiceactiontype')
    op.execute('DROP TYPE IF EXISTS voicecommandstatus')
    op.execute('DROP TYPE IF EXISTS voicecommandtype') 