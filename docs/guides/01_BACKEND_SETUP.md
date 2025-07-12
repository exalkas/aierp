# Greek ERP/CRM Backend Setup Guide

## 🏛️ Overview

The backend infrastructure for the Greek ERP/CRM system has been successfully set up with a microservices architecture featuring:

- **5 Backend Services** (Python/FastAPI)
- **Separate Database per Company** architecture
- **Greek Business Compliance** built-in
- **AADE Integration** ready
- **AI Services** for voice and support

## 📁 Backend Architecture

```
services/
├── api/              # Main API service (Port 8000)
├── auth/             # Authentication service (Port 8001)
├── files/            # File storage service (Port 8002)
└── integrations/     # AADE & external integrations (Port 8003)

packages/ai-services/
├── voice-service/    # Voice AI service (Port 8004)
└── ai-support-service/ # AI support service (Port 8005)
```

## 🚀 Quick Start

### 1. Setup Virtual Environments

**For Linux/macOS:**

```bash
chmod +x scripts/setup-backend.sh
./scripts/setup-backend.sh
```

**For Windows:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\setup-backend.ps1
```

### 2. Configure Environment Variables

Create `.env` files in each service directory using the template from `services/.env.example`:

```bash
# Copy environment template to each service
cp services/.env.example services/api/.env
cp services/.env.example services/auth/.env
cp services/.env.example services/files/.env
cp services/.env.example services/integrations/.env
cp services/.env.example packages/ai-services/voice-service/.env
cp services/.env.example packages/ai-services/ai-support-service/.env
```

**Key settings to configure:**

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Application secret key
- `JWT_SECRET_KEY`: JWT signing key
- `AADE_SUBSCRIPTION_KEY`: Greek tax authority API key

### 3. Setup Database with Alembic Migrations

**📋 Complete Database Setup Guide Available:** [scripts/database-setup-guide.md](../../scripts/database-setup-guide.md)

**Quick Setup:**

1. **Install PostgreSQL** with Greek locale support
2. **Create database:**

```bash
# Windows
.\scripts\setup-database-windows.ps1

# Linux/macOS
chmod +x scripts/setup-database-linux.sh
./scripts/setup-database-linux.sh
```

3. **Run Alembic migrations:**

```bash
cd services/api
source venv/bin/activate  # Linux/macOS
# OR venv\Scripts\Activate.ps1  # Windows

# Initialize database with migrations
alembic upgrade 0001  # Core models
alembic upgrade 0002  # Document state machine
```

4. **Seed Greek document workflows:**

```bash
python -m app.scripts.seed_greek_document_workflows
```

5. **Create initial company and admin user:**

```bash
python -m app.scripts.create_superuser
```

### 4. Start Services

**Main API Service:**

```bash
cd services/api
source venv/bin/activate  # Linux/macOS
# OR venv\Scripts\Activate.ps1  # Windows
uvicorn main:app --reload --port 8000
```

**All Services (in separate terminals):**

```bash
# API Service
cd services/api && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Auth Service
cd services/auth && source venv/bin/activate && uvicorn main:app --reload --port 8001

# Files Service
cd services/files && source venv/bin/activate && uvicorn main:app --reload --port 8002

# Integrations Service
cd services/integrations && source venv/bin/activate && uvicorn main:app --reload --port 8003

# Voice AI Service
cd packages/ai-services/voice-service && source venv/bin/activate && uvicorn main:app --reload --port 8004

# AI Support Service
cd packages/ai-services/ai-support-service && source venv/bin/activate && uvicorn main:app --reload --port 8005
```

## 🏛️ Greek Business Features

### Built-in Compliance

- **AFM Validation**: Greek tax number validation with checksum
- **DOY Validation**: Greek tax office codes
- **VAT Calculations**: 24%, 13%, 6%, 0% rates
- **Greek Localization**: Dates, currency, phone numbers
- **AADE Integration**: Ready for MyDATA submissions

### Document State Machine

- **16 Greek Document Types**: Complete support for all παραστατικά
- **Workflow Management**: State transitions with business rules
- **Greek Business Rules**: VAT, AADE, and legal compliance
- **Audit Trail**: Complete document lifecycle tracking
- **Automated Workflows**: Rule-based state transitions

### Company Isolation

- **Separate Database per Company**: No data mixing between tenants
- **JWT Company Context**: Every request tied to specific company
- **Middleware Protection**: Automatic isolation enforcement

### Audit & Compliance

- **Complete Audit Trail**: All API operations logged
- **Greek Data Protection**: Sensitive data handling
- **Security Middleware**: Rate limiting, input validation
- **Document History**: Complete state change tracking

## 🛠️ Service Details

### API Service (Port 8000)

- **Main business logic**
- **Greek compliance middleware**
- **Company isolation**
- **Audit logging**

**Key Endpoints:**

- `GET /health` - Service health
- `GET /api/v1/greek/vat-rates` - Greek VAT rates
- `POST /api/v1/greek/validate/afm` - AFM validation

**Document Workflow Endpoints:**

- `POST /api/v1/workflow/initialize` - Initialize document workflow
- `GET /api/v1/workflow/status/{document_id}` - Get workflow status
- `POST /api/v1/workflow/execute/{document_id}` - Execute state transition
- `GET /api/v1/workflow/actions/{document_id}` - Get available actions
- `GET /api/v1/workflow/history/{document_id}` - Get state history
- `GET /api/v1/workflow/templates` - Get workflow templates
- `GET /api/v1/workflow/states` - Get all document states
- `GET /api/v1/workflow/actions` - Get all document actions

### Auth Service (Port 8001)

- **JWT authentication**
- **Company context in tokens**
- **Multi-factor authentication ready**

### Files Service (Port 8002)

- **Secure file upload/download**
- **Greek document processing**
- **PDF generation for invoices**

### Integrations Service (Port 8003)

- **AADE MyDATA integration**
- **Greek banking APIs**
- **Payment gateways**

### Voice AI Service (Port 8004)

- **Greek speech recognition**
- **Text-to-speech synthesis**
- **Voice commands for ERP**

### AI Support Service (Port 8005)

- **Greek language chatbot**
- **Intelligent ticket routing**
- **ERP knowledge base**

## 📊 Database Schema

### Master Database (`greek_erp_master`)

- **companies**: Company registry with Greek business data
- **users**: User accounts with Greek localization
- **company_users**: Multi-tenant user associations
- **audit_logs**: Comprehensive audit trail

### Company Databases (`erp_company_{id}`)

- Separate database for each company
- Full ERP/CRM schema per company
- Complete data isolation

### Document State Machine Schema

- **state_transition_rules**: Workflow transition rules with Greek business logic
- **document_workflow_instances**: Active workflow instances for documents
- **document_state_history**: Complete audit trail of state changes
- **document_automation_rules**: Automated workflow rules
- **greek_document_workflow_templates**: Pre-configured Greek document workflows

## 🔧 Development Tools

### API Documentation

When running in development mode:

- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Health Checks

- API Service: http://localhost:8000/health
- Auth Service: http://localhost:8001/health
- Files Service: http://localhost:8002/health
- Integrations: http://localhost:8003/health
- Voice AI: http://localhost:8004/health
- AI Support: http://localhost:8005/health

### Document Workflow Testing

```bash
# Test workflow endpoints
curl http://localhost:8000/api/v1/workflow/states
curl http://localhost:8000/api/v1/workflow/actions
curl http://localhost:8000/api/v1/workflow/templates

# Test workflow initialization
curl -X POST http://localhost:8000/api/v1/workflow/initialize \
  -H "Content-Type: application/json" \
  -d '{"document_type": "sales_invoice", "document_id": "uuid-here"}'

# Test workflow execution
curl -X POST http://localhost:8000/api/v1/workflow/execute/uuid-here \
  -H "Content-Type: application/json" \
  -d '{"action": "FINALIZE", "notes": "Ready for approval"}'
```

### Logging

All services configured with:

- **Console logging** (development)
- **File logging** (`logs/` directory)
- **Audit logging** (compliance)

## 🔒 Security Features

### Authentication

- **JWT tokens** with company context
- **15-minute access tokens**
- **7-day refresh tokens**
- **Multi-factor authentication ready**

### Company Isolation

- **Middleware enforcement**
- **Database-level separation**
- **JWT company binding**

### Greek Compliance

- **AFM/DOY validation**
- **Greek VAT rate enforcement**
- **AADE integration preparation**

## 🚀 Next Steps

1. **Configure environment variables** in each service
2. **Setup PostgreSQL** with Greek locale
3. **Run database migrations**
4. **Start all services**
5. **Test health endpoints**
6. **Begin frontend integration**

## 📋 Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in all `.env` files
2. Configure proper database URLs
3. Set up HTTPS/SSL certificates
4. Configure proper AADE production credentials
5. Set up monitoring and alerting
6. Configure backup strategies

## 🆘 Troubleshooting

### Common Issues

**Port conflicts:**

```bash
# Check what's using ports
lsof -i :8000-8005  # Linux/macOS
netstat -an | findstr :8000  # Windows
```

**Database connection:**

```bash
# Test PostgreSQL connection
psql -h localhost -U username -d greek_erp_master
```

**Virtual environment issues:**

```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The backend infrastructure is now ready for development! 🎉
