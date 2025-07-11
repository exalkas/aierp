// Greek ERP/CRM - Standard Dashboard Module

// Dashboard types
export interface DashboardWidget {
  id: string;
  title: string;
  type: "chart" | "metric" | "table" | "custom";
  config: Record<string, any>;
  position: { x: number; y: number; width: number; height: number };
}

export interface DashboardConfig {
  id: string;
  title: string;
  widgets: DashboardWidget[];
  layout: "grid" | "flex";
}

// Dashboard utilities
export const createDefaultDashboard = (): DashboardConfig => {
  return {
    id: "default-dashboard",
    title: "Greek Business Dashboard",
    layout: "grid",
    widgets: [
      {
        id: "sales-metric",
        title: "Sales This Month",
        type: "metric",
        config: { metric: "sales", period: "month" },
        position: { x: 0, y: 0, width: 2, height: 1 },
      },
      {
        id: "customer-chart",
        title: "Customer Growth",
        type: "chart",
        config: { chart: "line", data: "customers" },
        position: { x: 2, y: 0, width: 4, height: 2 },
      },
    ],
  };
};

export const calculateMetrics = (data: any[]): Record<string, number> => {
  return {
    totalSales: data.reduce((sum, item) => sum + (item.amount || 0), 0),
    totalCustomers: data.length,
    avgOrderValue:
      data.length > 0
        ? data.reduce((sum, item) => sum + (item.amount || 0), 0) / data.length
        : 0,
  };
};
