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

  const handleCreateCustomer = () => {
    router.push("/dashboard/customers/create");
  };

  const handleCustomerClick = (entity: any) => {
    router.push(`/dashboard/customers/${entity.id}`);
  };

  return (
    <div className="space-y-6">
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
