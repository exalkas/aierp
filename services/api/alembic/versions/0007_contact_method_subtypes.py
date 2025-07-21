"""Contact method subtypes migration

Revision ID: 0007
Revises: 0006
Create Date: 2025-01-19 23:30:00.000000

Adds configurable contact method subtypes table and migrates existing enum data
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0007_contact_method_subtypes'
down_revision = '0006_dynamic_entities_system'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade to configurable contact method subtypes"""
    
    # Create contact_method_subtypes table
    op.create_table('contact_method_subtypes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('method_type', sa.Enum('PHONE', 'MOBILE', 'EMAIL', 'ADDRESS', 'FAX', 'WEBSITE', 'SOCIAL_MEDIA', name='contactmethodtype'), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('name_greek', sa.String(length=100)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('description_greek', sa.String(length=255)),
        sa.Column('icon', sa.String(length=50)),
        sa.Column('color', sa.String(length=7)),
        sa.Column('is_system', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, default=False),
        sa.Column('display_order', sa.Integer(), default=0),
        sa.Column('usage_count', sa.Integer(), default=0),
        sa.Column('last_used', sa.DateTime()),
        sa.Column('validation_rules', sa.JSON(), default={}),
        sa.Column('format_template', sa.String(length=255)),
        sa.Column('auto_suggestions', sa.JSON(), default=[]),
        sa.Column('requires_verification', sa.Boolean(), default=False),
        sa.Column('allows_marketing', sa.Boolean(), default=True),
        sa.Column('business_hours_only', sa.Boolean(), default=False),
        sa.Column('greek_compliance_required', sa.Boolean(), default=False),
        sa.Column('aade_field_mapping', sa.String(length=100)),
        sa.Column('custom_properties', sa.JSON(), default={}),
        sa.Column('tags', sa.JSON(), default=[]),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True))
    )
    
    # Create indexes
    op.create_index('idx_contact_method_subtype_company', 'contact_method_subtypes', ['company_id'])
    op.create_index('idx_contact_method_subtype_type', 'contact_method_subtypes', ['method_type'])
    op.create_index('idx_contact_method_subtype_code', 'contact_method_subtypes', ['code'])
    op.create_index('idx_contact_method_subtype_active', 'contact_method_subtypes', ['is_active'])
    op.create_index('idx_contact_method_subtype_system', 'contact_method_subtypes', ['is_system'])
    op.create_index('idx_contact_method_subtype_default', 'contact_method_subtypes', ['is_default'])
    op.create_index('idx_contact_method_subtype_order', 'contact_method_subtypes', ['display_order'])
    op.create_index('idx_contact_method_subtype_company_type', 'contact_method_subtypes', ['company_id', 'method_type'])
    op.create_index('idx_contact_method_subtype_company_code', 'contact_method_subtypes', ['company_id', 'code'])
    op.create_index('idx_contact_method_subtype_type_active', 'contact_method_subtypes', ['method_type', 'is_active'])
    op.create_index('idx_contact_method_subtype_unique', 'contact_method_subtypes', ['company_id', 'method_type', 'code'], unique=True)
    
    # Create system default subtypes for all companies
    # This will be populated by the application on first run for each company
    
    # Add subtype_id column to contact_methods table
    op.add_column('contact_methods', sa.Column('subtype_id', postgresql.UUID(as_uuid=True)))
    
    # Create index for the new foreign key
    op.create_index('idx_contact_method_subtype_fk', 'contact_methods', ['subtype_id'])
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_contact_method_subtype', 
        'contact_methods', 
        'contact_method_subtypes',
        ['subtype_id'], 
        ['id']
    )
    
    # Note: Data migration will be handled by the application
    # The application will:
    # 1. Create system default subtypes for each company
    # 2. Map existing method_subtype enum values to new subtypes
    # 3. Populate subtype_id for existing contact methods
    # 4. Drop the old method_subtype column once migration is complete
    
    print("✅ Created contact_method_subtypes table and added subtype_id to contact_methods")
    print("⚠️  Run the data migration script to populate subtypes and migrate existing data")


def downgrade() -> None:
    """Downgrade from configurable contact method subtypes"""
    
    # Remove foreign key constraint
    op.drop_constraint('fk_contact_method_subtype', 'contact_methods', type_='foreignkey')
    
    # Remove index
    op.drop_index('idx_contact_method_subtype_fk', table_name='contact_methods')
    
    # Remove subtype_id column
    op.drop_column('contact_methods', 'subtype_id')
    
    # Drop contact_method_subtypes table
    op.drop_table('contact_method_subtypes')
    
    # Recreate the old enum column if needed
    # Note: This would require manual data recovery
    print("⚠️  Downgraded to enum-based subtypes. Manual data recovery may be required.") 