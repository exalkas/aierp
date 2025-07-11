# 🔔 Notification Preferences Screen Specification

## Overview

The Notification Preferences Screen allows users to customize their notification settings across all channels (in-app, email, SMS, push) and manage their communication preferences. This screen is part of the Client App settings and provides granular control over how users receive notifications.

## Features

### 1. Notification Channels

#### Channel Configuration

- **In-App Notifications**: Browser notifications and toast messages
- **Email Notifications**: Email delivery preferences and scheduling
- **SMS Notifications**: Mobile SMS delivery (Greek carriers)
- **Push Notifications**: Browser push notifications
- **Desktop Notifications**: Native OS notifications

#### Per-Channel Settings

- **Enable/Disable**: Toggle each channel on/off
- **Delivery Schedule**: Set quiet hours and active periods
- **Priority Filter**: Choose which priority levels to receive
- **Frequency Control**: Immediate, digest, or batch delivery

### 2. Notification Categories

#### Business Notifications

- **Order Management**: Order updates, shipping notifications
- **Invoice & Payments**: Invoice generation, payment confirmations
- **Customer Communications**: New leads, follow-ups, reminders
- **Task Management**: Task assignments, deadlines, completions
- **Calendar Events**: Meetings, appointments, reminders

#### Greek Compliance Notifications

- **AADE Submissions**: Tax filing notifications, submission confirmations
- **VAT Reporting**: Monthly/quarterly VAT report reminders
- **Legal Deadlines**: Court dates, contract renewals, permit renewals
- **Banking**: Bank reconciliation reminders, payment notifications
- **Social Insurance**: IKA submission deadlines, compliance alerts

#### System Notifications

- **Security Alerts**: Failed logins, suspicious activity
- **System Updates**: Maintenance windows, feature releases
- **Performance Alerts**: Storage warnings, quota notifications
- **Integration Status**: API failures, sync issues

### 3. Email Preferences

#### Email Delivery Settings

- **Primary Email**: Main email address for notifications
- **Secondary Email**: Backup email for critical notifications
- **Language Preference**: Greek or English for email content
- **Format Preference**: HTML, plain text, or both
- **Attachment Handling**: Include/exclude PDF attachments

#### Email Scheduling

- **Delivery Hours**: Set active hours for email delivery
- **Quiet Hours**: Define do-not-disturb periods
- **Weekend Delivery**: Enable/disable weekend emails
- **Vacation Mode**: Temporary suspension of non-critical emails

#### Email Content

- **Template Selection**: Choose from available email templates
- **Personalization**: Include/exclude personal information
- **Branding**: Company logo and branding in emails
- **Signature**: Custom email signature preferences

### 4. Advanced Settings

#### Quota Management

- **Storage Notifications**: Alerts when approaching storage limits
- **AI Usage Alerts**: Notifications about AI API usage and costs
- **Cost Thresholds**: Set spending alerts for various services
- **Usage Reports**: Monthly usage summaries

#### Privacy Settings

- **Data Collection**: Control what data is collected for notifications
- **Third-Party Sharing**: Manage data sharing with external services
- **Retention Period**: Set how long notification data is kept
- **GDPR Compliance**: Manage consent and data protection preferences

## User Interface

### 1. Main Settings Screen

#### Navigation Structure

```
Settings
├── Profile
├── Security
├── Notifications & Email ← This screen
├── Language & Regional
├── Privacy & Data
└── Account
```

#### Screen Layout

```
┌─────────────────────────────────────────────────────┐
│ ← Settings                    Notifications & Email │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 🔔 Notification Channels                           │
│ ┌─────────────────────────────────────────────────┐ │
│ │ In-App         [●] ✓ Enabled                    │ │
│ │ Email          [●] ✓ Enabled                    │ │
│ │ SMS            [○] ✗ Disabled                   │ │
│ │ Push           [●] ✓ Enabled                    │ │
│ │ Desktop        [○] ✗ Disabled                   │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ 📧 Email Preferences                               │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Primary Email    john@company.gr                │ │
│ │ Language         [Greek ▼]                      │ │
│ │ Format           [HTML ▼]                       │ │
│ │ Quiet Hours      22:00 - 08:00                  │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ 🏢 Business Notifications                          │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Orders & Invoices     [●] All [●] Email [○] SMS │ │
│ │ Customer Updates      [●] All [●] Email [○] SMS │ │
│ │ Task Assignments      [●] All [●] Email [○] SMS │ │
│ │ Calendar Events       [●] All [●] Email [○] SMS │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ 🇬🇷 Greek Compliance                               │
│ ┌─────────────────────────────────────────────────┐ │
│ │ AADE Submissions      [●] All [●] Email [●] SMS │ │
│ │ VAT Reporting         [●] All [●] Email [●] SMS │ │
│ │ Legal Deadlines       [●] All [●] Email [●] SMS │ │
│ │ Banking Alerts        [●] All [●] Email [○] SMS │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ⚙️ System Notifications                            │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Security Alerts       [●] All [●] Email [●] SMS │ │
│ │ System Updates        [●] All [●] Email [○] SMS │ │
│ │ Performance Alerts    [●] All [●] Email [○] SMS │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│           [Save Changes]  [Reset to Default]       │
└─────────────────────────────────────────────────────┘
```

### 2. Detailed Channel Settings

#### Email Configuration Modal

```
┌─────────────────────────────────────────────────────┐
│ ✕                Email Settings                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 📧 Email Addresses                                  │
│ Primary Email                                       │
│ ┌─────────────────────────────────────────────────┐ │
│ │ john@company.gr                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Secondary Email (Optional)                          │
│ ┌─────────────────────────────────────────────────┐ │
│ │ john.backup@gmail.com                           │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ 🕐 Delivery Schedule                                │
│ Quiet Hours                                         │
│ From: [22:00 ▼] To: [08:00 ▼]                      │
│                                                     │
│ Active Days                                         │
│ [✓] Mon [✓] Tue [✓] Wed [✓] Thu [✓] Fri            │
│ [✓] Sat [✓] Sun                                     │
│                                                     │
│ 🎨 Email Format                                     │
│ Language:    [Greek ▼]                              │
│ Format:      [HTML ▼]                               │
│ Template:    [Corporate ▼]                          │
│                                                     │
│ ⚡ Delivery Options                                  │
│ [✓] Include attachments (PDFs, documents)          │
│ [✓] Include company branding                        │
│ [✓] Track email opens and clicks                   │
│ [○] Digest mode (daily summary)                    │
│                                                     │
│ 🔒 Privacy Options                                  │
│ [✓] GDPR compliant processing                       │
│ [✓] Allow marketing communications                  │
│ [○] Share with business partners                   │
│                                                     │
│              [Save]  [Cancel]                       │
└─────────────────────────────────────────────────────┘
```

### 3. Greek Compliance Settings

#### AADE Notification Settings

```
┌─────────────────────────────────────────────────────┐
│ ✕            AADE Notification Settings             │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 🇬🇷 AADE Submission Notifications                   │
│                                                     │
│ Submission Success                                  │
│ [●] In-App  [●] Email  [●] SMS  [○] Push           │
│                                                     │
│ Submission Errors                                   │
│ [●] In-App  [●] Email  [●] SMS  [●] Push           │
│                                                     │
│ Daily Summary                                       │
│ [●] In-App  [●] Email  [○] SMS  [○] Push           │
│                                                     │
│ 📊 VAT Reporting                                    │
│                                                     │
│ Monthly VAT Due                                     │
│ [●] In-App  [●] Email  [●] SMS  [○] Push           │
│ Notify: [3 days ▼] before deadline                 │
│                                                     │
│ Quarterly VAT Due                                   │
│ [●] In-App  [●] Email  [●] SMS  [○] Push           │
│ Notify: [7 days ▼] before deadline                 │
│                                                     │
│ 🏛️ Legal Deadlines                                  │
│                                                     │
│ Contract Renewals                                   │
│ [●] In-App  [●] Email  [●] SMS  [○] Push           │
│ Notify: [30 days ▼] before expiry                  │
│                                                     │
│ Permit Renewals                                     │
│ [●] In-App  [●] Email  [●] SMS  [○] Push           │
│ Notify: [45 days ▼] before expiry                  │
│                                                     │
│ 📄 Document Templates                               │
│ AADE Email Template: [Greek Official ▼]            │
│ VAT Report Template: [Greek Business ▼]            │
│ Legal Notice Template: [Greek Legal ▼]             │
│                                                     │
│              [Save]  [Cancel]                       │
└─────────────────────────────────────────────────────┘
```

## Development Requirements

### 1. UI Components to be Created

#### Primary Components

- **`NotificationPreferencesScreen`** - Main container component
- **`NotificationChannelCard`** - Individual channel configuration
- **`EmailPreferencesModal`** - Detailed email settings popup
- **`NotificationCategorySection`** - Business/Compliance/System sections
- **`ChannelToggleGroup`** - Multi-channel toggle for categories
- **`QuietHoursPicker`** - Time range selector for quiet hours
- **`NotificationTestButton`** - Send test notification functionality

#### Supporting Components

- **`PreferencesSaveBar`** - Sticky save/reset bar
- **`NotificationPreview`** - Live preview of notification appearance
- **`EmailTemplateSelector`** - Template selection dropdown
- **`LanguageToggle`** - Greek/English language switcher

### 2. Reusable Components to be Used

#### From `@erp/shared-ui`

```typescript
import {
  Button,
  Modal,
  Card,
  Input,
  Select,
  Checkbox,
  Toggle,
  LoadingSpinner,
  Toast,
  Tabs,
  Divider,
  Badge,
  Tooltip,
} from "@erp/shared-ui";
```

#### From `@erp/shared-forms`

```typescript
import {
  FormProvider,
  FormField,
  FormSection,
  FormActions,
  ValidationError,
  FormSubmitButton,
} from "@erp/shared-forms";
```

#### From `@erp/shared-layout`

```typescript
import {
  SettingsLayout,
  SidebarNavigation,
  ContentHeader,
  ActionBar,
} from "@erp/shared-layout";
```

### 3. Contexts to be Used

#### Authentication Context

```typescript
import { useAuth } from "@erp/shared-auth";
// Provides: user, permissions, subscription info
```

#### Notifications Context

```typescript
import { useNotifications } from "@erp/notifications";
// Provides: preferences, updatePreferences, testNotification
```

#### Localization Context

```typescript
import { useTranslation } from "react-i18next";
// Provides: t() function, language switching
```

#### Theme Context

```typescript
import { useTheme } from "@erp/shared-ui";
// Provides: theme colors, dark/light mode
```

#### Form Context

```typescript
import { useForm } from "react-hook-form";
// Provides: form state, validation, submission
```

### 4. Tests to be Created

#### Unit Tests (`*.test.tsx`)

```typescript
// Component tests
NotificationPreferencesScreen.test.tsx;
NotificationChannelCard.test.tsx;
EmailPreferencesModal.test.tsx;
NotificationCategorySection.test.tsx;
QuietHoursPicker.test.tsx;

// Utility tests
notificationPreferencesService.test.ts;
preferencesValidation.test.ts;
```

#### Integration Tests (`*.integration.test.tsx`)

```typescript
// Full screen workflow tests
NotificationPreferencesWorkflow.integration.test.tsx;
EmailSettingsFlow.integration.test.tsx;
GreekComplianceSettings.integration.test.tsx;
```

#### API Tests (`*.api.test.ts`)

```typescript
// Backend integration tests
NotificationPreferencesAPI.test.ts;
TestNotificationAPI.test.ts;
PreferencesValidationAPI.test.ts;
```

#### E2E Tests (`*.e2e.test.ts`)

```typescript
// Cypress/Playwright tests
notification - preferences - settings.e2e.test.ts;
email - configuration - flow.e2e.test.ts;
greek - compliance - setup.e2e.test.ts;
```

#### Accessibility Tests (`*.a11y.test.tsx`)

```typescript
// WCAG compliance tests
NotificationPreferencesA11y.test.tsx;
FormAccessibility.test.tsx;
KeyboardNavigation.test.tsx;
```

### 5. APIs to be Created

#### Backend Endpoints (FastAPI)

```python
# Get user notification preferences
GET /api/v1/users/{user_id}/notification-preferences
Response: NotificationPreferencesSchema

# Update user notification preferences
PUT /api/v1/users/{user_id}/notification-preferences
Body: NotificationPreferencesUpdateSchema
Response: NotificationPreferencesSchema

# Send test notification
POST /api/v1/users/{user_id}/test-notification
Body: TestNotificationSchema
Response: TestNotificationResultSchema

# Get available notification templates
GET /api/v1/notification-templates
Query: ?language={el|en}&category={business|compliance|system}
Response: List[NotificationTemplateSchema]

# Get supported notification channels
GET /api/v1/notification-channels
Response: List[NotificationChannelSchema]

# Get quota status for user
GET /api/v1/users/{user_id}/quota-status
Response: QuotaStatusSchema

# Validate preferences before saving
POST /api/v1/users/{user_id}/notification-preferences/validate
Body: NotificationPreferencesUpdateSchema
Response: ValidationResultSchema
```

#### Frontend API Service

```typescript
// NotificationPreferencesService
class NotificationPreferencesService {
  getPreferences(userId: string): Promise<NotificationPreferences>;
  updatePreferences(
    userId: string,
    prefs: NotificationPreferences
  ): Promise<void>;
  testNotification(userId: string, channel: string): Promise<TestResult>;
  validatePreferences(
    prefs: NotificationPreferences
  ): Promise<ValidationResult>;
  getAvailableTemplates(language: string): Promise<NotificationTemplate[]>;
  getQuotaStatus(userId: string): Promise<QuotaStatus>;
}
```

### 6. Models to be Created

#### Frontend TypeScript Models

```typescript
// Core preference models
interface NotificationPreferences {
  id: string;
  userId: string;
  channels: NotificationChannels;
  categories: NotificationCategories;
  email: EmailPreferences;
  sms: SMSPreferences;
  privacy: PrivacySettings;
  createdAt: Date;
  updatedAt: Date;
}

interface NotificationChannels {
  inApp: ChannelSettings;
  email: ChannelSettings;
  sms: ChannelSettings;
  push: ChannelSettings;
  desktop: ChannelSettings;
}

interface ChannelSettings {
  enabled: boolean;
  priority: NotificationPriority;
  quietHours: QuietHours;
  rateLimiting: RateLimitSettings;
}

interface EmailPreferences {
  primaryEmail: string;
  secondaryEmail?: string;
  language: "el" | "en";
  format: "html" | "text" | "both";
  template: string;
  includeAttachments: boolean;
  includeBranding: boolean;
  trackingEnabled: boolean;
  digestMode: boolean;
  unsubscribePreferences: UnsubscribeSettings;
}

interface NotificationCategories {
  business: CategorySettings;
  compliance: CategorySettings;
  system: CategorySettings;
  marketing: CategorySettings;
}

interface CategorySettings {
  [subcategory: string]: {
    enabled: boolean;
    channels: string[];
    priority: NotificationPriority;
    frequency: NotificationFrequency;
    conditions: NotificationConditions[];
  };
}

// Greek-specific models
interface GreekComplianceSettings {
  aade: {
    submissions: boolean;
    errors: boolean;
    dailySummary: boolean;
    advanceNotice: number; // days
  };
  vat: {
    monthlyReports: boolean;
    quarterlyReports: boolean;
    advanceNotice: number; // days
  };
  legal: {
    contractRenewals: boolean;
    permitRenewals: boolean;
    courtDates: boolean;
    advanceNotice: number; // days
  };
}

// Test and validation models
interface TestNotificationRequest {
  channel: NotificationChannel;
  template?: string;
  data?: Record<string, any>;
}

interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}
```

#### Backend Python Models (Pydantic)

```python
# Pydantic schemas for API
class NotificationPreferencesSchema(BaseModel):
    id: UUID
    user_id: UUID
    channels: Dict[str, Any]
    categories: Dict[str, Any]
    email: Dict[str, Any]
    privacy: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class NotificationPreferencesUpdateSchema(BaseModel):
    channels: Optional[Dict[str, Any]]
    categories: Optional[Dict[str, Any]]
    email: Optional[Dict[str, Any]]
    privacy: Optional[Dict[str, Any]]

class TestNotificationSchema(BaseModel):
    channel: str
    template: Optional[str]
    data: Optional[Dict[str, Any]]

# SQLAlchemy models for database
class NotificationPreferences(Base):
    __tablename__ = "notification_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    channels = Column(JSON)
    categories = Column(JSON)
    email = Column(JSON)
    privacy = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

### 7. Additional Requirements

#### Database Schema

```sql
-- PostgreSQL migrations
-- Migration: create_notification_preferences_table
CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    channels JSONB DEFAULT '{}',
    categories JSONB DEFAULT '{}',
    email JSONB DEFAULT '{}',
    privacy JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notification_preferences_user_id ON notification_preferences(user_id);
CREATE INDEX idx_notification_preferences_channels ON notification_preferences USING GIN(channels);

-- Trigger for updated_at
CREATE TRIGGER update_notification_preferences_updated_at
    BEFORE UPDATE ON notification_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### Validation Schemas

```typescript
// Zod validation schemas
import { z } from "zod";

export const emailPreferencesSchema = z.object({
  primaryEmail: z.string().email().min(1, "Primary email is required"),
  secondaryEmail: z.string().email().optional(),
  language: z.enum(["el", "en"]),
  format: z.enum(["html", "text", "both"]),
  quietHours: z.object({
    start: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/),
    end: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/),
  }),
  includeAttachments: z.boolean(),
  includeBranding: z.boolean(),
  trackingEnabled: z.boolean(),
  digestMode: z.boolean(),
});

export const notificationPreferencesSchema = z.object({
  channels: z.record(z.boolean()),
  categories: z.record(
    z.object({
      enabled: z.boolean(),
      channels: z.array(z.string()),
      priority: z.enum(["all", "high", "critical"]),
    })
  ),
  email: emailPreferencesSchema,
  privacy: z.object({
    gdprCompliant: z.boolean(),
    marketingEnabled: z.boolean(),
    partnerSharing: z.boolean(),
  }),
});
```

#### Error Handling

```typescript
// Custom error classes
export class NotificationPreferencesError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = "NotificationPreferencesError";
  }
}

export class ValidationError extends NotificationPreferencesError {
  constructor(message: string, public field: string, public value: any) {
    super(message, "VALIDATION_ERROR", { field, value });
  }
}

export class QuotaExceededError extends NotificationPreferencesError {
  constructor(quotaType: string, limit: number, current: number) {
    super(
      `${quotaType} quota exceeded: ${current}/${limit}`,
      "QUOTA_EXCEEDED",
      { quotaType, limit, current }
    );
  }
}
```

#### Performance Considerations

```typescript
// React Query for caching
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

export const useNotificationPreferences = (userId: string) => {
  return useQuery({
    queryKey: ["notification-preferences", userId],
    queryFn: () => notificationService.getPreferences(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useUpdatePreferences = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, preferences }: UpdatePreferencesParams) =>
      notificationService.updatePreferences(userId, preferences),
    onSuccess: (_, { userId }) => {
      queryClient.invalidateQueries(["notification-preferences", userId]);
    },
  });
};

// Debounced auto-save
import { useDebounce } from "@erp/shared-hooks";

const useAutoSave = (preferences: NotificationPreferences, userId: string) => {
  const debouncedPreferences = useDebounce(preferences, 2000);
  const updateMutation = useUpdatePreferences();

  useEffect(() => {
    if (debouncedPreferences) {
      updateMutation.mutate({ userId, preferences: debouncedPreferences });
    }
  }, [debouncedPreferences, userId]);
};
```

#### Security Considerations

```typescript
// Rate limiting for API calls
export const rateLimitConfig = {
  updatePreferences: { maxRequests: 10, windowMs: 60000 }, // 10 per minute
  testNotification: { maxRequests: 5, windowMs: 300000 }, // 5 per 5 minutes
};

// Input sanitization
import DOMPurify from "dompurify";

export const sanitizeEmailInput = (input: string): string => {
  return DOMPurify.sanitize(input.trim());
};

// CSRF protection
export const apiHeaders = {
  "Content-Type": "application/json",
  "X-CSRF-Token": getCsrfToken(),
  Authorization: `Bearer ${getAuthToken()}`,
};
```

#### Accessibility Requirements

```typescript
// ARIA labels and roles
export const accessibilityProps = {
  channelToggle: {
    role: "switch",
    "aria-describedby": "channel-description",
    "aria-labelledby": "channel-label",
  },
  preferencesForm: {
    role: "form",
    "aria-label": "Notification preferences settings",
  },
  saveButton: {
    "aria-describedby": "save-status",
    "aria-live": "polite",
  },
};

// Keyboard navigation support
export const keyboardHandlers = {
  onKeyDown: (e: KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleToggle();
    }
  },
};
```

## Implementation

### 1. React Components

#### Main Settings Component

```typescript
import React, { useState, useEffect } from "react";
import { useAuth } from "@erp/shared-auth";
import { useNotifications } from "@erp/notifications";
import { useTranslation } from "react-i18next";

interface NotificationPreferences {
  channels: {
    inApp: boolean;
    email: boolean;
    sms: boolean;
    push: boolean;
    desktop: boolean;
  };
  categories: {
    [key: string]: {
      enabled: boolean;
      channels: string[];
      priority: "all" | "high" | "critical";
    };
  };
  email: {
    primaryEmail: string;
    secondaryEmail?: string;
    language: "el" | "en";
    format: "html" | "text" | "both";
    quietHours: {
      start: string;
      end: string;
    };
    activeDays: string[];
    includeAttachments: boolean;
    includeBranding: boolean;
    trackingEnabled: boolean;
    digestMode: boolean;
  };
  privacy: {
    gdprCompliant: boolean;
    marketingEnabled: boolean;
    partnerSharing: boolean;
  };
}

export const NotificationPreferencesScreen: React.FC = () => {
  const { user } = useAuth();
  const { updatePreferences, getPreferences } = useNotifications();
  const { t } = useTranslation();

  const [preferences, setPreferences] =
    useState<NotificationPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadPreferences();
  }, [user]);

  const loadPreferences = async () => {
    try {
      const userPrefs = await getPreferences(user?.id);
      setPreferences(userPrefs);
    } catch (error) {
      console.error("Failed to load preferences:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSavePreferences = async () => {
    if (!preferences) return;

    setSaving(true);
    try {
      await updatePreferences(user?.id, preferences);
      // Show success notification
    } catch (error) {
      console.error("Failed to save preferences:", error);
      // Show error notification
    } finally {
      setSaving(false);
    }
  };

  const handleChannelToggle = (channel: string, enabled: boolean) => {
    setPreferences((prev) =>
      prev
        ? {
            ...prev,
            channels: {
              ...prev.channels,
              [channel]: enabled,
            },
          }
        : null
    );
  };

  const handleCategoryUpdate = (category: string, settings: any) => {
    setPreferences((prev) =>
      prev
        ? {
            ...prev,
            categories: {
              ...prev.categories,
              [category]: settings,
            },
          }
        : null
    );
  };

  if (loading) {
    return <div className="p-4">Loading preferences...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          {t("notifications.title")}
        </h1>
        <p className="text-gray-600">{t("notifications.description")}</p>
      </div>

      {/* Notification Channels */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          🔔 {t("notifications.channels.title")}
        </h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <NotificationChannels
            channels={preferences?.channels}
            onToggle={handleChannelToggle}
          />
        </div>
      </div>

      {/* Email Preferences */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          📧 {t("notifications.email.title")}
        </h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <EmailPreferences
            email={preferences?.email}
            onChange={(email) =>
              setPreferences((prev) => (prev ? { ...prev, email } : null))
            }
          />
        </div>
      </div>

      {/* Business Notifications */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          🏢 {t("notifications.business.title")}
        </h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <BusinessNotifications
            categories={preferences?.categories}
            onUpdate={handleCategoryUpdate}
          />
        </div>
      </div>

      {/* Greek Compliance */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          🇬🇷 {t("notifications.compliance.title")}
        </h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <GreekComplianceNotifications
            categories={preferences?.categories}
            onUpdate={handleCategoryUpdate}
          />
        </div>
      </div>

      {/* System Notifications */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          ⚙️ {t("notifications.system.title")}
        </h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <SystemNotifications
            categories={preferences?.categories}
            onUpdate={handleCategoryUpdate}
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-end space-x-4">
        <button
          onClick={() => loadPreferences()}
          className="px-4 py-2 text-gray-600 bg-gray-200 rounded-md hover:bg-gray-300"
        >
          {t("common.reset")}
        </button>
        <button
          onClick={handleSavePreferences}
          disabled={saving}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? t("common.saving") : t("common.save")}
        </button>
      </div>
    </div>
  );
};
```

#### Notification Channels Component

```typescript
interface NotificationChannelsProps {
  channels: any;
  onToggle: (channel: string, enabled: boolean) => void;
}

const NotificationChannels: React.FC<NotificationChannelsProps> = ({
  channels,
  onToggle,
}) => {
  const { t } = useTranslation();

  const channelConfig = [
    {
      key: "inApp",
      label: t("notifications.channels.inApp"),
      icon: "🔔",
      description: t("notifications.channels.inApp.description"),
    },
    {
      key: "email",
      label: t("notifications.channels.email"),
      icon: "📧",
      description: t("notifications.channels.email.description"),
    },
    {
      key: "sms",
      label: t("notifications.channels.sms"),
      icon: "📱",
      description: t("notifications.channels.sms.description"),
    },
    {
      key: "push",
      label: t("notifications.channels.push"),
      icon: "🔔",
      description: t("notifications.channels.push.description"),
    },
    {
      key: "desktop",
      label: t("notifications.channels.desktop"),
      icon: "🖥️",
      description: t("notifications.channels.desktop.description"),
    },
  ];

  return (
    <div className="space-y-4">
      {channelConfig.map((channel) => (
        <div
          key={channel.key}
          className="flex items-center justify-between p-3 bg-white rounded-lg border"
        >
          <div className="flex items-center space-x-3">
            <span className="text-xl">{channel.icon}</span>
            <div>
              <h3 className="font-medium text-gray-900">{channel.label}</h3>
              <p className="text-sm text-gray-600">{channel.description}</p>
            </div>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={channels?.[channel.key] || false}
              onChange={(e) => onToggle(channel.key, e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
          </label>
        </div>
      ))}
    </div>
  );
};
```

#### Email Preferences Component

```typescript
interface EmailPreferencesProps {
  email: any;
  onChange: (email: any) => void;
}

const EmailPreferences: React.FC<EmailPreferencesProps> = ({
  email,
  onChange,
}) => {
  const { t } = useTranslation();

  const handleChange = (field: string, value: any) => {
    onChange({
      ...email,
      [field]: value,
    });
  };

  return (
    <div className="space-y-6">
      {/* Email Addresses */}
      <div>
        <h3 className="font-medium text-gray-900 mb-3">
          {t("notifications.email.addresses")}
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("notifications.email.primary")}
            </label>
            <input
              type="email"
              value={email?.primaryEmail || ""}
              onChange={(e) => handleChange("primaryEmail", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="john@company.gr"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("notifications.email.secondary")}
            </label>
            <input
              type="email"
              value={email?.secondaryEmail || ""}
              onChange={(e) => handleChange("secondaryEmail", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="john.backup@gmail.com"
            />
          </div>
        </div>
      </div>

      {/* Language and Format */}
      <div>
        <h3 className="font-medium text-gray-900 mb-3">
          {t("notifications.email.format")}
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("notifications.email.language")}
            </label>
            <select
              value={email?.language || "el"}
              onChange={(e) => handleChange("language", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="el">Ελληνικά</option>
              <option value="en">English</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("notifications.email.format")}
            </label>
            <select
              value={email?.format || "html"}
              onChange={(e) => handleChange("format", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="html">HTML</option>
              <option value="text">Plain Text</option>
              <option value="both">Both</option>
            </select>
          </div>
        </div>
      </div>

      {/* Quiet Hours */}
      <div>
        <h3 className="font-medium text-gray-900 mb-3">
          {t("notifications.email.quietHours")}
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("notifications.email.quietStart")}
            </label>
            <input
              type="time"
              value={email?.quietHours?.start || "22:00"}
              onChange={(e) =>
                handleChange("quietHours", {
                  ...email?.quietHours,
                  start: e.target.value,
                })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t("notifications.email.quietEnd")}
            </label>
            <input
              type="time"
              value={email?.quietHours?.end || "08:00"}
              onChange={(e) =>
                handleChange("quietHours", {
                  ...email?.quietHours,
                  end: e.target.value,
                })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Options */}
      <div>
        <h3 className="font-medium text-gray-900 mb-3">
          {t("notifications.email.options")}
        </h3>
        <div className="space-y-3">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={email?.includeAttachments || false}
              onChange={(e) =>
                handleChange("includeAttachments", e.target.checked)
              }
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">
              {t("notifications.email.includeAttachments")}
            </span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={email?.includeBranding || false}
              onChange={(e) =>
                handleChange("includeBranding", e.target.checked)
              }
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">
              {t("notifications.email.includeBranding")}
            </span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={email?.trackingEnabled || false}
              onChange={(e) =>
                handleChange("trackingEnabled", e.target.checked)
              }
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">
              {t("notifications.email.trackingEnabled")}
            </span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={email?.digestMode || false}
              onChange={(e) => handleChange("digestMode", e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">
              {t("notifications.email.digestMode")}
            </span>
          </label>
        </div>
      </div>
    </div>
  );
};
```

### 2. API Integration

#### Preferences Service

```typescript
class NotificationPreferencesService {
  private apiUrl = process.env.REACT_APP_API_URL;

  async getPreferences(userId: string): Promise<NotificationPreferences> {
    const response = await fetch(
      `${this.apiUrl}/users/${userId}/notification-preferences`
    );
    if (!response.ok) {
      throw new Error("Failed to fetch preferences");
    }
    return response.json();
  }

  async updatePreferences(
    userId: string,
    preferences: NotificationPreferences
  ): Promise<void> {
    const response = await fetch(
      `${this.apiUrl}/users/${userId}/notification-preferences`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(preferences),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to update preferences");
    }
  }

  async testNotification(userId: string, channel: string): Promise<void> {
    const response = await fetch(
      `${this.apiUrl}/users/${userId}/test-notification`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ channel }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to send test notification");
    }
  }
}
```

### 3. Localization

#### Greek Translations

```json
{
  "notifications": {
    "title": "Ειδοποιήσεις & Email",
    "description": "Διαχειριστείτε τις προτιμήσεις ειδοποιήσεων και email",
    "channels": {
      "title": "Κανάλια Ειδοποιήσεων",
      "inApp": "Ειδοποιήσεις Εφαρμογής",
      "email": "Email",
      "sms": "SMS",
      "push": "Push Notifications",
      "desktop": "Ειδοποιήσεις Επιφάνειας Εργασίας"
    },
    "email": {
      "title": "Προτιμήσεις Email",
      "addresses": "Διευθύνσεις Email",
      "primary": "Κύριο Email",
      "secondary": "Δευτερεύον Email",
      "language": "Γλώσσα",
      "format": "Μορφή",
      "quietHours": "Ώρες Ησυχίας",
      "quietStart": "Από",
      "quietEnd": "Έως",
      "options": "Επιλογές",
      "includeAttachments": "Συμπεριλαμβάνω συνημμένα",
      "includeBranding": "Συμπεριλαμβάνω εταιρικό branding",
      "trackingEnabled": "Ενεργοποίηση tracking",
      "digestMode": "Λειτουργία σύνοψης"
    },
    "business": {
      "title": "Επιχειρηματικές Ειδοποιήσεις",
      "orders": "Παραγγελίες & Τιμολόγια",
      "customers": "Ενημερώσεις Πελατών",
      "tasks": "Εργασίες",
      "calendar": "Ημερολόγιο"
    },
    "compliance": {
      "title": "Συμμόρφωση Ελλάδας",
      "aade": "Υποβολές AADE",
      "vat": "Αναφορές ΦΠΑ",
      "legal": "Νομικές Προθεσμίες",
      "banking": "Τραπεζικές Ειδοποιήσεις"
    },
    "system": {
      "title": "Ειδοποιήσεις Συστήματος",
      "security": "Ασφάλεια",
      "updates": "Ενημερώσεις",
      "performance": "Απόδοση"
    }
  }
}
```

#### English Translations

```json
{
  "notifications": {
    "title": "Notifications & Email",
    "description": "Manage your notification and email preferences",
    "channels": {
      "title": "Notification Channels",
      "inApp": "In-App Notifications",
      "email": "Email",
      "sms": "SMS",
      "push": "Push Notifications",
      "desktop": "Desktop Notifications"
    },
    "email": {
      "title": "Email Preferences",
      "addresses": "Email Addresses",
      "primary": "Primary Email",
      "secondary": "Secondary Email",
      "language": "Language",
      "format": "Format",
      "quietHours": "Quiet Hours",
      "quietStart": "From",
      "quietEnd": "To",
      "options": "Options",
      "includeAttachments": "Include attachments",
      "includeBranding": "Include company branding",
      "trackingEnabled": "Enable tracking",
      "digestMode": "Digest mode"
    },
    "business": {
      "title": "Business Notifications",
      "orders": "Orders & Invoices",
      "customers": "Customer Updates",
      "tasks": "Tasks",
      "calendar": "Calendar"
    },
    "compliance": {
      "title": "Greek Compliance",
      "aade": "AADE Submissions",
      "vat": "VAT Reports",
      "legal": "Legal Deadlines",
      "banking": "Banking Alerts"
    },
    "system": {
      "title": "System Notifications",
      "security": "Security",
      "updates": "Updates",
      "performance": "Performance"
    }
  }
}
```

## Integration Points

### 1. Backend API Endpoints

```python
# Python FastAPI endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/{user_id}/notification-preferences")
async def get_notification_preferences(
    user_id: str,
    db: Session = Depends(get_db)
):
    # Get user preferences from database
    preferences = db.query(NotificationPreferences).filter_by(user_id=user_id).first()
    return preferences

@router.put("/users/{user_id}/notification-preferences")
async def update_notification_preferences(
    user_id: str,
    preferences: NotificationPreferencesSchema,
    db: Session = Depends(get_db)
):
    # Update user preferences
    db_preferences = db.query(NotificationPreferences).filter_by(user_id=user_id).first()
    if db_preferences:
        for key, value in preferences.dict().items():
            setattr(db_preferences, key, value)
    else:
        db_preferences = NotificationPreferences(user_id=user_id, **preferences.dict())
        db.add(db_preferences)

    db.commit()
    return {"message": "Preferences updated successfully"}
```

### 2. Database Schema

```sql
-- PostgreSQL schema
CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    channels JSONB DEFAULT '{"inApp": true, "email": true, "sms": false, "push": false, "desktop": false}',
    categories JSONB DEFAULT '{}',
    email_settings JSONB DEFAULT '{}',
    privacy_settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notification_preferences_user_id ON notification_preferences(user_id);
```

This comprehensive notification preferences screen provides users with full control over their communication settings while maintaining Greek compliance and multilingual support.
