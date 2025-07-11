-- Greek ERP/CRM Database Setup Script
-- Creates master database and company-specific database templates

-- ==============================================
-- MASTER DATABASE SETUP
-- ==============================================

-- Create master database (run as superuser)
-- CREATE DATABASE greek_erp_master 
--   WITH ENCODING 'UTF8' 
--   LC_COLLATE = 'el_GR.UTF-8' 
--   LC_CTYPE = 'el_GR.UTF-8' 
--   TEMPLATE = template0;

-- Connect to master database
\c greek_erp_master;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone to Athens
SET timezone = 'Europe/Athens';

-- ==============================================
-- MASTER DATABASE TABLES
-- ==============================================

-- Companies table (master tenant registry)
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    afm VARCHAR(9) UNIQUE NOT NULL, -- Greek tax number
    doy VARCHAR(10) NOT NULL, -- Greek tax office
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(10),
    country VARCHAR(2) DEFAULT 'GR',
    
    -- Database connection info
    database_name VARCHAR(100) UNIQUE NOT NULL,
    database_url TEXT,
    
    -- Subscription info
    subscription_plan VARCHAR(50) DEFAULT 'basic',
    subscription_status VARCHAR(20) DEFAULT 'active',
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Greek business settings
    vat_rate DECIMAL(5,4) DEFAULT 0.24,
    currency VARCHAR(3) DEFAULT 'EUR',
    locale VARCHAR(10) DEFAULT 'el_GR',
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    updated_by UUID
);

-- Users table (master user registry)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    
    -- Account status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    is_superuser BOOLEAN DEFAULT false,
    
    -- Greek localization
    preferred_language VARCHAR(5) DEFAULT 'el',
    timezone VARCHAR(50) DEFAULT 'Europe/Athens',
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- Security
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE
);

-- Company users association (many-to-many)
CREATE TABLE IF NOT EXISTS company_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    
    -- Permissions
    permissions JSONB DEFAULT '{}',
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(company_id, user_id)
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Action details
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    
    -- Request context
    ip_address INET,
    user_agent TEXT,
    request_id UUID,
    
    -- Data
    old_data JSONB,
    new_data JSONB,
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- INDEXES FOR PERFORMANCE
-- ==============================================

-- Companies
CREATE INDEX IF NOT EXISTS idx_companies_afm ON companies(afm);
CREATE INDEX IF NOT EXISTS idx_companies_email ON companies(email);
CREATE INDEX IF NOT EXISTS idx_companies_subscription_status ON companies(subscription_status);

-- Users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Company users
CREATE INDEX IF NOT EXISTS idx_company_users_company_id ON company_users(company_id);
CREATE INDEX IF NOT EXISTS idx_company_users_user_id ON company_users(user_id);
CREATE INDEX IF NOT EXISTS idx_company_users_role ON company_users(role);

-- Audit logs
CREATE INDEX IF NOT EXISTS idx_audit_logs_company_id ON audit_logs(company_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- ==============================================
-- TRIGGERS FOR UPDATED_AT
-- ==============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- ==============================================
-- SAMPLE DATA (DEVELOPMENT ONLY)
-- ==============================================

-- Insert sample company (uncomment for development)
-- INSERT INTO companies (name, afm, doy, email, database_name) VALUES
-- ('Sample Greek Company Ltd', '9', 'A1234', 'info@samplecompany.gr', 'erp_company_sample')
-- ON CONFLICT (afm) DO NOTHING;

-- Insert sample user (uncomment for development)
-- INSERT INTO users (email, password_hash, first_name, last_name) VALUES
-- ('admin@samplecompany.gr', '$2b$12$sample.hash', 'Γιάννης', 'Παπαδόπουλος')
-- ON CONFLICT (email) DO NOTHING;

COMMIT; 