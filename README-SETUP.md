# Greek ERP/CRM System Setup Guide

Complete setup guide for developers to get the **hybrid Poetry + npm workspace** system running locally.

## 🏗️ **Hybrid Monorepo Architecture**

This system uses a **modern hybrid monorepo** approach:

- **📦 npm workspaces** - JavaScript/TypeScript frontend applications and shared packages
- **🐍 Poetry workspace** - Python backend services with unified dependency management
- **🔄 Single Poetry environment** - Replaces 6 separate virtual environments
- **⚡ Unified commands** - One interface for both JavaScript and Python ecosystems

### **Key Benefits:**

- ✅ **Dependency consolidation** - Common Python packages installed once
- ✅ **Simplified development** - Single environment for all Python services
- ✅ **Faster setup** - Unified installation process
- ✅ **Better orchestration** - npm scripts manage both ecosystems
- ✅ **Consistent tooling** - Shared linting, formatting, and testing

## 🚀 Quick Start

**For experienced developers:**

```bash
# 1. Install Poetry (if not installed)
pip install poetry

# 2. Install all dependencies (JavaScript + Python)
npm run install:both

# 3. Setup database (Windows)
powershell -ExecutionPolicy Bypass -File scripts/setup-database-windows.ps1

# 4. Initialize database schema
psql -U greek_erp_user -d greek_erp_master -f scripts/database-init.sql

# 5. Create superuser
poetry run python create-superuser.py

# 6. Start all services
npm run dev:all
```

## 📋 Prerequisites

### System Requirements

- **Windows 10/11** (for development)
- **Python 3.11+** with pip
- **Poetry** (Python dependency management) - `pip install poetry`
- **Node.js 18+** (for frontend and npm workspaces)
- **PostgreSQL 12+** (will be installed automatically)
- **Git** (for version control)

### Hardware Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **CPU**: Multi-core processor recommended

## 🔧 Step-by-Step Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd greek-erp-crm
```

### Step 2: Dependencies Setup

#### **Install All Dependencies (Recommended)**

```bash
# Install both JavaScript and Python dependencies
npm run install:both
```

#### **Manual Installation**

```bash
# 1. Install JavaScript dependencies (frontend apps + packages)
npm run install:js

# 2. Install Python dependencies (Poetry workspace)
npm run install:python

# 3. Verify Poetry workspace
poetry env info
```

**What this does:**

- ✅ **JavaScript ecosystem**: Installs all npm workspace dependencies
- ✅ **Python ecosystem**: Creates single Poetry workspace for all 6 services
- ✅ **Shared dependencies**: FastAPI, SQLAlchemy, PyJWT installed once
- ✅ **Service-specific deps**: Each service gets its specialized packages
- ✅ **Development tools**: Black, MyPy, pytest configured
- ✅ **No virtual env conflicts**: Single unified Poetry environment

**Expected output:**

```bash
> npm run install:both

> greek-erp-crm@1.0.0 install:both
> npm run install:js && npm run install:python

✓ JavaScript dependencies installed
✓ Poetry workspace created: greek-erp-monorepo-L_BTagln-py3.12
✓ Python dependencies installed
✓ All 6 services configured in Poetry workspace
🎉 Hybrid monorepo setup complete!
```

#### **Verify Installation**

```bash
# Test Poetry environment
poetry run python --version
# Python 3.12.1

# Test shared dependencies
poetry run python -c "import fastapi; print(fastapi.__version__)"
# 0.104.1

# Check workspace info
poetry env info
```

#### Troubleshooting Dependencies

| Issue                  | Solution                              |
| ---------------------- | ------------------------------------- |
| Poetry not found       | `pip install poetry`, add to PATH     |
| npm not found          | Install Node.js 18+ and add to PATH   |
| Permission denied      | Run PowerShell as Administrator       |
| Poetry workspace error | `poetry env remove python` then retry |

### Step 3: Database Setup

#### Windows Database Setup

```powershell
# Run database setup script
powershell -ExecutionPolicy Bypass -File scripts/setup-database-windows.ps1
```

**What this script does:**

- ✅ Detects/installs PostgreSQL
- ✅ Configures database authentication
- ✅ Creates database and user
- ✅ Sets up Greek locale support
- ✅ Updates .env files with connection details
- ✅ Tests database connection

**Interactive prompts:**

1. **PostgreSQL Installation**: If not found, installs via winget
2. **Postgres Password**: Enter the postgres superuser password
3. **Existing Data**: Choose whether to recreate existing database/user

**Expected output:**

```
Greek ERP/CRM Database Setup for Windows
=========================================
✓ PostgreSQL found: PostgreSQL 16.1
✓ PostgreSQL tools ready
✓ PostgreSQL connection successful
✓ Database user 'greek_erp_user' created
✓ Database 'greek_erp_master' created with Greek locale
✓ Permissions configured
✓ New user connection successful
🎉 Database Setup Complete!
```

#### Linux Database Setup

```bash
# Make script executable
chmod +x scripts/setup-database-linux.sh

# Run database setup
./scripts/setup-database-linux.sh
```

### Step 4: Initialize Database Schema

```bash
# Windows
psql -U greek_erp_user -d greek_erp_master -f scripts/database-init.sql

# Linux
psql -U greek_erp_user -d greek_erp_master -f scripts/database-init.sql
```

**What this creates:**

- 📋 Company management tables
- 👥 User and role management
- 🏪 Customer and product management
- 🧾 Invoice management with Greek tax support
- 📊 Audit logging system
- 🇬🇷 Greek tax configuration
- 📋 AADE integration logging
- 🔧 Database functions for Greek business logic

### Step 5: Create Superuser Account

```bash
# Use Poetry to run the superuser creation script
poetry run python create-superuser.py
```

**Interactive setup:**

1. **Company Information**:

   - Company Name
   - AFM (Greek Tax Number) - validated
   - DOY (Tax Office Code)
   - Address, City, Postal Code
   - Phone, Email, Website
   - Legal Form (ΑΕ, ΕΠΕ, ΟΕ, ΕΕ, ΙΚΕ, Other)

2. **User Account**:
   - Username (minimum 3 characters)
   - Email (validated format)
   - Password (minimum 8 characters)
   - First Name, Last Name
   - Phone (Greek format)

**Expected output:**

```
Greek ERP/CRM Superuser Creation
========================================
✓ Database connection successful
✓ Database schema found
✓ Company 'Test Company' created successfully
✓ Superuser 'admin' created successfully
✓ Admin role assigned to user
✓ Company configuration initialized
🎉 Setup completed successfully!
```

### Step 6: Start Services

#### **Start All Services (Recommended)**

```bash
# Start all frontend and backend services
npm run dev:all
```

#### **Start Services Separately**

```bash
# Start all frontend apps
npm run dev:js

# Start all backend services
npm run dev:python

# Or start individual services
npm run dev:api            # Main API (port 8000)
npm run dev:auth           # Auth service (port 8001)
npm run dev:files          # File service (port 8002)
npm run dev:integrations   # Integrations (port 8003)
npm run dev:ai-support     # AI Support (port 8004)
npm run dev:voice          # Voice AI (port 8005)
```

**Services started via Poetry workspace:**

- 📡 **API Service** (port 8000) - Main business logic with Poetry
- 🔐 **Auth Service** (port 8001) - Authentication via Poetry
- 📁 **Files Service** (port 8002) - File management via Poetry
- 🔌 **Integrations Service** (port 8003) - AADE integration via Poetry
- 🤖 **AI Support Service** (port 8004) - AI assistance via Poetry
- 🎤 **Voice AI Service** (port 8005) - Voice commands via Poetry

### Step 7: Verify Installation

```bash
# Test API health
curl http://localhost:8000/health

# Test Auth service
curl http://localhost:8001/health

# Expected response:
{"status": "healthy", "service": "Greek ERP/CRM API", "version": "1.0.0"}
```

## 🌐 Frontend Setup (Optional)

The frontend is already set up as a Next.js monorepo. To run it:

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:3000
```

## 📁 Project Structure

```
greek-erp-crm/
├── services/                 # Backend services
│   ├── api/                 # Main API service
│   ├── auth/                # Authentication service
│   ├── files/               # File management service
│   └── integrations/        # External integrations
├── packages/
│   ├── ai-services/         # AI-powered services
│   │   ├── voice-service/   # Voice recognition
│   │   └── ai-support-service/ # AI support
│   └── web-apps/           # Frontend applications
├── scripts/                 # Setup and utility scripts
├── create-superuser.py      # Superuser creation script
└── README-SETUP.md         # This file
```

## 🔧 Configuration

### Environment Variables

Each service has its own `.env` file with:

- Database connection details
- JWT authentication settings
- Greek business configuration
- AADE integration settings
- Service communication URLs

### Greek Business Configuration

- **VAT Rates**: 24% (default), 13%, 6%, 0%
- **Currency**: EUR
- **Locale**: Greek (el_GR)
- **Timezone**: Europe/Athens
- **AADE**: MyDATA integration for Greek tax compliance

## 🚨 Troubleshooting

### Common Issues

#### "PowerShell execution policy error"

```powershell
# Solution: Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### "Python not found"

```bash
# Solution: Install Python 3.8+ and add to PATH
# Download from: https://www.python.org/downloads/
```

#### "PostgreSQL connection failed"

```bash
# Solution: Check if PostgreSQL is running
# Windows: services.msc -> PostgreSQL service
# Linux: sudo systemctl status postgresql
```

#### "Port already in use"

```bash
# Solution: Stop conflicting services
# Windows: netstat -ano | findstr :8000
# Linux: sudo lsof -i :8000
```

#### "Database schema not found"

```bash
# Solution: Run database initialization
psql -U greek_erp_user -d greek_erp_master -f scripts/database-init.sql
```

#### "AFM validation failed"

```bash
# Solution: Use valid Greek AFM with correct checksum
# Example valid AFM: 9 (test only)
```

### Service-Specific Issues

#### API Service Errors

- **Config parsing error**: Check `.env` file format
- **Database connection**: Verify DATABASE_URL in `.env`
- **Import errors**: Ensure all dependencies installed

#### Auth Service Errors

- **JWT secret missing**: Set JWT_SECRET_KEY in `.env`
- **Role assignment**: Verify roles table populated

#### Database Issues

- **Connection refused**: Check PostgreSQL service status
- **Permission denied**: Verify user privileges
- **Locale errors**: Check Greek locale installation

## 📊 Monitoring and Logs

### Service Logs

Each service logs to console with structured logging:

- **INFO**: General operation information
- **ERROR**: Error conditions and exceptions
- **DEBUG**: Detailed debugging information

### Database Monitoring

- **Connections**: Monitor active connections
- **Performance**: Query performance and slow queries
- **Storage**: Database size and growth

### Health Checks

All services provide health check endpoints:

- `GET /health` - Service health status
- `GET /metrics` - Service metrics (if enabled)

## 🔐 Security Notes

### Default Credentials

- **Database User**: `greek_erp_user`
- **Database Password**: ``
- **Superuser**: Created during setup

### Production Considerations

- Change all default passwords
- Use environment-specific secrets
- Enable SSL/TLS for all services
- Configure proper firewall rules
- Regular security updates

## 🆘 Support

### Documentation

- **API Documentation**: Available at `/docs` endpoint
- **Database Schema**: See `scripts/database-init.sql`
- **Configuration**: Check `.env` files

### Community

- **Issues**: Report on GitHub issues
- **Discussions**: GitHub discussions for questions
- **Wiki**: Detailed documentation and guides

## 🎯 Next Steps

After successful setup:

1. **Access Web Interface**: http://localhost:3000
2. **Login**: Use created superuser credentials
3. **Configure Company**: Set up your Greek business details
4. **Import Data**: Use import tools for existing data
5. **Customize**: Configure workflows and permissions
6. **Go Live**: Deploy to production environment

## 📝 Development Notes

### Development Workflow

```bash
# Start backend services
scripts/start-all-services.ps1

# Start frontend (separate terminal)
npm run dev

# Make changes and test
# Services auto-reload on changes
```

### Database Changes

```bash
# Apply schema changes
psql -U greek_erp_user -d greek_erp_master -f scripts/database-init.sql

# Create migrations (if using Alembic)
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Testing

```bash
# Run backend tests
cd services/api
python -m pytest

# Run frontend tests
npm test
```

---

**🎉 Congratulations!** Your Greek ERP/CRM system is now ready for development and testing.

For production deployment, see the production deployment guide.
