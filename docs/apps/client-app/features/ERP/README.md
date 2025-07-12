# ERP Module - Modular Greek Business Management

## Overview

The ERP module provides a comprehensive, modular business management solution specifically designed for Greek businesses. Unlike traditional monolithic ERP systems, our modular approach allows businesses to start with just the features they need and expand as they grow, all while maintaining seamless integration with the CRM module.

## 🎯 Core Value Proposition

**Problem Solved**: Current ERP solutions force businesses to:

- Pay for features they don't need or use
- Deal with complex setups for simple requirements
- Use separate systems that don't communicate
- Struggle with Greek compliance and regulations

**Our Solution**: Modular ERP where businesses can:

- Start with just invoicing (€19/month) or inventory (€29/month)
- Add modules as they grow without changing systems
- Maintain seamless CRM integration from day one
- Get built-in Greek compliance in every module

---

## 🧩 ERP Module Breakdown

### **1. Basic Invoicing Module** - €19/month

**Perfect for**: Freelancers, Doctors, Lawyers, Consultants
**Dependencies**: None (uses CRM customer data)

#### Features:

- **16 Greek Document Types**: Complete support for all Greek business documents (parastatika)
- **AADE MyDATA Integration**: Real-time tax authority submission
- **QR Code Generation**: Mandatory QR codes on all invoices
- **Document Workflow**: Proper business document relationships and workflows
- **Professional Services**: Enhanced support for service-only businesses
- **Greek VAT Compliance**: Automatic VAT calculations based on business type
- **Customer Integration**: Seamless use of CRM customer database

#### Supported Document Types:

**Legal Documents (Νόμιμα Παραστατικά)**:

- **Sales Invoice** (Τιμολόγιο Πώλησης) - Standard B2B invoicing
- **Receipt** (Απόδειξη Λιανικής Πώλησης) - Retail sales up to €500
- **Credit Note** (Πιστωτικό Τιμολόγιο) - Invoice corrections/returns
- **Debit Note** (Χρεωστικό Τιμολόγιο) - Additional charges
- **Proforma Invoice** (Προτιμολόγιο) - Quotation document
- **Delivery Note** (Δελτίο Αποστολής) - Goods delivery tracking
- **Simplified Invoice** (Απλοποιημένο Τιμολόγιο) - Simplified B2B
- **Self-billing** (Αυτο-τιμολόγηση) - Reverse charge scenarios
- **E-Invoice** (Ηλεκτρονικό Τιμολόγιο) - UBL/XML format

**Business Workflow Documents**:

- **Sales Order** (Δελτίο Παραγγελίας) - Customer orders
- **Order Confirmation** (Επιβεβαίωση Παραγγελίας) - Order acceptance
- **Purchase Order** (Παραγγελία Προμηθευτή) - Supplier orders
- **Request for Quotation** (Αίτημα Προσφοράς) - Quote requests
- **Sales Quotation** (Προσφορά Πώλησης) - Customer quotes
- **Return Note** (Δελτίο Επιστροφής) - Returns management
- **Internal Transfer** (Εσωτερική Μεταφορά) - Inter-location transfers

#### Use Cases:

```typescript
// Doctor billing patients - Enhanced service management
const medicalInvoice = {
  customerId: "patient-123",
  documentType: "sales_invoice", // or "receipt" for cash payments
  services: [
    {
      name: "General Consultation",
      duration: 45, // minutes
      price: 50.0,
      vatExempt: true,
      professionalType: "healthcare",
      serviceLocation: "office",
      appointmentDateTime: "2025-01-15T10:00:00Z",
    },
    {
      name: "Medical Certificate",
      duration: 15,
      price: 25.0,
      vatExempt: true,
      requiresLicense: true,
      preparationTime: 10, // minutes for certificate preparation
    },
  ],
  greekCompliance: {
    aadeSubmission: true,
    vatExemption: "medical_services",
    professionalType: "healthcare",
    medicalChamberRegistration: "ISA-12345",
  },
  recurring: {
    isRecurring: false, // One-time appointment
    followUpRequired: true,
    followUpInterval: "monthly",
  },
};

// Lawyer billing client - Professional services with time tracking
const legalInvoice = {
  customerId: "client-456",
  documentType: "sales_invoice",
  services: [
    {
      name: "Legal Consultation",
      duration: 180, // 3 hours
      pricing: "hourly",
      hourlyRate: 150.0,
      totalHours: 3,
      vatExempt: true,
      professionalType: "legal",
      serviceLocation: "office",
      requiresLicense: true,
      certificationRequired: "DSA_BAR_LICENSE",
    },
    {
      name: "Document Preparation",
      duration: 120, // 2 hours
      pricing: "project",
      price: 200.0,
      vatExempt: true,
      serviceLocation: "remote", // Can be done remotely
      allowsRemoteDelivery: true,
    },
  ],
  greekCompliance: {
    aadeSubmission: true,
    vatExemption: "legal_services",
    professionalType: "legal",
    barAssociationMembership: "DSA-67890",
  },
  // Case-based billing with proper documentation
  caseReference: "CASE-2025-001",
  clientMatter: "Contract Review and Legal Opinion",
};

// Engineering Consultant - Technical services with site visits
const engineeringInvoice = {
  customerId: "construction-company-789",
  documentType: "sales_invoice",
  services: [
    {
      name: "Structural Analysis",
      duration: 480, // 8 hours
      pricing: "project",
      price: 800.0,
      vatRate: 24.0, // Engineers pay VAT
      professionalType: "engineering",
      serviceLocation: "client_location",
      requiresLicense: true,
      certificationRequired: "TEE_STRUCTURAL_ENGINEER",
    },
    {
      name: "Site Inspection",
      duration: 240, // 4 hours
      pricing: "hourly",
      hourlyRate: 75.0,
      totalHours: 4,
      vatRate: 24.0,
      serviceLocation: "client_location",
      requiresPreparation: true,
      preparationTime: 30, // minutes
    },
  ],
  greekCompliance: {
    aadeSubmission: true,
    professionalType: "engineering",
    teeRegistration: "TEE-54321",
    projectPermitReference: "PERMIT-2025-BLD-001",
  },
  projectDetails: {
    projectName: "Residential Building - Athens",
    projectPhase: "design_review",
    deliverables: ["structural_calculations", "inspection_report"],
  },
};
```

---

### **2. Product Catalog & Inventory** - €29/month

**Perfect for**: Retail stores, Small warehouses, Product-based businesses
**Dependencies**: None (standalone module)

#### Features:

- **Flexible Product Management**: Products, services, subscriptions, and bundles
- **Service-Only Business Support**: Complete service management without inventory
- **Professional Services**: Booking, scheduling, and license management
- **Product Variants**: Unlimited dynamic attributes (color, size, material, etc.)
- **Smart Inventory**: Only track inventory for physical products
- **Barcode Support**: SKU generation and barcode scanning
- **Advanced Categories**: Hierarchical organization with VAT defaults
- **Flexible Pricing**: Multiple pricing tiers, hourly rates, project-based
- **Service Scheduling**: Appointment booking and calendar integration

#### Product Types Supported:

```typescript
// Simple Products (most common)
interface SimpleProduct {
  type: "simple";
  name: string;
  sku: string;
  price: number;
  stock: number;
  vatRate: number;
  category: string;
}

// Variable Products (clothing, accessories)
interface VariableProduct {
  type: "variable";
  name: string;
  basePrice: number;
  variants: [
    { attributes: { color: "Red"; size: "M" }; sku: "SHIRT-RED-M"; stock: 25 },
    { attributes: { color: "Blue"; size: "L" }; sku: "SHIRT-BLUE-L"; stock: 15 }
  ];
  attributes: [
    { name: "Color"; values: ["Red", "Blue", "Green", "Black"] },
    { name: "Size"; values: ["S", "M", "L", "XL"] }
  ];
}

// Service Products - Enhanced for Service-Only Businesses
interface ServiceProduct {
  type: "service";
  name: string;
  pricing: "fixed" | "hourly" | "project";

  // Booking & Scheduling
  duration?: number; // Service duration in minutes
  bufferTime?: number; // Buffer between appointments
  isBookable: boolean; // Can be booked via calendar
  advanceBookingDays?: number; // How far in advance
  maxBookingsPerDay?: number; // Daily booking limit

  // Professional Requirements
  requiresLicense?: boolean; // Professional certification required
  certificationRequired?: string; // Specific certification needed
  professionalType?: string; // "doctor", "lawyer", "engineer", etc.

  // Service Delivery
  serviceLocation: "office" | "client_location" | "remote" | "any";
  allowsRemoteDelivery: boolean; // Can be delivered remotely
  requiresPreparation: boolean; // Needs preparation time
  preparationTime?: number; // Preparation time in minutes

  // Recurring Services
  isRecurring: boolean; // Subscription/recurring service
  recurringInterval?: "daily" | "weekly" | "monthly" | "yearly";
  recurringDuration?: number; // How many intervals

  // Pricing & VAT
  vatRate: number;
  vatExempt?: boolean; // Professional services exemption

  // Inventory (services don't track inventory)
  trackInventory: false;
  requiresShipping: false;
}

// Bundle Products
interface BundleProduct {
  type: "bundle";
  name: string;
  components: [
    { productId: "laptop"; quantity: 1 },
    { productId: "mouse"; quantity: 1 },
    { productId: "setup-service"; quantity: 1 }
  ];
  bundleDiscount: 10; // 10% off
}
```

---

### **3. Financial Management** - €39/month

**Perfect for**: Growing businesses needing full accounting
**Dependencies**: Basic Invoicing (upgrades existing invoicing functionality)

#### Features:

- **Double-Entry Accounting**: Complete bookkeeping system
- **Greek Chart of Accounts**: Pre-configured for Greek businesses
- **Advanced AADE Integration**: Full MyDATA compliance with all document types
- **Financial Reports**: P&L, Balance Sheet, Cash Flow, VAT reports
- **Bank Reconciliation**: Match bank transactions with accounting records
- **Multi-Currency Support**: Handle international transactions
- **Cost Centers**: Track profitability by department or project

#### Greek Compliance Features:

```typescript
const greekFinancialCompliance = {
  // AADE MyDATA Integration
  aadeFeatures: [
    "invoice_submission",
    "receipt_submission",
    "credit_note_submission",
    "vat_return_preparation",
    "periodic_summaries",
  ],

  // Greek Tax Calculations
  taxCalculations: [
    "vat_standard_24",
    "vat_reduced_13",
    "vat_super_reduced_6",
    "island_vat_reductions",
    "professional_exemptions",
  ],

  // Banking Integration
  bankingSupport: [
    "alpha_bank",
    "eurobank",
    "national_bank",
    "piraeus_bank",
    "attica_bank",
  ],

  // Reporting
  greekReports: [
    "vat_return_forms",
    "income_tax_calculations",
    "social_security_reports",
    "withholding_tax_reports",
  ],
};
```

---

### **4. Advanced Inventory & Purchasing** - €49/month

**Perfect for**: Multi-location businesses, Complex supply chains
**Dependencies**: Product Catalog Module

#### Features:

- **Multi-Location Inventory**: Track stock across multiple warehouses/stores
- **Automated Purchasing**: Smart reordering based on sales velocity
- **Supplier Management**: Vendor relationships and performance tracking
- **Purchase Orders**: Complete procurement workflow
- **Stock Transfers**: Move inventory between locations
- **Advanced Analytics**: Inventory turnover, dead stock analysis
- **Barcode Scanning**: Mobile inventory management

#### Inventory Intelligence:

```typescript
const inventoryIntelligence = {
  // Automated Reordering
  reorderRules: {
    minimumStock: 10,
    reorderQuantity: 50,
    leadTime: 7, // days
    seasonalAdjustment: true,
  },

  // Multi-location Management
  locations: [
    { name: "Main Warehouse", type: "warehouse", address: "Athens" },
    { name: "Retail Store", type: "store", address: "Thessaloniki" },
    { name: "Online Fulfillment", type: "fulfillment", address: "Piraeus" },
  ],

  // Supplier Integration
  suppliers: [
    {
      name: "Greek Supplier SA",
      products: ["local_products"],
      leadTime: 3,
      paymentTerms: "30_days",
    },
  ],
};
```

---

### **5. Human Resources & Payroll** - €59/month

**Perfect for**: Businesses with employees
**Dependencies**: Financial Management (for payroll accounting integration)

#### Features:

- **Employee Lifecycle Management**: Hiring to retirement
- **Greek Payroll System**: IKA, EFKA, OAED compliance
- **Time & Attendance**: Work hours, overtime, Greek holiday calendar
- **Performance Management**: Reviews, goals, training tracking
- **Document Management**: Contracts, certifications, employee files
- **Leave Management**: Vacation, sick leave, Greek public holidays

#### Greek Labor Compliance:

```typescript
const greekLaborCompliance = {
  // Social Security Integration
  socialSecurity: [
    "ika_contributions",
    "efka_integration",
    "oaed_unemployment",
    "auxiliary_funds",
  ],

  // Tax Calculations
  payrollTaxes: [
    "income_tax",
    "solidarity_contribution",
    "municipal_tax",
    "employer_contributions",
  ],

  // Labor Law Compliance
  laborLaw: [
    "minimum_wage_enforcement",
    "overtime_calculations",
    "holiday_pay",
    "annual_leave_accrual",
    "termination_procedures",
  ],

  // Reporting Requirements
  reportingRequirements: [
    "monthly_declarations",
    "annual_statements",
    "labor_inspectorate_reports",
    "tax_authority_filings",
  ],
};
```

---

### **6. Business Intelligence & Analytics** - €69/month

**Perfect for**: Data-driven businesses wanting insights
**Dependencies**: Financial Management (needs financial data for analysis)

#### Features:

- **Executive Dashboards**: Real-time KPI monitoring
- **Sales Analytics**: Revenue trends, customer analysis, product performance
- **Financial Analytics**: Profitability analysis, cost center reporting
- **Predictive Analytics**: Sales forecasting, demand planning
- **Custom Reports**: Build your own reports and dashboards
- **Mobile Analytics**: Access insights anywhere

---

## 💰 Subscription Packages & Bundle Pricing

### **Standalone Modules** (À la carte pricing)

- **Basic Invoicing**: €19/month
- **Product Catalog**: €29/month
- **Financial Management**: €39/month (requires Basic Invoicing)
- **Advanced Inventory**: €49/month (requires Product Catalog)
- **HR & Payroll**: €59/month (requires Financial Management)
- **Business Intelligence**: €69/month (requires Financial Management)

### **Bundle Packages** (Save with bundles)

#### **🏥 Professional Services Bundle** - €59/month

**Save €10** (vs €50 CRM + €19 Invoicing = €69)

- **Includes**: CRM + Enhanced Invoicing with 16 Document Types
- **Perfect for**: Doctors, Lawyers, Engineers, Consultants, Freelancers
- **Focus**: Service-only businesses with professional requirements

**Enhanced Service Features**:

- **Appointment Booking**: Calendar integration with buffer times
- **Professional Licensing**: License and certification tracking
- **Service Scheduling**: Duration, preparation time, booking limits
- **Greek Professional Compliance**: Medical Chamber, Bar Association, TEE
- **Multi-Location Services**: Office, client location, remote delivery
- **Recurring Services**: Subscription and maintenance contracts
- **Professional Invoicing**: VAT-exempt services, insurance billing
- **No Inventory Hassle**: Services don't track physical inventory

#### **🏪 Small Business Bundle** - €129/month

**Save €28** (vs €167 separate pricing)

- **Includes**: CRM + Product Catalog + Financial Management + Advanced Inventory
- **Perfect for**: Retail stores, Product-based businesses
- **Focus**: Complete product management with accounting

#### **🏢 Complete Business Suite** - €199/month

**Save €56** (vs €255 separate pricing)

- **Includes**: All modules (CRM + all 6 ERP modules)
- **Perfect for**: Growing businesses with employees
- **Focus**: Full business management solution

#### **🏗️ Enterprise Package** - €349/month

**Includes**: Complete Business Suite + Priority Support + Custom Integrations

- **Perfect for**: Large businesses, complex requirements
- **Focus**: Enterprise-grade features and support

---

## 🔄 CRM-ERP Integration Examples

### **Lead to Invoice Workflow**

```typescript
// 1. CRM: Lead captured and qualified
const businessLead = {
  company: "Taverna Mykonos",
  contact: "Nikos Papadopoulos",
  business: "Restaurant",
  needs: ["pos_system", "inventory_management", "financial_reporting"],
};

// 2. CRM: Lead converted to customer (data flows to ERP)
const newCustomer = {
  id: "customer-taverna-123",
  companyName: "Taverna Mykonos",
  contactPerson: "Nikos Papadopoulos",
  greekTaxInfo: {
    afm: "9",
    doy: "Α' ΑΘΗΝΩΝ",
    vatRegistered: true,
  },
  address: {
    street: "Mitropoleos 15",
    city: "Mykonos",
    postalCode: "84600",
    country: "Greece",
  },
};

// 3. ERP: Quote created using CRM customer data
const quote = {
  customerId: newCustomer.id, // Automatically available from CRM
  items: [
    {
      type: "product",
      productId: "pos-system-basic",
      description: "POS System with Greek Receipt Printer",
      quantity: 1,
      unitPrice: 1200.0,
      vatRate: 24,
    },
    {
      type: "service",
      productId: "setup-training",
      description: "Installation and Staff Training",
      quantity: 8, // hours
      unitPrice: 75.0,
      vatRate: 24,
    },
  ],
  greekCompliance: {
    aadeRequired: true,
    customerVatNumber: newCustomer.greekTaxInfo.afm,
  },
};

// 4. ERP: Quote accepted → Invoice automatically generated
const invoice = {
  ...quote,
  invoiceNumber: "INV-2025-001",
  issueDate: new Date(),
  dueDate: addDays(new Date(), 30),
  aadeSubmitted: false, // Will be submitted automatically
  status: "pending_payment",
};

// 5. CRM: Opportunity updated with invoice details
updateOpportunity(opportunityId, {
  status: "closed_won",
  revenue: invoice.total,
  invoiceReference: invoice.invoiceNumber,
  notes: "POS system order confirmed, installation scheduled",
});
```

### **Product to Sales Integration**

```typescript
// 1. ERP: Product created with Greek market specifics
const greekProduct = {
  name: "Organic Olive Oil - Kalamata",
  type: "variable",
  basePrice: 12.0,
  variants: [
    { size: "250ml", price: 8.0, stock: 100 },
    { size: "500ml", price: 12.0, stock: 75 },
    { size: "1L", price: 18.0, stock: 50 },
  ],
  greekSpecifics: {
    origin: "Kalamata, Messinia",
    organicCertification: "DIO-GR-001",
    vatRate: 13, // Reduced rate for food products
    seasonalProduct: true,
    harvestYear: 2024,
  },
};

// 2. CRM: Sales rep creates quote with real-time inventory
const customerQuote = {
  customerId: "gourmet-shop-athens",
  items: [
    {
      productId: greekProduct.id,
      variantId: "500ml",
      quantity: 25,
      unitPrice: 12.0,
      // Real-time stock check
      availableStock: checkStock(greekProduct.id, "500ml"), // Returns: 75
      reservedStock: 25, // Temporarily reserved for quote
    },
  ],
  validUntil: addDays(new Date(), 14),
  greekBusinessRules: {
    seasonalDiscount: true, // 10% off during harvest season
    bulkDiscount: true, // 5% off for orders > 20 units
    islandDelivery: false, // Mainland delivery
  },
};

// 3. ERP: Quote accepted → Stock automatically updated
const confirmedOrder = {
  ...customerQuote,
  status: "confirmed",
  stockUpdate: {
    productId: greekProduct.id,
    variantId: "500ml",
    oldStock: 75,
    newStock: 50, // 75 - 25 = 50
    reservedStock: 0, // Reservation cleared
  },
};
```

---

## 🎭 Real-World Customer Examples

### **👨‍⚕️ Dr. Sophia Dimitriou - Cardiologist**

**Package**: Professional Services Bundle (€59/month)
**Modules**: CRM + Basic Invoicing

```typescript
const cardiologistSetup = {
  businessType: "healthcare_specialist",

  // Enhanced Service Management
  serviceConfiguration: {
    // Professional Requirements
    professionalType: "doctor",
    requiresLicense: true,
    certificationRequired: "ISA_CARDIOLOGY_SPECIALIST",
    professionalChamber: "medical_association_athens",

    // Service Types with Enhanced Details
    appointmentTypes: [
      {
        name: "Initial Consultation",
        duration: 45, // minutes
        bufferTime: 15, // time between appointments
        price: 80,
        isBookable: true,
        advanceBookingDays: 30,
        requiresPreparation: true,
        preparationTime: 10,
        serviceLocation: "office",
      },
      {
        name: "Follow-up Visit",
        duration: 30,
        bufferTime: 10,
        price: 50,
        isBookable: true,
        advanceBookingDays: 60,
        serviceLocation: "office",
      },
      {
        name: "ECG Test",
        duration: 20,
        bufferTime: 5,
        price: 35,
        isBookable: true,
        requiresPreparation: true,
        preparationTime: 5,
        serviceLocation: "office",
      },
      {
        name: "Home Visit",
        duration: 60,
        bufferTime: 30, // travel time
        price: 150,
        isBookable: true,
        advanceBookingDays: 7,
        serviceLocation: "client_location",
        allowsRemoteDelivery: false,
      },
    ],

    // Scheduling Configuration
    maxBookingsPerDay: 12,
    workingHours: {
      monday: { start: "09:00", end: "17:00" },
      tuesday: { start: "09:00", end: "17:00" },
      wednesday: { start: "09:00", end: "17:00" },
      thursday: { start: "09:00", end: "17:00" },
      friday: { start: "09:00", end: "15:00" },
      saturday: { closed: true },
      sunday: { closed: true },
    },

    // Recurring Services
    recurringServices: [
      {
        name: "Monthly Checkup",
        duration: 30,
        price: 50,
        isRecurring: true,
        recurringInterval: "monthly",
        recurringDuration: 12, // 12 months
      },
    ],
  },

  // CRM Configuration for Patient Management
  patientManagement: {
    customFields: [
      "medical_history",
      "insurance_provider",
      "emergency_contact",
      "allergies",
      "current_medications",
      "preferred_appointment_time",
    ],
    greekHealthcareCompliance: true,
    gdprCompliance: true,
    medicalDataEncryption: true,
  },

  // Enhanced Invoicing Configuration
  invoicing: {
    // Greek Healthcare Billing
    vatExempt: true, // Medical services exempt from VAT
    aadeIntegration: true,
    documentTypes: [
      "sales_invoice", // For private patients
      "receipt", // For cash payments
      "proforma", // For insurance pre-approval
    ],

    // Professional Compliance
    professionalChamber: "medical_association_athens",
    medicalChamberRegistration: "ISA-12345",

    // Payment Methods
    paymentMethods: [
      "cash",
      "card",
      "bank_transfer",
      "insurance_direct", // Direct insurance billing
      "installments", // For expensive procedures
    ],

    // Insurance Integration
    insuranceBilling: {
      supportedProviders: ["IKA", "EOPYY", "private_insurance"],
      directBilling: true,
      preAuthorizationRequired: true,
    },
  },

  // Service-Only Business - No Inventory Needed
  inventorySettings: {
    trackInventory: false, // Services don't need inventory
    requiresShipping: false,
    physicalProducts: false,
  },

  // No employees needed for solo practice
  additionalModules: [],

  // Service-Specific Reports
  reportingNeeds: [
    "patient_appointment_history",
    "revenue_by_service_type",
    "insurance_billing_summary",
    "professional_chamber_reporting",
    "tax_exempt_services_report",
  ],
};
```

### **🛍️ "Aegean Treasures" - Tourist Gift Shop**

**Package**: Small Business Bundle (€129/month)
**Modules**: CRM + Product Catalog + Financial Management + Advanced Inventory

```typescript
const giftShopSetup = {
  businessType: "retail_tourism",

  // Product Management (thousands of items)
  productCatalog: {
    categories: ["jewelry", "ceramics", "textiles", "food_products"],
    variants: {
      jewelry: ["material", "size"],
      textiles: ["color", "size", "pattern"],
      ceramics: ["size", "design"],
    },
    suppliers: ["local_artisans", "wholesale_athens", "import_turkey"],
  },

  // Multi-location inventory
  locations: [
    { name: "Mykonos Store", type: "retail", peak_season: "apr_oct" },
    { name: "Santorini Store", type: "retail", peak_season: "may_sep" },
    { name: "Athens Warehouse", type: "warehouse", year_round: true },
  ],

  // Seasonal business patterns
  seasonalManagement: {
    peakSeason: { months: [4, 5, 6, 7, 8, 9, 10], stockMultiplier: 3 },
    offSeason: { months: [11, 12, 1, 2, 3], stockMultiplier: 0.5 },
    tourismTax: true,
    currencySupport: ["EUR", "USD", "GBP"], // Tourist currencies
  },

  // Customer segments
  customerTypes: [
    "local_customers",
    "greek_tourists",
    "international_tourists",
  ],

  // Greek business features
  greekFeatures: {
    islandVatReduction: true, // Reduced VAT rates for islands
    tourismReporting: true,
    customsDocumentation: true, // For imported goods
  },
};
```

### **🏗️ "Hellenic Construction Ltd" - Construction Company**

**Package**: Complete Business Suite (€199/month)
**Modules**: All modules included

```typescript
const constructionSetup = {
  businessType: "construction_engineering",

  // Project-based CRM
  projectManagement: {
    projectTypes: ["residential", "commercial", "infrastructure", "renovation"],
    clientTypes: [
      "private_individuals",
      "developers",
      "government",
      "eu_projects",
    ],
    projectStages: [
      "planning",
      "permits",
      "construction",
      "completion",
      "warranty",
    ],
  },

  // Complex inventory (materials, equipment, tools)
  inventory: {
    materialCategories: ["cement", "steel", "aggregates", "tools", "equipment"],
    supplierTypes: ["local_suppliers", "multinational", "specialized"],
    projectAllocation: true, // Track materials per project
    equipmentRental: true,
  },

  // Employee management with Greek labor compliance
  humanResources: {
    employeeTypes: [
      {
        role: "construction_worker",
        ika_required: true,
        safety_training: true,
      },
      {
        role: "foreman",
        tee_membership: false,
        experience_required: "5_years",
      },
      { role: "engineer", tee_membership: true, continuing_education: true },
      {
        role: "project_manager",
        tee_membership: true,
        certification_required: true,
      },
    ],
    greekLaborLaw: {
      overtimeRules: "construction_specific",
      safetyRequirements: true,
      seasonalWork: true,
      foreignWorkers: true, // EU/non-EU documentation
    },
  },

  // Financial management with project accounting
  financialManagement: {
    projectAccounting: true,
    progressBilling: true, // Bill clients based on project progress
    costCenters: "per_project",
    cashFlowManagement: true, // Critical for construction
    retentionAccounting: true, // Hold percentage until project completion
  },

  // Business intelligence for project profitability
  analytics: {
    projectProfitability: true,
    laborCostTracking: true,
    materialCostVariance: true,
    equipmentUtilization: true,
    clientPaymentAnalysis: true,
  },

  // Greek construction compliance
  greekCompliance: {
    technicalChamber: true, // TEE membership verification
    buildingPermits: true,
    safetyInspections: true,
    environmentalCompliance: true,
    laborInspectorate: true,
  },
};
```

---

## 🔧 Technical Architecture

### **Module Dependencies Tree**

```
CRM (Base System)
├── Basic Invoicing (€19) - No dependencies
├── Product Catalog (€29) - No dependencies
├── Financial Management (€39) - Requires: Basic Invoicing
│   ├── HR & Payroll (€59) - Requires: Financial Management
│   └── Business Intelligence (€69) - Requires: Financial Management
└── Advanced Inventory (€49) - Requires: Product Catalog
```

### **Smart Module Suggestions**

```typescript
const moduleRecommendations = {
  // Trigger: Customer manually creates 15+ products in Basic Invoicing
  suggest_product_catalog: {
    trigger: "manual_product_creation >= 15",
    currentModule: "basic_invoicing",
    suggestedModule: "product_catalog",
    message: "Upgrade to Product Catalog for better inventory management",
    benefit: "Organize products, track variants, manage stock levels",
    discount: "50% off first month",
  },

  // Trigger: Frequent out-of-stock issues
  suggest_advanced_inventory: {
    trigger: "out_of_stock_events >= 5_per_month",
    currentModule: "product_catalog",
    suggestedModule: "advanced_inventory",
    message: "Add Advanced Inventory to prevent stockouts",
    benefit: "Automated reordering, supplier management, multi-location",
    incentive: "Free setup and training",
  },

  // Trigger: Manual employee expense entries
  suggest_hr_module: {
    trigger: "employee_expense_entries >= 20_per_month",
    currentModule: "financial_management",
    suggestedModule: "hr_payroll",
    message: "Automate payroll with HR Module",
    benefit: "Save 15+ hours per month, ensure Greek compliance",
    roi: "Pays for itself in time savings",
  },

  // Trigger: Frequent custom report requests
  suggest_business_intelligence: {
    trigger: "custom_report_requests >= 10",
    currentModule: "financial_management",
    suggestedModule: "business_intelligence",
    message: "Get instant insights with BI Module",
    benefit: "Self-service dashboards, predictive analytics",
    demo: "Free 2-week trial available",
  },
};
```

### **Seamless Data Flow**

```typescript
// Unified Business Data Model
interface UnifiedBusinessData {
  // Customer data (shared across all modules)
  customers: {
    crmData: CustomerProfile; // From CRM module
    invoicingData: BillingInfo; // From invoicing module
    financialData: AccountBalance; // From financial module
    greekData: GreekTaxInfo; // Shared compliance data
  };

  // Product data (when catalog module active)
  products: {
    catalogData: ProductInfo; // From product catalog
    inventoryData: StockLevels; // From inventory module
    salesData: SalesHistory; // From CRM opportunities
    financialData: CostPricing; // From financial module
  };

  // Employee data (when HR module active)
  employees: {
    hrData: EmployeeProfile; // From HR module
    payrollData: SalaryInfo; // From payroll calculations
    timeData: AttendanceRecord; // From time tracking
    performanceData: ReviewData; // From performance management
  };

  // Financial data (when financial module active)
  finances: {
    transactionData: Transaction; // All financial transactions
    reportingData: FinancialReport; // Generated reports
    complianceData: AADESubmission; // Greek tax submissions
    analyticsData: BusinessMetrics; // From BI module
  };
}
```

---

## 🚀 Implementation Strategy

### **Phase 1: Core Modules (Month 1-3)**

1. **Basic Invoicing**: Essential for immediate revenue
2. **Product Catalog**: Foundation for product-based businesses
3. **CRM Integration**: Seamless customer data flow

### **Phase 2: Advanced Features (Month 4-6)**

1. **Financial Management**: Complete accounting system
2. **Advanced Inventory**: Multi-location and automation
3. **Smart Upgrade Detection**: AI-powered module suggestions

### **Phase 3: Business Intelligence (Month 7-9)**

1. **HR & Payroll**: Complete employee management
2. **Business Intelligence**: Advanced analytics and reporting
3. **Advanced Integrations**: Third-party system connections

### **Phase 4: Enterprise Features (Month 10-12)**

1. **Custom Modules**: Industry-specific requirements
2. **Enterprise Support**: Dedicated account management
3. **Advanced Compliance**: Complex regulatory requirements

---

This modular ERP approach ensures businesses can start small and grow organically, while maintaining seamless integration between all business functions and comprehensive Greek compliance throughout their journey.
