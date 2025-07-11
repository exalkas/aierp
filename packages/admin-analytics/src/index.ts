// Greek ERP/CRM - Admin Analytics Module

// Analytics types
export interface AnalyticsEvent {
  id: string;
  type: string;
  category: string;
  action: string;
  label?: string;
  value?: number;
  properties: Record<string, any>;
  userId?: string;
  companyId?: string;
  sessionId: string;
  timestamp: Date;
  ip?: string;
  userAgent?: string;
}

export interface AnalyticsReport {
  id: string;
  title: string;
  type: "usage" | "performance" | "business" | "error";
  metrics: AnalyticsMetric[];
  dateRange: DateRange;
  filters: AnalyticsFilter[];
  generatedAt: Date;
  data: AnalyticsData;
}

export interface AnalyticsMetric {
  id: string;
  name: string;
  value: number;
  change: number;
  changeType: "increase" | "decrease" | "neutral";
  unit?: string;
  format?: "number" | "percentage" | "currency" | "duration";
}

export interface AnalyticsFilter {
  field: string;
  operator:
    | "equals"
    | "not_equals"
    | "contains"
    | "greater_than"
    | "less_than"
    | "between";
  value: any;
}

export interface AnalyticsData {
  labels: string[];
  datasets: AnalyticsDataset[];
  summary: Record<string, number>;
}

export interface AnalyticsDataset {
  label: string;
  data: number[];
  color?: string;
  type?: "line" | "bar" | "pie" | "doughnut";
}

export interface DateRange {
  start: Date;
  end: Date;
}

// Analytics utilities
export const trackEvent = (event: Partial<AnalyticsEvent>): AnalyticsEvent => {
  return {
    id: `event_${Date.now()}`,
    type: event.type || "custom",
    category: event.category || "general",
    action: event.action || "unknown",
    label: event.label,
    value: event.value,
    properties: event.properties || {},
    userId: event.userId,
    companyId: event.companyId,
    sessionId: event.sessionId || generateSessionId(),
    timestamp: new Date(),
    ip: event.ip,
    userAgent: event.userAgent,
  };
};

export const generateSessionId = (): string => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
};

export const calculateMetrics = (
  events: AnalyticsEvent[]
): AnalyticsMetric[] => {
  const totalEvents = events.length;
  const uniqueUsers = new Set(events.map((e) => e.userId)).size;
  const uniqueCompanies = new Set(events.map((e) => e.companyId)).size;

  return [
    {
      id: "total-events",
      name: "Total Events",
      value: totalEvents,
      change: 0,
      changeType: "neutral",
      format: "number",
    },
    {
      id: "unique-users",
      name: "Unique Users",
      value: uniqueUsers,
      change: 0,
      changeType: "neutral",
      format: "number",
    },
    {
      id: "unique-companies",
      name: "Unique Companies",
      value: uniqueCompanies,
      change: 0,
      changeType: "neutral",
      format: "number",
    },
  ];
};

export const getPopularActions = (
  events: AnalyticsEvent[]
): { action: string; count: number }[] => {
  const actionCounts = events.reduce((acc, event) => {
    acc[event.action] = (acc[event.action] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return Object.entries(actionCounts)
    .map(([action, count]) => ({ action, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);
};

export const formatAnalyticsValue = (
  value: number,
  format?: string
): string => {
  switch (format) {
    case "percentage":
      return `${(value * 100).toFixed(2)}%`;
    case "currency":
      return new Intl.NumberFormat("el-GR", {
        style: "currency",
        currency: "EUR",
      }).format(value);
    case "duration":
      return `${Math.floor(value / 1000)}s`;
    default:
      return value.toLocaleString("el-GR");
  }
};
