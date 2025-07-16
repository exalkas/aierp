"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import BusinessEntityList from "../../../components/business-entities/BusinessEntityList";
import { Button, Card, CardContent, CardHeader } from "@erp/shared-ui";
import { Building2, Package, TrendingDown, Star } from "lucide-react";

interface SupplierStats {
  totalSuppliers: number;
  activeSuppliers: number;
  totalPurchases: number;
  averageRating: number;
}

export default function SuppliersPage() {
  const router = useRouter();
  const [stats, setStats] = useState<SupplierStats>({
    totalSuppliers: 0,
    activeSuppliers: 0,
    totalPurchases: 0,
    averageRating: 0,
  });

  const handleCreateSupplier = () => {
    router.push("/dashboard/suppliers/create");
  };

  const handleSupplierClick = (entity: any) => {
    router.push(`/dashboard/suppliers/${entity.id}`);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Suppliers</h1>
          <p className="text-gray-600">
            Manage your supplier relationships and procurement processes
          </p>
        </div>
        <Button
          onClick={handleCreateSupplier}
          className="flex items-center gap-2"
        >
          <Building2 className="w-4 h-4" />
          Add New Supplier
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Total Suppliers
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.totalSuppliers.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-blue-100">
                <Building2 className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Active Suppliers
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.activeSuppliers.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-green-100">
                <Package className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Total Purchases
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  €{stats.totalPurchases.toLocaleString()}
                </p>
              </div>
              <div className="p-3 rounded-full bg-orange-100">
                <TrendingDown className="w-6 h-6 text-orange-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">
                  Average Rating
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.averageRating.toFixed(1)}/5.0
                </p>
              </div>
              <div className="p-3 rounded-full bg-yellow-100">
                <Star className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Supplier List */}
      <BusinessEntityList
        roleFilter="supplier"
        title="Supplier Directory"
        showCreateButton={true}
        onCreateClick={handleCreateSupplier}
        onEntityClick={handleSupplierClick}
      />
    </div>
  );
}
