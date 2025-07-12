# 01. Basic Invoicing Module - Unified CRM+ERP Integration

## Document Information

- **Version**: 3.0 (Unified Architecture)
- **Date**: January 2025
- **Module**: Basic Invoicing (€19/month)
- **Dependencies**: Unified Business Entity Management
- **Target Users**: Freelancers, Doctors, Lawyers, Consultants, Small Service Businesses, Engineers, All Professional Services
- **Integration**: Full CRM+ERP integration with 360° business view

## Overview

The Basic Invoicing Module provides comprehensive Greek business document management with full AADE compliance, supporting all 16 Greek document types (παραστατικά). Built on our unified BusinessEntity architecture, this module seamlessly integrates with CRM data to provide complete business relationship visibility and eliminate data silos between customer management and invoicing.

### 🔗 **Unified CRM+ERP Integration**

**Key Advantage**: When you invoice a business, you see their complete relationship history:

- All communications and interactions (CRM data)
- Previous invoices and payment history (ERP data)
- Support tickets and satisfaction scores
- Opportunity pipeline and deal context
- Supplier relationships (if they're also a supplier)

### Supported Document Types (16 Complete Greek Business Documents)

**Legal Documents (Νόμιμα Παραστατικά)** - AADE Submission Required:

- **Sales Invoice** (Τιμολόγιο Πώλησης) - Standard B2B invoicing
- **Receipt** (Απόδειξη Λιανικής Πώλησης) - Retail sales up to €500
- **Credit Note** (Πιστωτικό Τιμολόγιο) - Invoice corrections and returns
- **Debit Note** (Χρεωστικό Τιμολόγιο) - Additional charges to existing invoices
- **Proforma Invoice** (Προτιμολόγιο) - Quotation document (no VAT impact)
- **Delivery Note** (Δελτίο Αποστολής) - Goods delivery tracking
- **Simplified Invoice** (Απλοποιημένο Τιμολόγιο) - Simplified B2B transactions
- **Self-billing** (Αυτο-τιμολόγηση) - Reverse charge scenarios
- **E-Invoice** (Ηλεκτρονικό Τιμολόγιο) - UBL/XML structured format

**Business Workflow Documents** - Internal Business Use:

- **Sales Order** (Δελτίο Παραγγελίας) - Business order management
- **Order Confirmation** (Επιβεβαίωση Παραγγελίας) - Order acceptance
- **Purchase Order** (Παραγγελία Προμηθευτή) - Supplier ordering
- **Request for Quotation** (Αίτημα Προσφοράς) - Quote requests
- **Sales Quotation** (Προσφορά Πώλησης) - Business quotes
- **Return Note** (Δελτίο Επιστροφής) - Returns and exchanges
- **Internal Transfer** (Εσωτερική Μεταφορά) - Inter-location transfers

### Key Features

- **🔗 360° Business Context**: See complete business relationship while invoicing
- **🏢 BusinessEntity Integration**: Single source of truth for all external businesses
- **📋 Complete Document Workflow**: Proper business document relationships (Quote → Order → Invoice → Payment)
- **🇬🇷 Greek VAT Compliance**: Automatic VAT calculations based on business type and location
- **📡 AADE MyDATA Integration**: Real-time submission for legal documents
- **🔧 Professional Services Support**: Enhanced support for service-only businesses
- **📱 QR Code Generation**: Mandatory QR codes on all legal documents
- **📄 Document Templates**: Professional Greek business document templates

---

## 🖥️ Screens & User Interface

### 1. Invoice Dashboard (`/erp/invoicing/dashboard`)

**Purpose**: Overview of invoicing activity with unified business insights

#### UI Components:

```typescript
interface InvoiceDashboardProps {
  dateRange: DateRange;
  companyId: string;
}

const InvoiceDashboard: React.FC<InvoiceDashboardProps> = () => {
  return (
    <DashboardLayout>
      <DashboardHeader title="Invoicing Overview" />

      {/* Key Metrics Cards with Business Context */}
      <MetricsGrid>
        <MetricCard
          title="Total Revenue This Month"
          value="€12,450"
          change="+15.3%"
          trend="up"
          icon={<EuroIcon />}
          drilldown="/businesses?filter=revenue"
        />
        <MetricCard
          title="Outstanding Invoices"
          value="€3,200"
          count="8 invoices"
          businessCount="5 businesses"
          status="warning"
          icon={<ClockIcon />}
          drilldown="/businesses?filter=outstanding"
        />
        <MetricCard
          title="Overdue Payments"
          value="€850"
          count="2 invoices"
          businessCount="2 businesses"
          status="danger"
          icon={<AlertIcon />}
          drilldown="/businesses?filter=overdue"
        />
        <MetricCard
          title="AADE Submissions"
          value="24/25"
          status="success"
          icon={<CheckIcon />}
        />
      </MetricsGrid>

      {/* Quick Actions with Business Context */}
      <QuickActions>
        <QuickActionButton
          label="Create Invoice"
          icon={<PlusIcon />}
          href="/erp/invoicing/create"
          primary
        />
        <QuickActionButton
          label="View All Invoices"
          icon={<ListIcon />}
          href="/erp/invoicing/list"
        />
        <QuickActionButton
          label="Business Health Check"
          icon={<BusinessIcon />}
          href="/businesses?filter=financial_health"
        />
        <QuickActionButton
          label="Payment Follow-ups"
          icon={<PaymentIcon />}
          href="/businesses?filter=payment_required"
        />
      </QuickActions>

      {/* Recent Invoices with Business Context */}
      <RecentInvoicesWidget 
        limit={5} 
        showBusinessContext={true}
        showOpportunityLinks={true}
      />

      {/* Payment Status Chart by Business Segment */}
      <PaymentStatusChart groupBy="businessSegment" />

      {/* Top Businesses by Revenue */}
      <TopBusinessesWidget 
        metric="revenue"
        period="month"
        limit={10}
      />

      {/* AADE Submission Status */}
      <AADEStatusWidget />
    </DashboardLayout>
  );
};
```

### 2. Invoice List (`/erp/invoicing/list`)

**Purpose**: View and manage all invoices with business relationship context

#### UI Components:

```typescript
interface InvoiceListProps {
  filters: InvoiceFilters;
  pagination: PaginationConfig;
}

const InvoiceList: React.FC<InvoiceListProps> = () => {
  const { invoices, loading, error } = useInvoices();
  const { filters, updateFilter } = useInvoiceFilters();

  return (
    <PageLayout>
      <PageHeader
        title="Invoices"
        subtitle="Unified view with complete business context"
        actions={<CreateInvoiceButton href="/erp/invoicing/create" />}
      />

      {/* Enhanced Filters with Business Context */}
      <FilterBar>
        <StatusFilter
          value={filters.status}
          onChange={(status) => updateFilter("status", status)}
          options={[
            { value: "all", label: "All Invoices" },
            { value: "draft", label: "Draft" },
            { value: "sent", label: "Sent" },
            { value: "paid", label: "Paid" },
            { value: "overdue", label: "Overdue" },
          ]}
        />
        <DateRangeFilter
          value={filters.dateRange}
          onChange={(range) => updateFilter("dateRange", range)}
        />
        <BusinessEntityFilter
          value={filters.businessEntityId}
          onChange={(id) => updateFilter("businessEntityId", id)}
          placeholder="Search businesses..."
          showRoles={true}
          showHealthScore={true}
        />
        <BusinessRoleFilter
          value={filters.businessRoles}
          onChange={(roles) => updateFilter("businessRoles", roles)}
          options={["customer", "partner", "government"]}
        />
        <AADEStatusFilter
          value={filters.aadeStatus}
          onChange={(status) => updateFilter("aadeStatus", status)}
        />
      </FilterBar>

      {/* Enhanced Invoice Data Grid with Business Context */}
      <InvoiceDataGrid
        invoices={invoices}
        loading={loading}
        error={error}
        columns={[
          {
            key: "invoiceNumber",
            title: "Invoice #",
            sortable: true,
            render: (invoice) => (
              <Link href={`/erp/invoicing/${invoice.id}`}>
                {invoice.invoiceNumber}
              </Link>
            ),
          },
          {
            key: "businessEntity",
            title: "Business",
            sortable: true,
            render: (invoice) => (
              <BusinessEntityCell 
                business={invoice.businessEntity}
                showRoles={true}
                showHealthScore={true}
                showQuickActions={true}
                href={`/businesses/${invoice.businessEntity.id}`}
              />
            ),
          },
          {
            key: "amount",
            title: "Amount",
            sortable: true,
            align: "right",
            render: (invoice) => (
              <AmountCell 
                amount={invoice.totalAmount}
                currency={invoice.currency}
                paymentStatus={invoice.paymentStatus}
              />
            ),
          },
          {
            key: "issueDate",
            title: "Issue Date",
            sortable: true,
            render: (invoice) => formatDate(invoice.issueDate),
          },
          {
            key: "dueDate",
            title: "Due Date", 
            sortable: true,
            render: (invoice) => (
              <DueDateCell 
                dueDate={invoice.dueDate}
                status={invoice.status}
                showOverdueIndicator={true}
              />
            ),
          },
          {
            key: "status",
            title: "Status",
            render: (invoice) => (
              <StatusBadge 
                status={invoice.status}
                aadeStatus={invoice.aadeStatus}
              />
            ),
          },
          {
            key: "businessContext",
            title: "Context",
            render: (invoice) => (
              <BusinessContextCell
                businessEntity={invoice.businessEntity}
                showOpportunities={true}
                showRecentActivity={true}
                showCommunications={true}
              />
            ),
          },
          {
            key: "actions",
            title: "Actions",
            render: (invoice) => (
              <InvoiceActionsMenu 
                invoice={invoice}
                businessEntity={invoice.businessEntity}
                actions={[
                  "view", "edit", "duplicate", "send", 
                  "viewBusiness", "addNote", "scheduleFollowup"
                ]}
              />
            ),
          },
        ]}
        onRowClick={(invoice) => `/erp/invoicing/${invoice.id}`}
        showBusinessContext={true}
        enableBulkActions={true}
        bulkActions={[
          "send", "markPaid", "exportPDF", "submitAADE", 
          "sendPaymentReminder", "updateBusinessNotes"
        ]}
      />

      {/* Business Insights Panel */}
      <BusinessInsightsPanel
        visible={filters.businessEntityId}
        businessId={filters.businessEntityId}
        showFinancialHealth={true}
        showRecentActivity={true}
        showOpportunities={true}
      />
    </PageLayout>
  );
};
```

### 3. Invoice Creation (`/erp/invoicing/create`)

**Purpose**: Create new invoices with complete business relationship context

#### UI Components:

```typescript
interface InvoiceCreateProps {
  businessEntityId?: string;          // Pre-selected from business view
  opportunityId?: string;             // Pre-selected from opportunity
  quoteId?: string;                   // Converting from quote
}

const InvoiceCreate: React.FC<InvoiceCreateProps> = ({ 
  businessEntityId, 
  opportunityId, 
  quoteId 
}) => {
  const { form, handleSubmit } = useInvoiceForm({
    businessEntityId,
    opportunityId,
    quoteId,
  });

  return (
    <PageLayout>
      <PageHeader 
        title="Create Invoice"
        subtitle="Integrated with complete business context"
      />

      <FormLayout>
        {/* Business Entity Selection with 360° Context */}
        <FormSection title="Business Information">
          <BusinessEntitySelector
            value={form.businessEntityId}
            onChange={(businessId) => form.setBusinessEntityId(businessId)}
            showBusinessCard={true}
            showHealthScore={true}
            showRecentActivity={true}
            showPaymentHistory={true}
            showCreditStatus={true}
            onBusinessSelect={(business) => {
              // Auto-populate invoice data from business
              form.setPaymentTerms(business.paymentTerms);
              form.setDiscountPercentage(business.discountPercentage);
              form.setCurrency(business.preferredCurrency || "EUR");
            }}
          />
        
          {form.businessEntityId && (
            <BusinessContextCard
              businessId={form.businessEntityId}
              showMetrics={["totalSales", "outstandingAmount", "paymentHistory"]}
              showAlerts={["creditLimit", "overduePayments", "aadeIssues"]}
              showQuickLinks={[
                { label: "View Business", href: `/businesses/${form.businessEntityId}` },
                { label: "Recent Communications", href: `/businesses/${form.businessEntityId}/communications` },
                { label: "Payment History", href: `/businesses/${form.businessEntityId}/payments` }
              ]}
            />
          )}
        </FormSection>

        {/* Document Type and Settings */}
        <FormSection title="Document Information">
          <DocumentTypeSelector
            value={form.documentType}
            onChange={(type) => form.setDocumentType(type)}
            businessContext={form.businessEntity}
            showLegalRequirements={true}
            showAADERequirements={true}
          />
        
          <InvoiceNumberGenerator
            series={form.series}
            sequence={form.sequenceNumber}
            onChange={(number) => form.setInvoiceNumber(number)}
            businessEntityType={form.businessEntity?.entityType}
          />
        
          <DatePickers
            issueDate={form.issueDate}
            dueDate={form.dueDate}
            serviceDate={form.serviceDate}
            onChange={(dates) => form.setDates(dates)}
            paymentTerms={form.businessEntity?.paymentTerms}
          />
        </FormSection>

        {/* Line Items with Product/Service Integration */}
        <FormSection title="Invoice Items">
          <InvoiceLineItems
            items={form.lineItems}
            onChange={(items) => form.setLineItems(items)}
            businessEntity={form.businessEntity}
            showProductSuggestions={true}
            showServiceTemplates={true}
            showPricingHistory={true}
            enableBulkActions={true}
            greekVATCalculation={true}
          />
        
          <ProductServiceSelector
            businessEntityId={form.businessEntityId}
            showRecentPurchases={true}
            showPricingHistory={true}
            showBundleOptions={true}
            onProductSelect={(product) => form.addLineItem(product)}
          />
        </FormSection>

        {/* Greek VAT and Compliance */}
        <FormSection title="Greek Tax Compliance">
          <GreekVATCalculator
            lineItems={form.lineItems}
            businessEntity={form.businessEntity}
            documentType={form.documentType}
            onChange={(vatData) => form.setVATData(vatData)}
            showBreakdown={true}
            validateCompliance={true}
          />
        
          <AADEComplianceChecker
            documentType={form.documentType}
            businessEntity={form.businessEntity}
            showRequirements={true}
            autoValidate={true}
          />
        </FormSection>

        {/* Totals and Payment Information */}
        <FormSection title="Payment Terms">
          <InvoiceTotals
            lineItems={form.lineItems}
            discountPercentage={form.discountPercentage}
            vatData={form.vatData}
            currency={form.currency}
            showBreakdown={true}
          />
        
          <PaymentTermsSelector
            businessEntity={form.businessEntity}
            value={form.paymentTerms}
            onChange={(terms) => form.setPaymentTerms(terms)}
            showCreditStatus={true}
            showHistoricalBehavior={true}
          />
        </FormSection>

        {/* Notes and Attachments */}
        <FormSection title="Additional Information">
          <NotesField
            value={form.notes}
            onChange={(notes) => form.setNotes(notes)}
            showTemplates={true}
            businessContext={form.businessEntity}
          />
        
          <AttachmentsField
            files={form.attachments}
            onChange={(files) => form.setAttachments(files)}
            allowedTypes={["pdf", "doc", "docx", "jpg", "png"]}
            maxSize="10MB"
          />
        </FormSection>

        {/* Form Actions */}
        <FormActions>
          <SaveDraftButton 
            onClick={() => handleSubmit("draft")}
            disabled={!form.isValid}
          />
          <SendInvoiceButton
            onClick={() => handleSubmit("send")}
            disabled={!form.isComplete}
            businessEntity={form.businessEntity}
          />
          <PreviewButton
            onClick={() => form.preview()}
            disabled={!form.hasItems}
          />
        </FormActions>
      </FormLayout>
    </PageLayout>
  );
};
```

### 4. Invoice Detail View (`/erp/invoicing/:id`)

**Purpose**: Complete invoice view with full business relationship context

#### UI Components:

```typescript
interface InvoiceDetailProps {
  invoiceId: string;
}

const InvoiceDetail: React.FC<InvoiceDetailProps> = ({ invoiceId }) => {
  const { invoice, business, loading } = useInvoiceWithBusiness(invoiceId);

  return (
    <PageLayout>
      <PageHeader
        title={`Invoice ${invoice.invoiceNumber}`}
        subtitle={`${business.displayName} • ${invoice.documentType}`}
        actions={
          <InvoiceActions
            invoice={invoice}
            business={business}
            actions={[
              "edit", "duplicate", "send", "markPaid", "generatePDF",
              "submitAADE", "viewBusiness", "addNote", "scheduleFollowup"
            ]}
          />
        }
      />

      <DetailLayout>
        {/* Invoice Document Panel */}
        <MainPanel>
          <InvoiceDocument
            invoice={invoice}
            business={business}
            showQRCode={true}
            showAADEStatus={true}
            enableActions={true}
          />
        
          <InvoiceTimeline
            invoice={invoice}
            showBusinessContext={true}
            showCommunications={true}
            showPayments={true}
            showAADEEvents={true}
          />
        </MainPanel>

        {/* Business Context Sidebar */}
        <SidePanel>
          <BusinessContextPanel
            business={business}
            currentInvoice={invoice}
            sections={[
              "overview",
              "contacts", 
              "recentActivity",
              "paymentHistory",
              "openInvoices",
              "opportunities",
              "communications"
            ]}
          />
        
          <QuickActionsPanel
            business={business}
            invoice={invoice}
            actions={[
              { label: "Send Payment Reminder", action: "sendReminder" },
              { label: "Schedule Follow-up", action: "scheduleTask" },
              { label: "Add Business Note", action: "addNote" },
              { label: "View All Invoices", href: `/businesses/${business.id}/invoices` },
              { label: "View Business Profile", href: `/businesses/${business.id}` }
            ]}
          />
        
          <RelatedInvoicesPanel
            businessId={business.id}
            currentInvoiceId={invoice.id}
            showStatus={true}
            showAmounts={true}
            limit={10}
          />
        </SidePanel>
      </DetailLayout>
    </PageLayout>
  );
};
```

### 5. Payment Tracking (`/erp/invoicing/payments`)

**Purpose**: Track and manage invoice payments

#### UI Components:

```typescript
const PaymentTracking: React.FC = () => {
  const { payments, loading } = usePayments();
  const { overdueInvoices } = useOverdueInvoices();

  return (
    <PageLayout>
      <PageHeader title="Payment Tracking" />

      {/* Payment Overview */}
      <PaymentOverview>
        <OverviewCard
          title="Total Outstanding"
          amount="€8,450"
          count="15 invoices"
          status="warning"
        />
        <OverviewCard
          title="Overdue"
          amount="€1,250"
          count="3 invoices"
          status="danger"
        />
        <OverviewCard
          title="Due This Week"
          amount="€2,100"
          count="5 invoices"
          status="info"
        />
      </PaymentOverview>

      {/* Overdue Invoices Alert */}
      {overdueInvoices.length > 0 && (
        <OverdueAlert
          count={overdueInvoices.length}
          totalAmount={overdueInvoices.reduce(
            (sum, inv) => sum + inv.amountDue,
            0
          )}
        />
      )}

      {/* Payment List */}
      <PaymentList
        payments={payments}
        loading={loading}
        columns={[
          "invoice",
          "customer",
          "dueDate",
          "amount",
          "status",
          "actions",
        ]}
      />
    </PageLayout>
  );
};
```

---

## 🔗 API Endpoints

### Invoice Management APIs

```typescript
// GET /api/erp/invoicing/invoices
interface GetInvoicesRequest {
  page?: number;
  limit?: number;
  status?: InvoiceStatus[];
  customerId?: string;
  dateFrom?: Date;
  dateTo?: Date;
  aadeStatus?: AADEStatus[];
}

interface GetInvoicesResponse {
  invoices: Invoice[];
  pagination: PaginationInfo;
  summary: InvoiceSummary;
}

// POST /api/erp/invoicing/invoices
interface CreateInvoiceRequest {
  customerId: string;
  items: InvoiceItem[];
  dueDate?: Date;
  paymentTerms?: string;
  notes?: string;
  customerNotes?: string;
  saveAsDraft?: boolean;
}

interface CreateInvoiceResponse {
  invoice: Invoice;
  pdf?: string; // Base64 PDF if not draft
  aadeSubmission?: AADESubmissionResult;
}

// GET /api/erp/invoicing/invoices/:id
interface GetInvoiceResponse {
  invoice: Invoice;
  pdf: string; // Base64 PDF
  timeline: InvoiceActivity[];
}

// PUT /api/erp/invoicing/invoices/:id
interface UpdateInvoiceRequest {
  items?: InvoiceItem[];
  dueDate?: Date;
  notes?: string;
  customerNotes?: string;
}

// POST /api/erp/invoicing/invoices/:id/send
interface SendInvoiceRequest {
  email?: string;
  sendCopy?: boolean;
  customMessage?: string;
}

// POST /api/erp/invoicing/invoices/:id/aade-submit
interface AADESubmitResponse {
  success: boolean;
  mark?: string;
  qrCode?: string;
  submissionDate: Date;
  errors?: AADEError[];
}
```

### Payment APIs

```typescript
// GET /api/erp/invoicing/payments
interface GetPaymentsRequest {
  invoiceId?: string;
  customerId?: string;
  dateFrom?: Date;
  dateTo?: Date;
  status?: PaymentStatus[];
}

// POST /api/erp/invoicing/payments
interface CreatePaymentRequest {
  invoiceId: string;
  amount: number;
  paymentDate: Date;
  paymentMethod: PaymentMethod;
  referenceNumber?: string;
  notes?: string;
}

// GET /api/erp/invoicing/overdue
interface GetOverdueInvoicesResponse {
  invoices: OverdueInvoice[];
  totalAmount: number;
  oldestDays: number;
}
```

### Greek Compliance APIs

```typescript
// GET /api/erp/invoicing/vat-rates
interface GetVATRatesResponse {
  rates: GreekVATRate[];
  specialRules: VATSpecialRule[];
  businessTypeExemptions: VATExemption[];
}

// POST /api/erp/invoicing/vat-calculate
interface CalculateVATRequest {
  items: InvoiceItem[];
  customerId: string;
  businessType: BusinessType;
  invoiceDate: Date;
}

interface CalculateVATResponse {
  subtotal: number;
  vatBreakdown: VATBreakdown[];
  total: number;
  exemptions: VATExemption[];
}

// GET /api/erp/invoicing/aade-status
interface GetAADEStatusResponse {
  pendingSubmissions: number;
  failedSubmissions: AADEFailure[];
  dailyLimit: AADELimit;
}
```

---

## 🗃️ Data Models

### Enhanced Invoice Model - Supporting 16 Greek Document Types

```typescript
interface Invoice {
  id: string;
  invoiceNumber: string;
  series: string;
  sequenceNumber: number;
  
  // Company and customer
  companyId: string;
  customerId: string;
  customer: Customer; // From CRM

  // Document type and classification
  invoiceType: InvoiceType; // 16 Greek document types
  status: InvoiceStatus;
  
  // Greek business compliance
  isLegalDocument: boolean; // Legal document (requires AADE) vs business workflow
  affectsVat: boolean; // Does this document affect VAT calculations
  affectsInventory: boolean; // Does this document affect inventory

  // Document dates
  issueDate: Date;
  dueDate: Date;
  serviceDate?: Date; // Date of service delivery
  deliveryDate?: Date; // Actual delivery date

  // Document workflow - related documents
  parentDocumentId?: string; // Parent document (e.g., Order for Invoice)
  originalDocumentId?: string; // Original document for corrections
  
  // Items
  items: InvoiceItem[];

  // Financial calculations
  subtotal: number;
  totalVatAmount: number;
  totalDiscountAmount: number;
  totalExtraCharges: number;
  totalGross: number;
  totalNet: number;
  currency: string;

  // Payment information
  paymentStatus: PaymentStatus;
  amountPaid: number;
  amountDue: number;
  paymentTerms: string;
  paymentMethod?: PaymentMethod;

  // Greek AADE compliance
  aadeStatus: AADEStatus;
  aadeSubmissionDate?: Date;
  aadeMark?: string; // MyDATA submission mark
  qrCode?: string; // QR code for legal documents
  aadeClassification?: string; // AADE classification
  greekVATInfo: GreekVATInfo;

  // Document relationships and workflow
  documentWorkflow: DocumentWorkflow;
  
  // Multi-language support
  language: "greek" | "english";
  
  // Additional information
  notes?: string;
  customerNotes?: string;
  internalNotes?: string;
  
  // Terms and conditions
  termsAndConditions?: string;
  
  // Delivery information
  deliveryAddress?: Address;
  deliveryMethod?: string;
  
  // Greek business fields
  greekBusinessFields: GreekBusinessFields;

  // Audit trail
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  lastModifiedBy: string;

  // Relations
  payments: Payment[];
  activities: InvoiceActivity[];
  attachments: DocumentAttachment[];
}

// 16 Greek Document Types
type InvoiceType = 
  // Legal documents (νόμιμα παραστατικά)
  | "sales_invoice"           // Τιμολόγιο Πώλησης
  | "receipt"                 // Απόδειξη Λιανικής Πώλησης
  | "credit_note"             // Πιστωτικό Τιμολόγιο
  | "debit_note"              // Χρεωστικό Τιμολόγιο
  | "proforma"                // Προτιμολόγιο
  | "delivery_note"           // Δελτίο Αποστολής
  | "simplified_invoice"      // Απλοποιημένο Τιμολόγιο
  | "self_billing"            // Αυτο-τιμολόγηση
  | "e_invoice"               // Ηλεκτρονικό Τιμολόγιο
  // Business workflow documents
  | "sales_order"             // Δελτίο Παραγγελίας
  | "order_confirmation"      // Επιβεβαίωση Παραγγελίας
  | "purchase_order"          // Παραγγελία Προμηθευτή
  | "request_for_quotation"   // Αίτημα Προσφοράς
  | "sales_quotation"         // Προσφορά Πώλησης
  | "return_note"             // Δελτίο Επιστροφής
  | "internal_transfer";      // Εσωτερική Μεταφορά

interface InvoiceItem {
  id: string;
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;

  // Product/Service reference
  productId?: string;
  product?: Product;
  
  // VAT information
  vatRate: number;
  vatAmount: number;
  vatExempt: boolean;
  vatExemptionReason?: string;
  vatCategory: VatCategory;

  // Service-specific fields
  serviceId?: string;
  duration?: number; // For hourly services
  serviceDate?: Date;
  professionalType?: string;

  // Discount and charges
  discountPercentage?: number;
  discountAmount?: number;
  extraCharges?: number;
  
  // Greek business compliance
  greekTaxCategory: GreekTaxCategory;
  islandVatReduction: boolean;
  
  // Unit of measure
  unitOfMeasure: string;
  
  // Custom fields
  customFields: Record<string, any>;
}

interface DocumentWorkflow {
  // Document relationships
  isParentDocument: boolean;
  hasChildDocuments: boolean;
  childDocumentIds: string[];
  
  // Workflow stage
  workflowStage: WorkflowStage;
  nextAllowedActions: string[];
  
  // Approval workflow
  requiresApproval: boolean;
  approvalStatus?: "pending" | "approved" | "rejected";
  approvedBy?: string;
  approvedAt?: Date;
  
  // Version control
  version: number;
  isCurrentVersion: boolean;
  previousVersionId?: string;
}

type WorkflowStage = 
  | "draft"
  | "pending_approval"
  | "approved"
  | "sent"
  | "accepted"
  | "in_progress"
  | "completed"
  | "cancelled";

interface GreekBusinessFields {
  // Professional service fields
  professionalChamberRegistration?: string;
  professionalType?: string;
  
  // AADE specific
  aadeTransactionId?: string;
  invoiceVariationType?: string;
  
  // Tax office information
  issuerTaxOffice: string;
  customerTaxOffice?: string;
  
  // Special business scenarios
  isB2B: boolean;
  isB2C: boolean;
  isB2G: boolean; // Business to Government
  
  // Island VAT reduction
  islandReduction: boolean;
  islandReducionPercentage?: number;
  
  // Special tax scenarios
  reverseChargeApplicable: boolean;
  marginSchemeApplicable: boolean;
  
  // Export/import
  isExport: boolean;
  isImport: boolean;
  countryOfOrigin?: string;
  countryOfDestination?: string;
}

type InvoiceStatus =
  | "draft"
  | "pending_approval"
  | "approved"
  | "sent"
  | "viewed"
  | "accepted"
  | "rejected"
  | "cancelled"
  | "completed";

type PaymentStatus = "unpaid" | "partially_paid" | "paid" | "overdue";

type AADEStatus = "not_required" | "pending" | "submitted" | "accepted" | "rejected" | "error";

type VatCategory = "standard" | "reduced_1" | "reduced_2" | "zero" | "exempt";

type PaymentMethod = "cash" | "bank_transfer" | "credit_card" | "debit_card" | "cheque" | "installments";
```

### Payment Model

```typescript
interface Payment {
  id: string;
  invoiceId: string;

  // Payment Details
  amount: number;
  paymentDate: Date;
  paymentMethod: PaymentMethod;
  referenceNumber?: string;

  // Bank Details (for transfers)
  bankAccount?: string;
  transactionId?: string;

  // Status
  status: PaymentStatus;
  verifiedDate?: Date;
  verifiedBy?: string;

  // Notes
  notes?: string;

  // Audit
  createdAt: Date;
  createdBy: string;
}

type PaymentMethod =
  | "cash"
  | "bank_transfer"
  | "credit_card"
  | "debit_card"
  | "cheque";
```

### Greek VAT Models

```typescript
interface GreekVATInfo {
  // Business VAT Info
  businessVATNumber: string;
  businessVATRegistered: boolean;

  // Customer VAT Info
  customerVATNumber?: string;
  customerVATRegistered: boolean;

  // VAT Calculation
  vatCalculationMethod: "standard" | "reverse_charge" | "exempt";
  vatBreakdown: VATBreakdown[];

  // Special Rules
  islandReduction: boolean;
  professionalExemption: boolean;

  // AADE Specific
  aadeClassification: string;
  aadeDocumentType: string;
}

interface VATBreakdown {
  rate: number;
  netAmount: number;
  vatAmount: number;
  category: GreekVATCategory;
}

type GreekVATCategory =
  | "standard_24"
  | "reduced_13"
  | "super_reduced_6"
  | "exempt_0";

interface GreekVATRate {
  rate: number;
  category: GreekVATCategory;
  description: string;
  applicableBusinessTypes: BusinessType[];
  effectiveFrom: Date;
  effectiveTo?: Date;
}
```

---

## 🧩 UI Components

### Reusable Invoice Components

```typescript
// Invoice Form Components
export const InvoiceForm: React.FC<InvoiceFormProps>;
export const InvoiceItemsEditor: React.FC<InvoiceItemsEditorProps>;
export const CustomerSelector: React.FC<CustomerSelectorProps>;
export const GreekVATCalculator: React.FC<GreekVATCalculatorProps>;
export const AADESubmissionWidget: React.FC<AADESubmissionWidgetProps>;

// Display Components
export const InvoicePreview: React.FC<InvoicePreviewProps>;
export const InvoicePDFViewer: React.FC<InvoicePDFViewerProps>;
export const PaymentStatus: React.FC<PaymentStatusProps>;
export const AADEStatusBadge: React.FC<AADEStatusBadgeProps>;
export const QRCodeDisplay: React.FC<QRCodeDisplayProps>;

// List Components
export const InvoiceDataGrid: React.FC<InvoiceDataGridProps>;
export const PaymentList: React.FC<PaymentListProps>;
export const InvoiceTimeline: React.FC<InvoiceTimelineProps>;

// Filter Components
export const InvoiceFilters: React.FC<InvoiceFiltersProps>;
export const DateRangeFilter: React.FC<DateRangeFilterProps>;
export const StatusFilter: React.FC<StatusFilterProps>;
export const AADEStatusFilter: React.FC<AADEStatusFilterProps>;

// Action Components
export const InvoiceActionMenu: React.FC<InvoiceActionMenuProps>;
export const SendInvoiceButton: React.FC<SendInvoiceButtonProps>;
export const RecordPaymentButton: React.FC<RecordPaymentButtonProps>;
export const SubmitToAADEButton: React.FC<SubmitToAADEButtonProps>;
```

### Greek-Specific Components

```typescript
// Greek Formatting
export const GreekDateDisplay: React.FC<{ date: Date }>;
export const GreekCurrencyDisplay: React.FC<{ amount: number }>;
export const GreekAddressDisplay: React.FC<{ address: GreekAddress }>;
export const AFMDisplay: React.FC<{ afm: string; verified?: boolean }>;

// Greek VAT
export const VATRateSelector: React.FC<VATRateSelectorProps>;
export const VATBreakdownTable: React.FC<VATBreakdownTableProps>;
export const VATExemptionIndicator: React.FC<VATExemptionIndicatorProps>;

// AADE Integration
export const AADEComplianceWidget: React.FC<AADEComplianceWidgetProps>;
export const AADEErrorDisplay: React.FC<AADEErrorDisplayProps>;
export const MyDATAStatusIndicator: React.FC<MyDATAStatusIndicatorProps>;
```

---

## 🪝 Custom Hooks

### Invoice Management Hooks

```typescript
// Invoice CRUD
export const useInvoices = (filters?: InvoiceFilters) => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Implementation...

  return {
    invoices,
    loading,
    error,
    refetch,
    createInvoice,
    updateInvoice,
  };
};

export const useInvoice = (invoiceId: string) => {
  // Single invoice management
  return {
    invoice,
    loading,
    error,
    update,
    delete: deleteInvoice,
    sendToCustomer,
    submitToAADE,
  };
};

export const useInvoiceForm = (initialData?: Partial<Invoice>) => {
  const [form, setForm] = useState<InvoiceFormData>(initialData || {});
  const [errors, setErrors] = useState<FormErrors>({});

  // Form validation
  const validateForm = useCallback(() => {
    const newErrors: FormErrors = {};

    if (!form.customerId) {
      newErrors.customer = "Customer is required";
    }

    if (!form.items || form.items.length === 0) {
      newErrors.items = "At least one item is required";
    }

    // Greek-specific validation
    if (
      form.customer?.greekTaxInfo?.vatRegistered &&
      !form.customer.greekTaxInfo.afm
    ) {
      newErrors.customerVAT =
        "VAT number required for VAT-registered customers";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [form]);

  const handleSubmit = useCallback(
    async (action: "draft" | "send") => {
      if (!validateForm()) return;

      try {
        if (action === "draft") {
          return await saveInvoiceDraft(form);
        } else {
          return await createAndSendInvoice(form);
        }
      } catch (error) {
        setErrors({ submit: error.message });
      }
    },
    [form, validateForm]
  );

  return {
    form,
    setForm,
    errors,
    isValid: Object.keys(errors).length === 0,
    handleSubmit,
    validateForm,
  };
};
```

### Payment Hooks

```typescript
export const usePayments = (filters?: PaymentFilters) => {
  return {
    payments,
    loading,
    error,
    createPayment,
    updatePayment,
  };
};

export const useOverdueInvoices = () => {
  return {
    overdueInvoices,
    totalOverdue,
    oldestOverdue,
    sendReminders,
  };
};

export const usePaymentTracking = (invoiceId: string) => {
  return {
    paymentHistory,
    paymentStatus,
    recordPayment,
    markAsPaid,
  };
};
```

### Greek Compliance Hooks

```typescript
export const useGreekVATRates = () => {
  const [rates, setRates] = useState<GreekVATRate[]>([]);

  useEffect(() => {
    // Load current Greek VAT rates
    loadGreekVATRates().then(setRates);
  }, []);

  const calculateVAT = useCallback(
    (items: InvoiceItem[], customer: Customer) => {
      // Greek VAT calculation logic
      return calculateGreekVAT(items, customer, rates);
    },
    [rates]
  );

  return { rates, calculateVAT };
};

export const useAADEIntegration = () => {
  const submitToAADE = useCallback(async (invoice: Invoice) => {
    try {
      const result = await aadeAPI.submitInvoice(invoice);
      return result;
    } catch (error) {
      throw new AADEError(error.message);
    }
  }, []);

  const checkAADEStatus = useCallback(async (invoiceId: string) => {
    return await aadeAPI.checkStatus(invoiceId);
  }, []);

  return {
    submitToAADE,
    checkAADEStatus,
    generateQRCode,
    validateAADEData,
  };
};

export const useGreekBusinessRules = (businessType: BusinessType) => {
  const [rules, setRules] = useState<GreekBusinessRule[]>([]);

  useEffect(() => {
    loadBusinessRules(businessType).then(setRules);
  }, [businessType]);

  const validateInvoice = useCallback(
    (invoice: Invoice) => {
      return rules.map((rule) => rule.validate(invoice));
    },
    [rules]
  );

  return { rules, validateInvoice };
};
```

---

## 🌐 Context Providers

### Invoice Context

```typescript
interface InvoiceContextValue {
  // Current invoice being edited
  currentInvoice: Invoice | null;
  setCurrentInvoice: (invoice: Invoice | null) => void;

  // Form state
  isEditing: boolean;
  setIsEditing: (editing: boolean) => void;

  // Settings
  defaultPaymentTerms: string;
  defaultDueDays: number;

  // Greek settings
  businessVATNumber: string;
  defaultVATRate: number;
  aadeEnabled: boolean;
}

export const InvoiceProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentInvoice, setCurrentInvoice] = useState<Invoice | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  // Load settings from company configuration
  const { company } = useCompany();

  const value: InvoiceContextValue = {
    currentInvoice,
    setCurrentInvoice,
    isEditing,
    setIsEditing,
    defaultPaymentTerms: company.defaultPaymentTerms || "30_days",
    defaultDueDays: company.defaultDueDays || 30,
    businessVATNumber: company.greekTaxInfo.afm,
    defaultVATRate: company.defaultVATRate || 24,
    aadeEnabled: company.aadeEnabled || true,
  };

  return (
    <InvoiceContext.Provider value={value}>{children}</InvoiceContext.Provider>
  );
};

export const useInvoiceContext = () => {
  const context = useContext(InvoiceContext);
  if (!context) {
    throw new Error("useInvoiceContext must be used within InvoiceProvider");
  }
  return context;
};
```

### Greek Compliance Context

```typescript
interface GreekComplianceContextValue {
  // VAT Configuration
  vatRates: GreekVATRate[];
  businessType: BusinessType;
  vatExemptions: VATExemption[];

  // AADE Configuration
  aadeEnabled: boolean;
  aadeCredentials: AADECredentials;
  aadeEnvironment: "production" | "sandbox";

  // Business Rules
  businessRules: GreekBusinessRule[];
  complianceChecks: ComplianceCheck[];

  // Functions
  calculateVAT: (items: InvoiceItem[], customer: Customer) => VATCalculation;
  validateCompliance: (invoice: Invoice) => ComplianceResult;
  submitToAADE: (invoice: Invoice) => Promise<AADEResult>;
}

export const GreekComplianceProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const { company } = useCompany();
  const [vatRates, setVatRates] = useState<GreekVATRate[]>([]);
  const [businessRules, setBusinessRules] = useState<GreekBusinessRule[]>([]);

  useEffect(() => {
    // Load Greek compliance data
    Promise.all([
      loadGreekVATRates(),
      loadGreekBusinessRules(company.businessType),
    ]).then(([rates, rules]) => {
      setVatRates(rates);
      setBusinessRules(rules);
    });
  }, [company.businessType]);

  const calculateVAT = useCallback(
    (items: InvoiceItem[], customer: Customer) => {
      return calculateGreekVAT(items, customer, vatRates, company.businessType);
    },
    [vatRates, company.businessType]
  );

  const validateCompliance = useCallback(
    (invoice: Invoice) => {
      return businessRules.map((rule) => rule.validate(invoice));
    },
    [businessRules]
  );

  const submitToAADE = useCallback(
    async (invoice: Invoice) => {
      if (!company.aadeEnabled) {
        throw new Error("AADE integration not enabled");
      }

      return await aadeAPI.submitInvoice(invoice, company.aadeCredentials);
    },
    [company.aadeEnabled, company.aadeCredentials]
  );

  const value: GreekComplianceContextValue = {
    vatRates,
    businessType: company.businessType,
    vatExemptions: company.vatExemptions || [],
    aadeEnabled: company.aadeEnabled || false,
    aadeCredentials: company.aadeCredentials,
    aadeEnvironment: company.aadeEnvironment || "sandbox",
    businessRules,
    complianceChecks: [],
    calculateVAT,
    validateCompliance,
    submitToAADE,
  };

  return (
    <GreekComplianceContext.Provider value={value}>
      {children}
    </GreekComplianceContext.Provider>
  );
};
```

---

## 🧪 Testing Strategy

### Unit Tests

```typescript
// Invoice form validation tests
describe("InvoiceForm", () => {
  test("validates required customer selection", () => {
    const { form } = renderInvoiceForm();
    expect(form.validateForm()).toBe(false);
    expect(form.errors.customer).toBe("Customer is required");
  });

  test("validates Greek VAT for VAT-registered customers", () => {
    const vatRegisteredCustomer = {
      id: "1",
      greekTaxInfo: { vatRegistered: true, afm: "" },
    };

    const { form } = renderInvoiceForm({ customer: vatRegisteredCustomer });
    expect(form.validateForm()).toBe(false);
    expect(form.errors.customerVAT).toBeDefined();
  });
});

// Greek VAT calculation tests
describe("GreekVATCalculation", () => {
  test("applies correct VAT rate for standard products", () => {
    const items = [
      { description: "Product", unitPrice: 100, quantity: 1, vatRate: 24 },
    ];

    const result = calculateGreekVAT(items, customer, vatRates);
    expect(result.vatAmount).toBe(24);
    expect(result.total).toBe(124);
  });

  test("applies VAT exemption for medical services", () => {
    const medicalItems = [
      {
        description: "Consultation",
        unitPrice: 50,
        quantity: 1,
        vatExempt: true,
      },
    ];

    const result = calculateGreekVAT(medicalItems, patient, vatRates);
    expect(result.vatAmount).toBe(0);
    expect(result.total).toBe(50);
  });
});
```

### Integration Tests

```typescript
// AADE integration tests
describe("AADE Integration", () => {
  test("successfully submits invoice to AADE", async () => {
    const invoice = createTestInvoice();
    const result = await submitToAADE(invoice);

    expect(result.success).toBe(true);
    expect(result.mark).toBeDefined();
    expect(result.qrCode).toBeDefined();
  });

  test("handles AADE validation errors", async () => {
    const invalidInvoice = createInvalidInvoice();

    await expect(submitToAADE(invalidInvoice)).rejects.toThrow(
      "AADE validation failed"
    );
  });
});

// Payment tracking tests
describe("Payment Tracking", () => {
  test("updates invoice status when payment recorded", async () => {
    const invoice = await createTestInvoice();
    const payment = await recordPayment(invoice.id, invoice.total);

    const updatedInvoice = await getInvoice(invoice.id);
    expect(updatedInvoice.paymentStatus).toBe("paid");
    expect(updatedInvoice.amountPaid).toBe(invoice.total);
  });
});
```

---

## 📋 Implementation Checklist

### Phase 1: Core Invoicing (Week 1-2)

- [ ] Invoice data models and database schema
- [ ] Basic invoice CRUD APIs
- [ ] Invoice creation form with customer selection
- [ ] Invoice list and detail views
- [ ] PDF generation with Greek formatting

### Phase 2: Greek Compliance (Week 3-4)

- [ ] Greek VAT calculation engine
- [ ] AADE MyDATA integration
- [ ] QR code generation
- [ ] VAT rate management
- [ ] Business type validation rules

### Phase 3: Payment Tracking (Week 5-6)

- [ ] Payment recording system
- [ ] Payment status tracking
- [ ] Overdue invoice detection
- [ ] Payment reminders
- [ ] Financial reporting basics

### Phase 4: Advanced Features (Week 7-8)

- [ ] Invoice templates and automation
- [ ] Bulk operations
- [ ] Advanced filtering and search
- [ ] Email integration
- [ ] Mobile responsiveness

### Phase 5: Testing & Polish (Week 9-10)

- [ ] Comprehensive testing suite
- [ ] Performance optimization
- [ ] Error handling and validation
- [ ] Documentation and help system
- [ ] User acceptance testing

This Basic Invoicing Module provides a solid foundation for service-based businesses while maintaining the flexibility to integrate with other ERP modules as businesses grow.
