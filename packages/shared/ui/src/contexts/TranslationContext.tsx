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
  // Initialize language with detection
  const [language, setLanguageState] = useState<Language>(() => {
    if (typeof window === "undefined") return defaultLanguage;

    // Try to get from localStorage first
    const stored = localStorage.getItem(storageKey);
    if (stored && (stored === "el" || stored === "en")) {
      return stored as Language;
    }

    // Auto-detect language if enabled
    if (detectLanguage) {
      const detected =
        detectLanguageFromPath() ||
        detectLanguageFromHeaders() ||
        detectLanguageFromNavigator();

      if (detected) {
        localStorage.setItem(storageKey, detected);
        return detected;
      }
    }

    return defaultLanguage;
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();

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
        const currentLangResources = resources[language];
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
        const fallbackLangResources = resources[fallbackLanguage];
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
    [language, resources, fallbackLanguage]
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
      resources,
      isLoading,
      error,
    }),
    [language, setLanguage, t, resources, isLoading, error]
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
