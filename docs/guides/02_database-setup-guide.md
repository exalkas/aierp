# Greek ERP Database Setup Guide

## 🏛️ Complete Database Setup Instructions

This guide provides step-by-step instructions for setting up the Greek ERP/CRM database with Alembic migrations and complete workflow seeding.

## 📋 Prerequisites

- PostgreSQL 12+ installed with Greek locale support
- Python 3.9+ with virtual environment
- All backend services set up (see [BACKEND_SETUP.md](../docs/progress/BACKEND_SETUP.md))

## 🗄️ Database Setup Process

### Step 1: Create PostgreSQL Database

## 🔄 What Each Script Does:

| Script             | Database          | Tables           | Data     |
| ------------------ | ----------------- | ---------------- | -------- |
| complete-setup.ps1 | ✅ Checks/Creates | ✅ Drops/Creates | ✅ Seeds |
| reset-database.ps1 | ❌ Assumes exists | ✅ Drops/Creates | ✅ Seeds |
| create-db-user.sql | ✅ Creates        | ❌ None          | ❌ None  |

**Windows (PowerShell):**

```powershell
.\scripts\setup-database-windows.ps1
```

**Linux/macOS:**

```bash
chmod +x scripts/setup-database-linux.sh
./scripts/setup-database-linux.sh
```

**Manual Setup:**

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database with Greek locale
CREATE DATABASE greek_erp_master
  WITH ENCODING 'UTF8'
  LC_COLLATE = 'el_GR.UTF-8'
  LC_CTYPE = 'el_GR.UTF-8'
  TEMPLATE = template0;

-- Create user for the application
CREATE USER greek_erp_user WITH PASSWORD '';
GRANT ALL PRIVILEGES ON DATABASE greek_erp_master TO greek_erp_user;
```

### Step 2: Configure Environment Variables

Create or update `.env` file in `services/api/`:

```env
# Database Configuration
DATABASE_URL=postgresql://greek_erp_user:@localhost/greek_erp_master

# Application Settings
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ENVIRONMENT=development

# Greek Business Settings
DEFAULT_TIMEZONE=Europe/Athens
DEFAULT_LOCALE=el_GR
DEFAULT_CURRENCY=EUR
DEFAULT_VAT_RATE=0.24

# AADE Integration (for production)
AADE_SUBSCRIPTION_KEY=your-aade-key-here
AADE_USER_ID=your-aade-user-id
AADE_API_BASE_URL=https://mydata-dev.aade.gr
```

### Step 3: Initialize Alembic Database

Navigate to the API service directory:

```bash
cd services/api
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\Activate.ps1  # Windows
```

Run Alembic migrations:

```bash
# Run all migrations to latest version
alembic upgrade head

# This will apply all migrations in order:
# 0001 - Initial Greek ERP schema (companies, users, business entities, etc.)
# 0002 - Document state machine models
# 0003 - CRM and ERP models (leads, opportunities, activities, etc.)
# 0004 - Voice command system
# 0005 - Master database models (Greek reference data, system configuration)

# Verify current migration
alembic current
```

### Step 4: Seed Database with Greek Reference Data

Seed the database with Greek reference data and document workflows:

```bash
# First, seed Greek reference data (shared across all companies)
python -m app.scripts.seed_greek_reference_data

# Then seed Greek document workflows for all companies
python -m app.scripts.seed_greek_document_workflows

# Or seed workflows for specific company
python -m app.scripts.seed_greek_document_workflows --company-id <company-uuid>
```

**What gets seeded:**

- **Greek Reference Data**: 13 regions, major tax offices, VAT rates, legal forms, banks
- **Document Workflows**: All 16 Greek document types with state machines
- **Voice Commands**: Default Greek voice commands (if companies exist)

### Step 5: Create Initial Company and User

Create your first company and admin user:

```bash
# Run the superuser creation script
python -m app.scripts.create_superuser
```

Or manually:

```python
# create_company_and_user.py
import asyncio
from app.core.database import async_session
from app.models.company import Company
from app.models.user import User
from app.models.company_user import CompanyUser
from app.core.security import get_password_hash

async def create_initial_setup():
    async with async_session() as db:
        # Create company
        company = Company(
            name="Sample Greek Company Ltd",
            afm="9",
            doy="A1234",
            email="info@company.gr",
            database_name="erp_company_sample",
            city="Athens",
            country="GR"
        )
        db.add(company)
        await db.flush()

        # Create admin user
        admin_user = User(
            email="admin@company.gr",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        await db.flush()

        # Associate user with company
        company_user = CompanyUser(
            company_id=company.id,
            user_id=admin_user.id,
            role="admin",
            is_active=True
        )
        db.add(company_user)

        await db.commit()
        print(f"Created company: {company.name}")
        print(f"Created admin user: {admin_user.email}")

if __name__ == "__main__":
    asyncio.run(create_initial_setup())
```

### Step 6: Verify Setup

Test the database setup:

```bash
# Start the API service
uvicorn main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/workflow/templates
curl http://localhost:8000/api/v1/workflow/states
curl http://localhost:8000/api/v1/workflow/actions
```

## 🔍 Database Schema Overview

### Master Database Tables (Shared Reference Data)

1. **companies** - Master company registry
2. **users** - User accounts
3. **greek_regions** - Greek regions and prefectures with VAT zones
4. **greek_tax_offices** - DOY offices directory
5. **greek_vat_rates** - Context-aware VAT rates by business type
6. **greek_business_activities** - KAD codes with classifications
7. **greek_legal_forms** - Greek legal forms (AE, EPE, OE, etc.)
8. **greek_banks** - Greek banks with SWIFT codes
9. **postal_codes** - Greek postal codes with geographic data
10. **system_configurations** - Global system settings
11. **subscription_plan_definitions** - Available subscription plans
12. **company_subscriptions** - Company subscription tracking
13. **usage_metrics** - Usage tracking across companies
14. **system_notifications** - System-wide notifications
15. **api_keys** - API keys for integrations

### Core Business Tables (Per Company Database)

1. **business_entities** - Unified customers/suppliers
2. **products** - Product catalog with Greek VAT compliance
3. **invoices** - All document types (16 Greek παραστατικά)
4. **contacts** - Contact information
5. **audit_logs** - Complete audit trail
6. **leads** - CRM lead management
7. **opportunities** - Sales pipeline
8. **activities** - CRM activities and tasks
9. **cases** - Customer service cases
10. **campaigns** - Marketing campaigns

### State Machine Tables (Per Company Database)

1. **state_transition_rules** - Workflow transition rules
2. **document_workflow_instances** - Active workflow instances
3. **document_state_history** - Complete state history
4. **document_automation_rules** - Automated workflow rules
5. **greek_document_workflow_templates** - Document templates

### Voice Command Tables (Per Company Database)

1. **system_voice_commands** - Default system voice commands
2. **user_voice_commands** - User customizations
3. **voice_command_logs** - Execution analytics
4. **voice_command_templates** - Command creation templates

## 🏛️ Greek Document Types Supported

The system supports all 16 Greek business document types (παραστατικά):

1. **Προτιμολόγιο** (Proforma)
2. **Δελτίο Παραγγελίας** (Sales Order)
3. **Επιβεβαίωση Παραγγελίας** (Order Confirmation)
4. **Παραγγελία Προμηθευτή** (Purchase Order)
5. **Δελτίο Αποστολής** (Delivery Note)
6. **Τιμολόγιο Πώλησης** (Sales Invoice)
7. **Απλοποιημένο Τιμολόγιο** (Simplified Invoice)
8. **Απόδειξη Λιανικής** (Receipt)
9. **Πιστωτικό Τιμολόγιο** (Credit Note)
10. **Χρεωστικό Τιμολόγιο** (Debit Note)
11. **Τιμολόγιο Αγοράς** (Purchase Invoice)
12. **Αναφορά Δαπανών** (Expense Report)
13. **Σύμβαση** (Contract)
14. **Αυτοτιμολόγιο** (Self Invoice)
15. **Παραστατικό Πληρωμής** (Payment Voucher)
16. **Απόδειξη Ταμείου** (Cash Register Receipt)

## 🔧 Migration Commands

Common Alembic commands:

```bash
# Check current migration
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade 0002

# Downgrade one revision
alembic downgrade -1

# Show differences between database and models
alembic check

# Create new migration (when models change)
alembic revision --autogenerate -m "Add new feature"
```

## 🚀 Production Deployment

For production deployment:

1. **Use strong passwords** for database and application
2. **Set up SSL/TLS** for database connections
3. **Configure proper AADE credentials** for MyDATA integration
4. **Set up backup strategy** for database
5. **Configure monitoring** for workflow processes
6. **Set up log rotation** for audit logs

```env
# Production environment variables
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@db-server/greek_erp_master
SECRET_KEY=
JWT_SECRET_KEY=
AADE_SUBSCRIPTION_KEY=
AADE_API_BASE_URL=https://mydata.aade.gr
```

## 🆘 Troubleshooting

### Common Issues

**Migration fails with "table already exists":**

```bash
# Mark current state as migrated
alembic stamp head
```

**Database connection errors:**

```bash
# Test connection
psql -h localhost -U greek_erp_user -d greek_erp_master

# Check if database exists
psql -U postgres -l | grep greek_erp
```

**Workflow seeding fails:**

```bash
# Check if companies exist
python -c "
import asyncio
from app.core.database import async_session
from app.models.company import Company
from sqlalchemy import select

async def check():
    async with async_session() as db:
        result = await db.execute(select(Company))
        companies = result.scalars().all()
        print(f'Found {len(companies)} companies')
        for c in companies:
            print(f'  - {c.name} ({c.afm})')

asyncio.run(check())
"
```

**Alembic version conflicts:**

```bash
# Reset alembic to current database state
alembic stamp head

# Or start fresh
alembic stamp base
alembic upgrade head
```

## 📊 Monitoring and Maintenance

### Database Health Checks

```sql
-- Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check workflow statistics
SELECT
    document_type,
    current_state,
    COUNT(*) as count
FROM document_workflow_instances
GROUP BY document_type, current_state
ORDER BY document_type, count DESC;

-- Check audit log growth
SELECT
    DATE(created_at) as date,
    COUNT(*) as actions
FROM audit_logs
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Backup Strategy

```bash
# Daily backup
pg_dump -h localhost -U greek_erp_user greek_erp_master > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -h localhost -U greek_erp_user greek_erp_master | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore from backup
psql -h localhost -U greek_erp_user greek_erp_master < backup_20240101.sql
```

The database is now ready for development and production use! 🎉

## 🔗 Next Steps

1. **Configure frontend applications** to connect to the API
2. **Implement Greek reference data components** using [Greek Reference Data API Guide](03_greek-reference-data-api.md)
3. **Set up AADE integration** for production
4. **Configure email notifications** for workflow actions
5. **Set up monitoring** for performance and errors
6. **Configure automated backups** for production

## 📚 Related Documentation

- [Greek Reference Data API Reference](03_greek-reference-data-api.md) - API endpoints for Greek reference data
- [Master Database Models](../progress/MASTER_DATABASE_MODELS.md) - Complete model documentation
- [Backend Setup Guide](../progress/BACKEND_SETUP.md) - Backend service setup
