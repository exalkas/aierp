// Greek ERP/CRM - Standard Reports Module

// Report types
export interface ReportConfig {
  id: string;
  title: string;
  type: "sales" | "customers" | "inventory" | "financial" | "tax";
  parameters: Record<string, any>;
  dateRange: DateRange;
  filters: ReportFilter[];
  groupBy: string[];
  orderBy: string[];
}

export interface DateRange {
  start: Date;
  end: Date;
}

export interface ReportFilter {
  field: string;
  operator: "equals" | "contains" | "greater" | "less" | "between";
  value: any;
}

export interface ReportData {
  columns: ReportColumn[];
  rows: Record<string, any>[];
  summary: Record<string, number>;
  metadata: ReportMetadata;
}

export interface ReportColumn {
  key: string;
  title: string;
  type: "string" | "number" | "date" | "currency";
  format?: string;
}

export interface ReportMetadata {
  generatedAt: Date;
  totalRows: number;
  executionTime: number;
  parameters: Record<string, any>;
}

// Report utilities
export const createSalesReport = (dateRange: DateRange): ReportConfig => {
  return {
    id: "sales-report",
    title: "Sales Report",
    type: "sales",
    parameters: {},
    dateRange,
    filters: [],
    groupBy: ["date"],
    orderBy: ["date"],
  };
};

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat("el-GR", {
    style: "currency",
    currency: "EUR",
  }).format(amount);
};

export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat("el-GR").format(date);
};
