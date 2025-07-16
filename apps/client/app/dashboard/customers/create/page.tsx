"use client";

import React from "react";
import { useRouter } from "next/navigation";
import BusinessEntityForm from "../../../../components/business-entities/BusinessEntityForm";

export default function CreateCustomerPage() {
  const router = useRouter();

  const handleSuccess = (entity: any) => {
    // Redirect to customer detail page or customer list
    router.push(`/dashboard/customers/${entity.id}`);
  };

  const handleCancel = () => {
    router.push("/dashboard/customers");
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <BusinessEntityForm
        mode="create"
        initialRole="customer"
        onSuccess={handleSuccess}
        onCancel={handleCancel}
      />
    </div>
  );
}
