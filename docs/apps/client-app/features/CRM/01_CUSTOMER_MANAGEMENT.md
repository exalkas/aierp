# 01_CUSTOMER_MANAGEMENT - Core Foundation

## Document Information

- **Feature**: Customer Management (Contacts, Accounts, Leads)
- **Priority**: ⭐ CRITICAL FIRST - Foundation for all CRM
- **Implementation**: Month 1 (Phase 1)
- **Dependencies**: Authentication, Core Infrastructure
- **Impact**: Enables all other CRM functionality

## 🎯 Feature Overview

Customer Management forms the foundation of the entire CRM system, providing comprehensive contact, account, and lead management with Greek market specialization.

### Core Capabilities

- **Contact Management**: Complete contact lifecycle with Greek-specific fields
- **Account Management**: Company profiles and business relationships
- **Lead Management**: Lead capture, qualification, and conversion
- **Greek Integration**: AFM validation, Greek addresses, business compliance

---

## 📋 Screens & User Interface

### 1. Contact Management Screens

#### Contact List Screen (`/contacts`)

```typescript
interface ContactListScreen {
  // Grid with filtering, sorting, pagination
  // Quick search (name, email, phone, AFM)
  // Bulk actions (email, assign, tag, export)
  // Column customization and saved views
  // Advanced filters (location, industry, tags)
}
```

#### Contact Detail Screen (`/contacts/:id`) - **Unified Customer Hub**

```typescript
interface ContactDetailScreen {
  // Core Customer Information (Always Available)
  overview: CustomerOverview; // Personal info, Greek fields, summary metrics
  communications: CustomerCommunications; // Email, calls, meetings, SMS history
  activities: CustomerActivities; // Tasks, notes timeline
  appointments: CustomerAppointments; // Scheduled meetings, consultations, services
  relationships: CustomerRelationships; // Contacts, accounts, opportunities

  // Conditional Tabs (Based on Purchased Modules)
  orders?: OrderHistory; // Only if ERP/invoicing module purchased
  invoices?: InvoiceHistory; // Only if ERP/invoicing module purchased
  payments?: PaymentHistory; // Only if ERP/invoicing module purchased
  projects?: ProjectHistory; // Only if project management purchased
  support?: SupportTickets; // Only if support module purchased

  // Tab Visibility Logic
  availableTabs: TabConfiguration[]; // Dynamic based on user's purchased modules
  modulePermissions: ModuleAccess[]; // What tabs user can access
}

interface CustomerCommunications {
  emailHistory: EmailCommunication[]; // Complete email thread history
  phoneCallLogs: PhoneCall[]; // Call records with duration, notes
  meetingNotes: Meeting[]; // Meeting summaries and outcomes
  smsHistory: SMSCommunication[]; // SMS conversation history
  socialInteractions: SocialInteraction[]; // Social media engagements
  voiceCommands: VoiceCommand[]; // Voice command history and accuracy
  communicationSummary: CommunicationMetrics; // Frequency, preferences, response rates
  nextFollowUp?: ScheduledFollowUp; // Planned next contact
}

interface TabConfiguration {
  key: string; // Tab identifier
  label: string; // Display name (Greek)
  icon: string; // Tab icon
  requiredModule?: string; // Module needed for visibility
  permissionLevel: "view" | "edit" | "admin"; // User access level required
  badgeCount?: number; // Notification count (e.g., unread emails)
  isDefault?: boolean; // Whether tab loads by default
}
```

#### Contact Form Screen (`/contacts/new` | `/contacts/:id/edit`)

```typescript
interface ContactFormScreen {
  // Multi-step form with validation
  // Greek address autocomplete
  // Duplicate detection and merge
  // Custom field support
  // Photo and social media integration
}
```

### 2. Account Management Screens

#### Account List Screen (`/accounts`)

```typescript
interface AccountListScreen {
  // Company overview with metrics
  // Revenue tracking and growth
  // Contact hierarchy display
  // Account health scoring
  // Territory management
}
```

#### Account Detail Screen (`/accounts/:id`)

```typescript
interface AccountDetailScreen {
  // Company profile with Greek details
  // Financial summary and credit info
  // Contact roster with roles
  // Opportunity pipeline view
  // Greek tax information (VAT, DOY)
}
```

### 3. Lead Management Screens

#### Lead List Screen (`/leads`)

```typescript
interface LeadListScreen {
  // Lead scoring and status
  // Source tracking and attribution
  // Assignment and routing rules
  // Conversion funnel analytics
  // Bulk import processing
}
```

#### Lead Detail Screen (`/leads/:id`)

```typescript
interface LeadDetailScreen {
  // Qualification information
  // Interest and preferences
  // Communication history
  // Lead scoring breakdown
  // Conversion probability
}
```

#### Lead Conversion Screen (`/leads/:id/convert`)

```typescript
interface LeadConversionScreen {
  // Convert to contact/account/opportunity
  // Data mapping and validation
  // Workflow automation triggers
  // Source attribution tracking
}
```

---

## 🗄️ Data Models

### Contact Model

```typescript
interface Contact {
  // Core Fields
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;

  // Greek-Specific Fields
  fatherName?: string; // Required for Greek legal docs
  motherName?: string; // Optional Greek field
  afm?: string; // Greek Tax ID (AFM)
  amka?: string; // Greek Social Security (AMKA)
  idCard?: string; // Greek ID card number

  // Address (Greek Format)
  address: GreekAddress;

  // Business Fields
  title?: string;
  company?: string;
  accountId?: string; // Link to Account
  industry?: string;

  // Relationship Fields
  leadSource?: string;
  assignedUserId?: string;
  teamIds?: string[];
  tags?: string[];

  // Custom Fields (EspoCRM-style)
  customFields?: Record<string, any>;

  // Audit Fields
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

interface GreekAddress {
  street: string;
  number: string;
  area?: string; // Greek neighborhood
  city: string;
  postalCode: string; // Greek postal format
  region: string; // Greek periphery
  country: string; // Default: Greece
}
```

### Account Model

```typescript
interface Account {
  // Core Fields
  id: string;
  name: string;
  website?: string;
  phone?: string;

  // Greek Business Fields
  afm: string; // Required Greek Tax ID
  doy: string; // Greek Tax Office
  vatNumber?: string; // EU VAT if applicable
  gemiNumber?: string; // Greek Business Registry

  // Business Information
  industry: string;
  type: "customer" | "prospect" | "partner" | "competitor";
  size?: "small" | "medium" | "large" | "enterprise";
  revenue?: number;
  employees?: number;

  // Address
  billingAddress: GreekAddress;
  shippingAddress?: GreekAddress;

  // Relationship Fields
  parentAccountId?: string;
  assignedUserId?: string;
  teamIds?: string[];

  // Financial Fields
  creditLimit?: number;
  paymentTerms?: string;
  currency: string; // Default: EUR

  // Custom Fields
  customFields?: Record<string, any>;

  // Audit Fields
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}
```

### Lead Model

```typescript
interface Lead {
  // Core Fields
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  company?: string;

  // Lead Qualification
  status: "new" | "assigned" | "qualified" | "unqualified" | "converted";
  source: string; // Campaign, website, referral, etc.
  rating?: "hot" | "warm" | "cold";
  score?: number; // Lead scoring (0-100)

  // Greek Fields
  afm?: string;
  address?: GreekAddress;

  // Business Information
  title?: string;
  industry?: string;
  revenue?: number;
  employees?: number;

  // Qualification Details
  budget?: number;
  decisionMaker?: boolean;
  timeline?: string;
  requirements?: string;

  // Assignment
  assignedUserId?: string;
  teamIds?: string[];

  // Conversion Tracking
  convertedDate?: Date;
  convertedContactId?: string;
  convertedAccountId?: string;
  convertedOpportunityId?: string;

  // Custom Fields
  customFields?: Record<string, any>;

  // Audit Fields
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}
```

### Communication Models (Customer Hub)

```typescript
interface EmailCommunication {
  id: string;
  customerId: string;
  direction: "inbound" | "outbound";
  fromEmail: string;
  toEmails: string[];
  ccEmails?: string[];
  subject: string;
  body: string;
  htmlBody?: string;
  attachments?: EmailAttachment[];
  threadId?: string; // Group related emails
  isRead: boolean;
  sentAt: Date;
  receivedAt?: Date;
  engagementScore?: number; // Opens, clicks, replies
  tags?: string[];
  createdAt: Date;
}

interface PhoneCall {
  id: string;
  customerId: string;
  direction: "inbound" | "outbound";
  fromNumber: string;
  toNumber: string;
  duration: number; // seconds
  startTime: Date;
  endTime: Date;
  status: "completed" | "missed" | "busy" | "voicemail";
  notes?: string;
  recording?: string; // file path or URL
  transcription?: string;
  callOutcome?:
    | "interested"
    | "not_interested"
    | "callback"
    | "meeting_scheduled";
  followUpRequired?: boolean;
  createdBy: string;
  createdAt: Date;
}

interface Meeting {
  id: string;
  customerId: string;
  type: "in_person" | "video_call" | "phone_meeting";
  subject: string;
  description?: string;
  startTime: Date;
  endTime: Date;
  location?: string; // Or video meeting URL
  attendees: MeetingAttendee[];
  agenda?: string[];
  notes?: string;
  outcomes?: string[];
  nextSteps?: string[];
  attachments?: MeetingAttachment[];
  createdBy: string;
  createdAt: Date;
}

interface SMSCommunication {
  id: string;
  customerId: string;
  direction: "inbound" | "outbound";
  fromNumber: string;
  toNumber: string;
  message: string;
  sentAt: Date;
  deliveredAt?: Date;
  readAt?: Date;
  threadId?: string; // Group SMS conversation
  isRead: boolean;
  createdAt: Date;
}

interface SocialInteraction {
  id: string;
  customerId: string;
  platform: "facebook" | "linkedin" | "twitter" | "instagram";
  interactionType: "like" | "comment" | "share" | "direct_message" | "mention";
  content?: string;
  postUrl?: string;
  timestamp: Date;
  engagementLevel: "low" | "medium" | "high";
  createdAt: Date;
}

interface CommunicationMetrics {
  totalEmails: number;
  totalCalls: number;
  totalMeetings: number;
  totalSMS: number;
  averageResponseTime: number; // hours
  preferredCommunicationMethod: "email" | "phone" | "sms" | "meeting";
  lastContactDate: Date;
  engagementScore: number; // 0-100
  communicationFrequency: "daily" | "weekly" | "monthly" | "quarterly";
}

interface ScheduledFollowUp {
  id: string;
  customerId: string;
  type: "email" | "call" | "meeting" | "sms";
  scheduledDate: Date;
  purpose: string;
  notes?: string;
  status: "scheduled" | "completed" | "cancelled" | "overdue";
  createdBy: string;
  createdAt: Date;
}

interface ModuleAccess {
  module: string; // "invoicing", "projects", "support", etc.
  hasAccess: boolean;
  permissions: ("view" | "create" | "edit" | "delete")[];
  purchaseDate?: Date;
  expirationDate?: Date;
  licenseType?: "basic" | "professional" | "enterprise";
}

interface CustomerOverview {
  basicInfo: Contact; // Core contact information
  healthScore: number; // Overall customer health (0-100)
  lifetimeValue: number; // CLV if available
  firstContact: Date;
  lastActivity: Date;
  totalInteractions: number;
  upcomingAppointments: number; // Count of scheduled appointments
  preferredLanguage: "el" | "en"; // Greek or English
  complianceStatus: {
    gdprConsent: boolean;
    dataRetentionExpiry?: Date;
    communicationPreferences: ("email" | "phone" | "sms" | "post")[];
  };
}

interface CustomerAppointments {
  upcomingAppointments: Appointment[]; // Scheduled future appointments
  pastAppointments: Appointment[]; // Historical appointment records
  appointmentHistory: AppointmentHistory[]; // Complete appointment timeline
  appointmentPreferences: AppointmentPreferences; // Customer scheduling preferences
  appointmentSummary: AppointmentMetrics; // Appointment statistics and patterns
  recurringAppointments?: RecurringAppointment[]; // Regular appointment schedules
}

interface Appointment {
  id: string;
  customerId: string;
  type: AppointmentType;
  title: string;
  description?: string;

  // Scheduling Details
  startTime: Date;
  endTime: Date;
  duration: number; // minutes
  timeZone: string;
  location?: AppointmentLocation;

  // Participants
  assignedStaffId?: string; // Staff member handling appointment
  attendees?: AppointmentAttendee[];

  // Service Details (for service-based appointments)
  serviceId?: string;
  serviceName?: string;
  servicePrice?: number;
  serviceCategory?: ServiceCategory;

  // Status & Workflow
  status: AppointmentStatus;
  confirmationStatus: ConfirmationStatus;
  remindersSent: ReminderLog[];
  cancellationReason?: string;

  // Business Context
  appointmentSource: AppointmentSource;
  priority: AppointmentPriority;
  tags?: string[];

  // Follow-up
  outcome?: AppointmentOutcome;
  notes?: string;
  followUpRequired?: boolean;
  nextAppointmentId?: string;

  // Integration
  linkedRecords?: {
    opportunityId?: string;
    leadId?: string;
    projectId?: string;
    caseId?: string;
  };

  // Greek Business Features
  greekHolidayConflict?: boolean;
  nameDay?: boolean; // If appointment is for name day celebration

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

type AppointmentType =
  | "sales_meeting"
  | "consultation"
  | "service_delivery"
  | "follow_up"
  | "demo"
  | "training"
  | "support"
  | "haircut"
  | "beauty_service"
  | "professional_service"
  | "technical_service";

type AppointmentStatus =
  | "scheduled"
  | "confirmed"
  | "in_progress"
  | "completed"
  | "cancelled"
  | "no_show"
  | "rescheduled";

type ConfirmationStatus =
  | "pending"
  | "confirmed"
  | "declined"
  | "auto_confirmed";

type AppointmentSource =
  | "online_booking"
  | "phone_call"
  | "walk_in"
  | "staff_created"
  | "lead_conversion"
  | "recurring_schedule";

type AppointmentPriority = "low" | "normal" | "high" | "urgent";

interface AppointmentLocation {
  type: "physical" | "virtual" | "phone";
  address?: GreekAddress;
  meetingUrl?: string;
  roomNumber?: string;
  instructions?: string;
}

interface AppointmentAttendee {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  role: "customer" | "staff" | "third_party";
  attendance: "required" | "optional";
  responseStatus: "pending" | "accepted" | "declined";
}

interface AppointmentOutcome {
  outcome: "successful" | "cancelled" | "no_show" | "rescheduled";
  salesResult?: "sale_made" | "follow_up_needed" | "not_interested";
  serviceResult?:
    | "service_completed"
    | "service_partial"
    | "customer_unsatisfied";
  nextSteps?: string[];
  rating?: number; // 1-5 customer satisfaction
  revenue?: number;
  notes?: string;
}

interface AppointmentPreferences {
  preferredTimeSlots: TimeSlot[];
  preferredStaff?: string[];
  preferredServices?: string[];
  preferredLocation?: string;
  communicationPreferences: {
    confirmationMethod: "email" | "sms" | "phone" | "whatsapp";
    reminderFrequency: "none" | "once" | "twice" | "daily";
    reminderTiming: number[]; // hours before appointment
  };
  accessibilityRequirements?: string[];
  specialInstructions?: string;
}

interface AppointmentMetrics {
  totalAppointments: number;
  completedAppointments: number;
  cancelledAppointments: number;
  noShowRate: number;
  averageAppointmentValue: number;
  preferredAppointmentTypes: AppointmentType[];
  averageAdvanceBooking: number; // days
  punctualityScore: number; // 0-100
  satisfactionScore: number; // 0-100
  lastAppointmentDate?: Date;
  nextAppointmentDate?: Date;
}

interface RecurringAppointment {
  id: string;
  customerId: string;
  appointmentTemplate: Omit<Appointment, "id" | "startTime" | "endTime">;
  recurrencePattern: RecurrencePattern;
  nextOccurrence: Date;
  endDate?: Date;
  maxOccurrences?: number;
  generatedAppointments: string[]; // Appointment IDs
  isActive: boolean;
}

interface RecurrencePattern {
  type: "daily" | "weekly" | "monthly" | "yearly";
  interval: number; // Every N days/weeks/months
  daysOfWeek?: number[]; // For weekly recurrence (0=Sunday)
  dayOfMonth?: number; // For monthly recurrence
  weekOfMonth?: number; // For monthly recurrence (1st, 2nd, etc.)
  monthOfYear?: number; // For yearly recurrence
  excludeGreekHolidays?: boolean;
}

interface TimeSlot {
  dayOfWeek: number; // 0-6 (Sunday-Saturday)
  startTime: string; // HH:MM format
  endTime: string; // HH:MM format
}

interface ServiceCategory {
  id: string;
  name: string;
  icon: string;
  color: string;
  businessType: "salon" | "professional" | "sales" | "support" | "general";
}
```

### Voice Command System

```typescript
interface VoiceCommand {
  id: string;
  userId: string;
  customerId?: string; // If command was executed in customer context

  // Audio Processing
  audioUrl?: string; // Original audio file (temporary storage)
  audioLength: number; // Duration in seconds
  transcriptRaw: string; // Raw Whisper output
  transcriptProcessed: string; // Cleaned/normalized text
  language: "el" | "en" | "mixed"; // Detected language
  confidence: number; // STT confidence (0-100)

  // Command Understanding
  intent: VoiceIntent;
  entities: VoiceEntity[]; // Extracted entities (names, numbers, etc.)
  parameters: Record<string, any>; // Parsed command parameters

  // Execution
  status: VoiceCommandStatus;
  executedAction?: string; // What action was taken
  executionResult?: any; // Result data
  errorMessage?: string;

  // Context
  contextModule: string; // Which CRM module user was in
  contextScreen: string; // Specific screen/page
  contextData?: Record<string, any>; // Additional context

  // Performance
  processingTime: number; // Total processing time (ms)
  sttTime: number; // Speech-to-text time (ms)
  nlpTime: number; // Natural language processing time (ms)

  // Audit
  createdAt: Date;
  completedAt?: Date;
}

type VoiceCommandStatus =
  | "processing"
  | "completed"
  | "failed"
  | "cancelled"
  | "partially_completed";

interface VoiceIntent {
  action: VoiceAction;
  confidence: number; // Intent classification confidence (0-100)
  alternativeIntents?: {
    action: VoiceAction;
    confidence: number;
  }[];
}

type VoiceAction =
  // Navigation
  | "navigate_to_customers"
  | "navigate_to_leads"
  | "navigate_to_appointments"
  | "navigate_to_reports"
  | "open_calendar"
  | "go_back"
  | "go_home"

  // Customer Management
  | "create_customer"
  | "find_customer"
  | "edit_customer"
  | "add_customer_note"
  | "call_customer"
  | "email_customer"

  // Appointment Management
  | "schedule_appointment"
  | "reschedule_appointment"
  | "cancel_appointment"
  | "find_availability"
  | "view_today_schedule"

  // Communication
  | "log_call"
  | "send_email"
  | "add_note"
  | "create_task"
  | "schedule_followup"

  // Data Entry
  | "add_product"
  | "create_lead"
  | "update_opportunity"
  | "create_quote"

  // Search & Filter
  | "search_customers"
  | "filter_by_status"
  | "show_recent"
  | "find_appointments_today"

  // Reports & Analytics
  | "show_sales_report"
  | "view_customer_stats"
  | "generate_report";

interface VoiceEntity {
  type: VoiceEntityType;
  value: string; // Raw extracted value
  normalizedValue: any; // Processed/typed value
  confidence: number;
  startIndex: number; // Position in transcript
  endIndex: number;
}

type VoiceEntityType =
  | "customer_name"
  | "customer_id"
  | "phone_number"
  | "email"
  | "date"
  | "time"
  | "duration"
  | "amount"
  | "product_name"
  | "service_type"
  | "location"
  | "priority"
  | "status"
  | "note_text"
  | "greek_afm"
  | "greek_city";

// Voice Command Processing Pipeline
interface VoiceCommandRequest {
  audioBlob: Blob; // Audio data from client
  contextModule: string; // Current CRM module
  contextScreen: string; // Current screen
  contextData?: Record<string, any>; // Additional context
  userId: string;
  customerId?: string; // If in customer context
}

interface VoiceCommandResponse {
  commandId: string;
  status: VoiceCommandStatus;

  // Processing Results
  transcript: string;
  intent: VoiceIntent;
  entities: VoiceEntity[];

  // Client Actions
  action: ClientAction;
  message: string; // User feedback message

  // Error Handling
  error?: {
    type: "stt_error" | "nlp_error" | "execution_error" | "validation_error";
    message: string;
    suggestions?: string[];
  };
}

interface ClientAction {
  type: ClientActionType;
  payload?: any;
  navigation?: {
    route: string;
    params?: Record<string, any>;
  };
  modal?: {
    component: string;
    props?: Record<string, any>;
    prefill?: Record<string, any>; // Pre-filled form data
  };
  notification?: {
    type: "success" | "error" | "info" | "warning";
    message: string;
    duration?: number;
  };
}

type ClientActionType =
  | "navigate"
  | "open_modal"
  | "fill_form"
  | "show_notification"
  | "refresh_data"
  | "update_ui"
  | "start_web_speech" // Continue with Web Speech API for form filling
  | "execute_search"
  | "apply_filter";

// Greek Language Support
interface GreekVoiceSupport {
  // Common Greek business terms
  businessTerms: Map<string, string>; // "πελάτης" -> "customer"

  // Name normalization
  greekNames: string[]; // Common Greek first/last names

  // Address parsing
  greekCities: string[];
  greekRegions: string[];
  streetTypes: string[]; // "οδός", "λεωφόρος", etc.

  // Number processing
  greekNumbers: Map<string, number>; // "τρία" -> 3

  // Business contexts
  appointmentTerms: string[]; // "ραντεβού", "συνάντηση"
  serviceTerms: string[]; // "υπηρεσία", "κούρεμα"
}

// Voice Command Examples for Different Modules
interface VoiceCommandExamples {
  // Customer Management
  customerCommands: [
    "δημιούργησε νέο πελάτη", // Create new customer
    "βρες πελάτη Παπαδόπουλος", // Find customer Papadopoulos
    "κάλεσε τον Γιάννη", // Call John
    "πρόσθεσε σημείωση στον πελάτη", // Add note to customer
    "στείλε email στην Μαρία" // Send email to Maria
  ];

  // Appointment Management
  appointmentCommands: [
    "προγραμμάτισε ραντεβού για αύριο στις τρεις", // Schedule appointment tomorrow at 3
    "ακύρωσε το ραντεβού του Κώστα", // Cancel Kostas' appointment
    "δείξε το πρόγραμμα σήμερα", // Show today's schedule
    "βρες διαθέσιμη ώρα για κούρεμα", // Find available time for haircut
    "μετάθεσε το ραντεβού για Δευτέρα" // Reschedule appointment for Monday
  ];

  // Navigation
  navigationCommands: [
    "πήγαινε στους πελάτες", // Go to customers
    "άνοιξε το ημερολόγιο", // Open calendar
    "δείξε τις αναφορές", // Show reports
    "πίσω στην αρχική", // Back to home
    "εύρεση προσόπων" // Find leads
  ];

  // Mixed Greek/English (common in business)
  mixedCommands: [
    "δημιούργησε νέο lead για την ABC company", // Create new lead for ABC company
    "στείλε email follow-up στον πελάτη", // Send follow-up email to customer
    "schedule meeting με τον manager", // Schedule meeting with manager
    "update το status σε completed" // Update status to completed
  ];
}
```

---

## 🔌 API Specifications

### Contact APIs

```typescript
// GET /api/contacts - List contacts with filtering
interface GetContactsRequest {
  page?: number;
  limit?: number;
  search?: string;
  filters?: {
    assignedUserId?: string;
    accountId?: string;
    tags?: string[];
    industry?: string;
    location?: string;
  };
  sort?: {
    field: string;
    direction: "asc" | "desc";
  };
}

interface GetContactsResponse {
  data: Contact[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
  filters: FilterMetadata;
}

// POST /api/contacts - Create new contact
interface CreateContactRequest {
  contact: Omit<
    Contact,
    "id" | "createdAt" | "updatedAt" | "createdBy" | "updatedBy"
  >;
  duplicateCheck?: boolean;
}

interface CreateContactResponse {
  contact: Contact;
  duplicates?: Contact[]; // If duplicates found
}

// PUT /api/contacts/:id - Update contact
interface UpdateContactRequest {
  contact: Partial<Contact>;
  merge?: boolean; // Merge with existing data
}

// DELETE /api/contacts/:id - Delete contact
interface DeleteContactRequest {
  transferData?: {
    newContactId?: string; // Transfer relationships
    newAccountId?: string;
  };
}

// POST /api/contacts/validate-afm - Validate Greek AFM
interface ValidateAfmRequest {
  afm: string;
}

interface ValidateAfmResponse {
  valid: boolean;
  details?: {
    company?: string;
    status?: string;
    doy?: string;
  };
}
```

### Account APIs

```typescript
// GET /api/accounts - List accounts
interface GetAccountsRequest extends GetContactsRequest {
  filters?: {
    assignedUserId?: string;
    type?: string;
    industry?: string;
    size?: string;
    revenue?: { min?: number; max?: number };
  };
}

// POST /api/accounts - Create account
interface CreateAccountRequest {
  account: Omit<
    Account,
    "id" | "createdAt" | "updatedAt" | "createdBy" | "updatedBy"
  >;
  autoCreateContacts?: boolean; // Create contact for key personnel
}

// POST /api/accounts/lookup-greek-business - Lookup by AFM
interface LookupGreekBusinessRequest {
  afm: string;
}

interface LookupGreekBusinessResponse {
  found: boolean;
  business?: {
    name: string;
    afm: string;
    doy: string;
    status: string;
    address: GreekAddress;
  };
}
```

### Lead APIs

```typescript
// GET /api/leads - List leads
interface GetLeadsRequest extends GetContactsRequest {
  filters?: {
    status?: string;
    source?: string;
    rating?: string;
    assignedUserId?: string;
    score?: { min?: number; max?: number };
  };
}

// POST /api/leads - Create lead
interface CreateLeadRequest {
  lead: Omit<
    Lead,
    "id" | "createdAt" | "updatedAt" | "createdBy" | "updatedBy"
  >;
  autoScore?: boolean; // Calculate lead score
  autoAssign?: boolean; // Apply assignment rules
}

// POST /api/leads/:id/convert - Convert lead
interface ConvertLeadRequest {
  createContact?: boolean;
  createAccount?: boolean;
  createOpportunity?: boolean;
  contactData?: Partial<Contact>;
  accountData?: Partial<Account>;
  opportunityData?: any; // Defined in sales management
}

interface ConvertLeadResponse {
  contact?: Contact;
  account?: Account;
  opportunity?: any;
  lead: Lead; // Updated with conversion data
}

// POST /api/leads/score - Calculate lead score
interface ScoreLeadRequest {
  leadId?: string;
  leadData?: Partial<Lead>;
}

interface ScoreLeadResponse {
  score: number;
  factors: {
    factor: string;
    weight: number;
    value: number;
  }[];
}
```

### Customer Hub APIs (Unified Customer View)

```typescript
// GET /api/customers/:id/hub - Get unified customer hub data
interface GetCustomerHubRequest {
  customerId: string;
  includeModules?: string[]; // Which optional modules to load
  dateRange?: {
    from: Date;
    to: Date;
  };
}

interface GetCustomerHubResponse {
  overview: CustomerOverview;
  communications: CustomerCommunications;
  activities: CustomerActivities;
  relationships: CustomerRelationships;
  availableTabs: TabConfiguration[];
  moduleData?: {
    orders?: OrderHistory;
    invoices?: InvoiceHistory;
    payments?: PaymentHistory;
    projects?: ProjectHistory;
    support?: SupportTickets;
  };
}

// GET /api/customers/:id/communications - Get communication history
interface GetCommunicationsRequest {
  customerId: string;
  type?: "email" | "phone" | "meeting" | "sms" | "social";
  page?: number;
  limit?: number;
  dateRange?: {
    from: Date;
    to: Date;
  };
}

interface GetCommunicationsResponse {
  data: (
    | EmailCommunication
    | PhoneCall
    | Meeting
    | SMSCommunication
    | SocialInteraction
  )[];
  pagination: PaginationInfo;
  summary: CommunicationMetrics;
}

// POST /api/customers/:id/communications/email - Log email communication
interface LogEmailRequest {
  customerId: string;
  direction: "inbound" | "outbound";
  fromEmail: string;
  toEmails: string[];
  subject: string;
  body: string;
  attachments?: EmailAttachment[];
  threadId?: string;
}

// POST /api/customers/:id/communications/call - Log phone call
interface LogCallRequest {
  customerId: string;
  direction: "inbound" | "outbound";
  fromNumber: string;
  toNumber: string;
  duration: number;
  notes?: string;
  callOutcome?: string;
  followUpRequired?: boolean;
}

// GET /api/customers/:id/module-access - Check user's module access
interface GetModuleAccessResponse {
  modules: ModuleAccess[];
  availableTabs: TabConfiguration[];
  permissions: {
    canViewOrders: boolean;
    canViewInvoices: boolean;
    canViewPayments: boolean;
    canViewProjects: boolean;
    canViewSupport: boolean;
  };
}

// POST /api/customers/:id/follow-up - Schedule follow-up
interface ScheduleFollowUpRequest {
  customerId: string;
  type: "email" | "call" | "meeting" | "sms";
  scheduledDate: Date;
  purpose: string;
  notes?: string;
}

// GET /api/customers/:id/timeline - Get unified activity timeline
interface GetCustomerTimelineRequest {
  customerId: string;
  includeTypes?: (
    | "communication"
    | "activity"
    | "appointment"
    | "order"
    | "invoice"
    | "support"
  )[];
  page?: number;
  limit?: number;
  dateRange?: {
    from: Date;
    to: Date;
  };
}

interface GetCustomerTimelineResponse {
  timeline: TimelineItem[];
  pagination: PaginationInfo;
  filters: TimelineFilter[];
}

interface TimelineItem {
  id: string;
  type:
    | "email"
    | "call"
    | "meeting"
    | "sms"
    | "appointment"
    | "order"
    | "invoice"
    | "payment"
    | "note";
  title: string;
  description?: string;
  timestamp: Date;
  data: any; // Type-specific data
  user?: string; // Who performed the action
  moduleSource?: string; // Which module generated this item
}

// GET /api/customers/:id/appointments - Get customer appointments
interface GetCustomerAppointmentsRequest {
  customerId: string;
  status?: AppointmentStatus[];
  appointmentType?: AppointmentType[];
  dateRange?: {
    from: Date;
    to: Date;
  };
  includeRecurring?: boolean;
  page?: number;
  limit?: number;
}

interface GetCustomerAppointmentsResponse {
  appointments: Appointment[];
  upcomingCount: number;
  pastCount: number;
  recurringAppointments?: RecurringAppointment[];
  appointmentSummary: AppointmentMetrics;
  pagination: PaginationInfo;
}

// POST /api/customers/:id/appointments - Schedule new appointment
interface CreateAppointmentRequest {
  customerId: string;
  type: AppointmentType;
  title: string;
  description?: string;
  startTime: Date;
  duration: number; // minutes
  location?: AppointmentLocation;
  serviceId?: string;
  assignedStaffId?: string;
  priority?: AppointmentPriority;
  reminderSettings?: ReminderSettings;
  recurringSettings?: RecurrencePattern;
}

interface CreateAppointmentResponse {
  appointment: Appointment;
  conflicts?: ConflictWarning[];
  confirmationRequired: boolean;
  reminderScheduled: boolean;
}

// PUT /api/appointments/:id - Update appointment
interface UpdateAppointmentRequest {
  appointmentId: string;
  updates: Partial<Appointment>;
  notifyCustomer?: boolean;
  rescheduleReason?: string;
}

interface UpdateAppointmentResponse {
  appointment: Appointment;
  notificationSent: boolean;
  conflicts?: ConflictWarning[];
}

// POST /api/appointments/:id/confirm - Confirm appointment
interface ConfirmAppointmentRequest {
  appointmentId: string;
  confirmationMethod: "email" | "sms" | "phone" | "in_person";
  confirmedBy: string;
  customerNotes?: string;
}

// POST /api/appointments/:id/complete - Complete appointment
interface CompleteAppointmentRequest {
  appointmentId: string;
  outcome: AppointmentOutcome;
  duration?: number; // Actual duration if different
  notes?: string;
  nextAppointmentNeeded?: boolean;
  followUpTasks?: string[];
}

// GET /api/appointments/availability - Check availability
interface CheckAvailabilityRequest {
  startTime: Date;
  duration: number;
  staffId?: string;
  serviceId?: string;
  excludeAppointmentId?: string; // For rescheduling
}

interface CheckAvailabilityResponse {
  available: boolean;
  conflicts?: Appointment[];
  alternativeSlots?: AvailabilitySlot[];
}

// POST /api/appointments/bulk-schedule - Bulk appointment scheduling
interface BulkScheduleRequest {
  appointments: CreateAppointmentRequest[];
  conflictResolution: "skip" | "reschedule" | "override";
}

interface BulkScheduleResponse {
  scheduled: Appointment[];
  conflicts: ConflictResult[];
  failed: FailedScheduling[];
}

// Appointment-specific interfaces
interface ConflictWarning {
  type: "staff_conflict" | "resource_conflict" | "customer_conflict";
  conflictingAppointment: Appointment;
  severity: "warning" | "error";
  suggestedActions: string[];
}

interface AvailabilitySlot {
  startTime: Date;
  endTime: Date;
  staffId?: string;
  confidence: number; // 0-100 how likely this slot will work
  reason?: string;
}

interface ReminderSettings {
  enabled: boolean;
  methods: ("email" | "sms" | "push" | "whatsapp")[];
  timings: number[]; // hours before appointment
  customMessage?: string;
}

// Voice Command APIs
// POST /api/voice/process - Process voice command
interface ProcessVoiceCommandRequest {
  audioData: string; // Base64 encoded audio
  audioFormat: "webm" | "ogg" | "wav" | "mp3";
  contextModule: string;
  contextScreen: string;
  contextData?: Record<string, any>;
  userId: string;
  customerId?: string;
}

interface ProcessVoiceCommandResponse {
  commandId: string;
  transcript: string;
  confidence: number;
  language: "el" | "en" | "mixed";
  intent: VoiceIntent;
  entities: VoiceEntity[];
  action: ClientAction;
  message: string;
  processingTime: number;
  error?: VoiceCommandError;
}

// GET /api/voice/commands/:userId - Get user's voice command history
interface GetVoiceCommandsRequest {
  userId: string;
  limit?: number;
  offset?: number;
  dateRange?: {
    from: Date;
    to: Date;
  };
  module?: string;
  status?: VoiceCommandStatus[];
}

interface GetVoiceCommandsResponse {
  commands: VoiceCommand[];
  pagination: PaginationInfo;
  stats: {
    totalCommands: number;
    successRate: number;
    averageProcessingTime: number;
    mostUsedActions: { action: VoiceAction; count: number }[];
    languageDistribution: { language: string; count: number }[];
  };
}

// POST /api/voice/feedback - Provide feedback on voice command accuracy
interface VoiceCommandFeedbackRequest {
  commandId: string;
  feedback: "correct" | "incorrect" | "partially_correct";
  correctedTranscript?: string;
  correctedIntent?: VoiceAction;
  notes?: string;
}

// GET /api/voice/analytics - Voice command analytics
interface VoiceAnalyticsRequest {
  userId?: string;
  teamId?: string;
  dateRange: {
    from: Date;
    to: Date;
  };
}

interface VoiceAnalyticsResponse {
  overview: {
    totalCommands: number;
    successRate: number;
    averageProcessingTime: number;
    timeSaved: number; // Estimated time saved in minutes
  };
  trends: {
    dailyUsage: { date: Date; count: number }[];
    popularCommands: {
      action: VoiceAction;
      count: number;
      successRate: number;
    }[];
    languageUsage: { language: string; percentage: number }[];
  };
  performance: {
    sttAccuracy: number;
    intentAccuracy: number;
    entityExtractionAccuracy: number;
    averageLatency: number;
  };
  userAdoption: {
    activeUsers: number;
    commandsPerUser: number;
    retentionRate: number;
  };
}

// Voice Command Error Types
interface VoiceCommandError {
  type:
    | "audio_processing"
    | "stt_failed"
    | "intent_unclear"
    | "entity_missing"
    | "execution_failed"
    | "permission_denied";
  message: string;
  details?: any;
  suggestions?: string[];
  fallbackActions?: ClientAction[];
}
```

---

## ⚛️ React Components

### Core Components

```typescript
// Contact List Component
interface ContactListProps {
  filters?: ContactFilters;
  onContactSelect?: (contact: Contact) => void;
  onBulkAction?: (action: string, contacts: Contact[]) => void;
  showActions?: boolean;
  embedded?: boolean;
}

const ContactList: React.FC<ContactListProps> = ({ ... }) => {
  const { data, loading, refetch } = useContacts(filters);
  const { selectedContacts, handleSelection } = useContactSelection();

  return (
    <DataGrid<Contact>
      data={data}
      loading={loading}
      onRowSelect={handleSelection}
      actions={<ContactActions />}
      columns={contactColumns}
      filters={<ContactFilters />}
    />
  );
};

// Contact Form Component
interface ContactFormProps {
  contact?: Contact;
  onSave?: (contact: Contact) => void;
  onCancel?: () => void;
  mode?: 'create' | 'edit' | 'view';
}

const ContactForm: React.FC<ContactFormProps> = ({ contact, onSave, mode = 'create' }) => {
  const { form, handleSubmit, validate } = useContactForm(contact);
  const { validateAfm } = useGreekValidation();

  return (
    <FormBuilder
      schema={contactFormSchema}
      data={form}
      onSubmit={handleSubmit}
      validators={{ afm: validateAfm }}
      layout="tabs"
    />
  );
};

// Account Detail Component
interface AccountDetailProps {
  accountId: string;
  onEdit?: () => void;
}

const AccountDetail: React.FC<AccountDetailProps> = ({ accountId, onEdit }) => {
  const { account, loading } = useAccount(accountId);
  const { contacts } = useAccountContacts(accountId);
  const { opportunities } = useAccountOpportunities(accountId);

  return (
    <DetailLayout>
      <AccountHeader account={account} onEdit={onEdit} />
      <TabContainer>
        <Tab label="Overview">
          <AccountOverview account={account} />
        </Tab>
        <Tab label="Contacts">
          <ContactList filters={{ accountId }} embedded />
        </Tab>
        <Tab label="Opportunities">
          <OpportunityList filters={{ accountId }} embedded />
        </Tab>
      </TabContainer>
    </DetailLayout>
  );
};

// Lead Conversion Component
interface LeadConversionProps {
  lead: Lead;
  onConvert?: (result: ConvertLeadResponse) => void;
  onCancel?: () => void;
}

const LeadConversion: React.FC<LeadConversionProps> = ({ lead, onConvert }) => {
  const { convertLead } = useLeadConversion();
  const [conversionOptions, setConversionOptions] = useState({
    createContact: true,
    createAccount: true,
    createOpportunity: false,
  });

  return (
    <ConversionWizard>
      <Step1_ConversionOptions
        options={conversionOptions}
        onChange={setConversionOptions}
      />
      <Step2_DataMapping
        lead={lead}
        options={conversionOptions}
      />
      <Step3_Confirmation
        onConfirm={() => convertLead(lead, conversionOptions)}
      />
    </ConversionWizard>
  );
};
```

### Customer Hub Components (Unified Customer View)

```typescript
// Main Customer Hub Component
interface CustomerHubProps {
  customerId: string;
  defaultTab?: string;
}

const CustomerHub: React.FC<CustomerHubProps> = ({
  customerId,
  defaultTab = "overview",
}) => {
  const { hubData, loading } = useCustomerHub(customerId);
  const { moduleAccess } = useModuleAccess();
  const [activeTab, setActiveTab] = useState(defaultTab);

  const availableTabs = useMemo(() => {
    return (
      hubData?.availableTabs.filter(
        (tab) => !tab.requiredModule || moduleAccess[tab.requiredModule]
      ) || []
    );
  }, [hubData?.availableTabs, moduleAccess]);

  if (loading) return <CustomerHubSkeleton />;

  return (
    <CustomerHubLayout>
      <CustomerHubHeader customer={hubData.overview} />

      <TabNavigation>
        {availableTabs.map((tab) => (
          <TabButton
            key={tab.key}
            active={activeTab === tab.key}
            onClick={() => setActiveTab(tab.key)}
            badge={tab.badgeCount}
            icon={tab.icon}
          >
            {tab.label}
          </TabButton>
        ))}
      </TabNavigation>

      <TabContent>
        {activeTab === "overview" && (
          <CustomerOverviewTab data={hubData.overview} />
        )}
        {activeTab === "communications" && (
          <CustomerCommunicationsTab data={hubData.communications} />
        )}
        {activeTab === "activities" && (
          <CustomerActivitiesTab customerId={customerId} />
        )}
        {activeTab === "appointments" && (
          <CustomerAppointmentsTab
            data={hubData.appointments}
            customerId={customerId}
          />
        )}
        {activeTab === "relationships" && (
          <CustomerRelationshipsTab data={hubData.relationships} />
        )}

        {/* Conditional ERP/Module Tabs */}
        {activeTab === "orders" && moduleAccess.invoicing && (
          <CustomerOrdersTab customerId={customerId} />
        )}
        {activeTab === "invoices" && moduleAccess.invoicing && (
          <CustomerInvoicesTab customerId={customerId} />
        )}
        {activeTab === "payments" && moduleAccess.invoicing && (
          <CustomerPaymentsTab customerId={customerId} />
        )}
        {activeTab === "projects" && moduleAccess.projects && (
          <CustomerProjectsTab customerId={customerId} />
        )}
        {activeTab === "support" && moduleAccess.support && (
          <CustomerSupportTab customerId={customerId} />
        )}
      </TabContent>
    </CustomerHubLayout>
  );
};

// Communications Tab Component
interface CustomerCommunicationsTabProps {
  data: CustomerCommunications;
}

const CustomerCommunicationsTab: React.FC<CustomerCommunicationsTabProps> = ({
  data,
}) => {
  const [filter, setFilter] = useState<
    "all" | "email" | "phone" | "meeting" | "sms"
  >("all");
  const [timeRange, setTimeRange] = useState<
    "week" | "month" | "quarter" | "year"
  >("month");

  return (
    <CommunicationsLayout>
      <CommunicationsHeader>
        <CommunicationMetrics data={data.communicationSummary} />
        <CommunicationFilters
          filter={filter}
          onFilterChange={setFilter}
          timeRange={timeRange}
          onTimeRangeChange={setTimeRange}
        />
      </CommunicationsHeader>

      <CommunicationsTimeline>
        <EmailThreads
          emails={data.emailHistory}
          visible={filter === "all" || filter === "email"}
        />
        <CallLogs
          calls={data.phoneCallLogs}
          visible={filter === "all" || filter === "phone"}
        />
        <MeetingHistory
          meetings={data.meetingNotes}
          visible={filter === "all" || filter === "meeting"}
        />
        <SMSHistory
          sms={data.smsHistory}
          visible={filter === "all" || filter === "sms"}
        />
      </CommunicationsTimeline>

      <QuickActions>
        <Button icon="email" onClick={() => composeEmail()}>
          Στείλε Email
        </Button>
        <Button icon="phone" onClick={() => initiateCall()}>
          Κάλεσε
        </Button>
        <Button icon="calendar" onClick={() => scheduleMeeting()}>
          Προγραμμάτισε Συνάντηση
        </Button>
        <Button icon="sms" onClick={() => sendSMS()}>
          Στείλε SMS
        </Button>
      </QuickActions>

      {data.nextFollowUp && <UpcomingFollowUp followUp={data.nextFollowUp} />}
    </CommunicationsLayout>
  );
};

// Timeline Component for Unified Activity View
interface CustomerTimelineProps {
  customerId: string;
  includeModules?: string[];
}

const CustomerTimeline: React.FC<CustomerTimelineProps> = ({
  customerId,
  includeModules = [],
}) => {
  const { timeline, loading } = useCustomerTimeline(customerId, {
    includeModules,
  });
  const [groupBy, setGroupBy] = useState<"date" | "type">("date");

  return (
    <TimelineContainer>
      <TimelineHeader>
        <TimelineFilters groupBy={groupBy} onGroupByChange={setGroupBy} />
        <TimelineSearch placeholder="Αναζήτηση στο ιστορικό..." />
      </TimelineHeader>

      <TimelineContent>
        {loading ? (
          <TimelineSkeleton />
        ) : (
          timeline.map((item) => (
            <TimelineItem
              key={item.id}
              type={item.type}
              title={item.title}
              description={item.description}
              timestamp={item.timestamp}
              user={item.user}
              moduleSource={item.moduleSource}
              data={item.data}
            />
          ))
        )}
      </TimelineContent>
    </TimelineContainer>
  );
};

// Module Access Wrapper Component
interface ConditionalModuleTabProps {
  module: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ConditionalModuleTab: React.FC<ConditionalModuleTabProps> = ({
  module,
  children,
  fallback,
}) => {
  const { moduleAccess } = useModuleAccess();

  if (!moduleAccess[module]) {
    return (
      fallback || (
        <ModuleUpsell module={module}>
          <h3>Αναβάθμισε για Πρόσβαση</h3>
          <p>Αναβάθμισε το πλάνο σου για να δεις τα {module} στοιχεία.</p>
          <Button variant="primary">Αναβάθμιση</Button>
        </ModuleUpsell>
      )
    );
  }

  return <>{children}</>;
};

// Appointments Tab Component
interface CustomerAppointmentsTabProps {
  data: CustomerAppointments;
  customerId: string;
}

const CustomerAppointmentsTab: React.FC<CustomerAppointmentsTabProps> = ({
  data,
  customerId,
}) => {
  const [view, setView] = useState<"calendar" | "list" | "timeline">(
    "calendar"
  );
  const [filter, setFilter] = useState<"all" | "upcoming" | "past">("upcoming");

  return (
    <AppointmentsLayout>
      <AppointmentsHeader>
        <AppointmentMetrics data={data.appointmentSummary} />
        <AppointmentFilters
          view={view}
          onViewChange={setView}
          filter={filter}
          onFilterChange={setFilter}
        />
      </AppointmentsHeader>

      {view === "calendar" && (
        <AppointmentCalendar
          appointments={data.upcomingAppointments}
          onAppointmentClick={(apt) => openAppointmentDetails(apt)}
          onSlotClick={(slot) => scheduleNewAppointment(slot)}
        />
      )}

      {view === "list" && (
        <AppointmentList
          appointments={
            filter === "upcoming"
              ? data.upcomingAppointments
              : data.pastAppointments
          }
          showActions={filter === "upcoming"}
          onReschedule={(apt) => handleReschedule(apt)}
          onCancel={(apt) => handleCancel(apt)}
        />
      )}

      {view === "timeline" && (
        <AppointmentTimeline
          history={data.appointmentHistory}
          showOutcomes={true}
          onFollowUpCreate={(apt) => createFollowUp(apt)}
        />
      )}

      <QuickActions>
        <Button
          icon="calendar-plus"
          variant="primary"
          onClick={() => scheduleNewAppointment()}
        >
          Προγραμμάτισε Ραντεβού
        </Button>
        <Button icon="clock" onClick={() => checkAvailability()}>
          Έλεγχος Διαθεσιμότητας
        </Button>
        <Button icon="repeat" onClick={() => setupRecurringAppointment()}>
          Τακτικό Ραντεβού
        </Button>
        <Button icon="settings" onClick={() => configurePreferences()}>
          Προτιμήσεις
        </Button>
      </QuickActions>

      {data.recurringAppointments && data.recurringAppointments.length > 0 && (
        <RecurringAppointments appointments={data.recurringAppointments} />
      )}
    </AppointmentsLayout>
  );
};

// Appointment Scheduling Component
interface AppointmentSchedulerProps {
  customerId: string;
  prefilledData?: Partial<CreateAppointmentRequest>;
  onScheduled?: (appointment: Appointment) => void;
  onCancel?: () => void;
}

const AppointmentScheduler: React.FC<AppointmentSchedulerProps> = ({
  customerId,
  prefilledData,
  onScheduled,
  onCancel,
}) => {
  const { services } = useServices();
  const { staff } = useStaff();
  const { checkAvailability } = useAppointmentAvailability();
  const { scheduleAppointment } = useScheduleAppointment();

  const [step, setStep] = useState<
    "service" | "datetime" | "details" | "confirm"
  >("service");
  const [appointmentData, setAppointmentData] =
    useState<CreateAppointmentRequest>({
      customerId,
      type: "consultation",
      title: "",
      startTime: new Date(),
      duration: 60,
      ...prefilledData,
    });

  return (
    <SchedulerWizard>
      {step === "service" && (
        <ServiceSelection
          services={services}
          selectedService={appointmentData.serviceId}
          onServiceSelect={(serviceId) => {
            setAppointmentData((prev) => ({ ...prev, serviceId }));
            setStep("datetime");
          }}
        />
      )}

      {step === "datetime" && (
        <DateTimeSelection
          duration={appointmentData.duration}
          staffId={appointmentData.assignedStaffId}
          onSlotSelect={(startTime) => {
            setAppointmentData((prev) => ({ ...prev, startTime }));
            setStep("details");
          }}
          onBack={() => setStep("service")}
        />
      )}

      {step === "details" && (
        <AppointmentDetails
          appointmentData={appointmentData}
          onChange={setAppointmentData}
          onNext={() => setStep("confirm")}
          onBack={() => setStep("datetime")}
        />
      )}

      {step === "confirm" && (
        <AppointmentConfirmation
          appointmentData={appointmentData}
          onConfirm={async () => {
            const result = await scheduleAppointment(appointmentData);
            onScheduled?.(result.appointment);
          }}
          onBack={() => setStep("details")}
          onCancel={onCancel}
        />
      )}
    </SchedulerWizard>
  );
};

// Appointment Calendar Component
interface AppointmentCalendarProps {
  appointments: Appointment[];
  onAppointmentClick?: (appointment: Appointment) => void;
  onSlotClick?: (slot: { date: Date; time: string }) => void;
  view?: "month" | "week" | "day";
  staffFilter?: string[];
}

const AppointmentCalendar: React.FC<AppointmentCalendarProps> = ({
  appointments,
  onAppointmentClick,
  onSlotClick,
  view = "week",
  staffFilter,
}) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const { greekHolidays } = useGreekHolidays();

  const filteredAppointments = appointments.filter(
    (apt) =>
      !staffFilter ||
      !apt.assignedStaffId ||
      staffFilter.includes(apt.assignedStaffId)
  );

  return (
    <CalendarContainer>
      <CalendarHeader>
        <CalendarNavigation
          currentDate={currentDate}
          onDateChange={setCurrentDate}
          view={view}
        />
        <CalendarFilters
          staffFilter={staffFilter}
          onStaffFilterChange={(staff) => setStaffFilter(staff)}
        />
      </CalendarHeader>

      <CalendarGrid
        date={currentDate}
        view={view}
        appointments={filteredAppointments}
        holidays={greekHolidays}
        onAppointmentClick={onAppointmentClick}
        onSlotClick={onSlotClick}
        renderAppointment={(apt) => (
          <CalendarAppointment
            appointment={apt}
            showCustomer={true}
            showService={true}
            colorByType={true}
          />
        )}
      />
    </CalendarContainer>
  );
};

// Service-Based Appointment Components (for barber shops, etc.)
interface ServiceAppointmentManagerProps {
  businessType: "salon" | "professional" | "sales" | "support";
  locationId: string;
}

const ServiceAppointmentManager: React.FC<ServiceAppointmentManagerProps> = ({
  businessType,
  locationId,
}) => {
  const [view, setView] = useState<"schedule" | "walk_ins" | "services">(
    "schedule"
  );

  return (
    <ServiceManagerLayout>
      <ServiceManagerHeader>
        <ViewToggle view={view} onViewChange={setView} />
        <LiveMetrics locationId={locationId} />
      </ServiceManagerHeader>

      {view === "schedule" && (
        <DailyScheduleView
          locationId={locationId}
          businessType={businessType}
          showWalkIns={true}
          allowOverbooking={businessType === "salon"}
        />
      )}

      {view === "walk_ins" && businessType === "salon" && (
        <WalkInManager
          locationId={locationId}
          onCustomerAdd={(customer) => addToWaitingList(customer)}
          onServiceStart={(appointment) => startService(appointment)}
        />
      )}

      {view === "services" && (
        <ServiceConfiguration
          businessType={businessType}
          onServiceUpdate={(service) => updateServiceOffering(service)}
        />
      )}
    </ServiceManagerLayout>
  );
};

// Voice Command Components
interface VoiceCommandButtonProps {
  size?: "small" | "medium" | "large";
  variant?: "floating" | "inline" | "toolbar";
  onCommand?: (response: ProcessVoiceCommandResponse) => void;
  onError?: (error: VoiceCommandError) => void;
  disabled?: boolean;
  contextModule: string;
  contextScreen: string;
  contextData?: Record<string, any>;
}

const VoiceCommandButton: React.FC<VoiceCommandButtonProps> = ({
  size = "medium",
  variant = "floating",
  onCommand,
  onError,
  disabled = false,
  contextModule,
  contextScreen,
  contextData,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const { processVoiceCommand } = useVoiceCommands();
  const { startRecording, stopRecording, audioBlob } = useAudioRecording();

  const handleVoiceCommand = async () => {
    if (isRecording) {
      // Stop recording and process
      const audio = await stopRecording();
      setIsRecording(false);
      setIsProcessing(true);

      try {
        const response = await processVoiceCommand({
          audioData: await blobToBase64(audio),
          audioFormat: "webm",
          contextModule,
          contextScreen,
          contextData,
          userId: user.id,
          customerId: contextData?.customerId,
        });

        onCommand?.(response);
        executeClientAction(response.action);
      } catch (error) {
        onError?.(error);
      } finally {
        setIsProcessing(false);
      }
    } else {
      // Start recording
      setIsRecording(true);
      startRecording();
    }
  };

  return (
    <VoiceButton
      variant={variant}
      size={size}
      isRecording={isRecording}
      isProcessing={isProcessing}
      disabled={disabled}
      onClick={handleVoiceCommand}
      className={`voice-command-button voice-command-button--${variant}`}
    >
      {isProcessing ? (
        <ProcessingIcon spin />
      ) : isRecording ? (
        <StopIcon pulse />
      ) : (
        <MicrophoneIcon />
      )}

      {variant === "inline" && (
        <span>
          {isProcessing
            ? "Επεξεργασία..."
            : isRecording
            ? "Εγγραφή..."
            : "Φωνητική εντολή"}
        </span>
      )}
    </VoiceButton>
  );
};

// Voice Command History Component
interface VoiceCommandHistoryProps {
  userId: string;
  limit?: number;
  showAnalytics?: boolean;
}

const VoiceCommandHistory: React.FC<VoiceCommandHistoryProps> = ({
  userId,
  limit = 50,
  showAnalytics = true,
}) => {
  const { commands, stats, loading } = useVoiceCommandHistory(userId, {
    limit,
  });
  const [filter, setFilter] = useState<VoiceCommandStatus | "all">("all");

  const filteredCommands = commands.filter(
    (cmd) => filter === "all" || cmd.status === filter
  );

  return (
    <VoiceHistoryContainer>
      {showAnalytics && (
        <VoiceStats>
          <StatCard>
            <StatLabel>Συνολικές εντολές</StatLabel>
            <StatValue>{stats.totalCommands}</StatValue>
          </StatCard>
          <StatCard>
            <StatLabel>Ποσοστό επιτυχίας</StatLabel>
            <StatValue>{stats.successRate}%</StatValue>
          </StatCard>
          <StatCard>
            <StatLabel>Μέσος χρόνος</StatLabel>
            <StatValue>{stats.averageProcessingTime}ms</StatValue>
          </StatCard>
        </VoiceStats>
      )}

      <VoiceHistoryFilters>
        <FilterSelect value={filter} onChange={setFilter}>
          <option value="all">Όλες οι εντολές</option>
          <option value="completed">Επιτυχημένες</option>
          <option value="failed">Αποτυχημένες</option>
          <option value="processing">Σε επεξεργασία</option>
        </FilterSelect>
      </VoiceHistoryFilters>

      <VoiceCommandList>
        {filteredCommands.map((command) => (
          <VoiceCommandItem key={command.id}>
            <CommandTimestamp>
              {formatDistanceToNow(command.createdAt, { locale: el })}
            </CommandTimestamp>
            <CommandTranscript confidence={command.confidence}>
              "{command.transcriptProcessed}"
            </CommandTranscript>
            <CommandAction status={command.status}>
              {getActionLabel(command.intent.action)}
            </CommandAction>
            <CommandMetrics>
              <MetricBadge type="confidence">{command.confidence}%</MetricBadge>
              <MetricBadge type="time">{command.processingTime}ms</MetricBadge>
              <MetricBadge type="language">{command.language}</MetricBadge>
            </CommandMetrics>
          </VoiceCommandItem>
        ))}
      </VoiceCommandList>
    </VoiceHistoryContainer>
  );
};

// Voice Command Feedback Component
interface VoiceCommandFeedbackProps {
  command: VoiceCommand;
  onFeedbackSubmitted?: () => void;
}

const VoiceCommandFeedback: React.FC<VoiceCommandFeedbackProps> = ({
  command,
  onFeedbackSubmitted,
}) => {
  const [feedback, setFeedback] = useState<
    "correct" | "incorrect" | "partially_correct"
  >();
  const [correctedTranscript, setCorrectedTranscript] = useState(
    command.transcriptProcessed
  );
  const [notes, setNotes] = useState("");
  const { submitFeedback } = useVoiceCommandFeedback();

  const handleSubmit = async () => {
    if (!feedback) return;

    await submitFeedback({
      commandId: command.id,
      feedback,
      correctedTranscript:
        feedback !== "correct" ? correctedTranscript : undefined,
      notes,
    });

    onFeedbackSubmitted?.();
  };

  return (
    <FeedbackModal>
      <FeedbackHeader>
        <h3>Αξιολόγηση φωνητικής εντολής</h3>
        <p>Βοηθήστε μας να βελτιώσουμε την ακρίβεια του συστήματος</p>
      </FeedbackHeader>

      <FeedbackContent>
        <OriginalCommand>
          <label>Αρχική εγγραφή:</label>
          <span>"{command.transcriptRaw}"</span>
        </OriginalCommand>

        <ProcessedCommand>
          <label>Επεξεργασμένη εγγραφή:</label>
          <span>"{command.transcriptProcessed}"</span>
        </ProcessedCommand>

        <DetectedIntent>
          <label>Εντοπισμένη πρόθεση:</label>
          <span>{getActionLabel(command.intent.action)}</span>
        </DetectedIntent>

        <FeedbackOptions>
          <label>Η εντολή ήταν:</label>
          <RadioGroup value={feedback} onChange={setFeedback}>
            <Radio value="correct">Σωστή</Radio>
            <Radio value="partially_correct">Μερικώς σωστή</Radio>
            <Radio value="incorrect">Λανθασμένη</Radio>
          </RadioGroup>
        </FeedbackOptions>

        {feedback && feedback !== "correct" && (
          <CorrectionFields>
            <TextArea
              label="Σωστή εγγραφή:"
              value={correctedTranscript}
              onChange={setCorrectedTranscript}
              placeholder="Γράψτε την σωστή εγγραφή εδώ..."
            />
            <TextArea
              label="Σημειώσεις (προαιρετικό):"
              value={notes}
              onChange={setNotes}
              placeholder="Πρόσθετες πληροφορίες..."
            />
          </CorrectionFields>
        )}
      </FeedbackContent>

      <FeedbackActions>
        <Button variant="outline" onClick={onFeedbackSubmitted}>
          Ακύρωση
        </Button>
        <Button variant="primary" onClick={handleSubmit} disabled={!feedback}>
          Υποβολή αξιολόγησης
        </Button>
      </FeedbackActions>
    </FeedbackModal>
  );
};

// Global Voice Command Provider
interface VoiceCommandProviderProps {
  children: React.ReactNode;
  enabled?: boolean;
  whisperEndpoint?: string;
}

const VoiceCommandProvider: React.FC<VoiceCommandProviderProps> = ({
  children,
  enabled = true,
  whisperEndpoint = "/api/voice",
}) => {
  const [isGlobalListening, setIsGlobalListening] = useState(false);
  const { user } = useAuth();

  // Global keyboard shortcut for voice commands
  useEffect(() => {
    if (!enabled) return;

    const handleKeyPress = (event: KeyboardEvent) => {
      // Ctrl + Space or Cmd + Space to trigger voice command
      if ((event.ctrlKey || event.metaKey) && event.code === "Space") {
        event.preventDefault();
        triggerGlobalVoiceCommand();
      }
    };

    document.addEventListener("keydown", handleKeyPress);
    return () => document.removeEventListener("keydown", handleKeyPress);
  }, [enabled]);

  const triggerGlobalVoiceCommand = () => {
    // Implementation for global voice command trigger
    setIsGlobalListening(true);
  };

  const contextValue = {
    enabled,
    whisperEndpoint,
    isGlobalListening,
    triggerGlobalVoiceCommand,
    user,
  };

  return (
    <VoiceCommandContext.Provider value={contextValue}>
      {children}
      {isGlobalListening && (
        <GlobalVoiceCommandModal
          onClose={() => setIsGlobalListening(false)}
          onCommand={(response) => {
            executeClientAction(response.action);
            setIsGlobalListening(false);
          }}
        />
      )}
    </VoiceCommandContext.Provider>
  );
};
```

### Reusable Components

```typescript
// Greek Address Input
interface GreekAddressInputProps {
  value?: GreekAddress;
  onChange?: (address: GreekAddress) => void;
  required?: boolean;
}

const GreekAddressInput: React.FC<GreekAddressInputProps> = ({
  value,
  onChange,
}) => {
  const { autocomplete } = useGreekAddressAutocomplete();

  return (
    <AddressFieldGroup>
      <Input label="Οδός" name="street" autocomplete={autocomplete} />
      <Input label="Αριθμός" name="number" />
      <Input label="Περιοχή" name="area" />
      <Select label="Πόλη" name="city" options={greekCities} />
      <Input label="Τ.Κ." name="postalCode" pattern="[0-9]{5}" />
      <Select label="Περιφέρεια" name="region" options={greekRegions} />
    </AddressFieldGroup>
  );
};

// AFM Validation Input
interface AfmInputProps {
  value?: string;
  onChange?: (afm: string) => void;
  showValidation?: boolean;
}

const AfmInput: React.FC<AfmInputProps> = ({
  value,
  onChange,
  showValidation = true,
}) => {
  const { validateAfm, lookupAfm } = useGreekValidation();
  const [validation, setValidation] = useState<AfmValidation>();

  const handleAfmChange = async (newAfm: string) => {
    onChange?.(newAfm);
    if (showValidation && newAfm.length === 9) {
      const result = await validateAfm(newAfm);
      setValidation(result);
    }
  };

  return (
    <InputWithValidation
      label="Α.Φ.Μ."
      value={value}
      onChange={handleAfmChange}
      validation={validation}
      pattern="[0-9]{9}"
      maxLength={9}
    />
  );
};
```

---

## 🪝 Custom Hooks

### Data Hooks

```typescript
// Contact Management Hooks
const useContacts = (filters?: ContactFilters) => {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: ["contacts", filters],
    queryFn: () => contactApi.getContacts(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

const useContact = (id: string) => {
  return useQuery({
    queryKey: ["contact", id],
    queryFn: () => contactApi.getContact(id),
    enabled: !!id,
  });
};

const useCreateContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: contactApi.createContact,
    onSuccess: () => {
      queryClient.invalidateQueries(["contacts"]);
    },
  });
};

const useUpdateContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Contact> }) =>
      contactApi.updateContact(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries(["contact", variables.id]);
      queryClient.invalidateQueries(["contacts"]);
    },
  });
};

// Account Management Hooks
const useAccounts = (filters?: AccountFilters) => {
  return useQuery({
    queryKey: ["accounts", filters],
    queryFn: () => accountApi.getAccounts(filters),
  });
};

const useAccountContacts = (accountId: string) => {
  return useQuery({
    queryKey: ["account-contacts", accountId],
    queryFn: () => contactApi.getContacts({ filters: { accountId } }),
    enabled: !!accountId,
  });
};

// Lead Management Hooks
const useLeadConversion = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: leadApi.convertLead,
    onSuccess: () => {
      queryClient.invalidateQueries(["leads"]);
      queryClient.invalidateQueries(["contacts"]);
      queryClient.invalidateQueries(["accounts"]);
    },
  });
};
```

### Customer Hub Hooks

```typescript
// Main customer hub data hook
const useCustomerHub = (customerId: string) => {
  const { moduleAccess } = useModuleAccess();

  return useQuery({
    queryKey: ["customer-hub", customerId, moduleAccess],
    queryFn: () =>
      customerHubApi.getCustomerHub(customerId, {
        includeModules: Object.keys(moduleAccess).filter(
          (module) => moduleAccess[module]
        ),
      }),
    enabled: !!customerId,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

// Customer communications hook
const useCustomerCommunications = (
  customerId: string,
  filters?: CommunicationFilters
) => {
  return useQuery({
    queryKey: ["customer-communications", customerId, filters],
    queryFn: () => customerHubApi.getCommunications(customerId, filters),
    enabled: !!customerId,
  });
};

// Customer timeline hook
const useCustomerTimeline = (customerId: string, options?: TimelineOptions) => {
  return useQuery({
    queryKey: ["customer-timeline", customerId, options],
    queryFn: () => customerHubApi.getCustomerTimeline(customerId, options),
    enabled: !!customerId,
  });
};

// Module access check hook
const useModuleAccess = () => {
  const { user } = useAuth();

  return useQuery({
    queryKey: ["module-access", user?.id],
    queryFn: () => customerHubApi.getModuleAccess(),
    staleTime: 10 * 60 * 1000, // 10 minutes - doesn't change often
  });
};

// Communication logging hooks
const useLogEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: LogEmailRequest) => customerHubApi.logEmail(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries([
        "customer-communications",
        variables.customerId,
      ]);
      queryClient.invalidateQueries([
        "customer-timeline",
        variables.customerId,
      ]);
      queryClient.invalidateQueries(["customer-hub", variables.customerId]);
    },
  });
};

const useLogCall = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: LogCallRequest) => customerHubApi.logCall(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries([
        "customer-communications",
        variables.customerId,
      ]);
      queryClient.invalidateQueries([
        "customer-timeline",
        variables.customerId,
      ]);
      queryClient.invalidateQueries(["customer-hub", variables.customerId]);
    },
  });
};

const useScheduleFollowUp = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ScheduleFollowUpRequest) =>
      customerHubApi.scheduleFollowUp(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries(["customer-hub", variables.customerId]);
      queryClient.invalidateQueries([
        "customer-communications",
        variables.customerId,
      ]);
    },
  });
};

// Customer hub navigation hook
const useCustomerHubNavigation = (customerId: string) => {
  const [activeTab, setActiveTab] = useState("overview");
  const { moduleAccess } = useModuleAccess();
  const { hubData } = useCustomerHub(customerId);

  const availableTabs = useMemo(() => {
    return (
      hubData?.availableTabs.filter(
        (tab) => !tab.requiredModule || moduleAccess.data?.[tab.requiredModule]
      ) || []
    );
  }, [hubData?.availableTabs, moduleAccess.data]);

  const navigateToTab = (tabKey: string) => {
    if (availableTabs.some((tab) => tab.key === tabKey)) {
      setActiveTab(tabKey);
    }
  };

  const getTabBadgeCount = (tabKey: string) => {
    return availableTabs.find((tab) => tab.key === tabKey)?.badgeCount || 0;
  };

  return {
    activeTab,
    availableTabs,
    navigateToTab,
    getTabBadgeCount,
    canAccessTab: (tabKey: string) =>
      availableTabs.some((tab) => tab.key === tabKey),
  };
};

// Communication preferences hook
const useCommunicationPreferences = (customerId: string) => {
  const { data: preferences } = useQuery({
    queryKey: ["communication-preferences", customerId],
    queryFn: () => customerHubApi.getCommunicationPreferences(customerId),
    enabled: !!customerId,
  });

  const updatePreferences = useMutation({
    mutationFn: (data: CommunicationPreferences) =>
      customerHubApi.updateCommunicationPreferences(customerId, data),
  });

  return {
    preferences,
    updatePreferences: updatePreferences.mutate,
    isUpdating: updatePreferences.isLoading,
  };
};
```

### Appointment Management Hooks

```typescript
// Customer appointments hook
const useCustomerAppointments = (
  customerId: string,
  filters?: AppointmentFilters
) => {
  return useQuery({
    queryKey: ["customer-appointments", customerId, filters],
    queryFn: () => customerHubApi.getCustomerAppointments(customerId, filters),
    enabled: !!customerId,
  });
};

// Appointment scheduling hook
const useScheduleAppointment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: CreateAppointmentRequest) =>
      appointmentApi.createAppointment(request),
    onSuccess: (result, variables) => {
      // Invalidate related queries
      queryClient.invalidateQueries([
        "customer-appointments",
        variables.customerId,
      ]);
      queryClient.invalidateQueries(["customer-hub", variables.customerId]);
      queryClient.invalidateQueries([
        "customer-timeline",
        variables.customerId,
      ]);
      queryClient.invalidateQueries([
        "staff-schedule",
        variables.assignedStaffId,
      ]);
    },
  });
};

// Appointment availability checking hook
const useAppointmentAvailability = () => {
  const checkAvailability = useCallback(
    async (
      request: CheckAvailabilityRequest
    ): Promise<CheckAvailabilityResponse> => {
      return appointmentApi.checkAvailability(request);
    },
    []
  );

  const findAlternativeSlots = useCallback(
    async (request: CreateAppointmentRequest): Promise<AvailabilitySlot[]> => {
      const result = await appointmentApi.checkAvailability({
        startTime: request.startTime,
        duration: request.duration,
        staffId: request.assignedStaffId,
        serviceId: request.serviceId,
      });
      return result.alternativeSlots || [];
    },
    []
  );

  return { checkAvailability, findAlternativeSlots };
};

// Appointment management hook
const useAppointmentManagement = () => {
  const queryClient = useQueryClient();

  const updateAppointment = useMutation({
    mutationFn: (request: UpdateAppointmentRequest) =>
      appointmentApi.updateAppointment(request.appointmentId, request),
    onSuccess: (result, variables) => {
      queryClient.invalidateQueries(["appointment", variables.appointmentId]);
      queryClient.invalidateQueries(["customer-appointments"]);
      queryClient.invalidateQueries(["staff-schedule"]);
    },
  });

  const cancelAppointment = useMutation({
    mutationFn: ({
      appointmentId,
      reason,
    }: {
      appointmentId: string;
      reason: string;
    }) => appointmentApi.cancelAppointment(appointmentId, reason),
    onSuccess: () => {
      queryClient.invalidateQueries(["customer-appointments"]);
      queryClient.invalidateQueries(["staff-schedule"]);
    },
  });

  const completeAppointment = useMutation({
    mutationFn: (request: CompleteAppointmentRequest) =>
      appointmentApi.completeAppointment(request.appointmentId, request),
    onSuccess: (result, variables) => {
      queryClient.invalidateQueries(["appointment", variables.appointmentId]);
      queryClient.invalidateQueries(["customer-appointments"]);
      queryClient.invalidateQueries(["customer-timeline"]);
    },
  });

  const confirmAppointment = useMutation({
    mutationFn: (request: ConfirmAppointmentRequest) =>
      appointmentApi.confirmAppointment(request.appointmentId, request),
    onSuccess: (result, variables) => {
      queryClient.invalidateQueries(["appointment", variables.appointmentId]);
      queryClient.invalidateQueries(["customer-appointments"]);
    },
  });

  return {
    updateAppointment: updateAppointment.mutate,
    cancelAppointment: cancelAppointment.mutate,
    completeAppointment: completeAppointment.mutate,
    confirmAppointment: confirmAppointment.mutate,
    isUpdating: updateAppointment.isLoading,
    isCancelling: cancelAppointment.isLoading,
    isCompleting: completeAppointment.isLoading,
    isConfirming: confirmAppointment.isLoading,
  };
};

// Greek calendar integration hook
const useGreekHolidays = () => {
  const currentYear = new Date().getFullYear();

  const { data: holidays = [] } = useQuery({
    queryKey: ["greek-holidays", currentYear],
    queryFn: () => greekCalendarApi.getHolidays(currentYear),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
  });

  const isGreekHoliday = useCallback(
    (date: Date): boolean => {
      return holidays.some((holiday) => isSameDay(holiday.date, date));
    },
    [holidays]
  );

  const getNextWorkingDay = useCallback(
    (date: Date): Date => {
      let nextDay = addDays(date, 1);
      while (isGreekHoliday(nextDay) || isWeekend(nextDay)) {
        nextDay = addDays(nextDay, 1);
      }
      return nextDay;
    },
    [isGreekHoliday]
  );

  return {
    holidays,
    isGreekHoliday,
    getNextWorkingDay,
  };
};

// Recurring appointments hook
const useRecurringAppointments = (customerId: string) => {
  const queryClient = useQueryClient();

  const { data: recurringAppointments = [] } = useQuery({
    queryKey: ["recurring-appointments", customerId],
    queryFn: () => appointmentApi.getRecurringAppointments(customerId),
    enabled: !!customerId,
  });

  const createRecurringAppointment = useMutation({
    mutationFn: (request: CreateRecurringAppointmentRequest) =>
      appointmentApi.createRecurringAppointment(request),
    onSuccess: () => {
      queryClient.invalidateQueries(["recurring-appointments", customerId]);
      queryClient.invalidateQueries(["customer-appointments", customerId]);
    },
  });

  const updateRecurringAppointment = useMutation({
    mutationFn: (request: UpdateRecurringAppointmentRequest) =>
      appointmentApi.updateRecurringAppointment(request.id, request),
    onSuccess: () => {
      queryClient.invalidateQueries(["recurring-appointments", customerId]);
      queryClient.invalidateQueries(["customer-appointments", customerId]);
    },
  });

  const pauseRecurringAppointment = useMutation({
    mutationFn: (recurringId: string) =>
      appointmentApi.pauseRecurringAppointment(recurringId),
    onSuccess: () => {
      queryClient.invalidateQueries(["recurring-appointments", customerId]);
    },
  });

  return {
    recurringAppointments,
    createRecurring: createRecurringAppointment.mutate,
    updateRecurring: updateRecurringAppointment.mutate,
    pauseRecurring: pauseRecurringAppointment.mutate,
    isCreating: createRecurringAppointment.isLoading,
    isUpdating: updateRecurringAppointment.isLoading,
  };
};

// Service business hooks (for barber shops, salons)
const useServiceBusinessAppointments = (
  locationId: string,
  businessType: string
) => {
  const [currentDate, setCurrentDate] = useState(new Date());

  const { data: dailySchedule } = useQuery({
    queryKey: ["daily-schedule", locationId, format(currentDate, "yyyy-MM-dd")],
    queryFn: () => serviceApi.getDailySchedule(locationId, currentDate),
    refetchInterval: 30000, // Refetch every 30 seconds for live updates
  });

  const { data: walkIns = [] } = useQuery({
    queryKey: ["walk-ins", locationId, format(currentDate, "yyyy-MM-dd")],
    queryFn: () => serviceApi.getWalkIns(locationId, currentDate),
    enabled: businessType === "salon",
    refetchInterval: 10000, // Refetch every 10 seconds
  });

  const addWalkIn = useMutation({
    mutationFn: (walkIn: WalkInCustomer) =>
      serviceApi.addWalkIn(locationId, walkIn),
    onSuccess: () => {
      queryClient.invalidateQueries(["walk-ins", locationId]);
      queryClient.invalidateQueries(["daily-schedule", locationId]);
    },
  });

  const startService = useMutation({
    mutationFn: (appointmentId: string) =>
      serviceApi.startService(appointmentId),
    onSuccess: () => {
      queryClient.invalidateQueries(["daily-schedule", locationId]);
    },
  });

  return {
    dailySchedule,
    walkIns,
    currentDate,
    setCurrentDate,
    addWalkIn: addWalkIn.mutate,
    startService: startService.mutate,
    isAddingWalkIn: addWalkIn.isLoading,
    isStartingService: startService.isLoading,
  };
};
```

### Voice Command Hooks

```typescript
// Main voice command processing hook
const useVoiceCommands = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const processVoiceCommand = useMutation({
    mutationFn: (request: ProcessVoiceCommandRequest) =>
      voiceApi.processCommand(request),
    onSuccess: (response, variables) => {
      // Update voice command history
      queryClient.invalidateQueries(["voice-commands", variables.userId]);

      // Update customer timeline if command was in customer context
      if (variables.customerId) {
        queryClient.invalidateQueries([
          "customer-timeline",
          variables.customerId,
        ]);
        queryClient.invalidateQueries(["customer-hub", variables.customerId]);
      }
    },
  });

  const executeClientAction = useCallback((action: ClientAction) => {
    switch (action.type) {
      case "navigate":
        if (action.navigation) {
          router.push(action.navigation.route, action.navigation.params);
        }
        break;

      case "open_modal":
        if (action.modal) {
          modalService.open(action.modal.component, {
            ...action.modal.props,
            prefill: action.modal.prefill,
          });
        }
        break;

      case "fill_form":
        // Start Web Speech API for continued form filling
        if (action.payload?.formId) {
          webSpeechService.startContinuousRecognition(action.payload.formId);
        }
        break;

      case "show_notification":
        if (action.notification) {
          notificationService.show(action.notification);
        }
        break;

      case "start_web_speech":
        // Hand off to Web Speech API for form filling
        webSpeechService.startFormFilling(action.payload);
        break;

      case "execute_search":
        if (action.payload?.query) {
          searchService.executeSearch(
            action.payload.query,
            action.payload.filters
          );
        }
        break;

      case "apply_filter":
        if (action.payload?.filters) {
          filterService.applyFilters(action.payload.filters);
        }
        break;

      default:
        console.warn("Unknown client action type:", action.type);
    }
  }, []);

  return {
    processVoiceCommand: processVoiceCommand.mutate,
    executeClientAction,
    isProcessing: processVoiceCommand.isLoading,
    error: processVoiceCommand.error,
  };
};

// Audio recording hook
const useAudioRecording = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(
    null
  );
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });

      const recorder = new MediaRecorder(stream, {
        mimeType: "audio/webm;codecs=opus",
      });

      const chunks: BlobPart[] = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/webm" });
        setAudioBlob(blob);
        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start(1000); // Collect data every second
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (error) {
      console.error("Error starting recording:", error);
      throw new Error("Microphone access denied");
    }
  }, []);

  const stopRecording = useCallback((): Promise<Blob> => {
    return new Promise((resolve) => {
      if (mediaRecorder && isRecording) {
        mediaRecorder.onstop = () => {
          const blob = audioBlob;
          setIsRecording(false);
          setMediaRecorder(null);
          resolve(blob!);
        };
        mediaRecorder.stop();
      }
    });
  }, [mediaRecorder, isRecording, audioBlob]);

  return {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
  };
};

// Voice command history hook
const useVoiceCommandHistory = (
  userId: string,
  options?: { limit?: number }
) => {
  return useQuery({
    queryKey: ["voice-commands", userId, options],
    queryFn: () => voiceApi.getVoiceCommands(userId, options),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

// Voice command feedback hook
const useVoiceCommandFeedback = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (feedback: VoiceCommandFeedbackRequest) =>
      voiceApi.submitFeedback(feedback),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries(["voice-commands"]);
      queryClient.invalidateQueries(["voice-analytics"]);
    },
  });
};

// Voice analytics hook
const useVoiceAnalytics = (
  userId?: string,
  dateRange?: { from: Date; to: Date }
) => {
  return useQuery({
    queryKey: ["voice-analytics", userId, dateRange],
    queryFn: () => voiceApi.getVoiceAnalytics(userId, dateRange),
    enabled: !!dateRange,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Web Speech API integration hook (for form filling)
const useWebSpeechFormFilling = () => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(
    null
  );

  useEffect(() => {
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();

      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = "el-GR"; // Greek primary, but can detect English

      setRecognition(recognitionInstance);
    }
  }, []);

  const startFormFilling = useCallback(
    (formConfig: {
      formId: string;
      fields: { id: string; label: string; type: string }[];
    }) => {
      if (!recognition) return;

      setIsListening(true);
      recognition.start();

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map((result) => result[0].transcript)
          .join("");

        // Process transcript and fill form fields
        processFormTranscript(transcript, formConfig);
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };
    },
    [recognition]
  );

  const stopFormFilling = useCallback(() => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
    }
  }, [recognition, isListening]);

  const processFormTranscript = useCallback(
    (transcript: string, formConfig: any) => {
      // Greek form filling logic
      const greekPatterns = {
        name: /(?:το όνομά μου είναι|με λένε|ονομάζομαι)\s+(.+)/i,
        phone: /(?:τηλέφωνο|το νούμερό μου είναι)\s+([\d\s\-\+]+)/i,
        email: /(?:email|το email μου είναι)\s+([\w\.-]+@[\w\.-]+\.\w+)/i,
        address: /(?:διεύθυνση|μένω στη|κατοικώ στη)\s+(.+)/i,
        notes: /(?:σημείωση|σημείωσε|γράψε)\s+(.+)/i,
      };

      // Extract and fill form fields based on Greek patterns
      Object.entries(greekPatterns).forEach(([fieldType, pattern]) => {
        const match = transcript.match(pattern);
        if (match) {
          const fieldId = formConfig.fields.find(
            (f: any) => f.type === fieldType
          )?.id;
          if (fieldId) {
            fillFormField(fieldId, match[1].trim());
          }
        }
      });
    },
    []
  );

  const fillFormField = useCallback((fieldId: string, value: string) => {
    const field = document.getElementById(fieldId) as HTMLInputElement;
    if (field) {
      field.value = value;
      field.dispatchEvent(new Event("input", { bubbles: true }));
      field.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }, []);

  return {
    isListening,
    startFormFilling,
    stopFormFilling,
    isSupported: !!recognition,
  };
};

// Greek language processing hook
const useGreekLanguageProcessing = () => {
  const normalizeGreekText = useCallback((text: string): string => {
    // Remove diacritics for better matching
    const normalized = text
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();

    return normalized;
  }, []);

  const extractGreekEntities = useCallback((text: string): VoiceEntity[] => {
    const entities: VoiceEntity[] = [];

    // Greek name patterns
    const namePattern = /\b([Α-Ωα-ωάέήίόύώ]{2,})\s+([Α-Ωα-ωάέήίόύώ]{2,})\b/g;
    let match;
    while ((match = namePattern.exec(text)) !== null) {
      entities.push({
        type: "customer_name",
        value: match[0],
        normalizedValue: `${match[1]} ${match[2]}`,
        confidence: 0.8,
        startIndex: match.index,
        endIndex: match.index + match[0].length,
      });
    }

    // Greek phone numbers
    const phonePattern = /\b(?:2\d{9}|69\d{8})\b/g;
    while ((match = phonePattern.exec(text)) !== null) {
      entities.push({
        type: "phone_number",
        value: match[0],
        normalizedValue: match[0],
        confidence: 0.9,
        startIndex: match.index,
        endIndex: match.index + match[0].length,
      });
    }

    // Greek cities
    const greekCities = ["Αθήνα", "Θεσσαλονίκη", "Πάτρα", "Ηράκλειο", "Λάρισα"];
    greekCities.forEach((city) => {
      const cityIndex = text.indexOf(city);
      if (cityIndex !== -1) {
        entities.push({
          type: "greek_city",
          value: city,
          normalizedValue: city,
          confidence: 0.95,
          startIndex: cityIndex,
          endIndex: cityIndex + city.length,
        });
      }
    });

    return entities;
  }, []);

  const translateBusinessTerms = useCallback((text: string): string => {
    const translations = {
      πελάτης: "customer",
      πελάτες: "customers",
      ραντεβού: "appointment",
      συνάντηση: "meeting",
      τηλέφωνο: "phone",
      email: "email",
      σημείωση: "note",
      υπηρεσία: "service",
      προϊόν: "product",
      παραγγελία: "order",
      τιμολόγιο: "invoice",
    };

    let translatedText = text;
    Object.entries(translations).forEach(([greek, english]) => {
      const regex = new RegExp(`\\b${greek}\\b`, "gi");
      translatedText = translatedText.replace(regex, english);
    });

    return translatedText;
  }, []);

  return {
    normalizeGreekText,
    extractGreekEntities,
    translateBusinessTerms,
  };
};
```

### Greek Validation Hooks

```typescript
const useGreekValidation = () => {
  const validateAfm = async (afm: string): Promise<AfmValidation> => {
    if (!afm || afm.length !== 9) {
      return { valid: false, error: "Το Α.Φ.Μ. πρέπει να έχει 9 ψηφία" };
    }

    // Greek AFM checksum validation
    const digits = afm.split("").map(Number);
    const checksum =
      digits
        .slice(0, 8)
        .reduce(
          (sum, digit, index) => sum + digit * Math.pow(2, 8 - index),
          0
        ) % 11;

    const lastDigit = checksum < 10 ? checksum : 0;

    if (digits[8] !== lastDigit) {
      return { valid: false, error: "Μη έγκυρο Α.Φ.Μ." };
    }

    return { valid: true };
  };

  const validateAmka = (amka: string): AmkaValidation => {
    if (!amka || amka.length !== 11) {
      return { valid: false, error: "Το ΑΜΚΑ πρέπει να έχει 11 ψηφία" };
    }

    // AMKA validation algorithm
    const digits = amka.split("").map(Number);
    const checksum =
      digits
        .slice(0, 10)
        .reduce(
          (sum, digit, index) => sum + digit * (index % 2 === 0 ? 1 : 2),
          0
        ) % 10;

    return digits[10] === checksum
      ? { valid: true }
      : { valid: false, error: "Μη έγκυρο ΑΜΚΑ" };
  };

  return { validateAfm, validateAmka };
};

const useGreekAddressAutocomplete = () => {
  const [suggestions, setSuggestions] = useState<AddressSuggestion[]>([]);

  const autocomplete = async (query: string): Promise<AddressSuggestion[]> => {
    if (query.length < 3) return [];

    try {
      const results = await greekApi.autocompleteAddress(query);
      setSuggestions(results);
      return results;
    } catch (error) {
      console.error("Address autocomplete error:", error);
      return [];
    }
  };

  return { autocomplete, suggestions };
};
```

---

## 🏗️ Context & State Management

### Customer Context

```typescript
interface CustomerContextValue {
  // Current selections
  selectedContacts: Contact[];
  selectedAccounts: Account[];
  selectedLeads: Lead[];

  // Actions
  selectContact: (contact: Contact) => void;
  selectAccount: (account: Account) => void;
  selectLead: (lead: Lead) => void;
  clearSelections: () => void;

  // Bulk operations
  bulkEdit: (
    entity: "contact" | "account" | "lead",
    ids: string[],
    changes: any
  ) => Promise<void>;
  bulkDelete: (
    entity: "contact" | "account" | "lead",
    ids: string[]
  ) => Promise<void>;
  bulkAssign: (
    entity: "contact" | "account" | "lead",
    ids: string[],
    userId: string
  ) => Promise<void>;

  // Greek-specific operations
  validateGreekData: (data: any) => Promise<ValidationResult>;
  lookupGreekBusiness: (afm: string) => Promise<GreekBusinessData>;
}

const CustomerContext = createContext<CustomerContextValue | null>(null);

export const CustomerProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [selectedContacts, setSelectedContacts] = useState<Contact[]>([]);
  const [selectedAccounts, setSelectedAccounts] = useState<Account[]>([]);
  const [selectedLeads, setSelectedLeads] = useState<Lead[]>([]);

  const selectContact = (contact: Contact) => {
    setSelectedContacts((prev) =>
      prev.find((c) => c.id === contact.id)
        ? prev.filter((c) => c.id !== contact.id)
        : [...prev, contact]
    );
  };

  const bulkEdit = async (entity: string, ids: string[], changes: any) => {
    // Implementation for bulk editing
    const api =
      entity === "contact"
        ? contactApi
        : entity === "account"
        ? accountApi
        : leadApi;

    await Promise.all(ids.map((id) => api.update(id, changes)));

    // Refresh relevant queries
    queryClient.invalidateQueries([entity + "s"]);
  };

  const validateGreekData = async (data: any): Promise<ValidationResult> => {
    const errors: ValidationError[] = [];

    if (data.afm) {
      const afmValidation = await validateAfm(data.afm);
      if (!afmValidation.valid) {
        errors.push({ field: "afm", message: afmValidation.error });
      }
    }

    if (data.amka) {
      const amkaValidation = validateAmka(data.amka);
      if (!amkaValidation.valid) {
        errors.push({ field: "amka", message: amkaValidation.error });
      }
    }

    return { valid: errors.length === 0, errors };
  };

  const value: CustomerContextValue = {
    selectedContacts,
    selectedAccounts,
    selectedLeads,
    selectContact,
    selectAccount,
    selectLead,
    clearSelections: () => {
      setSelectedContacts([]);
      setSelectedAccounts([]);
      setSelectedLeads([]);
    },
    bulkEdit,
    bulkDelete,
    bulkAssign,
    validateGreekData,
    lookupGreekBusiness,
  };

  return (
    <CustomerContext.Provider value={value}>
      {children}
    </CustomerContext.Provider>
  );
};

export const useCustomer = () => {
  const context = useContext(CustomerContext);
  if (!context) {
    throw new Error("useCustomer must be used within CustomerProvider");
  }
  return context;
};
```

---

## 🧪 Testing Specifications

### Unit Tests

```typescript
// Contact Form Tests
describe("ContactForm", () => {
  it("validates Greek AFM correctly", async () => {
    const { getByLabelText, getByText } = render(<ContactForm mode="create" />);

    const afmInput = getByLabelText("Α.Φ.Μ.");
    fireEvent.change(afmInput, { target: { value: "9" } });

    await waitFor(() => {
      expect(getByText("Μη έγκυρο Α.Φ.Μ.")).toBeInTheDocument();
    });
  });

  it("handles Greek address autocomplete", async () => {
    const mockAutocomplete = jest
      .fn()
      .mockResolvedValue([
        { street: "Πανεπιστημίου", number: "10", city: "Αθήνα" },
      ]);

    jest.mock("../hooks/useGreekAddressAutocomplete", () => ({
      useGreekAddressAutocomplete: () => ({ autocomplete: mockAutocomplete }),
    }));

    const { getByLabelText } = render(<ContactForm mode="create" />);

    const streetInput = getByLabelText("Οδός");
    fireEvent.change(streetInput, { target: { value: "Πανεπ" } });

    await waitFor(() => {
      expect(mockAutocomplete).toHaveBeenCalledWith("Πανεπ");
    });
  });

  it("prevents duplicate contact creation", async () => {
    const mockCreateContact = jest.fn().mockResolvedValue({
      contact: mockContact,
      duplicates: [existingContact],
    });

    // Test duplicate detection logic
  });
});

// Greek Validation Tests
describe("useGreekValidation", () => {
  it("validates correct AFM", async () => {
    const { validateAfm } = useGreekValidation();
    const result = await validateAfm("0"); // Valid AFM

    expect(result.valid).toBe(true);
    expect(result.error).toBeUndefined();
  });

  it("rejects invalid AFM", async () => {
    const { validateAfm } = useGreekValidation();
    const result = await validateAfm("9"); // Invalid AFM

    expect(result.valid).toBe(false);
    expect(result.error).toBe("Μη έγκυρο Α.Φ.Μ.");
  });

  it("validates AMKA correctly", () => {
    const { validateAmka } = useGreekValidation();
    const result = validateAmka("901"); // Valid AMKA

    expect(result.valid).toBe(true);
  });
});

// API Tests
describe("Contact API", () => {
  it("creates contact with Greek data", async () => {
    const contactData = {
      firstName: "Γιάννης",
      lastName: "Παπαδόπουλος",
      afm: "0",
      address: {
        street: "Πανεπιστημίου",
        number: "10",
        city: "Αθήνα",
        postalCode: "10679",
        region: "Αττική",
        country: "Ελλάδα",
      },
    };

    const response = await contactApi.createContact({ contact: contactData });

    expect(response.contact.id).toBeDefined();
    expect(response.contact.afm).toBe("0");
    expect(response.duplicates).toEqual([]);
  });

  it("handles AFM validation error", async () => {
    const contactData = {
      firstName: "Test",
      lastName: "User",
      afm: "invalid-afm",
    };

    await expect(
      contactApi.createContact({ contact: contactData })
    ).rejects.toThrow("Invalid AFM format");
  });
});
```

### Integration Tests

```typescript
// End-to-End Contact Management Flow
describe("Contact Management E2E", () => {
  it("completes full contact lifecycle", async () => {
    // 1. Create new contact
    await page.goto("/contacts/new");
    await page.fill('[data-testid="firstName"]', "Μαρία");
    await page.fill('[data-testid="lastName"]', "Γεωργίου");
    await page.fill('[data-testid="email"]', "maria@example.gr");
    await page.fill('[data-testid="afm"]', "0");

    // 2. Fill Greek address
    await page.fill('[data-testid="street"]', "Ερμού");
    await page.fill('[data-testid="number"]', "15");
    await page.selectOption('[data-testid="city"]', "Θεσσαλονίκη");
    await page.fill('[data-testid="postalCode"]', "54624");

    // 3. Save contact
    await page.click('[data-testid="save-contact"]');

    // 4. Verify creation
    await expect(page.locator(".success-message")).toContainText(
      "Επιτυχής δημιουργία επαφής"
    );

    // 5. Navigate to contact list
    await page.goto("/contacts");

    // 6. Search for created contact
    await page.fill('[data-testid="search"]', "Μαρία Γεωργίου");

    // 7. Verify contact appears in list
    await expect(page.locator('[data-testid="contact-row"]')).toContainText(
      "Μαρία Γεωργίου"
    );
  });

  it("handles lead conversion workflow", async () => {
    // Create lead → Qualify → Convert to Contact + Account + Opportunity
    const leadId = await createTestLead();

    await page.goto(`/leads/${leadId}`);
    await page.click('[data-testid="convert-lead"]');

    // Conversion wizard
    await page.check('[data-testid="create-contact"]');
    await page.check('[data-testid="create-account"]');
    await page.check('[data-testid="create-opportunity"]');

    await page.click('[data-testid="next-step"]');

    // Data mapping
    await page.fill('[data-testid="company-name"]', "Νέα Εταιρεία ΑΕ");
    await page.fill('[data-testid="opportunity-value"]', "50000");

    await page.click('[data-testid="convert"]');

    // Verify conversion
    await expect(page.locator(".conversion-success")).toBeVisible();

    // Check created records
    const contactLink = page.locator('[data-testid="created-contact-link"]');
    const accountLink = page.locator('[data-testid="created-account-link"]');

    await expect(contactLink).toBeVisible();
    await expect(accountLink).toBeVisible();
  });
});

// Performance Tests
describe("Contact Performance", () => {
  it("loads contact list under 2 seconds", async () => {
    const startTime = Date.now();

    await page.goto("/contacts");
    await page.waitForSelector('[data-testid="contact-list"]');

    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(2000);
  });

  it("handles 1000+ contacts efficiently", async () => {
    // Seed database with 1000 contacts
    await seedLargeContactDataset();

    await page.goto("/contacts");

    // Test scrolling performance
    const startTime = Date.now();

    for (let i = 0; i < 10; i++) {
      await page.evaluate(() => window.scrollBy(0, 500));
      await page.waitForTimeout(100);
    }

    const scrollTime = Date.now() - startTime;
    expect(scrollTime).toBeLessThan(3000);
  });
});
```

### Greek Compliance Tests

```typescript
describe("Greek Market Compliance", () => {
  it("validates all Greek business fields", async () => {
    const greekBusinessData = {
      afm: "0",
      doy: "Α' ΑΘΗΝΩΝ",
      vatNumber: "EL0",
      gemiNumber: "9",
      address: {
        street: "Πανεπιστημίου",
        number: "10",
        city: "Αθήνα",
        postalCode: "10679",
        region: "Αττική",
        country: "Ελλάδα",
      },
    };

    const validation = await validateGreekBusinessData(greekBusinessData);
    expect(validation.valid).toBe(true);
    expect(validation.errors).toEqual([]);
  });

  it("validates Greek postal codes", async () => {
    const validPostalCodes = ["10679", "54624", "85100"];
    const invalidPostalCodes = ["1234", "123456", "00000"];

    for (const code of validPostalCodes) {
      const result = validateGreekPostalCode(code);
      expect(result.valid).toBe(true);
    }

    for (const code of invalidPostalCodes) {
      const result = validateGreekPostalCode(code);
      expect(result.valid).toBe(false);
    }
  });
});
```

---

## 📋 Implementation Checklist

### Phase 1: Foundation (Week 1-2)

- [ ] **Data Models**: Contact, Account, Lead models with Greek fields
- [ ] **Database Schema**: PostgreSQL tables with proper indexes
- [ ] **Basic APIs**: CRUD operations for all entities
- [ ] **Greek Validation**: AFM, AMKA validation logic
- [ ] **Address System**: Greek address format and autocomplete

### Phase 2: Core UI (Week 3-4)

- [ ] **List Views**: Contact, Account, Lead list screens
- [ ] **Detail Views**: Complete detail screens with tabs
- [ ] **Form Components**: Create/edit forms with validation
- [ ] **Greek Components**: AFM input, address input, Greek fields
- [ ] **Search & Filters**: Advanced filtering and search

### Phase 3: Advanced Features (Week 5-6)

- [ ] **Lead Conversion**: Complete conversion workflow
- [ ] **Bulk Operations**: Multi-select and bulk actions
- [ ] **Duplicate Detection**: Prevent and merge duplicates
- [ ] **Import/Export**: CSV import and export functionality
- [ ] **Activity Integration**: Link with activity management

### Phase 4: Testing & Polish (Week 7-8)

- [ ] **Unit Tests**: 90%+ coverage for all components
- [ ] **Integration Tests**: API and workflow testing
- [ ] **E2E Tests**: Complete user journey testing
- [ ] **Performance Tests**: Load testing with large datasets
- [ ] **Greek Data Tests**: AFM/AMKA validation and formatting

---

**Status**: Specification Complete  
**Next**: Begin Phase 1 Implementation  
**Dependencies**: Core Infrastructure, Authentication  
**Team**: Frontend, Backend, QA Engineers
