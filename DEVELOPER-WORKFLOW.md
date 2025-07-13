# 🚀 Developer Workflow - Hybrid Poetry + npm Workspace

**Complete guide for developing in the Greek ERP/CRM hybrid monorepo**

## 🏗️ **Architecture Overview**

This project uses a **modern hybrid monorepo** that combines the best of both JavaScript and Python ecosystems:

```
greek-erp-crm/
├── 📦 npm workspaces          # JavaScript/TypeScript ecosystem
│   ├── apps/*                # Frontend applications
│   ├── packages/shared/*      # Shared UI components
│   ├── packages/standard-modules/*  # Standard modules
│   └── package.json           # npm workspace config
├── 🐍 Poetry workspace        # Python ecosystem
│   ├── services/*             # Backend services
│   ├── packages/ai-services/* # AI services
│   ├── pyproject.toml         # Poetry workspace config
│   └── poetry.lock            # Unified dependency lock
└── 🔄 Unified orchestration   # Single command interface
    └── package.json           # Cross-ecosystem scripts
```

### **🎯 Key Benefits:**

- ✅ **Single Poetry environment** - Replaces 6 separate virtual environments
- ✅ **Shared dependencies** - FastAPI, SQLAlchemy, PyJWT installed once
- ✅ **Unified commands** - npm scripts orchestrate both ecosystems
- ✅ **Faster development** - No context switching between environments
- ✅ **Consistent tooling** - Shared linting, formatting, testing
- ✅ **Better performance** - Reduced memory usage and faster installs

## 🚀 **Daily Workflow**

### **1. Environment Setup (One-time)**

```bash
# Clone repository
git clone <repo-url>
cd greek-erp-crm

# Install Poetry (if not installed)
pip install poetry

# Install all dependencies
npm run install:both

# Verify setup
poetry env info
npm list --depth=0
```

### **2. Development Commands**

#### **🔄 Start All Services**

```bash
# Start everything (frontend + backend)
npm run dev:all

# Services will be available at:
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

#### **📦 Frontend Development**

```bash
# Start all frontend apps
npm run dev:js

# Individual frontend apps
npm run dev:client         # Main app (3000)
npm run dev:admin          # Admin (3001)
npm run dev:user-support   # Support (3002)
npm run dev:staff-support  # Staff (3003)
npm run dev:setup          # Setup (3004)

# Frontend package development
cd packages/shared/ui
npm run dev                # Component library
```

#### **🐍 Backend Development**

```bash
# Start all backend services
npm run dev:python

# Individual backend services (via Poetry)
npm run dev:api            # Main API (8000)
npm run dev:auth           # Auth service (8001)
npm run dev:files          # File service (8002)
npm run dev:integrations   # AADE integration (8003)
npm run dev:ai-support     # AI support (8004)
npm run dev:voice          # Voice AI (8005)

# Direct Poetry commands
poetry run uvicorn services.api.main:app --reload
poetry run python -m services.auth.main
```

### **3. Code Quality & Testing**

#### **🧹 Formatting & Linting**

```bash
# Format everything (JS + Python)
npm run format

# Lint everything (JS + Python)
npm run lint

# Individual ecosystems
npm run format:js          # JavaScript/TypeScript
npm run format:python      # Python (Black + isort)
npm run lint:js            # ESLint + TypeScript
npm run lint:python        # Flake8 + MyPy
```

#### **🧪 Testing**

```bash
# Run all tests (JS + Python)
npm run test

# Individual test suites
npm run test:js            # Jest + React Testing Library
npm run test:python        # pytest

# Python testing with Poetry
poetry run pytest services/api/tests/
poetry run pytest --cov=services/api
```

### **4. Dependency Management**

#### **📦 JavaScript Dependencies**

```bash
# Add to workspace root
npm install --save-dev typescript

# Add to specific app
npm install --workspace=apps/client react-query

# Add to shared package
npm install --workspace=packages/shared/ui lucide-react
```

#### **🐍 Python Dependencies**

```bash
# Add shared dependency (available to all services)
poetry add fastapi

# Add to specific service pyproject.toml
cd services/api
poetry add requests

# Add development dependency
poetry add --group dev pytest-cov

# Update dependencies
poetry update
```

### **5. Environment Variables**

```bash
# Root .env (shared across services)
DATABASE_URL=postgresql://user:pass@localhost/db
JWT_SECRET=your-secret-here

# Service-specific .env files
services/api/.env
services/auth/.env
```

## 🔧 **Advanced Workflows**

### **🏗️ Adding New Services**

#### **Frontend App**

```bash
# Create new Next.js app
cd apps/
npx create-next-app@latest new-app --typescript --tailwind

# Add to npm workspaces (package.json)
"workspaces": [
  "apps/*",
  "apps/new-app"  # Auto-detected
]

# Install dependencies
npm run install:js
```

#### **Backend Service**

```bash
# Create new service directory
mkdir services/new-service
cd services/new-service

# Create pyproject.toml
cat > pyproject.toml << EOF
[tool.poetry]
name = "new-service"
version = "0.1.0"
description = "New Greek ERP service"

[tool.poetry.dependencies]
python = "^3.11"
# Service-specific dependencies
special-package = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
EOF

# Install dependencies
poetry install
```

### **🔍 Debugging**

#### **Backend Debugging**

```bash
# Debug with Poetry environment
poetry run python -m debugpy --listen 5678 --wait-for-client services/api/main.py

# VS Code launch.json
{
  "name": "Python: FastAPI",
  "type": "python",
  "request": "attach",
  "connect": {"host": "localhost", "port": 5678},
  "pathMappings": [{"localRoot": "${workspaceFolder}", "remoteRoot": "."}]
}
```

#### **Environment Inspection**

```bash
# Check Poetry environment
poetry env info
poetry show                # List all packages
poetry show fastapi        # Show specific package

# Check npm workspaces
npm list --workspaces
npm run env               # Environment variables
```

### **🚀 Production Builds**

```bash
# Build everything
npm run build

# Individual builds
npm run build:apps         # All frontend apps
poetry run python -m build # Python packages (if needed)
```

### **🧰 Troubleshooting**

#### **Common Issues**

| Issue                        | Solution                                 |
| ---------------------------- | ---------------------------------------- |
| `poetry not found`           | `pip install poetry`, restart terminal   |
| `npm workspaces error`       | Delete `node_modules`, run `npm install` |
| `Poetry dependency conflict` | `poetry lock --no-update`                |
| `Port already in use`        | `npm run dev:api -- --port 8001`         |
| `Python import errors`       | `poetry install`, check PYTHONPATH       |

#### **Reset Environment**

```bash
# Reset Poetry environment
poetry env remove python
poetry install

# Reset npm workspaces
rm -rf node_modules package-lock.json
npm install

# Complete reset
npm run install:both
```

## 📊 **Monitoring & Performance**

### **Development Metrics**

```bash
# Check Poetry environment size
poetry env info

# Check dependency tree
poetry show --tree

# npm workspace analysis
npm list --depth=1
npm audit
```

### **Service Health Checks**

```bash
# API health endpoints
curl http://localhost:8000/health    # Main API
curl http://localhost:8001/health    # Auth service
curl http://localhost:8002/health    # Files service

# Database connection
poetry run python -c "from services.api.core.database import engine; print('DB OK')"
```

## 🎯 **Best Practices**

### **✅ Do's**

- ✅ Use `npm run install:both` for setup
- ✅ Use `npm run dev:all` for development
- ✅ Add shared Python deps to root `pyproject.toml`
- ✅ Add service-specific deps to service `pyproject.toml`
- ✅ Use Poetry for all Python commands
- ✅ Keep frontends in npm workspaces
- ✅ Run linting before commits
- ✅ Use the unified testing commands

### **❌ Don'ts**

- ❌ Don't create individual Python venvs
- ❌ Don't install Python packages with pip directly
- ❌ Don't mix npm and Poetry for same dependency
- ❌ Don't skip the unified linting/formatting
- ❌ Don't commit without running tests
- ❌ Don't modify Poetry files manually (use `poetry add`)

---

## 🚀 **Quick Reference**

```bash
# Setup
npm run install:both

# Development
npm run dev:all

# Individual services
npm run dev:api
npm run dev:client

# Code quality
npm run format
npm run lint
npm run test

# Dependency management
poetry add package-name
npm install --workspace=apps/client package-name

# Environment
poetry env info
poetry show
```

**🎉 Happy coding in your hybrid monorepo!**
