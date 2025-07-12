"""Initial Greek ERP/CRM schema setup

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"unaccent\"")
    
    # Set timezone
    op.execute("SET timezone = 'Europe/Athens'")
    
    # Create companies table
    op.create_table('companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('afm', sa.String(length=9), nullable=False),
        sa.Column('doy', sa.String(length=10), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('postal_code', sa.String(length=10), nullable=True),
        sa.Column('country', sa.String(length=2), nullable=True, default='GR'),
        sa.Column('database_name', sa.String(length=100), nullable=False),
        sa.Column('database_url', sa.Text(), nullable=True),
        sa.Column('subscription_plan', sa.String(length=50), nullable=True, default='basic'),
        sa.Column('subscription_status', sa.String(length=20), nullable=True, default='active'),
        sa.Column('subscription_expires_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('vat_rate', sa.Numeric(precision=5, scale=4), nullable=True, default=0.24),
        sa.Column('currency', sa.String(length=3), nullable=True, default='EUR'),
        sa.Column('locale', sa.String(length=10), nullable=True, default='el_GR'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('afm'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('database_name'),
        sa.CheckConstraint("afm ~ '^[0-9]{9}$'", name='chk_afm_format'),
        sa.CheckConstraint("email ~ '^[^@]+@[^@]+\\.[^@]+$'", name='chk_email_format')
    )
    
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=True, default=False),
        sa.Column('preferred_language', sa.String(length=5), nullable=True, default='el'),
        sa.Column('timezone', sa.String(length=50), nullable=True, default='Europe/Athens'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('last_login_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=True, default=0),
        sa.Column('locked_until', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create company_users table
    op.create_table('company_users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, default='user'),
        sa.Column('permissions', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'")),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('joined_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'user_id')
    )
    
    # Create business_entities table
    op.create_table('business_entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(length=20), nullable=False),
        sa.Column('entity_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('afm', sa.String(length=9), nullable=True),
        sa.Column('doy', sa.String(length=10), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('postal_code', sa.String(length=10), nullable=True),
        sa.Column('country', sa.String(length=2), nullable=True, default='GR'),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('mobile', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('vat_number', sa.String(length=20), nullable=True),
        sa.Column('payment_terms', sa.Integer(), nullable=True, default=30),
        sa.Column('credit_limit', sa.Numeric(precision=15, scale=2), nullable=True, default=0.00),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'entity_code'),
        sa.CheckConstraint("entity_type IN ('customer', 'supplier', 'both')", name='chk_entity_type_valid'),
        sa.CheckConstraint("afm IS NULL OR afm ~ '^[0-9]{9}$'", name='chk_afm_format'),
        sa.CheckConstraint("email IS NULL OR email ~ '^[^@]+@[^@]+\\.[^@]+$'", name='chk_email_format')
    )
    
    # Create products table
    op.create_table('products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('unit_of_measure', sa.String(length=20), nullable=True, default='piece'),
        sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=False, default=0.00),
        sa.Column('cost', sa.Numeric(precision=15, scale=2), nullable=True, default=0.00),
        sa.Column('vat_rate', sa.Numeric(precision=5, scale=4), nullable=True, default=0.24),
        sa.Column('stock_quantity', sa.Integer(), nullable=True, default=0),
        sa.Column('min_stock_level', sa.Integer(), nullable=True, default=0),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_service', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'code'),
        sa.CheckConstraint('price >= 0', name='chk_price_positive'),
        sa.CheckConstraint('vat_rate >= 0 AND vat_rate <= 1', name='chk_vat_rate_valid')
    )
    
    # Create product_vat_configs table
    op.create_table('product_vat_configs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_location', sa.String(length=10), nullable=False),
        sa.Column('vat_rate', sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column('vat_exemption_reason', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'customer_location')
    )
    
    # Create invoices table
    op.create_table('invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_type', sa.String(length=30), nullable=False),
        sa.Column('series', sa.String(length=10), nullable=False),
        sa.Column('aa', sa.Integer(), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('subtotal', sa.Numeric(precision=15, scale=2), nullable=False, default=0.00),
        sa.Column('total_vat', sa.Numeric(precision=15, scale=2), nullable=False, default=0.00),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=False, default=0.00),
        sa.Column('currency', sa.String(length=3), nullable=False, default='EUR'),
        sa.Column('exchange_rate', sa.Numeric(precision=10, scale=6), nullable=True, default=1.0),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('aade_mark', sa.String(length=100), nullable=True),
        sa.Column('aade_uid', sa.String(length=100), nullable=True),
        sa.Column('aade_auth_code', sa.String(length=100), nullable=True),
        sa.Column('aade_qr_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['customer_id'], ['business_entities.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'series', 'aa'),
        sa.UniqueConstraint('company_id', 'invoice_number'),
        sa.CheckConstraint('subtotal >= 0 AND total_vat >= 0 AND total_amount >= 0', name='chk_amounts_positive')
    )
    
    # Create contacts table
    op.create_table('contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('mobile', sa.String(length=20), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['business_entity_id'], ['business_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("email IS NULL OR email ~ '^[^@]+@[^@]+\\.[^@]+$'", name='chk_email_format')
    )
    
    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('old_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('new_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_companies_afm', 'companies', ['afm'])
    op.create_index('idx_companies_email', 'companies', ['email'])
    op.create_index('idx_companies_subscription_status', 'companies', ['subscription_status'])
    
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_is_active', 'users', ['is_active'])
    
    op.create_index('idx_company_users_company_id', 'company_users', ['company_id'])
    op.create_index('idx_company_users_user_id', 'company_users', ['user_id'])
    op.create_index('idx_company_users_role', 'company_users', ['role'])
    
    op.create_index('idx_business_entities_company_id', 'business_entities', ['company_id'])
    op.create_index('idx_business_entities_entity_type', 'business_entities', ['entity_type'])
    op.create_index('idx_business_entities_afm', 'business_entities', ['afm'])
    op.create_index('idx_business_entities_entity_code', 'business_entities', ['entity_code'])
    
    op.create_index('idx_products_company_id', 'products', ['company_id'])
    op.create_index('idx_products_code', 'products', ['code'])
    op.create_index('idx_products_is_active', 'products', ['is_active'])
    
    op.create_index('idx_product_vat_configs_company_id', 'product_vat_configs', ['company_id'])
    op.create_index('idx_product_vat_configs_product_id', 'product_vat_configs', ['product_id'])
    
    op.create_index('idx_invoices_company_id', 'invoices', ['company_id'])
    op.create_index('idx_invoices_customer_id', 'invoices', ['customer_id'])
    op.create_index('idx_invoices_document_type', 'invoices', ['document_type'])
    op.create_index('idx_invoices_issue_date', 'invoices', ['issue_date'])
    op.create_index('idx_invoices_invoice_number', 'invoices', ['invoice_number'])
    
    op.create_index('idx_contacts_company_id', 'contacts', ['company_id'])
    op.create_index('idx_contacts_business_entity_id', 'contacts', ['business_entity_id'])
    op.create_index('idx_contacts_is_primary', 'contacts', ['is_primary'])
    
    op.create_index('idx_audit_logs_company_id', 'audit_logs', ['company_id'])
    op.create_index('idx_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_logs_created_at', 'audit_logs', ['created_at'])
    
    # Create update trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Create triggers
    op.execute("CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_business_entities_updated_at BEFORE UPDATE ON business_entities FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_product_vat_configs_updated_at BEFORE UPDATE ON product_vat_configs FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")
    op.execute("CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();")


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_contacts_updated_at ON contacts;")
    op.execute("DROP TRIGGER IF EXISTS update_invoices_updated_at ON invoices;")
    op.execute("DROP TRIGGER IF EXISTS update_product_vat_configs_updated_at ON product_vat_configs;")
    op.execute("DROP TRIGGER IF EXISTS update_products_updated_at ON products;")
    op.execute("DROP TRIGGER IF EXISTS update_business_entities_updated_at ON business_entities;")
    op.execute("DROP TRIGGER IF EXISTS update_users_updated_at ON users;")
    op.execute("DROP TRIGGER IF EXISTS update_companies_updated_at ON companies;")
    
    # Drop function
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop indexes
    op.drop_index('idx_audit_logs_created_at', 'audit_logs')
    op.drop_index('idx_audit_logs_action', 'audit_logs')
    op.drop_index('idx_audit_logs_user_id', 'audit_logs')
    op.drop_index('idx_audit_logs_company_id', 'audit_logs')
    
    op.drop_index('idx_contacts_is_primary', 'contacts')
    op.drop_index('idx_contacts_business_entity_id', 'contacts')
    op.drop_index('idx_contacts_company_id', 'contacts')
    
    op.drop_index('idx_invoices_invoice_number', 'invoices')
    op.drop_index('idx_invoices_issue_date', 'invoices')
    op.drop_index('idx_invoices_document_type', 'invoices')
    op.drop_index('idx_invoices_customer_id', 'invoices')
    op.drop_index('idx_invoices_company_id', 'invoices')
    
    op.drop_index('idx_product_vat_configs_product_id', 'product_vat_configs')
    op.drop_index('idx_product_vat_configs_company_id', 'product_vat_configs')
    
    op.drop_index('idx_products_is_active', 'products')
    op.drop_index('idx_products_code', 'products')
    op.drop_index('idx_products_company_id', 'products')
    
    op.drop_index('idx_business_entities_entity_code', 'business_entities')
    op.drop_index('idx_business_entities_afm', 'business_entities')
    op.drop_index('idx_business_entities_entity_type', 'business_entities')
    op.drop_index('idx_business_entities_company_id', 'business_entities')
    
    op.drop_index('idx_company_users_role', 'company_users')
    op.drop_index('idx_company_users_user_id', 'company_users')
    op.drop_index('idx_company_users_company_id', 'company_users')
    
    op.drop_index('idx_users_is_active', 'users')
    op.drop_index('idx_users_email', 'users')
    
    op.drop_index('idx_companies_subscription_status', 'companies')
    op.drop_index('idx_companies_email', 'companies')
    op.drop_index('idx_companies_afm', 'companies')
    
    # Drop tables
    op.drop_table('audit_logs')
    op.drop_table('contacts')
    op.drop_table('invoices')
    op.drop_table('product_vat_configs')
    op.drop_table('products')
    op.drop_table('business_entities')
    op.drop_table('company_users')
    op.drop_table('users')
    op.drop_table('companies') 