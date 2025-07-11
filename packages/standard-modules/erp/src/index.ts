// Greek ERP/CRM - Standard ERP Module

// ERP types
export interface Product {
  id: string;
  name: string;
  description: string;
  sku: string;
  price: number;
  vatRate: number; // Greek VAT rate
  category: string;
  stock: number;
  companyId: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Invoice {
  id: string;
  customerId: string;
  number: string;
  date: Date;
  dueDate: Date;
  items: InvoiceItem[];
  subtotal: number;
  vatAmount: number;
  total: number;
  status: "draft" | "sent" | "paid" | "overdue";
  aadeSubmitted: boolean; // Greek tax authority submission
  companyId: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface InvoiceItem {
  id: string;
  productId: string;
  quantity: number;
  unitPrice: number;
  vatRate: number;
  total: number;
}

// ERP utilities
export const calculateVAT = (amount: number, vatRate: number): number => {
  return amount * (vatRate / 100);
};

export const calculateInvoiceTotal = (
  items: InvoiceItem[]
): { subtotal: number; vatAmount: number; total: number } => {
  const subtotal = items.reduce(
    (sum, item) => sum + item.quantity * item.unitPrice,
    0
  );
  const vatAmount = items.reduce(
    (sum, item) =>
      sum + calculateVAT(item.quantity * item.unitPrice, item.vatRate),
    0
  );
  const total = subtotal + vatAmount;

  return { subtotal, vatAmount, total };
};

export const getGreekVATRates = (): Record<string, number> => {
  return {
    standard: 24,
    reduced: 13,
    superReduced: 6,
  };
};
