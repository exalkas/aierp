# 🏢 Simple SaaS + Enterprise Strategy

## Overview

Two clear paths: **Standard SaaS** customers use `app.alkas.com` with subscription-based modules, **Enterprise** customers with custom development get their own subdomains.

---

## 🌐 **STANDARD SAAS CUSTOMERS**

### **Single Domain: app.alkas.com**

All standard customers log into the same domain and see modules based on their subscription.

```typescript
// Subscription-based module visibility
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

### **Examples:**

#### **Hotel Customer Login**

```typescript
// Hotel owner logs into app.alkas.com
const hotelCustomer = {
  email: "owner@grandhotel.com",
  subscription: "hotel-management",
  customerId: "hotel-customer-123",
};

// System shows only their subscribed modules
const visibleModules = [
  "dashboard",
  "crm", // Customer management
  "erp", // Financial management
  "hotel-booking", // Room reservations
  "reports", // Analytics
];

// Navigation appears as:
const navigation = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Customers", path: "/crm" },
  { label: "Finances", path: "/erp" },
  { label: "Hotel Booking", path: "/hotel-booking" }, // Their main feature
  { label: "Reports", path: "/reports" },
];
```

#### **Restaurant Customer Login**

```typescript
// Restaurant owner logs into app.alkas.com
const restaurantCustomer = {
  email: "manager@tastyrestaurant.com",
  subscription: "restaurant-pro",
  customerId: "restaurant-customer-456",
};

// System shows only their subscribed modules
const visibleModules = [
  "dashboard",
  "crm", // Customer management
  "erp", // Financial management
  "table-booking", // Table reservations
  "menu-management", // Menu & pricing
  "reports", // Analytics
];

// Navigation appears as:
const navigation = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Customers", path: "/crm" },
  { label: "Finances", path: "/erp" },
  { label: "Reservations", path: "/table-booking" },
  { label: "Menu", path: "/menu-management" },
  { label: "Reports", path: "/reports" },
];
```

### **Module Visibility System**

```typescript
// Frontend checks subscription to show/hide modules
export const ModuleVisibilityService = {
  async getVisibleModules(customerId: string): Promise<string[]> {
    const customer = await fetch(`/api/customers/${customerId}`);
    const subscription = customer.subscription;

    return subscriptionPackages[subscription].modules;
  },

  async canAccessModule(
    customerId: string,
    moduleId: string
  ): Promise<boolean> {
    const visibleModules = await this.getVisibleModules(customerId);
    return visibleModules.includes(moduleId);
  },
};

// Router guards
router.beforeEach(async (to, from, next) => {
  const moduleId = to.path.split("/")[1]; // e.g., '/crm' -> 'crm'
  const canAccess = await ModuleVisibilityService.canAccessModule(
    customerId,
    moduleId
  );

  if (canAccess) {
    next();
  } else {
    next("/upgrade"); // Redirect to upgrade page
  }
});
```

---

## 🏪 **ENTERPRISE CUSTOMERS WITH CUSTOM DEVELOPMENT**

### **Custom Subdomains: customername.alkas.com**

When customers need modules that don't exist in standard packages, we develop custom modules and deploy to their own subdomain.

### **Pet Shop Example**

#### **Customer Request**

```typescript
const petShopRequest = {
  customer: "Happy Paws Pet Shop",
  email: "info@happypaws.com",
  needs: [
    "Pet profile management",
    "Medical history tracking",
    "Vaccination schedules",
    "Grooming appointments",
    "Pet boarding management",
  ],
  budget: "€12,000",
  timeline: "6 weeks",
};
```

#### **Our Development Process**

```bash
# 1. Create customer branch
git checkout -b customer/petshop

# 2. Develop custom modules
mkdir -p src/modules/pet-management
mkdir -p src/modules/pet-medical
mkdir -p src/modules/pet-boarding

# 3. Create customer-specific build
npm run build:customer petshop

# 4. Deploy to subdomain
npm run deploy:customer petshop petshop.alkas.com
```

#### **Pet Shop Customer Gets**

```typescript
// Pet shop owner logs into petshop.alkas.com
const petShopCustomer = {
  email: "owner@happypaws.com",
  domain: "petshop.alkas.com",
  customerId: "petshop-customer-789",
};

// They see standard modules + custom modules
const visibleModules = [
  // Standard modules
  "dashboard",
  "crm",
  "erp",
  "invoicing",
  "reports",

  // Custom modules (developed specifically for them)
  "pet-management",
  "pet-medical",
  "pet-boarding",
];

// Navigation appears as:
const navigation = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Customers", path: "/crm" },
  { label: "Finances", path: "/erp" },
  { label: "Invoicing", path: "/invoicing" },
  { section: "Pet Shop" },
  { label: "Pet Management", path: "/pet-management" }, // Custom!
  { label: "Medical Records", path: "/pet-medical" }, // Custom!
  { label: "Pet Boarding", path: "/pet-boarding" }, // Custom!
  { label: "Reports", path: "/reports" },
];
```

#### **Custom Module Example**

```typescript
// /src/modules/pet-management/PetManagementModule.ts
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
  components: {
    PetListPage: () => import("./pages/PetListPage.vue"),
    PetCreatePage: () => import("./pages/PetCreatePage.vue"),
    PetDetailPage: () => import("./pages/PetDetailPage.vue"),
  },
};
```

---

## 🔧 **TECHNICAL IMPLEMENTATION**

### **Standard SaaS (app.alkas.com)**

```typescript
// Single build for all standard customers
// vite.config.ts
export default defineConfig({
  build: {
    outDir: "dist/saas",
    rollupOptions: {
      input: {
        main: "src/main.ts",
      },
    },
  },
});

// src/main.ts - Standard SaaS entry point
import { createApp } from "vue";
import App from "./App.vue";
import { createRouter } from "./router";

// All standard modules
import { DashboardModule } from "./modules/dashboard";
import { CRMModule } from "./modules/crm";
import { ERPModule } from "./modules/erp";
import { HotelBookingModule } from "./modules/hotel-booking";
import { TableBookingModule } from "./modules/table-booking";
import { MenuManagementModule } from "./modules/menu-management";
import { ReportsModule } from "./modules/reports";

const standardModules = [
  DashboardModule,
  CRMModule,
  ERPModule,
  HotelBookingModule,
  TableBookingModule,
  MenuManagementModule,
  ReportsModule,
];

const app = createApp(App);
const router = createRouter(standardModules);

app.use(router);
app.mount("#app");
```

### **Enterprise Custom (petshop.alkas.com)**

```typescript
// Custom build for pet shop customer
// vite.config.petshop.ts
export default defineConfig({
  build: {
    outDir: "dist/customers/petshop",
    rollupOptions: {
      input: {
        main: "src/customers/petshop/main.ts",
      },
    },
  },
});

// src/customers/petshop/main.ts - Pet Shop entry point
import { createApp } from "vue";
import App from "../../App.vue";
import { createRouter } from "../../router";

// Standard modules
import { DashboardModule } from "../../modules/dashboard";
import { CRMModule } from "../../modules/crm";
import { ERPModule } from "../../modules/erp";
import { ReportsModule } from "../../modules/reports";

// Custom modules (only for pet shop)
import { PetManagementModule } from "../../modules/pet-management";
import { PetMedicalModule } from "../../modules/pet-medical";
import { PetBoardingModule } from "../../modules/pet-boarding";

const allModules = [
  // Standard
  DashboardModule,
  CRMModule,
  ERPModule,
  ReportsModule,

  // Custom
  PetManagementModule,
  PetMedicalModule,
  PetBoardingModule,
];

const app = createApp(App);
const router = createRouter(allModules);

app.use(router);
app.mount("#app");
```

---

## 🚀 **DEPLOYMENT STRATEGY**

### **Standard SaaS Deployment**

```bash
# Build standard SaaS version
npm run build

# Deploy to app.alkas.com
npm run deploy:saas

# All standard customers use this single deployment
```

### **Enterprise Custom Deployment**

```bash
# Build customer-specific version
npm run build:customer petshop

# Deploy to customer subdomain
npm run deploy:customer petshop petshop.alkas.com

# Each enterprise customer gets their own deployment
```

### **Nginx Configuration**

```nginx
# Standard SaaS
server {
    listen 443 ssl;
    server_name app.alkas.com;
    root /var/www/saas/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

# Enterprise Customer
server {
    listen 443 ssl;
    server_name petshop.alkas.com;
    root /var/www/customers/petshop/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 💰 **BUSINESS MODEL**

### **Standard SaaS Pricing**

```typescript
const standardPricing = {
  "basic-crm": "€50/month",
  "business-suite": "€150/month",
  "hotel-management": "€200/month",
  "restaurant-pro": "€180/month",
};
```

### **Enterprise Custom Development**

```typescript
const customDevelopment = {
  "simple-module": "€5,000 - €15,000",
  "complex-module": "€15,000 - €50,000",
  "full-custom-system": "€50,000+",
};
```

---

## 🎯 **SUMMARY**

### **✅ Standard SaaS Customers:**

- **Domain:** app.alkas.com
- **Modules:** Based on subscription
- **Pricing:** Monthly recurring
- **Development:** Zero custom work

### **✅ Enterprise Customers:**

- **Domain:** customername.alkas.com
- **Modules:** Standard + Custom
- **Pricing:** One-time development fee
- **Development:** Custom modules as needed

This is exactly how successful SaaS companies like Salesforce, Shopify, and others operate! 🚀
