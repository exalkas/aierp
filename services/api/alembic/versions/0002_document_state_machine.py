"""Add document state machine models

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-01 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create state transition rules table
    op.create_table('state_transition_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_type', sa.String(length=30), nullable=False),
        sa.Column('from_state', sa.String(length=50), nullable=False),
        sa.Column('to_state', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('is_automatic', sa.Boolean(), nullable=True, default=False),
        sa.Column('conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('required_role', sa.String(length=50), nullable=True),
        sa.Column('greek_business_rules', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('aade_requirements', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('validation_rules', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'document_type', 'from_state', 'action')
    )
    
    # Create document workflow instances table
    op.create_table('document_workflow_instances',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_type', sa.String(length=30), nullable=False),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('current_state', sa.String(length=50), nullable=False),
        sa.Column('workflow_template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('context_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'document_type', 'document_id')
    )
    
    # Create document state history table
    op.create_table('document_state_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('workflow_instance_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('from_state', sa.String(length=50), nullable=True),
        sa.Column('to_state', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False, default=sa.text('NOW()')),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('was_automatic', sa.Boolean(), nullable=True, default=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workflow_instance_id'], ['document_workflow_instances.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create document automation rules table
    op.create_table('document_automation_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('document_type', sa.String(length=30), nullable=False),
        sa.Column('trigger_state', sa.String(length=50), nullable=False),
        sa.Column('target_action', sa.String(length=50), nullable=False),
        sa.Column('conditions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('delay_minutes', sa.Integer(), nullable=True, default=0),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create Greek document workflow templates table
    op.create_table('greek_document_workflow_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('document_type', sa.String(length=30), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('initial_state', sa.String(length=50), nullable=False),
        sa.Column('final_states', postgresql.ARRAY(sa.String(length=50)), nullable=False),
        sa.Column('state_config', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('action_config', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('greek_legal_refs', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('aade_mydata_mapping', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'document_type', 'name')
    )
    
    # Add workflow_instance_id to invoices table
    op.add_column('invoices', sa.Column('workflow_instance_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_invoices_workflow_instance', 'invoices', 'document_workflow_instances', ['workflow_instance_id'], ['id'], ondelete='SET NULL')
    
    # Create indexes
    op.create_index('idx_state_transition_rules_company_id', 'state_transition_rules', ['company_id'])
    op.create_index('idx_state_transition_rules_document_type', 'state_transition_rules', ['document_type'])
    op.create_index('idx_state_transition_rules_from_state', 'state_transition_rules', ['from_state'])
    op.create_index('idx_state_transition_rules_action', 'state_transition_rules', ['action'])
    
    op.create_index('idx_document_workflow_instances_company_id', 'document_workflow_instances', ['company_id'])
    op.create_index('idx_document_workflow_instances_document_type', 'document_workflow_instances', ['document_type'])
    op.create_index('idx_document_workflow_instances_document_id', 'document_workflow_instances', ['document_id'])
    op.create_index('idx_document_workflow_instances_current_state', 'document_workflow_instances', ['current_state'])
    
    op.create_index('idx_document_state_history_company_id', 'document_state_history', ['company_id'])
    op.create_index('idx_document_state_history_workflow_instance_id', 'document_state_history', ['workflow_instance_id'])
    op.create_index('idx_document_state_history_timestamp', 'document_state_history', ['timestamp'])
    op.create_index('idx_document_state_history_action', 'document_state_history', ['action'])
    
    op.create_index('idx_document_automation_rules_company_id', 'document_automation_rules', ['company_id'])
    op.create_index('idx_document_automation_rules_document_type', 'document_automation_rules', ['document_type'])
    op.create_index('idx_document_automation_rules_trigger_state', 'document_automation_rules', ['trigger_state'])
    
    op.create_index('idx_greek_document_workflow_templates_company_id', 'greek_document_workflow_templates', ['company_id'])
    op.create_index('idx_greek_document_workflow_templates_document_type', 'greek_document_workflow_templates', ['document_type'])
    op.create_index('idx_greek_document_workflow_templates_is_default', 'greek_document_workflow_templates', ['is_default'])
    
    op.create_index('idx_invoices_workflow_instance_id', 'invoices', ['workflow_instance_id'])
    
    # Create triggers for updated_at columns
    op.execute("CREATE TRIGGER update_state_transition_rules_updated_at BEFORE UPDATE ON state_transition_rules FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_document_workflow_instances_updated_at BEFORE UPDATE ON document_workflow_instances FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_document_automation_rules_updated_at BEFORE UPDATE ON document_automation_rules FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_greek_document_workflow_templates_updated_at BEFORE UPDATE ON greek_document_workflow_templates FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_greek_document_workflow_templates_updated_at ON greek_document_workflow_templates;")
    op.execute("DROP TRIGGER IF EXISTS update_document_automation_rules_updated_at ON document_automation_rules;")
    op.execute("DROP TRIGGER IF EXISTS update_document_workflow_instances_updated_at ON document_workflow_instances;")
    op.execute("DROP TRIGGER IF EXISTS update_state_transition_rules_updated_at ON state_transition_rules;")
    
    # Drop indexes
    op.drop_index('idx_invoices_workflow_instance_id', 'invoices')
    
    op.drop_index('idx_greek_document_workflow_templates_is_default', 'greek_document_workflow_templates')
    op.drop_index('idx_greek_document_workflow_templates_document_type', 'greek_document_workflow_templates')
    op.drop_index('idx_greek_document_workflow_templates_company_id', 'greek_document_workflow_templates')
    
    op.drop_index('idx_document_automation_rules_trigger_state', 'document_automation_rules')
    op.drop_index('idx_document_automation_rules_document_type', 'document_automation_rules')
    op.drop_index('idx_document_automation_rules_company_id', 'document_automation_rules')
    
    op.drop_index('idx_document_state_history_action', 'document_state_history')
    op.drop_index('idx_document_state_history_timestamp', 'document_state_history')
    op.drop_index('idx_document_state_history_workflow_instance_id', 'document_state_history')
    op.drop_index('idx_document_state_history_company_id', 'document_state_history')
    
    op.drop_index('idx_document_workflow_instances_current_state', 'document_workflow_instances')
    op.drop_index('idx_document_workflow_instances_document_id', 'document_workflow_instances')
    op.drop_index('idx_document_workflow_instances_document_type', 'document_workflow_instances')
    op.drop_index('idx_document_workflow_instances_company_id', 'document_workflow_instances')
    
    op.drop_index('idx_state_transition_rules_action', 'state_transition_rules')
    op.drop_index('idx_state_transition_rules_from_state', 'state_transition_rules')
    op.drop_index('idx_state_transition_rules_document_type', 'state_transition_rules')
    op.drop_index('idx_state_transition_rules_company_id', 'state_transition_rules')
    
    # Drop foreign key and column from invoices
    op.drop_constraint('fk_invoices_workflow_instance', 'invoices', type_='foreignkey')
    op.drop_column('invoices', 'workflow_instance_id')
    
    # Drop tables
    op.drop_table('greek_document_workflow_templates')
    op.drop_table('document_automation_rules')
    op.drop_table('document_state_history')
    op.drop_table('document_workflow_instances')
    op.drop_table('state_transition_rules') 