-- Greek ERP/CRM Database Initialization Script
-- Creates database tables, indexes, and initial data
-- Compatible with PostgreSQL 12+ and Greek business requirements

-- Set client encoding to UTF-8 for Greek characters
SET CLIENT_ENCODING TO 'UTF8';
SET TIMEZONE TO 'Europe/Athens';

-- Create extensions if they don't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Company Management Tables
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    afm VARCHAR(9) UNIQUE NOT NULL,
    doy VARCHAR(10) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    vat_number VARCHAR(20),
    legal_form VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT chk_afm_format CHECK (afm ~ '^[0-9]{9}$'),
    CONSTRAINT chk_email_format CHECK (email ~ '^[^@]+@[^@]+\.[^@]+$')
);

-- Users Table with Company Isolation
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT chk_email_format CHECK (email ~ '^[^@]+@[^@]+\.[^@]+$'),
    CONSTRAINT chk_role_valid CHECK (role IN ('admin', 'manager', 'user', 'accountant', 'sales'))
);

-- Roles and Permissions
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, role_id)
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT chk_action_valid CHECK (action IN ('CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT'))
);

-- Customer Management Tables
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    customer_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    afm VARCHAR(9),
    doy VARCHAR(10),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(10),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    vat_number VARCHAR(20),
    payment_terms INTEGER DEFAULT 30,
    credit_limit DECIMAL(15,2) DEFAULT 0.00,
    customer_type VARCHAR(50) DEFAULT 'individual',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT chk_afm_format CHECK (afm IS NULL OR afm ~ '^[0-9]{9}$'),
    CONSTRAINT chk_email_format CHECK (email IS NULL OR email ~ '^[^@]+@[^@]+\.[^@]+$'),
    CONSTRAINT chk_customer_type CHECK (customer_type IN ('individual', 'business', 'government'))
);

-- Product/Service Management
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    unit_of_measure VARCHAR(20) DEFAULT 'piece',
    price DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    cost DECIMAL(15,2) DEFAULT 0.00,
    vat_rate DECIMAL(5,4) DEFAULT 0.24,
    stock_quantity INTEGER DEFAULT 0,
    min_stock_level INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_service BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT chk_vat_rate_valid CHECK (vat_rate >= 0 AND vat_rate <= 1)
);

-- Invoice Management
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    customer_id UUID NOT NULL REFERENCES customers(id),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE,
    series VARCHAR(10) DEFAULT 'A',
    aa INTEGER NOT NULL,
    subtotal DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    vat_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'draft',
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    notes TEXT,
    aade_mark VARCHAR(100),
    aade_uid VARCHAR(100),
    aade_auth_code VARCHAR(100),
    aade_qr_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT chk_amounts_positive CHECK (subtotal >= 0 AND vat_amount >= 0 AND total_amount >= 0),
    CONSTRAINT chk_status_valid CHECK (status IN ('draft', 'sent', 'paid', 'cancelled')),
    CONSTRAINT chk_payment_status_valid CHECK (payment_status IN ('unpaid', 'partial', 'paid', 'overdue'))
);

-- Invoice Line Items
CREATE TABLE IF NOT EXISTS invoice_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    description VARCHAR(500) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL DEFAULT 1,
    unit_price DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    discount_percent DECIMAL(5,2) DEFAULT 0.00,
    vat_rate DECIMAL(5,4) NOT NULL DEFAULT 0.24,
    line_total DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    vat_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    
    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_unit_price_positive CHECK (unit_price >= 0),
    CONSTRAINT chk_discount_valid CHECK (discount_percent >= 0 AND discount_percent <= 100)
);

-- Greek Tax Configuration
CREATE TABLE IF NOT EXISTS greek_tax_config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    config_key VARCHAR(50) NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(company_id, config_key)
);

-- AADE Integration Log
CREATE TABLE IF NOT EXISTS aade_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    submission_type VARCHAR(50) NOT NULL,
    request_data JSONB,
    response_data JSONB,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT chk_submission_type CHECK (submission_type IN ('invoice', 'payment', 'cancellation')),
    CONSTRAINT chk_status_valid CHECK (status IN ('pending', 'success', 'failed', 'retry'))
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_companies_afm ON companies(afm);
CREATE INDEX IF NOT EXISTS idx_users_company_id ON users(company_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_audit_logs_company_id ON audit_logs(company_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_customers_company_id ON customers(company_id);
CREATE INDEX IF NOT EXISTS idx_customers_afm ON customers(afm);
CREATE INDEX IF NOT EXISTS idx_customers_customer_code ON customers(customer_code);
CREATE INDEX IF NOT EXISTS idx_products_company_id ON products(company_id);
CREATE INDEX IF NOT EXISTS idx_products_code ON products(code);
CREATE INDEX IF NOT EXISTS idx_invoices_company_id ON invoices(company_id);
CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_date ON invoices(invoice_date);
CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id);
CREATE INDEX IF NOT EXISTS idx_invoice_items_product_id ON invoice_items(product_id);
CREATE INDEX IF NOT EXISTS idx_greek_tax_config_company_id ON greek_tax_config(company_id);
CREATE INDEX IF NOT EXISTS idx_aade_submissions_company_id ON aade_submissions(company_id);
CREATE INDEX IF NOT EXISTS idx_aade_submissions_invoice_id ON aade_submissions(invoice_id);

-- Insert Default Roles
INSERT INTO roles (name, description, permissions) VALUES
    ('admin', 'System Administrator', '["admin:*"]'),
    ('manager', 'Company Manager', '["customers:*", "products:*", "invoices:*", "reports:view"]'),
    ('accountant', 'Accountant', '["invoices:*", "customers:view", "products:view", "reports:view"]'),
    ('sales', 'Sales Representative', '["customers:*", "invoices:create", "invoices:update", "products:view"]'),
    ('user', 'Regular User', '["customers:view", "products:view", "invoices:view"]')
ON CONFLICT (name) DO NOTHING;

-- Insert Default Greek Tax Configuration
INSERT INTO greek_tax_config (company_id, config_key, config_value, description) 
SELECT 
    c.id,
    'DEFAULT_VAT_RATE',
    '0.24',
    'Default Greek VAT rate (24%)'
FROM companies c
WHERE NOT EXISTS (
    SELECT 1 FROM greek_tax_config 
    WHERE company_id = c.id AND config_key = 'DEFAULT_VAT_RATE'
);

INSERT INTO greek_tax_config (company_id, config_key, config_value, description) 
SELECT 
    c.id,
    'REDUCED_VAT_RATE_1',
    '0.13',
    'Reduced Greek VAT rate 1 (13%)'
FROM companies c
WHERE NOT EXISTS (
    SELECT 1 FROM greek_tax_config 
    WHERE company_id = c.id AND config_key = 'REDUCED_VAT_RATE_1'
);

INSERT INTO greek_tax_config (company_id, config_key, config_value, description) 
SELECT 
    c.id,
    'REDUCED_VAT_RATE_2',
    '0.06',
    'Reduced Greek VAT rate 2 (6%)'
FROM companies c
WHERE NOT EXISTS (
    SELECT 1 FROM greek_tax_config 
    WHERE company_id = c.id AND config_key = 'REDUCED_VAT_RATE_2'
);

INSERT INTO greek_tax_config (company_id, config_key, config_value, description) 
SELECT 
    c.id,
    'ZERO_VAT_RATE',
    '0.00',
    'Zero Greek VAT rate (0%)'
FROM companies c
WHERE NOT EXISTS (
    SELECT 1 FROM greek_tax_config 
    WHERE company_id = c.id AND config_key = 'ZERO_VAT_RATE'
);

-- Create Functions for Common Operations

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_greek_tax_config_updated_at BEFORE UPDATE ON greek_tax_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to generate invoice number
CREATE OR REPLACE FUNCTION generate_invoice_number(company_uuid UUID, series_name VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    next_aa INTEGER;
    invoice_num VARCHAR;
BEGIN
    -- Get next AA (sequential number) for this company and series
    SELECT COALESCE(MAX(aa), 0) + 1 
    INTO next_aa 
    FROM invoices 
    WHERE company_id = company_uuid 
    AND series = series_name 
    AND EXTRACT(YEAR FROM invoice_date) = EXTRACT(YEAR FROM CURRENT_DATE);
    
    -- Generate invoice number: SERIES-YYYY-AA
    invoice_num := series_name || '-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-' || LPAD(next_aa::TEXT, 6, '0');
    
    RETURN invoice_num;
END;
$$ LANGUAGE plpgsql;

-- Function to validate Greek AFM
CREATE OR REPLACE FUNCTION validate_greek_afm(afm_input VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    afm_digits INTEGER[];
    sum_value INTEGER := 0;
    checksum INTEGER;
    i INTEGER;
BEGIN
    -- Check if AFM is exactly 9 digits
    IF afm_input IS NULL OR LENGTH(afm_input) != 9 OR afm_input !~ '^[0-9]{9}$' THEN
        RETURN FALSE;
    END IF;
    
    -- Convert to array of digits
    FOR i IN 1..9 LOOP
        afm_digits[i] := CAST(SUBSTR(afm_input, i, 1) AS INTEGER);
    END LOOP;
    
    -- Calculate checksum
    FOR i IN 1..8 LOOP
        sum_value := sum_value + afm_digits[i] * POWER(2, 9-i);
    END LOOP;
    
    checksum := sum_value % 11;
    
    -- Handle special case
    IF checksum = 10 THEN
        checksum := 0;
    END IF;
    
    -- Validate checksum
    RETURN checksum = afm_digits[9];
END;
$$ LANGUAGE plpgsql;

-- Final Success Message
DO $$
BEGIN
    RAISE NOTICE 'Greek ERP/CRM Database initialized successfully!';
    RAISE NOTICE 'Database includes:';
    RAISE NOTICE '- Company management with AFM validation';
    RAISE NOTICE '- User management with role-based permissions';
    RAISE NOTICE '- Customer and product management';
    RAISE NOTICE '- Invoice management with Greek tax compliance';
    RAISE NOTICE '- AADE integration logging';
    RAISE NOTICE '- Comprehensive audit trail';
    RAISE NOTICE '- Greek locale support';
END $$; 