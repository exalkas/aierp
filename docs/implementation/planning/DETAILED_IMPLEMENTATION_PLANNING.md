# Detailed Implementation Planning - Greek ERP/CRM System

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: Complete screen-by-screen implementation plan
- **Scope**: All features from 27 specification documents

## Executive Summary

This document provides a **comprehensive screen-by-screen breakdown** of the entire Greek ERP/CRM system, mapping every feature to specific screens, models, APIs, hooks, components, and tests across all applications.

### Key Market Differentiator

**Bridging the Greek CRM+ERP Gap**: Currently in the Greek market, CRM and ERP systems are completely disconnected. Businesses struggle with:

- Separate systems that don't communicate
- Duplicate data entry between sales and accounting
- No unified customer view across departments
- Manual processes to sync customer information
- Expensive integrations that rarely work well

**Our Solution**: A unified CRM+ERP platform where:

- Customer data flows seamlessly from leads to invoices
- Sales teams and accounting work from the same system
- Greek compliance is built into both CRM and ERP modules
- Dynamic entity management allows businesses to customize both sides
- No integration needed - it's one system from the start

---

## 1. APPLICATION ARCHITECTURE

### 1.1 Multiple Applications Structure

We need to build **4 applications**:

1. **Client Application** - Main business operations (responsive web app)
2. **Admin Application** - System administration
3. **Support Application** - Customer support
4. **Setup Application** - Onboarding and migration

### 1.2 Deployment Models

The system will support **2 deployment options**:

1. **Cloud SAAS** - Webapp running in cloud infrastructure

   - Multi-tenant architecture
   - Automatic updates and scaling
   - Pay-per-use pricing model

2. **Local Installation** - Webapp running locally at client premises

   - On-site installation by technical team
   - Remote support and maintenance
   - Full customization capabilities
   - Offline capability for critical operations

### 1.3 Mobile Access Strategy

Instead of native mobile apps, we provide **excellent mobile browser experience**:

- **Progressive Web App (PWA)** - App-like experience in mobile browsers
- **Responsive Design** - Optimal viewing on all screen sizes
- **Touch-Optimized UI** - Mobile-friendly interactions
- **Offline Capability** - PWA features for offline access
- **Push Notifications** - Browser-based notifications
- **Camera Integration** - Mobile camera access for documents/receipts
- **Installation Prompt** - "Add to Home Screen" for app-like access
- **Native Feel** - Fullscreen mode, splash screens, app icons

### 1.4 Deployment Considerations

**Cloud SAAS Deployment:**

- Docker containers with load balancing
- Auto-scaling based on usage
- CDN for global performance
- Automated backup and monitoring

**Local Installation Deployment:**

- **Multi-Platform Native Installation** (No Docker - compatible with all major operating systems)
- **Platform-Specific Installer Packages**:
  - **Windows**: .msi installer with automated dependency management
  - **macOS**: .pkg installer with Homebrew integration
  - **Linux**: .deb/.rpm packages with native package managers
- **Automated Component Installation** (all platforms):
  - PostgreSQL 16+ (platform-appropriate installation)
  - Python 3.12+ runtime with required packages
  - Redis 7.2+ as system service
  - Node.js 20+ for frontend build tools
- **Support Monitoring System**:
  - **Installation Tracking**: Complete history of all changes and updates
  - **Remote Diagnostics Agent**: Real-time system health monitoring
  - **Configuration Registry**: All settings and customizations tracked
  - **Automatic Log Collection**: Error logs, performance metrics, usage data
  - **Support Dashboard**: Real-time visibility into customer installations
- **Secure Support Access**:
  - Encrypted support tunnel for remote assistance
  - Session recording for troubleshooting
  - Remote desktop capability when authorized
- **Update Management**:
  - Automated update notifications
  - Rollback capability for failed updates
  - Staged deployment testing

### 1.5 Local Installation Support Monitoring

**Installation Tracking Models:**

```typescript
interface LocalInstallation {
  id: string;
  companyId: string;
  installationId: string; // Unique per installation

  // Installation Details
  version: string;
  installedComponents: InstalledComponent[];
  installationDate: Date;
  lastUpdateDate: Date;

  // System Information
  operatingSystem: "windows" | "macos" | "linux";
  osVersion: string;
  architecture: "x64" | "arm64";
  hardwareSpecs: HardwareSpecs;
  networkConfiguration: NetworkConfig;

  // Configuration
  databaseConfig: DatabaseConfig;
  customizations: Customization[];
  integrations: Integration[];

  // Support Access
  supportTunnelEnabled: boolean;
  lastSupportSession?: Date;
  supportHistory: SupportSession[];

  // Monitoring
  healthStatus: "healthy" | "warning" | "critical" | "offline";
  lastHeartbeat: Date;
  performanceMetrics: PerformanceMetrics[];
}

interface SupportSession {
  id: string;
  installationId: string;
  supportUserId: string;
  startTime: Date;
  endTime?: Date;
  sessionType: "remote_desktop" | "diagnostic" | "update" | "troubleshooting";
  actions: SupportAction[];
  resolution?: string;
}

interface SystemChangeLog {
  id: string;
  installationId: string;
  changeType: "update" | "configuration" | "customization" | "integration";
  component: string;
  beforeValue: any;
  afterValue: any;
  changeDate: Date;
  initiatedBy: "user" | "support" | "system";
  reason: string;
}
```

**Support Dashboard Features:**

- **Real-time Installation Map**: All customer installations with status indicators
- **Health Monitoring**: CPU, memory, disk usage, database performance
- **Change History**: Complete audit trail of all modifications
- **Alert System**: Automated alerts for critical issues or failures
- **Remote Diagnostics**: One-click access to system logs and configuration
- **Update Deployment**: Controlled rollout of updates with rollback capability
- **Performance Analytics**: Historical performance trends and optimization recommendations

### 1.6 Platform-Specific Implementation Details

**Windows Installation:**

```bash
# Windows Installer (.msi)
- Silent PostgreSQL installation with Windows service
- Python 3.12+ with pip packages pre-installed
- Redis as Windows service
- IIS or standalone Kestrel for web server
- Windows Task Scheduler for background jobs
- Windows Event Log integration
```

**macOS Installation:**

```bash
# macOS Package (.pkg)
- Homebrew integration for dependencies:
  brew install postgresql@16 python@3.12 redis node@20
- launchd services for background processes
- Keychain integration for secure credential storage
- macOS notification center integration
- Built-in macOS backup integration (Time Machine compatible)
```

**Linux Installation:**

```bash
# Ubuntu/Debian (.deb package)
sudo apt update
sudo apt install postgresql-16 python3.12 redis-server nodejs

# CentOS/RHEL (.rpm package)
sudo yum install postgresql16-server python312 redis nodejs

# Systemd services for all background processes
# Native Linux package management
# SELinux compatibility for enterprise environments
```

**Cross-Platform Service Management:**

```typescript
interface PlatformService {
  platform: "windows" | "macos" | "linux";
  serviceName: string;
  serviceManager: "systemctl" | "launchctl" | "sc.exe";
  configPath: string;
  logPath: string;

  // Platform-specific commands
  startCommand: string;
  stopCommand: string;
  restartCommand: string;
  statusCommand: string;
}

// Examples:
const postgresqlService: PlatformService[] = [
  {
    platform: "windows",
    serviceName: "postgresql-x64-16",
    serviceManager: "sc.exe",
    startCommand: "sc start postgresql-x64-16",
    configPath: "C:\\Program Files\\PostgreSQL\\16\\data\\postgresql.conf",
  },
  {
    platform: "macos",
    serviceName: "postgresql@16",
    serviceManager: "launchctl",
    startCommand: "brew services start postgresql@16",
    configPath: "/opt/homebrew/var/postgresql@16/postgresql.conf",
  },
  {
    platform: "linux",
    serviceName: "postgresql",
    serviceManager: "systemctl",
    startCommand: "sudo systemctl start postgresql",
    configPath: "/etc/postgresql/16/main/postgresql.conf",
  },
];
```

**Platform Benefits:**

✅ **Windows**: Largest market share in Greek businesses, enterprise integration  
✅ **macOS**: Growing market, excellent for design agencies, modern Greek startups  
✅ **Linux**: Cost-effective for larger businesses, popular in tech companies  
✅ **Same Support Dashboard**: Unified monitoring regardless of customer's OS  
✅ **Reduced TCO**: Customers can use existing hardware/OS preferences

---

## 2. CLIENT APPLICATION SCREENS

### 2.1 Authentication & User Management (7 screens)

**Screens List:**

1. `/login` - Login Screen
2. `/register` - Register Screen
3. `/reset-password` - Reset Password Screen
4. `/profile` - Profile Management Screen
5. `/users` - User Management Screen
6. `/roles` - Role Management Screen
7. `/permissions` - Permission Management Screen

**Models Needed:**

```typescript
interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: Role;
  companyId: string;
  isActive: boolean;
  greekCertifications: GreekCertification[];
}

interface Role {
  id: string;
  name: string;
  permissions: Permission[];
  greekProfessionalRequirements: GreekProfessionalRequirement[];
}

interface Permission {
  id: string;
  resource: string;
  action: string;
  greekComplianceLevel: "basic" | "professional" | "enterprise";
}
```

**API Endpoints:**

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/reset-password` - Password reset
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `PUT /api/users/:id` - Update user
- `GET /api/roles` - List roles
- `POST /api/roles` - Create role

**Custom Hooks:**

- `useAuth()` - Authentication state
- `useUsers()` - User management
- `useRoles()` - Role management
- `usePermissions()` - Permission checking
- `useGreekCertifications()` - Greek certification management
- `useAuthTranslation()` - Authentication-specific translations
- `useUserLanguagePreferences()` - User language settings
- `useAuthLocalization()` - Authentication localization

**Components:**

- `LoginForm` - Login form with MFA
- `RegisterForm` - Registration with Greek validation
- `UserCard` - User display card
- `RoleSelector` - Role dropdown
- `GreekCertificationBadge` - Certification display
- `MultilingualLoginForm` - Login form with language selection
- `LanguagePreferencesForm` - User language preferences form
- `LocalizedErrorMessage` - Error messages in user's language
- `AuthTranslationProvider` - Authentication translation context

### 2.2 Dynamic Entity Management (7 screens)

**Screens List:**

1. `/admin/entities/builder` - Entity Builder Screen
2. `/admin/entities` - Entity List Screen
3. `/admin/entities/:id` - Entity Detail Screen
4. `/admin/entities/:id/fields` - Field Builder Screen
5. `/admin/entities/:id/relationships` - Relationship Builder Screen
6. `/entities/:entityType` - Dynamic Entity Data Screen
7. `/entities/:entityType/:id` - Dynamic Entity Detail Screen

**Models Needed:**

```typescript
interface DynamicEntity {
  id: string;
  name: string;
  pluralName: string;
  fields: DynamicField[];
  relationships: EntityRelationship[];
  greekCompliance: GreekComplianceConfig;
  customizationLevel: "platform" | "module" | "custom" | "enterprise";
}

interface DynamicField {
  id: string;
  name: string;
  type: FieldType;
  required: boolean;
  greekValidation: GreekFieldValidation;
}
```

**API Endpoints:**

- `GET /api/entities` - List entities
- `POST /api/entities` - Create entity
- `PUT /api/entities/:id` - Update entity
- `POST /api/entities/:id/fields` - Add field
- `GET /api/data/:entityType` - Get entity data
- `POST /api/data/:entityType` - Create entity record

**Custom Hooks:**

- `useEntityBuilder()` - Entity creation
- `useFieldBuilder()` - Field management
- `useDynamicData()` - Dynamic entity data
- `useEntityPermissions()` - Entity permissions
- `useEntityTranslation()` - Entity name and description translations
- `useFieldTranslation()` - Field label and help text translations
- `useDynamicFormTranslation()` - Dynamic form translations
- `useEntityValidationTranslation()` - Entity validation message translations
- `useMultilingualEntityData()` - Entity data in multiple languages

**Components:**

- `EntityBuilder` - Drag-drop entity builder
- `FieldBuilder` - Field creation form
- `DynamicForm` - Auto-generated forms
- `DynamicTable` - Auto-generated tables
- `GreekFieldValidator` - Greek field validation
- `MultilingualEntityBuilder` - Entity builder with translation support
- `FieldTranslationPanel` - Field translation management
- `DynamicMultilingualForm` - Auto-generated forms with translations
- `EntityTranslationManager` - Entity translation management
- `MultilingualFieldValidator` - Field validation with translated messages
- `DynamicEntityLanguageSelector` - Language selector for dynamic entities

### 2.3 CRM Module (23 screens)

**Key Features**:

- **EspoCRM-Style Customization** - Users can create custom entities, fields, and workflows directly from the CRM interface without technical knowledge
- **Import/Export & ETL Integration** - Seamless data migration with shared ETL infrastructure
- **Messaging Platform Integration** - WhatsApp, Viber, Telegram integration for mobile sales teams

**Implementation Priority for Messaging:**

1. **WhatsApp Business API** (Priority 1) - Most used in Greek market
2. **Viber Public Accounts** (Priority 2) - Popular alternative in Greece
3. **Telegram Bot API** (Priority 3) - Easier to implement, good for internal teams

**Screens List:**

1. `/crm/dashboard` - CRM Dashboard
2. `/crm/accounts` - Account List (Companies/Organizations)
3. `/crm/accounts/:id` - Account Detail
4. `/crm/contacts` - Contact List (People within accounts)
5. `/crm/contacts/:id` - Contact Detail
6. `/crm/leads` - Lead List
7. `/crm/leads/:id` - Lead Detail
8. `/crm/opportunities` - Opportunity Pipeline
9. `/crm/opportunities/:id` - Opportunity Detail
10. `/crm/activities` - Activity Timeline
11. `/crm/reports` - Sales Reports
12. `/crm/lead-forms` - Lead Capture Forms
13. `/crm/entities` - Custom Entity Management
14. `/crm/entities/create` - Create New Entity
15. `/crm/entities/:entityType` - Custom Entity Data
16. `/crm/entities/:entityType/:id` - Custom Entity Detail
17. `/crm/entity-builder` - Visual Entity Builder
18. `/crm/import-export` - Import/Export Data Management
19. `/crm/import-export/csv` - CSV Import/Export
20. `/crm/import-export/templates` - Data Templates
21. `/crm/messaging` - Messaging Platform Integration
22. `/crm/messaging/setup` - WhatsApp/Viber/Telegram Setup
23. `/crm/messaging/conversations` - Message Conversations

**CRM+ERP Integration Examples:**

- Lead converts to Account → Account automatically available in ERP for invoicing
- Opportunity closed → Automatically creates ERP Project for delivery
- Account Greek tax info → Shared with ERP for compliant invoicing
- Custom CRM fields → Available in ERP documents and reports
- Sales activities → Linked to ERP payments and project timelines

**Mobile Sales Team Use Cases:**

- **WhatsApp Integration**: "Send me info about client ABC" → System responds with account details
- **Quick Updates**: "Update ABC status to qualified" → Lead status updated in CRM
- **Meeting Notes**: Voice message → Converted to text and added to activity timeline
- **Contact Creation**: "Create contact John Doe at ABC Corp" → New contact added with company link
- **Opportunity Updates**: "ABC deal moved to proposal stage" → Pipeline updated automatically
- **Document Sharing**: Send contract via WhatsApp → Automatically logged in CRM

**ETL Integration Benefits:**

- **Shared Infrastructure**: Import/export uses same ETL engine as migration system
- **Greek Data Validation**: Reuses Greek compliance validation from ETL system
- **Template Library**: Common templates for Greek business data formats
- **Error Handling**: Consistent error reporting across CRM and ETL systems
- **Scheduled Imports**: Automated data synchronization from external systems

**Models Needed:**

```typescript
interface Account {
  id: string;
  companyName: string;
  type: "prospect" | "customer" | "partner" | "vendor";
  industry: string;
  website: string;
  email: string;
  phone: string;
  address: GreekAddress;
  greekTaxInfo: GreekTaxInfo;

  // File Attachments
  contracts: FileRecord[];
  legalDocuments: FileRecord[];
  taxDocuments: FileRecord[];
  correspondence: FileRecord[];
  generalFiles: FileRecord[];

  customFields: Record<string, any>;
  contacts: Contact[];
  opportunities: Opportunity[];
}

interface Contact {
  id: string;
  accountId: string;
  account: Account;
  firstName: string;
  lastName: string;
  jobTitle: string;
  email: string;
  phone: string;
  mobile: string;
  isPrimary: boolean;
  customFields: Record<string, any>;
}

interface Lead {
  id: string;
  firstName: string;
  lastName: string;
  companyName: string;
  email: string;
  phone: string;
  source: string;
  status: LeadStatus;
  score: number;
  customFields: Record<string, any>;
}

interface Opportunity {
  id: string;
  title: string;
  accountId: string;
  account: Account;
  contactId?: string;
  contact?: Contact;
  value: number;
  stage: OpportunityStage;
  probability: number;
  expectedCloseDate: Date;
  customFields: Record<string, any>;
}

interface ImportExportJob {
  id: string;
  type: "import" | "export";
  entityType: string;
  format: "csv" | "xlsx" | "json";
  status: "pending" | "processing" | "completed" | "failed";
  filename: string;
  totalRecords: number;
  processedRecords: number;
  errorCount: number;
  createdBy: string;
  createdAt: Date;
  mapping: FieldMapping[];
}

interface FieldMapping {
  sourceField: string;
  targetField: string;
  transformation?: string;
  greekValidation?: boolean;
}

interface MessagingConversation {
  id: string;
  platform: "whatsapp" | "viber" | "telegram";
  contactId: string;
  contact: Contact;
  phoneNumber: string;
  lastMessage: string;
  lastMessageAt: Date;
  unreadCount: number;
  isActive: boolean;
}

interface MessagingMessage {
  id: string;
  conversationId: string;
  direction: "inbound" | "outbound";
  content: string;
  messageType: "text" | "image" | "document" | "voice" | "location";
  timestamp: Date;
  isRead: boolean;
  crmAction?: "create_lead" | "update_contact" | "log_activity";
}
```

**API Endpoints:**

- `GET /api/crm/accounts` - List accounts
- `POST /api/crm/accounts` - Create account
- `PUT /api/crm/accounts/:id` - Update account
- `GET /api/crm/contacts` - List contacts
- `POST /api/crm/contacts` - Create contact
- `PUT /api/crm/contacts/:id` - Update contact
- `GET /api/crm/leads` - List leads
- `POST /api/crm/leads` - Create lead
- `POST /api/crm/leads/:id/convert` - Convert lead to account/contact
- `GET /api/crm/opportunities` - List opportunities
- `POST /api/crm/opportunities` - Create opportunity
- `PUT /api/crm/opportunities/:id` - Update opportunity
- `GET /api/crm/entities` - List custom entities
- `POST /api/crm/entities` - Create custom entity
- `PUT /api/crm/entities/:id` - Update custom entity
- `DELETE /api/crm/entities/:id` - Delete custom entity
- `GET /api/crm/data/:entityType` - Get custom entity data
- `POST /api/crm/data/:entityType` - Create custom entity record
- `PUT /api/crm/data/:entityType/:id` - Update custom entity record
- `DELETE /api/crm/data/:entityType/:id` - Delete custom entity record
- `POST /api/crm/import` - Start import job
- `GET /api/crm/import/:jobId` - Get import job status
- `POST /api/crm/export` - Start export job
- `GET /api/crm/export/:jobId` - Get export job status
- `GET /api/crm/export/:jobId/download` - Download export file
- `POST /api/crm/import/validate` - Validate import data
- `GET /api/crm/import/templates` - Get import templates
- `POST /api/crm/messaging/webhook` - Messaging webhook endpoint
- `GET /api/crm/accounts/:id/files` - Get account files
- `POST /api/crm/accounts/:id/files` - Upload files to account
- `DELETE /api/crm/accounts/:id/files/:fileId` - Remove file from account
- `GET /api/crm/contacts/:id/files` - Get contact files
- `POST /api/crm/contacts/:id/files` - Upload files to contact
- `GET /api/crm/messaging/conversations` - List conversations
- `POST /api/crm/messaging/conversations` - Create conversation
- `GET /api/crm/messaging/conversations/:id/messages` - Get conversation messages
- `POST /api/crm/messaging/conversations/:id/messages` - Send message
- `POST /api/crm/messaging/setup` - Setup messaging platform
- `PUT /api/crm/messaging/setup/:platform` - Update platform settings

**Custom Hooks:**

- `useAccounts()` - Account management
- `useContacts()` - Contact management
- `useLeads()` - Lead management
- `useOpportunities()` - Opportunity management
- `useSalesPipeline()` - Sales pipeline
- `useLeadConversion()` - Lead to account/contact conversion
- `useCRMEntities()` - CRM entity management
- `useCRMEntityBuilder()` - CRM entity builder
- `useCRMEntityData()` - CRM entity data management
- `useCRMEntityPermissions()` - CRM entity permissions
- `useImportExport()` - Import/export job management
- `useImportValidation()` - Import data validation
- `useExportTemplates()` - Export template management
- `useMessagingConversations()` - Messaging conversations
- `useMessagingMessages()` - Message management
- `useMessagingSetup()` - Platform setup and configuration
- `useMessagingWebhook()` - Webhook handling for incoming messages
- `useCRMTranslation()` - CRM-specific translations
- `useMultilingualCustomerData()` - Customer data in multiple languages
- `useMessagingTranslation()` - Messaging translations for WhatsApp/Viber/Telegram
- `useCRMEntityTranslation()` - Custom entity translations
- `useActivityTranslation()` - Activity translations
- `useSalesTerminology()` - Sales terminology in multiple languages

**Components:**

- `AccountCard` - Account display
- `ContactCard` - Contact display
- `LeadCard` - Lead display
- `SalesPipeline` - Drag-drop pipeline
- `ActivityTimeline` - Activity timeline
- `GreekTaxInfoForm` - Greek tax form
- `LeadConversionWizard` - Lead conversion process
- `CRMEntityBuilder` - CRM entity builder
- `CRMEntityCard` - Custom entity display
- `CRMEntityForm` - Custom entity form
- `CRMEntityTable` - Custom entity table
- `ImportExportWizard` - Import/export wizard
- `DataMappingTool` - Field mapping interface
- `ImportValidationResults` - Import validation display
- `ExportTemplateBuilder` - Export template creator
- `MessagingConversationList` - Conversation list
- `MessagingChatWindow` - Chat interface
- `MessagingSetupForm` - Platform setup form
- `QuickMessageActions` - Quick CRM actions from messages
- `MultilingualCustomerForm` - Customer form with multilingual support
- `LocalizedActivityTimeline` - Activity timeline with translations
- `MessagingLanguageSelector` - Language selector for messaging
- `TranslatedMessageTemplate` - Message templates in multiple languages
- `CRMEntityTranslationPanel` - Entity translation management
- `MultilingualSalesPipeline` - Sales pipeline with localized stages
- `LocalizedReportsGenerator` - CRM reports in user's language
- `CustomerLanguagePreferences` - Customer language settings

### 2.4 ERP Financial Module (15 screens)

**Screens List:**

1. `/erp/dashboard` - Financial Dashboard
2. `/erp/invoices` - Invoice List
3. `/erp/invoices/:id` - Invoice Detail
4. `/erp/invoices/create` - Invoice Creator
5. `/erp/products` - Product List
6. `/erp/products/:id` - Product Detail
7. `/erp/inventory` - Inventory Management
8. `/erp/payments` - Payment List
9. `/erp/payments/:id` - Payment Detail
10. `/erp/reports` - Financial Reports
11. `/erp/tax` - Tax Management
12. `/erp/banking` - Bank Reconciliation
13. `/erp/customer-statements` - Customer Statements Management (Καταστάσεις Πελατών)
14. `/erp/customer-statements/create` - Customer Statement Generator
15. `/erp/customer-statements/:id` - Customer Statement Detail & Preview

**Models Needed:**

```typescript
interface Invoice {
  id: string;
  invoiceNumber: string;
  accountId: string;
  account: Account;
  contactId?: string;
  contact?: Contact;
  items: InvoiceItem[];
  total: number;
  greekTaxInfo: GreekInvoiceTaxInfo;
  aadeInfo: AADEInfo;

  // File Attachments
  attachments: FileRecord[];
  invoicePdf?: FileRecord;
  receiptPdf?: FileRecord;
  supportingDocuments: FileRecord[];

  customFields: Record<string, any>;
}

interface Product {
  id: string;
  name: string;
  price: number;
  stockQuantity: number;
  greekTaxCategory: GreekTaxCategory;

  // File Attachments
  images: FileRecord[];
  specifications: FileRecord[];
  documentation: FileRecord[];
  certificates: FileRecord[];

  customFields: Record<string, any>;
}

interface Payment {
  id: string;
  invoice: Invoice;
  amount: number;
  greekBankingInfo: GreekBankingInfo;
  customFields: Record<string, any>;
}

interface CustomerStatement {
  id: string;
  statementNumber: string;
  customerId: string;
  customer: Account;

  // Statement Details
  statementType: "monthly" | "quarterly" | "annual" | "on_demand";
  periodStart: Date;
  periodEnd: Date;
  generatedDate: Date;
  dueDate?: Date;

  // Balances
  openingBalance: number;
  closingBalance: number;
  totalTransactions: number;
  totalPayments: number;
  totalCredits: number;
  outstandingAmount: number;

  // Greek Compliance
  aadeCompliant: boolean;
  aadeSubmissionId?: string;
  aadeSubmissionDate?: Date;
  aadeStatus: "pending" | "submitted" | "accepted" | "rejected";

  // Document Management
  pdfFile?: FileRecord;
  pdfGeneratedDate?: Date;
  emailSent: boolean;
  emailSentDate?: Date;

  // Metadata
  createdBy: string;
  approvedBy?: string;
  status: "draft" | "generated" | "sent" | "filed";

  // Relationships
  transactions: CustomerStatementTransaction[];
  payments: CustomerStatementPayment[];
  customFields: Record<string, any>;
}

interface CustomerStatementTransaction {
  id: string;
  statementId: string;

  // Transaction Details
  date: Date;
  type: "invoice" | "payment" | "credit" | "debit" | "adjustment";
  referenceNumber: string;
  description: string;
  amount: number;
  runningBalance: number;

  // VAT Information
  netAmount?: number;
  vatAmount?: number;
  vatRate?: number;

  // Greek Compliance
  aadeTransactionId?: string;
  invoiceType?: string;

  // Relationships
  sourceInvoiceId?: string;
  sourcePaymentId?: string;
}

interface CustomerStatementPayment {
  id: string;
  statementId: string;
  date: Date;
  amount: number;
  paymentMethod: string;
  referenceNumber: string;
  notes?: string;
}

interface CustomerStatementConfiguration {
  id: string;
  companyId: string;

  // Automatic Generation Settings
  monthlyEnabled: boolean;
  quarterlyEnabled: boolean;
  annualEnabled: boolean;

  // Generation Rules
  minimumAmountThreshold: number;
  includeZeroBalanceCustomers: boolean;
  includeDormantCustomers: boolean;

  // Formatting Options
  language: "greek" | "english" | "bilingual";
  includeVATDetails: boolean;
  includePaymentTerms: boolean;
  includeAgingAnalysis: boolean;
  includeCompanySeal: boolean;

  // AADE Integration
  autoSubmitToAADE: boolean;
  aadeSubmissionDelay: number; // days

  // Email Settings
  autoEmailToCustomers: boolean;
  emailTemplate: string;
  emailSubjectTemplate: string;

  // Scheduling
  monthlyGenerationDay: number; // 1-31
  quarterlyGenerationDay: number;
  annualGenerationDay: number;
}
```

**API Endpoints:**

- `GET /api/erp/invoices` - List invoices
- `POST /api/erp/invoices` - Create invoice
- `POST /api/erp/invoices/:id/aade` - Submit to AADE
- `GET /api/erp/products` - List products
- `POST /api/erp/products` - Create product
- `GET /api/erp/payments` - List payments
- `POST /api/erp/payments` - Create payment
- `GET /api/erp/invoices/:id/files` - Get invoice attachments
- `POST /api/erp/invoices/:id/files` - Upload files to invoice
- `DELETE /api/erp/invoices/:id/files/:fileId` - Remove file from invoice
- `GET /api/erp/products/:id/files` - Get product files
- `POST /api/erp/products/:id/files` - Upload files to product

**Customer Statements API Endpoints:**

- `GET /api/erp/customer-statements` - List customer statements
- `POST /api/erp/customer-statements` - Create customer statement
- `GET /api/erp/customer-statements/:id` - Get statement details
- `PUT /api/erp/customer-statements/:id` - Update statement
- `DELETE /api/erp/customer-statements/:id` - Delete statement
- `POST /api/erp/customer-statements/generate` - Generate statements for period
- `POST /api/erp/customer-statements/generate/monthly` - Generate monthly statements
- `POST /api/erp/customer-statements/generate/quarterly` - Generate quarterly statements
- `POST /api/erp/customer-statements/generate/annual` - Generate annual statements
- `GET /api/erp/customer-statements/:id/pdf` - Generate statement PDF
- `POST /api/erp/customer-statements/:id/email` - Send statement via email
- `POST /api/erp/customer-statements/:id/aade` - Submit statement to AADE
- `GET /api/erp/customer-statements/:id/preview` - Preview statement content
- `GET /api/erp/customer-statements/configuration` - Get statement configuration
- `PUT /api/erp/customer-statements/configuration` - Update statement configuration
- `GET /api/erp/customer-statements/templates` - Get statement templates
- `POST /api/erp/customer-statements/batch/email` - Send multiple statements via email
- `POST /api/erp/customer-statements/batch/aade` - Submit multiple statements to AADE
- `GET /api/erp/customer-statements/analytics` - Get statement analytics

**Custom Hooks:**

- `useInvoices()` - Invoice management
- `useProducts()` - Product management
- `usePayments()` - Payment management
- `useAADEIntegration()` - AADE integration
- `useGreekTaxCalculation()` - Tax calculations
- `useERPTranslation()` - ERP-specific translations
- `useMultilingualInvoicing()` - Multilingual invoice generation
- `useProductTranslation()` - Product descriptions in multiple languages
- `useFinancialReportTranslation()` - Financial reports in multiple languages
- `useGreekComplianceTranslation()` - Greek compliance form translations
- `useMultilingualDocumentGeneration()` - Document generation in multiple languages

**Customer Statements Custom Hooks:**

- `useCustomerStatements()` - Customer statement management
- `useCustomerStatementGenerator()` - Statement generation logic
- `useCustomerStatementPDF()` - PDF generation for statements
- `useCustomerStatementEmail()` - Email sending for statements
- `useCustomerStatementAADE()` - AADE submission for statements
- `useCustomerStatementConfiguration()` - Statement configuration management
- `useCustomerStatementScheduler()` - Automatic statement scheduling
- `useCustomerStatementAnalytics()` - Statement analytics and reporting
- `useCustomerStatementTemplates()` - Statement template management
- `useCustomerStatementBatch()` - Batch operations for statements
- `useGreekCustomerStatements()` - Greek-specific statement features
- `useCustomerStatementTranslation()` - Statement multilingual support
- `useCustomerStatementPreview()` - Statement preview functionality
- `useCustomerStatementValidation()` - Statement validation logic

**Components:**

- `InvoiceForm` - Invoice creation form
- `ProductCard` - Product display
- `InvoicePreview` - Invoice preview
- `AADEStatusBadge` - AADE status
- `GreekTaxCalculator` - Tax calculator
- `MultilingualInvoiceForm` - Invoice form with language selection
- `LocalizedInvoicePreview` - Invoice preview in customer's language
- `ProductTranslationPanel` - Product translation management
- `MultilingualFinancialReports` - Financial reports with localization
- `GreekComplianceTranslationForm` - Greek compliance forms with translations
- `CurrencyLocalizer` - Currency display with locale formatting
- `MultilingualDocumentTemplates` - Document templates in multiple languages
- `ERPLanguageSelector` - ERP-specific language selector

**Customer Statements Components:**

- `CustomerStatementDashboard` - Statement management dashboard
- `CustomerStatementList` - Statement listing with filters
- `CustomerStatementCard` - Individual statement card display
- `CustomerStatementForm` - Statement creation and editing form
- `CustomerStatementPreview` - Statement preview modal
- `CustomerStatementPDFPreview` - PDF preview with Greek formatting
- `CustomerStatementGenerator` - Automatic statement generation interface
- `CustomerStatementConfiguration` - Statement configuration panel
- `CustomerStatementScheduler` - Automatic scheduling interface
- `CustomerStatementAnalytics` - Statement analytics dashboard
- `CustomerStatementTemplateEditor` - Template customization interface
- `CustomerStatementBatchActions` - Bulk operations panel
- `CustomerStatementAADEStatus` - AADE submission status indicator
- `CustomerStatementEmailPanel` - Email sending interface
- `GreekCustomerStatementForm` - Greek-specific statement form
- `CustomerStatementTransactionTable` - Transaction listing in statements
- `CustomerStatementSummary` - Statement summary section
- `CustomerStatementFilters` - Advanced filtering options
- `CustomerStatementExportOptions` - Export format options
- `CustomerStatementComplianceChecker` - Greek compliance validation
- `CustomerStatementLanguageSelector` - Language selection for statements

### 2.5 Business Configuration & Setup Module (8 screens)

**Screens List:**

1. `/setup/wizard` - Installation & Business Setup Wizard
2. `/setup/business-type` - Business Type Configuration
3. `/setup/vat-configuration` - Dynamic VAT Rules Management
4. `/setup/product-configuration` - Product/Service Setup by Business Type
5. `/setup/location-configuration` - Greek Location & Tax Zone Setup
6. `/setup/regulatory-updates` - Tax Law Change Management
7. `/setup/system-validation` - Configuration Testing & Validation
8. `/setup/deployment-settings` - SAAS vs Local Installation Settings

**Models Needed:**

```typescript
interface BusinessConfiguration {
  id: string;
  companyId: string;
  businessType: BusinessType;
  businessSubtype?: string;
  industry: string;
  primaryLocation: GreekBusinessLocation;
  additionalLocations: GreekBusinessLocation[];
  vatConfiguration: VATConfiguration;
  taxExemptions: TaxExemption[];
  productConfiguration: ProductConfiguration;
  serviceConfiguration: ServiceConfiguration;
  operationalSettings: OperationalSettings;
  complianceRequirements: ComplianceRequirement[];
  customFields: Record<string, any>;
  configuredBy: string;
  configuredAt: Date;
  lastUpdated: Date;
  configurationVersion: string;
}

interface GreekBusinessLocation {
  id: string;
  name: string;
  address: GreekAddress;
  locationType: "mainland" | "island" | "special_zone";
  prefecture: string;
  municipality: string;
  postalCode: string;
  doyCode: string;
  vatZone: VATZone;
  specialTaxRules: SpecialTaxRule[];
  islandGroup?:
    | "cyclades"
    | "dodecanese"
    | "ionian"
    | "aegean"
    | "crete"
    | "other";
  reducedVATEligible: boolean;
  touristArea: boolean;
  seasonalRules: SeasonalRule[];
}

interface VATCalculationContext {
  businessType: BusinessType;
  businessLocation: GreekBusinessLocation;
  customerLocation: GreekBusinessLocation;
  customerType: "individual" | "business";
  item: ProductOrService;
  itemCategory: string;
  transactionType: "sale" | "service" | "rental" | "subscription";
  deliveryMethod: "pickup" | "delivery" | "digital" | "in_person";
  consumptionMethod?: "takeaway" | "dine_in" | "online" | "offline";
  transactionDate: Date;
  season?: "peak" | "off_peak";
  serviceLocation?: GreekBusinessLocation;
  deliveryLocation?: GreekBusinessLocation;
}

interface ProductVariant {
  id: string;
  parentProductId: string;
  attributes: Record<string, string>;
  sku: string;
  price?: number;
  stockQuantity: number;
  weight?: number;
  dimensions?: ProductDimensions;
  images: string[];
  documents: string[];
}

interface VariantAttribute {
  id: string;
  name: string;
  type: "color" | "size" | "text" | "number";
  values: VariantAttributeValue[];
  required: boolean;
  displayOrder: number;
}

interface ServiceProduct {
  id: string;
  name: string;
  description: string;
  category: string;
  basePrice: number;
  currency: string;
  vatCategory: string;
  taxExempt: boolean;
  productType: "service";
  duration?: number;
  serviceType: "consultation" | "project" | "subscription" | "hourly";
  bookable: boolean;
  advanceBookingDays?: number;
  requiresLicense?: boolean;
  certificationRequired?: string[];
  businessTypeFields: Record<string, any>;
}

interface TaxRegulationUpdate {
  id: string;
  updateType:
    | "vat_rate_change"
    | "exemption_change"
    | "new_rule"
    | "location_change";
  regulationTitle: string;
  regulationNumber: string;
  publishedDate: Date;
  effectiveDate: Date;
  expiryDate?: Date;
  affectedBusinessTypes: BusinessType[];
  affectedLocations: string[];
  impactLevel: "low" | "medium" | "high" | "critical";
  oldRules: TaxRule[];
  newRules: TaxRule[];
  migrationRequired: boolean;
  implementationStatus: "pending" | "testing" | "deployed" | "completed";
  implementationNotes: string;
  customersNotified: boolean;
  notificationsSent: Date[];
  acknowledgmentRequired: boolean;
}

interface SystemRequirements {
  id: string;
  deploymentType: "saas" | "local";
  checkType: "initial" | "periodic" | "upgrade";

  // Hardware Requirements
  hardwareRequirements: HardwareRequirements;
  hardwareResults: HardwareResults;

  // Software Requirements
  softwareRequirements: SoftwareRequirements;
  softwareResults: SoftwareResults;

  // Network Requirements
  networkRequirements: NetworkRequirements;
  networkResults: NetworkResults;

  // Performance Benchmarks
  performanceBenchmarks: PerformanceBenchmarks;
  performanceResults: PerformanceResults;

  // Overall Results
  overallStatus: "passed" | "warning" | "failed";
  requirementsMet: boolean;
  warnings: string[];
  errors: string[];
  recommendations: string[];

  // Metadata
  checkedAt: Date;
  checkedBy: string;
  systemInfo: SystemInfo;
}

interface HardwareRequirements {
  minRAM: number;
  recommendedRAM: number;
  minStorage: number;
  recommendedStorage: number;
  minCPUCores: number;
  minCPUSpeed: number;
  minScreenResolution: string;
  recommendedScreenResolution: string;
}

interface HardwareResults {
  detectedRAM: number;
  availableRAM: number;
  detectedStorage: number;
  availableStorage: number;
  cpuCores: number;
  cpuSpeed: number;
  cpuModel: string;
  screenResolution: string;
  gpuInfo: string;
  ramMeetsRequirement: boolean;
  storageMeetsRequirement: boolean;
  cpuMeetsRequirement: boolean;
  screenMeetsRequirement: boolean;
}

interface SoftwareRequirements {
  operatingSystem: string[];
  browser: string[];
  browserVersion: string;
  requiredSoftware: string[];
  dotNetVersion?: string;
  pythonVersion?: string;
  nodeVersion?: string;
  databaseVersion?: string;
}

interface SoftwareResults {
  detectedOS: string;
  detectedBrowser: string;
  detectedBrowserVersion: string;
  installedSoftware: string[];
  missingRequirements: string[];
  compatibilityIssues: string[];
  updateRequired: string[];
}

interface NetworkRequirements {
  minBandwidth: number;
  maxLatency: number;
  requiredPorts: number[];
  sslRequired: boolean;
  dnsResolution: boolean;
}

interface NetworkResults {
  detectedBandwidth: number;
  detectedLatency: number;
  openPorts: number[];
  blockedPorts: number[];
  sslSupported: boolean;
  dnsWorking: boolean;
  connectivityIssues: string[];
}

interface PerformanceBenchmarks {
  cpuBenchmarkMin: number;
  memorySpeedMin: number;
  storageSpeedMin: number;
  networkThroughputMin: number;
  javascriptPerformanceMin: number;
  pageLoadTimeMax: number;
  databaseResponseMax: number;
}

interface PerformanceResults {
  cpuBenchmarkScore: number;
  memorySpeed: number;
  storageSpeed: number;
  networkThroughput: number;
  javascriptPerformance: number;
  pageLoadTime: number;
  databaseResponse: number;
  overallGrade: "A+" | "A" | "B+" | "B" | "C" | "D" | "F";
}

interface SystemInfo {
  platform: string;
  architecture: string;
  userAgent: string;
  timezone: string;
  language: string;
  screen: string;
  colorDepth: number;
  pixelRatio: number;
  touchSupport: boolean;
  cookieEnabled: boolean;
  localStorage: boolean;
  sessionStorage: boolean;
  webGL: boolean;
  canvas: boolean;
}

interface PrerequisiteInstallation {
  id: string;
  componentName: string;
  componentType:
    | "database"
    | "runtime"
    | "service"
    | "library"
    | "language_pack";
  version: string;
  downloadUrl: string;
  fileSize: number;

  // Installation Status
  status:
    | "pending"
    | "downloading"
    | "installing"
    | "configuring"
    | "completed"
    | "failed";
  progress: number;
  startedAt?: Date;
  completedAt?: Date;

  // Configuration
  configurationSteps: ConfigurationStep[];
  customConfiguration?: Record<string, any>;

  // Dependencies
  dependencies: string[];
  dependsOn: string[];

  // Validation
  validationChecks: ValidationCheck[];
  validationPassed: boolean;

  // Error Handling
  errorMessage?: string;
  retryCount: number;
  maxRetries: number;
  rollbackAvailable: boolean;
}

interface ConfigurationStep {
  id: string;
  name: string;
  description: string;
  command?: string;
  parameters?: Record<string, any>;
  status: "pending" | "running" | "completed" | "failed";
  output?: string;
  errorMessage?: string;
}

interface ValidationCheck {
  id: string;
  name: string;
  description: string;
  checkType:
    | "version"
    | "connection"
    | "service"
    | "configuration"
    | "performance";
  expectedValue: any;
  actualValue?: any;
  status: "pending" | "running" | "passed" | "failed";
  errorMessage?: string;
}
```

**API Endpoints:**

- `GET /api/setup/business-types` - Get available business type templates
- `POST /api/setup/business-configuration` - Create business configuration
- `PUT /api/setup/business-configuration/:id` - Update business configuration
- `GET /api/setup/business-configuration/:id` - Get business configuration
- `POST /api/setup/wizard/start` - Start setup wizard
- `POST /api/setup/wizard/step` - Complete wizard step
- `GET /api/setup/wizard/progress` - Get wizard progress
- `POST /api/setup/vat/calculate` - Calculate VAT for complex scenarios
- `GET /api/setup/vat/rules` - Get VAT rules configuration
- `PUT /api/setup/vat/rules` - Update VAT rules
- `POST /api/setup/vat/test` - Test VAT calculation scenarios
- `GET /api/setup/locations/greek` - Get Greek location data with VAT zones
- `POST /api/setup/locations/validate` - Validate Greek business location
- `GET /api/setup/product-templates` - Get product templates by business type
- `POST /api/setup/products/configure` - Configure product complexity
- `POST /api/setup/services/configure` - Configure service types
- `GET /api/setup/regulatory-updates` - Get pending regulatory updates
- `POST /api/setup/regulatory-updates/:id/apply` - Apply regulatory update
- `POST /api/setup/regulatory-updates/:id/acknowledge` - Acknowledge update
- `GET /api/setup/validation/run` - Run system configuration validation
- `POST /api/setup/deployment/configure` - Configure deployment settings
- `GET /api/setup/requirements/check` - Check system requirements
- `POST /api/setup/requirements/hardware` - Run hardware performance test
- `POST /api/setup/requirements/network` - Test network connectivity
- `POST /api/setup/requirements/browser` - Validate browser compatibility
- `GET /api/setup/requirements/greek-features` - Check Greek localization features
- `POST /api/setup/prerequisites/install` - Install system prerequisites
- `GET /api/setup/prerequisites/status` - Get installation status
- `POST /api/setup/prerequisites/validate` - Validate installed components

**Custom Hooks:**

- `useBusinessSetupWizard()` - Setup wizard state management
- `useBusinessConfiguration()` - Business configuration management
- `useVATCalculation()` - Dynamic VAT calculation
- `useVATRules()` - VAT rules management
- `useGreekLocationData()` - Greek location and VAT zone data
- `useProductConfiguration()` - Product complexity configuration
- `useServiceConfiguration()` - Service type configuration
- `useProductVariants()` - Product variant management
- `useVariantAttributes()` - Variant attribute management
- `useRegulatoryUpdates()` - Tax law change management
- `useRegulatoryNotifications()` - Update notification handling
- `useSystemValidation()` - Configuration validation
- `useDeploymentConfiguration()` - Deployment settings
- `useBusinessTypeTemplates()` - Business type template management
- `useGreekVATEngine()` - Complex VAT calculation engine
- `useLocationVATCalculation()` - Location-based VAT calculation
- `useConsumptionVATCalculation()` - Consumption method VAT calculation
- `useSetupWizardProgress()` - Wizard progress tracking
- `useBusinessTypeDetection()` - Automatic business type detection
- `useConfigurationMigration()` - Configuration update migration
- `useSystemRequirements()` - System requirements checking and validation
- `useHardwareCheck()` - Hardware requirements validation
- `useSoftwareCheck()` - Software requirements validation
- `useNetworkCheck()` - Network connectivity and performance testing
- `usePerformanceBenchmark()` - System performance benchmarking
- `usePrerequisiteInstallation()` - Prerequisites installation management
- `useInstallationProgress()` - Installation progress tracking
- `useSystemValidation()` - System validation after installation
- `useCompatibilityCheck()` - Browser and system compatibility checking
- `useGreekFeatureCheck()` - Greek localization feature validation

**Components:**

- `BusinessSetupWizard` - Multi-step setup wizard
- `BusinessTypeSelector` - Business type selection interface
- `BusinessConfigurationForm` - Business configuration form
- `VATRulesManager` - Dynamic VAT rules management
- `VATCalculator` - VAT calculation interface
- `VATTestingPanel` - VAT calculation testing
- `GreekLocationSelector` - Greek location with VAT zone selection
- `LocationVATIndicator` - Location-based VAT rate display
- `ProductConfigurationWizard` - Product setup wizard
- `ProductComplexitySelector` - Simple vs variable product selection
- `VariantAttributeManager` - Product variant attribute management
- `VariantAttributeEditor` - Individual attribute editor
- `ServiceConfigurationPanel` - Service type configuration
- `ServiceTypeSelector` - Service type selection
- `BusinessTemplatePreview` - Business template preview
- `RegulatoryUpdateNotification` - Tax law change notifications
- `RegulatoryUpdateDashboard` - Update management dashboard
- `UpdateImpactAnalysis` - Impact analysis display
- `SystemValidationPanel` - Configuration validation interface
- `DeploymentConfigurationPanel` - Deployment settings
- `ConfigurationSummary` - Setup summary display
- `WizardProgressIndicator` - Setup progress display
- `BusinessTypeRecommendations` - Recommended configurations
- `VATScenarioTester` - Complex VAT scenario testing
- `ConfigurationExportImport` - Configuration backup/restore
- `MultiLocationManager` - Multiple business location management
- `SeasonalRulesManager` - Seasonal tax rule management
- `ComplianceRequirementsChecker` - Compliance validation
- `SystemRequirementsChecker` - System requirements validation interface
- `HardwareRequirementsDisplay` - Hardware requirements and results display
- `SoftwareRequirementsDisplay` - Software requirements and results display
- `NetworkRequirementsDisplay` - Network requirements and results display
- `PerformanceBenchmarkDisplay` - Performance test results display
- `PerformanceBenchmarkRunner` - Performance benchmark execution
- `PrerequisiteInstaller` - Prerequisites installation interface
- `InstallationProgressTracker` - Installation progress display
- `ComponentInstallationStatus` - Individual component installation status
- `SystemValidationPanel` - System validation after installation
- `CompatibilityChecker` - Browser and system compatibility checker
- `GreekFeatureValidator` - Greek localization feature validation
- `RequirementsFixAssistant` - Automated requirements issue resolution
- `SystemInfoDisplay` - System information display panel
- `InstallationWizardNavigation` - Installation wizard navigation
- `RequirementsReportGenerator` - System requirements report generation

### 2.6 Greek Compliance Module (7 screens)

**Screens List:**

1. `/compliance/aade` - AADE Dashboard
2. `/compliance/aade/submissions` - AADE Submissions
3. `/compliance/tax/reports` - Tax Reports
4. `/compliance/banking` - Greek Banking
5. `/compliance/settings` - Compliance Settings
6. `/compliance/certifications` - Professional Certifications
7. `/compliance/government` - Government Integration

**Models Needed:**

```typescript
interface AADESubmission {
  id: string;
  invoice: Invoice;
  status: AADEStatus;
  mark: string;
  qrCode: string;
  customFields: Record<string, any>;
}

interface GreekTaxReport {
  id: string;
  reportType: GreekTaxReportType;
  period: string;
  status: "draft" | "submitted";
  customFields: Record<string, any>;
}
```

**API Endpoints:**

- `GET /api/compliance/aade/submissions` - AADE submissions
- `POST /api/compliance/aade/submit` - Submit to AADE
- `GET /api/compliance/tax/reports` - Tax reports
- `POST /api/compliance/tax/reports` - Generate report

**Custom Hooks:**

- `useAADEIntegration()` - AADE integration
- `useGreekTaxReports()` - Tax reports
- `useGreekBanking()` - Banking integration
- `useComplianceStatus()` - Compliance status
- `useComplianceTranslation()` - Compliance-specific translations
- `useGreekGovernmentTerms()` - Greek government terminology
- `useAADETranslation()` - AADE form translations
- `useComplianceDocumentTranslation()` - Compliance document translations
- `useGreekLegalTranslation()` - Greek legal terminology

**Components:**

- `AADEStatusIndicator` - AADE status
- `GreekTaxForm` - Tax form
- `ComplianceChecklist` - Compliance checklist
- `MultilingualComplianceForm` - Compliance forms with translations
- `GreekGovernmentTermGlossary` - Government terminology glossary
- `AADETranslationPanel` - AADE form translation management
- `ComplianceDocumentTranslator` - Compliance document translator
- `GreekLegalTermDisplay` - Greek legal term display with translations
- `ComplianceLanguageSelector` - Language selector for compliance forms

### 2.7 File Storage & Document Management (5 screens)

**Screens List:**

1. `/files/manager` - File Manager Interface
2. `/files/upload` - File Upload & Processing
3. `/files/preview/:id` - File Preview & Versioning
4. `/files/analytics` - Storage Analytics & Reporting
5. `/files/permissions` - File Permissions & Sharing

**Models Needed:**

```typescript
interface FileRecord {
  id: string; // UUID for SAAS, auto-increment for Local
  filename: string;
  originalFilename: string;
  mimetype: string;
  size: number;

  // Storage Details (Deployment-Specific)
  storageProvider: "local" | "aws_s3" | "azure_blob" | "gcp_storage";
  storagePath: string; // Full cloud path or relative local path
  storageUrl?: string; // CDN URL for SAAS, null for Local
  storageIdentifier: string; // UUID for SAAS, relative path for Local

  // Metadata
  title?: string;
  description?: string;
  tags: string[];
  category: string;

  // Security
  accessLevel: "public" | "private" | "restricted";
  encryptionKey?: string;

  // Relationships
  entityType: string; // 'customer', 'invoice', 'product', etc.
  entityId: string;
  folderId?: string;

  // Versioning
  version: number;
  previousVersionId?: string;
  isLatestVersion: boolean;

  // Greek-Specific
  greekCategory?: GreekDocumentCategory;
  aadeCompliant?: boolean;
  taxYear?: number;

  // Audit Trail
  uploadedBy: string;
  uploadedAt: Date;
  lastModifiedBy: string;
  lastModifiedAt: Date;

  // Processing Status
  processingStatus: "pending" | "processing" | "completed" | "failed";
  ocrText?: string;
  thumbnailPath?: string;
  previewPath?: string;

  // Multilingual
  multilingualMetadata?: Record<string, FileMetadataTranslation>;
  customFields: Record<string, any>;
}

interface FileFolder {
  id: string;
  name: string;
  description?: string;
  parentId?: string;

  // Relationships
  entityType: string;
  entityId: string;

  // Permissions
  permissions: FolderPermission[];
  isPublic: boolean;

  // Greek-Specific
  greekLabel?: string;
  businessPurpose?: string;

  // Metadata
  createdBy: string;
  createdAt: Date;
  lastModifiedAt: Date;

  // Computed Properties
  fileCount?: number;
  totalSize?: number;
  subfolderCount?: number;

  // Multilingual
  multilingualNames?: Record<string, string>;
  customFields: Record<string, any>;
}

interface FilePermission {
  id: string;
  fileId: string;

  // Permission Target
  targetType: "user" | "role" | "department" | "company";
  targetId: string;

  // Permissions
  canRead: boolean;
  canWrite: boolean;
  canDelete: boolean;
  canShare: boolean;
  canDownload: boolean;

  // Conditions
  ipRestrictions?: string[];
  expirationDate?: Date;

  // Audit
  grantedBy: string;
  grantedAt: Date;
  lastUsed?: Date;
  customFields: Record<string, any>;
}

interface FileShare {
  id: string;
  fileId: string;
  shareToken: string;

  // Access Control
  shareType: "public" | "password" | "user_specific";
  password?: string;
  allowedUsers?: string[];

  // Expiration
  expiresAt?: Date;
  maxDownloads?: number;
  downloadCount: number;

  // Permissions
  canDownload: boolean;
  canPreview: boolean;
  canComment: boolean;

  // Audit
  createdBy: string;
  createdAt: Date;
  lastAccessedAt?: Date;
  customFields: Record<string, any>;
}

interface FileProcessingJob {
  id: string;
  fileId: string;
  jobType:
    | "thumbnail"
    | "ocr"
    | "virus_scan"
    | "metadata_extraction"
    | "greek_document_recognition";
  status: "pending" | "processing" | "completed" | "failed";

  // Processing Configuration
  processingSettings: Record<string, any>;

  // Results
  processingResult?: FileProcessingResult;
  errorMessage?: string;

  // Timing
  startedAt?: Date;
  completedAt?: Date;
  processingTimeMs?: number;
  customFields: Record<string, any>;
}

interface StorageQuota {
  id: string;
  companyId: string;

  // Quota Limits
  maxStorageBytes: number;
  maxFilesCount: number;
  maxFileSizeBytes: number;

  // Current Usage
  currentStorageBytes: number;
  currentFilesCount: number;

  // Quota Policies
  quotaPolicy: "hard" | "soft" | "flexible";
  warningThreshold: number; // percentage

  // Subscription Integration
  subscriptionTier: string;
  overageAllowed: boolean;

  // Last Updated
  lastCalculated: Date;
  nextCalculation: Date;
  customFields: Record<string, any>;
}

enum GreekDocumentCategory {
  TAX_DOCUMENTS = "tax_documents",
  LEGAL_DOCUMENTS = "legal_documents",
  CONTRACTS = "contracts",
  INVOICES = "invoices",
  RECEIPTS = "receipts",
  BANK_STATEMENTS = "bank_statements",
  GOVERNMENT_FORMS = "government_forms",
  LICENSES = "licenses",
  CERTIFICATES = "certificates",
  PERSONAL_DOCUMENTS = "personal_documents",
}
```

**API Endpoints:**

- `POST /api/files/upload` - Upload file(s)
- `GET /api/files` - List files with filtering/pagination
- `GET /api/files/:id` - Get file details
- `GET /api/files/:id/download` - Download file
- `GET /api/files/:id/preview` - Get file preview
- `PUT /api/files/:id` - Update file metadata
- `DELETE /api/files/:id` - Delete file
- `POST /api/files/:id/share` - Create file share
- `GET /api/files/shared/:token` - Access shared file
- `POST /api/files/batch/upload` - Batch file upload
- `DELETE /api/files/batch` - Batch file deletion
- `POST /api/files/search` - Advanced file search
- `GET /api/folders` - List folders
- `POST /api/folders` - Create folder
- `PUT /api/folders/:id` - Update folder
- `DELETE /api/folders/:id` - Delete folder
- `POST /api/files/:id/move` - Move file to folder
- `POST /api/files/:id/copy` - Copy file
- `GET /api/files/:id/versions` - Get file versions
- `POST /api/files/:id/permissions` - Set file permissions
- `GET /api/storage/quota` - Get storage quota info
- `GET /api/storage/analytics` - Get storage analytics
- `POST /api/files/process` - Process file (OCR, thumbnails)
- `GET /api/files/greek/categories` - Get Greek document categories
- `POST /api/files/greek/validate` - Validate Greek document compliance

**Custom Hooks:**

- `useFileManager()` - Complete file management system
- `useFileUpload()` - File upload with progress tracking
- `useFilePreview()` - File preview functionality
- `useFileSearch()` - File search and filtering
- `useFilePermissions()` - File access control
- `useFileSharing()` - File sharing functionality
- `useFileVersioning()` - File version management
- `useFileOrganization()` - Folder and categorization
- `useStorageQuota()` - Storage quota management
- `useFileAnalytics()` - File usage analytics
- `useFileProcessing()` - File processing automation
- `useGreekDocumentProcessor()` - Greek document recognition
- `useFileBackup()` - File backup and recovery
- `useFileDragAndDrop()` - Drag and drop operations
- `useFileTranslation()` - File metadata translations
- `useMultilingualFileSearch()` - Multilingual file search
- `useFileLocalization()` - File display localization

**Components:**

- `FileManager` - Complete file management interface
- `FileUpload` - File upload with drag & drop
- `FileList` - File list with grid/table view
- `FilePreview` - File preview modal
- `FileCard` - File display card
- `FileGrid` - File grid view
- `FileTable` - File table view
- `FolderTree` - Folder tree navigation
- `FileDropzone` - Drag and drop zone
- `FileProgress` - Upload progress indicator
- `FileVersions` - File version management
- `FileSharing` - File sharing interface
- `FilePermissions` - File permission management
- `FileSearch` - File search interface
- `FileFilter` - File filtering options
- `StorageQuota` - Storage quota display
- `FileAnalytics` - File usage analytics
- `GreekDocumentUpload` - Greek document upload
- `GreekDocumentPreview` - Greek document preview
- `AADEComplianceChecker` - AADE compliance verification
- `GreekDocumentCategories` - Greek document categorization
- `GreekFileMetadata` - Greek-specific file metadata
- `TaxDocumentManager` - Tax document management
- `LegalDocumentManager` - Legal document management
- `MultilingualFileCard` - File card with multilingual metadata
- `FileTranslationPanel` - File metadata translation management
- `LocalizedFilePreview` - File preview with localized metadata
- `MultilingualFileSearch` - File search in multiple languages
- `LocalizedStorageQuota` - Storage quota display with localization

### 2.8 Workflow Engine (7 screens)

**Screens List:**

1. `/workflows/builder` - Workflow Builder
2. `/workflows` - Workflow List
3. `/workflows/:id` - Workflow Detail
4. `/workflows/:id/executions` - Execution History
5. `/workflows/templates` - Workflow Templates
6. `/workflows/bots` - Bot Marketplace
7. `/workflows/dashboard` - Automation Dashboard

**Models Needed:**

```typescript
interface Workflow {
  id: string;
  name: string;
  triggers: WorkflowTrigger[];
  steps: WorkflowStep[];
  greekBusinessRules: GreekBusinessRule[];
  customFields: Record<string, any>;
}

interface WorkflowExecution {
  id: string;
  workflowId: string;
  status: ExecutionStatus;
  results: StepResult[];
  customFields: Record<string, any>;
}
```

**API Endpoints:**

- `GET /api/workflows` - List workflows
- `POST /api/workflows` - Create workflow
- `POST /api/workflows/:id/execute` - Execute workflow
- `GET /api/workflows/bots` - List bots
- `POST /api/workflows/bots/install` - Install bot

**Custom Hooks:**

- `useWorkflows()` - Workflow management
- `useWorkflowBuilder()` - Workflow builder
- `useBots()` - Bot management
- `useGreekBusinessRules()` - Greek business rules

**Components:**

- `WorkflowBuilder` - Drag-drop builder
- `WorkflowStep` - Step component
- `BotCard` - Bot marketplace card
- `ExecutionStatus` - Status indicator

---

## 3. ADMIN APPLICATION SCREENS

### 3.1 System Administration (8 screens)

**Screens List:**

1. `/admin/dashboard` - Admin Dashboard
2. `/admin/company` - Company Settings
3. `/admin/modules` - Module Management
4. `/admin/subscription` - Subscription Management
5. `/admin/integrations` - Integration Settings
6. `/admin/backup` - Backup & Restore
7. `/admin/logs` - System Logs
8. `/admin/performance` - Performance Monitoring

---

## 4. SUPPORT APPLICATION SCREENS

### 4.1 Customer Support (8 screens)

**Screens List:**

1. `/support/dashboard` - Support Dashboard
2. `/support/installations` - Local Installation Monitor
3. `/support/installations/:id` - Installation Detail View
4. `/support/chat` - Live Chat
5. `/support/tickets` - Ticket Management
6. `/support/knowledge-base` - Knowledge Base
7. `/support/remote` - Remote Assistance
8. `/support/health` - Customer Health

**Local Installation Monitoring Screens:**

**Installation Monitor Screen** (`/support/installations`):

- **Components**: InstallationMap, HealthStatus, AlertsList, QuickActions
- **Features**: Real-time status of all installations, health indicators, alert management
- **Data**: All customer installations with status, performance metrics, alerts
- **Actions**: Connect to installation, view details, send update, create support ticket

**Installation Detail Screen** (`/support/installations/:id`):

- **Components**: SystemInfo, ChangeHistory, PerformanceCharts, RemoteAccess
- **Features**: Complete installation details, change audit trail, performance monitoring
- **Data**: Installation configuration, change logs, performance history, support sessions
- **Actions**: Start remote session, view logs, deploy update, modify configuration

**Models for Support Screens:**

```typescript
interface SupportInstallationView {
  installation: LocalInstallation;
  realtimeMetrics: PerformanceMetrics;
  activeAlerts: SystemAlert[];
  changeHistory: SystemChangeLog[];
  supportSessions: SupportSession[];
}

interface SystemAlert {
  id: string;
  installationId: string;
  severity: "info" | "warning" | "critical";
  category: "performance" | "disk_space" | "memory" | "database" | "security";
  message: string;
  details: string;
  firstOccurred: Date;
  lastOccurred: Date;
  resolved: boolean;
  resolvedBy?: string;
  resolvedAt?: Date;
}
```

**Custom Hooks for Support:**

- `useInstallationMonitoring()` - Real-time monitoring of installations
- `useRemoteSupport()` - Remote assistance session management
- `useSystemAlerts()` - Alert management and notifications
- `useChangeTracking()` - Installation change history and audit
- `usePerformanceMetrics()` - Performance monitoring and analytics

---

## 5. SETUP APPLICATION SCREENS

### 5.1 Onboarding (7 screens)

**Screens List:**

1. `/setup/welcome` - Welcome Screen
2. `/setup/company` - Company Profile
3. `/setup/greek-business` - Greek Business Setup
4. `/setup/users` - User Creation
5. `/setup/migration` - Data Migration
6. `/setup/configuration` - Configuration Wizard
7. `/setup/training` - Training Modules

---

## 6. MULTILINGUAL INFRASTRUCTURE

### 6.1 Multilingual Models

```typescript
interface Translation {
  id: string;
  namespace: string;
  key: string;
  language: LanguageCode;
  value: string;
  context?: string;
  isApproved: boolean;
  translatedBy: string;
  translatedAt: Date;
  reviewedBy?: string;
  reviewedAt?: Date;
  customFields: Record<string, any>;
}

interface UserLanguagePreferences {
  id: string;
  userId: string;
  primaryLanguage: LanguageCode;
  fallbackLanguage: LanguageCode;
  customFields: Record<string, any>;
}

interface LocalizationSettings {
  id: string;
  userId: string;
  dateFormat: DateFormat;
  numberFormat: NumberFormat;
  currency: CurrencyCode;
  timezone: TimezoneCode;
  customFields: Record<string, any>;
}

interface BusinessLocaleSettings {
  id: string;
  userId: string;
  country: CountryCode;
  businessCulture: BusinessCultureSettings;
  addressFormat: AddressFormatSettings;
  phoneFormat: PhoneFormatSettings;
  businessHours: BusinessHoursSettings;
  holidays: HolidaySettings;
  customFields: Record<string, any>;
}

interface ComplianceDisplaySettings {
  id: string;
  userId: string;
  country: CountryCode;
  taxNumberDisplay: TaxNumberDisplaySettings;
  complianceFormats: ComplianceFormatSettings;
  governmentIntegrationDisplay: GovernmentDisplaySettings;
  legalDocumentFormats: LegalDocumentFormatSettings;
  customFields: Record<string, any>;
}

interface MultilingualContent {
  id: string;
  entityType: string;
  entityId: string;
  field: string;
  translations: Record<LanguageCode, string>;
  defaultLanguage: LanguageCode;
  autoTranslated: boolean;
  lastUpdated: Date;
  customFields: Record<string, any>;
}

interface TranslationJob {
  id: string;
  type: "import" | "export" | "auto_translate" | "bulk_update";
  status: "pending" | "processing" | "completed" | "failed";
  progress: number;
  sourceLanguage: LanguageCode;
  targetLanguages: LanguageCode[];
  itemCount: number;
  processedCount: number;
  startedAt: Date;
  completedAt?: Date;
  error?: string;
  customFields: Record<string, any>;
}

interface LanguageSupport {
  code: LanguageCode;
  name: string;
  nativeName: string;
  isActive: boolean;
  isDefault: boolean;
  completeness: number; // Percentage of translations complete
  lastUpdated: Date;
  maintainers: string[];
  customFields: Record<string, any>;
}
```

### 6.2 Multilingual API Endpoints

```typescript
// Translation Management
const translationAPIs = {
  // Core Translation CRUD
  "GET /api/i18n/translations": "List translations with filters",
  "POST /api/i18n/translations": "Create translation",
  "PUT /api/i18n/translations/:id": "Update translation",
  "DELETE /api/i18n/translations/:id": "Delete translation",
  "GET /api/i18n/translations/export": "Export translations",
  "POST /api/i18n/translations/import": "Import translations",

  // Language Management
  "GET /api/i18n/languages": "List supported languages",
  "POST /api/i18n/languages": "Add language support",
  "PUT /api/i18n/languages/:code": "Update language settings",
  "GET /api/i18n/languages/:code/stats": "Get language statistics",

  // Translation Jobs
  "GET /api/i18n/jobs": "List translation jobs",
  "POST /api/i18n/jobs/auto-translate": "Start auto-translation job",
  "POST /api/i18n/jobs/bulk-update": "Start bulk update job",
  "GET /api/i18n/jobs/:id": "Get job status",
  "DELETE /api/i18n/jobs/:id": "Cancel job",

  // User Language Preferences
  "GET /api/i18n/user-preferences": "Get user language preferences",
  "PUT /api/i18n/user-preferences": "Update user preferences",
  "POST /api/i18n/user-preferences/detect": "Auto-detect language",

  // Dynamic Content Translation
  "GET /api/i18n/content/:entityType/:entityId": "Get multilingual content",
  "PUT /api/i18n/content/:entityType/:entityId": "Update multilingual content",
  "POST /api/i18n/content/translate": "Translate dynamic content",

  // Translation Validation
  "POST /api/i18n/validate": "Validate translations",
  "GET /api/i18n/missing": "Get missing translations",
  "GET /api/i18n/quality": "Get translation quality metrics",

  // Greek Business Terms
  "GET /api/i18n/greek-terms": "Get Greek business terms",
  "POST /api/i18n/greek-terms": "Add Greek business term",
  "PUT /api/i18n/greek-terms/:id": "Update Greek business term",
};
```

### 6.3 Multilingual Custom Hooks

```typescript
const multilingualHooks = {
  // Core Translation Hooks
  useTranslation: "Main translation hook with namespace support",
  useTranslationWithFallback: "Translation with fallback languages",
  useTranslationLoader: "Load translations on demand",
  useTranslationCache: "Translation caching and invalidation",

  // Language Management Hooks
  useLanguage: "Current language state and switching",
  useLanguageDetection: "Auto-detect user language",
  useLanguagePreferences: "User language preferences management",
  useSupportedLanguages: "List of supported languages",

  // Dynamic Content Hooks
  useMultilingualContent: "Manage multilingual entity content",
  useContentTranslation: "Translate dynamic content",
  useAutoTranslation: "Auto-translation services",
  useTranslationJobs: "Translation job management",

  // Greek-Specific Hooks
  useGreekLocalization: "Greek locale formatting",
  useGreekBusinessTerms: "Greek business terminology",
  useGreekValidationMessages: "Greek validation messages",
  useGreekFormats: "Greek date/number/phone formats",

  // Translation Management Hooks
  useTranslationEditor: "In-context translation editing",
  useTranslationReview: "Translation review workflow",
  useTranslationQuality: "Translation quality metrics",
  useTranslationImportExport: "Translation import/export",

  // Context-Aware Hooks
  useContextualTranslation: "Context-aware translations",
  useTranslationVariables: "Translation with variables",
  usePluralization: "Pluralization rules",
  useRTLSupport: "Right-to-left language support",
};
```

### 6.4 Multilingual Components

```typescript
const multilingualComponents = {
  // Core Translation Components
  TranslationProvider: "Main translation context provider",
  TranslationWrapper: "Wrap components with translation context",
  TranslatedText: "Render translated text with fallback",
  TranslationPlaceholder: "Show loading state for translations",

  // Language Selection Components
  LanguageSelector: "Language dropdown selector",
  LanguageSwitcher: "Quick language switching",
  LanguageFlag: "Language flag display",
  LanguageProgress: "Translation completion progress",

  // Form Components
  MultilingualInput: "Input field with translation support",
  MultilingualTextarea: "Textarea with multilingual support",
  MultilingualRichEditor: "Rich text editor with translations",
  MultilingualFormField: "Form field with translation wrapper",

  // Display Components
  LocalizedDate: "Date display with locale formatting",
  LocalizedNumber: "Number display with locale formatting",
  LocalizedCurrency: "Currency display with locale formatting",
  LocalizedAddress: "Address display with locale formatting",

  // Greek-Specific Components
  GreekBusinessTermDisplay: "Greek business term display",
  GreekValidationMessage: "Greek validation messages",
  GreekPhoneDisplay: "Greek phone number display",
  GreekDatePicker: "Greek date picker with Orthodox calendar",

  // Translation Management Components
  TranslationEditor: "In-context translation editor",
  TranslationReview: "Translation review interface",
  TranslationImportExport: "Translation import/export interface",
  TranslationQualityIndicator: "Translation quality display",

  // Dynamic Content Components
  DynamicMultilingualContent: "Render multilingual dynamic content",
  ContentTranslationPanel: "Content translation management",
  AutoTranslationButton: "Auto-translate content button",
  TranslationJobStatus: "Translation job status display",

  // Navigation Components
  MultilingualBreadcrumb: "Breadcrumb with translations",
  MultilingualMenu: "Menu with multilingual support",
  MultilingualTooltip: "Tooltip with translations",
  MultilingualNotification: "Notification with translations",
};
```

### 6.5 Multilingual Contexts

```typescript
const multilingualContexts = {
  // Core Translation Contexts
  TranslationContext: "Main translation state and functions",
  LanguageContext: "Current language and switching logic",
  LocalizationContext: "Locale-specific formatting",

  // Content Management Contexts
  MultilingualContentContext: "Dynamic content translation state",
  TranslationJobContext: "Translation job management state",

  // Greek-Specific Contexts
  GreekLocaleContext: "Greek locale settings and formatting",
  GreekBusinessTermContext: "Greek business terminology",

  // User Preferences Contexts
  UserLanguageContext: "User language preferences",
  PersonalizationContext: "Personalized translation settings",

  // Admin Contexts
  TranslationManagementContext: "Translation management state",
  LanguageAdminContext: "Language administration",
};
```

### 6.6 Multilingual Screens

#### 6.6.1 Admin Application - Translation Management (8 screens)

**Screens List:**

1. `/admin/translations` - Translation Management Dashboard
2. `/admin/translations/editor` - Translation Editor
3. `/admin/translations/import` - Translation Import
4. `/admin/translations/export` - Translation Export
5. `/admin/translations/jobs` - Translation Jobs
6. `/admin/translations/quality` - Translation Quality
7. `/admin/languages` - Language Management
8. `/admin/translations/greek-terms` - Greek Business Terms

**Models:** Translation, TranslationJob, LanguageSupport, UserLanguagePreferences

**API Endpoints:** All translation management endpoints

**Custom Hooks:** useTranslationEditor, useTranslationJobs, useLanguageManagement

**Components:** TranslationEditor, TranslationJobStatus, LanguageSelector, GreekTermManager

#### 6.6.2 User Settings - Language & Localization (4 screens)

**Screens List:**

1. `/settings/language` - Language Preferences (Primary/Fallback Language Selection)
2. `/settings/localization` - Localization Settings (Date/Number/Currency Formats)
3. `/settings/business-locale` - Business Locale Settings (Country-Specific Business Rules)
4. `/settings/compliance` - Compliance Preferences (Regulatory Display Preferences)

**Models:** UserLanguagePreferences, BusinessLocaleSettings, ComplianceDisplaySettings

**API Endpoints:** User preference management endpoints, business locale endpoints

**Custom Hooks:** useLanguagePreferences, useBusinessLocale, useComplianceSettings

**Components:** LanguageSelector, LocalizationForm, BusinessLocaleForm, ComplianceSettingsForm

---

## 7. SHARED INFRASTRUCTURE

### 7.1 Reusable Components

```typescript
const sharedComponents = {
  // Basic UI Components
  Button: "Primary, secondary, tertiary button variants",
  IconButton: "Icon-only buttons with tooltips",
  ButtonGroup: "Grouped button actions",
  LoadingButton: "Button with loading state",

  // Form Components
  Input: "Text input with validation",
  TextArea: "Multi-line text input",
  Select: "Dropdown select with search",
  MultiSelect: "Multiple selection dropdown",
  DatePicker: "Date selection with calendar",
  TimePicker: "Time selection component",
  DateRangePicker: "Date range selection",
  FileUpload: "File upload with drag-drop",
  ImageUpload: "Image upload with preview",
  Checkbox: "Checkbox with indeterminate state",
  Radio: "Radio button groups",
  Switch: "Toggle switch component",
  Slider: "Range slider component",

  // Advanced Form Components
  DynamicForm: "Auto-generated forms",
  FormBuilder: "Drag-drop form builder",
  FieldGroup: "Grouped form fields",
  FormWizard: "Multi-step form wizard",
  GreekValidationForm: "Greek validation forms",
  MultilingualForm: "Form with translation support",

  // Data Display Components
  Card: "Content card with header/body/footer",
  InfoCard: "Information display card",
  StatsCard: "Statistics display card",
  ActionCard: "Card with action buttons",

  // List & Table Components
  List: "Basic list component",
  VirtualizedList: "Performance-optimized list",
  DataTable: "Advanced data tables with sorting/filtering",
  SimpleTable: "Basic table component",
  TreeTable: "Hierarchical table with expand/collapse",
  MultilingualDataTable: "Data table with multilingual support",

  // Filtering & Search Components
  FilterPanel: "Advanced filtering sidebar",
  FilterBuilder: "Visual filter construction",
  QuickFilter: "Quick filter buttons",
  SearchInput: "Search input with suggestions",
  AdvancedSearch: "Multi-field search form",
  SavedFilters: "Save and manage filter presets",
  FilterTags: "Display active filters as tags",

  // Pagination Components
  Pagination: "Standard pagination with page numbers",
  SimplePagination: "Previous/Next pagination",
  InfiniteScroll: "Auto-loading pagination",
  LoadMore: "Load more button pagination",
  PaginationInfo: "Results count and page info",

  // Modal & Dialog Components
  Modal: "Basic modal component",
  ConfirmDialog: "Confirmation dialog with actions",
  AlertDialog: "Alert/warning dialog",
  FormModal: "Modal with form content",
  FullscreenModal: "Full-screen modal overlay",
  DrawerModal: "Side drawer modal",

  // Notification Components
  Toast: "Toast notification system",
  Alert: "Inline alert messages",
  Banner: "Top banner notifications",
  NotificationCenter: "Notification management",
  StatusIndicator: "Status badge/indicator",

  // Navigation Components
  Navigation: "Dynamic navigation",
  Breadcrumb: "Breadcrumb navigation",
  Tabs: "Tab navigation component",
  VerticalTabs: "Vertical tab layout",
  Stepper: "Step-by-step navigation",
  Sidebar: "Collapsible sidebar",
  Header: "Application header",
  MultilingualNavigation: "Navigation with translation support",

  // Layout Components
  Container: "Content container with responsive design",
  Grid: "CSS Grid layout component",
  Flex: "Flexbox layout component",
  Stack: "Vertical/horizontal stack layout",
  Divider: "Content divider/separator",
  Spacer: "Layout spacing component",

  // Data Visualization
  DynamicChart: "Dynamic charts with multiple types",
  LineChart: "Line chart component",
  BarChart: "Bar chart component",
  PieChart: "Pie chart component",
  KanbanBoard: "Kanban boards",
  Timeline: "Timeline/Gantt view",
  CalendarView: "Calendar component",

  // Greek-Specific Components
  GreekAddressInput: "Greek address input",
  AFMInput: "Greek AFM input with validation",
  DOYSelector: "Tax office selector",
  GreekBusinessTermDisplay: "Greek business term display",
  GreekPhoneInput: "Greek phone number input",
  GreekPostalCodeInput: "Greek postal code input",

  // Multilingual Components
  TranslationProvider: "Translation context provider",
  LanguageSelector: "Language selection component",
  LocalizedText: "Localized text display",
  MultilingualInput: "Input with multilingual support",
  TranslationEditor: "Inline translation editor",

  // Utility Components
  Tooltip: "Tooltip with positioning",
  Popover: "Popover content overlay",
  Dropdown: "Dropdown menu component",
  Avatar: "User avatar with fallback",
  Badge: "Notification badge",
  Tag: "Label/tag component",
  Skeleton: "Loading skeleton placeholders",
  EmptyState: "Empty state illustration",
  ErrorBoundary: "Error boundary with recovery",

  // Business-Specific Components
  CustomerCard: "Customer information card",
  ProductCard: "Product display card",
  InvoiceCard: "Invoice summary card",
  ActivityCard: "Activity timeline card",
  EntityCard: "Dynamic entity card",

  // File Management Components
  FileManager: "Complete file management interface",
  FileUpload: "File upload with drag & drop",
  FileList: "File list with grid/table view",
  FilePreview:
    "Advanced file preview modal with zoom, annotations, and full-screen",
  FileCard: "File display card with thumbnail preview",
  FileGrid: "File grid view with thumbnail previews",
  FileTable: "File table view with inline preview",
  FolderTree: "Folder tree navigation",
  FileDropzone: "Drag and drop zone",
  FileProgress: "Upload progress indicator",
  FileVersions: "File version management",
  FileSharing: "File sharing interface",
  FilePermissions: "File permission management",
  FileSearch: "File search interface",
  FileFilter: "File filtering options",
  StorageQuota: "Storage quota display",
  FileAnalytics: "File usage analytics",

  // File Preview Components
  ImagePreview: "Image preview with zoom, rotate, and transform tools",
  PDFPreview: "PDF preview with page navigation, search, and annotations",
  DocumentPreview: "Word/Excel/PowerPoint preview with formatting",
  VideoPreview: "Video preview with playback controls and subtitles",
  AudioPreview: "Audio preview with waveform and controls",
  TextPreview: "Text file preview with syntax highlighting",
  ArchivePreview: "Archive file contents preview",
  CADPreview: "CAD file preview for engineering documents",
  PreviewToolbar: "Universal preview toolbar with controls",
  PreviewTabs: "Tabbed preview interface",
  ThumbnailGenerator: "Automatic thumbnail generation",
  PreviewModal: "Universal preview modal container",
  PreviewSidebar: "File details and metadata sidebar",
  PreviewComments: "File commenting and annotation system",
  PreviewAnnotations: "Annotation tools for PDFs and images",
  PreviewSearch: "Search within file content",
  PreviewFullscreen: "Full-screen preview mode",
  PreviewDownload: "Download and export options",
  PreviewSharing: "Preview sharing controls",
  PreviewVersions: "Version comparison in preview",
  ConversionProgress: "File conversion progress indicator",
  PreviewSettings: "Preview quality and display settings",

  // Greek-Specific File Components
  GreekDocumentUpload: "Greek document upload with auto-categorization",
  GreekDocumentPreview: "Greek document preview with compliance checking",
  AADEComplianceChecker: "AADE compliance verification with visual feedback",
  GreekDocumentCategories: "Greek document categorization with auto-detection",
  GreekFileMetadata: "Greek-specific file metadata with validation",
  TaxDocumentManager: "Tax document management with preview",
  LegalDocumentManager: "Legal document management with preview",
  GreekDocumentProcessor: "Greek document processing with OCR",
  GreekComplianceIndicator: "Visual compliance status indicator",

  // Advanced Features
  DataExport: "Data export functionality",
  BulkActions: "Bulk operation component",
  RichTextEditor: "WYSIWYG text editor",
  CodeEditor: "Code/JSON editor",
  ColorPicker: "Color selection component",
  IconPicker: "Icon selection component",
};
```

### 7.2 Custom Hooks

```typescript
const sharedHooks = {
  // Data Management Hooks
  useQuery: "Enhanced React Query with caching",
  useMutation: "Data mutation with optimistic updates",
  useInfiniteQuery: "Infinite scroll data loading",
  usePaginatedQuery: "Paginated data fetching",
  useLocalStorage: "Local storage state management",
  useSessionStorage: "Session storage state management",

  // Form Management Hooks
  useForm: "Form state management with validation",
  useFormBuilder: "Dynamic form builder",
  useFormValidation: "Form validation with custom rules",
  useFieldArray: "Dynamic form field arrays",
  useFormPersist: "Auto-save form data",
  useFormWizard: "Multi-step form management",

  // UI State Hooks
  useModal: "Modal state management",
  useDialog: "Dialog/confirmation state",
  useToast: "Toast notification management",
  useNotifications: "Notification center management",
  useDisclosure: "Open/close state management",
  useToggle: "Boolean state toggle",
  useClipboard: "Clipboard operations",
  useHover: "Hover state detection",
  useFocus: "Focus state management",

  // Filtering & Search Hooks
  useFilter: "Advanced filtering logic",
  useFilterBuilder: "Visual filter construction",
  useSearch: "Search functionality with debouncing",
  useAdvancedSearch: "Multi-field search management",
  useSavedFilters: "Save and load filter presets",
  useFilterTags: "Active filter display",
  useSortable: "Sortable list management",

  // Pagination Hooks
  usePagination: "Pagination state management",
  useInfiniteScroll: "Infinite scroll implementation",
  useVirtualization: "List virtualization for performance",
  useTablePagination: "Table-specific pagination",

  // Data Table Hooks
  useDataTable: "Complete data table management",
  useTableSelection: "Row selection management",
  useTableSorting: "Column sorting logic",
  useTableFiltering: "Table filtering integration",
  useBulkActions: "Bulk operation management",
  useTableExport: "Data export functionality",

  // Layout & Navigation Hooks
  useNavigation: "Navigation state management",
  useBreadcrumb: "Breadcrumb navigation",
  useSidebar: "Sidebar collapse/expand",
  useResponsive: "Responsive design helpers",
  useBreakpoint: "CSS breakpoint detection",

  // Performance Hooks
  useDebounce: "Value debouncing",
  useThrottle: "Function throttling",
  useMemoizedCallback: "Callback memoization",
  useVirtualList: "Virtual list rendering",
  useLazyLoading: "Lazy loading implementation",

  // Business Logic Hooks
  usePermissions: "Permission checking",
  useGreekValidation: "Greek validation",
  useWorkflow: "Workflow execution",
  useEntityCRUD: "Entity CRUD operations",
  useCustomFields: "Dynamic custom fields",

  // File Management Hooks
  useFileUpload: "File upload with progress and preview generation",
  useFileManager: "Complete file management system with preview",
  useImageUpload: "Image upload with preview and editing",
  useFilePreview: "Advanced file preview functionality",
  useFileDragAndDrop: "Drag and drop operations",
  useFileVersioning: "File version management",
  useFileSharing: "File sharing and permissions",
  useFileSearch: "File search and filtering",
  useFileFolder: "Folder management",
  useFileOrganization: "File organization and categorization",
  useFilePermissions: "File access control",
  useFileBackup: "File backup and recovery",
  useFileProcessing: "File processing and automation",
  useFileAnalytics: "File usage analytics",
  useStorageQuota: "Storage quota management",

  // File Preview Hooks
  useImagePreview: "Image preview with zoom, rotate, and transform",
  usePDFPreview: "PDF preview with navigation and annotations",
  useDocumentPreview: "Word/Excel/PowerPoint preview with formatting",
  useVideoPreview: "Video preview with playback controls",
  useAudioPreview: "Audio preview with waveform visualization",
  useTextPreview: "Text file preview with syntax highlighting",
  useArchivePreview: "Archive file contents preview",
  useCADPreview: "CAD file preview for engineering documents",
  usePreviewModal: "Universal preview modal management",
  usePreviewToolbar: "Preview toolbar state and controls",
  usePreviewAnnotations: "Annotation system for files",
  usePreviewComments: "Comment system for files",
  usePreviewSearch: "Search within file content",
  usePreviewFullscreen: "Full-screen preview mode",
  usePreviewSharing: "Preview sharing controls",
  usePreviewVersions: "Version comparison in preview",
  useThumbnailGeneration: "Automatic thumbnail generation",
  useFileConversion: "File format conversion",
  usePreviewSettings: "Preview quality and display settings",
  usePreviewCache: "Preview caching and performance",

  // Greek-Specific File Hooks
  useGreekDocumentProcessing: "Greek document processing with OCR",
  useGreekDocumentValidation: "Greek document validation",
  useAADECompliance: "AADE compliance checking",
  useGreekFileMetadata: "Greek-specific metadata extraction",
  useGreekDocumentCategories: "Automatic Greek document categorization",

  // Export/Import Hooks
  useDataExport: "Data export in multiple formats",
  useDataImport: "Data import with validation",
  useCSVExport: "CSV export functionality",
  useExcelExport: "Excel export functionality",
  usePDFExport: "PDF generation and export",

  // Greek-Specific Hooks
  useGreekAddressValidation: "Greek address validation",
  useAFMValidation: "Greek AFM validation",
  useDOYLookup: "Tax office lookup",
  useGreekPhoneValidation: "Greek phone validation",
  useAADEIntegration: "AADE integration hooks",

  // Multilingual Hooks
  useTranslation: "Main translation hook",
  useLanguage: "Language management",
  useMultilingualContent: "Multilingual content management",
  useGreekLocalization: "Greek localization",
  useTranslationCache: "Translation caching",
  useLanguageDetection: "Auto-detect user language",
  useContentTranslation: "Dynamic content translation",

  // Real-time & WebSocket Hooks
  useWebSocket: "WebSocket connection management",
  useRealTimeUpdates: "Real-time data updates",
  usePresence: "User presence detection",
  useLiveNotifications: "Live notification system",

  // Analytics & Tracking Hooks
  useAnalytics: "Analytics event tracking",
  usePageTracking: "Page view tracking",
  useUserBehavior: "User behavior analytics",
  usePerformanceTracking: "Performance monitoring",
};
```

### 7.3 Context Providers

```typescript
const contexts = {
  AuthContext: "Authentication state",
  CompanyContext: "Company information",
  DynamicEntityContext: "Entity definitions",
  WorkflowContext: "Workflow state",
  GreekComplianceContext: "Compliance state",
  FileStorageContext: "File storage and management state",

  // Multilingual Contexts
  TranslationContext: "Translation state and functions",
  LanguageContext: "Language selection and switching",
  LocalizationContext: "Locale-specific formatting",
  GreekLocaleContext: "Greek locale settings",
  MultilingualContentContext: "Dynamic content translation",
};
```

---

## 7. IMPLEMENTATION STRATEGY

### 7.1 Screen Implementation Priority

**Phase 1 (Foundation) - 18 screens:**

1. Authentication screens (7)
2. Dynamic entity screens (7)
3. User language & localization screens (4)

**Phase 2 (Core Business) - 47 screens:**

1. CRM screens (23)
2. ERP Financial screens (12)
3. Greek Compliance screens (7)
4. File Storage screens (5)

**Phase 3 (Advanced Features) - 29 screens:**

1. Workflow screens (7)
2. Admin screens (8)
3. Setup screens (7)
4. Translation management screens (8)

**Phase 4 (Support & Infrastructure) - 8 screens:**

1. Support screens (8)

**Total: 113 screens** (85 original + 12 multilingual + 5 file storage + 3 customer statements + 8 business configuration screens)

### 7.2 Technical Stack

**Frontend:**

- Next.js 15+ with TypeScript
- Tailwind CSS + shadcn/ui
- React Hook Form + Zod
- Zustand + React Query

**Backend:**

- FastAPI with Python 3.12+
- PostgreSQL 16+ with JSONB
- Redis for caching
- Celery for background tasks

**Cross-Platform Support:**

- **Windows**: Native .msi installer, Windows services, Event Log integration
- **macOS**: .pkg installer, Homebrew integration, launchd services
- **Linux**: .deb/.rpm packages, systemd services, native package management
- **Unified Monitoring**: Same support dashboard for all platforms

**Testing:**

- Jest + React Testing Library
- Playwright for E2E (cross-platform)
- Platform-specific installer testing
- Greek-specific test data
- Multi-OS CI/CD pipeline

---

## 8. SCREEN DEVELOPMENT TEMPLATE

For each screen, we'll create:

1. **Screen Component** - Main React component
2. **Models** - TypeScript interfaces
3. **API Hooks** - Custom hooks for data fetching
4. **Form Schemas** - Zod validation schemas
5. **Components** - Reusable UI components
6. **Tests** - Unit, integration, and E2E tests

### 8.1 Example Screen Structure

```typescript
// Screen: /crm/customers
// Files needed:
src / pages / crm / customers / index.tsx[id].tsx; // Main screen component // Customer detail screen
components / crm / CustomerCard.tsx; // Customer display card
CustomerForm.tsx; // Customer form
CustomerTable.tsx; // Customer table
hooks / crm / useCustomers.ts; // Customer management hook
useCustomerForm.ts; // Customer form hook
types / crm / customer.ts; // Customer types
schemas / crm / customer.ts; // Customer validation schemas
tests / crm / customers.test.tsx; // Screen tests
customer - form.test.tsx; // Form tests
```

---

## 9. CONCLUSION

This detailed plan provides:

- **113 total screens** across 4 applications (85 original + 12 multilingual + 5 file storage + 3 customer statements + 8 business configuration)
- **Complete technical breakdown** for each screen including multilingual components
- **Comprehensive multilingual infrastructure** with 16 specialized hooks and 18 components
- **Full translation management system** with 8 dedicated admin screens
- **Prioritized implementation order** including multilingual phases
- **Shared infrastructure** for reusability including translation contexts
- **Testing strategy** for each component including multilingual testing
- **Two deployment models** (Cloud SAAS + Local Installation)
- **Excellent mobile browser experience** via PWA with multilingual support

**Multilingual Infrastructure Includes:**

- **5 Core Models**: Translation, UserLanguagePreferences, MultilingualContent, TranslationJob, LanguageSupport
- **20 API Endpoints**: Complete translation management, user preferences, dynamic content translation
- **16 Custom Hooks**: Translation management, language switching, localization, Greek business terms
- **18 Components**: Language selectors, multilingual forms, localized displays, translation editors
- **9 Contexts**: Translation state, language management, localization, Greek locale settings

**Enhanced Module Support:**

- **Authentication**: Language preferences, localized login/register, translated error messages
- **CRM**: Multilingual customer data, messaging translations, localized sales pipeline
- **ERP**: Multilingual invoicing, product translations, localized financial reports
- **Greek Compliance**: Government form translations, legal terminology, AADE translations
- **Dynamic Entities**: Entity translations, field labels, validation messages in multiple languages
- **File Storage**: Complete document management with Greek document recognition, AADE compliance, multilingual metadata

**Next Steps:**

1. Start with Phase 1 (Authentication + Dynamic Entities + Language & Localization)
2. Build multilingual shared components and hooks
3. Implement CRM and ERP screens with translation support
4. Add Greek compliance features with multilingual documentation
5. Build admin translation management system
6. Build support applications with multilingual capabilities
7. Optimize for mobile browser experience with language switching

This approach ensures systematic development with clear milestones and reduces development time through reusable multilingual components and hooks. The comprehensive multilingual support positions the platform for international expansion while maintaining Greek market specialization.
