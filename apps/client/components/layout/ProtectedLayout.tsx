"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  AuthProvider,
  useAuth,
  TranslationProvider,
  useTranslation,
  ThemeProvider,
  useTheme,
  AppName,
  Sidebar,
  LanguageSelector,
  ThemeSelector,
  Logo,
} from "@erp/shared-ui";
import {
  Home,
  Users,
  Building2,
  Package,
  FileText,
  BarChart3,
  Settings,
  AlertTriangle,
  Loader2,
  LogOut,
  TestTube,
  Store,
  ChevronLeft,
  Menu,
} from "lucide-react";

// Simple mock for company context until we can fix the imports
const useCompany = () => ({
  state: {
    currentCompany: null,
  },
});

// Loading Spinner Component
function LoadingSpinner() {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
      <div className="text-center">
        <div className="mb-4 mx-auto flex justify-center">
          <Logo size="md" />
        </div>
        <Loader2
          size={32}
          className="animate-spin text-blue-600 mb-4 mx-auto"
        />
        <p className="text-gray-600 dark:text-gray-400">
          {t("loading", { ns: "common" })}
        </p>
      </div>
    </div>
  );
}

// Error Display Component
function ErrorDisplay({
  error,
  onRetry,
}: {
  error: string;
  onRetry: () => void;
}) {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
      <div className="text-center max-w-md mx-auto p-6">
        <AlertTriangle size={48} className="text-red-500 mb-4 mx-auto" />
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          {t("error", { ns: "common" })}
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">{error}</p>
        <button
          onClick={onRetry}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          {t("back", { ns: "common" })}
        </button>
      </div>
    </div>
  );
}

// Navigation Component with Sidebar
function Navigation({ children }: { children: React.ReactNode }) {
  const { user, logout, isLoading } = useAuth();
  const { state: companyState } = useCompany();
  const { t } = useTranslation();
  const { theme } = useTheme();
  const router = useRouter();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Check if we're on mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024);
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);

    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const navigationItems = [
    {
      id: "dashboard",
      label: t("dashboard", { ns: "navigation" }),
      href: "/dashboard",
      icon: <Home size={20} />,
      onClick: () => {
        router.push("/dashboard");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "customers",
      label: t("customers", { ns: "navigation" }),
      href: "/dashboard/customers",
      icon: <Users size={20} />,
      onClick: () => {
        router.push("/dashboard/customers");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "suppliers",
      label: t("suppliers", { ns: "navigation" }),
      href: "/dashboard/suppliers",
      icon: <Building2 size={20} />,
      onClick: () => {
        router.push("/dashboard/suppliers");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "products",
      label: t("products", { ns: "navigation" }),
      href: "/dashboard/products",
      icon: <Package size={20} />,
      disabled: true,
      onClick: () => {
        router.push("/dashboard/products");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "invoices",
      label: t("invoices", { ns: "navigation" }),
      href: "/dashboard/invoices",
      icon: <FileText size={20} />,
      disabled: true,
      onClick: () => {
        router.push("/dashboard/invoices");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "reports",
      label: t("reports", { ns: "navigation" }),
      href: "/dashboard/reports",
      icon: <BarChart3 size={20} />,
      disabled: true,
      onClick: () => {
        router.push("/dashboard/reports");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "test-flow",
      label: t("test_flow", { ns: "navigation" }),
      href: "/dashboard/test-business-flow",
      icon: <TestTube size={20} />,
      onClick: () => {
        router.push("/dashboard/test-business-flow");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
    {
      id: "settings",
      label: t("settings", { ns: "navigation" }),
      href: "/dashboard/settings",
      icon: <Settings size={20} />,
      disabled: true,
      onClick: () => {
        router.push("/dashboard/settings");
        if (isMobile) setMobileMenuOpen(false);
      },
    },
  ];

  // Get company info for display
  const getCompanyDisplayInfo = () => {
    if (companyState.currentCompany) {
      return {
        name: companyState.currentCompany.name,
        afm: companyState.currentCompany.afm,
      };
    }

    // Extract readable company name from user data
    const companyName =
      user?.name || user?.email?.split("@")[0] || "Δεν έχει οριστεί";

    return {
      name: companyName,
      afm: null,
    };
  };

  const companyInfo = getCompanyDisplayInfo();

  const sidebarHeader = (
    <div className="space-y-3">
      {/* Main header with app info */}
      <div className="flex items-start justify-between">
        <div
          className={`min-w-0 transition-all duration-300 ease-in-out ${
            sidebarCollapsed ? "opacity-0 w-0 overflow-hidden" : "opacity-100"
          }`}
        >
          {/* Logo and App Name Row */}
          <div className="flex items-center space-x-3 mb-1">
            <div className="flex-shrink-0">
              <Logo size="sm" />
            </div>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-white truncate flex-1">
              {t("app_name", { ns: "navigation" })}
            </h1>
          </div>

          {/* User/Company Name Row - Left Aligned */}
          <div className="ml-0">
            <p className="text-xs text-gray-600 dark:text-gray-400 truncate">
              {companyInfo.name}
              {companyInfo.afm && ` • ΑΦΜ: ${companyInfo.afm}`}
            </p>
          </div>
        </div>

        {/* Close button always visible and aligned to the right */}
        <button
          onClick={() => setSidebarCollapsed(true)}
          className="p-1 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors flex-shrink-0"
        >
          <ChevronLeft size={20} />
        </button>
      </div>

      {/* Theme and Language controls when sidebar is open */}
      {!sidebarCollapsed && (
        <div className="flex items-center justify-start pt-2 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2">
            <ThemeSelector variant="toggle" size="sm" />
            <LanguageSelector
              variant="dropdown"
              size="sm"
              showFlag={true}
              showNativeName={false}
              className="min-w-0"
              theme={theme}
            />
          </div>
        </div>
      )}
    </div>
  );

  const sidebarFooter = (
    <div
      className={`transition-all duration-300 ease-in-out ${
        sidebarCollapsed ? "opacity-0 h-0 overflow-hidden" : "opacity-100"
      }`}
    >
      <button
        onClick={handleLogout}
        disabled={isLoading}
        className="w-full bg-red-600 dark:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-red-700 dark:hover:bg-red-600 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            {t("logging_out", { ns: "navigation" })}
          </>
        ) : (
          <>
            <LogOut size={16} />
            {t("logout", { ns: "navigation" })}
          </>
        )}
      </button>
    </div>
  );

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Desktop Sidebar */}
      <div className="hidden lg:block">
        <Sidebar
          items={navigationItems}
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          header={sidebarHeader}
          footer={sidebarFooter}
          className="h-full border-r border-gray-200 dark:border-gray-700 shadow-sm dark:bg-gray-800"
          showToggleButton={sidebarCollapsed}
          collapsible={true}
          width={sidebarCollapsed ? "w-16" : "w-64"}
        />
      </div>

      {/* Mobile Sidebar */}
      <div className="lg:hidden">
        <Sidebar
          items={navigationItems}
          collapsed={false}
          header={sidebarHeader}
          footer={sidebarFooter}
          className="h-full"
          overlayOnMobile={true}
          isOpen={mobileMenuOpen}
          onClose={() => setMobileMenuOpen(false)}
        />
      </div>

      {/* Main Content */}
      <div
        className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ease-in-out ${
          sidebarCollapsed ? "lg:ml-0" : "lg:ml-0"
        }`}
      >
        {/* Desktop Header - Only show when sidebar is collapsed */}
        {sidebarCollapsed && (
          <div className="hidden lg:block bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 shadow-sm">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Logo size="sm" />
                <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {t("app_name", { ns: "navigation" })}
                </h1>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 flex items-center justify-center">
                  <ThemeSelector
                    variant="toggle"
                    size="sm"
                    className="h-8 w-8 min-w-8"
                  />
                </div>
                <div className="h-8 flex items-center">
                  <LanguageSelector
                    variant="dropdown"
                    size="sm"
                    showFlag={true}
                    showNativeName={false}
                    className="min-w-0"
                    theme={theme}
                  />
                </div>
                <button
                  onClick={handleLogout}
                  disabled={isLoading}
                  className="h-8 w-8 flex items-center justify-center text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
                >
                  <LogOut size={16} />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Mobile Header */}
        <div className="lg:hidden bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setMobileMenuOpen(true)}
                className="p-2 rounded-md text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              >
                <Menu size={20} />
              </button>
              <div>
                <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {t("app_name", { ns: "navigation" })}
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400 truncate">
                  {companyInfo.name}
                  {companyInfo.afm && ` • ΑΦΜ: ${companyInfo.afm}`}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 flex items-center justify-center">
                <ThemeSelector
                  variant="toggle"
                  size="md"
                  className="h-8 w-8 min-w-8"
                />
              </div>
              <div className="h-8 flex items-center">
                <LanguageSelector
                  variant="dropdown"
                  size="sm"
                  showFlag={true}
                  showNativeName={false}
                  className="min-w-0"
                  theme={theme}
                />
              </div>
              <button
                onClick={handleLogout}
                disabled={isLoading}
                className="h-8 w-8 flex items-center justify-center text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <LogOut size={16} />
              </button>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <main className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-900">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

// Protected Layout Content
function ProtectedLayoutContent({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, error, user } = useAuth();
  const { t } = useTranslation();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  // Prevent hydration mismatch by only rendering after client mount
  useEffect(() => {
    setMounted(true);
  }, []);

  // Handle authentication state
  useEffect(() => {
    if (mounted && !isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [mounted, isAuthenticated, isLoading, router]);

  // Show loading during SSR and initial client render to prevent hydration mismatch
  if (!mounted) {
    return <LoadingSpinner />;
  }

  // Show loading while checking authentication
  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Show error if authentication failed
  if (error) {
    return (
      <ErrorDisplay error={error} onRetry={() => window.location.reload()} />
    );
  }

  // Redirect if not authenticated
  if (!isAuthenticated) {
    return <LoadingSpinner />;
  }

  // Check user role access (simplified for now)
  if (
    user &&
    ![
      "super_admin",
      "admin",
      "company_admin",
      "manager",
      "employee",
      "viewer",
      "client",
    ].includes(user.role)
  ) {
    return (
      <ErrorDisplay
        error={t("access_denied", { ns: "navigation" })}
        onRetry={() => router.push("/login")}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation children={children} />
    </div>
  );
}

// Protected Layout with all providers
export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <TranslationProvider>
      <ThemeProvider>
        <AuthProvider app={AppName.CLIENT}>
          <ProtectedLayoutContent>{children}</ProtectedLayoutContent>
        </AuthProvider>
      </ThemeProvider>
    </TranslationProvider>
  );
}
