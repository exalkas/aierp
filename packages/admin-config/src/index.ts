// Greek ERP/CRM - Admin Config Module

// Configuration types
export interface SystemConfig {
  id: string;
  key: string;
  value: any;
  type: "string" | "number" | "boolean" | "object" | "array";
  description: string;
  category: string;
  isPublic: boolean;
  isReadOnly: boolean;
  validationRules?: ValidationRule[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ValidationRule {
  type: "required" | "min" | "max" | "pattern" | "email" | "url";
  value?: any;
  message: string;
}

export interface CompanyConfig {
  id: string;
  companyId: string;
  settings: Record<string, any>;
  theme: ThemeConfig;
  localization: LocalizationConfig;
  integrations: IntegrationConfig[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ThemeConfig {
  primaryColor: string;
  secondaryColor: string;
  logo?: string;
  favicon?: string;
  customCss?: string;
}

export interface LocalizationConfig {
  defaultLanguage: "el" | "en";
  timezone: string;
  currency: string;
  dateFormat: string;
  numberFormat: string;
}

export interface IntegrationConfig {
  id: string;
  name: string;
  type: "aade" | "banking" | "email" | "sms" | "webhook";
  settings: Record<string, any>;
  isEnabled: boolean;
  isConfigured: boolean;
}

// Config utilities
export const createSystemConfig = (
  data: Partial<SystemConfig>
): SystemConfig => {
  const now = new Date();
  return {
    id: `config_${Date.now()}`,
    key: data.key || "",
    value: data.value,
    type: data.type || "string",
    description: data.description || "",
    category: data.category || "general",
    isPublic: data.isPublic !== undefined ? data.isPublic : false,
    isReadOnly: data.isReadOnly !== undefined ? data.isReadOnly : false,
    validationRules: data.validationRules || [],
    createdAt: now,
    updatedAt: now,
  };
};

export const getDefaultConfigs = (): SystemConfig[] => {
  return [
    {
      id: "app-name",
      key: "app.name",
      value: "Greek ERP/CRM",
      type: "string",
      description: "Application name",
      category: "general",
      isPublic: true,
      isReadOnly: false,
      createdAt: new Date(),
      updatedAt: new Date(),
    },
    {
      id: "max-upload-size",
      key: "upload.maxSize",
      value: 10485760, // 10MB
      type: "number",
      description: "Maximum file upload size in bytes",
      category: "files",
      isPublic: false,
      isReadOnly: false,
      createdAt: new Date(),
      updatedAt: new Date(),
    },
  ];
};

export const validateConfig = (config: SystemConfig): boolean => {
  if (!config.validationRules) return true;

  for (const rule of config.validationRules) {
    switch (rule.type) {
      case "required":
        if (!config.value) return false;
        break;
      case "min":
        if (typeof config.value === "number" && config.value < rule.value)
          return false;
        break;
      case "max":
        if (typeof config.value === "number" && config.value > rule.value)
          return false;
        break;
      case "pattern":
        if (
          typeof config.value === "string" &&
          !new RegExp(rule.value).test(config.value)
        )
          return false;
        break;
      case "email":
        if (
          typeof config.value === "string" &&
          !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(config.value)
        )
          return false;
        break;
    }
  }

  return true;
};
