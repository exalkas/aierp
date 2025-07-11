# 04. Communication Management

## Overview

Comprehensive communication system integrating email, SMS, calls, and meetings with Greek business communication standards and GDPR compliance.

## Core Features

### 4.1 Email Management System

- **Multi-account Integration**: Gmail, Outlook, Greek providers (Forthnet, OTE)
- **Template Engine**: Greek business templates, dynamic field insertion
- **Email Campaigns**: Bulk sending with Greek opt-in compliance
- **Tracking**: Open rates, click tracking, bounce management
- **Threading**: Conversation grouping and history
- **Greek Signatures**: Professional Greek business email signatures

### 4.2 SMS Management

- **Greek Carriers**: Integration with Cosmote, Vodafone, Wind Hellas
- **Bulk SMS**: Campaign management with Greek telecom regulations
- **Templates**: Greek SMS templates with character optimization
- **Delivery Reports**: Real-time status tracking
- **Two-way SMS**: Conversation management
- **Opt-out Compliance**: GDPR and Greek telecom law compliance

### 4.3 Call Management

- **VoIP Integration**: Greek providers (OTE, Forthnet, Cyta)
- **Call Logging**: Automatic activity creation
- **Recording**: GDPR-compliant call recording
- **Greek Numbers**: Support for 10-digit Greek phone format
- **Call Queues**: Business hours routing
- **Analytics**: Call metrics and performance

### 4.4 Meeting Management

- **Video Conferencing**: Zoom, Teams, WebEx integration
- **Greek Calendar**: Orthodox holidays integration
- **Room Booking**: Physical meeting room management
- **Attendee Management**: Internal and external participants
- **Meeting Minutes**: Automatic transcription and summary
- **Follow-up Tasks**: Action item tracking

## Data Models

### Email Model

```typescript
interface Email {
  id: string;
  type: "incoming" | "outgoing" | "draft";
  subject: string;
  body: string;
  htmlBody?: string;
  from: EmailAddress;
  to: EmailAddress[];
  cc?: EmailAddress[];
  bcc?: EmailAddress[];
  attachments: Attachment[];
  threadId?: string;
  parentId?: string;
  status: "draft" | "sent" | "delivered" | "read" | "failed";
  priority: "low" | "normal" | "high" | "urgent";
  isGreekBusiness: boolean;
  greekSignature?: GreekSignature;
  customFields: Record<string, any>;
  relatedTo?: {
    type: "contact" | "account" | "lead" | "opportunity";
    id: string;
  };
  sentAt?: Date;
  deliveredAt?: Date;
  readAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  tags: string[];
  isTemplate: boolean;
  templateCategory?: string;
}

interface EmailAddress {
  email: string;
  name?: string;
  isGreekBusiness?: boolean;
}

interface GreekSignature {
  companyName: string;
  afm?: string;
  doy?: string;
  address: GreekAddress;
  phones: string[];
  website?: string;
  logoUrl?: string;
}
```

### SMS Model

```typescript
interface SMS {
  id: string;
  type: "incoming" | "outgoing";
  message: string;
  from: string;
  to: string[];
  status: "pending" | "sent" | "delivered" | "failed" | "read";
  provider: "cosmote" | "vodafone" | "wind" | "other";
  cost?: number;
  currency: "EUR";
  isGreekNumber: boolean;
  campaignId?: string;
  customFields: Record<string, any>;
  relatedTo?: {
    type: "contact" | "account" | "lead";
    id: string;
  };
  sentAt?: Date;
  deliveredAt?: Date;
  readAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}
```

### Call Model

```typescript
interface Call {
  id: string;
  type: "incoming" | "outgoing" | "missed";
  from: string;
  to: string;
  duration?: number; // in seconds
  status:
    | "scheduled"
    | "ringing"
    | "active"
    | "completed"
    | "missed"
    | "failed";
  recordingUrl?: string;
  notes?: string;
  isGreekNumber: boolean;
  provider?: string;
  cost?: number;
  currency: "EUR";
  customFields: Record<string, any>;
  relatedTo?: {
    type: "contact" | "account" | "lead";
    id: string;
  };
  startedAt?: Date;
  endedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}
```

### Meeting Model

```typescript
interface Meeting {
  id: string;
  title: string;
  description?: string;
  type: "physical" | "video" | "phone";
  status: "scheduled" | "in-progress" | "completed" | "cancelled";
  startTime: Date;
  endTime: Date;
  timezone: string;
  location?: string;
  roomId?: string;
  meetingUrl?: string;
  provider?: "zoom" | "teams" | "webex" | "other";
  attendees: MeetingAttendee[];
  organizer: string;
  agenda?: string;
  minutes?: string;
  recording?: {
    url: string;
    duration: number;
  };
  isGreekBusinessHours: boolean;
  customFields: Record<string, any>;
  relatedTo?: {
    type: "contact" | "account" | "lead" | "opportunity";
    id: string;
  };
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  tags: string[];
}

interface MeetingAttendee {
  id: string;
  email: string;
  name?: string;
  type: "required" | "optional";
  status: "pending" | "accepted" | "declined" | "tentative";
  isExternal: boolean;
}
```

## API Endpoints

### Email APIs

```typescript
// Email Management
GET /api/emails
POST /api/emails
GET /api/emails/:id
PUT /api/emails/:id
DELETE /api/emails/:id
POST /api/emails/:id/send
POST /api/emails/:id/reply
POST /api/emails/:id/forward

// Email Threads
GET /api/emails/threads/:threadId
POST /api/emails/threads/:threadId/reply

// Email Templates
GET /api/email-templates
POST /api/email-templates
GET /api/email-templates/:id
PUT /api/email-templates/:id
DELETE /api/email-templates/:id

// Email Campaigns
GET /api/email-campaigns
POST /api/email-campaigns
GET /api/email-campaigns/:id
PUT /api/email-campaigns/:id
POST /api/email-campaigns/:id/send
GET /api/email-campaigns/:id/stats

// Greek Email Services
POST /api/emails/validate-greek-business
GET /api/emails/greek-templates
POST /api/emails/greek-signature/generate
```

### SMS APIs

```typescript
// SMS Management
GET /api/sms
POST /api/sms
GET /api/sms/:id
PUT /api/sms/:id
DELETE /api/sms/:id
POST /api/sms/:id/send

// SMS Campaigns
GET /api/sms-campaigns
POST /api/sms-campaigns
GET /api/sms-campaigns/:id
PUT /api/sms-campaigns/:id
POST /api/sms-campaigns/:id/send
GET /api/sms-campaigns/:id/stats

// Greek SMS Services
POST /api/sms/validate-greek-number
GET /api/sms/greek-providers
GET /api/sms/greek-pricing
POST /api/sms/bulk-greek
```

### Call APIs

```typescript
// Call Management
GET /api/calls
POST /api/calls
GET /api/calls/:id
PUT /api/calls/:id
DELETE /api/calls/:id
POST /api/calls/:id/start
POST /api/calls/:id/end
POST /api/calls/:id/record

// Call Analytics
GET /api/calls/stats
GET /api/calls/reports
GET /api/calls/recordings

// Greek Call Services
POST /api/calls/validate-greek-number
GET /api/calls/greek-providers
GET /api/calls/greek-rates
```

### Meeting APIs

```typescript
// Meeting Management
GET /api/meetings
POST /api/meetings
GET /api/meetings/:id
PUT /api/meetings/:id
DELETE /api/meetings/:id
POST /api/meetings/:id/start
POST /api/meetings/:id/end

// Meeting Attendees
GET /api/meetings/:id/attendees
POST /api/meetings/:id/attendees
PUT /api/meetings/:id/attendees/:attendeeId
DELETE /api/meetings/:id/attendees/:attendeeId

// Meeting Rooms
GET /api/meeting-rooms
GET /api/meeting-rooms/availability
POST /api/meeting-rooms/:id/book

// Greek Meeting Services
GET /api/meetings/greek-business-hours
GET /api/meetings/greek-holidays
POST /api/meetings/greek-schedule-check
```

## UI Components

### EmailManager Component

```typescript
interface EmailManagerProps {
  view: "inbox" | "sent" | "drafts" | "templates";
  filters?: EmailFilters;
  onEmailSelect?: (email: Email) => void;
  showGreekFeatures?: boolean;
}

const EmailManager: React.FC<EmailManagerProps> = ({
  view,
  filters,
  onEmailSelect,
  showGreekFeatures = true,
}) => {
  // Component implementation
};
```

### EmailComposer Component

```typescript
interface EmailComposerProps {
  to?: EmailAddress[];
  cc?: EmailAddress[];
  bcc?: EmailAddress[];
  subject?: string;
  body?: string;
  parentEmail?: Email;
  template?: EmailTemplate;
  useGreekTemplate?: boolean;
  onSend?: (email: Email) => void;
  onSave?: (email: Email) => void;
}

const EmailComposer: React.FC<EmailComposerProps> = ({
  to,
  cc,
  bcc,
  subject,
  body,
  parentEmail,
  template,
  useGreekTemplate,
  onSend,
  onSave,
}) => {
  // Component implementation
};
```

### SMSManager Component

```typescript
interface SMSManagerProps {
  view: "inbox" | "sent" | "campaigns";
  filters?: SMSFilters;
  onSMSSelect?: (sms: SMS) => void;
  showGreekProviders?: boolean;
}

const SMSManager: React.FC<SMSManagerProps> = ({
  view,
  filters,
  onSMSSelect,
  showGreekProviders = true,
}) => {
  // Component implementation
};
```

### CallManager Component

```typescript
interface CallManagerProps {
  view: "recent" | "missed" | "recordings";
  filters?: CallFilters;
  onCallSelect?: (call: Call) => void;
  showGreekFeatures?: boolean;
}

const CallManager: React.FC<CallManagerProps> = ({
  view,
  filters,
  onCallSelect,
  showGreekFeatures = true,
}) => {
  // Component implementation
};
```

### MeetingScheduler Component

```typescript
interface MeetingSchedulerProps {
  initialDate?: Date;
  attendees?: MeetingAttendee[];
  relatedTo?: {
    type: string;
    id: string;
  };
  useGreekCalendar?: boolean;
  onSchedule?: (meeting: Meeting) => void;
}

const MeetingScheduler: React.FC<MeetingSchedulerProps> = ({
  initialDate,
  attendees,
  relatedTo,
  useGreekCalendar = true,
  onSchedule,
}) => {
  // Component implementation
};
```

## Custom Hooks

### useEmails Hook

```typescript
interface UseEmailsOptions {
  view: "inbox" | "sent" | "drafts";
  filters?: EmailFilters;
  realtime?: boolean;
}

const useEmails = (options: UseEmailsOptions) => {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendEmail = async (email: Partial<Email>) => {
    // Implementation
  };

  const markAsRead = async (emailId: string) => {
    // Implementation
  };

  const deleteEmail = async (emailId: string) => {
    // Implementation
  };

  return {
    emails,
    loading,
    error,
    sendEmail,
    markAsRead,
    deleteEmail,
    refetch: () => {
      /* Implementation */
    },
  };
};
```

### useSMS Hook

```typescript
interface UseSMSOptions {
  view: "inbox" | "sent";
  filters?: SMSFilters;
  realtime?: boolean;
}

const useSMS = (options: UseSMSOptions) => {
  const [smsMessages, setSmsMessages] = useState<SMS[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendSMS = async (sms: Partial<SMS>) => {
    // Implementation
  };

  const sendBulkSMS = async (message: string, recipients: string[]) => {
    // Implementation
  };

  return {
    smsMessages,
    loading,
    error,
    sendSMS,
    sendBulkSMS,
    refetch: () => {
      /* Implementation */
    },
  };
};
```

### useCalls Hook

```typescript
interface UseCallsOptions {
  view: "recent" | "missed";
  filters?: CallFilters;
  realtime?: boolean;
}

const useCalls = (options: UseCallsOptions) => {
  const [calls, setCalls] = useState<Call[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startCall = async (to: string, type: "audio" | "video") => {
    // Implementation
  };

  const endCall = async (callId: string) => {
    // Implementation
  };

  const logCall = async (call: Partial<Call>) => {
    // Implementation
  };

  return {
    calls,
    loading,
    error,
    startCall,
    endCall,
    logCall,
    refetch: () => {
      /* Implementation */
    },
  };
};
```

### useMeetings Hook

```typescript
interface UseMeetingsOptions {
  view: "upcoming" | "past" | "today";
  filters?: MeetingFilters;
  useGreekCalendar?: boolean;
}

const useMeetings = (options: UseMeetingsOptions) => {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const scheduleMeeting = async (meeting: Partial<Meeting>) => {
    // Implementation
  };

  const cancelMeeting = async (meetingId: string) => {
    // Implementation
  };

  const joinMeeting = async (meetingId: string) => {
    // Implementation
  };

  return {
    meetings,
    loading,
    error,
    scheduleMeeting,
    cancelMeeting,
    joinMeeting,
    refetch: () => {
      /* Implementation */
    },
  };
};
```

### useGreekCommunication Hook

```typescript
const useGreekCommunication = () => {
  const validateGreekPhone = (phone: string): boolean => {
    // Greek phone validation (10 digits, starting with 2 or 6)
    const greekPhoneRegex = /^[26]\d{9}$/;
    return greekPhoneRegex.test(phone.replace(/\D/g, ""));
  };

  const formatGreekPhone = (phone: string): string => {
    // Format as +30 XXX XXX XXXX
    const cleaned = phone.replace(/\D/g, "");
    if (cleaned.length === 10) {
      return `+30 ${cleaned.slice(0, 3)} ${cleaned.slice(3, 6)} ${cleaned.slice(
        6
      )}`;
    }
    return phone;
  };

  const isGreekBusinessHours = (date: Date): boolean => {
    const hour = date.getHours();
    const day = date.getDay();

    // Monday-Friday 9-17, excluding lunch 13-14
    return (
      day >= 1 &&
      day <= 5 &&
      ((hour >= 9 && hour < 13) || (hour >= 14 && hour < 17))
    );
  };

  const getGreekHolidays = (year: number): Date[] => {
    // Orthodox holidays calculation
    // Implementation for Greek public holidays
    return [];
  };

  return {
    validateGreekPhone,
    formatGreekPhone,
    isGreekBusinessHours,
    getGreekHolidays,
  };
};
```

## Context Providers

### CommunicationProvider

```typescript
interface CommunicationContextType {
  // Email state
  emails: Email[];
  emailStats: EmailStats;

  // SMS state
  smsMessages: SMS[];
  smsStats: SMSStats;

  // Call state
  calls: Call[];
  activeCall: Call | null;
  callStats: CallStats;

  // Meeting state
  meetings: Meeting[];
  upcomingMeetings: Meeting[];

  // Greek features
  greekProviders: GreekProvider[];
  greekSettings: GreekCommunicationSettings;

  // Actions
  sendEmail: (email: Partial<Email>) => Promise<void>;
  sendSMS: (sms: Partial<SMS>) => Promise<void>;
  startCall: (to: string) => Promise<void>;
  scheduleMeeting: (meeting: Partial<Meeting>) => Promise<void>;

  // Settings
  updateGreekSettings: (
    settings: Partial<GreekCommunicationSettings>
  ) => Promise<void>;
}

const CommunicationProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  // Implementation
};
```

## Greek Integration Features

### Greek Email Templates

- Professional business email templates in Greek
- AFM/DOY inclusion in signatures
- Greek address formatting
- VAT notification templates
- Payment reminder templates in Greek business style

### Greek SMS Compliance

- Integration with Greek telecom providers
- GDPR-compliant opt-in/opt-out
- Greek character set optimization
- Business hours respect for SMS campaigns
- Greek holiday awareness

### Greek Business Communication

- Orthodox calendar integration
- Greek business hours (9-17, lunch 13-14)
- Public holiday scheduling prevention
- Greek phone number formatting
- Professional Greek communication templates

### GDPR Compliance

- Explicit consent tracking
- Right to be forgotten implementation
- Data portability features
- Communication preference management
- Audit trail for all communications

## Testing Specifications

### Unit Tests

```typescript
describe("Communication Models", () => {
  test("Email model validation with Greek fields", () => {});
  test("SMS model Greek phone validation", () => {});
  test("Call model duration calculation", () => {});
  test("Meeting model Greek business hours validation", () => {});
});

describe("Greek Communication Utils", () => {
  test("validateGreekPhone function", () => {});
  test("formatGreekPhone function", () => {});
  test("isGreekBusinessHours function", () => {});
  test("getGreekHolidays function", () => {});
});
```

### Integration Tests

```typescript
describe("Communication APIs", () => {
  test("Email CRUD operations", () => {});
  test("SMS sending with Greek providers", () => {});
  test("Call logging and recording", () => {});
  test("Meeting scheduling with conflicts", () => {});
  test("Greek template generation", () => {});
});
```

### E2E Tests

```typescript
describe("Communication Workflows", () => {
  test("Complete email conversation thread", () => {});
  test("SMS campaign with Greek compliance", () => {});
  test("Call recording and transcription", () => {});
  test("Meeting scheduling with Greek calendar", () => {});
  test("Multi-channel communication flow", () => {});
});
```

## Performance Considerations

### Real-time Features

- WebSocket connections for live email/SMS
- Efficient pagination for large communication logs
- Background sync for email accounts
- Real-time call status updates
- Live meeting participant management

### Greek Provider Integration

- Async SMS sending with queue management
- Email provider failover mechanisms
- Call quality monitoring
- Meeting room availability caching
- Greek holiday calendar caching

### Security Features

- End-to-end encryption for sensitive communications
- GDPR-compliant data handling
- Secure file attachment handling
- Call recording encryption
- Meeting access control

## Success Metrics

### Communication Efficiency

- Email response time improvement
- SMS delivery rates with Greek providers
- Call connection success rates
- Meeting scheduling efficiency
- Cross-channel communication tracking

### Greek Market Adoption

- Greek template usage rates
- Local provider integration success
- Business hours compliance
- Holiday scheduling accuracy
- GDPR compliance metrics

### User Engagement

- Multi-channel usage patterns
- Communication preference adoption
- Template customization rates
- Integration tool usage
- Support ticket reduction related to communication issues
