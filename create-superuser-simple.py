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
Simple Greek ERP/CRM Superuser Creation Script
Creates a company and superuser account
"""

import os
import sys
import asyncio
import getpass
import re
from uuid import uuid4
from datetime import datetime

# Add the services directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'api'))

try:
    import asyncpg
    from passlib.context import CryptContext
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install asyncpg passlib")
    sys.exit(1)

# Use the new credentials
DB_CONFIG = {"dsn": required_env("DATABASE_URL")}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def log_info(message):
    print(f"INFO: {message}")

def log_success(message):
    print(f"SUCCESS: {message}")

def log_error(message):
    print(f"ERROR: {message}")

def validate_email(email):
    """Simple email validation"""
    return '@' in email and '.' in email

def validate_afm(afm):
    """Simple AFM validation"""
    return len(afm) == 9 and afm.isdigit()

async def check_database_connection():
    """Test database connection"""
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        await conn.close()
        return True
    except Exception as e:
        log_error(f"Database connection failed: {e}")
        return False

async def create_company(conn, company_data):
    """Create a new company with new schema"""
    company_id = str(uuid4())
    
    try:
        await conn.execute("""
            INSERT INTO companies (
                id, name, display_name, business_activity, afm, doy, legal_form,
                email, address_street, address_number, address_city,
                address_postal_code, address_region, address_country, vat_number, vat_regime,
                default_currency, default_language, timezone, accounting_start_date,
                fiscal_year_start, subscription_plan, subscription_status,
                is_active, is_verified, setup_completed, database_name, database_created,
                created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29)
        """, 
        company_id, company_data['name'], company_data['name'], 
        "Software Development", company_data['afm'], company_data['doy'], company_data['legal_form'],
        company_data['email'], company_data['address'], "1", company_data['city'],
        company_data['postal_code'], "Attica", "GR", "EL" + company_data['afm'], "standard",
        "EUR", "el", "Europe/Athens", datetime.now(),
        "01-01", "basic", "active",
        True, True, True, f"company_{company_data['afm']}", True,
        datetime.now()
        )
        
        log_success(f"Company '{company_data['name']}' created")
        return company_id
        
    except Exception as e:
        log_error(f"Failed to create company: {e}")
        raise

async def create_superuser(conn, company_id, user_data):
    """Create a superuser"""
    user_id = str(uuid4())
    password_hash = pwd_context.hash(user_data['password'])
    
    try:
        await conn.execute("""
            INSERT INTO users (
                id, company_id, username, email, password_hash, 
                first_name, last_name, phone, role, status, is_active, 
                is_verified, is_super_user, can_be_deleted, can_change_password, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        """, 
        user_id, company_id, user_data['username'], user_data['email'],
        password_hash, user_data['first_name'], user_data['last_name'],
        user_data['phone'], 'SUPER_ADMIN', 'active', True, 
        True, True, False, True, datetime.now()
        )
        
        log_success(f"Superuser '{user_data['username']}' created")
        return user_id
        
    except Exception as e:
        log_error(f"Failed to create superuser: {e}")
        raise

def get_company_input():
    """Get company information from user"""
    print("\nCOMPANY INFORMATION:")
    print("===================")
    
    company_data = {}
    
    company_data['name'] = input("Company Name [alkas]: ").strip() or "alkas"
    
    company_data['afm'] = input("AFM (9 digits) [047180058]: ").strip() or "047180058"
    if not validate_afm(company_data['afm']):
        company_data['afm'] = input("AFM (9 digits, required): ").strip()
        while not validate_afm(company_data['afm']):
            company_data['afm'] = input("AFM (9 digits, required): ").strip()
    
    company_data['doy'] = input("DOY Code [1101]: ").strip() or "1101"
    company_data['address'] = input("Address [abc]: ").strip() or "abc"
    company_data['city'] = input("City [rafina]: ").strip() or "rafina"
    company_data['postal_code'] = input("Postal Code [19009]: ").strip() or "19009"
    company_data['phone'] = input("Phone [123]: ").strip() or "123"
    company_data['email'] = input("Email [alkas@alkas.gr]: ").strip() or "alkas@alkas.gr"
    company_data['website'] = input("Website [alkas.gr]: ").strip() or "alkas.gr"
    
    print("\nLegal Form Options:")
    print("1. AE (Ανώνυμη Εταιρία)")
    print("2. EPE (Εταιρία Περιορισμένης Ευθύνης)")
    print("3. OE (Ομόρρυθμη Εταιρία)")
    print("4. EE (Ετερόρρυθμη Εταιρία)")
    print("5. IKE (Ιδιωτική Κεφαλαιουχική Εταιρία)")
    print("6. Other")
    
    legal_forms = {"1": "AE", "2": "EPE", "3": "OE", "4": "EE", "5": "IKE", "6": "Other"}
    choice = input("Select legal form (1-6) [1]: ").strip() or "1"
    company_data['legal_form'] = legal_forms.get(choice, "AE")
    
    return company_data

def get_user_input():
    """Get user information"""
    print("\nADMIN USER INFORMATION:")
    print("======================")
    
    user_data = {}
    
    user_data['username'] = input("Username [alkas]: ").strip() or "alkas"
    
    user_data['email'] = input("Email [alkas@alkas.gr]: ").strip() or "alkas@alkas.gr"
    if not validate_email(user_data['email']):
        user_data['email'] = input("Email (valid format): ").strip()
        while not validate_email(user_data['email']):
            user_data['email'] = input("Email (valid format): ").strip()
    
    user_data['password'] = required_env("SUPERUSER_PASSWORD")
    
    user_data['first_name'] = input("First Name [alkis]: ").strip() or "alkis"
    user_data['last_name'] = input("Last Name [kas]: ").strip() or "kas"
    user_data['phone'] = input("Phone [123]: ").strip() or "123"
    
    return user_data

async def main():
    """Main function"""
    print("Greek ERP/CRM Superuser Creation")
    print("================================")
    
    # Check database connection
    log_info("Checking database connection...")
    if not await check_database_connection():
        log_error("Cannot connect to database. Please check your setup.")
        return
    
    log_success("Database connection successful")
    
    # Get company information
    company_data = get_company_input()
    
    # Get user information
    user_data = get_user_input()
    
    # Create company and user
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        
        company_id = await create_company(conn, company_data)
        user_id = await create_superuser(conn, company_id, user_data)
        
        await conn.close()
        
        print("\nSUCCESS! Setup completed successfully!")
        print(f"Company: {company_data['name']}")
        print(f"Admin User: {user_data['username']}")
        print(f"Email: {user_data['email']}")
        print("\nYou can now start the services and login to the system.")
        
    except Exception as e:
        log_error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 