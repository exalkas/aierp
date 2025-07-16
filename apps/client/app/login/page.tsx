"use client";

import React from "react";
import { LoginForm, AppName, useAuth } from "@erp/shared-ui";
import { useRouter, useSearchParams } from "next/navigation";

export default function LoginPage() {
  const { login, isLoading, error, clearError } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleLogin = async (data: {
    email: string;
    password: string;
    rememberMe?: boolean;
  }) => {
    try {
      // Clear any previous errors
      clearError();

      console.log("Attempting login...");

      // Call the real authentication login function
      await login(data);

      console.log("Login successful, redirecting...");

      // Get redirect URL from query params or default to dashboard
      const redirectTo = searchParams.get("redirect") || "/dashboard";

      console.log("Redirecting to:", redirectTo);

      // Wait for cookie to be set before redirecting
      const waitForCookie = () => {
        let attempts = 0;
        const maxAttempts = 20; // 1 second total wait time

        const checkCookie = () => {
          const hasCookie = document.cookie.includes("auth_token=");
          attempts++;

          if (hasCookie) {
            console.log("Cookie confirmed, redirecting...");
            router.push(redirectTo);
          } else if (attempts >= maxAttempts) {
            console.log("Cookie timeout, redirecting anyway...");
            router.push(redirectTo);
          } else {
            // Check again in 50ms
            setTimeout(checkCookie, 50);
          }
        };
        checkCookie();
      };

      waitForCookie();
    } catch (error) {
      // Error is already handled by the AuthContext and will show in LoginForm
      console.error("Login failed:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-maritime-blue to-blue-900 flex items-center justify-center p-4">
      <div className="w-full max-w-lg lg:max-w-xl xl:max-w-2xl">
        {/* Login Form Container with proper spacing */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Header Section - More compact */}
          <div className="bg-gradient-to-r from-maritime-blue to-blue-700 px-8 py-8 text-center">
            <div className="w-16 h-16 bg-white/20 rounded-full mx-auto mb-4 flex items-center justify-center backdrop-blur-sm">
              <span className="text-2xl text-white">🏢</span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-bold text-white mb-2">
              Ελληνικό ERP/CRM
            </h1>
            <p className="text-blue-100">Διαχείριση πελατών και επιχειρήσεων</p>
          </div>

          {/* Form Section - Reduced padding */}
          <div className="px-8 py-6 lg:px-10 lg:py-8">
            <div className="mb-4 text-center">
              <h2 className="text-xl lg:text-2xl font-bold text-gray-800 mb-2">
                Καλώς ήρθατε
              </h2>
              <p className="text-gray-600">Συνδεθείτε στον λογαριασμό σας</p>
            </div>

            <LoginForm
              app={AppName.CLIENT}
              onLogin={handleLogin}
              isLoading={isLoading}
              error={error}
              language="el"
            />
          </div>
        </div>

        {/* Footer with copyright */}
        <div className="text-center mt-6">
          <p className="text-blue-100 text-sm">
            © {new Date().getFullYear()} Alkas Software. Όλα τα δικαιώματα
            κατοχυρωμένα.
          </p>
        </div>
      </div>
    </div>
  );
}
