# 🔔 Notifications System Specification

## Overview

The Notifications System is a shared module providing real-time, multi-channel notification capabilities across all applications in the Greek ERP/CRM platform. It supports push notifications, in-app notifications, email notifications, SMS, and Greek-specific compliance notifications.

## Core Features

### 1. Multi-Channel Notifications

- **In-App Notifications**: Real-time browser notifications with toast/banner display
- **Push Notifications**: Browser push notifications even when app is closed
- **Email Notifications**: HTML/text email notifications with templates
- **SMS Notifications**: Greek mobile carrier integration
- **Desktop Notifications**: Native OS notifications
- **Slack/Teams Integration**: Workplace notification channels

### 2. Notification Types

#### Business Notifications

- **Invoice Status**: Payment received, overdue, sent
- **Order Updates**: Order confirmed, shipped, delivered
- **Inventory Alerts**: Low stock, reorder points, expired items
- **Customer Activities**: New leads, support tickets, contract renewals
- **Task Assignments**: New tasks, deadlines, completions
- **Meeting Reminders**: Calendar events, appointments

#### Greek Compliance Notifications

- **AADE Submissions**: Tax filing deadlines, submission confirmations
- **VAT Reporting**: Monthly/quarterly VAT report reminders
- **Social Insurance**: IKA submission deadlines
- **Bank Reconciliation**: Monthly reconciliation reminders
- **Legal Deadlines**: Court dates, contract renewals, permit renewals

#### System Notifications

- **Security Alerts**: Failed login attempts, suspicious activity
- **System Updates**: Maintenance windows, feature releases
- **Performance Alerts**: High CPU usage, storage warnings
- **Backup Status**: Backup completion, failures
- **Integration Errors**: API failures, sync issues

### 3. Notification Delivery

#### Priority Levels

- **Critical**: Immediate delivery, multiple channels
- **High**: Delivery within 1 minute
- **Medium**: Delivery within 5 minutes
- **Low**: Batch delivery (hourly/daily)

#### Delivery Channels by Priority

```typescript
const deliveryMatrix = {
  critical: ["push", "email", "sms", "in-app"],
  high: ["push", "in-app", "email"],
  medium: ["in-app", "email"],
  low: ["in-app"],
};
```

### 4. User Preferences

#### Notification Settings

- **Channel Preferences**: Enable/disable by channel type
- **Category Filters**: Choose notification categories
- **Quiet Hours**: Set do-not-disturb periods
- **Frequency Control**: Immediate, digest, or disabled
- **Language Preferences**: Greek/English notifications

#### Subscription Management

- **Opt-in/Opt-out**: GDPR-compliant subscription management
- **Granular Control**: Per-notification-type preferences
- **Bulk Actions**: Subscribe/unsubscribe to categories
- **Temporary Suspension**: Vacation mode, sick leave

## Architecture

### 1. Core Components

#### Notification Engine

```typescript
interface NotificationEngine {
  // Core notification creation
  create(notification: NotificationPayload): Promise<string>;

  // Batch operations
  createBatch(notifications: NotificationPayload[]): Promise<string[]>;

  // Scheduling
  schedule(
    notification: NotificationPayload,
    deliveryTime: Date
  ): Promise<string>;

  // Delivery management
  deliver(notificationId: string): Promise<DeliveryResult>;
  retry(notificationId: string): Promise<DeliveryResult>;
  cancel(notificationId: string): Promise<boolean>;
}
```

#### Channel Handlers

```typescript
interface ChannelHandler {
  type: NotificationChannel;
  send(notification: ProcessedNotification): Promise<DeliveryResult>;
  validate(notification: NotificationPayload): boolean;
  getStatus(deliveryId: string): Promise<DeliveryStatus>;
}
```

#### Template Engine

```typescript
interface TemplateEngine {
  render(
    templateId: string,
    data: Record<string, any>
  ): Promise<RenderedTemplate>;
  compile(template: NotificationTemplate): Promise<CompiledTemplate>;
  getTemplate(
    templateId: string,
    language: string
  ): Promise<NotificationTemplate>;
}
```

### 2. Data Models

#### Notification Payload

```typescript
interface NotificationPayload {
  id: string;
  type: NotificationType;
  priority: NotificationPriority;
  recipient: NotificationRecipient;
  title: string;
  content: string;
  data?: Record<string, any>;
  channels: NotificationChannel[];
  templateId?: string;
  scheduledFor?: Date;
  expiresAt?: Date;
  tags: string[];
  metadata: NotificationMetadata;
}
```

#### Notification Template

```typescript
interface NotificationTemplate {
  id: string;
  name: string;
  category: string;
  language: string;
  channels: {
    [key in NotificationChannel]: {
      subject?: string;
      body: string;
      html?: string;
      assets?: string[];
    };
  };
  variables: TemplateVariable[];
  rules: NotificationRule[];
}
```

#### Delivery Result

```typescript
interface DeliveryResult {
  success: boolean;
  deliveryId: string;
  channel: NotificationChannel;
  timestamp: Date;
  error?: DeliveryError;
  metadata: DeliveryMetadata;
  retryCount: number;
  nextRetry?: Date;
}
```

### 3. Greek-Specific Features

#### AADE Integration Notifications

```typescript
interface AADENotificationData {
  submissionId: string;
  documentType: "invoice" | "receipt" | "credit-note";
  aadeResponse: AADEResponse;
  businessId: string;
  amount: number;
  currency: "EUR";
  timestamp: Date;
}
```

#### Greek Language Support

```typescript
interface GreekNotificationConfig {
  language: "el" | "en";
  dateFormat: "DD/MM/YYYY" | "MM/DD/YYYY";
  numberFormat: "european" | "us";
  currency: "EUR";
  timezone: "Europe/Athens";
}
```

## Implementation

### 1. Notification Service

#### Core Service

```typescript
class NotificationService {
  private engine: NotificationEngine;
  private channels: Map<NotificationChannel, ChannelHandler>;
  private templates: TemplateEngine;
  private preferences: PreferencesService;
  private queue: NotificationQueue;

  async send(payload: NotificationPayload): Promise<string> {
    // Validate payload
    const validation = this.validatePayload(payload);
    if (!validation.valid) {
      throw new ValidationError(validation.errors);
    }

    // Check user preferences
    const userPrefs = await this.preferences.get(payload.recipient.id);
    const allowedChannels = this.filterChannels(payload.channels, userPrefs);

    if (allowedChannels.length === 0) {
      throw new Error("No delivery channels available for user preferences");
    }

    // Create notification record
    const notification = await this.engine.create({
      ...payload,
      channels: allowedChannels,
    });

    // Schedule delivery
    if (payload.scheduledFor) {
      await this.queue.schedule(notification, payload.scheduledFor);
    } else {
      await this.queue.enqueue(notification);
    }

    return notification;
  }

  async sendBatch(payloads: NotificationPayload[]): Promise<string[]> {
    const notifications = await Promise.all(
      payloads.map((payload) => this.send(payload))
    );
    return notifications;
  }

  private filterChannels(
    channels: NotificationChannel[],
    preferences: UserPreferences
  ): NotificationChannel[] {
    return channels.filter((channel) => {
      // Check if channel is enabled
      if (!preferences.channels[channel]?.enabled) {
        return false;
      }

      // Check quiet hours
      if (this.isQuietHours(preferences.quietHours)) {
        return channel === "in-app"; // Only in-app during quiet hours
      }

      return true;
    });
  }
}
```

#### Channel Implementations

##### Email Channel

```typescript
class EmailChannelHandler implements ChannelHandler {
  type = "email" as const;
  private emailService: EmailService;

  async send(notification: ProcessedNotification): Promise<DeliveryResult> {
    const emailData = {
      to: notification.recipient.email,
      subject: notification.title,
      html: notification.content,
      attachments: notification.assets,
    };

    try {
      const result = await this.emailService.send(emailData);
      return {
        success: true,
        deliveryId: result.messageId,
        channel: "email",
        timestamp: new Date(),
        metadata: { provider: "smtp", messageId: result.messageId },
        retryCount: 0,
      };
    } catch (error) {
      return {
        success: false,
        deliveryId: "",
        channel: "email",
        timestamp: new Date(),
        error: {
          code: "EMAIL_SEND_FAILED",
          message: error.message,
        },
        metadata: {},
        retryCount: 0,
        nextRetry: new Date(Date.now() + 5 * 60 * 1000), // 5 minutes
      };
    }
  }

  validate(notification: NotificationPayload): boolean {
    return !!(notification.recipient.email && notification.title);
  }
}
```

##### Push Channel

```typescript
class PushChannelHandler implements ChannelHandler {
  type = "push" as const;
  private webPush: WebPushService;

  async send(notification: ProcessedNotification): Promise<DeliveryResult> {
    const pushData = {
      title: notification.title,
      body: notification.content,
      icon: "/icons/notification-icon.png",
      badge: "/icons/badge.png",
      data: notification.data,
      actions: notification.actions,
    };

    try {
      const subscriptions = await this.getSubscriptions(
        notification.recipient.id
      );
      const results = await Promise.allSettled(
        subscriptions.map((sub) => this.webPush.sendNotification(sub, pushData))
      );

      const successCount = results.filter(
        (r) => r.status === "fulfilled"
      ).length;

      return {
        success: successCount > 0,
        deliveryId: `push-${Date.now()}`,
        channel: "push",
        timestamp: new Date(),
        metadata: {
          totalSubscriptions: subscriptions.length,
          successfulDeliveries: successCount,
        },
        retryCount: 0,
      };
    } catch (error) {
      return {
        success: false,
        deliveryId: "",
        channel: "push",
        timestamp: new Date(),
        error: {
          code: "PUSH_SEND_FAILED",
          message: error.message,
        },
        metadata: {},
        retryCount: 0,
        nextRetry: new Date(Date.now() + 2 * 60 * 1000), // 2 minutes
      };
    }
  }
}
```

##### SMS Channel (Greek Carriers)

```typescript
class SMSChannelHandler implements ChannelHandler {
  type = "sms" as const;
  private smsService: GreekSMSService;

  async send(notification: ProcessedNotification): Promise<DeliveryResult> {
    const smsData = {
      to: this.normalizeGreekPhone(notification.recipient.phone),
      message: notification.content,
      sender: "ERP-SYSTEM",
    };

    try {
      const result = await this.smsService.send(smsData);
      return {
        success: true,
        deliveryId: result.messageId,
        channel: "sms",
        timestamp: new Date(),
        metadata: {
          carrier: result.carrier,
          messageId: result.messageId,
          cost: result.cost,
        },
        retryCount: 0,
      };
    } catch (error) {
      return {
        success: false,
        deliveryId: "",
        channel: "sms",
        timestamp: new Date(),
        error: {
          code: "SMS_SEND_FAILED",
          message: error.message,
        },
        metadata: {},
        retryCount: 0,
        nextRetry: new Date(Date.now() + 10 * 60 * 1000), // 10 minutes
      };
    }
  }

  private normalizeGreekPhone(phone: string): string {
    // Normalize Greek phone numbers
    let normalized = phone.replace(/\D/g, "");

    // Add country code if missing
    if (normalized.length === 10) {
      normalized = "30" + normalized;
    }

    return "+" + normalized;
  }
}
```

### 2. Template System

#### Template Repository

```typescript
class NotificationTemplateRepository {
  private templates: Map<string, NotificationTemplate> = new Map();

  async getTemplate(
    templateId: string,
    language: string
  ): Promise<NotificationTemplate> {
    const key = `${templateId}-${language}`;

    if (!this.templates.has(key)) {
      const template = await this.loadTemplate(templateId, language);
      this.templates.set(key, template);
    }

    return this.templates.get(key)!;
  }

  private async loadTemplate(
    templateId: string,
    language: string
  ): Promise<NotificationTemplate> {
    // Load from database or file system
    const template = await this.database.getNotificationTemplate(
      templateId,
      language
    );

    if (!template) {
      throw new Error(`Template not found: ${templateId} (${language})`);
    }

    return template;
  }
}
```

#### Greek Templates

```typescript
const greekTemplates = {
  "invoice-payment-received": {
    el: {
      subject: "Πληρωμή Παραλήφθηκε - Τιμολόγιο #{{invoiceNumber}}",
      body: "Η πληρωμή για το τιμολόγιο #{{invoiceNumber}} ύψους {{amount}}€ έχει παραληφθεί επιτυχώς.",
      html: `
        <div style="font-family: Arial, sans-serif;">
          <h2>Πληρωμή Παραλήφθηκε</h2>
          <p>Αγαπητέ/ή {{customerName}},</p>
          <p>Η πληρωμή για το τιμολόγιο <strong>#{{invoiceNumber}}</strong> ύψους <strong>{{amount}}€</strong> έχει παραληφθεί επιτυχώς.</p>
          <p>Ημερομηνία πληρωμής: {{paymentDate}}</p>
          <p>Τρόπος πληρωμής: {{paymentMethod}}</p>
          <p>Σας ευχαριστούμε για την συνεργασία!</p>
        </div>
      `,
    },
    en: {
      subject: "Payment Received - Invoice #{{invoiceNumber}}",
      body: "Payment for invoice #{{invoiceNumber}} of {{amount}}€ has been received successfully.",
      html: `
        <div style="font-family: Arial, sans-serif;">
          <h2>Payment Received</h2>
          <p>Dear {{customerName}},</p>
          <p>Payment for invoice <strong>#{{invoiceNumber}}</strong> of <strong>{{amount}}€</strong> has been received successfully.</p>
          <p>Payment date: {{paymentDate}}</p>
          <p>Payment method: {{paymentMethod}}</p>
          <p>Thank you for your business!</p>
        </div>
      `,
    },
  },

  "aade-submission-success": {
    el: {
      subject: "Επιτυχής Υποβολή στο AADE - {{documentType}}",
      body: "Το έγγραφο {{documentType}} υποβλήθηκε επιτυχώς στο AADE με MARK: {{mark}}",
      html: `
        <div style="font-family: Arial, sans-serif;">
          <h2>Επιτυχής Υποβολή AADE</h2>
          <p>Το έγγραφο <strong>{{documentType}}</strong> υποβλήθηκε επιτυχώς στο AADE.</p>
          <p>MARK: <strong>{{mark}}</strong></p>
          <p>UID: {{uid}}</p>
          <p>Ημερομηνία υποβολής: {{submissionDate}}</p>
          <p>Κωδικός απόκρισης: {{responseCode}}</p>
        </div>
      `,
    },
    en: {
      subject: "AADE Submission Success - {{documentType}}",
      body: "Document {{documentType}} submitted successfully to AADE with MARK: {{mark}}",
      html: `
        <div style="font-family: Arial, sans-serif;">
          <h2>AADE Submission Success</h2>
          <p>Document <strong>{{documentType}}</strong> submitted successfully to AADE.</p>
          <p>MARK: <strong>{{mark}}</strong></p>
          <p>UID: {{uid}}</p>
          <p>Submission date: {{submissionDate}}</p>
          <p>Response code: {{responseCode}}</p>
        </div>
      `,
    },
  },
};
```

### 3. Real-time Notifications

#### WebSocket Integration

```typescript
class RealTimeNotificationService {
  private wsConnections: Map<string, WebSocket> = new Map();
  private notificationService: NotificationService;

  constructor(notificationService: NotificationService) {
    this.notificationService = notificationService;
    this.setupWebSocketServer();
  }

  private setupWebSocketServer(): void {
    const wss = new WebSocketServer({ port: 8080 });

    wss.on("connection", (ws, req) => {
      const userId = this.extractUserId(req);
      this.wsConnections.set(userId, ws);

      ws.on("close", () => {
        this.wsConnections.delete(userId);
      });
    });
  }

  async sendRealTimeNotification(
    notification: ProcessedNotification
  ): Promise<void> {
    const ws = this.wsConnections.get(notification.recipient.id);

    if (ws && ws.readyState === WebSocket.OPEN) {
      const payload = {
        type: "notification",
        data: {
          id: notification.id,
          title: notification.title,
          content: notification.content,
          priority: notification.priority,
          timestamp: new Date(),
          actions: notification.actions,
        },
      };

      ws.send(JSON.stringify(payload));
    }
  }
}
```

## Usage Examples

### 1. Basic Notification

```typescript
const notificationService = new NotificationService();

await notificationService.send({
  id: "notif-001",
  type: "business",
  priority: "high",
  recipient: {
    id: "user-123",
    email: "user@example.com",
    phone: "+30698765432",
  },
  title: "New Order Received",
  content: "Order #12345 has been received and is being processed.",
  channels: ["in-app", "email", "push"],
  tags: ["order", "business"],
  metadata: {
    orderId: "12345",
    customerId: "cust-456",
    amount: 250.0,
  },
});
```

### 2. AADE Compliance Notification

```typescript
await notificationService.send({
  id: "aade-001",
  type: "compliance",
  priority: "critical",
  recipient: {
    id: "user-123",
    email: "accountant@company.gr",
  },
  title: "AADE Submission Required",
  content: "Monthly VAT report submission deadline is tomorrow.",
  channels: ["in-app", "email", "sms"],
  templateId: "aade-vat-reminder",
  data: {
    reportType: "VAT",
    deadline: "2024-02-15",
    period: "2024-01",
    amount: 1250.0,
  },
  tags: ["aade", "vat", "compliance"],
  metadata: {
    businessId: "bus-789",
    reportId: "vat-2024-01",
  },
});
```

### 3. Scheduled Notification

```typescript
const reminderDate = new Date("2024-02-14T09:00:00Z");

await notificationService.send({
  id: "reminder-001",
  type: "reminder",
  priority: "medium",
  recipient: {
    id: "user-123",
    email: "manager@company.gr",
  },
  title: "Monthly Report Due",
  content: "Don't forget to submit your monthly sales report.",
  channels: ["in-app", "email"],
  scheduledFor: reminderDate,
  tags: ["reminder", "report"],
  metadata: {
    reportType: "sales",
    month: "2024-01",
  },
});
```

## Configuration

### Environment Variables

```env
# Notification Service
NOTIFICATION_SERVICE_URL=http://localhost:3001
NOTIFICATION_WS_PORT=8080
NOTIFICATION_QUEUE_REDIS_URL=redis://localhost:6379

# Email Configuration
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USER=notifications@yourcompany.com
EMAIL_SMTP_PASS=your-app-password

# Push Notifications
VAPID_PUBLIC_KEY=your-vapid-public-key
VAPID_PRIVATE_KEY=your-vapid-private-key
VAPID_SUBJECT=mailto:admin@yourcompany.com

# SMS Configuration (Greek Carriers)
SMS_PROVIDER=cosmote|vodafone|wind
SMS_API_KEY=your-sms-api-key
SMS_SENDER_ID=ERP-SYSTEM

# Database
NOTIFICATIONS_DB_URL=postgresql://user:pass@localhost/notifications
```

### Package Dependencies

```json
{
  "dependencies": {
    "web-push": "^3.6.0",
    "nodemailer": "^6.9.0",
    "ioredis": "^5.3.0",
    "bull": "^4.10.0",
    "ws": "^8.13.0",
    "handlebars": "^4.7.0",
    "greek-utils": "^1.0.0"
  }
}
```

## Performance Considerations

### 1. Scalability

- **Queue System**: Use Redis/Bull for notification queuing
- **Database Optimization**: Index notification tables properly
- **Connection Pooling**: Manage WebSocket connections efficiently
- **Rate Limiting**: Implement per-user rate limiting

### 2. Reliability

- **Retry Logic**: Exponential backoff for failed deliveries
- **Dead Letter Queue**: Handle permanently failed notifications
- **Circuit Breaker**: Prevent cascade failures
- **Monitoring**: Track delivery success rates

### 3. Security

- **Authentication**: Secure WebSocket connections
- **Data Encryption**: Encrypt sensitive notification data
- **Access Control**: Role-based notification permissions
- **Audit Logging**: Track notification activities

## Integration Points

### 1. Client Applications

- **React Hook**: `useNotifications()` for real-time updates
- **Event Handlers**: Handle notification actions
- **UI Components**: Toast notifications, notification center

### 2. Backend Services

- **Business Logic**: Trigger notifications from business events
- **Webhooks**: Handle external service notifications
- **Scheduled Tasks**: Cron jobs for recurring notifications

### 3. External Services

- **AADE Integration**: Tax submission notifications
- **Banking APIs**: Payment confirmation notifications
- **Third-party APIs**: Integration status notifications

This notification system provides comprehensive, scalable, and Greek-compliant notification capabilities across all applications in the ERP platform.
