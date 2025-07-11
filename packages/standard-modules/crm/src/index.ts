// Greek ERP/CRM - Standard CRM Module

// CRM types
export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  afm?: string; // Greek tax number
  address: Address;
  companyId: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Address {
  street: string;
  city: string;
  postalCode: string;
  region: string;
  country: string;
}

export interface Lead {
  id: string;
  customerId?: string;
  source: string;
  status: "new" | "contacted" | "qualified" | "converted" | "lost";
  priority: "low" | "medium" | "high";
  estimatedValue: number;
  companyId: string;
  assignedTo?: string;
  createdAt: Date;
  updatedAt: Date;
}

// CRM utilities
export const createCustomer = (data: Partial<Customer>): Customer => {
  const now = new Date();
  return {
    id: `cust_${Date.now()}`,
    name: data.name || "",
    email: data.email || "",
    phone: data.phone || "",
    afm: data.afm,
    address: data.address || {
      street: "",
      city: "",
      postalCode: "",
      region: "",
      country: "Greece",
    },
    companyId: data.companyId || "",
    createdAt: now,
    updatedAt: now,
  };
};

export const validateAFM = (afm: string): boolean => {
  // Basic Greek AFM validation
  return /^\d{9}$/.test(afm);
};
