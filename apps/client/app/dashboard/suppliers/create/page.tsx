"use client";

import React from "react";
import { useRouter } from "next/navigation";
import BusinessEntityForm from "../../../../components/business-entities/BusinessEntityForm";

export default function CreateSupplierPage() {
  const router = useRouter();

  const handleSuccess = (entity: any) => {
    // Redirect to supplier detail page or supplier list
    router.push(`/dashboard/suppliers/${entity.id}`);
  };

  const handleCancel = () => {
    router.push("/dashboard/suppliers");
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <BusinessEntityForm
        mode="create"
        initialRole="supplier"
        onSuccess={handleSuccess}
        onCancel={handleCancel}
      />
    </div>
  );
}
