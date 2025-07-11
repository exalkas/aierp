# 03. Financial Management Module - Technical Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Module**: Financial Management (€39/month)
- **Dependencies**: Basic Invoicing Module
- **Target Users**: Medium businesses, Accounting firms, Multi-department companies

## Overview

The Financial Management Module provides complete accounting functionality with full Greek compliance, including chart of accounts, double-entry bookkeeping, VAT reporting, AADE integration, and comprehensive financial reporting. This module transforms basic invoicing into a complete accounting system.

---

## 🖥️ Screens & User Interface

### 1. Financial Dashboard (`/erp/finance/dashboard`)

**Purpose**: Overview of financial health and key metrics

```typescript
const FinancialDashboard: React.FC = () => {
  const { summary, loading } = useFinancialSummary();
  const { cashFlow } = useCashFlowData();

  return (
    <DashboardLayout>
      <DashboardHeader title="Financial Overview" />

      <MetricsGrid>
        <MetricCard
          title="Total Revenue (YTD)"
          value={formatEuro(summary.totalRevenue)}
          change="+12.5%"
          trend="up"
          icon={<TrendingUpIcon />}
        />
        <MetricCard
          title="Net Profit Margin"
          value={`${summary.profitMargin}%`}
          change="+2.1%"
          trend="up"
          icon={<PercentIcon />}
        />
        <MetricCard
          title="Outstanding Receivables"
          value={formatEuro(summary.receivables)}
          count={`${summary.receivablesCount} invoices`}
          status="warning"
          icon={<ClockIcon />}
        />
        <MetricCard
          title="VAT to Pay"
          value={formatEuro(summary.vatLiability)}
          subtitle="Next submission due"
          status="info"
          icon={<CalculatorIcon />}
        />
      </MetricsGrid>

      <Row>
        <Col md={8}>
          <CashFlowChart data={cashFlow} />
        </Col>
        <Col md={4}>
          <VATComplianceWidget />
          <QuickFinancialActions />
        </Col>
      </Row>

      <RecentTransactionsWidget />
      <FinancialAlertsWidget />
    </DashboardLayout>
  );
};
```

### 2. Chart of Accounts (`/erp/finance/accounts`)

**Purpose**: Manage the Greek chart of accounts structure

```typescript
const ChartOfAccounts: React.FC = () => {
  const { accounts, loading } = useChartOfAccounts();
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);

  return (
    <PageLayout>
      <PageHeader
        title="Chart of Accounts"
        subtitle="Greek Standard Chart of Accounts"
        actions={<CreateAccountButton />}
      />

      <Split>
        <AccountsTreeView
          accounts={accounts}
          loading={loading}
          selectedAccountId={selectedAccount?.id}
          onAccountSelect={setSelectedAccount}
          showBalances
          showGreekCodes
        />

        {selectedAccount && (
          <AccountDetailPanel
            account={selectedAccount}
            showTransactions
            showSubAccounts
          />
        )}
      </Split>
    </PageLayout>
  );
};
```

### 3. Journal Entries (`/erp/finance/journal`)

**Purpose**: Record and manage journal entries with Greek compliance

```typescript
const JournalEntries: React.FC = () => {
  const { entries, loading } = useJournalEntries();
  const { filters, updateFilter } = useJournalFilters();

  return (
    <PageLayout>
      <PageHeader
        title="Journal Entries"
        actions={<CreateJournalEntryButton />}
      />

      <FilterBar>
        <DateRangeFilter
          value={filters.dateRange}
          onChange={(range) => updateFilter("dateRange", range)}
        />
        <AccountFilter
          value={filters.accountId}
          onChange={(id) => updateFilter("accountId", id)}
        />
        <EntryTypeFilter
          value={filters.entryType}
          onChange={(type) => updateFilter("entryType", type)}
        />
        <StatusFilter
          value={filters.status}
          onChange={(status) => updateFilter("status", status)}
        />
      </FilterBar>

      <JournalEntriesGrid
        entries={entries}
        loading={loading}
        columns={[
          "date",
          "reference",
          "description",
          "accounts",
          "debit",
          "credit",
          "status",
          "actions",
        ]}
        allowInlineEdit
        showRunningBalance
      />
    </PageLayout>
  );
};
```

### 4. VAT Management (`/erp/finance/vat`)

**Purpose**: Comprehensive VAT tracking and AADE compliance

```typescript
const VATManagement: React.FC = () => {
  const { vatPeriod, vatSummary } = useVATData();
  const { aadeStatus } = useAADEStatus();

  return (
    <PageLayout>
      <PageHeader title="VAT Management" />

      <VATOverview>
        <VATSummaryCard period={vatPeriod} summary={vatSummary} showBreakdown />
        <AADEStatusCard status={aadeStatus} showUpcomingDeadlines />
      </VATOverview>

      <VATTabs>
        <TabPanel label="VAT Returns">
          <VATReturns period={vatPeriod} allowCreate allowSubmit />
        </TabPanel>

        <TabPanel label="AADE Submissions">
          <AADESubmissions submissions={aadeStatus.submissions} allowResubmit />
        </TabPanel>

        <TabPanel label="VAT Analysis">
          <VATAnalytics period={vatPeriod} showTrends showComparisons />
        </TabPanel>
      </VATTabs>
    </PageLayout>
  );
};
```

### 5. Financial Reports (`/erp/finance/reports`)

**Purpose**: Generate comprehensive financial reports

```typescript
const FinancialReports: React.FC = () => {
  const [selectedReport, setSelectedReport] =
    useState<ReportType>("profit_loss");
  const [reportPeriod, setReportPeriod] = useState<DateRange>();

  return (
    <PageLayout>
      <PageHeader title="Financial Reports" />

      <ReportSelection>
        <ReportTypeSelector
          value={selectedReport}
          onChange={setSelectedReport}
          options={[
            { value: "profit_loss", label: "Profit & Loss Statement" },
            { value: "balance_sheet", label: "Balance Sheet" },
            { value: "cash_flow", label: "Cash Flow Statement" },
            { value: "trial_balance", label: "Trial Balance" },
            { value: "aged_receivables", label: "Aged Receivables" },
            { value: "vat_report", label: "VAT Report" },
          ]}
        />

        <PeriodSelector
          value={reportPeriod}
          onChange={setReportPeriod}
          presets={["month", "quarter", "year"]}
        />

        <GenerateReportButton
          reportType={selectedReport}
          period={reportPeriod}
          formats={["PDF", "Excel", "Print"]}
        />
      </ReportSelection>

      <ReportViewer
        reportType={selectedReport}
        period={reportPeriod}
        interactive
        allowDrillDown
      />
    </PageLayout>
  );
};
```

---

## 🔗 API Endpoints

### Account Management APIs

```typescript
// GET /api/erp/finance/accounts
interface GetAccountsResponse {
  accounts: Account[];
  hierarchy: AccountHierarchy;
  balances: AccountBalance[];
}

// POST /api/erp/finance/accounts
interface CreateAccountRequest {
  code: string;
  name: string;
  nameGreek?: string;
  parentAccountId?: string;
  accountType: AccountType;
  greekAccountCategory: GreekAccountCategory;
  vatRate?: number;
  isActive: boolean;
}

// GET /api/erp/finance/accounts/:id/transactions
interface GetAccountTransactionsRequest {
  accountId: string;
  dateFrom?: Date;
  dateTo?: Date;
  includeSubAccounts?: boolean;
}
```

### Journal Entry APIs

```typescript
// GET /api/erp/finance/journal-entries
interface GetJournalEntriesRequest {
  page?: number;
  dateFrom?: Date;
  dateTo?: Date;
  accountId?: string;
  entryType?: JournalEntryType;
  status?: JournalEntryStatus;
}

// POST /api/erp/finance/journal-entries
interface CreateJournalEntryRequest {
  date: Date;
  reference: string;
  description: string;
  entryType: JournalEntryType;
  lines: JournalEntryLine[];
  sourceDocument?: SourceDocument;
}

interface JournalEntryLine {
  accountId: string;
  debitAmount?: number;
  creditAmount?: number;
  description?: string;
  vatAmount?: number;
  vatRate?: number;
}
```

### VAT Management APIs

```typescript
// GET /api/erp/finance/vat/summary
interface GetVATSummaryRequest {
  periodStart: Date;
  periodEnd: Date;
  includeDetails?: boolean;
}

interface GetVATSummaryResponse {
  period: VATPeriod;
  inputVAT: number;
  outputVAT: number;
  netVAT: number;
  breakdown: VATBreakdown[];
  transactions: VATTransaction[];
}

// POST /api/erp/finance/vat/return
interface CreateVATReturnRequest {
  period: VATPeriod;
  includeAdjustments?: boolean;
  submitToAADE?: boolean;
}

// POST /api/erp/finance/aade/submit
interface SubmitToAADERequest {
  documentType: AADEDocumentType;
  documentId: string;
  data: AADESubmissionData;
}
```

### Financial Reporting APIs

```typescript
// GET /api/erp/finance/reports/profit-loss
interface GetProfitLossRequest {
  periodStart: Date;
  periodEnd: Date;
  comparisonPeriod?: DateRange;
  includeSubAccounts?: boolean;
}

// GET /api/erp/finance/reports/balance-sheet
interface GetBalanceSheetRequest {
  asOfDate: Date;
  comparisonDate?: Date;
  includeSubAccounts?: boolean;
}

// GET /api/erp/finance/reports/cash-flow
interface GetCashFlowRequest {
  periodStart: Date;
  periodEnd: Date;
  method: "direct" | "indirect";
}
```

---

## 🗃️ Data Models

### Account Model

```typescript
interface Account {
  id: string;
  code: string; // Greek account code (e.g., "10.01.001")
  name: string;
  nameGreek?: string;

  // Hierarchy
  parentAccountId?: string;
  parentAccount?: Account;
  childAccounts: Account[];
  level: number;

  // Classification
  accountType: AccountType;
  greekAccountCategory: GreekAccountCategory;
  isControlAccount: boolean;

  // Properties
  isActive: boolean;
  allowDirectEntries: boolean;
  requireVAT: boolean;
  defaultVATRate?: number;

  // Balances
  currentBalance: number;
  debitBalance: number;
  creditBalance: number;
  openingBalance: number;

  // Greek compliance
  greekTaxInfo: AccountGreekTaxInfo;
  aadeClassification?: string;

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}

type AccountType = "asset" | "liability" | "equity" | "revenue" | "expense";

type GreekAccountCategory =
  | "ΕΞΟΔΑ_ΠΩΛΗΣΕΩΝ" // Cost of Sales
  | "ΛΕΙΤΟΥΡΓΙΚΑ_ΕΞΟΔΑ" // Operating Expenses
  | "ΠΩΛΗΣΕΙΣ" // Sales
  | "ΠΑΓΙΑ_ΣΤΟΙΧΕΙΑ" // Fixed Assets
  | "ΚΥΚΛΟΦΟΡΟΥΝΤΑ" // Current Assets
  | "ΥΠΟΧΡΕΩΣΕΙΣ" // Liabilities
  | "ΚΕΦΑΛΑΙΑ"; // Equity
```

### Journal Entry Model

```typescript
interface JournalEntry {
  id: string;
  entryNumber: string;

  // Entry details
  date: Date;
  reference: string;
  description: string;
  entryType: JournalEntryType;

  // Lines (double-entry)
  lines: JournalEntryLine[];
  totalDebit: number;
  totalCredit: number;

  // Source information
  sourceDocument?: SourceDocument;
  automaticEntry: boolean;

  // Status
  status: JournalEntryStatus;
  postedDate?: Date;
  postedBy?: string;

  // Reversals
  reversedEntryId?: string;
  reversalReason?: string;

  // Greek compliance
  greekTaxPeriod: string;
  aadeReference?: string;

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}

interface JournalEntryLine {
  id: string;
  journalEntryId: string;

  // Account information
  accountId: string;
  account: Account;

  // Amounts
  debitAmount: number;
  creditAmount: number;

  // VAT information
  vatAmount?: number;
  vatRate?: number;
  vatAccountId?: string;

  // Description
  description?: string;

  // Analysis dimensions
  customerId?: string;
  supplierId?: string;
  projectId?: string;
  departmentId?: string;
}

type JournalEntryType =
  | "manual"
  | "invoice"
  | "payment"
  | "adjustment"
  | "accrual"
  | "depreciation";

type JournalEntryStatus = "draft" | "posted" | "reversed";
```

### VAT Model

```typescript
interface VATTransaction {
  id: string;

  // Document information
  documentType: VATDocumentType;
  documentId: string;
  documentNumber: string;
  documentDate: Date;

  // Counterpart
  counterpartType: "customer" | "supplier";
  counterpartId: string;
  counterpartVATNumber?: string;
  counterpartName: string;

  // VAT details
  netAmount: number;
  vatRate: number;
  vatAmount: number;
  totalAmount: number;

  // Classification
  vatType: "input" | "output";
  vatCategory: GreekVATCategory;
  isEUTransaction: boolean;
  isReverseCharge: boolean;

  // AADE information
  aadeSubmitted: boolean;
  aadeSubmissionDate?: Date;
  aadeMark?: string;

  // Period
  taxPeriod: string; // YYYY-MM format

  // Audit
  createdAt: Date;
}

interface VATReturn {
  id: string;

  // Period
  taxPeriod: string;
  periodStart: Date;
  periodEnd: Date;

  // VAT summary
  totalInputVAT: number;
  totalOutputVAT: number;
  netVATLiability: number;

  // Detailed breakdown
  vatBreakdown: VATReturnBreakdown[];
  transactions: VATTransaction[];

  // Status
  status: VATReturnStatus;
  submittedToAADE: boolean;
  aadeSubmissionDate?: Date;
  aadeConfirmation?: string;

  // Audit
  createdAt: Date;
  createdBy: string;
}

type VATDocumentType = "invoice" | "credit_note" | "receipt" | "expense";

type VATReturnStatus =
  | "draft"
  | "calculated"
  | "submitted"
  | "accepted"
  | "rejected";
```

---

## 🧩 UI Components

### Account Management Components

```typescript
// Account display and management
export const AccountsTreeView: React.FC<AccountsTreeViewProps>;
export const AccountCard: React.FC<AccountCardProps>;
export const AccountSelector: React.FC<AccountSelectorProps>;
export const AccountForm: React.FC<AccountFormProps>;
export const AccountBalanceDisplay: React.FC<AccountBalanceDisplayProps>;

// Greek-specific account components
export const GreekAccountCodeInput: React.FC<GreekAccountCodeInputProps>;
export const GreekAccountCategorySelector: React.FC<GreekAccountCategorySelectorProps>;
export const ChartOfAccountsImporter: React.FC<ChartOfAccountsImporterProps>;
```

### Journal Entry Components

```typescript
// Journal entry forms and displays
export const JournalEntryForm: React.FC<JournalEntryFormProps>;
export const JournalEntryGrid: React.FC<JournalEntryGridProps>;
export const JournalEntryLineEditor: React.FC<JournalEntryLineEditorProps>;
export const DoubleEntryValidator: React.FC<DoubleEntryValidatorProps>;

// Quick entry components
export const QuickJournalEntry: React.FC<QuickJournalEntryProps>;
export const RecurringEntryTemplate: React.FC<RecurringEntryTemplateProps>;
export const BulkJournalEntryImporter: React.FC<BulkJournalEntryImporterProps>;
```

### VAT Components

```typescript
// VAT management and display
export const VATSummaryCard: React.FC<VATSummaryCardProps>;
export const VATReturnForm: React.FC<VATReturnFormProps>;
export const VATTransactionList: React.FC<VATTransactionListProps>;
export const AADEStatusWidget: React.FC<AADEStatusWidgetProps>;

// VAT calculation and validation
export const VATCalculator: React.FC<VATCalculatorProps>;
export const VATBreakdownTable: React.FC<VATBreakdownTableProps>;
export const GreekVATRateSelector: React.FC<GreekVATRateSelectorProps>;
```

### Financial Reporting Components

```typescript
// Report generators and viewers
export const FinancialReportViewer: React.FC<FinancialReportViewerProps>;
export const ProfitLossStatement: React.FC<ProfitLossStatementProps>;
export const BalanceSheetReport: React.FC<BalanceSheetReportProps>;
export const CashFlowStatement: React.FC<CashFlowStatementProps>;

// Report configuration
export const ReportParameterForm: React.FC<ReportParameterFormProps>;
export const ReportScheduler: React.FC<ReportSchedulerProps>;
export const ReportExporter: React.FC<ReportExporterProps>;
```

---

## 🪝 Custom Hooks

### Account Management Hooks

```typescript
export const useChartOfAccounts = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [hierarchy, setHierarchy] = useState<AccountHierarchy>();

  const createAccount = useCallback(
    async (accountData: CreateAccountRequest) => {
      try {
        const newAccount = await accountsAPI.create(accountData);
        setAccounts((prev) => [...prev, newAccount]);
        return newAccount;
      } catch (error) {
        throw new AccountCreationError(error.message);
      }
    },
    []
  );

  const updateAccountBalance = useCallback(
    (accountId: string, amount: number, type: "debit" | "credit") => {
      setAccounts((prev) =>
        prev.map((account) =>
          account.id === accountId
            ? {
                ...account,
                currentBalance:
                  type === "debit"
                    ? account.currentBalance + amount
                    : account.currentBalance - amount,
              }
            : account
        )
      );
    },
    []
  );

  return {
    accounts,
    hierarchy,
    loading,
    createAccount,
    updateAccount,
    deleteAccount,
    updateAccountBalance,
    getAccountByCode,
    getAccountBalance,
  };
};

export const useAccountTransactions = (accountId: string) => {
  return {
    transactions,
    balance,
    loading,
    getTransactionHistory,
    calculateRunningBalance,
  };
};
```

### Journal Entry Hooks

```typescript
export const useJournalEntries = (filters?: JournalEntryFilters) => {
  const [entries, setEntries] = useState<JournalEntry[]>([]);

  const createJournalEntry = useCallback(
    async (entryData: CreateJournalEntryRequest) => {
      // Validate double-entry balance
      const totalDebit = entryData.lines.reduce(
        (sum, line) => sum + line.debitAmount,
        0
      );
      const totalCredit = entryData.lines.reduce(
        (sum, line) => sum + line.creditAmount,
        0
      );

      if (Math.abs(totalDebit - totalCredit) > 0.01) {
        throw new Error("Journal entry is not balanced");
      }

      try {
        const newEntry = await journalAPI.create(entryData);
        setEntries((prev) => [newEntry, ...prev]);

        // Update account balances
        newEntry.lines.forEach((line) => {
          updateAccountBalance(
            line.accountId,
            line.debitAmount || line.creditAmount,
            line.debitAmount > 0 ? "debit" : "credit"
          );
        });

        return newEntry;
      } catch (error) {
        throw new JournalEntryError(error.message);
      }
    },
    []
  );

  const postJournalEntry = useCallback(async (entryId: string) => {
    try {
      const postedEntry = await journalAPI.post(entryId);
      setEntries((prev) =>
        prev.map((entry) =>
          entry.id === entryId
            ? { ...entry, status: "posted", postedDate: new Date() }
            : entry
        )
      );
      return postedEntry;
    } catch (error) {
      throw new JournalEntryError(error.message);
    }
  }, []);

  return {
    entries,
    loading,
    createJournalEntry,
    updateJournalEntry,
    postJournalEntry,
    reverseJournalEntry,
  };
};

export const useDoubleEntryValidation = () => {
  const validateEntry = useCallback((lines: JournalEntryLine[]) => {
    const totalDebit = lines.reduce(
      (sum, line) => sum + (line.debitAmount || 0),
      0
    );
    const totalCredit = lines.reduce(
      (sum, line) => sum + (line.creditAmount || 0),
      0
    );

    return {
      isBalanced: Math.abs(totalDebit - totalCredit) < 0.01,
      totalDebit,
      totalCredit,
      difference: totalDebit - totalCredit,
    };
  }, []);

  return { validateEntry };
};
```

### VAT Management Hooks

```typescript
export const useVATData = (period: VATPeriod) => {
  const [vatSummary, setVATSummary] = useState<VATSummary>();
  const [vatTransactions, setVATTransactions] = useState<VATTransaction[]>([]);

  useEffect(() => {
    Promise.all([
      vatAPI.getSummary(period),
      vatAPI.getTransactions(period),
    ]).then(([summary, transactions]) => {
      setVATSummary(summary);
      setVATTransactions(transactions);
    });
  }, [period]);

  const calculateVATReturn = useCallback(async (period: VATPeriod) => {
    try {
      const vatReturn = await vatAPI.calculateReturn(period);
      return vatReturn;
    } catch (error) {
      throw new VATCalculationError(error.message);
    }
  }, []);

  const submitVATReturn = useCallback(async (vatReturnId: string) => {
    try {
      const result = await aadeAPI.submitVATReturn(vatReturnId);
      return result;
    } catch (error) {
      throw new AADESubmissionError(error.message);
    }
  }, []);

  return {
    vatSummary,
    vatTransactions,
    loading,
    calculateVATReturn,
    submitVATReturn,
    getVATBreakdown,
  };
};

export const useGreekVATCompliance = () => {
  const [vatRates, setVATRates] = useState<GreekVATRate[]>([]);
  const [businessRules, setBusinessRules] = useState<VATBusinessRule[]>([]);

  const validateVATTransaction = useCallback(
    (transaction: VATTransaction) => {
      const validationResults = businessRules.map((rule) =>
        rule.validate(transaction)
      );
      return validationResults.filter((result) => !result.isValid);
    },
    [businessRules]
  );

  const calculateGreekVAT = useCallback(
    (amount: number, vatCategory: GreekVATCategory, date: Date) => {
      const applicableRate = vatRates.find(
        (rate) =>
          rate.category === vatCategory &&
          rate.effectiveFrom <= date &&
          (!rate.effectiveTo || rate.effectiveTo >= date)
      );

      if (!applicableRate) {
        throw new Error(
          `No VAT rate found for category ${vatCategory} on ${date}`
        );
      }

      return {
        netAmount: amount,
        vatRate: applicableRate.rate,
        vatAmount: amount * (applicableRate.rate / 100),
        totalAmount: amount * (1 + applicableRate.rate / 100),
      };
    },
    [vatRates]
  );

  return {
    vatRates,
    businessRules,
    validateVATTransaction,
    calculateGreekVAT,
    getApplicableVATRate,
  };
};
```

### Financial Reporting Hooks

```typescript
export const useFinancialReports = () => {
  const generateProfitLoss = useCallback(async (params: ProfitLossParams) => {
    try {
      const report = await reportsAPI.generateProfitLoss(params);
      return report;
    } catch (error) {
      throw new ReportGenerationError(error.message);
    }
  }, []);

  const generateBalanceSheet = useCallback(
    async (params: BalanceSheetParams) => {
      try {
        const report = await reportsAPI.generateBalanceSheet(params);
        return report;
      } catch (error) {
        throw new ReportGenerationError(error.message);
      }
    },
    []
  );

  const generateCashFlow = useCallback(async (params: CashFlowParams) => {
    try {
      const report = await reportsAPI.generateCashFlow(params);
      return report;
    } catch (error) {
      throw new ReportGenerationError(error.message);
    }
  }, []);

  return {
    generateProfitLoss,
    generateBalanceSheet,
    generateCashFlow,
    exportReport,
    scheduleReport,
  };
};

export const useFinancialSummary = (period?: DateRange) => {
  const [summary, setSummary] = useState<FinancialSummary>();

  useEffect(() => {
    if (period) {
      reportsAPI.getFinancialSummary(period).then(setSummary);
    }
  }, [period]);

  return {
    summary,
    loading,
    refreshSummary: () => {
      if (period) {
        reportsAPI.getFinancialSummary(period).then(setSummary);
      }
    },
  };
};
```

---

## 🌐 Context Providers

### Financial Context

```typescript
interface FinancialContextValue {
  // Company financial settings
  fiscalYearStart: Date;
  baseCurrency: string;
  chartOfAccountsStandard: "GREEK_STANDARD" | "IFRS" | "CUSTOM";

  // VAT settings
  vatRegistrationNumber: string;
  vatSubmissionFrequency: "monthly" | "quarterly";
  nextVATSubmissionDate: Date;

  // AADE settings
  aadeEnvironment: "production" | "sandbox";
  aadeCredentials: AADECredentials;

  // Accounting preferences
  allowPostdatedEntries: boolean;
  requireJournalApproval: boolean;
  enableMultiCurrency: boolean;

  // Current period
  currentPeriod: AccountingPeriod;

  // Functions
  closeAccountingPeriod: (period: AccountingPeriod) => Promise<void>;
  generatePeriodEndEntries: (
    period: AccountingPeriod
  ) => Promise<JournalEntry[]>;
}

export const FinancialProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { company } = useCompany();
  const [currentPeriod, setCurrentPeriod] = useState<AccountingPeriod>();

  useEffect(() => {
    // Load current accounting period
    getCurrentAccountingPeriod(company.id).then(setCurrentPeriod);
  }, [company.id]);

  const closeAccountingPeriod = useCallback(
    async (period: AccountingPeriod) => {
      try {
        // Generate period-end adjustments
        const adjustments = await generatePeriodEndAdjustments(period);

        // Post all adjustments
        await Promise.all(adjustments.map((adj) => journalAPI.create(adj)));

        // Mark period as closed
        await accountingAPI.closePeriod(period.id);

        // Create new period
        const newPeriod = await accountingAPI.createNewPeriod(period);
        setCurrentPeriod(newPeriod);
      } catch (error) {
        throw new PeriodClosingError(error.message);
      }
    },
    []
  );

  const value: FinancialContextValue = {
    fiscalYearStart:
      company.fiscalYearStart || new Date(new Date().getFullYear(), 0, 1),
    baseCurrency: company.baseCurrency || "EUR",
    chartOfAccountsStandard:
      company.chartOfAccountsStandard || "GREEK_STANDARD",
    vatRegistrationNumber: company.greekTaxInfo.afm,
    vatSubmissionFrequency: company.vatSubmissionFrequency || "monthly",
    nextVATSubmissionDate: calculateNextVATSubmissionDate(
      company.vatSubmissionFrequency
    ),
    aadeEnvironment: company.aadeEnvironment || "sandbox",
    aadeCredentials: company.aadeCredentials,
    allowPostdatedEntries:
      company.accountingSettings?.allowPostdatedEntries || false,
    requireJournalApproval:
      company.accountingSettings?.requireJournalApproval || true,
    enableMultiCurrency:
      company.accountingSettings?.enableMultiCurrency || false,
    currentPeriod: currentPeriod!,
    closeAccountingPeriod,
    generatePeriodEndEntries: (period) => generatePeriodEndAdjustments(period),
  };

  return (
    <FinancialContext.Provider value={value}>
      {children}
    </FinancialContext.Provider>
  );
};
```

---

## 📋 Implementation Checklist

### Phase 1: Core Accounting (Week 1-3)

- [ ] Greek chart of accounts implementation
- [ ] Account management and hierarchy
- [ ] Journal entry system with double-entry validation
- [ ] Basic financial reports (P&L, Balance Sheet)
- [ ] Multi-period support

### Phase 2: VAT & Greek Compliance (Week 4-6)

- [ ] Greek VAT calculation engine
- [ ] VAT transaction tracking
- [ ] VAT return generation
- [ ] AADE MyDATA integration
- [ ] Greek tax period management

### Phase 3: Advanced Financial Features (Week 7-9)

- [ ] Cash flow management
- [ ] Aged receivables/payables
- [ ] Financial analytics and KPIs
- [ ] Period-end closing procedures
- [ ] Multi-currency support (optional)

### Phase 4: Integration & Testing (Week 10-12)

- [ ] Integration with invoicing module
- [ ] Integration with inventory module
- [ ] Comprehensive testing suite
- [ ] Performance optimization
- [ ] User documentation and training

This Financial Management Module provides complete accounting functionality while maintaining full Greek compliance and seamless integration with other ERP modules.
