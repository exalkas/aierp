"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import BusinessEntityList from "../../../components/business-entities/BusinessEntityList";
import { Button, Card, CardContent, CardHeader, useAuth } from "@erp/shared-ui";
import { Users, TrendingUp, DollarSign, Activity } from "lucide-react";

interface CustomerStats {
  totalCustomers: number;
  activeCustomers: number;
  totalSales: number;
  averageOrderValue: number;
}

export default function CustomersPage() {
  const router = useRouter();
  const { user, tokens, isAuthenticated } = useAuth();
  const [stats, setStats] = useState<CustomerStats>({
    totalCustomers: 0,
    activeCustomers: 0,
    totalSales: 0,
    averageOrderValue: 0,
  });

  // Debug authentication state
  useEffect(() => {
    console.log("CustomerPage - Auth Debug:", {
      isAuthenticated,
      hasTokens: !!tokens,
      hasAccessToken: !!tokens?.accessToken,
      user: user ? { id: user.id, email: user.email, role: user.role } : null,
      tokenExpiry: tokens?.expiresAt,
    });
  }, [isAuthenticated, tokens, user]);

  // Test API call to debug authentication
  const testApiCall = async () => {
    try {
      console.log("Testing API call with current tokens...");

      if (!tokens?.accessToken) {
        console.error("No access token available");
        return;
      }

      const response = await fetch("/api/v1/business-entities?limit=1", {
        headers: {
          Authorization: `Bearer ${tokens.accessToken}`,
          "Content-Type": "application/json",
        },
      });

      console.log("Test API Response:", {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Test API Success:", data);
        alert("API call successful! Check console for details.");
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.log("Test API Error:", errorData);
        alert(
          `API call failed: ${response.status} - ${
            errorData.detail || response.statusText
          }`
        );
      }
    } catch (error) {
      console.error("Test API Error:", error);
      alert(`API call error: ${error}`);
    }
  };

  // Clear all stored tokens and force re-login
  const clearTokensAndRelogin = () => {
    // Clear localStorage
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth-token");
      localStorage.removeItem("auth_token");
      localStorage.removeItem("authToken");

      // Clear cookies
      document.cookie =
        "auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie =
        "authToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    alert("Tokens cleared! Redirecting to login...");
    router.push("/login");
  };

  const handleCreateCustomer = () => {
    router.push("/dashboard/customers/create");
  };

  const handleCustomerClick = (entity: any) => {
    router.push(`/dashboard/customers/${entity.id}`);
  };

  return (
    <div className="space-y-6">
      {/* Debug Info - Remove in production */}
      {process.env.NODE_ENV === "development" && (
        <Card className="bg-yellow-50 border-yellow-200">
          <CardHeader>
            <h3 className="text-sm font-medium text-yellow-800">Debug Info</h3>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-yellow-700 space-y-1 mb-3">
              <div>Authenticated: {isAuthenticated ? "✅ Yes" : "❌ No"}</div>
              <div>Has Tokens: {tokens ? "✅ Yes" : "❌ No"}</div>
              <div>
                Access Token:{" "}
                {tokens?.accessToken ? "✅ Present" : "❌ Missing"}
              </div>
              <div>User Role: {user?.role || "None"}</div>
              <div>Company ID: {user?.companyId || "None"}</div>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={testApiCall}
                size="sm"
                variant="outline"
                className="text-xs"
              >
                Test API Call
              </Button>

              <Button
                onClick={clearTokensAndRelogin}
                size="sm"
                variant="destructive"
                className="text-xs"
              >
                Clear Tokens & Re-login
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Customers</h1>
          <p className="text-gray-600">
            Manage your customer relationships and track sales performance
          </p>
        </div>
        <Button
          onClick={handleCreateCustomer}
          className="flex items-center gap-2"
        >
          <Users className="w-4 h-4" />
          Add New Customer
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Total Customers
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.totalCustomers.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-blue-100">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Active Customers
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.activeCustomers.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-green-100">
                <Activity className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">Total Sales</p>
                <p className="text-2xl font-bold text-gray-900">
                  €{stats.totalSales.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-yellow-100">
                <DollarSign className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Avg. Order Value
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  €{stats.averageOrderValue.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-purple-100">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Customer List */}
      <BusinessEntityList
        roleFilter="customer"
        title="Customer Directory"
        showCreateButton={true}
        onCreateClick={handleCreateCustomer}
        onEntityClick={handleCustomerClick}
      />
    </div>
  );
}
