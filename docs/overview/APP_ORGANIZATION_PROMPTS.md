# Greek ERP/CRM - Monorepo Architecture & Development Prompts

## Document Information

- **Version**: 2.0
- **Date**: January 2025
- **Purpose**: Organize documentation for monorepo architecture with standard SaaS + enterprise custom deployments
- **Status**: Development Ready

---

## 🎯 Project Overview

This Greek ERP/CRM system follows a **monorepo architecture** with two deployment strategies:

1. **Standard SaaS** (app.alkas.com) - Subscription-based customers with standard modules
2. **Enterprise Custom** (customer.alkas.com) - Custom development with own subdomains

**Architecture**: Monorepo with shared packages, standard modules, and custom modules

---

## 📁 Project Structure

```
erp-monorepo/
├── packages/
│   ├── shared/                    # Common code for all deployments
│   │   ├── auth/                  # Authentication system
│   │   ├── ui/                    # UI components library
│   │   ├── utils/                 # Utility functions
│   │   ├── api/                   # API client
│   │   └── types/                 # TypeScript types
│   │
│   ├── standard-modules/          # Standard SaaS modules
│   │   ├── dashboard/
│   │   ├── crm/
│   │   ├── erp/
│   │   ├── invoicing/
│   │   ├── reports/
│   │   ├── hotel-booking/
│   │   ├── table-booking/
│   │   └── menu-management/
│   │
│   └── custom-modules/            # Enterprise custom modules
│       ├── pet-management/        # Pet shop modules
│       ├── pet-medical/
│       ├── hospital-patient/      # Hospital modules
│       ├── hospital-medical/
│       └── restaurant-kitchen/    # Restaurant modules
│
├── apps/
│   ├── saas/                      # Standard SaaS app
│   │   ├── src/
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   └── customers/                 # Customer-specific apps
│       ├── petshop/
│       ├── hospital/
│       └── restaurant/
│
├── services/
│   ├── api/                       # FastAPI backend
│   ├── auth/                      # Authentication service
│   └── integrations/              # Third-party APIs
│
└── scripts/
    ├── create-customer-app.sh
    ├── deploy-saas.sh
    └── deploy-customer.sh
```

---

## 🌐 STANDARD SAAS APPLICATION

### Context & Purpose

The **Standard SaaS Application** serves subscription-based customers who use standard modules without customization. All customers access the same domain (app.alkas.com) and see modules based on their subscription.

### Subscription Packages

```typescript
const subscriptionPackages = {
  "basic-crm": {
    price: "€50/month",
    modules: ["dashboard", "crm", "reports"],
  },
  "business-suite": {
    price: "€150/month",
    modules: ["dashboard", "crm", "erp", "invoicing", "reports"],
  },
  "hotel-management": {
    price: "€200/month",
    modules: ["dashboard", "crm", "erp", "hotel-booking", "reports"],
  },
  "restaurant-pro": {
    price: "€180/month",
    modules: [
      "dashboard",
      "crm",
      "erp",
      "table-booking",
      "menu-management",
      "reports",
    ],
  },
};
```

### Standard Modules

#### **Dashboard Module**

- **Purpose**: Overview and analytics
- **Features**: KPIs, charts, widgets, notifications
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`

#### **CRM Module**

- **Purpose**: Customer relationship management
- **Features**: Contacts, leads, opportunities, activities
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

#### **ERP Module**

- **Purpose**: Enterprise resource planning
- **Features**: Inventory, accounting, HR, project management
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

#### **Invoicing Module**

- **Purpose**: Invoice management with Greek compliance
- **Features**: Invoice creation, AADE integration, tax calculations
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

#### **Reports Module**

- **Purpose**: Business intelligence and reporting
- **Features**: Custom reports, analytics, exports
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

#### **Hotel Booking Module**

- **Purpose**: Hotel reservation management
- **Features**: Room management, bookings, availability
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

#### **Table Booking Module**

- **Purpose**: Restaurant reservation management
- **Features**: Table management, reservations, scheduling
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

#### **Menu Management Module**

- **Purpose**: Restaurant menu and pricing
- **Features**: Menu items, categories, pricing, ingredients
- **Dependencies**: `@erp/shared-auth`, `@erp/shared-ui`, `@erp/shared-utils`

### Technical Stack

- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **State Management**: Zustand + React Query
- **Forms**: React Hook Form + Zod validation
- **i18n**: React i18next (Greek/English)
- **Auth**: Shared auth package
- **Build**: Vite

### Database Models Required

```typescript
// Core Business Models
interface Company {
  id: string;
  name: string;
  afm: string; // Greek Tax ID
  doy: string; // Tax Office Code
  legal_form: string; // Legal Entity Type
  address: Address;
  aade_enabled: boolean;
  subscription_id: string;
  custom_fields: Record<string, any>;
}

interface Customer {
  id: string;
  company_id: string;
  name: string;
  email: string;
  phone: string;
  afm?: string;
  address: Address;
  customer_type: "individual" | "business";
  tags: string[];
  custom_fields: Record<string, any>;
}

interface Product {
  id: string;
  company_id: string;
  name: string;
  description: string;
  price: number;
  vat_rate: number;
  stock_quantity: number;
  categories: string[];
  custom_fields: Record<string, any>;
}

interface Invoice {
  id: string;
  company_id: string;
  customer_id: string;
  invoice_number: string;
  issue_date: Date;
  due_date: Date;
  items: InvoiceItem[];
  subtotal: number;
  vat_amount: number;
  total: number;
  status: "draft" | "sent" | "paid" | "overdue";
  aade_submitted: boolean;
  custom_fields: Record<string, any>;
}

interface Subscription {
  id: string;
  company_id: string;
  package_id: string;
  status: "active" | "cancelled" | "expired";
  start_date: Date;
  end_date: Date;
  modules: string[];
}
```

---

## 🏪 ENTERPRISE CUSTOM APPLICATIONS

### Context & Purpose

**Enterprise Custom Applications** are deployed to customer-specific subdomains (customer.alkas.com) when customers need modules that don't exist in standard packages.

### Development Workflow

1. **Customer Request**: Customer needs custom Pet Shop management
2. **Custom Development**: We develop pet-specific modules
3. **Customer App Creation**: Create customer-specific app
4. **Deployment**: Deploy to petshop.alkas.com
5. **Maintenance**: Regular updates via git merge

### Custom Module Examples

#### **Pet Management Module**

```typescript
// packages/custom-modules/pet-management/src/index.ts
export const PetManagementModule = {
  name: "Pet Management",
  routes: [
    { path: "/pet-management", component: PetListPage },
    { path: "/pet-management/create", component: PetCreatePage },
    { path: "/pet-management/:id", component: PetDetailPage },
  ],
  navigation: [
    { label: "Pet Management", path: "/pet-management", icon: "pets" },
  ],
};
```

#### **Hospital Patient Module**

```typescript
// packages/custom-modules/hospital-patient/src/index.ts
export const HospitalPatientModule = {
  name: "Patient Management",
  routes: [
    { path: "/patients", component: PatientListPage },
    { path: "/patients/:id/medical-history", component: MedicalHistoryPage },
  ],
  navigation: [{ label: "Patients", path: "/patients", icon: "medical" }],
};
```

### Customer App Structure

```typescript
// apps/customers/petshop/src/App.tsx
import { DashboardModule } from "@erp/standard-dashboard";
import { CRMModule } from "@erp/standard-crm";
import { ERPModule } from "@erp/standard-erp";
import { ReportsModule } from "@erp/standard-reports";

// Custom modules
import { PetManagementModule } from "@erp/custom-pet-management";
import { PetMedicalModule } from "@erp/custom-pet-medical";

const modules = [
  // Standard modules
  DashboardModule,
  CRMModule,
  ERPModule,
  ReportsModule,

  // Custom modules
  PetManagementModule,
  PetMedicalModule,
];
```

---

## 📦 SHARED PACKAGES

### **@erp/shared-auth**

- **Purpose**: Authentication system for all apps
- **Features**: Login/logout, permissions, subscription checks
- **Components**: AuthProvider, useAuth, AuthGuard

### **@erp/shared-ui**

- **Purpose**: UI component library
- **Features**: Consistent design system
- **Components**: Button, DataTable, Form, Layout, Navigation

### **@erp/shared-utils**

- **Purpose**: Utility functions
- **Features**: API client, date utils, validation
- **Functions**: formatCurrency, validateEmail, ApiClient

### **@erp/shared-api**

- **Purpose**: API client configuration
- **Features**: HTTP client, error handling, interceptors

### **@erp/shared-types**

- **Purpose**: TypeScript type definitions
- **Features**: Common interfaces and types

---

## 🔧 BUILD & DEPLOYMENT

### **Standard SaaS Deployment**

```bash
# Build SaaS app
npm run build:saas

# Deploy to app.alkas.com
npm run deploy:saas
```

### **Enterprise Custom Deployment**

```bash
# Create customer app
npm run create:customer petshop "Pet Shop Solutions"

# Build customer app
npm run build:customer petshop

# Deploy to petshop.alkas.com
npm run deploy:customer petshop
```

### **Git Workflow**

```bash
# Main branches
main                    # Production code
develop                 # Development integration

# Customer branches
customer/petshop        # Pet shop custom development
customer/hospital       # Hospital custom development

# Update customer with latest shared code
git checkout customer/petshop
git merge main          # Gets latest shared improvements
```

---

## 🎯 DEVELOPMENT PRIORITIES

### **Phase 1: Core Foundation (Weeks 1-4)**

1. **Setup monorepo structure**
2. **Build shared packages** (auth, ui, utils)
3. **Create standard SaaS app**
4. **Implement basic modules** (dashboard, crm, erp)

### **Phase 2: Standard Modules (Weeks 5-8)**

1. **Complete invoicing module** with Greek compliance
2. **Build reports module**
3. **Add hotel booking module**
4. **Add restaurant modules**

### **Phase 3: Enterprise Custom (Weeks 9-12)**

1. **Create customer app template**
2. **Build first custom module** (pet management)
3. **Setup deployment pipeline**
4. **Test complete workflow**

---

## 💰 BUSINESS MODEL

### **Standard SaaS Pricing**

- **Basic CRM**: €50/month
- **Business Suite**: €150/month
- **Hotel Management**: €200/month
- **Restaurant Pro**: €180/month

### **Enterprise Custom Development**

- **Simple Module**: €5,000 - €15,000
- **Complex Module**: €15,000 - €50,000
- **Full Custom System**: €50,000+

---

## 🚀 GETTING STARTED

### **Development Setup**

```bash
# Install dependencies
npm install

# Start SaaS development
npm run dev:saas

# Create customer app
npm run create:customer petshop "Pet Shop Solutions"

# Start customer development
npm run dev:customer petshop
```

### **Testing**

```bash
# Run all tests
npm test

# Test specific package
nx test shared-auth

# Test specific app
nx test saas
```

This architecture provides the perfect balance of **code reuse** and **customization flexibility**! 🚀
