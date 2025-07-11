# 📧 Email System Specification

## Overview

The Email System is a shared module providing comprehensive email capabilities for the Greek ERP/CRM platform. It handles transactional emails, marketing campaigns, automated business communications, and Greek-specific compliance communications with full multilingual support.

## Core Features

### 1. Email Types

#### Transactional Emails

- **Order Confirmations**: Order placement, shipping, delivery
- **Invoice & Payment**: Invoice generation, payment receipts, reminders
- **Account Management**: Registration, password reset, profile updates
- **System Notifications**: Security alerts, system updates, maintenance
- **Appointment Confirmations**: Booking confirmations, reminders, cancellations

#### Business Communications

- **Customer Onboarding**: Welcome sequences, setup guides
- **Follow-up Sequences**: Post-purchase, feedback requests
- **Renewal Reminders**: Subscription renewals, contract extensions
- **Support Communications**: Ticket updates, resolution notifications

#### Greek Compliance Emails

- **AADE Notifications**: Tax submission confirmations, error reports
- **VAT Communications**: Monthly/quarterly VAT reports
- **Legal Notifications**: Contract renewals, compliance deadlines
- **Banking Communications**: Reconciliation reports, payment confirmations

### 2. Email Capabilities

#### Advanced Features

- **Rich HTML Templates**: Responsive email templates
- **Attachment Support**: PDF invoices, documents, images
- **Multilingual Support**: Greek/English with automatic language detection
- **Template Inheritance**: Base templates with customizable sections
- **Dynamic Content**: Personalized content based on user data
- **A/B Testing**: Template and subject line testing

#### Delivery Management

- **Queue System**: Prioritized email sending
- **Batch Processing**: Bulk email campaigns
- **Retry Logic**: Automatic retry for failed deliveries
- **Bounce Handling**: Automatic bounce processing
- **Suppression Lists**: Unsubscribe and bounce management

#### Analytics & Tracking

- **Open Tracking**: Email open rates and timing
- **Click Tracking**: Link clicks and engagement
- **Delivery Reports**: Sent, delivered, bounced, failed
- **Engagement Metrics**: Response rates, conversion tracking
- **Performance Analytics**: Campaign performance reports

### 3. Greek-Specific Features

#### Language Support

- **Greek Fonts**: Proper Greek character rendering
- **RTL Support**: Limited RTL support for Greek text
- **Date/Time Formatting**: Greek locale formatting
- **Currency Formatting**: Euro formatting per Greek standards
- **Address Formatting**: Greek address standards

#### Compliance Features

- **GDPR Compliance**: Consent management, data protection
- **Greek Legal Requirements**: Required legal disclaimers
- **Tax Documentation**: Automated tax document emails
- **Business Registry**: Company registration details inclusion

## Architecture

### 1. Core Components

#### Email Service

```typescript
interface EmailService {
  // Core email sending
  send(email: EmailRequest): Promise<EmailResult>;
  sendBatch(emails: EmailRequest[]): Promise<EmailResult[]>;

  // Template management
  renderTemplate(templateId: string, data: any): Promise<RenderedEmail>;

  // Campaign management
  sendCampaign(campaign: EmailCampaign): Promise<CampaignResult>;

  // Analytics
  getDeliveryStats(emailId: string): Promise<DeliveryStats>;
  getCampaignStats(campaignId: string): Promise<CampaignStats>;
}
```

#### Template Engine

```typescript
interface TemplateEngine {
  compile(template: EmailTemplate): Promise<CompiledTemplate>;
  render(templateId: string, data: TemplateData): Promise<RenderedEmail>;
  getTemplate(templateId: string, language: string): Promise<EmailTemplate>;
  validateTemplate(template: EmailTemplate): Promise<ValidationResult>;
}
```

#### Queue Manager

```typescript
interface QueueManager {
  enqueue(email: EmailRequest, priority: Priority): Promise<string>;
  enqueueScheduled(email: EmailRequest, sendAt: Date): Promise<string>;
  getQueueStats(): Promise<QueueStats>;
  retryFailed(emailId: string): Promise<boolean>;
}
```

### 2. Data Models

#### Email Request

```typescript
interface EmailRequest {
  id: string;
  to: EmailRecipient[];
  cc?: EmailRecipient[];
  bcc?: EmailRecipient[];
  from: EmailSender;
  replyTo?: string;
  subject: string;
  content: EmailContent;
  attachments?: EmailAttachment[];
  templateId?: string;
  templateData?: TemplateData;
  priority: EmailPriority;
  tags: string[];
  metadata: EmailMetadata;
  scheduledFor?: Date;
  expiresAt?: Date;
}
```

#### Email Content

```typescript
interface EmailContent {
  text: string;
  html: string;
  amp?: string; // AMP for Email support
  previewText?: string;
  language: "el" | "en";
  charset: "UTF-8";
}
```

#### Email Template

```typescript
interface EmailTemplate {
  id: string;
  name: string;
  category: string;
  language: "el" | "en";
  version: string;
  subject: string;
  content: {
    text: string;
    html: string;
    amp?: string;
  };
  variables: TemplateVariable[];
  styles: EmailStyles;
  metadata: TemplateMetadata;
}
```

#### Greek-Specific Data

```typescript
interface GreekEmailData {
  companyDetails: {
    name: string;
    vatNumber: string;
    taxOffice: string;
    address: GreekAddress;
    phone: string;
    email: string;
  };
  legalNotices: {
    privacyPolicy: string;
    termsOfService: string;
    gdprNotice: string;
  };
  formatting: {
    currency: "EUR";
    dateFormat: "DD/MM/YYYY";
    timeFormat: "HH:mm";
    timezone: "Europe/Athens";
  };
}
```

### 3. Email Templates

#### Base Template Structure

```html
<!DOCTYPE html>
<html lang="{{language}}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{subject}}</title>
    <style>
      /* Greek font support */
      @import url("https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap");

      body {
        font-family: "Open Sans", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
      }

      .container {
        max-width: 600px;
        margin: 0 auto;
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      }

      .header {
        border-bottom: 2px solid #0066cc;
        padding-bottom: 20px;
        margin-bottom: 20px;
      }

      .logo {
        max-height: 60px;
        margin-bottom: 10px;
      }

      .content {
        margin-bottom: 30px;
      }

      .footer {
        border-top: 1px solid #eee;
        padding-top: 20px;
        font-size: 12px;
        color: #666;
      }

      .button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #0066cc;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        font-weight: 600;
      }

      .greek-text {
        font-family: "Open Sans", Arial, sans-serif;
        direction: ltr;
      }

      .amount {
        font-weight: 600;
        color: #0066cc;
      }

      .table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
      }

      .table th,
      .table td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #eee;
      }

      .table th {
        background-color: #f8f9fa;
        font-weight: 600;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <img src="{{companyLogo}}" alt="{{companyName}}" class="logo" />
        <h1>{{emailTitle}}</h1>
      </div>

      <div class="content">{{content}}</div>

      <div class="footer">
        <p><strong>{{companyName}}</strong></p>
        <p>{{companyAddress}}</p>
        <p>ΑΦΜ: {{vatNumber}} | ΔΟΥ: {{taxOffice}}</p>
        <p>Email: {{companyEmail}} | Τηλ: {{companyPhone}}</p>

        {{#if unsubscribeLink}}
        <p>
          <a href="{{unsubscribeLink}}">Κατάργηση εγγραφής</a> |
          <a href="{{privacyPolicyLink}}">Πολιτική Απορρήτου</a>
        </p>
        {{/if}}
      </div>
    </div>
  </body>
</html>
```

#### Greek Invoice Template

```html
<div class="greek-text">
  <h2>Τιμολόγιο #{{invoiceNumber}}</h2>

  <div
    style="display: flex; justify-content: space-between; margin-bottom: 20px;"
  >
    <div>
      <h3>Πληρωμή προς:</h3>
      <p>
        <strong>{{customerName}}</strong><br />
        {{customerAddress}}<br />
        ΑΦΜ: {{customerVatNumber}}<br />
        Email: {{customerEmail}}
      </p>
    </div>

    <div>
      <h3>Στοιχεία Τιμολογίου:</h3>
      <p>
        <strong>Αριθμός:</strong> {{invoiceNumber}}<br />
        <strong>Ημερομηνία:</strong> {{invoiceDate}}<br />
        <strong>Προθεσμία:</strong> {{dueDate}}<br />
        <strong>Νόμισμα:</strong> EUR
      </p>
    </div>
  </div>

  <table class="table">
    <thead>
      <tr>
        <th>Περιγραφή</th>
        <th>Ποσότητα</th>
        <th>Τιμή Μονάδας</th>
        <th>Σύνολο</th>
      </tr>
    </thead>
    <tbody>
      {{#each items}}
      <tr>
        <td>{{description}}</td>
        <td>{{quantity}}</td>
        <td>{{unitPrice}}€</td>
        <td>{{total}}€</td>
      </tr>
      {{/each}}
    </tbody>
  </table>

  <div style="text-align: right; margin-top: 20px;">
    <p>
      <strong>Μερικό Σύνολο:</strong> <span class="amount">{{subtotal}}€</span>
    </p>
    <p>
      <strong>ΦΠΑ ({{vatRate}}%):</strong>
      <span class="amount">{{vatAmount}}€</span>
    </p>
    <p style="font-size: 18px;">
      <strong>Τελικό Σύνολο:</strong> <span class="amount">{{total}}€</span>
    </p>
  </div>

  <div
    style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 4px;"
  >
    <h4>Οδηγίες Πληρωμής:</h4>
    <p>{{paymentInstructions}}</p>

    {{#if bankDetails}}
    <p>
      <strong>Τραπεζικά Στοιχεία:</strong><br />
      {{bankDetails.bankName}}<br />
      IBAN: {{bankDetails.iban}}<br />
      BIC: {{bankDetails.bic}}
    </p>
    {{/if}}
  </div>

  <div style="margin-top: 20px; font-size: 14px; color: #666;">
    <p>Αυτό το τιμολόγιο έχει υποβληθεί στο AADE με MARK: {{aadeMark}}</p>
    <p>Για οποιαδήποτε απορία, επικοινωνήστε μαζί μας στο {{supportEmail}}</p>
  </div>
</div>
```

#### AADE Notification Template

```html
<div class="greek-text">
  <h2>{{#if success}}Επιτυχής{{else}}Αποτυχημένη{{/if}} Υποβολή AADE</h2>

  <div
    style="padding: 15px; margin: 20px 0; border-radius: 4px; {{#if success}}background-color: #d4edda; color: #155724;{{else}}background-color: #f8d7da; color: #721c24;{{/if}}"
  >
    <h3>
      {{#if success}}Η υποβολή ολοκληρώθηκε επιτυχώς{{else}}Προέκυψε σφάλμα κατά
      την υποβολή{{/if}}
    </h3>
  </div>

  <table class="table">
    <tr>
      <th>Τύπος Εγγράφου:</th>
      <td>{{documentType}}</td>
    </tr>
    <tr>
      <th>Αριθμός Εγγράφου:</th>
      <td>{{documentNumber}}</td>
    </tr>
    <tr>
      <th>Ημερομηνία Υποβολής:</th>
      <td>{{submissionDate}}</td>
    </tr>
    {{#if success}}
    <tr>
      <th>MARK:</th>
      <td><strong>{{aadeMark}}</strong></td>
    </tr>
    <tr>
      <th>UID:</th>
      <td>{{aadeUid}}</td>
    </tr>
    {{else}}
    <tr>
      <th>Κωδικός Σφάλματος:</th>
      <td>{{errorCode}}</td>
    </tr>
    <tr>
      <th>Περιγραφή Σφάλματος:</th>
      <td>{{errorDescription}}</td>
    </tr>
    {{/if}}
  </table>

  {{#if success}}
  <div
    style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 4px;"
  >
    <h4>Επόμενα Βήματα:</h4>
    <ul>
      <li>Το έγγραφο έχει καταχωρηθεί επιτυχώς στο AADE</li>
      <li>Μπορείτε να βρείτε το MARK στο σύστημά σας</li>
      <li>Το έγγραφο είναι έγκυρο για φορολογικούς σκοπούς</li>
    </ul>
  </div>
  {{else}}
  <div
    style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 4px;"
  >
    <h4>Τι πρέπει να κάνετε:</h4>
    <ul>
      <li>Ελέγξτε τα στοιχεία του εγγράφου</li>
      <li>Διορθώστε τυχόν σφάλματα</li>
      <li>Επαναλάβετε την υποβολή</li>
      <li>Επικοινωνήστε με την τεχνική υποστήριξη αν χρειάζεται</li>
    </ul>
  </div>
  {{/if}}

  <div
    style="margin-top: 30px; padding: 15px; background-color: #fff3cd; border-radius: 4px; color: #856404;"
  >
    <p>
      <strong>Σημείωση:</strong> Αυτό το email δημιουργήθηκε αυτόματα από το
      σύστημα ERP. Παρακαλώ μην απαντήσετε σε αυτό το μήνυμα.
    </p>
  </div>
</div>
```

## Implementation

### 1. Email Service

#### Core Email Service

```typescript
class EmailService {
  private transporter: Transporter;
  private templateEngine: TemplateEngine;
  private queueManager: QueueManager;
  private analytics: EmailAnalytics;

  constructor(config: EmailConfig) {
    this.transporter = this.createTransporter(config);
    this.templateEngine = new TemplateEngine();
    this.queueManager = new QueueManager(config.redis);
    this.analytics = new EmailAnalytics(config.database);
  }

  async send(request: EmailRequest): Promise<EmailResult> {
    try {
      // Validate email request
      const validation = await this.validateRequest(request);
      if (!validation.valid) {
        throw new ValidationError(validation.errors);
      }

      // Render template if needed
      let content = request.content;
      if (request.templateId) {
        const rendered = await this.templateEngine.render(
          request.templateId,
          request.templateData || {}
        );
        content = rendered.content;
      }

      // Add tracking pixels
      content = await this.addTracking(content, request.id);

      // Process attachments
      const attachments = await this.processAttachments(
        request.attachments || []
      );

      // Send email
      const result = await this.transporter.sendMail({
        from: this.formatSender(request.from),
        to: request.to.map((r) => this.formatRecipient(r)),
        cc: request.cc?.map((r) => this.formatRecipient(r)),
        bcc: request.bcc?.map((r) => this.formatRecipient(r)),
        replyTo: request.replyTo,
        subject: request.subject,
        text: content.text,
        html: content.html,
        attachments,
        headers: {
          "X-Email-ID": request.id,
          "X-Priority": request.priority,
          "X-Tags": request.tags.join(","),
        },
      });

      // Record analytics
      await this.analytics.recordSent(request.id, result.messageId);

      return {
        success: true,
        messageId: result.messageId,
        emailId: request.id,
        timestamp: new Date(),
        recipients: request.to.length,
        error: null,
      };
    } catch (error) {
      await this.analytics.recordError(request.id, error);
      return {
        success: false,
        messageId: null,
        emailId: request.id,
        timestamp: new Date(),
        recipients: 0,
        error: {
          code: error.code || "UNKNOWN_ERROR",
          message: error.message,
        },
      };
    }
  }

  async sendBatch(requests: EmailRequest[]): Promise<EmailResult[]> {
    const results: EmailResult[] = [];
    const batchSize = 10; // Process in batches to avoid overwhelming

    for (let i = 0; i < requests.length; i += batchSize) {
      const batch = requests.slice(i, i + batchSize);
      const batchResults = await Promise.allSettled(
        batch.map((request) => this.send(request))
      );

      batchResults.forEach((result, index) => {
        if (result.status === "fulfilled") {
          results.push(result.value);
        } else {
          results.push({
            success: false,
            messageId: null,
            emailId: batch[index].id,
            timestamp: new Date(),
            recipients: 0,
            error: {
              code: "BATCH_ERROR",
              message: result.reason.message,
            },
          });
        }
      });

      // Add delay between batches to respect rate limits
      if (i + batchSize < requests.length) {
        await this.delay(1000);
      }
    }

    return results;
  }

  private createTransporter(config: EmailConfig): Transporter {
    return nodemailer.createTransporter({
      host: config.smtp.host,
      port: config.smtp.port,
      secure: config.smtp.secure,
      auth: {
        user: config.smtp.username,
        pass: config.smtp.password,
      },
      pool: true,
      maxConnections: 5,
      maxMessages: 100,
      rateDelta: 1000,
      rateLimit: 5,
    });
  }

  private async addTracking(
    content: EmailContent,
    emailId: string
  ): Promise<EmailContent> {
    // Add open tracking pixel
    const trackingPixel = `<img src="${process.env.EMAIL_TRACKING_URL}/open/${emailId}" width="1" height="1" style="display:none;">`;

    // Add click tracking to links
    const htmlWithTracking = content.html.replace(
      /<a([^>]*href=["']([^"']*)["'][^>]*)>/gi,
      (match, attributes, url) => {
        const trackingUrl = `${
          process.env.EMAIL_TRACKING_URL
        }/click/${emailId}?url=${encodeURIComponent(url)}`;
        return `<a${attributes.replace(
          /href=["'][^"']*["']/,
          `href="${trackingUrl}"`
        )}>`;
      }
    );

    return {
      ...content,
      html: htmlWithTracking + trackingPixel,
    };
  }

  private formatSender(from: EmailSender): string {
    return `${from.name} <${from.email}>`;
  }

  private formatRecipient(recipient: EmailRecipient): string {
    return recipient.name
      ? `${recipient.name} <${recipient.email}>`
      : recipient.email;
  }

  private async processAttachments(
    attachments: EmailAttachment[]
  ): Promise<any[]> {
    return Promise.all(
      attachments.map(async (attachment) => {
        if (attachment.type === "url") {
          // Download and attach file
          const response = await fetch(attachment.url);
          const buffer = await response.buffer();

          return {
            filename: attachment.filename,
            content: buffer,
            contentType: attachment.mimeType,
          };
        } else {
          // Direct attachment
          return {
            filename: attachment.filename,
            content: attachment.content,
            contentType: attachment.mimeType,
          };
        }
      })
    );
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
```

### 2. Template Engine

#### Template Processing

```typescript
class TemplateEngine {
  private templates: Map<string, CompiledTemplate> = new Map();
  private handlebars: typeof Handlebars;

  constructor() {
    this.handlebars = Handlebars.create();
    this.registerHelpers();
  }

  async render(templateId: string, data: TemplateData): Promise<RenderedEmail> {
    const template = await this.getCompiledTemplate(
      templateId,
      data.language || "en"
    );

    // Prepare template data with Greek-specific formatting
    const templateData = {
      ...data,
      ...this.getGreekFormatting(data),
      ...this.getCompanyData(data.companyId),
    };

    // Render content
    const html = template.html(templateData);
    const text = template.text(templateData);
    const subject = template.subject(templateData);

    return {
      subject,
      content: {
        html,
        text,
        language: data.language || "en",
        charset: "UTF-8",
      },
    };
  }

  private registerHelpers(): void {
    // Greek currency formatting
    this.handlebars.registerHelper("currency", (amount: number) => {
      return new Intl.NumberFormat("el-GR", {
        style: "currency",
        currency: "EUR",
      }).format(amount);
    });

    // Greek date formatting
    this.handlebars.registerHelper("date", (date: Date) => {
      return new Intl.DateTimeFormat("el-GR", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }).format(date);
    });

    // Greek phone formatting
    this.handlebars.registerHelper("phone", (phone: string) => {
      // Format Greek phone numbers
      const cleaned = phone.replace(/\D/g, "");
      if (cleaned.length === 10) {
        return cleaned.replace(/(\d{3})(\d{3})(\d{4})/, "$1 $2 $3");
      }
      return phone;
    });

    // VAT number formatting
    this.handlebars.registerHelper("vat", (vatNumber: string) => {
      // Format Greek VAT numbers
      const cleaned = vatNumber.replace(/\D/g, "");
      if (cleaned.length === 9) {
        return cleaned.replace(/(\d{3})(\d{3})(\d{3})/, "$1 $2 $3");
      }
      return vatNumber;
    });

    // Conditional helpers
    this.handlebars.registerHelper("ifEquals", function (arg1, arg2, options) {
      return arg1 == arg2 ? options.fn(this) : options.inverse(this);
    });

    this.handlebars.registerHelper("ifGreater", function (arg1, arg2, options) {
      return arg1 > arg2 ? options.fn(this) : options.inverse(this);
    });
  }

  private getGreekFormatting(data: TemplateData): any {
    const now = new Date();

    return {
      currentDate: new Intl.DateTimeFormat("el-GR").format(now),
      currentTime: new Intl.DateTimeFormat("el-GR", {
        hour: "2-digit",
        minute: "2-digit",
      }).format(now),
      timezone: "Europe/Athens",
    };
  }

  private async getCompanyData(companyId: string): Promise<any> {
    // Fetch company data from database
    const company = await this.database.getCompany(companyId);

    return {
      companyName: company.name,
      companyLogo: company.logoUrl,
      companyEmail: company.email,
      companyPhone: company.phone,
      companyAddress: this.formatGreekAddress(company.address),
      vatNumber: company.vatNumber,
      taxOffice: company.taxOffice,
      unsubscribeLink: `${process.env.APP_URL}/unsubscribe/${companyId}`,
      privacyPolicyLink: `${process.env.APP_URL}/privacy`,
    };
  }

  private formatGreekAddress(address: any): string {
    return [
      address.street,
      address.number,
      address.city,
      address.postalCode,
      address.country || "Ελλάδα",
    ]
      .filter(Boolean)
      .join(", ");
  }
}
```

### 3. Queue Management

#### Email Queue

```typescript
class QueueManager {
  private queue: Queue;
  private redis: Redis;

  constructor(redisConfig: RedisConfig) {
    this.redis = new Redis(redisConfig);
    this.queue = new Bull("email-queue", {
      redis: redisConfig,
      defaultJobOptions: {
        removeOnComplete: 100,
        removeOnFail: 50,
        attempts: 3,
        backoff: {
          type: "exponential",
          delay: 2000,
        },
      },
    });

    this.setupJobProcessing();
  }

  async enqueue(
    email: EmailRequest,
    priority: Priority = "normal"
  ): Promise<string> {
    const job = await this.queue.add("send-email", email, {
      priority: this.getPriorityValue(priority),
      delay: 0,
    });

    return job.id.toString();
  }

  async enqueueScheduled(email: EmailRequest, sendAt: Date): Promise<string> {
    const delay = sendAt.getTime() - Date.now();

    if (delay <= 0) {
      return this.enqueue(email);
    }

    const job = await this.queue.add("send-email", email, {
      delay,
      priority: this.getPriorityValue(email.priority),
    });

    return job.id.toString();
  }

  private setupJobProcessing(): void {
    this.queue.process("send-email", 5, async (job) => {
      const email = job.data as EmailRequest;
      const emailService = new EmailService(/* config */);

      try {
        const result = await emailService.send(email);

        if (!result.success) {
          throw new Error(result.error?.message || "Email sending failed");
        }

        return result;
      } catch (error) {
        // Log error for monitoring
        console.error("Email job failed:", error);
        throw error;
      }
    });

    // Job event handlers
    this.queue.on("completed", (job, result) => {
      console.log(`Email job ${job.id} completed successfully`);
    });

    this.queue.on("failed", (job, err) => {
      console.error(`Email job ${job.id} failed:`, err);
    });

    this.queue.on("stalled", (job) => {
      console.warn(`Email job ${job.id} stalled`);
    });
  }

  private getPriorityValue(priority: Priority): number {
    const priorities = {
      critical: 100,
      high: 80,
      normal: 50,
      low: 20,
    };
    return priorities[priority] || 50;
  }

  async getQueueStats(): Promise<QueueStats> {
    const [waiting, active, completed, failed, delayed] = await Promise.all([
      this.queue.getWaiting(),
      this.queue.getActive(),
      this.queue.getCompleted(),
      this.queue.getFailed(),
      this.queue.getDelayed(),
    ]);

    return {
      waiting: waiting.length,
      active: active.length,
      completed: completed.length,
      failed: failed.length,
      delayed: delayed.length,
    };
  }
}
```

## Usage Examples

### 1. Send Invoice Email

```typescript
const emailService = new EmailService();

await emailService.send({
  id: "inv-email-001",
  to: [
    {
      name: "Γιάννης Παπαδόπουλος",
      email: "giannis@example.com",
    },
  ],
  from: {
    name: "Εταιρεία ABC",
    email: "invoices@company.gr",
  },
  subject: "Τιμολόγιο #INV-2024-001",
  templateId: "invoice-greek",
  templateData: {
    language: "el",
    companyId: "comp-123",
    invoiceNumber: "INV-2024-001",
    customerName: "Γιάννης Παπαδόπουλος",
    items: [
      { description: "Υπηρεσία Α", quantity: 1, unitPrice: 100, total: 100 },
      { description: "Υπηρεσία Β", quantity: 2, unitPrice: 50, total: 100 },
    ],
    subtotal: 200,
    vatRate: 24,
    vatAmount: 48,
    total: 248,
    aadeMark: "400009090901",
  },
  attachments: [
    {
      filename: "invoice-INV-2024-001.pdf",
      type: "url",
      url: "https://storage.company.gr/invoices/INV-2024-001.pdf",
      mimeType: "application/pdf",
    },
  ],
  priority: "high",
  tags: ["invoice", "business", "greek"],
  metadata: {
    invoiceId: "inv-001",
    customerId: "cust-123",
    amount: 248,
  },
});
```

### 2. Send AADE Notification

```typescript
await emailService.send({
  id: "aade-notif-001",
  to: [
    {
      name: "Λογιστής Εταιρείας",
      email: "accountant@company.gr",
    },
  ],
  from: {
    name: "Σύστημα ERP",
    email: "system@company.gr",
  },
  subject: "Επιτυχής Υποβολή AADE - Τιμολόγιο #INV-2024-001",
  templateId: "aade-success-greek",
  templateData: {
    language: "el",
    companyId: "comp-123",
    success: true,
    documentType: "Τιμολόγιο Πώλησης",
    documentNumber: "INV-2024-001",
    submissionDate: new Date(),
    aadeMark: "400009090901",
    aadeUid: "abc123def456",
  },
  priority: "high",
  tags: ["aade", "compliance", "success"],
  metadata: {
    documentId: "inv-001",
    aadeSubmissionId: "aade-sub-001",
  },
});
```

### 3. Send Marketing Campaign

```typescript
const customers = await getCustomers();

const campaignEmails = customers.map((customer) => ({
  id: `campaign-${customer.id}`,
  to: [
    {
      name: customer.name,
      email: customer.email,
    },
  ],
  from: {
    name: "Εταιρεία ABC",
    email: "marketing@company.gr",
  },
  subject: "Ειδική Προσφορά - Εκπτώσεις έως 30%",
  templateId: "marketing-offer-greek",
  templateData: {
    language: customer.language || "el",
    companyId: "comp-123",
    customerName: customer.name,
    offerTitle: "Ειδική Προσφορά",
    discountPercentage: 30,
    offerValidUntil: new Date("2024-03-31"),
    offerUrl: `https://shop.company.gr/offers?ref=${customer.id}`,
  },
  priority: "low",
  tags: ["marketing", "campaign", "offers"],
  metadata: {
    campaignId: "campaign-001",
    customerId: customer.id,
    customerSegment: customer.segment,
  },
}));

await emailService.sendBatch(campaignEmails);
```

## Configuration

### Environment Variables

```env
# SMTP Configuration
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_SECURE=false
EMAIL_SMTP_USERNAME=your-email@gmail.com
EMAIL_SMTP_PASSWORD=your-app-password

# Email Service
EMAIL_FROM_NAME=Your Company
EMAIL_FROM_EMAIL=noreply@yourcompany.com
EMAIL_REPLY_TO=support@yourcompany.com

# Queue Configuration
EMAIL_QUEUE_REDIS_URL=redis://localhost:6379
EMAIL_QUEUE_CONCURRENCY=5

# Tracking
EMAIL_TRACKING_URL=https://yourcompany.com/email-tracking

# Templates
EMAIL_TEMPLATE_CDN=https://cdn.yourcompany.com/email-templates
EMAIL_ASSETS_CDN=https://cdn.yourcompany.com/assets

# Analytics
EMAIL_ANALYTICS_DB_URL=postgresql://user:pass@localhost/email_analytics

# Greek Specific
COMPANY_VAT_NUMBER=9
COMPANY_TAX_OFFICE=Α' ΑΘΗΝΩΝ
COMPANY_ADDRESS=Λεωφ. Κηφισίας 123, Αθήνα 11526
```

### Package Dependencies (Python Backend)

```python
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.0

# Email handling
email-validator==2.1.0
aiosmtplib==3.0.1
jinja2==3.1.2
premailer==3.10.0
html2text==2020.1.16

# Queue management
celery==5.3.4
redis==5.0.1
flower==2.0.1

# Greek support
babel==2.13.1
pytz==2023.3
phonenumbers==8.13.25

# Template processing
markdown==3.5.1
weasyprint==60.2  # For PDF generation
pillow==10.1.0

# Database
psycopg2-binary==2.9.9
asyncpg==0.29.0

# Utils
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

This email system provides comprehensive, scalable, and Greek-compliant email capabilities with rich templating, queue management, and analytics features.
