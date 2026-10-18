-- psql 15+ reads credentials from environment; never embed values in this file.
\getenv db_name DB_NAME
\getenv db_user DB_USER
\getenv db_password DB_PASSWORD
\set ON_ERROR_STOP on

-- Greek ERP/CRM Database and User Creation
-- Run this file as postgres user

-- Create database with Greek locale
CREATE DATABASE :"db_name"
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'Greek_Greece.1252'
    LC_CTYPE = 'Greek_Greece.1252'
    TEMPLATE = template0;

-- Create user (drop if exists first)
DROP USER IF EXISTS :"db_user";
CREATE USER :"db_user" WITH PASSWORD :'db_password';

-- Grant database creation privilege
ALTER USER :"db_user" CREATEDB;

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON DATABASE :"db_name" TO :"db_user";

-- Make user owner of the database
ALTER DATABASE :"db_name" OWNER TO :"db_user";

-- Connect to the database to set schema permissions
\connect :db_name

-- Grant all privileges on schema public
GRANT ALL ON SCHEMA public TO :"db_user";

-- Grant create privilege  
GRANT CREATE ON SCHEMA public TO :"db_user";

-- Grant usage privilege
GRANT USAGE ON SCHEMA public TO :"db_user";

-- Show confirmation
SELECT 'Database, user, and permissions configured successfully!' AS status; 