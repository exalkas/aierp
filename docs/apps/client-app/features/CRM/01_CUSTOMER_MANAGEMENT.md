# 01_BUSINESS_ENTITY_MANAGEMENT - Unified CRM+ERP Foundation

## Document Information

- **Feature**: Business Entity Management (Unified CRM+ERP)
- **Priority**: ⭐ CRITICAL FIRST - Foundation for all business management
- **Implementation**: Month 1 (Phase 1)
- **Dependencies**: Authentication, Core Infrastructure
- **Impact**: Eliminates CRM/ERP silos, enables 360° business view
- **Competitive Advantage**: Single source of truth for all business relationships

## 🎯 Feature Overview

Business Entity Management forms the foundation of our unified CRM+ERP system, providing comprehensive business relationship management that eliminates traditional silos between customer relationship management and enterprise resource planning.

### Core Capabilities

- **Universal Business Entity**: Single entity for customers, suppliers, partners, prospects
- **360° Business View**: Complete relationship visibility in one interface
- **Role-Based Relationships**: Dynamic role assignment (Customer • Supplier • Partner)
- **Contact Management**: People within business entities with full interaction history
- **Greek Integration**: Complete Greek business compliance and validation
- **Smart Navigation**: Contextual interfaces based on business entity roles

---

## 📋 Screens & User Interface

### 1. Business Entity Management Screens

#### Business List Screen (`/businesses`)

```typescript
interface BusinessListScreen {
  // Unified business grid showing ALL external entities
  grid: {
    businesses: BusinessEntity[];
    roleFilters: ["all", "customers", "suppliers", "partners", "prospects"];
    columns: ["name", "roles", "healthScore", "totalValue", "lastActivity", "assignedUser"];
    search: "name, email, phone, AFM, VAT number";
    filters: "location, industry, roles, activity, financial health";
    bulkActions: "email, assign, tag, export, merge";
  };
  
  // Smart metrics and insights
  insights: {
    totalBusinesses: number;
    activeCustomers: number;
    preferredSuppliers: number;
    strategicPartners: number;
    averageHealthScore: number;
    totalLifetimeValue: number;
  };
}
```

#### Business Detail Screen (`/businesses/:id`) - **THE 360° VIEW**

```typescript
interface BusinessDetailScreen {
  // Universal business header
  header: {
    businessName: string;
    roles: BusinessEntityRole[];          // Customer • Supplier • Partner badges
    healthScore: number;                  // 0-100 overall relationship health
    totalLifetimeValue: number;           // All transactions combined
    lastActivity: ActivitySummary;        // Most recent interaction
    assignedManager: User;                // Primary relationship manager
    quickActions: ContextualAction[];     // Role-based actions
  };

  // Smart tab system with conditional visibility
  tabs: {
    // Core tabs (always visible)
    overview: BusinessOverviewTab;        // Executive dashboard
    contacts: ContactsTab;                // People within business
    communications: CommunicationsTab;    // All interactions
    documents: DocumentsTab;              // Shared files and contracts
  
    // CRM tabs (conditional)
    opportunities?: OpportunitiesTab;     // If CRM module + customer role
    activities?: ActivitiesTab;           // If CRM module enabled
    marketing?: MarketingTab;             // If marketing module enabled
  
    // ERP tabs (conditional)
    orders?: OrdersTab;                   // If ERP module + (customer OR supplier)
    invoices?: InvoicesTab;               // If ERP invoicing module
    payments?: PaymentsTab;               // If ERP finance module
    inventory?: InventoryTab;             // If supplier role + inventory module
  
    // Support tabs (conditional)
    support?: SupportTab;                 // If support module enabled
  
    // Compliance tabs (conditional)
    compliance?: ComplianceTab;           // If Greek compliance enabled
    financial?: FinancialHealthTab;       // If finance permissions
  };
}

interface BusinessOverviewTab {
  // Key metrics grid
  metrics: {
    // Financial metrics
    totalSales: number;                   // All-time revenue from this business
    totalPurchases: number;               // All-time purchases from this business
    outstandingReceivables: number;       // Money they owe us
    outstandingPayables: number;          // Money we owe them
    creditUtilization: number;            // % of credit limit used
  
    // Relationship metrics
    relationshipLength: number;           // Years of business relationship
    interactionFrequency: number;         // Contacts per month
    responseRate: number;                 // Communication response rate
    satisfactionScore: number;            // Support/service satisfaction
  
    // Activity metrics
    activeOpportunities: number;          // Open sales opportunities
    recentOrders: number;                 // Orders in last 30 days
    supportTickets: number;               // Open support cases
    upcomingTasks: number;                // Scheduled follow-ups
  };
  
  // Recent activity timeline
  activityTimeline: {
    date: Date;
    type: ActivityType;                   // email, call, meeting, invoice, payment, order
    description: string;
    user: User;
    businessImpact?: "high" | "medium" | "low";
    amount?: number;                      // For financial activities
  }[];
  
  // Smart action suggestions
  suggestedActions: {
    type: "payment_reminder" | "follow_up" | "opportunity_update" | "reorder_stock";
    priority: "high" | "medium" | "low";
    description: string;
    dueDate?: Date;
  }[];
  
  // Health score breakdown
  healthScoreDetails: {
    financial: number;                    // Payment behavior, credit usage
    relationship: number;                 // Communication frequency, satisfaction
    compliance: number;                   // Greek tax compliance status
    growth: number;                       // Opportunity potential, trends
  };
}
```

#### Contact Management (Within Business Entity)

```typescript
interface ContactsTab {
  // Contact hierarchy within business
  contactHierarchy: {
    primaryContact: Contact;
    decisionMakers: Contact[];
    technicalContacts: Contact[];
    billingContacts: Contact[];
    otherContacts: Contact[];
  };
  
  // Contact list with interaction history
  contactList: {
    contact: Contact;
    recentInteractions: Interaction[];
    engagementScore: number;
    preferredContactMethod: "email" | "phone" | "meeting" | "whatsapp";
    lastContactDate: Date;
    upcomingTasks: Task[];
  }[];
  
  // Quick contact actions
  contactActions: {
    sendEmail: (contactId: string) => void;
    scheduleCall: (contactId: string) => void;
    scheduleMeeting: (contactId: string) => void;
    addNote: (contactId: string) => void;
    updateStatus: (contactId: string) => void;
  };
}

interface ContactDetailScreen {
  // Personal and professional information
  personalInfo: {
    firstName: string;
    lastName: string;
    jobTitle: string;
    department: string;
    email: string;
    phone: string;
    mobile: string;
  
    // Greek-specific fields
    fatherName?: string;
    motherName?: string;
    amka?: string;                        // Greek Social Security Number
    idCardNumber?: string;
  };
  
  // Communication preferences and history
  communicationProfile: {
    preferredMethod: "email" | "phone" | "meeting";
    preferredTime: string;
    language: "el" | "en";
    timezone: string;
  
    // Engagement metrics
    emailOpenRate: number;
    responseTime: number;
    meetingAttendanceRate: number;
    totalInteractions: number;
  };
  
  // Professional relationships
  relationships: {
    reportsTo?: Contact;
    directReports: Contact[];
    collaborators: Contact[];
    isDecisionMaker: boolean;
    influenceLevel: "high" | "medium" | "low";
  };
  
  // Interaction history
  interactionHistory: CommunicationHistory[];
  upcomingActivities: ScheduledActivity[];
  personalNotes: Note[];
}
```

---

## 🗄️ Data Models

### BusinessEntity Model

```typescript
interface BusinessEntity {
  // Core identification
  id: string;
  entityCode: string;                     // Internal reference code
  entityType: "business" | "individual" | "government" | "non_profit";
  
  // Basic information
  businessName?: string;                  // For business entities
  firstName?: string;                     // For individual entities
  lastName?: string;                      // For individual entities
  displayName: string;                    // Primary display name
  
  // Greek business compliance
  afm?: string;                          // Greek Tax Number (9 digits)
  doy?: string;                          // Greek Tax Office Code
  businessActivity?: string;              // Primary business activity
  legalForm?: string;                     // ΑΕ, ΕΠΕ, ΟΕ, ΕΕ, etc.
  vatNumber?: string;                     // EU VAT number
  vatExempt: boolean;
  
  // Contact information
  email?: string;
  phone?: string;
  mobile?: string;
  website?: string;
  
  // Address (Greek format)
  address: GreekAddress;
  billingAddress?: GreekAddress;          // If different from primary
  
  // Business relationship roles
  roles: BusinessEntityRole[];           // Customer, Supplier, Partner, etc.
  
  // Status and classification
  status: "active" | "inactive" | "suspended" | "prospect" | "blocked";
  entityCategory?: string;                // A, B, C classification
  entitySegment?: string;                 // Market segment
  
  // Financial information
  creditLimit: number;
  paymentTerms: PaymentTerms;
  discountPercentage: number;
  
  // Supplier-specific information
  supplierRating?: number;                // 1-5 rating
  supplierCategory?: string;              // Preferred, Standard, etc.
  leadTimeDays: number;
  minimumOrderAmount?: number;
  
  // CRM information
  leadSource?: string;
  assignedUserId?: string;
  tags: string[];
  notes?: string;
  
  // Business metrics
  totalSales: number;                     // Lifetime sales to this entity
  totalPurchases: number;                 // Lifetime purchases from this entity
  totalOrders: number;
  totalPurchaseOrders: number;
  lastOrderDate?: Date;
  lastPurchaseDate?: Date;
  firstOrderDate?: Date;
  firstPurchaseDate?: Date;
  
  // Preferences
  language: "el" | "en";
  preferredContactMethod: "email" | "phone" | "meeting";
  marketingConsent: boolean;
  newsletterSubscription: boolean;
  
  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

interface GreekAddress {
  street: string;
  number: string;
  area?: string;                          // Greek neighborhood/area
  city: string;
  postalCode: string;                     // Greek postal format (5 digits)
  region: string;                         // Greek periphery
  country: string;                        // Default: "GR"
}

type BusinessEntityRole = 
  | "customer"                            // Buys from us
  | "supplier"                            // Sells to us
  | "partner"                             // Collaborates with us
  | "competitor"                          // Competes with us
  | "prospect"                            // Potential customer/supplier
  | "lead";                               // Sales lead

type PaymentTerms = 
  | "net_0"                               // Cash on delivery
  | "net_15" | "net_30" | "net_60" | "net_90"
  | "prepaid";                            // Prepayment required
```

### Contact Model

```typescript
interface Contact {
  // Core identification
  id: string;
  businessEntityId: string;               // Parent business entity
  contactCode?: string;
  contactType: ContactType;
  
  // Personal information
  firstName: string;
  lastName: string;
  middleName?: string;
  displayName?: string;
  
  // Greek personal information
  fatherName?: string;                    // Greek requirement
  motherName?: string;                    // Greek requirement
  amka?: string;                          // Greek Social Security (11 digits)
  idCardNumber?: string;
  
  // Professional information
  jobTitle?: string;
  department?: string;
  reportsToId?: string;                   // Manager contact ID
  
  // Contact information
  email?: string;
  phone?: string;
  mobile?: string;
  
  // Address (if different from business entity)
  address?: GreekAddress;
  
  // Status and preferences
  status: ContactStatus;
  isPrimaryContact: boolean;
  isDecisionMaker: boolean;
  preferredContactMethod: "email" | "phone" | "meeting";
  language: "el" | "en";
  timezone: string;
  
  // Marketing preferences
  marketingConsent: boolean;
  newsletterSubscription: boolean;
  emailOptIn: boolean;
  smsOptIn: boolean;
  
  // Social media
  linkedinUrl?: string;
  twitterHandle?: string;
  otherSocialMedia: Record<string, string>;
  
  // CRM information
  leadSource?: string;
  assignedUserId?: string;
  tags: string[];
  notes?: string;
  
  // Interaction tracking
  lastContactDate?: Date;
  lastEmailDate?: Date;
  lastCallDate?: Date;
  lastMeetingDate?: Date;
  totalInteractions: number;
  
  // Engagement metrics
  emailOpens: number;
  emailClicks: number;
  emailBounces: number;
  
  // Important dates
  birthDate?: Date;
  anniversaryDate?: Date;
  
  // Extensibility
  customFields: Record<string, any>;
  
  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

type ContactType = 
  | "primary"                             // Main contact
  | "secondary"                           // Additional contact
  | "billing"                             // Billing contact
  | "technical"                           // Technical contact
  | "sales"                               // Sales contact
  | "support"                             // Support contact
  | "decision_maker"                      // Decision maker
  | "influencer";                         // Influencer in decisions

type ContactStatus = 
  | "active"
  | "inactive"
  | "bounced"                             // Email bounced
  | "unsubscribed"                        // Unsubscribed from communications
  | "do_not_contact";                     // Do not contact
```

---

## 🔗 API Endpoints

### Business Entity APIs

```typescript
// GET /api/businesses - List all business entities
interface GetBusinessEntitiesRequest {
  page?: number;
  limit?: number;
  search?: string;
  roles?: BusinessEntityRole[];           // Filter by roles
  status?: string[];
  assignedUserId?: string;
  healthScoreMin?: number;
  totalValueMin?: number;
  sort?: "name" | "totalValue" | "healthScore" | "lastActivity";
  order?: "asc" | "desc";
}

interface GetBusinessEntitiesResponse {
  businesses: BusinessEntity[];
  total: number;
  page: number;
  limit: number;
  filters: AppliedFilters;
}

// GET /api/businesses/:id - Get complete 360° business view
interface GetBusinessResponse {
  business: BusinessEntity;
  contacts: Contact[];
  healthScore: BusinessHealthScore;
  recentActivity: Activity[];
  financialSummary: FinancialSummary;
  
  // Module-specific data (if enabled)
  opportunities?: Opportunity[];
  orders?: Order[];
  invoices?: Invoice[];
  payments?: Payment[];
  supportTickets?: SupportTicket[];
}

// POST /api/businesses - Create new business entity
interface CreateBusinessEntityRequest {
  business: Omit<BusinessEntity, "id" | "createdAt" | "updatedAt">;
  initialRoles: BusinessEntityRole[];
  primaryContact?: Omit<Contact, "id" | "businessEntityId">;
}

// PUT /api/businesses/:id/roles - Update business entity roles
interface UpdateBusinessEntityRolesRequest {
  roles: {
    role: BusinessEntityRole;
    isActive: boolean;
    notes?: string;
  }[];
}

// GET /api/businesses/:id/health-score - Get detailed health scoring
interface GetBusinessHealthScoreResponse {
  overallScore: number;                   // 0-100
  breakdown: {
    financial: number;                    // Payment behavior, credit usage
    relationship: number;                 // Communication, satisfaction
    compliance: number;                   // Greek tax compliance
    growth: number;                       // Opportunity potential
  };
  recommendations: string[];
  riskFactors: string[];
  opportunities: string[];
}
```

### Contact APIs

```typescript
// GET /api/businesses/:id/contacts - List contacts within business
interface GetBusinessContactsResponse {
  contacts: Contact[];
  hierarchy: ContactHierarchy;
  engagementSummary: ContactEngagementSummary;
}

// POST /api/contacts - Create new contact
interface CreateContactRequest {
  contact: Omit<Contact, "id" | "createdAt" | "updatedAt">;
  businessEntityId: string;
}

// GET /api/contacts/:id/interactions - Get contact interaction history
interface GetContactInteractionsResponse {
  interactions: Interaction[];
  summary: InteractionSummary;
  upcomingActivities: ScheduledActivity[];
}
```

---

## 🔧 Implementation Strategy

### Phase 1: Core Business Entity (Month 1)

- ✅ BusinessEntity model with role system
- ✅ Contact management within BusinessEntity
- ✅ Basic 360° view with Overview and Contacts tabs
- ✅ Greek business validation and compliance

### Phase 2: CRM Integration (Month 2)

- Communications tab with complete interaction history
- Activity and task management linked to BusinessEntity
- Opportunity tracking with business context
- Lead conversion to BusinessEntity workflow

### Phase 3: ERP Integration (Month 3)

- Orders and invoices linked to BusinessEntity
- Payment tracking and credit management
- Supplier relationship management
- Financial health scoring and analytics

### Phase 4: Advanced Features (Month 4)

- Support ticket integration
- Document management and sharing
- Advanced business intelligence and reporting
- Workflow automation and business rules

### Phase 5: Greek Market Optimization (Month 5)

- Complete AADE integration in business view
- Greek banking and payment integration
- Professional certification tracking
- Regulatory compliance automation

---

## 🎯 Success Metrics

### User Experience

- **Information Access**: < 10 seconds to find any business information
- **Context Switches**: 90% reduction in CRM ↔ ERP navigation
- **User Satisfaction**: 95% prefer unified view over separate systems

### Business Impact

- **Relationship Intelligence**: 40% improvement in business relationship insights
- **Sales Efficiency**: 25% faster deal closure with complete business context
- **Customer Satisfaction**: 30% improvement from unified communication view

### System Performance

- **Load Performance**: < 2 seconds for complete 360° business view
- **Data Accuracy**: 99.9% consistency between CRM and ERP data
- **Mobile Experience**: Full functionality on tablets and smartphones

This unified approach eliminates traditional business management silos and creates an experience that business users will love.
