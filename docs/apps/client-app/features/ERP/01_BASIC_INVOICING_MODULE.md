# 01. Basic Invoicing Module - Technical Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Module**: Basic Invoicing (€19/month)
- **Dependencies**: None (uses shared CRM customer data)
- **Target Users**: Freelancers, Doctors, Lawyers, Consultants, Small Service Businesses

## Overview

The Basic Invoicing Module provides essential invoicing functionality with full Greek compliance, designed for service-based businesses that need simple yet professional billing capabilities. This module integrates seamlessly with CRM customer data while maintaining independence for businesses that only need invoicing.

---

## 🖥️ Screens & User Interface

### 1. Invoice Dashboard (`/erp/invoicing/dashboard`)

**Purpose**: Overview of invoicing activity and key metrics

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

      {/* Key Metrics Cards */}
      <MetricsGrid>
        <MetricCard
          title="Total Revenue This Month"
          value="€12,450"
          change="+15.3%"
          trend="up"
          icon={<EuroIcon />}
        />
        <MetricCard
          title="Outstanding Invoices"
          value="€3,200"
          count="8 invoices"
          status="warning"
          icon={<ClockIcon />}
        />
        <MetricCard
          title="Overdue Payments"
          value="€850"
          count="2 invoices"
          status="danger"
          icon={<AlertIcon />}
        />
        <MetricCard
          title="AADE Submissions"
          value="24/25"
          status="success"
          icon={<CheckIcon />}
        />
      </MetricsGrid>

      {/* Quick Actions */}
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
          label="Payment Tracking"
          icon={<PaymentIcon />}
          href="/erp/invoicing/payments"
        />
      </QuickActions>

      {/* Recent Invoices */}
      <RecentInvoicesWidget limit={5} />

      {/* Payment Status Chart */}
      <PaymentStatusChart />

      {/* AADE Submission Status */}
      <AADEStatusWidget />
    </DashboardLayout>
  );
};
```

### 2. Invoice List (`/erp/invoicing/list`)

**Purpose**: View and manage all invoices

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
        actions={<CreateInvoiceButton href="/erp/invoicing/create" />}
      />

      {/* Filters */}
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
        <CustomerFilter
          value={filters.customerId}
          onChange={(id) => updateFilter("customerId", id)}
        />
        <AADEStatusFilter
          value={filters.aadeStatus}
          onChange={(status) => updateFilter("aadeStatus", status)}
        />
      </FilterBar>

      {/* Invoice Data Grid */}
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
            key: "customer",
            title: "Customer",
            render: (invoice) => <CustomerCell customer={invoice.customer} />,
          },
          {
            key: "issueDate",
            title: "Issue Date",
            sortable: true,
            render: (invoice) => formatGreekDate(invoice.issueDate),
          },
          {
            key: "total",
            title: "Total",
            sortable: true,
            render: (invoice) => formatEuro(invoice.total),
          },
          {
            key: "status",
            title: "Status",
            render: (invoice) => <StatusBadge status={invoice.status} />,
          },
          {
            key: "aadeStatus",
            title: "AADE",
            render: (invoice) => (
              <AADEStatusBadge status={invoice.aadeStatus} />
            ),
          },
          {
            key: "actions",
            title: "Actions",
            render: (invoice) => <InvoiceActionMenu invoice={invoice} />,
          },
        ]}
        onRowClick={(invoice) => navigate(`/erp/invoicing/${invoice.id}`)}
      />

      <Pagination
        current={pagination.page}
        total={pagination.total}
        pageSize={pagination.size}
        onChange={(page) => updatePagination({ page })}
      />
    </PageLayout>
  );
};
```

### 3. Invoice Creation (`/erp/invoicing/create`)

**Purpose**: Create new invoices with Greek compliance

#### UI Components:

```typescript
interface InvoiceCreateProps {
  customerId?: string; // Pre-selected from CRM
  templateId?: string; // Invoice template
}

const InvoiceCreate: React.FC<InvoiceCreateProps> = () => {
  const { form, handleSubmit, errors } = useInvoiceForm();
  const { customers } = useCustomers();
  const { services } = useServices();
  const { vatRates } = useGreekVATRates();

  return (
    <FormLayout>
      <FormHeader
        title="Create Invoice"
        subtitle="Create a new invoice with Greek compliance"
      />

      <InvoiceForm onSubmit={handleSubmit}>
        {/* Customer Selection */}
        <FormSection title="Customer Information">
          <CustomerSelector
            value={form.customerId}
            onChange={(customer) => form.setCustomer(customer)}
            customers={customers}
            required
            allowCreate // Can create customer from CRM
          />

          {form.customer && (
            <CustomerSummary customer={form.customer} showGreekTaxInfo />
          )}
        </FormSection>

        {/* Invoice Details */}
        <FormSection title="Invoice Details">
          <Row>
            <Col md={6}>
              <InvoiceNumberField
                value={form.invoiceNumber}
                onChange={form.setInvoiceNumber}
                autoGenerate
                pattern="INV-{YYYY}-{###}"
              />
            </Col>
            <Col md={6}>
              <InvoiceDateField
                value={form.issueDate}
                onChange={form.setIssueDate}
                required
              />
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <DueDateField
                value={form.dueDate}
                onChange={form.setDueDate}
                defaultDays={30}
              />
            </Col>
            <Col md={6}>
              <PaymentTermsSelector
                value={form.paymentTerms}
                onChange={form.setPaymentTerms}
                options={["immediate", "15_days", "30_days", "60_days"]}
              />
            </Col>
          </Row>
        </FormSection>

        {/* Services/Items */}
        <FormSection title="Services & Items">
          <InvoiceItemsEditor
            items={form.items}
            onChange={form.setItems}
            services={services}
            vatRates={vatRates}
            allowCustomItems
          />

          <AddItemButton
            onClick={() => form.addItem()}
            options={[
              { type: "service", label: "Add Service" },
              { type: "custom", label: "Add Custom Item" },
              { type: "template", label: "From Template" },
            ]}
          />
        </FormSection>

        {/* Greek Tax Calculation */}
        <FormSection title="Tax Calculation">
          <GreekVATCalculator
            items={form.items}
            customer={form.customer}
            businessType={form.businessType}
            onCalculation={form.setTaxCalculation}
          />

          <TaxSummary
            subtotal={form.subtotal}
            vatAmount={form.vatAmount}
            total={form.total}
            vatBreakdown={form.vatBreakdown}
          />
        </FormSection>

        {/* Notes & Additional Info */}
        <FormSection title="Additional Information">
          <NotesField
            value={form.notes}
            onChange={form.setNotes}
            placeholder="Internal notes (not visible on invoice)"
          />

          <CustomerNotesField
            value={form.customerNotes}
            onChange={form.setCustomerNotes}
            placeholder="Notes visible to customer"
          />
        </FormSection>

        {/* Actions */}
        <FormActions>
          <SaveDraftButton
            onClick={() => handleSubmit("draft")}
            disabled={!form.isValid}
          />
          <SendInvoiceButton
            onClick={() => handleSubmit("send")}
            disabled={!form.isValid || !form.customer?.email}
          />
          <PreviewButton onClick={() => openPreview(form.data)} />
        </FormActions>
      </InvoiceForm>
    </FormLayout>
  );
};
```

### 4. Invoice Detail (`/erp/invoicing/:id`)

**Purpose**: View and manage individual invoice

#### UI Components:

```typescript
interface InvoiceDetailProps {
  invoiceId: string;
}

const InvoiceDetail: React.FC<InvoiceDetailProps> = ({ invoiceId }) => {
  const { invoice, loading, error } = useInvoice(invoiceId);
  const { permissions } = useInvoicePermissions(invoice);

  if (loading) return <InvoiceDetailSkeleton />;
  if (error) return <ErrorState error={error} />;

  return (
    <DetailLayout>
      <DetailHeader>
        <InvoiceTitle invoice={invoice} />
        <InvoiceActionToolbar invoice={invoice} permissions={permissions} />
      </DetailHeader>

      <DetailContent>
        {/* Invoice Preview */}
        <InvoicePreviewCard invoice={invoice}>
          <InvoicePDFViewer invoice={invoice} showGreekFormat />
        </InvoicePreviewCard>

        {/* Invoice Information */}
        <InvoiceInfoCard>
          <InfoSection title="Customer">
            <CustomerDisplay customer={invoice.customer} />
            <CustomerContactInfo customer={invoice.customer} />
          </InfoSection>

          <InfoSection title="Invoice Details">
            <DetailRow label="Invoice Number" value={invoice.invoiceNumber} />
            <DetailRow
              label="Issue Date"
              value={formatGreekDate(invoice.issueDate)}
            />
            <DetailRow
              label="Due Date"
              value={formatGreekDate(invoice.dueDate)}
            />
            <DetailRow label="Payment Terms" value={invoice.paymentTerms} />
          </InfoSection>

          <InfoSection title="Financial Summary">
            <DetailRow label="Subtotal" value={formatEuro(invoice.subtotal)} />
            <DetailRow
              label="VAT Amount"
              value={formatEuro(invoice.vatAmount)}
            />
            <DetailRow label="Total" value={formatEuro(invoice.total)} strong />
          </InfoSection>
        </InvoiceInfoCard>

        {/* AADE Compliance */}
        <AADEComplianceCard invoice={invoice}>
          <AADESubmissionStatus
            status={invoice.aadeStatus}
            submissionDate={invoice.aadeSubmissionDate}
            mark={invoice.aadeMark}
          />

          {invoice.aadeStatus === "pending" && (
            <SubmitToAADEButton
              invoiceId={invoice.id}
              onSubmit={handleAADESubmission}
            />
          )}

          {invoice.qrCode && (
            <QRCodeDisplay qrCode={invoice.qrCode} label="AADE QR Code" />
          )}
        </AADEComplianceCard>

        {/* Payment Tracking */}
        <PaymentTrackingCard invoice={invoice}>
          <PaymentStatus
            status={invoice.paymentStatus}
            amountPaid={invoice.amountPaid}
            amountDue={invoice.amountDue}
          />

          <PaymentHistory payments={invoice.payments} />

          {permissions.canRecordPayment && (
            <RecordPaymentButton
              invoiceId={invoice.id}
              amountDue={invoice.amountDue}
            />
          )}
        </PaymentTrackingCard>

        {/* Activity Timeline */}
        <ActivityTimelineCard>
          <InvoiceTimeline activities={invoice.activities} showSystemEvents />
        </ActivityTimelineCard>
      </DetailContent>
    </DetailLayout>
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

### Core Invoice Model

```typescript
interface Invoice {
  id: string;
  invoiceNumber: string;
  customerId: string;
  customer: Customer; // From CRM

  // Invoice Details
  issueDate: Date;
  dueDate: Date;
  paymentTerms: string;

  // Items
  items: InvoiceItem[];

  // Financial
  subtotal: number;
  vatAmount: number;
  total: number;
  currency: string;

  // Status
  status: InvoiceStatus;
  paymentStatus: PaymentStatus;
  amountPaid: number;
  amountDue: number;

  // Greek Compliance
  aadeStatus: AADEStatus;
  aadeSubmissionDate?: Date;
  aadeMark?: string;
  qrCode?: string;
  greekVATInfo: GreekVATInfo;

  // Additional Info
  notes?: string;
  customerNotes?: string;

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;

  // Relations
  payments: Payment[];
  activities: InvoiceActivity[];
}

interface InvoiceItem {
  id: string;
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;

  // VAT
  vatRate: number;
  vatAmount: number;
  vatExempt: boolean;
  vatExemptionReason?: string;

  // Service-specific
  serviceId?: string;
  duration?: number; // For hourly services

  // Greek specifics
  greekTaxCategory: GreekTaxCategory;
}

type InvoiceStatus =
  | "draft"
  | "sent"
  | "viewed"
  | "accepted"
  | "rejected"
  | "cancelled";

type PaymentStatus = "unpaid" | "partially_paid" | "paid" | "overdue";

type AADEStatus = "pending" | "submitted" | "accepted" | "rejected" | "error";
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
