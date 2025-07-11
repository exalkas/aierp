// Greek ERP/CRM - Admin Subscriptions Module

// Subscription types
export interface Subscription {
  id: string;
  companyId: string;
  planId: string;
  status: "active" | "suspended" | "cancelled" | "expired";
  startDate: Date;
  endDate: Date;
  renewalDate: Date;
  isAutoRenew: boolean;
  price: number;
  currency: string;
  features: string[];
  limits: SubscriptionLimits;
  createdAt: Date;
  updatedAt: Date;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  billingPeriod: "monthly" | "annual";
  features: string[];
  limits: SubscriptionLimits;
  isActive: boolean;
  order: number;
}

export interface SubscriptionLimits {
  users: number;
  customers: number;
  invoices: number;
  storage: number; // in GB
  apiCalls: number;
  modules: string[];
}

// Subscription utilities
export const createSubscription = (
  data: Partial<Subscription>
): Subscription => {
  const now = new Date();
  const startDate = data.startDate || now;
  const endDate =
    data.endDate || new Date(startDate.getTime() + 365 * 24 * 60 * 60 * 1000); // 1 year

  return {
    id: `sub_${Date.now()}`,
    companyId: data.companyId || "",
    planId: data.planId || "",
    status: data.status || "active",
    startDate,
    endDate,
    renewalDate: data.renewalDate || endDate,
    isAutoRenew: data.isAutoRenew !== undefined ? data.isAutoRenew : true,
    price: data.price || 0,
    currency: data.currency || "EUR",
    features: data.features || [],
    limits: data.limits || {
      users: 5,
      customers: 1000,
      invoices: 500,
      storage: 1,
      apiCalls: 10000,
      modules: ["crm", "erp"],
    },
    createdAt: now,
    updatedAt: now,
  };
};

export const isSubscriptionActive = (subscription: Subscription): boolean => {
  return subscription.status === "active" && subscription.endDate > new Date();
};

export const getDefaultPlans = (): SubscriptionPlan[] => {
  return [
    {
      id: "basic",
      name: "Basic",
      description: "Perfect for small Greek businesses",
      price: 29,
      currency: "EUR",
      billingPeriod: "monthly",
      features: ["CRM", "Basic ERP", "AADE Integration", "Email Support"],
      limits: {
        users: 5,
        customers: 1000,
        invoices: 500,
        storage: 1,
        apiCalls: 10000,
        modules: ["crm", "erp"],
      },
      isActive: true,
      order: 1,
    },
    {
      id: "professional",
      name: "Professional",
      description: "For growing Greek businesses",
      price: 59,
      currency: "EUR",
      billingPeriod: "monthly",
      features: [
        "CRM",
        "Full ERP",
        "Advanced Reports",
        "API Access",
        "Priority Support",
      ],
      limits: {
        users: 25,
        customers: 10000,
        invoices: 2000,
        storage: 5,
        apiCalls: 50000,
        modules: ["crm", "erp", "reports", "api"],
      },
      isActive: true,
      order: 2,
    },
  ];
};
