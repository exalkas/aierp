import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} must be set in the environment or ignored .env file")
    return value



#!/usr/bin/env python3
"""
Greek ERP/CRM Superuser Creation Script
Creates a company and superuser account for the Greek ERP/CRM system
"""

import os
import sys
import asyncio
import getpass
import re
from uuid import uuid4
from datetime import datetime
from typing import Optional

# Add the services directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'api'))

try:
    import asyncpg
    from passlib.context import CryptContext
    import psycopg2
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("Please install the required packages:")
    print("pip install asyncpg passlib psycopg2-binary")
    sys.exit(1)

# Configuration
DB_CONFIG = {"dsn": required_env("DATABASE_URL")}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ANSI color codes for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    GRAY = '\033[0;37m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def log_info(message: str):
    print(f"{Colors.BLUE}{message}{Colors.NC}")

def log_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

def log_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")

def log_error(message: str):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def log_gray(message: str):
    print(f"{Colors.GRAY}{message}{Colors.NC}")

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_afm(afm: str) -> bool:
    """Validate Greek AFM (Tax Identification Number)"""
    if not afm or len(afm) != 9 or not afm.isdigit():
        return False
    
    # AFM checksum validation
    digits = [int(d) for d in afm]
    sum_value = sum(digits[i] * (2 ** (8 - i)) for i in range(8))
    checksum = sum_value % 11
    
    if checksum == 10:
        checksum = 0
    
    return checksum == digits[8]

def validate_phone(phone: str) -> bool:
    """Validate Greek phone number format"""
    # Accept Greek phone numbers: +30XXXXXXXXX, 30XXXXXXXXX, or 2XXXXXXXXX
    pattern = r'^(\+30|30|2)[0-9]{9,10}$'
    return re.match(pattern, phone) is not None

async def check_database_connection():
    """Test database connection"""
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        await conn.close()
        return True
    except Exception as e:
        log_error(f"Database connection failed: {e}")
        return False

async def check_database_schema():
    """Check if database schema exists"""
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        
        # Check if companies table exists
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'companies'
            );
        """)
        
        await conn.close()
        return result
    except Exception as e:
        log_error(f"Schema check failed: {e}")
        return False

async def create_company(conn, company_data: dict) -> str:
    """Create a new company"""
    company_id = str(uuid4())
    
    try:
        await conn.execute("""
            INSERT INTO companies (
                id, name, afm, doy, address, city, postal_code, 
                phone, email, website, legal_form, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """, 
        company_id, company_data['name'], company_data['afm'], 
        company_data['doy'], company_data['address'], company_data['city'],
        company_data['postal_code'], company_data['phone'], 
        company_data['email'], company_data['website'], 
        company_data['legal_form'], datetime.now()
        )
        
        log_success(f"Company '{company_data['name']}' created successfully")
        return company_id
        
    except Exception as e:
        log_error(f"Failed to create company: {e}")
        raise

async def create_superuser(conn, company_id: str, user_data: dict) -> str:
    """Create a superuser"""
    user_id = str(uuid4())
    password_hash = pwd_context.hash(user_data['password'])
    
    try:
        await conn.execute("""
            INSERT INTO users (
                id, company_id, username, email, password_hash, 
                first_name, last_name, phone, role, is_active, 
                is_superuser, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """, 
        user_id, company_id, user_data['username'], user_data['email'],
        password_hash, user_data['first_name'], user_data['last_name'],
        user_data['phone'], 'admin', True, True, datetime.now()
        )
        
        log_success(f"Superuser '{user_data['username']}' created successfully")
        return user_id
        
    except Exception as e:
        log_error(f"Failed to create superuser: {e}")
        raise

async def assign_admin_role(conn, user_id: str):
    """Assign admin role to user"""
    try:
        # Get admin role ID
        admin_role_id = await conn.fetchval("""
            SELECT id FROM roles WHERE name = 'admin'
        """)
        
        if not admin_role_id:
            log_error("Admin role not found in database")
            return
        
        # Assign role to user
        await conn.execute("""
            INSERT INTO user_roles (user_id, role_id, assigned_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id, role_id) DO NOTHING
        """, user_id, admin_role_id, datetime.now())
        
        log_success("Admin role assigned to user")
        
    except Exception as e:
        log_error(f"Failed to assign admin role: {e}")
        raise

async def initialize_company_config(conn, company_id: str):
    """Initialize company-specific configuration"""
    try:
        # Greek tax configuration
        tax_configs = [
            ('DEFAULT_VAT_RATE', '0.24', 'Default Greek VAT rate (24%)'),
            ('REDUCED_VAT_RATE_1', '0.13', 'Reduced Greek VAT rate 1 (13%)'),
            ('REDUCED_VAT_RATE_2', '0.06', 'Reduced Greek VAT rate 2 (6%)'),
            ('ZERO_VAT_RATE', '0.00', 'Zero Greek VAT rate (0%)'),
            ('AADE_ENVIRONMENT', 'sandbox', 'AADE environment (sandbox/production)'),
            ('INVOICE_SERIES', 'A', 'Default invoice series'),
            ('CURRENCY', 'EUR', 'Default currency'),
            ('TIMEZONE', 'Europe/Athens', 'Company timezone')
        ]
        
        for config_key, config_value, description in tax_configs:
            await conn.execute("""
                INSERT INTO greek_tax_config (
                    id, company_id, config_key, config_value, description, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (company_id, config_key) DO NOTHING
            """, str(uuid4()), company_id, config_key, config_value, description, datetime.now())
        
        log_success("Company configuration initialized")
        
    except Exception as e:
        log_error(f"Failed to initialize company config: {e}")
        raise

def get_company_input() -> dict:
    """Get company information from user"""
    log_info("Company Information Setup")
    log_info("=" * 30)
    
    company_data = {}
    
    # Company name
    while True:
        company_data['name'] = input("Company Name: ").strip()
        if company_data['name']:
            break
        log_error("Company name is required")
    
    # AFM (Greek Tax Number)
    while True:
        afm = input("AFM (Greek Tax Number - 9 digits): ").strip()
        if validate_afm(afm):
            company_data['afm'] = afm
            break
        log_error("Invalid AFM format. Must be 9 digits with valid checksum")
    
    # DOY (Tax Office)
    while True:
        company_data['doy'] = input("DOY (Tax Office Code): ").strip()
        if company_data['doy']:
            break
        log_error("DOY is required")
    
    # Address
    company_data['address'] = input("Address (optional): ").strip() or None
    company_data['city'] = input("City (optional): ").strip() or None
    company_data['postal_code'] = input("Postal Code (optional): ").strip() or None
    
    # Phone
    while True:
        phone = input("Phone (optional): ").strip()
        if not phone:
            company_data['phone'] = None
            break
        if validate_phone(phone):
            company_data['phone'] = phone
            break
        log_error("Invalid phone format. Use Greek format: +30XXXXXXXXX")
    
    # Email
    while True:
        email = input("Email (optional): ").strip()
        if not email:
            company_data['email'] = None
            break
        if validate_email(email):
            company_data['email'] = email
            break
        log_error("Invalid email format")
    
    # Website
    company_data['website'] = input("Website (optional): ").strip() or None
    
    # Legal form
    legal_forms = ['ΑΕ', 'ΕΠΕ', 'ΟΕ', 'ΕΕ', 'ΙΚΕ', 'Other']
    log_info("Legal Forms: " + ", ".join(f"{i+1}. {form}" for i, form in enumerate(legal_forms)))
    
    while True:
        try:
            choice = input("Select Legal Form (1-6): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 6:
                company_data['legal_form'] = legal_forms[int(choice) - 1]
                break
            log_error("Invalid choice. Please select 1-6")
        except ValueError:
            log_error("Invalid input. Please enter a number")
    
    return company_data

def get_user_input() -> dict:
    """Get superuser information from user"""
    print()
    log_info("Superuser Account Setup")
    log_info("=" * 30)
    
    user_data = {}
    
    # Username
    while True:
        user_data['username'] = input("Username: ").strip()
        if user_data['username'] and len(user_data['username']) >= 3:
            break
        log_error("Username is required and must be at least 3 characters")
    
    # Email
    while True:
        email = input("Email: ").strip()
        if validate_email(email):
            user_data['email'] = email
            break
        log_error("Invalid email format")
    
    # Password
    while True:
        password = getpass.getpass("Password (min 8 characters): ")
        if len(password) >= 8:
            confirm_password = getpass.getpass("Confirm Password: ")
            if password == confirm_password:
                user_data['password'] = password
                break
            log_error("Passwords don't match")
        else:
            log_error("Password must be at least 8 characters")
    
    # First name
    user_data['first_name'] = input("First Name: ").strip()
    
    # Last name
    user_data['last_name'] = input("Last Name: ").strip()
    
    # Phone
    while True:
        phone = input("Phone (optional): ").strip()
        if not phone:
            user_data['phone'] = None
            break
        if validate_phone(phone):
            user_data['phone'] = phone
            break
        log_error("Invalid phone format. Use Greek format: +30XXXXXXXXX")
    
    return user_data

async def main():
    """Main execution function"""
    print(f"{Colors.BOLD}Greek ERP/CRM Superuser Creation{Colors.NC}")
    print("=" * 40)
    print()
    
    # Check database connection
    log_info("Checking database connection...")
    if not await check_database_connection():
        log_error("Cannot connect to database. Please ensure:")
        log_gray("1. PostgreSQL is running")
        log_gray("2. Database 'greek_erp_master' exists")
        log_gray("3. User 'greek_erp_user' has access")
        log_gray("4. Connection details are correct")
        sys.exit(1)
    
    log_success("Database connection successful")
    
    # Check database schema
    log_info("Checking database schema...")
    if not await check_database_schema():
        log_error("Database schema not found. Please run:")
        log_gray("psql -U greek_erp_user -d greek_erp_master -f scripts/database-init.sql")
        sys.exit(1)
    
    log_success("Database schema found")
    
    # Get input from user
    company_data = get_company_input()
    user_data = get_user_input()
    
    # Confirm creation
    print()
    log_info("Summary:")
    log_gray(f"Company: {company_data['name']} (AFM: {company_data['afm']})")
    log_gray(f"User: {user_data['username']} ({user_data['email']})")
    
    confirm = input("\nCreate company and superuser? (y/N): ").strip().lower()
    if confirm != 'y':
        log_info("Setup cancelled")
        sys.exit(0)
    
    # Create company and user
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        
        # Start transaction
        async with conn.transaction():
            # Create company
            log_info("Creating company...")
            company_id = await create_company(conn, company_data)
            
            # Create superuser
            log_info("Creating superuser...")
            user_id = await create_superuser(conn, company_id, user_data)
            
            # Assign admin role
            log_info("Assigning admin role...")
            await assign_admin_role(conn, user_id)
            
            # Initialize company configuration
            log_info("Initializing company configuration...")
            await initialize_company_config(conn, company_id)
        
        await conn.close()
        
        # Success message
        print()
        log_success("🎉 Setup completed successfully!")
        print("=" * 40)
        log_gray(f"Company ID: {company_id}")
        log_gray(f"User ID: {user_id}")
        log_gray(f"Username: {user_data['username']}")
        log_gray(f"Email: {user_data['email']}")
        print()
        log_info("You can now:")
        log_gray("1. Start the API services")
        log_gray("2. Login with the created credentials")
        log_gray("3. Begin using the Greek ERP/CRM system")
        
    except Exception as e:
        log_error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_info("Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        sys.exit(1) 