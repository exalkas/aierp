# 🔧 Shared Modules Overview

## Overview

The Greek ERP/CRM platform includes two critical shared modules that work together to provide comprehensive communication capabilities across all applications:

1. **Notifications System** - Multi-channel notification delivery
2. **Email System** - Advanced email capabilities with Greek compliance

## Module Relationship

### Integration Architecture

```typescript
// High-level integration flow
NotificationSystem -> EmailSystem -> SMTP/External Services
     ^                     ^
     |                     |
Business Logic      Template Engine
     |                     |
All Applications    Greek Compliance
```

### How They Work Together

#### 1. Notification Triggers Email

The Notifications System uses the Email System as one of its delivery channels:

```typescript
// In NotificationService
class EmailChannelHandler implements ChannelHandler {
  private emailService: EmailService;

  async send(notification: ProcessedNotification): Promise<DeliveryResult> {
    return await this.emailService.send({
      id: notification.id,
      to: [{ email: notification.recipient.email }],
      subject: notification.title,
      templateId: notification.templateId,
      templateData: notification.data,
    });
  }
}
```

#### 2. Shared Template System

Both systems share templates for consistency:

```typescript
// Shared template for invoice notifications
const invoiceTemplate = {
  notification: {
    title: "Τιμολόγιο #{{invoiceNumber}} - {{status}}",
    content: "Το τιμολόγιο έχει {{statusText}}",
  },
  email: {
    subject: "Τιμολόγιο #{{invoiceNumber}} - {{status}}",
    templateId: "invoice-notification-greek",
  },
};
```

## Key Features

### 1. Notifications System

- **Multi-channel delivery** (in-app, push, email, SMS)
- **Real-time notifications** via WebSocket
- **Quota management** for AI and storage
- **Greek compliance notifications** (AADE, VAT, legal)
- **User preferences** and quiet hours
- **Priority-based delivery**

### 2. Email System

- **Rich HTML templates** with Greek support
- **Attachment handling** (PDFs, documents)
- **Queue management** with retry logic
- **Analytics and tracking** (opens, clicks)
- **Greek templates** for business communications
- **SMTP integration** with multiple providers

## Usage Patterns

### 1. Business Event Notification

```typescript
// When an invoice is created
const invoice = await createInvoice(invoiceData);

// Send notification via notification system
await notificationService.send({
  type: "business",
  priority: "high",
  recipient: { id: invoice.customerId },
  title: "Νέο Τιμολόγιο",
  content: `Το τιμολόγιο #${invoice.number} έχει δημιουργηθεί`,
  channels: ["in-app", "email"], // Email will be handled by EmailSystem
  templateId: "invoice-created",
  data: { invoice },
});
```

### 2. Direct Email Sending

```typescript
// For marketing campaigns or bulk communications
await emailService.send({
  to: customers,
  templateId: "marketing-campaign-greek",
  templateData: { campaignData },
  priority: "low",
});
```

### 3. AADE Compliance Notifications

```typescript
// When AADE submission completes
await notificationService.send({
  type: "compliance",
  priority: "critical",
  recipient: { id: accountantId },
  title: "Υποβολή AADE",
  content: "Επιτυχής υποβολή στο AADE",
  channels: ["in-app", "email", "sms"],
  templateId: "aade-submission-success",
  data: { aadeResponse },
});
```

## Configuration

### Shared Configuration

```typescript
interface SharedModulesConfig {
  notifications: {
    enabled: boolean;
    channels: NotificationChannel[];
    realTimeEnabled: boolean;
    quotaLimits: QuotaLimits;
  };
  email: {
    enabled: boolean;
    smtp: SMTPConfig;
    templates: TemplateConfig;
    queue: QueueConfig;
    analytics: AnalyticsConfig;
  };
  integration: {
    emailAsNotificationChannel: boolean;
    sharedTemplates: boolean;
    unifiedAnalytics: boolean;
  };
}
```

### Environment Setup

```env
# Notifications
NOTIFICATION_SERVICE_ENABLED=true
NOTIFICATION_REALTIME_ENABLED=true
NOTIFICATION_WS_PORT=8080

# Email
EMAIL_SERVICE_ENABLED=true
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587

# Integration
SHARED_TEMPLATES_ENABLED=true
UNIFIED_ANALYTICS_ENABLED=true
```

## Development Guidelines

### 1. Creating New Notification Types

1. Define notification template in both systems
2. Set up appropriate channels (in-app, email, SMS)
3. Configure Greek/English versions
4. Test delivery across all channels

### 2. Adding Email Templates

1. Create Handlebars template with Greek support
2. Add proper styling for Greek fonts
3. Include company branding and legal notices
4. Test rendering with sample data

### 3. Testing Strategy

```typescript
// Test both systems together
describe("Notification + Email Integration", () => {
  it("should send email when notification uses email channel", async () => {
    const notification = createTestNotification();
    const result = await notificationService.send(notification);

    expect(result.success).toBe(true);
    expect(emailService.getSentEmails()).toContain(notification.id);
  });
});
```

## Performance Considerations

### 1. Shared Resources

- **Template Cache**: Shared template caching between systems
- **Queue Management**: Unified queue for better resource utilization
- **Database Connections**: Shared connection pools

### 2. Scalability

- **Horizontal Scaling**: Both systems can scale independently
- **Load Balancing**: Distribute load across multiple instances
- **Caching**: Redis for templates and user preferences

### 3. Monitoring

- **Unified Dashboard**: Combined metrics from both systems
- **Health Checks**: Monitor both notification and email delivery
- **Alerts**: Set up alerts for failed deliveries or queue backlogs

## Security

### 1. Data Protection

- **Encryption**: Encrypt sensitive data in transit and at rest
- **Access Control**: Role-based access to notification/email systems
- **Audit Logging**: Track all notification and email activities

### 2. Greek Compliance

- **GDPR**: Consent management for notifications and emails
- **Data Retention**: Automatic cleanup of old notifications/emails
- **Privacy Controls**: User controls for notification preferences

## Deployment

### 1. Package Structure

```
packages/
├── notifications/
│   ├── src/
│   ├── templates/
│   └── package.json
├── email/
│   ├── src/
│   ├── templates/
│   └── package.json
└── shared-communication/
    ├── types/
    ├── templates/
    └── package.json
```

### 2. Service Dependencies

```yaml
# docker-compose.yml
version: "3.8"
services:
  notification-service:
    build: ./packages/notifications
    depends_on:
      - redis
      - postgres
    environment:
      - EMAIL_SERVICE_URL=http://email-service:3000

  email-service:
    build: ./packages/email
    depends_on:
      - redis
      - postgres
    environment:
      - SMTP_HOST=${EMAIL_SMTP_HOST}

  redis:
    image: redis:7-alpine

  postgres:
    image: postgres:15-alpine
```

This integrated approach ensures seamless communication capabilities across all Greek ERP/CRM applications while maintaining modularity and scalability.
