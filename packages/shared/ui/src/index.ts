// Greek ERP/CRM - Shared UI Components

// Component types
export interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  className?: string;
}

export interface InputProps {
  type?: "text" | "email" | "password" | "number" | "tel";
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
  error?: string;
  label?: string;
  required?: boolean;
  className?: string;
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg" | "xl";
  showCloseButton?: boolean;
  overlayClosable?: boolean;
}

// Theme types
export interface ThemeConfig {
  colors: {
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    error: string;
    background: string;
    text: string;
  };
  typography: {
    fontFamily: string;
    fontSize: Record<string, string>;
    fontWeight: Record<string, string>;
  };
  spacing: Record<string, string>;
  breakpoints: Record<string, string>;
}

// Utility functions
export const cn = (
  ...classes: (string | undefined | null | false)[]
): string => {
  return classes.filter(Boolean).join(" ");
};

export const getDefaultTheme = (): ThemeConfig => ({
  colors: {
    primary: "#0066CC",
    secondary: "#FFF700",
    success: "#22C55E",
    warning: "#F59E0B",
    error: "#EF4444",
    background: "#FFFFFF",
    text: "#1F2937",
  },
  typography: {
    fontFamily: "Inter, system-ui, sans-serif",
    fontSize: {
      xs: "0.75rem",
      sm: "0.875rem",
      base: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
    },
    fontWeight: {
      light: "300",
      normal: "400",
      medium: "500",
      semibold: "600",
      bold: "700",
    },
  },
  spacing: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem",
    "2xl": "3rem",
  },
  breakpoints: {
    sm: "640px",
    md: "768px",
    lg: "1024px",
    xl: "1280px",
  },
});

// Form validation utilities
export const validateEmail = (email: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const validateAFM = (afm: string): boolean => {
  // Basic Greek AFM (tax number) validation
  return /^\d{9}$/.test(afm.replace(/\s/g, ""));
};

export const validateGreekPhone = (phone: string): boolean => {
  // Greek phone number validation (mobile and landline)
  const cleanPhone = phone.replace(/\s|-|\(|\)/g, "");
  return /^(\+30|0030|30)?[26-9]\d{8}$/.test(cleanPhone);
};

// Format utilities
export const formatCurrency = (amount: number, currency = "EUR"): string => {
  return new Intl.NumberFormat("el-GR", {
    style: "currency",
    currency,
  }).format(amount);
};

export const formatDate = (date: Date | string): string => {
  const dateObj = typeof date === "string" ? new Date(date) : date;
  return new Intl.DateTimeFormat("el-GR").format(dateObj);
};

export const formatAFM = (afm: string): string => {
  // Format Greek AFM with spaces: 9 -> 123 456 789
  const cleaned = afm.replace(/\s/g, "");
  return cleaned.replace(/(\d{3})(\d{3})(\d{3})/, "$1 $2 $3");
};
