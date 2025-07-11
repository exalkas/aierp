# 🔄 Shared Code Architecture - Enterprise Custom Development

## Overview

How to share common code (auth, UI, utilities) between standard SaaS and custom enterprise deployments while maintaining clean separation and git workflow.

---

## 🏗️ **MONOREPO ARCHITECTURE**

### **Project Structure**

```
erp-monorepo/
├── packages/
│   ├── shared/                    # Common code for all deployments
│   │   ├── auth/                  # Authentication system
│   │   ├── ui/                    # UI components library
│   │   ├── utils/                 # Utility functions
│   │   ├── api/                   # API client
│   │   ├── types/                 # TypeScript types
│   │   ├── config/                # Configuration management
│   │   ├── voice/                 # Voice command components
│   │   └── ai/                    # AI service integrations
│   │
│   ├── standard-modules/          # Standard SaaS modules
│   │   ├── dashboard/
│   │   ├── crm/
│   │   ├── erp/
│   │   ├── hotel-booking/
│   │   ├── table-booking/
│   │   ├── menu-management/
│   │   └── reports/
│   │
│   ├── ai-services/               # AI Infrastructure Services
│   │   ├── voice-service/         # Greek voice command processing
│   │   ├── ai-support-service/    # AI business assistant
│   │   └── shared-ai/             # Shared AI utilities
│   │
│   └── custom-modules/            # Enterprise custom modules
│       ├── pet-management/        # Pet shop modules
│       ├── pet-medical/
│       ├── pet-boarding/
│       ├── hospital-patient/      # Hospital modules
│       ├── hospital-medical/
│       └── restaurant-kitchen/    # Restaurant modules
│
├── apps/
│   ├── client/                    # Main business app (ERP/CRM)
│   │   ├── src/
│   │   ├── package.json
│   │   └── next.config.js
│   │
│   ├── admin/                     # Admin interface
│   │   ├── src/
│   │   ├── package.json
│   │   └── next.config.js
│   │
│   ├── user-support/              # Customer-facing support portal
│   │   ├── src/
│   │   ├── package.json
│   │   └── next.config.js
│   │
│   ├── staff-support/             # Internal support management
│   │   ├── src/
│   │   ├── package.json
│   │   └── next.config.js
│   │
│   └── setup/                     # Onboarding wizard
│       ├── src/
│       ├── package.json
│       └── next.config.js
│
├── package.json                   # Root package.json (npm workspaces)
└── services/                      # Backend services
    ├── api/                       # FastAPI backend
    ├── auth/                      # Authentication service
    ├── files/                     # File storage service
    └── integrations/              # Third-party integrations
```

### **Package.json Setup**

```json
// Root package.json (npm workspaces - no Lerna/NX needed)
{
  "name": "greek-erp-crm",
  "version": "1.0.0",
  "private": true,
  "workspaces": ["apps/*", "packages/*", "services/*"],
  "scripts": {
    "dev": "concurrently \"npm run dev:api\" \"npm run dev:client\"",
    "dev:client": "cd apps/client && npm run dev",
    "dev:admin": "cd apps/admin && npm run dev",
    "dev:user-support": "cd apps/user-support && npm run dev",
    "dev:staff-support": "cd apps/staff-support && npm run dev",
    "dev:setup": "cd apps/setup && npm run dev",
    "dev:api": "cd services/api && uvicorn main:app --reload",
    "build": "npm run build:packages && npm run build:apps",
    "build:packages": "npm run build --workspaces --if-present",
    "build:apps": "npm run build --workspace=apps/*",
    "test": "npm run test --workspaces"
  },
  "devDependencies": {
    "concurrently": "^8.0.0",
    "typescript": "^5.0.0"
  }
}
```

---

## 📦 **SHARED PACKAGES**

### **1. Shared Auth Package**

```typescript
// packages/shared/auth/src/index.ts
export { AuthProvider } from './AuthProvider';
export { useAuth } from './useAuth';
export { AuthGuard } from './AuthGuard';
export { LoginPage } from './LoginPage';
export type { User, AuthState } from './types';

// packages/shared/auth/package.json
{
  "name": "@erp/shared-auth",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dependencies": {
    "react": "^18.0.0",
    "react-router-dom": "^6.0.0"
  }
}
```

### **2. Shared UI Components**

```typescript
// packages/shared/ui/src/index.ts
export { Button } from './Button';
export { DataTable } from './DataTable';
export { Modal } from './Modal';
export { Form } from './Form';
export { Layout } from './Layout';
export { Navigation } from './Navigation';

// packages/shared/ui/package.json
{
  "name": "@erp/shared-ui",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dependencies": {
    "react": "^18.0.0",
    "@mui/material": "^5.0.0"
  }
}
```

### **3. Shared Utilities**

```typescript
// packages/shared/utils/src/index.ts
export { formatCurrency } from './formatCurrency';
export { validateEmail } from './validateEmail';
export { debounce } from './debounce';
export { ApiClient } from './ApiClient';
export { DateUtils } from './DateUtils';

// packages/shared/utils/package.json
{
  "name": "@erp/shared-utils",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts"
}
```

### **4. Shared Voice Components**

```typescript
// packages/shared/voice/src/index.ts
export { VoiceCommandButton } from './VoiceCommandButton';
export { VoiceRecorder } from './VoiceRecorder';
export { VoiceTranscription } from './VoiceTranscription';
export { GreekVoiceProcessor } from './GreekVoiceProcessor';
export { useVoiceCommand } from './useVoiceCommand';
export type { VoiceCommand, VoiceResult } from './types';

// packages/shared/voice/package.json
{
  "name": "@erp/shared-voice",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dependencies": {
    "react": "^18.0.0",
    "web-audio-api": "^1.0.0"
  }
}
```

### **5. Shared AI Components**

```typescript
// packages/shared/ai/src/index.ts
export { AIAssistant } from './AIAssistant';
export { BusinessInsights } from './BusinessInsights';
export { PredictiveAnalytics } from './PredictiveAnalytics';
export { GreekBusinessContext } from './GreekBusinessContext';
export { useAIAssistant } from './useAIAssistant';
export type { AIResponse, BusinessIntent } from './types';

// packages/shared/ai/package.json
{
  "name": "@erp/shared-ai",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dependencies": {
    "react": "^18.0.0",
    "@erp/shared-voice": "^1.0.0"
  }
}
```

---

## 🤖 **AI SERVICES ARCHITECTURE**

### **AI Services Structure**

```
ai-services/
├── voice-service/                 # Greek Voice Command Service
│   ├── src/
│   │   ├── models/                # Whisper models
│   │   ├── processors/            # Audio processing
│   │   ├── classifiers/           # Intent classification
│   │   └── api/                   # Voice API endpoints
│   ├── Dockerfile
│   ├── requirements.txt
│   └── package.json
│
├── ai-support-service/            # AI Business Assistant
│   ├── src/
│   │   ├── llm/                   # Language models
│   │   ├── analytics/             # Business analytics
│   │   ├── insights/              # Predictive insights
│   │   └── api/                   # AI API endpoints
│   ├── Dockerfile
│   ├── requirements.txt
│   └── package.json
│
└── shared-ai/                     # Shared AI Utilities
    ├── src/
    │   ├── greek-nlp/             # Greek NLP utilities
    │   ├── business-context/      # Greek business context
    │   ├── performance/           # Performance optimization
    │   └── security/              # AI security utilities
    └── package.json
```

### **Voice Service Implementation**

```python
# ai-services/voice-service/src/api/voice_api.py
from fastapi import FastAPI, UploadFile, File
from .processors.greek_voice_processor import GreekVoiceProcessor
from .classifiers.intent_classifier import GreekIntentClassifier

app = FastAPI()
voice_processor = GreekVoiceProcessor()
intent_classifier = GreekIntentClassifier()

@app.post("/voice/process")
async def process_voice_command(
    audio: UploadFile = File(...),
    company_id: str,
    user_context: dict
):
    """Process Greek voice command"""

    # Convert audio to text
    transcription = await voice_processor.transcribe(
        audio.file.read(),
        language="el"
    )

    # Classify business intent
    intent = await intent_classifier.classify(
        transcription,
        business_context=user_context
    )

    return {
        "transcription": transcription,
        "intent": intent,
        "confidence": intent.confidence
    }

# ai-services/voice-service/package.json
{
  "name": "@erp/voice-service",
  "version": "1.0.0",
  "dependencies": {
    "@erp/shared-ai": "^1.0.0"
  }
}
```

### **AI Support Service Implementation**

```python
# ai-services/ai-support-service/src/api/ai_api.py
from fastapi import FastAPI
from .analytics.business_analyzer import GreekBusinessAnalyzer
from .insights.predictive_engine import PredictiveEngine

app = FastAPI()
business_analyzer = GreekBusinessAnalyzer()
predictive_engine = PredictiveEngine()

@app.post("/ai/analyze")
async def analyze_business_question(
    question: str,
    company_id: str,
    business_data: dict
):
    """Analyze business question and provide insights"""

    # Understand the question
    intent = await business_analyzer.analyze_intent(question)

    # Generate insights
    insights = await business_analyzer.generate_insights(
        intent,
        business_data
    )

    # Predict future trends
    predictions = await predictive_engine.predict(
        intent,
        business_data
    )

    return {
        "intent": intent,
        "insights": insights,
        "predictions": predictions
    }

# ai-services/ai-support-service/package.json
{
  "name": "@erp/ai-support-service",
  "version": "1.0.0",
  "dependencies": {
    "@erp/shared-ai": "^1.0.0"
  }
}
```

### **Container Orchestration**

```yaml
# docker-compose.ai-services.yml
version: "3.8"

services:
  # Core ERP Services
  api:
    build: ./apps/saas
    environment:
      - AI_VOICE_SERVICE_URL=http://voice-service:8002
      - AI_SUPPORT_SERVICE_URL=http://ai-support-service:8003
    depends_on: [voice-service, ai-support-service]

  # AI Services
  voice-service:
    build: ./ai-services/voice-service
    ports: ["8002:8002"]
    environment:
      - WHISPER_MODEL=large-v3
      - CUDA_VISIBLE_DEVICES=0
      - GPU_MEMORY_FRACTION=0.6
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./ai-models:/app/models

  ai-support-service:
    build: ./ai-services/ai-support-service
    ports: ["8003:8003"]
    environment:
      - MODEL_NAME=llama-2-13b-greek-business
      - CUDA_VISIBLE_DEVICES=0
      - GPU_MEMORY_FRACTION=0.4
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on: [postgres, redis]

  # Database per company
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=company_manager
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

---

## 🎯 **STANDARD MODULES**

### **Standard Module Structure**

```typescript
// packages/standard-modules/crm/src/index.ts
import { AuthGuard } from '@erp/shared-auth';
import { DataTable, Button } from '@erp/shared-ui';
import { ApiClient } from '@erp/shared-utils';

export const CRMModule = {
  name: 'CRM',
  routes: [
    {
      path: '/crm',
      component: AuthGuard(CRMListPage),
      permissions: ['crm:read']
    },
    {
      path: '/crm/create',
      component: AuthGuard(CRMCreatePage),
      permissions: ['crm:write']
    }
  ],
  navigation: [
    { label: 'CRM', path: '/crm', icon: 'people' }
  ]
};

// packages/standard-modules/crm/package.json
{
  "name": "@erp/standard-crm",
  "version": "1.0.0",
  "dependencies": {
    "@erp/shared-auth": "^1.0.0",
    "@erp/shared-ui": "^1.0.0",
    "@erp/shared-utils": "^1.0.0"
  }
}
```

---

## 🐕 **CUSTOM MODULES**

### **Pet Management Module**

```typescript
// packages/custom-modules/pet-management/src/index.ts
import { AuthGuard } from '@erp/shared-auth';
import { DataTable, Button, Form } from '@erp/shared-ui';
import { ApiClient } from '@erp/shared-utils';

export const PetManagementModule = {
  name: 'Pet Management',
  routes: [
    {
      path: '/pet-management',
      component: AuthGuard(PetListPage),
      permissions: ['pets:read']
    },
    {
      path: '/pet-management/create',
      component: AuthGuard(PetCreatePage),
      permissions: ['pets:write']
    }
  ],
  navigation: [
    { label: 'Pet Management', path: '/pet-management', icon: 'pets' }
  ]
};

// Pet-specific components using shared UI
const PetListPage = () => {
  const apiClient = new ApiClient();

  return (
    <DataTable
      title="Pet Management"
      apiEndpoint="/api/pets"
      columns={[
        { field: 'name', header: 'Pet Name' },
        { field: 'breed', header: 'Breed' },
        { field: 'owner', header: 'Owner' },
        { field: 'lastVisit', header: 'Last Visit' }
      ]}
      actions={[
        <Button href="/pet-management/create">Add Pet</Button>
      ]}
    />
  );
};

// packages/custom-modules/pet-management/package.json
{
  "name": "@erp/custom-pet-management",
  "version": "1.0.0",
  "dependencies": {
    "@erp/shared-auth": "^1.0.0",
    "@erp/shared-ui": "^1.0.0",
    "@erp/shared-utils": "^1.0.0"
  }
}
```

---

## 🚀 **APPLICATION BUILDS**

### **Main Client App** (ERP/CRM Business Interface)

```typescript
// apps/client/src/app/page.tsx
import { useState } from 'react';
import { AuthProvider } from '@erp/shared-auth';
import { Button } from '@erp/shared-ui';
import { VoiceCommandButton } from '@erp/shared-voice';
import { AIAssistant } from '@erp/shared-ai';

// Main business modules
import { DashboardModule } from '@erp/standard-dashboard';
import { CRMModule } from '@erp/standard-crm';
import { ERPModule } from '@erp/standard-erp';
import { ReportsModule } from '@erp/standard-reports';

export default function ClientApp() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="flex justify-between items-center px-6 py-4">
            <h1 className="text-2xl font-bold text-gray-900">Greek ERP/CRM</h1>
            <div className="flex items-center space-x-4">
              <VoiceCommandButton />
              <AIAssistant />
            </div>
          </div>
        </header>

        <main>
          <DashboardModule />
          <CRMModule />
          <ERPModule />
          <ReportsModule />
        </main>
      </div>
    </AuthProvider>
  );
}

// apps/client/package.json
{
  "name": "@erp/client-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "15.0.0",
    "react": "^18.0.0",
    "@erp/shared-auth": "*",
    "@erp/shared-ui": "*",
    "@erp/shared-voice": "*",
    "@erp/shared-ai": "*",
    "@erp/standard-dashboard": "*",
    "@erp/standard-crm": "*",
    "@erp/standard-erp": "*",
    "@erp/standard-reports": "*"
  }
}
```

### **Admin App** (System Administration Interface)

```typescript
// apps/admin/src/app/page.tsx
import { AuthProvider } from '@erp/shared-auth';
import { AdminLayout } from '@erp/shared-ui';
import { AIAssistant } from '@erp/shared-ai';

// Admin-specific modules
import { UserManagementModule } from '@erp/admin-users';
import { SubscriptionModule } from '@erp/admin-subscriptions';
import { SystemConfigModule } from '@erp/admin-config';
import { AnalyticsModule } from '@erp/admin-analytics';

export default function AdminApp() {
  return (
    <AuthProvider>
      <AdminLayout>
        <div className="admin-dashboard">
          <header className="admin-header">
            <h1>System Administration</h1>
            <AIAssistant mode="admin" />
          </header>

          <nav className="admin-nav">
            <UserManagementModule />
            <SubscriptionModule />
            <SystemConfigModule />
            <AnalyticsModule />
          </nav>
        </div>
      </AdminLayout>
    </AuthProvider>
  );
}

// apps/admin/package.json
{
  "name": "@erp/admin-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev -p 3001",
    "build": "next build",
    "start": "next start -p 3001"
  },
  "dependencies": {
    "next": "15.0.0",
    "react": "^18.0.0",
    "@erp/shared-auth": "*",
    "@erp/shared-ui": "*",
    "@erp/shared-ai": "*",
    "@erp/admin-users": "*",
    "@erp/admin-subscriptions": "*",
    "@erp/admin-config": "*",
    "@erp/admin-analytics": "*"
  }
}
```

---

## 📝 **GIT WORKFLOW**

### **Branch Strategy**

```bash
# Main development branches
main                    # Production-ready code
develop                 # Development integration
feature/*               # New features
shared/*                # Shared package updates

# App-specific branches
app/client              # Client app specific features
app/admin               # Admin interface features
app/user-support        # Customer support portal features
app/staff-support       # Staff support management features
app/setup               # Setup wizard features

# Release branches
release/v1.0.0          # Platform release
release/client-v1.0.0   # Client app release
release/admin-v1.0.0    # Admin app release
```

### **Development Workflow**

#### **1. Standard Feature Development**

```bash
# Develop new standard feature
git checkout develop
git checkout -b feature/new-crm-feature

# Work on feature
git add .
git commit -m "Add new CRM feature"

# Merge back to develop
git checkout develop
git merge feature/new-crm-feature

# Eventually merge to main
git checkout main
git merge develop
```

#### **2. Customer Custom Development**

```bash
# Start customer development
git checkout main
git checkout -b customer/petshop

# Develop custom modules
mkdir -p packages/custom-modules/pet-management
# ... develop custom modules ...

# Commit customer-specific changes
git add .
git commit -m "Add pet management module for petshop customer"

# Build and deploy customer app
npm run build:customer petshop
```

#### **3. Updating Customer with Latest Shared Code**

```bash
# Customer wants latest shared improvements
git checkout customer/petshop

# Merge latest from main (this includes shared package updates)
git merge main

# Resolve any conflicts
# ... resolve conflicts ...

# Test and rebuild
npm run test:petshop
npm run build:customer petshop

# Deploy updated customer app
npm run deploy:customer petshop
```

### **Handling Conflicts**

```bash
# When merging main into customer branch
git checkout customer/petshop
git merge main

# If there are conflicts in shared packages
Auto-merging packages/shared/auth/src/AuthProvider.ts
CONFLICT (content): Merge conflict in packages/shared/auth/src/AuthProvider.ts

# Resolve conflicts manually
# Edit packages/shared/auth/src/AuthProvider.ts
# Keep both standard improvements and customer customizations

git add packages/shared/auth/src/AuthProvider.ts
git commit -m "Resolve merge conflicts with main"
```

---

## 🔧 **BUILD SCRIPTS**

### **Build Commands** (npm workspaces)

```bash
# Install dependencies for all workspaces
npm install

# Build all packages
npm run build

# Build specific package
npm run build --workspace=packages/shared-auth

# Development servers (parallel)
npm run dev  # Starts both API and client

# Individual development servers
npm run dev:client   # Main business app (port 3000)
npm run dev:admin    # Admin interface (port 3001)
npm run dev:user-support   # Customer support portal (port 3002)
npm run dev:staff-support  # Staff support management (port 3003)
npm run dev:setup    # Setup wizard (port 3004)

# Test all workspaces
npm run test

# Test specific workspace
npm run test --workspace=apps/client
```

---

## 🚀 **DEPLOYMENT STRATEGY**

### **CI/CD Pipeline**

```yaml
# .github/workflows/deploy.yml
name: Deploy Greek ERP/CRM Platform

on:
  push:
    branches: [main, "app/*"]

jobs:
  deploy-client:
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/app/client'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Build client app
        run: npm run build --workspace=apps/client
      - name: Deploy to app.alkas.com
        run: ./scripts/deploy-client.sh

  deploy-admin:
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/app/admin'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Build admin app
        run: npm run build --workspace=apps/admin
      - name: Deploy to admin.alkas.com
        run: ./scripts/deploy-admin.sh

  deploy-user-support:
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/app/user-support'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Build user support app
        run: npm run build --workspace=apps/user-support
      - name: Deploy to support.alkas.com
        run: ./scripts/deploy-user-support.sh

  deploy-staff-support:
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/app/staff-support'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Build staff support app
        run: npm run build --workspace=apps/staff-support
      - name: Deploy to admin.alkas.com/support
        run: ./scripts/deploy-staff-support.sh

  deploy-api:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy FastAPI backend
        run: ./scripts/deploy-api.sh
```

---

## 🎯 **BENEFITS**

### **✅ Code Reuse:**

- **Shared packages** used by all apps
- **Auth, UI, Utils** consistent across all deployments
- **Standard modules** reused in custom apps
- **No code duplication**

### **✅ Maintainability:**

- **Single source of truth** for shared code
- **Easy updates** to shared packages
- **Consistent UI/UX** across all apps
- **Clear separation** between standard and custom

### **✅ Development Efficiency:**

- **Monorepo tooling** (NX, Lerna)
- **Hot reloading** for development
- **Parallel builds** for different apps
- **Shared dependencies** management

### **✅ Git Management:**

- **App-specific branches** for focused development
- **Regular merges** from main to get updates
- **Conflict resolution** for shared code changes
- **Independent deployments** per application

### **✅ AI Integration:**

- **Shared AI components** for voice commands and business insights
- **Containerized AI services** with GPU acceleration
- **Voice command integration** across all applications
- **Consistent AI experience** throughout the platform

This architecture gives you the **best of both worlds**: shared code benefits with modern monorepo tooling and cutting-edge AI integration! 🚀
