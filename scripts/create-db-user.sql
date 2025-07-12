-- Greek ERP/CRM Database and User Creation
-- Run this file as postgres user

-- Create database with Greek locale
CREATE DATABASE erp_maritime_hellenic_4007 
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'Greek_Greece.1252'
    LC_CTYPE = 'Greek_Greece.1252'
    TEMPLATE = template0;

-- Create user (drop if exists first)
DROP USER IF EXISTS erp_admin_315;
CREATE USER erp_admin_315 WITH PASSWORD '';

-- Grant database creation privilege
ALTER USER erp_admin_315 CREATEDB;

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON DATABASE erp_maritime_hellenic_4007 TO erp_admin_315;

-- Make user owner of the database
ALTER DATABASE erp_maritime_hellenic_4007 OWNER TO erp_admin_315;

-- Connect to the database to set schema permissions
\c erp_maritime_hellenic_4007;

-- Grant all privileges on schema public
GRANT ALL ON SCHEMA public TO erp_admin_315;

-- Grant create privilege  
GRANT CREATE ON SCHEMA public TO erp_admin_315;

-- Grant usage privilege
GRANT USAGE ON SCHEMA public TO erp_admin_315;

-- Show confirmation
SELECT 'Database, user, and permissions configured successfully!' AS status; 