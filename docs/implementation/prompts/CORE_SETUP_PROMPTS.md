# 🚀 Core Setup Prompts - Monorepo SaaS + Enterprise Architecture

## Overview

These prompts implement the **SHARED_CODE_ARCHITECTURE.md** with monorepo structure for standard SaaS + enterprise custom deployments.

---

## PROMPT 1.1: Initialize Complete Project Structure

**CONTEXT**: Create monorepo structure with 4 applications and core packages matching the roadmap.

**EXECUTE THIS:**

```powershell
# Create Greek ERP/CRM monorepo structure (Windows)
# We're already in the project root, so create structure here

# Create 4 main applications
New-Item -ItemType Directory -Path "apps\client" -Force
New-Item -ItemType Directory -Path "apps\admin" -Force
New-Item -ItemType Directory -Path "apps\user-support" -Force
New-Item -ItemType Directory -Path "apps\staff-support" -Force
New-Item -ItemType Directory -Path "apps\setup" -Force

# Create core packages
New-Item -ItemType Directory -Path "packages\authorization" -Force
New-Item -ItemType Directory -Path "packages\data-engine" -Force
New-Item -ItemType Directory -Path "packages\plugin-system" -Force
New-Item -ItemType Directory -Path "packages\dynamic-entities" -Force
New-Item -ItemType Directory -Path "packages\greek-compliance" -Force
New-Item -ItemType Directory -Path "packages\shared-ui" -Force
New-Item -ItemType Directory -Path "packages\shared-types" -Force

# Create custom modules directory structure
# This supports the plugin-based architecture for Greek ERP customization
New-Item -ItemType Directory -Path "modules\core" -Force         # Core business modules
New-Item -ItemType Directory -Path "modules\industry" -Force     # Industry-specific modules
New-Item -ItemType Directory -Path "modules\third-party" -Force  # Third-party integrations
New-Item -ItemType Directory -Path "modules\custom" -Force       # Customer-specific modules

# Create industry-specific module folders for Greek market
New-Item -ItemType Directory -Path "modules\industry\shipping" -Force      # Maritime/shipping companies
New-Item -ItemType Directory -Path "modules\industry\tourism" -Force       # Hotels, travel agencies
New-Item -ItemType Directory -Path "modules\industry\retail" -Force        # Retail chains, shops
New-Item -ItemType Directory -Path "modules\industry\construction" -Force  # Construction companies
New-Item -ItemType Directory -Path "modules\industry\agriculture" -Force   # Farming, food production
New-Item -ItemType Directory -Path "modules\industry\manufacturing" -Force # Manufacturing companies
New-Item -ItemType Directory -Path "modules\industry\services" -Force      # Service providers

# Create core business modules (loaded by default)
New-Item -ItemType Directory -Path "modules\core\crm" -Force         # Customer relationship management
New-Item -ItemType Directory -Path "modules\core\erp" -Force         # Enterprise resource planning
New-Item -ItemType Directory -Path "modules\core\invoicing" -Force   # Invoicing and billing
New-Item -ItemType Directory -Path "modules\core\inventory" -Force   # Inventory management
New-Item -ItemType Directory -Path "modules\core\accounting" -Force  # Financial accounting
New-Item -ItemType Directory -Path "modules\core\reporting" -Force   # Report generation
New-Item -ItemType Directory -Path "modules\core\analytics" -Force   # Business analytics

# Create services
New-Item -ItemType Directory -Path "services\api" -Force
New-Item -ItemType Directory -Path "services\auth" -Force
New-Item -ItemType Directory -Path "services\files" -Force
New-Item -ItemType Directory -Path "services\integrations" -Force

# Create additional directories
New-Item -ItemType Directory -Path "scripts" -Force

# Create root package.json
@"
{
  "name": "greek-erp-crm",
  "version": "1.0.0",
  "private": true,
  "workspaces": ["apps/*", "packages/*", "services/*", "modules/*/*"],
  "scripts": {
    "dev": "concurrently \"npm run dev:api\" \"npm run dev:client\"",
    "dev:client": "cd apps/client && npm run dev",
    "dev:admin": "cd apps/admin && npm run dev",
    "dev:user-support": "cd apps/user-support && npm run dev",
    "dev:staff-support": "cd apps/staff-support && npm run dev",
    "dev:setup": "cd apps/setup && npm run dev",
    "dev:api": "cd services/api && uvicorn main:app --reload",
    "build": "npm run build:packages && npm run build:modules && npm run build:apps",
    "build:packages": "npm run build --workspaces --if-present",
    "build:modules": "npm run build --workspaces --if-present",
    "build:apps": "npm run build:client && npm run build:admin && npm run build:user-support && npm run build:staff-support && npm run build:setup",
    "build:client": "cd apps/client && npm run build",
    "build:admin": "cd apps/admin && npm run build",
    "build:user-support": "cd apps/user-support && npm run build",
    "build:staff-support": "cd apps/staff-support && npm run build",
    "build:setup": "cd apps/setup && npm run build",
    "test": "npm run test --workspaces",
    "deploy:all": "./scripts/deploy-all.sh",
    "setup:db": "cd services/api && python -m alembic upgrade head",
    "create:module": "./scripts/create-module.sh",
    "list:modules": "find modules -name package.json -exec dirname {} \\; | sort",
    "install:modules": "npm install --workspaces"
  },
  "devDependencies": {
    "concurrently": "^8.0.0",
    "typescript": "^5.0.0",
    "lerna": "^8.0.0"
  }
}
"@ | Out-File -FilePath "package.json" -Encoding UTF8

# Create deployment script
@"
#!/bin/bash
echo "Building and deploying all applications..."

# Build all packages first
npm run build:packages

# Build and deploy each app
echo "Building Client App..."
npm run build:client

echo "Building Admin App..."
npm run build:admin

echo "Building User Support App..."
npm run build:user-support

echo "Building Staff Support App..."
npm run build:staff-support

echo "Building Setup App..."
npm run build:setup

echo "All applications built successfully!"
"@ | Out-File -FilePath "scripts/deploy-all.sh" -Encoding UTF8

# Create app initialization script
@"
#!/bin/bash
APP_NAME=$1

if [ -z "$APP_NAME" ]; then
    echo "Usage: ./create-app.sh <app-name>"
    exit 1
fi

echo "Creating Next.js app: $APP_NAME..."
cd apps/$APP_NAME
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

echo "App $APP_NAME created successfully!"
"@ | Out-File -FilePath "scripts/create-app.sh" -Encoding UTF8

# Create module initialization script
@"
#!/bin/bash
MODULE_TYPE=$1
MODULE_NAME=$2

if [ -z "$MODULE_TYPE" ] || [ -z "$MODULE_NAME" ]; then
    echo "Usage: ./create-module.sh <module-type> <module-name>"
    echo "Module types: core, industry, third-party, custom"
    echo "Example: ./create-module.sh industry hotel-management"
    exit 1
fi

MODULE_PATH="modules/$MODULE_TYPE/$MODULE_NAME"

if [ -d "$MODULE_PATH" ]; then
    echo "Module $MODULE_PATH already exists!"
    exit 1
fi

echo "Creating module: $MODULE_PATH..."
mkdir -p "$MODULE_PATH/src"
mkdir -p "$MODULE_PATH/types"
mkdir -p "$MODULE_PATH/components"
mkdir -p "$MODULE_PATH/hooks"
mkdir -p "$MODULE_PATH/utils"

# Create package.json for the module
cat > "$MODULE_PATH/package.json" << EOL
{
  "name": "@erp/module-$MODULE_NAME",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "test": "jest"
  },
  "dependencies": {
    "@erp/shared-types": "workspace:*",
    "@erp/shared-ui": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0",
    "jest": "^29.0.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  }
}
EOL

# Create TypeScript config
cat > "$MODULE_PATH/tsconfig.json" << EOL
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["dist", "node_modules"]
}
EOL

# Create main index file
cat > "$MODULE_PATH/src/index.ts" << EOL
// Module: $MODULE_NAME
// Type: $MODULE_TYPE
// Generated: $(date)

export * from './types';
export * from './components';
export * from './hooks';
export * from './utils';
EOL

# Create types file
cat > "$MODULE_PATH/src/types.ts" << EOL
// Types for $MODULE_NAME module
export interface ${MODULE_NAME^}Config {
  enabled: boolean;
  version: string;
  settings: Record<string, any>;
}

export interface ${MODULE_NAME^}State {
  initialized: boolean;
  loading: boolean;
  error: string | null;
}
EOL

# Create components index
cat > "$MODULE_PATH/src/components/index.ts" << EOL
// Components for $MODULE_NAME module
// Export your React components here
EOL

# Create hooks index
cat > "$MODULE_PATH/src/hooks/index.ts" << EOL
// Hooks for $MODULE_NAME module
// Export your custom hooks here
EOL

# Create utils index
cat > "$MODULE_PATH/src/utils/index.ts" << EOL
// Utilities for $MODULE_NAME module
// Export your utility functions here
EOL

# Create README
cat > "$MODULE_PATH/README.md" << EOL
# $MODULE_NAME Module

## Overview
This is a $MODULE_TYPE module for the Greek ERP/CRM system.

## Installation
This module is part of the monorepo workspace and will be automatically installed.

## Usage
\`\`\`typescript
import { /* your exports */ } from '@erp/module-$MODULE_NAME';
\`\`\`

## Configuration
Module configuration options and setup instructions.

## Development
- \`npm run dev\` - Development mode with file watching
- \`npm run build\` - Build the module
- \`npm run test\` - Run tests
EOL

echo "Module $MODULE_NAME created successfully at $MODULE_PATH!"
echo "Don't forget to run 'npm install' to install dependencies."
"@ | Out-File -FilePath "scripts/create-module.sh" -Encoding UTF8
```

**ACCEPTANCE CRITERIA:**
✅ All 5 applications created (client, admin, user-support, staff-support, setup)
✅ Core packages directory structure ready
✅ Custom modules directory with industry-specific and core business modules
✅ Services directory with API, auth, files, integrations
✅ Build scripts for all applications, packages, and modules
✅ Root package.json with workspace configuration including modules

---

## PROMPT 1.2: Shared Auth Package with Storage & AI API Quota Management

**CONTEXT**: Build shared authentication system with storage limitations and AI API expense management.

**EXECUTE THIS:**

```typescript
// packages/shared/auth/src/index.ts
export interface QuotaLimits {
  storage: {
    maxFileSizeBytes: number;        // Max single file size
    maxTotalStorageBytes: number;    // Total storage across all files
    maxFilesPerType: {
      images: number;
      documents: number;
      videos: number;
      attachments: number;
    };
    retentionDays: number;           // File retention period
  };
  ai: {
    monthlyBudgetEuros: number;      // Monthly AI API budget
    dailyBudgetEuros: number;        // Daily AI API budget
    maxRequestsPerMinute: number;    // Rate limiting
    maxRequestsPerHour: number;      // Rate limiting
    enabledServices: string[];       // Which AI services are enabled
    costPerService: {
      chatCompletion: number;        // Cost per chat completion
      textAnalysis: number;          // Cost per text analysis
      documentOcr: number;           // Cost per OCR operation
      translation: number;           // Cost per translation
      voiceTranscription: number;    // Cost per voice transcription
    };
  };
}

export interface UsageStats {
  storage: {
    currentUsageBytes: number;
    filesCount: number;
    filesByType: {
      images: number;
      documents: number;
      videos: number;
      attachments: number;
    };
    lastUpdated: Date;
  };
  ai: {
    currentMonthSpendEuros: number;
    currentDaySpendEuros: number;
    requestsToday: number;
    requestsThisHour: number;
    lastRequestTime: Date;
    serviceUsage: {
      chatCompletion: { count: number; cost: number };
      textAnalysis: { count: number; cost: number };
      documentOcr: { count: number; cost: number };
      translation: { count: number; cost: number };
      voiceTranscription: { count: number; cost: number };
    };
  };
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  permissions: string[];
  customerId?: string;
  subscription?: string;
  quotaLimits: QuotaLimits;
  currentUsage: UsageStats;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  quotaWarnings: string[];
}

export interface AuthContextType {
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkPermission: (permission: string) => boolean;
  canAccessModule: (moduleId: string) => boolean;
  // Storage quota methods
  canUploadFile: (fileSizeBytes: number, fileType: string) => { allowed: boolean; reason?: string };
  updateStorageUsage: (fileSizeBytes: number, fileType: string) => void;
  // AI API quota methods
  canUseAIService: (service: string, estimatedCost: number) => { allowed: boolean; reason?: string };
  recordAIUsage: (service: string, cost: number) => void;
  getQuotaStatus: () => { storage: number; ai: number }; // Returns percentage used
}

// Authentication Provider
import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
    quotaWarnings: []
  });

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) throw new Error('Login failed');

      const user = await response.json();
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'LOGIN_ERROR', payload: error.message });
    }
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
  };

  const checkPermission = (permission: string): boolean => {
    return state.user?.permissions.includes(permission) || false;
  };

  const canAccessModule = (moduleId: string): boolean => {
    if (!state.user) return false;

    // Check subscription-based access
    const subscription = state.user.subscription;
    if (!subscription) return false;

    const subscriptionModules = getModulesForSubscription(subscription);
    return subscriptionModules.includes(moduleId);
  };

  const canUploadFile = (fileSizeBytes: number, fileType: string): { allowed: boolean; reason?: string } => {
    if (!state.user) return { allowed: false, reason: 'User not authenticated' };

    const { quotaLimits, currentUsage } = state.user;

    // Check single file size limit
    if (fileSizeBytes > quotaLimits.storage.maxFileSizeBytes) {
      return {
        allowed: false,
        reason: `File size exceeds limit of ${formatBytes(quotaLimits.storage.maxFileSizeBytes)}`
      };
    }

    // Check total storage limit
    if (currentUsage.storage.currentUsageBytes + fileSizeBytes > quotaLimits.storage.maxTotalStorageBytes) {
      return {
        allowed: false,
        reason: `Would exceed total storage limit of ${formatBytes(quotaLimits.storage.maxTotalStorageBytes)}`
      };
    }

    // Check file type limits
    const typeKey = fileType as keyof typeof quotaLimits.storage.maxFilesPerType;
    if (quotaLimits.storage.maxFilesPerType[typeKey] &&
        currentUsage.storage.filesByType[typeKey] >= quotaLimits.storage.maxFilesPerType[typeKey]) {
      return {
        allowed: false,
        reason: `Maximum ${fileType} files limit reached (${quotaLimits.storage.maxFilesPerType[typeKey]})`
      };
    }

    return { allowed: true };
  };

  const updateStorageUsage = (fileSizeBytes: number, fileType: string) => {
    if (!state.user) return;

    const updatedUser = {
      ...state.user,
      currentUsage: {
        ...state.user.currentUsage,
        storage: {
          ...state.user.currentUsage.storage,
          currentUsageBytes: state.user.currentUsage.storage.currentUsageBytes + fileSizeBytes,
          filesCount: state.user.currentUsage.storage.filesCount + 1,
          filesByType: {
            ...state.user.currentUsage.storage.filesByType,
            [fileType]: (state.user.currentUsage.storage.filesByType[fileType] || 0) + 1
          },
          lastUpdated: new Date()
        }
      }
    };

    dispatch({ type: 'UPDATE_USER', payload: updatedUser });
  };

  const canUseAIService = (service: string, estimatedCost: number): { allowed: boolean; reason?: string } => {
    if (!state.user) return { allowed: false, reason: 'User not authenticated' };

    const { quotaLimits, currentUsage } = state.user;

    // Check if service is enabled
    if (!quotaLimits.ai.enabledServices.includes(service)) {
      return { allowed: false, reason: `AI service '${service}' not enabled in your subscription` };
    }

    // Check monthly budget
    if (currentUsage.ai.currentMonthSpendEuros + estimatedCost > quotaLimits.ai.monthlyBudgetEuros) {
      return {
        allowed: false,
        reason: `Would exceed monthly AI budget of €${quotaLimits.ai.monthlyBudgetEuros}`
      };
    }

    // Check daily budget
    if (currentUsage.ai.currentDaySpendEuros + estimatedCost > quotaLimits.ai.dailyBudgetEuros) {
      return {
        allowed: false,
        reason: `Would exceed daily AI budget of €${quotaLimits.ai.dailyBudgetEuros}`
      };
    }

    // Check rate limits
    if (currentUsage.ai.requestsThisHour >= quotaLimits.ai.maxRequestsPerHour) {
      return { allowed: false, reason: 'Hourly AI request limit reached' };
    }

    const now = new Date();
    const minuteAgo = new Date(now.getTime() - 60000);
    if (currentUsage.ai.lastRequestTime > minuteAgo &&
        currentUsage.ai.requestsToday >= quotaLimits.ai.maxRequestsPerMinute) {
      return { allowed: false, reason: 'Per-minute AI request limit reached' };
    }

    return { allowed: true };
  };

  const recordAIUsage = (service: string, cost: number) => {
    if (!state.user) return;

    const updatedUser = {
      ...state.user,
      currentUsage: {
        ...state.user.currentUsage,
        ai: {
          ...state.user.currentUsage.ai,
          currentMonthSpendEuros: state.user.currentUsage.ai.currentMonthSpendEuros + cost,
          currentDaySpendEuros: state.user.currentUsage.ai.currentDaySpendEuros + cost,
          requestsToday: state.user.currentUsage.ai.requestsToday + 1,
          requestsThisHour: state.user.currentUsage.ai.requestsThisHour + 1,
          lastRequestTime: new Date(),
          serviceUsage: {
            ...state.user.currentUsage.ai.serviceUsage,
            [service]: {
              count: (state.user.currentUsage.ai.serviceUsage[service]?.count || 0) + 1,
              cost: (state.user.currentUsage.ai.serviceUsage[service]?.cost || 0) + cost
            }
          }
        }
      }
    };

    dispatch({ type: 'UPDATE_USER', payload: updatedUser });
  };

  const getQuotaStatus = () => {
    if (!state.user) return { storage: 0, ai: 0 };

    const storagePercentage = (state.user.currentUsage.storage.currentUsageBytes /
                               state.user.quotaLimits.storage.maxTotalStorageBytes) * 100;

    const aiPercentage = (state.user.currentUsage.ai.currentMonthSpendEuros /
                          state.user.quotaLimits.ai.monthlyBudgetEuros) * 100;

    return {
      storage: Math.min(storagePercentage, 100),
      ai: Math.min(aiPercentage, 100)
    };
  };

  // Monitor quota warnings
  useEffect(() => {
    if (!state.user) return;

    const warnings: string[] = [];
    const quotaStatus = getQuotaStatus();

    if (quotaStatus.storage > 80) {
      warnings.push(`Storage usage at ${quotaStatus.storage.toFixed(1)}%`);
    }

    if (quotaStatus.ai > 80) {
      warnings.push(`AI budget usage at ${quotaStatus.ai.toFixed(1)}%`);
    }

    if (warnings.length > 0) {
      dispatch({ type: 'SET_QUOTA_WARNINGS', payload: warnings });
    }
  }, [state.user]);

  return (
    <AuthContext.Provider value={{
      state,
      login,
      logout,
      checkPermission,
      canAccessModule,
      canUploadFile,
      updateStorageUsage,
      canUseAIService,
      recordAIUsage,
      getQuotaStatus
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// Auth reducer
const authReducer = (state: AuthState, action: any): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, loading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { ...state, user: action.payload, isAuthenticated: true, loading: false };
    case 'LOGIN_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'LOGOUT':
      return { ...state, user: null, isAuthenticated: false, quotaWarnings: [] };
    case 'UPDATE_USER':
      return { ...state, user: action.payload };
    case 'SET_QUOTA_WARNINGS':
      return { ...state, quotaWarnings: action.payload };
    default:
      return state;
  }
};

// Route guard component with quota checks
export const AuthGuard: React.FC<{
  children: React.ReactNode;
  permission?: string;
  moduleId?: string;
  requiresAI?: boolean;
  requiresStorage?: boolean;
}> = ({ children, permission, moduleId, requiresAI, requiresStorage }) => {
  const { state, checkPermission, canAccessModule, getQuotaStatus } = useAuth();

  if (!state.isAuthenticated) {
    return <div>Please log in</div>;
  }

  if (permission && !checkPermission(permission)) {
    return <div>Access denied</div>;
  }

  if (moduleId && !canAccessModule(moduleId)) {
    return <div>Module not available in your subscription</div>;
  }

  // Check quota limits
  const quotaStatus = getQuotaStatus();

  if (requiresAI && quotaStatus.ai >= 100) {
    return <div>AI budget exceeded. Please upgrade your subscription.</div>;
  }

  if (requiresStorage && quotaStatus.storage >= 100) {
    return <div>Storage limit exceeded. Please upgrade your subscription.</div>;
  }

  return <>{children}</>;
};

// Subscription configuration with storage and AI limits
const getSubscriptionConfig = (subscription: string): { modules: string[]; quotaLimits: QuotaLimits } => {
  const subscriptionConfigs = {
    'basic-crm': {
      modules: ['dashboard', 'crm', 'reports'],
      quotaLimits: {
        storage: {
          maxFileSizeBytes: 10 * 1024 * 1024,      // 10MB
          maxTotalStorageBytes: 1024 * 1024 * 1024, // 1GB
          maxFilesPerType: { images: 100, documents: 50, videos: 10, attachments: 100 },
          retentionDays: 365
        },
        ai: {
          monthlyBudgetEuros: 20,
          dailyBudgetEuros: 2,
          maxRequestsPerMinute: 10,
          maxRequestsPerHour: 100,
          enabledServices: ['chatCompletion', 'textAnalysis'],
          costPerService: {
            chatCompletion: 0.02,
            textAnalysis: 0.01,
            documentOcr: 0.05,
            translation: 0.03,
            voiceTranscription: 0.04
          }
        }
      }
    },
    'business-suite': {
      modules: ['dashboard', 'crm', 'erp', 'invoicing', 'reports'],
      quotaLimits: {
        storage: {
          maxFileSizeBytes: 50 * 1024 * 1024,       // 50MB
          maxTotalStorageBytes: 10 * 1024 * 1024 * 1024, // 10GB
          maxFilesPerType: { images: 500, documents: 200, videos: 50, attachments: 500 },
          retentionDays: 1095 // 3 years
        },
        ai: {
          monthlyBudgetEuros: 100,
          dailyBudgetEuros: 10,
          maxRequestsPerMinute: 30,
          maxRequestsPerHour: 500,
          enabledServices: ['chatCompletion', 'textAnalysis', 'documentOcr', 'translation'],
          costPerService: {
            chatCompletion: 0.015,
            textAnalysis: 0.008,
            documentOcr: 0.04,
            translation: 0.025,
            voiceTranscription: 0.03
          }
        }
      }
    },
    'enterprise': {
      modules: ['dashboard', 'crm', 'erp', 'invoicing', 'reports', 'analytics', 'automation'],
      quotaLimits: {
        storage: {
          maxFileSizeBytes: 200 * 1024 * 1024,      // 200MB
          maxTotalStorageBytes: 100 * 1024 * 1024 * 1024, // 100GB
          maxFilesPerType: { images: 2000, documents: 1000, videos: 200, attachments: 2000 },
          retentionDays: 2555 // 7 years
        },
        ai: {
          monthlyBudgetEuros: 500,
          dailyBudgetEuros: 50,
          maxRequestsPerMinute: 100,
          maxRequestsPerHour: 2000,
          enabledServices: ['chatCompletion', 'textAnalysis', 'documentOcr', 'translation', 'voiceTranscription'],
          costPerService: {
            chatCompletion: 0.01,
            textAnalysis: 0.005,
            documentOcr: 0.03,
            translation: 0.02,
            voiceTranscription: 0.025
          }
        }
      }
    }
  };

  return subscriptionConfigs[subscription] || subscriptionConfigs['basic-crm'];
};

const getModulesForSubscription = (subscription: string): string[] => {
  return getSubscriptionConfig(subscription).modules;
};

// Utility functions
const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Custom hooks for quota monitoring
export const useQuotaMonitor = () => {
  const { state, getQuotaStatus } = useAuth();

  return {
    quotaStatus: getQuotaStatus(),
    warnings: state.quotaWarnings,
    isNearLimit: (type: 'storage' | 'ai', threshold = 80) => {
      const status = getQuotaStatus();
      return status[type] > threshold;
    }
  };
};

// packages/shared/auth/package.json
{
  "name": "@erp/shared-auth",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-router-dom": "^6.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0"
  }
}
```

**ACCEPTANCE CRITERIA:**
✅ Shared auth package with subscription-based access
✅ Storage quota management with file size/type/total limits
✅ AI API expense management with budget controls
✅ Rate limiting for AI services
✅ Real-time quota monitoring and warnings
✅ AuthGuard component with quota checks
✅ Configurable subscription tiers with different limits
✅ Usage tracking for storage and AI services
✅ TypeScript types for quotas and usage stats

---

## PROMPT 1.3: Shared UI Components

**CONTEXT**: Build shared UI component library used by all apps.

**EXECUTE THIS:**

```typescript
// packages/shared/ui/src/index.ts
export { Button } from './components/Button';
export { DataTable } from './components/DataTable';
export { Form } from './components/Form';
export { Layout } from './components/Layout';
export { Navigation } from './components/Navigation';
export { Modal } from './components/Modal';
export { Card } from './components/Card';

// packages/shared/ui/src/components/Button.tsx
import React from 'react';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  href?: string;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  href,
  disabled = false
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition-colors';

  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  const className = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`;

  if (href) {
    return (
      <a href={href} className={className}>
        {children}
      </a>
    );
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={className}
    >
      {children}
    </button>
  );
};

// packages/shared/ui/src/components/DataTable.tsx
import React from 'react';

interface Column {
  field: string;
  header: string;
  width?: string;
  render?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
  title?: string;
  data: any[];
  columns: Column[];
  loading?: boolean;
  actions?: React.ReactNode[];
  onRowClick?: (row: any) => void;
}

export const DataTable: React.FC<DataTableProps> = ({
  title,
  data,
  columns,
  loading = false,
  actions,
  onRowClick
}) => {
  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  return (
    <div className="bg-white shadow rounded-lg">
      {title && (
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-lg font-semibold">{title}</h2>
          {actions && <div className="flex space-x-2">{actions}</div>}
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.field}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  style={{ width: column.width }}
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, index) => (
              <tr
                key={index}
                onClick={() => onRowClick?.(row)}
                className={onRowClick ? 'hover:bg-gray-50 cursor-pointer' : ''}
              >
                {columns.map((column) => (
                  <td key={column.field} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {column.render ? column.render(row[column.field], row) : row[column.field]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// packages/shared/ui/src/components/Layout.tsx
import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
  navigation?: React.ReactNode;
  sidebar?: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children, navigation, sidebar }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      {navigation}
      <div className="flex">
        {sidebar && (
          <div className="w-64 bg-white shadow-sm">
            {sidebar}
          </div>
        )}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

// packages/shared/ui/package.json
{
  "name": "@erp/shared-ui",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "tailwindcss": "^3.0.0"
  }
}
```

**ACCEPTANCE CRITERIA:**
✅ Shared UI components with consistent styling
✅ DataTable component for CRUD operations
✅ Button component with variants
✅ Layout component with navigation and sidebar support

---

## PROMPT 1.4: Standard SaaS Application

**CONTEXT**: Build the standard SaaS application that serves subscription-based customers.

**EXECUTE THIS:**

```typescript
// apps/saas/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// Import shared packages
import { AuthProvider } from '@erp/shared-auth';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// apps/saas/src/App.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuth } from '@erp/shared-auth';
import { Layout } from '@erp/shared-ui';

// Import standard modules
import { DashboardModule } from '@erp/standard-dashboard';
import { CRMModule } from '@erp/standard-crm';
import { ERPModule } from '@erp/standard-erp';
import { HotelBookingModule } from '@erp/standard-hotel-booking';
import { ReportsModule } from '@erp/standard-reports';

import Navigation from './components/Navigation';
import LoginPage from './pages/LoginPage';

const App: React.FC = () => {
  const { state } = useAuth();

  if (!state.isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <Layout navigation={<Navigation />}>
      <Routes>
        <Route path="/" element={<DashboardModule />} />
        <Route path="/crm/*" element={<CRMModule />} />
        <Route path="/erp/*" element={<ERPModule />} />
        <Route path="/hotel-booking/*" element={<HotelBookingModule />} />
        <Route path="/reports/*" element={<ReportsModule />} />
      </Routes>
    </Layout>
  );
};

export default App;

// apps/saas/src/components/Navigation.tsx
import React from 'react';
import { useAuth } from '@erp/shared-auth';

const Navigation: React.FC = () => {
  const { state, canAccessModule } = useAuth();

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', path: '/' },
    { id: 'crm', label: 'CRM', path: '/crm' },
    { id: 'erp', label: 'ERP', path: '/erp' },
    { id: 'hotel-booking', label: 'Hotel Booking', path: '/hotel-booking' },
    { id: 'table-booking', label: 'Table Booking', path: '/table-booking' },
    { id: 'menu-management', label: 'Menu Management', path: '/menu-management' },
    { id: 'reports', label: 'Reports', path: '/reports' }
  ];

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold">ERP System</h1>
            </div>
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => (
                canAccessModule(item.id) && (
                  <a
                    key={item.id}
                    href={item.path}
                    className="text-gray-900 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
                  >
                    {item.label}
                  </a>
                )
              ))}
            </div>
          </div>
          <div className="flex items-center">
            <span className="text-sm text-gray-700">Welcome, {state.user?.name}</span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

// apps/saas/package.json
{
  "name": "@erp/saas-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-router-dom": "^6.0.0",
    "@erp/shared-auth": "^1.0.0",
    "@erp/shared-ui": "^1.0.0",
    "@erp/standard-dashboard": "^1.0.0",
    "@erp/standard-crm": "^1.0.0",
    "@erp/standard-erp": "^1.0.0",
    "@erp/standard-hotel-booking": "^1.0.0",
    "@erp/standard-reports": "^1.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^4.0.0"
  }
}

// apps/saas/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true
  },
  server: {
    port: 3000
  }
});
```

**ACCEPTANCE CRITERIA:**
✅ Standard SaaS app with subscription-based module access
✅ Navigation shows only modules user can access
✅ Uses shared auth and UI components
✅ Vite build configuration ready

---

## PROMPT 1.5: Customer Development Template

**CONTEXT**: Create template for customer-specific app development.

**EXECUTE THIS:**

```bash
# Create customer app template script
# scripts/create-customer-app.sh

#!/bin/bash

CUSTOMER_ID=$1
CUSTOMER_NAME=$2

if [ -z "$CUSTOMER_ID" ] || [ -z "$CUSTOMER_NAME" ]; then
    echo "Usage: ./create-customer-app.sh <customer-id> <customer-name>"
    exit 1
fi

echo "Creating customer app for $CUSTOMER_NAME ($CUSTOMER_ID)..."

# Create customer app directory
mkdir -p "apps/customers/$CUSTOMER_ID"

# Create customer app structure
mkdir -p "apps/customers/$CUSTOMER_ID/src/components"
mkdir -p "apps/customers/$CUSTOMER_ID/src/pages"
mkdir -p "apps/customers/$CUSTOMER_ID/public"

# Create package.json for customer
cat > "apps/customers/$CUSTOMER_ID/package.json" << EOF
{
  "name": "@erp/$CUSTOMER_ID-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-router-dom": "^6.0.0",
    "@erp/shared-auth": "^1.0.0",
    "@erp/shared-ui": "^1.0.0",
    "@erp/standard-dashboard": "^1.0.0",
    "@erp/standard-crm": "^1.0.0",
    "@erp/standard-erp": "^1.0.0",
    "@erp/standard-reports": "^1.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^4.0.0"
  }
}
EOF

# Create main.tsx
cat > "apps/customers/$CUSTOMER_ID/src/main.tsx" << EOF
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

import { AuthProvider } from '@erp/shared-auth';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
EOF

# Create App.tsx
cat > "apps/customers/$CUSTOMER_ID/src/App.tsx" << EOF
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuth } from '@erp/shared-auth';
import { Layout } from '@erp/shared-ui';

// Import standard modules
import { DashboardModule } from '@erp/standard-dashboard';
import { CRMModule } from '@erp/standard-crm';
import { ERPModule } from '@erp/standard-erp';
import { ReportsModule } from '@erp/standard-reports';

// Import custom modules (add as needed)
// import { CustomModule } from '@erp/custom-module-name';

import Navigation from './components/Navigation';
import LoginPage from './pages/LoginPage';

const App: React.FC = () => {
  const { state } = useAuth();

  if (!state.isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <Layout navigation={<Navigation />}>
      <Routes>
        <Route path="/" element={<DashboardModule />} />
        <Route path="/crm/*" element={<CRMModule />} />
        <Route path="/erp/*" element={<ERPModule />} />
        <Route path="/reports/*" element={<ReportsModule />} />
        {/* Add custom module routes here */}
      </Routes>
    </Layout>
  );
};

export default App;
EOF

# Create vite.config.ts
cat > "apps/customers/$CUSTOMER_ID/vite.config.ts" << EOF
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true
  },
  server: {
    port: 3001
  }
});
EOF

# Add to NX configuration
node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('nx.json', 'utf8'));
config.projects['$CUSTOMER_ID-app'] = {
  root: 'apps/customers/$CUSTOMER_ID',
  type: 'application'
};
fs.writeFileSync('nx.json', JSON.stringify(config, null, 2));
"

echo "✅ Customer app created for $CUSTOMER_NAME"
echo "📂 Location: apps/customers/$CUSTOMER_ID"
echo "🚀 Run: npm run dev:$CUSTOMER_ID"
echo "🔨 Build: npm run build:customer $CUSTOMER_ID"
```

**ACCEPTANCE CRITERIA:**
✅ Script creates customer app structure
✅ Customer app uses shared packages
✅ Standard modules included by default
✅ Ready for custom module addition
✅ NX configuration updated automatically

---

## PROMPT 1.6: Build & Deploy Scripts

**CONTEXT**: Create build and deployment scripts for both SaaS and customer apps.

**EXECUTE THIS:**

```bash
# Update package.json scripts
cat > package.json << EOF
{
  "name": "erp-monorepo",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "packages/*",
    "packages/shared/*",
    "packages/standard-modules/*",
    "packages/custom-modules/*",
    "apps/*",
    "apps/customers/*",
    "services/*"
  ],
  "scripts": {
    "dev": "nx serve saas",
    "dev:saas": "nx serve saas",
    "dev:customer": "nx serve",
    "build": "nx build",
    "build:saas": "nx build saas",
    "build:customer": "nx build",
    "build:all": "nx run-many --target=build --all",
    "test": "nx test",
    "deploy:saas": "./scripts/deploy-saas.sh",
    "deploy:customer": "./scripts/deploy-customer.sh",
    "create:customer": "./scripts/create-customer-app.sh",
    "lint": "nx lint",
    "format": "prettier --write ."
  },
  "devDependencies": {
    "@nx/workspace": "^17.0.0",
    "lerna": "^8.0.0",
    "typescript": "^5.0.0",
    "concurrently": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
EOF

# Create enhanced deploy scripts
cat > scripts/deploy-saas.sh << 'EOF'
#!/bin/bash
echo "🚀 Deploying SaaS application..."

# Build the SaaS app
echo "📦 Building SaaS app..."
nx build saas

# Build shared packages
echo "📦 Building shared packages..."
nx build shared-auth
nx build shared-ui
nx build shared-utils

# Deploy to app.alkas.com
echo "🌐 Deploying to app.alkas.com..."
# Add your deployment logic here
# Examples:
# - Upload to S3
# - Deploy to Vercel/Netlify
# - Update Docker container
# - Run deployment scripts

echo "✅ SaaS deployment completed!"
EOF

cat > scripts/deploy-customer.sh << 'EOF'
#!/bin/bash
CUSTOMER_ID=$1
SUBDOMAIN=$2

if [ -z "$CUSTOMER_ID" ]; then
    echo "Usage: ./deploy-customer.sh <customer-id> [subdomain]"
    exit 1
fi

if [ -z "$SUBDOMAIN" ]; then
    SUBDOMAIN="$CUSTOMER_ID.alkas.com"
fi

echo "🚀 Deploying customer app for $CUSTOMER_ID..."

# Build the customer app
echo "📦 Building customer app..."
nx build "$CUSTOMER_ID-app"

# Build shared packages
echo "📦 Building shared packages..."
nx build shared-auth
nx build shared-ui
nx build shared-utils

# Deploy to customer subdomain
echo "🌐 Deploying to $SUBDOMAIN..."
# Add your deployment logic here
# Examples:
# - Upload to S3 with custom subdomain
# - Deploy to Vercel with custom domain
# - Update Docker container with custom config
# - Run customer-specific deployment scripts

echo "✅ Customer deployment completed!"
echo "🌐 Customer app available at: https://$SUBDOMAIN"
EOF

# Create development helper scripts
cat > scripts/dev-customer.sh << 'EOF'
#!/bin/bash
CUSTOMER_ID=$1

if [ -z "$CUSTOMER_ID" ]; then
    echo "Usage: ./dev-customer.sh <customer-id>"
    exit 1
fi

echo "🚀 Starting development server for $CUSTOMER_ID..."
nx serve "$CUSTOMER_ID-app"
EOF

# Make scripts executable
chmod +x scripts/*.sh

# Create example customer (Pet Shop)
./scripts/create-customer-app.sh petshop "Pet Shop Solutions"

# Create README for customers
cat > apps/customers/README.md << 'EOF'
# Customer Applications

This directory contains customer-specific applications with custom modules.

## Structure

```

apps/customers/
├── petshop/ # Pet Shop customer app
├── hospital/ # Hospital customer app
└── restaurant/ # Restaurant customer app

````

## Creating New Customer App

```bash
# Create new customer app
npm run create:customer <customer-id> <customer-name>

# Example
npm run create:customer petshop "Pet Shop Solutions"
````

## Development

```bash
# Start development server
npm run dev:customer <customer-id>

# Build customer app
npm run build:customer <customer-id>

# Deploy customer app
npm run deploy:customer <customer-id>
```

## Adding Custom Modules

1. Create custom module in `packages/custom-modules/`
2. Add to customer app's `package.json` dependencies
3. Import and use in customer app's `App.tsx`
   EOF

```

**ACCEPTANCE CRITERIA:**
✅ Build scripts for both SaaS and customer apps
✅ Deployment scripts with subdomain support
✅ Development helper scripts
✅ Example customer app (Pet Shop) created
✅ Documentation for customer app management

This completes the core monorepo setup with shared packages, standard SaaS application, and customer development workflow! 🚀
```
