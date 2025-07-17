/**
 * Translation Context for Multilingual Support
 * Provides translation functions and language management
 */

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
} from "react";
import {
  Language,
  TranslationContextValue,
  TranslationOptions,
  LanguageResources,
  UserLanguagePreferences,
} from "../types";

// Default translation resources (will be loaded from JSON files)
const DEFAULT_RESOURCES: LanguageResources = {
  el: {
    common: {
      loading: "Φόρτωση...",
      error: "Σφάλμα",
      success: "Επιτυχία",
      cancel: "Ακύρωση",
      confirm: "Επιβεβαίωση",
      save: "Αποθήκευση",
      edit: "Επεξεργασία",
      delete: "Διαγραφή",
      close: "Κλείσιμο",
      back: "Πίσω",
      next: "Επόμενο",
      previous: "Προηγούμενο",
      search: "Αναζήτηση",
      filter: "Φίλτρο",
      sort: "Ταξινόμηση",
      required: "Υποχρεωτικό",
      optional: "Προαιρετικό",
      select: "Επιλογή",
      select_option: "Επιλέξτε μια επιλογή",
      no_results: "Δεν βρέθηκαν αποτελέσματα",
      clear_all: "Καθαρισμός όλων",
      retry: "Δοκιμή ξανά",
    },
    forms: {
      field_required: "Το πεδίο είναι υποχρεωτικό",
      invalid_email: "Μη έγκυρη διεύθυνση email",
      invalid_phone: "Μη έγκυρος αριθμός τηλεφώνου",
      invalid_afm: "Μη έγκυρος αριθμός ΑΦΜ",
      invalid_doy: "Μη έγκυρος κωδικός ΔΟΥ",
      invalid_postal_code: "Μη έγκυρος ταχυδρομικός κώδικας",
      invalid_iban: "Μη έγκυρος αριθμός IBAN",
      min_length: "Ελάχιστο μήκος: {{count}} χαρακτήρες",
      max_length: "Μέγιστο μήκος: {{count}} χαρακτήρες",
      min_value: "Ελάχιστη τιμή: {{value}}",
      max_value: "Μέγιστη τιμή: {{value}}",
    },
    greek: {
      afm_label: "Α.Φ.Μ.",
      afm_placeholder: "Εισάγετε τον Α.Φ.Μ.",
      doy_label: "Δ.Ο.Υ.",
      doy_placeholder: "Επιλέξτε Δ.Ο.Υ.",
      phone_label: "Τηλέφωνο",
      phone_placeholder: "Εισάγετε τον αριθμό τηλεφώνου",
      address_label: "Διεύθυνση",
      region_label: "Περιφέρεια",
      postal_code_label: "Τ.Κ.",
      city_label: "Πόλη",
      street_label: "Οδός",
      street_number_label: "Αριθμός",
      legal_form_label: "Νομική Μορφή",
      business_activity_label: "Δραστηριότητα",
      bank_label: "Τράπεζα",
      iban_label: "IBAN",
      vat_rate_label: "Συντελεστής Φ.Π.Α.",
    },
    navigation: {
      dashboard: "Κεντρικός Πίνακας",
      customers: "Πελάτες",
      suppliers: "Προμηθευτές",
      products: "Προϊόντα",
      invoices: "Τιμολόγια",
      reports: "Αναφορές",
      test_flow: "Δοκιμαστική Ροή",
      settings: "Ρυθμίσεις",
      app_name: "Axiologic",
      welcome_user: "Καλώς ήρθατε, {{name}}",
      logout: "Αποσύνδεση",
      logging_out: "Αποσύνδεση...",
      access_denied: "Δεν έχετε πρόσβαση. Επικοινωνήστε με τον διαχειριστή.",
    },
    dashboard: {
      welcome_user: "Καλώς ήρθατε, {{name}}!",
      company_overview:
        "Επισκόπηση της επιχείρησής σας • Εταιρεία: {{company}}",
      company_not_set: "Δεν έχει οριστεί",
      development_progress: "Πρόοδος Ανάπτυξης",
      milestone_1_progress: "Milestone 1: CRM + Τιμολόγηση (Ολοκληρώθηκε 75%)",
      erp_core_next: "ERP Core: Αποθέματα + Οικονομικά (Επόμενο)",
      total_customers: "Συνολικοί Πελάτες",
      monthly_invoices: "Μηνιαία Τιμολόγια",
      monthly_revenue: "Μηνιαίος Τζίρος",
      active_opportunities: "Ενεργές Ευκαιρίες",
      recent_activities: "Πρόσφατες Δραστηριότητες",
      quick_actions: "Γρήγορες Ενέργειες",
      new_invoice: "Νέο Τιμολόγιο",
      new_invoice_desc: "Δημιουργία και αποστολή στο AADE",
      new_customer: "Νέος Πελάτης",
      new_customer_desc: "Καταχώρηση επιχείρησης/προμηθευτή",
      new_opportunity: "Νέα Ευκαιρία",
      new_opportunity_desc: "Καταχώρηση ευκαιρίας πώλησης",
      // Error messages
      error_loading_stats: "Σφάλμα φόρτωσης στατιστικών",
      data_temporarily_unavailable: "Δεδομένα προσωρινά μη διαθέσιμα",
      retry_in_moment: "Δοκιμάστε ξανά σε λίγο",
      contact_support: "Επικοινωνήστε με την υποστήριξη",
      loading_stats: "Φόρτωση στατιστικών...",
      stats_unavailable: "Στατιστικά μη διαθέσιμα",
      schedule: "Προγραμματισμός",
      schedule_desc: "Νέο ραντεβού ή δραστηριότητα",
      system_modules: "Μονάδες Συστήματος - Roadmap Ανάπτυξης",
      milestone_1_title: "Milestone 1: CRM + Τιμολόγηση",
      milestone_1_desc: "Βασικές επιχειρηματικές λειτουργίες",
      erp_core_title: "ERP Core: Αποθέματα + Οικονομικά",
      erp_core_desc: "Ολοκληρωμένη επιχειρησιακή διαχείριση",
      erp_expansion_title: "ERP Expansion: Προηγμένες Λειτουργίες",
      erp_expansion_desc: "Προηγμένες αναλύσεις & αυτοματισμοί",
      module_active: "Ενεργό",
      module_developing: "Ανάπτυξη",
      module_planned: "Προγραμματισμένο",
      open_module: "Άνοιγμα μονάδας",
      in_development: "Σε ανάπτυξη",
      next_phase: "Επόμενη φάση",
      view_all_activities: "Δείτε όλες τις δραστηριότητες →",
      no_recent_activities: "Δεν υπάρχουν πρόσφατες δραστηριότητες",
      no_recent_activities_desc:
        "Όταν δημιουργήσετε τιμολόγια, πελάτες ή άλλες δραστηριότητες, θα εμφανιστούν εδώ",
      error_loading_activities: "Σφάλμα φόρτωσης δραστηριοτήτων",
      business_management: "Διαχείριση Επιχειρήσεων",
      business_management_desc: "Πελάτες, προμηθευτές, επαφές & σχέσεις",
      greek_invoicing: "Ελληνική Τιμολόγηση",
      greek_invoicing_desc: "16 είδη παραστατικών & AADE ενσωμάτωση",
      sales_pipeline: "Πωλήσεις & Pipeline",
      sales_pipeline_desc: "Ευκαιρίες, προσφορές & πρόβλεψη πωλήσεων",
      product_catalog: "Κατάλογος Προϊόντων",
      product_catalog_desc: "Προϊόντα, υπηρεσίες & τιμολόγηση",
      inventory_management: "Διαχείριση Αποθέματος",
      inventory_management_desc: "Αποθήκες, κίνηση & αυτοματισμοί",
      financial_management: "Οικονομική Διαχείριση",
      financial_management_desc: "Λογιστική, ταμείο & χρηματοροές",
      business_analytics: "Επιχειρηματικές Αναλύσεις",
      business_analytics_desc: "Dashboards, KPIs & προβλέψεις",
      aade_compliance: "AADE Συμμόρφωση",
      aade_compliance_desc: "MyDATA, φορολογικές υποχρεώσεις",
      hr_management: "Διαχείριση Προσωπικού",
      hr_management_desc: "HR, μισθοδοσία & παρουσίες",
      multi_company_security: "Πολυ-εταιρικό σύστημα ασφαλείας ✓",
      axiologic_integrated: "Axiologic - Ενοποιημένη Επιχειρηματική Διαχείριση",
      development_phases:
        "Milestone 1: CRM + Τιμολόγηση • ERP Core: Αποθέματα + Οικονομικά • ERP Expansion: HR + Analytics",
    },
    auth: {
      welcome: "Καλώς ήρθατε",
      sign_in_prompt: "Συνδεθείτε στον λογαριασμό σας",
      company_description: "Διαχείριση πελατών και επιχειρήσεων",
      all_rights_reserved: "Όλα τα δικαιώματα κατοχυρωμένα.",
      select_language: "Επιλογή γλώσσας",
      select_theme: "Επιλογή θέματος",
    },
  },
  en: {
    common: {
      loading: "Loading...",
      error: "Error",
      success: "Success",
      cancel: "Cancel",
      confirm: "Confirm",
      save: "Save",
      edit: "Edit",
      delete: "Delete",
      close: "Close",
      back: "Back",
      next: "Next",
      previous: "Previous",
      search: "Search",
      filter: "Filter",
      sort: "Sort",
      required: "Required",
      optional: "Optional",
      select: "Select",
      select_option: "Select an option",
      no_results: "No results found",
      clear_all: "Clear all",
      retry: "Try again",
    },
    forms: {
      field_required: "Field is required",
      invalid_email: "Invalid email address",
      invalid_phone: "Invalid phone number",
      invalid_afm: "Invalid AFM number",
      invalid_doy: "Invalid DOY code",
      invalid_postal_code: "Invalid postal code",
      invalid_iban: "Invalid IBAN number",
      min_length: "Minimum length: {{count}} characters",
      max_length: "Maximum length: {{count}} characters",
      min_value: "Minimum value: {{value}}",
      max_value: "Maximum value: {{value}}",
    },
    greek: {
      afm_label: "Tax Number (AFM)",
      afm_placeholder: "Enter tax number",
      doy_label: "Tax Office (DOY)",
      doy_placeholder: "Select tax office",
      phone_label: "Phone",
      phone_placeholder: "Enter phone number",
      address_label: "Address",
      region_label: "Region",
      postal_code_label: "Postal Code",
      city_label: "City",
      street_label: "Street",
      street_number_label: "Number",
      legal_form_label: "Legal Form",
      business_activity_label: "Business Activity",
      bank_label: "Bank",
      iban_label: "IBAN",
      vat_rate_label: "VAT Rate",
    },
    navigation: {
      dashboard: "Dashboard",
      customers: "Customers",
      suppliers: "Suppliers",
      products: "Products",
      invoices: "Invoices",
      reports: "Reports",
      test_flow: "Test Workflow",
      settings: "Settings",
      app_name: "Axiologic",
      welcome_user: "Welcome, {{name}}",
      logout: "Logout",
      logging_out: "Logging out...",
      access_denied: "Access denied. Please contact your administrator.",
    },
    dashboard: {
      welcome_user: "Welcome, {{name}}!",
      company_overview: "Business overview • Company: {{company}}",
      company_not_set: "Not set",
      development_progress: "Development Progress",
      milestone_1_progress: "Milestone 1: CRM + Invoicing (75% Complete)",
      erp_core_next: "ERP Core: Inventory + Finance (Next)",
      total_customers: "Total Customers",
      monthly_invoices: "Monthly Invoices",
      monthly_revenue: "Monthly Revenue",
      active_opportunities: "Active Opportunities",
      recent_activities: "Recent Activities",
      quick_actions: "Quick Actions",
      new_invoice: "New Invoice",
      new_invoice_desc: "Create and send to AADE",
      new_customer: "New Customer",
      new_customer_desc: "Register business/supplier",
      new_opportunity: "New Opportunity",
      new_opportunity_desc: "Register sales opportunity",
      // Error messages
      error_loading_stats: "Error loading statistics",
      data_temporarily_unavailable: "Data temporarily unavailable",
      retry_in_moment: "Please try again in a moment",
      contact_support: "Contact support if the problem persists",
      loading_stats: "Loading statistics...",
      stats_unavailable: "Statistics unavailable",
      schedule: "Schedule",
      schedule_desc: "New appointment or activity",
      system_modules: "System Modules - Development Roadmap",
      milestone_1_title: "Milestone 1: CRM + Invoicing",
      milestone_1_desc: "Core business operations",
      erp_core_title: "ERP Core: Inventory + Finance",
      erp_core_desc: "Integrated business management",
      erp_expansion_title: "ERP Expansion: Advanced Features",
      erp_expansion_desc: "Advanced analytics & automation",
      module_active: "Active",
      module_developing: "Development",
      module_planned: "Planned",
      open_module: "Open module",
      in_development: "In development",
      next_phase: "Next phase",
      view_all_activities: "View all activities →",
      no_recent_activities: "No recent activities",
      no_recent_activities_desc:
        "When you create invoices, customers, or other activities, they will appear here",
      error_loading_activities: "Error loading activities",
      business_management: "Business Management",
      business_management_desc:
        "Customers, suppliers, contacts & relationships",
      greek_invoicing: "Greek Invoicing",
      greek_invoicing_desc: "16 document types & AADE integration",
      sales_pipeline: "Sales & Pipeline",
      sales_pipeline_desc: "Opportunities, quotes & sales forecasting",
      product_catalog: "Product Catalog",
      product_catalog_desc: "Products, services & pricing",
      inventory_management: "Inventory Management",
      inventory_management_desc: "Warehouses, movement & automation",
      financial_management: "Financial Management",
      financial_management_desc: "Accounting, cash flow & finance",
      business_analytics: "Business Analytics",
      business_analytics_desc: "Dashboards, KPIs & forecasting",
      aade_compliance: "AADE Compliance",
      aade_compliance_desc: "MyDATA, tax obligations",
      hr_management: "HR Management",
      hr_management_desc: "HR, payroll & attendance",
      multi_company_security: "Multi-company security system ✓",
      axiologic_integrated: "Axiologic - Integrated Business Management",
      development_phases:
        "Milestone 1: CRM + Invoicing • ERP Core: Inventory + Finance • ERP Expansion: HR + Analytics",
    },
    auth: {
      welcome: "Welcome",
      sign_in_prompt: "Sign in to your account",
      company_description: "Customer and Business Management",
      all_rights_reserved: "All rights reserved.",
      select_language: "Select language",
      select_theme: "Select theme",
    },
  },
};

// Translation context
const TranslationContext = createContext<TranslationContextValue | null>(null);

// Storage keys
const LANGUAGE_STORAGE_KEY = "ui_language";
const PREFERENCES_STORAGE_KEY = "ui_language_preferences";

// Language detection utilities
const detectLanguageFromPath = (): Language | null => {
  const path = window.location.pathname;
  const pathLang = path.split("/")[1];
  return pathLang === "el" || pathLang === "en" ? pathLang : null;
};

const detectLanguageFromNavigator = (): Language | null => {
  const browserLang = navigator.language || navigator.languages?.[0];
  if (browserLang?.startsWith("el")) return "el";
  if (browserLang?.startsWith("en")) return "en";
  return null;
};

const detectLanguageFromHeaders = (): Language | null => {
  // For SSR, this would check Accept-Language header
  // For now, we'll use navigator as fallback
  return detectLanguageFromNavigator();
};

// Translation utilities
const interpolateString = (
  str: string,
  variables?: Record<string, string | number>
): string => {
  if (!variables) return str;

  return str.replace(/\{\{(\w+)\}\}/g, (match, key) => {
    return String(variables[key] || match);
  });
};

const getNestedValue = (obj: any, path: string): string | undefined => {
  return path.split(".").reduce((current, key) => current?.[key], obj);
};

// Translation provider component
interface TranslationProviderProps {
  children: React.ReactNode;
  defaultLanguage?: Language;
  resources?: LanguageResources;
  detectLanguage?: boolean;
  storageKey?: string;
  fallbackLanguage?: Language;
}

export const TranslationProvider: React.FC<TranslationProviderProps> = ({
  children,
  defaultLanguage = "el",
  resources = DEFAULT_RESOURCES,
  detectLanguage = true,
  storageKey = LANGUAGE_STORAGE_KEY,
  fallbackLanguage = "en",
}) => {
  // Initialize language with stable SSR value
  const [language, setLanguageState] = useState<Language>(defaultLanguage);
  const [translationResources, setTranslationResources] =
    useState<LanguageResources>(resources);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>(undefined);
  const [isClient, setIsClient] = useState(false);

  // Fix hydration mismatch by updating language after mount
  useEffect(() => {
    setIsClient(true);

    // Only check stored/detected language after client mount
    if (typeof window !== "undefined") {
      // Try to get from localStorage first
      const stored = localStorage.getItem(storageKey);
      if (stored && (stored === "el" || stored === "en")) {
        setLanguageState(stored as Language);
        return;
      }

      // Auto-detect language if enabled
      if (detectLanguage) {
        const detected =
          detectLanguageFromPath() ||
          detectLanguageFromHeaders() ||
          detectLanguageFromNavigator();

        if (detected) {
          localStorage.setItem(storageKey, detected);
          setLanguageState(detected);
          return;
        }
      }
    }
  }, [detectLanguage, storageKey]);

  // Language preferences
  const [preferences, setPreferences] = useState<UserLanguagePreferences>(
    () => {
      if (typeof window === "undefined") {
        return {
          primaryLanguage: language,
          fallbackLanguage: fallbackLanguage,
          dateFormat: "dd/MM/yyyy",
          numberFormat: "european",
          currency: "EUR",
          timezone: "Europe/Athens",
        };
      }

      const stored = localStorage.getItem(PREFERENCES_STORAGE_KEY);
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch {
          // Fall through to defaults
        }
      }

      return {
        primaryLanguage: language,
        fallbackLanguage: fallbackLanguage,
        dateFormat: "dd/MM/yyyy",
        numberFormat: "european",
        currency: "EUR",
        timezone: "Europe/Athens",
      };
    }
  );

  // Update language and persist to storage
  const setLanguage = useCallback(
    (newLanguage: Language) => {
      setLanguageState(newLanguage);
      localStorage.setItem(storageKey, newLanguage);

      // Update preferences
      setPreferences((prev) => ({
        ...prev,
        primaryLanguage: newLanguage,
      }));
    },
    [storageKey]
  );

  // Translation function
  const t = useCallback(
    (key: string, options?: TranslationOptions): string => {
      const {
        ns = "common",
        defaultValue = key,
        variables,
        count,
      } = options || {};

      try {
        // Get translation from current language
        const currentLangResources = translationResources[language];
        if (currentLangResources) {
          const namespace = currentLangResources[ns];
          if (namespace) {
            const value = getNestedValue(namespace, key);
            if (value) {
              // Handle pluralization
              if (count !== undefined && typeof count === "number") {
                // Simple pluralization logic - can be extended
                const pluralKey = count === 1 ? key : `${key}_plural`;
                const pluralValue = getNestedValue(namespace, pluralKey);
                if (pluralValue) {
                  return interpolateString(pluralValue, {
                    ...variables,
                    count,
                  });
                }
              }

              return interpolateString(value, variables);
            }
          }
        }

        // Fallback to fallback language
        const fallbackLangResources = translationResources[fallbackLanguage];
        if (fallbackLangResources) {
          const namespace = fallbackLangResources[ns];
          if (namespace) {
            const value = getNestedValue(namespace, key);
            if (value) {
              return interpolateString(value, variables);
            }
          }
        }

        // Return default value or key
        return interpolateString(defaultValue, variables);
      } catch (err) {
        console.warn(`Translation error for key "${key}":`, err);
        return defaultValue;
      }
    },
    [language, translationResources, fallbackLanguage]
  );

  // Save preferences to localStorage
  useEffect(() => {
    localStorage.setItem(PREFERENCES_STORAGE_KEY, JSON.stringify(preferences));
  }, [preferences]);

  // Context value
  const contextValue = useMemo<TranslationContextValue>(
    () => ({
      language,
      setLanguage,
      t,
      resources: translationResources,
      isLoading,
      error,
    }),
    [language, setLanguage, t, translationResources, isLoading, error]
  );

  return (
    <TranslationContext.Provider value={contextValue}>
      {children}
    </TranslationContext.Provider>
  );
};

// Hook to use translation context
export const useTranslation = () => {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error("useTranslation must be used within a TranslationProvider");
  }
  return context;
};

// Hook to get current language and setter
export const useLanguage = () => {
  const { language, setLanguage } = useTranslation();
  return { language, setLanguage };
};

// Hook to get translation function with namespace
export const useTranslationNamespace = (namespace: string) => {
  const { t } = useTranslation();
  return useCallback(
    (key: string, options?: Omit<TranslationOptions, "ns">) => {
      return t(key, { ...options, ns: namespace });
    },
    [t, namespace]
  );
};
