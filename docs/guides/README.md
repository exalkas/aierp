# Greek ERP/CRM System - Guides

This directory contains comprehensive guides for setting up, developing, and maintaining the Greek ERP/CRM system.

## 📚 Available Guides

### Setup & Configuration

- **[01_BACKEND_SETUP.md](./01_BACKEND_SETUP.md)** - Backend services setup and configuration
- **[02_database-setup-guide.md](./02_database-setup-guide.md)** - PostgreSQL database setup guide
- **[03_greek-reference-data-api.md](./03_greek-reference-data-api.md)** - Greek reference data and API setup

### Development & Migration

- **[04_complete-migration-system.md](./04_complete-migration-system.md)** - Complete database migration system guide
  - 🚀 **NEW**: Intelligent migration system that replaces Alembic
  - ⚡ **Fast**: Migrations in seconds instead of hours
  - 🛡️ **Safe**: Automatic data preservation and transformation
  - 🧹 **Clean**: Automatic cleanup of temporary files

## 🎯 Quick Reference

### Database Operations

```powershell
# Complete database migration with data preservation
scripts\reset-database.ps1

# Create admin user
scripts\create-admin-user.ps1

# Complete setup (database + data + user)
scripts\complete-setup.ps1
```

### Development Workflow

```powershell
# Start all services
npm run dev:all

# Start individual services
npm run dev:client     # Frontend
npm run dev:api        # Backend API
npm run dev:auth       # Auth service
```

## 📖 Guide Categories

### 🔧 **Setup Guides**

Step-by-step instructions for initial system setup and configuration.

### 🏗️ **Development Guides**

Best practices, workflows, and tools for development.

### 🚀 **Deployment Guides**

Production deployment, CI/CD, and maintenance procedures.

### 🇬🇷 **Greek Compliance**

Greek business compliance, tax integration, and localization.

---

**Need help?** Check the specific guide for your use case, or refer to the main documentation in `/docs/`.
