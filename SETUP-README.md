# Greek ERP/CRM Local Development Setup

## 🚀 **Quick Setup (Recommended)**

Run the complete automated setup:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/complete-setup.ps1
```

This runs all setup steps automatically in the correct order.

---

## 📋 **Manual Step-by-Step Setup**

If you prefer to run each step manually:

### **Prerequisites**

- Windows 10/11 ✅ (you have this)
- Python 3.8+ ✅
- PostgreSQL 17 ✅ (installed at `C:\Program Files\PostgreSQL\17\`)
- Git ✅

### **Step 1: Backend Services**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup-backend.ps1
```

**Creates:** Virtual environments for all 6 services, installs dependencies

### **Step 2: Database Setup**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup-database-windows.ps1
```

**Creates:** Database `erp_maritime_hellenic_4007`, user `erp_admin_315`, permissions

### **Step 3: Database Schema**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/init-database-schema.ps1
```

**Creates:** All tables, indexes, Greek business functions, audit system

### **Step 4: Admin User**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/create-admin-user.ps1
```

**Creates:** Your company and admin user account

### **Step 5: Start Services**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-all-services.ps1
```

**Starts:** All 6 backend services on ports 8000-8005

---

## 🔐 **Your Credentials**

Saved in `scripts/secure-credentials.env`:

```
Database: erp_maritime_hellenic_4007
User: erp_admin_315
Password: 
```

---

## ✅ **Verify Setup**

After setup, test these URLs:

- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health
- **Auth Service**: http://localhost:8001/health

**Expected Response:**

```json
{ "status": "healthy", "service": "Greek ERP/CRM API" }
```

---

## 🚀 **What's Running**

### **Backend Services (6 services)**

- **API Service** (8000) - Main business logic
- **Auth Service** (8001) - Authentication
- **Files Service** (8002) - File management
- **Integrations** (8003) - AADE integration
- **Voice AI** (8004) - Voice commands ⭐
- **AI Support** (8005) - Local AI support ⭐

### **Database**

- **PostgreSQL 17** with Greek locale
- **Multi-tenant** architecture
- **Greek business** validation (AFM, DOY, VAT)
- **AADE integration** ready

### **Features Ready**

- ✅ Company management
- ✅ User authentication
- ✅ Greek tax compliance
- ✅ Multi-tenant isolation
- ✅ Audit logging
- ✅ Voice command infrastructure
- ✅ AI support infrastructure

---

## 🛠️ **Troubleshooting**

### **PostgreSQL not found**

```powershell
# Check if PostgreSQL 17 is installed
Test-Path "C:\Program Files\PostgreSQL\17\bin\psql.exe"
```

### **Port conflicts**

```powershell
# Check what's using ports 8000-8005
netstat -an | findstr :8000
```

### **Service startup issues**

```powershell
# Check Python processes
Get-Process python
```

### **Database connection issues**

```powershell
# Test direct connection
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U erp_admin_315 -d erp_maritime_hellenic_4007 -c "SELECT 1;"
```

---

## 📁 **File Structure**

```
erp/
├── scripts/                    # Setup scripts
│   ├── complete-setup.ps1      # ⭐ Master setup script
│   ├── setup-backend.ps1       # Backend services
│   ├── setup-database-windows.ps1 # Database setup
│   ├── init-database-schema.ps1   # Schema creation
│   ├── create-admin-user.ps1   # Admin user creation
│   ├── start-all-services.ps1  # Start all services
│   ├── secure-credentials.env  # Your credentials
│   ├── database-init.sql       # Database schema
│   ├── create-db-user.sql      # Database creation
│   └── fix-permissions.sql     # Permission fixes
├── services/                   # Backend services
├── create-superuser-simple.py  # User creation script
└── apps/                       # Frontend (for Week 1+)
```

---

## 🎯 **Next Steps**

After successful setup:

1. **✅ Week 1 Foundation Setup** - COMPLETE
2. **🚀 Start Week 1 Development:**

   - Frontend setup (React/Next.js)
   - Business Entity Management UI
   - Authentication UI
   - Voice command integration

3. **📋 Development Workflow:**

   ```powershell
   # Start services (daily)
   scripts/start-all-services.ps1

   # Access API docs
   # Visit: http://localhost:8000/docs
   ```

---

## 🔒 **Security Notes**

- ✅ Production-ready credentials
- ✅ Multi-tenant company isolation
- ✅ Greek business validation
- ✅ Secure password hashing
- ✅ Environment-based configuration

**For production:** Change all credentials and use proper secrets management.

---

**🎉 Your Greek ERP/CRM development environment is ready!**
