import React, {
  createContext,
  useContext,
  useReducer,
  useEffect,
  ReactNode,
} from "react";

export interface ColorPalette {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  success: string;
  warning: string;
  error: string;
  info: string;
  disabled: string;
  hover: string;
  focus: string;
  active: string;
}

export interface MaritimeTheme {
  name: string;
  colors: ColorPalette;
  typography: {
    fontFamily: string;
    fontSize: {
      xs: string;
      sm: string;
      md: string;
      lg: string;
      xl: string;
      xxl: string;
    };
    fontWeight: {
      light: number;
      normal: number;
      medium: number;
      semibold: number;
      bold: number;
    };
    lineHeight: {
      tight: number;
      normal: number;
      relaxed: number;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    xxl: string;
  };
  borderRadius: {
    none: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    full: string;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  breakpoints: {
    mobile: string;
    tablet: string;
    desktop: string;
    wide: string;
  };
  animations: {
    duration: {
      fast: string;
      medium: string;
      slow: string;
    };
    easing: {
      ease: string;
      easeIn: string;
      easeOut: string;
      easeInOut: string;
    };
  };
  components: {
    button: {
      padding: string;
      borderRadius: string;
      fontSize: string;
      fontWeight: number;
    };
    input: {
      padding: string;
      borderRadius: string;
      fontSize: string;
      borderWidth: string;
    };
    card: {
      padding: string;
      borderRadius: string;
      shadow: string;
    };
    modal: {
      borderRadius: string;
      shadow: string;
      backdrop: string;
    };
  };
  greek: {
    colors: {
      blue: string; // Greek flag blue
      white: string; // Greek flag white
      gold: string; // Greek heritage gold
      olive: string; // Greek olive green
      marble: string; // Greek marble white
      aegean: string; // Aegean sea blue
      mediterranean: string; // Mediterranean blue
    };
    patterns: {
      meander: string; // Greek key pattern
      wave: string; // Wave pattern
      column: string; // Column pattern
    };
    cultural: {
      fontFamily: string; // Greek-compatible font
      iconStyle: string; // Greek icon style
      ornaments: string[]; // Greek ornamental elements
    };
  };
}

export interface ThemeSettings {
  mode: "light" | "dark" | "auto";
  theme: "maritime" | "classic" | "modern" | "greek" | "custom";
  compactMode: boolean;
  highContrast: boolean;
  reducedMotion: boolean;
  colorBlindSupport: boolean;
  fontSize: "small" | "medium" | "large";
  customizations: {
    primaryColor?: string;
    secondaryColor?: string;
    accentColor?: string;
    fontFamily?: string;
    borderRadius?: string;
    spacing?: string;
  };
  accessibility: {
    screenReader: boolean;
    keyboardNavigation: boolean;
    focusVisible: boolean;
    announcements: boolean;
  };
  performance: {
    animationsEnabled: boolean;
    transitionsEnabled: boolean;
    shadowsEnabled: boolean;
    gradientsEnabled: boolean;
  };
  regional: {
    language: "el" | "en";
    rtl: boolean;
    greekTypography: boolean;
    culturalElements: boolean;
  };
}

interface ThemeContextState {
  currentTheme: MaritimeTheme;
  availableThemes: MaritimeTheme[];
  settings: ThemeSettings;
  systemPreference: "light" | "dark";
  loading: boolean;
  error: string | null;
  customTheme: Partial<MaritimeTheme> | null;
  themeHistory: string[];
  preferences: {
    userId: string;
    savedThemes: string[];
    lastUsed: string;
    autoSwitch: boolean;
    syncAcrossDevices: boolean;
  };
}

type ThemeAction =
  | { type: "SET_THEME"; payload: MaritimeTheme }
  | { type: "SET_THEME_BY_NAME"; payload: string }
  | { type: "SET_SETTINGS"; payload: Partial<ThemeSettings> }
  | { type: "SET_SYSTEM_PREFERENCE"; payload: "light" | "dark" }
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_ERROR"; payload: string | null }
  | { type: "SET_CUSTOM_THEME"; payload: Partial<MaritimeTheme> | null }
  | { type: "ADD_TO_HISTORY"; payload: string }
  | { type: "CLEAR_HISTORY" }
  | {
      type: "UPDATE_PREFERENCES";
      payload: Partial<ThemeContextState["preferences"]>;
    }
  | { type: "TOGGLE_MODE" }
  | { type: "TOGGLE_COMPACT_MODE" }
  | { type: "TOGGLE_HIGH_CONTRAST" }
  | { type: "TOGGLE_REDUCED_MOTION" }
  | { type: "RESET_THEME" };

// Maritime theme definitions
const maritimeTheme: MaritimeTheme = {
  name: "maritime",
  colors: {
    primary: "#0066CC", // Ocean blue
    secondary: "#003366", // Deep sea blue
    accent: "#FFF700", // Signal yellow
    background: "#F8FAFC", // Light gray
    surface: "#FFFFFF", // White
    text: "#1E293B", // Dark gray
    textSecondary: "#64748B", // Medium gray
    border: "#E2E8F0", // Light border
    success: "#22C55E", // Green
    warning: "#F59E0B", // Amber
    error: "#EF4444", // Red
    info: "#3B82F6", // Blue
    disabled: "#9CA3AF", // Gray
    hover: "#0052A3", // Darker blue
    focus: "#0066CC", // Primary blue
    active: "#003D7A", // Darkest blue
  },
  typography: {
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontSize: {
      xs: "0.75rem",
      sm: "0.875rem",
      md: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      xxl: "1.5rem",
    },
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  spacing: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem",
    xxl: "3rem",
  },
  borderRadius: {
    none: "0",
    sm: "0.125rem",
    md: "0.375rem",
    lg: "0.5rem",
    xl: "0.75rem",
    full: "9999px",
  },
  shadows: {
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
    xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
  },
  breakpoints: {
    mobile: "640px",
    tablet: "768px",
    desktop: "1024px",
    wide: "1280px",
  },
  animations: {
    duration: {
      fast: "150ms",
      medium: "300ms",
      slow: "500ms",
    },
    easing: {
      ease: "cubic-bezier(0.4, 0, 0.2, 1)",
      easeIn: "cubic-bezier(0.4, 0, 1, 1)",
      easeOut: "cubic-bezier(0, 0, 0.2, 1)",
      easeInOut: "cubic-bezier(0.4, 0, 0.2, 1)",
    },
  },
  components: {
    button: {
      padding: "0.5rem 1rem",
      borderRadius: "0.375rem",
      fontSize: "0.875rem",
      fontWeight: 500,
    },
    input: {
      padding: "0.5rem 0.75rem",
      borderRadius: "0.375rem",
      fontSize: "0.875rem",
      borderWidth: "1px",
    },
    card: {
      padding: "1.5rem",
      borderRadius: "0.5rem",
      shadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    },
    modal: {
      borderRadius: "0.75rem",
      shadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
      backdrop: "rgba(0, 0, 0, 0.5)",
    },
  },
  greek: {
    colors: {
      blue: "#0D5EAF", // Greek flag blue
      white: "#FFFFFF", // Greek flag white
      gold: "#FFD700", // Greek heritage gold
      olive: "#808000", // Greek olive green
      marble: "#F8F8FF", // Greek marble white
      aegean: "#1E90FF", // Aegean sea blue
      mediterranean: "#006994", // Mediterranean blue
    },
    patterns: {
      meander:
        'url("data:image/svg+xml,%3Csvg width="20" height="20" viewBox="0 0 20 20"%3E%3Cpath d="M0 0h20v20H0z" fill="none"/%3E%3C/svg%3E")',
      wave: 'url("data:image/svg+xml,%3Csvg width="40" height="40" viewBox="0 0 40 40"%3E%3Cpath d="M0 20c10 0 10-20 20-20s10 20 20 20v20H0z" fill="rgba(13,94,175,0.1)"/%3E%3C/svg%3E")',
      column:
        'url("data:image/svg+xml,%3Csvg width="30" height="30" viewBox="0 0 30 30"%3E%3Crect width="30" height="30" fill="none"/%3E%3C/svg%3E")',
    },
    cultural: {
      fontFamily: '"Noto Sans", "Roboto", sans-serif',
      iconStyle: "outlined",
      ornaments: ["🏛️", "🌊", "🫒", "☀️", "🏺"],
    },
  },
};

// Dark theme variant
const darkMaritimeTheme: MaritimeTheme = {
  ...maritimeTheme,
  name: "maritime-dark",
  colors: {
    ...maritimeTheme.colors,
    primary: "#3B82F6", // Lighter blue for dark mode
    secondary: "#1E40AF", // Medium blue
    background: "#0F172A", // Dark background
    surface: "#1E293B", // Dark surface
    text: "#F1F5F9", // Light text
    textSecondary: "#94A3B8", // Medium light text
    border: "#374151", // Dark border
    disabled: "#6B7280", // Darker gray
    hover: "#2563EB", // Hover blue
    focus: "#3B82F6", // Focus blue
    active: "#1D4ED8", // Active blue
  },
};

const defaultSettings: ThemeSettings = {
  mode: "auto",
  theme: "maritime",
  compactMode: false,
  highContrast: false,
  reducedMotion: false,
  colorBlindSupport: false,
  fontSize: "medium",
  customizations: {},
  accessibility: {
    screenReader: false,
    keyboardNavigation: true,
    focusVisible: true,
    announcements: true,
  },
  performance: {
    animationsEnabled: true,
    transitionsEnabled: true,
    shadowsEnabled: true,
    gradientsEnabled: true,
  },
  regional: {
    language: "en",
    rtl: false,
    greekTypography: false,
    culturalElements: true,
  },
};

const initialState: ThemeContextState = {
  currentTheme: maritimeTheme,
  availableThemes: [maritimeTheme, darkMaritimeTheme],
  settings: defaultSettings,
  systemPreference: "light",
  loading: false,
  error: null,
  customTheme: null,
  themeHistory: [],
  preferences: {
    userId: "",
    savedThemes: [],
    lastUsed: "maritime",
    autoSwitch: false,
    syncAcrossDevices: false,
  },
};

function themeReducer(
  state: ThemeContextState,
  action: ThemeAction
): ThemeContextState {
  switch (action.type) {
    case "SET_THEME":
      return {
        ...state,
        currentTheme: action.payload,
        themeHistory: [action.payload.name, ...state.themeHistory.slice(0, 9)],
      };

    case "SET_THEME_BY_NAME":
      const theme = state.availableThemes.find(
        (t) => t.name === action.payload
      );
      if (theme) {
        return {
          ...state,
          currentTheme: theme,
          themeHistory: [action.payload, ...state.themeHistory.slice(0, 9)],
        };
      }
      return state;

    case "SET_SETTINGS":
      return { ...state, settings: { ...state.settings, ...action.payload } };

    case "SET_SYSTEM_PREFERENCE":
      return { ...state, systemPreference: action.payload };

    case "SET_LOADING":
      return { ...state, loading: action.payload };

    case "SET_ERROR":
      return { ...state, error: action.payload };

    case "SET_CUSTOM_THEME":
      return { ...state, customTheme: action.payload };

    case "ADD_TO_HISTORY":
      return {
        ...state,
        themeHistory: [action.payload, ...state.themeHistory.slice(0, 9)],
      };

    case "CLEAR_HISTORY":
      return { ...state, themeHistory: [] };

    case "UPDATE_PREFERENCES":
      return {
        ...state,
        preferences: { ...state.preferences, ...action.payload },
      };

    case "TOGGLE_MODE":
      const newMode = state.settings.mode === "light" ? "dark" : "light";
      return {
        ...state,
        settings: { ...state.settings, mode: newMode },
        currentTheme: newMode === "dark" ? darkMaritimeTheme : maritimeTheme,
      };

    case "TOGGLE_COMPACT_MODE":
      return {
        ...state,
        settings: {
          ...state.settings,
          compactMode: !state.settings.compactMode,
        },
      };

    case "TOGGLE_HIGH_CONTRAST":
      return {
        ...state,
        settings: {
          ...state.settings,
          highContrast: !state.settings.highContrast,
        },
      };

    case "TOGGLE_REDUCED_MOTION":
      return {
        ...state,
        settings: {
          ...state.settings,
          reducedMotion: !state.settings.reducedMotion,
        },
      };

    case "RESET_THEME":
      return {
        ...state,
        currentTheme: maritimeTheme,
        settings: defaultSettings,
        customTheme: null,
      };

    default:
      return state;
  }
}

const ThemeContext = createContext<{
  state: ThemeContextState;
  dispatch: React.Dispatch<ThemeAction>;
  // Theme management
  setTheme: (theme: MaritimeTheme | string) => void;
  setThemeByName: (name: string) => void;
  toggleMode: () => void;
  setMode: (mode: "light" | "dark" | "auto") => void;
  // Customization
  createCustomTheme: (
    baseTheme: string,
    customizations: Partial<MaritimeTheme>
  ) => void;
  applyCustomization: (
    customizations: Partial<ThemeSettings["customizations"]>
  ) => void;
  resetCustomizations: () => void;
  // Settings
  updateSettings: (settings: Partial<ThemeSettings>) => void;
  toggleCompactMode: () => void;
  toggleHighContrast: () => void;
  toggleReducedMotion: () => void;
  setFontSize: (size: "small" | "medium" | "large") => void;
  // Accessibility
  updateAccessibilitySettings: (
    settings: Partial<ThemeSettings["accessibility"]>
  ) => void;
  enableScreenReaderMode: () => void;
  enableKeyboardNavigation: () => void;
  enableHighContrast: () => void;
  // Performance
  updatePerformanceSettings: (
    settings: Partial<ThemeSettings["performance"]>
  ) => void;
  disableAnimations: () => void;
  enableAnimations: () => void;
  // Regional
  updateRegionalSettings: (
    settings: Partial<ThemeSettings["regional"]>
  ) => void;
  enableGreekTypography: () => void;
  enableRTL: () => void;
  // Utilities
  getCurrentTheme: () => MaritimeTheme;
  getThemeByName: (name: string) => MaritimeTheme | undefined;
  exportTheme: () => string;
  importTheme: (themeData: string) => void;
  // CSS generation
  generateCSS: () => string;
  generateCSSVariables: () => Record<string, string>;
  applyThemeToDocument: () => void;
  // Preferences
  savePreferences: () => void;
  loadPreferences: () => void;
  syncPreferences: () => void;
} | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(themeReducer, initialState);

  // Theme management
  const setTheme = (theme: MaritimeTheme | string) => {
    if (typeof theme === "string") {
      dispatch({ type: "SET_THEME_BY_NAME", payload: theme });
    } else {
      dispatch({ type: "SET_THEME", payload: theme });
    }
  };

  const setThemeByName = (name: string) => {
    dispatch({ type: "SET_THEME_BY_NAME", payload: name });
  };

  const toggleMode = () => {
    dispatch({ type: "TOGGLE_MODE" });
  };

  const setMode = (mode: "light" | "dark" | "auto") => {
    dispatch({ type: "SET_SETTINGS", payload: { mode } });

    if (mode === "auto") {
      const systemPreference = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
        ? "dark"
        : "light";
      dispatch({ type: "SET_SYSTEM_PREFERENCE", payload: systemPreference });
      setTheme(systemPreference === "dark" ? darkMaritimeTheme : maritimeTheme);
    } else {
      setTheme(mode === "dark" ? darkMaritimeTheme : maritimeTheme);
    }
  };

  // Customization
  const createCustomTheme = (
    baseTheme: string,
    customizations: Partial<MaritimeTheme>
  ) => {
    const base =
      state.availableThemes.find((t) => t.name === baseTheme) || maritimeTheme;
    const customTheme = {
      ...base,
      ...customizations,
      name: "custom",
    };

    dispatch({ type: "SET_CUSTOM_THEME", payload: customTheme });
    dispatch({ type: "SET_THEME", payload: customTheme });
  };

  const applyCustomization = (
    customizations: Partial<ThemeSettings["customizations"]>
  ) => {
    dispatch({ type: "SET_SETTINGS", payload: { customizations } });

    // Apply customizations to current theme
    if (customizations.primaryColor || customizations.secondaryColor) {
      const customTheme = {
        ...state.currentTheme,
        colors: {
          ...state.currentTheme.colors,
          ...(customizations.primaryColor && {
            primary: customizations.primaryColor,
          }),
          ...(customizations.secondaryColor && {
            secondary: customizations.secondaryColor,
          }),
          ...(customizations.accentColor && {
            accent: customizations.accentColor,
          }),
        },
      };

      dispatch({ type: "SET_THEME", payload: customTheme });
    }
  };

  const resetCustomizations = () => {
    dispatch({ type: "SET_SETTINGS", payload: { customizations: {} } });
    dispatch({ type: "SET_CUSTOM_THEME", payload: null });
    setTheme(maritimeTheme);
  };

  // Settings
  const updateSettings = (settings: Partial<ThemeSettings>) => {
    dispatch({ type: "SET_SETTINGS", payload: settings });
  };

  const toggleCompactMode = () => {
    dispatch({ type: "TOGGLE_COMPACT_MODE" });
  };

  const toggleHighContrast = () => {
    dispatch({ type: "TOGGLE_HIGH_CONTRAST" });
  };

  const toggleReducedMotion = () => {
    dispatch({ type: "TOGGLE_REDUCED_MOTION" });
  };

  const setFontSize = (size: "small" | "medium" | "large") => {
    dispatch({ type: "SET_SETTINGS", payload: { fontSize: size } });
  };

  // Accessibility
  const updateAccessibilitySettings = (
    settings: Partial<ThemeSettings["accessibility"]>
  ) => {
    dispatch({
      type: "SET_SETTINGS",
      payload: {
        accessibility: { ...state.settings.accessibility, ...settings },
      },
    });
  };

  const enableScreenReaderMode = () => {
    updateAccessibilitySettings({ screenReader: true });
  };

  const enableKeyboardNavigation = () => {
    updateAccessibilitySettings({ keyboardNavigation: true });
  };

  const enableHighContrast = () => {
    dispatch({ type: "SET_SETTINGS", payload: { highContrast: true } });
  };

  // Performance
  const updatePerformanceSettings = (
    settings: Partial<ThemeSettings["performance"]>
  ) => {
    dispatch({
      type: "SET_SETTINGS",
      payload: { performance: { ...state.settings.performance, ...settings } },
    });
  };

  const disableAnimations = () => {
    updatePerformanceSettings({
      animationsEnabled: false,
      transitionsEnabled: false,
    });
  };

  const enableAnimations = () => {
    updatePerformanceSettings({
      animationsEnabled: true,
      transitionsEnabled: true,
    });
  };

  // Regional
  const updateRegionalSettings = (
    settings: Partial<ThemeSettings["regional"]>
  ) => {
    dispatch({
      type: "SET_SETTINGS",
      payload: { regional: { ...state.settings.regional, ...settings } },
    });
  };

  const enableGreekTypography = () => {
    updateRegionalSettings({ greekTypography: true });
  };

  const enableRTL = () => {
    updateRegionalSettings({ rtl: true });
  };

  // Utilities
  const getCurrentTheme = () => {
    return state.currentTheme;
  };

  const getThemeByName = (name: string) => {
    return state.availableThemes.find((t) => t.name === name);
  };

  const exportTheme = () => {
    return JSON.stringify(
      {
        theme: state.currentTheme,
        settings: state.settings,
        customTheme: state.customTheme,
      },
      null,
      2
    );
  };

  const importTheme = (themeData: string) => {
    try {
      const parsed = JSON.parse(themeData);
      if (parsed.theme) {
        dispatch({ type: "SET_THEME", payload: parsed.theme });
      }
      if (parsed.settings) {
        dispatch({ type: "SET_SETTINGS", payload: parsed.settings });
      }
      if (parsed.customTheme) {
        dispatch({ type: "SET_CUSTOM_THEME", payload: parsed.customTheme });
      }
    } catch (error) {
      dispatch({ type: "SET_ERROR", payload: "Invalid theme data" });
    }
  };

  // CSS generation
  const generateCSS = () => {
    const theme = state.currentTheme;
    const settings = state.settings;

    return `
      :root {
        ${Object.entries(generateCSSVariables())
          .map(([key, value]) => `${key}: ${value};`)
          .join("\n        ")}
      }
      
      ${
        settings.compactMode
          ? `
        .compact-mode {
          --spacing-sm: 0.25rem;
          --spacing-md: 0.5rem;
          --spacing-lg: 0.75rem;
        }
      `
          : ""
      }
      
      ${
        settings.highContrast
          ? `
        .high-contrast {
          --text-color: #000000;
          --background-color: #ffffff;
          --border-color: #000000;
        }
      `
          : ""
      }
      
      ${
        settings.reducedMotion
          ? `
        .reduced-motion *,
        .reduced-motion *::before,
        .reduced-motion *::after {
          animation-duration: 0.01ms !important;
          animation-iteration-count: 1 !important;
          transition-duration: 0.01ms !important;
        }
      `
          : ""
      }
    `;
  };

  const generateCSSVariables = () => {
    const theme = state.currentTheme;
    const variables: Record<string, string> = {};

    // Colors
    Object.entries(theme.colors).forEach(([key, value]) => {
      variables[`--color-${key}`] = value;
    });

    // Typography
    Object.entries(theme.typography.fontSize).forEach(([key, value]) => {
      variables[`--font-size-${key}`] = value;
    });

    // Spacing
    Object.entries(theme.spacing).forEach(([key, value]) => {
      variables[`--spacing-${key}`] = value;
    });

    // Border radius
    Object.entries(theme.borderRadius).forEach(([key, value]) => {
      variables[`--border-radius-${key}`] = value;
    });

    // Shadows
    Object.entries(theme.shadows).forEach(([key, value]) => {
      variables[`--shadow-${key}`] = value;
    });

    return variables;
  };

  const applyThemeToDocument = () => {
    const css = generateCSS();
    const styleElement =
      document.getElementById("theme-styles") ||
      document.createElement("style");
    styleElement.id = "theme-styles";
    styleElement.textContent = css;

    if (!document.getElementById("theme-styles")) {
      document.head.appendChild(styleElement);
    }

    // Apply theme classes to document
    document.documentElement.className = [
      state.settings.mode === "dark" ? "dark" : "light",
      state.settings.compactMode ? "compact-mode" : "",
      state.settings.highContrast ? "high-contrast" : "",
      state.settings.reducedMotion ? "reduced-motion" : "",
      state.settings.regional.rtl ? "rtl" : "ltr",
    ]
      .filter(Boolean)
      .join(" ");
  };

  // Preferences
  const savePreferences = () => {
    const preferences = {
      theme: state.currentTheme.name,
      settings: state.settings,
      customTheme: state.customTheme,
    };

    localStorage.setItem("theme-preferences", JSON.stringify(preferences));
  };

  const loadPreferences = () => {
    try {
      const saved = localStorage.getItem("theme-preferences");
      if (saved) {
        const preferences = JSON.parse(saved);
        if (preferences.settings) {
          dispatch({ type: "SET_SETTINGS", payload: preferences.settings });
        }
        if (preferences.customTheme) {
          dispatch({
            type: "SET_CUSTOM_THEME",
            payload: preferences.customTheme,
          });
        }
        if (preferences.theme) {
          setThemeByName(preferences.theme);
        }
      }
    } catch (error) {
      console.error("Failed to load theme preferences:", error);
    }
  };

  const syncPreferences = () => {
    // In a real implementation, sync with server
    savePreferences();
  };

  // Effects
  useEffect(() => {
    // Load preferences on mount
    loadPreferences();

    // Listen for system theme changes
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleChange = (e: MediaQueryListEvent) => {
      dispatch({
        type: "SET_SYSTEM_PREFERENCE",
        payload: e.matches ? "dark" : "light",
      });
      if (state.settings.mode === "auto") {
        setTheme(e.matches ? darkMaritimeTheme : maritimeTheme);
      }
    };

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  useEffect(() => {
    // Apply theme to document whenever theme changes
    applyThemeToDocument();

    // Save preferences
    savePreferences();
  }, [state.currentTheme, state.settings]);

  const contextValue = {
    state,
    dispatch,
    setTheme,
    setThemeByName,
    toggleMode,
    setMode,
    createCustomTheme,
    applyCustomization,
    resetCustomizations,
    updateSettings,
    toggleCompactMode,
    toggleHighContrast,
    toggleReducedMotion,
    setFontSize,
    updateAccessibilitySettings,
    enableScreenReaderMode,
    enableKeyboardNavigation,
    enableHighContrast,
    updatePerformanceSettings,
    disableAnimations,
    enableAnimations,
    updateRegionalSettings,
    enableGreekTypography,
    enableRTL,
    getCurrentTheme,
    getThemeByName,
    exportTheme,
    importTheme,
    generateCSS,
    generateCSSVariables,
    applyThemeToDocument,
    savePreferences,
    loadPreferences,
    syncPreferences,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}

export default ThemeContext;
