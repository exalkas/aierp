"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Input,
  AFMInput,
  DOYSelector,
  GreekAddressInput,
  GreekPhoneInput,
  Badge,
  LoadingButton,
} from "@erp/shared-ui";

// Temporary FormField components until we can refactor to pure react-hook-form
const FormField = ({ children }: { children: React.ReactNode }) => (
  <>{children}</>
);
const FormMessage = ({ children }: { children?: React.ReactNode }) =>
  children ? <p className="text-red-500 text-sm mt-1">{children}</p> : null;
import { useAuth } from "@erp/shared-ui";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  Building2,
  Users,
  Mail,
  Phone,
  MapPin,
  FileText,
  Check,
  X,
} from "lucide-react";

// Form validation schema
const businessEntitySchema = z.object({
  entity_type: z.enum(["business", "individual", "government", "non_profit"]),
  business_name: z.string().optional(),
  first_name: z.string().optional(),
  last_name: z.string().optional(),
  display_name: z.string().min(1, "Display name is required"),
  afm: z.string().optional(),
  doy: z.string().optional(),
  business_activity: z.string().optional(),
  legal_form: z.string().optional(),
  vat_number: z.string().optional(),
  vat_exempt: z.boolean().default(false),
  email: z.string().email("Invalid email format").optional().or(z.literal("")),
  phone: z.string().optional(),
  mobile: z.string().optional(),
  website: z.string().url("Invalid website URL").optional().or(z.literal("")),
  // Address fields
  address_street: z.string().optional(),
  address_number: z.string().optional(),
  address_city: z.string().optional(),
  address_postal_code: z.string().optional(),
  address_region: z.string().optional(),
  // Business settings
  entity_category: z.string().optional(),
  payment_terms: z
    .enum(["net_0", "net_15", "net_30", "net_60", "net_90", "prepaid"])
    .default("net_30"),
  credit_limit: z.number().min(0).optional(),
  discount_percentage: z.number().min(0).max(100).optional(),
  // Notes and tags
  notes: z.string().optional(),
});

type BusinessEntityFormData = z.infer<typeof businessEntitySchema>;

export interface BusinessEntityFormProps {
  mode: "create" | "edit";
  entityId?: string;
  initialRole?: "customer" | "supplier" | "partner";
  onSuccess?: (entity: any) => void;
  onCancel?: () => void;
  className?: string;
}

export default function BusinessEntityForm({
  mode,
  entityId,
  initialRole = "customer",
  onSuccess,
  onCancel,
  className = "",
}: BusinessEntityFormProps) {
  const { tokens } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [validatingAFM, setValidatingAFM] = useState(false);
  const [afmValid, setAfmValid] = useState<boolean | null>(null);
  const [selectedDOY, setSelectedDOY] = useState<any>(null);

  const form = useForm<BusinessEntityFormData>({
    resolver: zodResolver(businessEntitySchema),
    defaultValues: {
      entity_type: "business",
      vat_exempt: false,
      payment_terms: "net_30",
      credit_limit: 0,
      discount_percentage: 0,
    },
  });

  // Watch entity type to toggle required fields
  const entityType = form.watch("entity_type");
  const businessName = form.watch("business_name");
  const firstName = form.watch("first_name");
  const lastName = form.watch("last_name");

  // Auto-generate display name
  useEffect(() => {
    let displayName = "";
    if (entityType === "business" && businessName) {
      displayName = businessName;
    } else if (entityType === "individual" && firstName && lastName) {
      displayName = `${firstName} ${lastName}`;
    }

    if (displayName && displayName !== form.getValues("display_name")) {
      form.setValue("display_name", displayName);
    }
  }, [entityType, businessName, firstName, lastName, form]);

  // Load existing entity data if editing
  useEffect(() => {
    if (mode === "edit" && entityId && tokens?.accessToken) {
      loadEntityData();
    }
  }, [mode, entityId, tokens]);

  const loadEntityData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/v1/business-entities/${entityId}`, {
        headers: {
          Authorization: `Bearer ${tokens?.accessToken}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to load entity data");
      }

      const entity = await response.json();

      // Populate form with existing data
      Object.keys(entity).forEach((key) => {
        if (key in businessEntitySchema.shape) {
          form.setValue(key as keyof BusinessEntityFormData, entity[key]);
        }
      });
    } catch (error) {
      console.error("Error loading entity data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAFMValidation = async (afm: string) => {
    if (!afm || afm.length !== 9) {
      setAfmValid(null);
      return;
    }

    setValidatingAFM(true);
    try {
      const response = await fetch(
        `/api/v1/business-entities/validate/afm?afm=${afm}`,
        {
          headers: {
            Authorization: `Bearer ${tokens?.accessToken}`,
          },
        }
      );

      if (response.ok) {
        const result = await response.json();
        setAfmValid(result.is_valid);
      } else {
        setAfmValid(false);
      }
    } catch (error) {
      console.error("AFM validation error:", error);
      setAfmValid(false);
    } finally {
      setValidatingAFM(false);
    }
  };

  const handleDOYSelection = (doyId: string, doyData: any) => {
    setSelectedDOY(doyData);
    form.setValue("doy", doyData?.code || doyId);
  };

  const onSubmit = async (data: BusinessEntityFormData) => {
    try {
      setLoading(true);

      // Add the initial role to the request
      const requestData = {
        ...data,
        roles: [initialRole],
      };

      const url =
        mode === "create"
          ? "/api/v1/business-entities/"
          : `/api/v1/business-entities/${entityId}`;

      const method = mode === "create" ? "POST" : "PUT";

      const response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${tokens?.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to save business entity");
      }

      const entity = await response.json();

      if (onSuccess) {
        onSuccess(entity);
      } else {
        // Default navigation based on role
        const targetPath =
          initialRole === "customer"
            ? "/dashboard/customers"
            : "/dashboard/suppliers";
        router.push(targetPath);
      }
    } catch (error) {
      console.error("Error saving entity:", error);
      // TODO: Show error message to user
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {mode === "create" ? "Create" : "Edit"}{" "}
            {initialRole.charAt(0).toUpperCase() + initialRole.slice(1)}
          </h1>
          <p className="text-gray-600">
            {mode === "create" ? "Add a new" : "Update"} business entity with
            Greek compliance
          </p>
        </div>
        {onCancel && (
          <Button variant="outline" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Entity Type Selection */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Entity Type</h3>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { value: "business", label: "Business", icon: Building2 },
                { value: "individual", label: "Individual", icon: Users },
              ].map(({ value, label, icon: Icon }) => (
                <div
                  key={value}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    entityType === value
                      ? "border-blue-500 bg-blue-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                  onClick={() => form.setValue("entity_type", value as any)}
                >
                  <Icon className="w-6 h-6 mb-2 text-gray-600" />
                  <div className="font-medium">{label}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Basic Information */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Basic Information</h3>
          </CardHeader>
          <CardContent className="space-y-4">
            {entityType === "business" ? (
              <FormField
                control={form.control}
                name="business_name"
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Business Name *
                    </label>
                    <Input
                      {...field}
                      placeholder="Enter business name"
                      error={form.formState.errors.business_name?.message}
                    />
                  </div>
                )}
              />
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="first_name"
                  render={({ field }) => (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        First Name *
                      </label>
                      <Input
                        {...field}
                        placeholder="Enter first name"
                        error={form.formState.errors.first_name?.message}
                      />
                    </div>
                  )}
                />
                <FormField
                  control={form.control}
                  name="last_name"
                  render={({ field }) => (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Last Name *
                      </label>
                      <Input
                        {...field}
                        placeholder="Enter last name"
                        error={form.formState.errors.last_name?.message}
                      />
                    </div>
                  )}
                />
              </div>
            )}

            <FormField
              control={form.control}
              name="display_name"
              render={({ field }) => (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Display Name *
                  </label>
                  <Input
                    {...field}
                    placeholder="Display name for lists and reports"
                    error={form.formState.errors.display_name?.message}
                  />
                </div>
              )}
            />
          </CardContent>
        </Card>

        {/* Greek Tax Information */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Greek Tax Information
            </h3>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="afm"
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      AFM (Tax Number)
                      {afmValid === true && (
                        <Badge variant="success" className="ml-2">
                          <Check className="w-3 h-3 mr-1" />
                          Valid
                        </Badge>
                      )}
                      {afmValid === false && (
                        <Badge variant="error" className="ml-2">
                          <X className="w-3 h-3 mr-1" />
                          Invalid
                        </Badge>
                      )}
                    </label>
                    <AFMInput
                      {...field}
                      validateCompanyAFM={entityType === "business"}
                      onValidChange={(isValid, afm) => {
                        setAfmValid(isValid);
                        if (isValid) {
                          handleAFMValidation(afm);
                        }
                      }}
                      error={form.formState.errors.afm?.message}
                    />
                  </div>
                )}
              />

              <FormField
                control={form.control}
                name="doy"
                render={({ field }) => (
                  <div>
                    <DOYSelector
                      value={field.value}
                      onChange={handleDOYSelection}
                      label="DOY (Tax Office)"
                      error={form.formState.errors.doy?.message}
                    />
                  </div>
                )}
              />
            </div>

            {entityType === "business" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="business_activity"
                  render={({ field }) => (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Business Activity
                      </label>
                      <Input
                        {...field}
                        placeholder="e.g., Software Development"
                        error={form.formState.errors.business_activity?.message}
                      />
                    </div>
                  )}
                />

                <FormField
                  control={form.control}
                  name="legal_form"
                  render={({ field }) => (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Legal Form
                      </label>
                      <select
                        {...field}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Select legal form</option>
                        <option value="AE">ΑΕ (Ανώνυμη Εταιρεία)</option>
                        <option value="EPE">
                          ΕΠΕ (Εταιρεία Περιορισμένης Ευθύνης)
                        </option>
                        <option value="OE">ΟΕ (Ομόρρυθμη Εταιρεία)</option>
                        <option value="EE">ΕΕ (Ετερόρρυθμη Εταιρεία)</option>
                        <option value="IKE">
                          ΙΚΕ (Ιδιωτική Κεφαλαιουχική Εταιρεία)
                        </option>
                        <option value="AT">ΑΤ (Ατομική Επιχείρηση)</option>
                      </select>
                    </div>
                  )}
                />
              </div>
            )}

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="vat_exempt"
                {...form.register("vat_exempt")}
                className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
              />
              <label htmlFor="vat_exempt" className="text-sm text-gray-700">
                VAT Exempt
              </label>
            </div>
          </CardContent>
        </Card>

        {/* Contact Information */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Mail className="w-5 h-5" />
              Contact Information
            </h3>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email Address
                    </label>
                    <Input
                      {...field}
                      type="email"
                      placeholder="email@example.com"
                      leftIcon={<Mail className="w-4 h-4" />}
                      error={form.formState.errors.email?.message}
                    />
                  </div>
                )}
              />

              <FormField
                control={form.control}
                name="website"
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Website
                    </label>
                    <Input
                      {...field}
                      placeholder="https://example.com"
                      error={form.formState.errors.website?.message}
                    />
                  </div>
                )}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="phone"
                render={({ field }) => (
                  <div>
                    <GreekPhoneInput
                      {...field}
                      label="Phone Number"
                      allowLandline={true}
                      allowMobile={false}
                      error={form.formState.errors.phone?.message}
                    />
                  </div>
                )}
              />

              <FormField
                control={form.control}
                name="mobile"
                render={({ field }) => (
                  <div>
                    <GreekPhoneInput
                      {...field}
                      label="Mobile Number"
                      allowLandline={false}
                      allowMobile={true}
                      error={form.formState.errors.mobile?.message}
                    />
                  </div>
                )}
              />
            </div>
          </CardContent>
        </Card>

        {/* Address Information */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <MapPin className="w-5 h-5" />
              Address Information
            </h3>
          </CardHeader>
          <CardContent>
            <GreekAddressInput
              value={{
                street: form.watch("address_street"),
                number: form.watch("address_number"),
                city: form.watch("address_city"),
                postalCode: form.watch("address_postal_code"),
                region: form.watch("address_region"),
              }}
              onChange={(address) => {
                form.setValue("address_street", address.street || "");
                form.setValue("address_number", address.number || "");
                form.setValue("address_city", address.city || "");
                form.setValue("address_postal_code", address.postalCode || "");
                form.setValue("address_region", address.region || "");
              }}
              required={false}
              layout="vertical"
            />
          </CardContent>
        </Card>

        {/* Business Settings (for customers/suppliers) */}
        {(initialRole === "customer" || initialRole === "supplier") && (
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold">Business Settings</h3>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <FormField
                  control={form.control}
                  name="payment_terms"
                  render={({ field }) => (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Payment Terms
                      </label>
                      <select
                        {...field}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="net_0">Cash on Delivery</option>
                        <option value="net_15">Net 15 days</option>
                        <option value="net_30">Net 30 days</option>
                        <option value="net_60">Net 60 days</option>
                        <option value="net_90">Net 90 days</option>
                        <option value="prepaid">Prepaid</option>
                      </select>
                    </div>
                  )}
                />

                {initialRole === "customer" && (
                  <FormField
                    control={form.control}
                    name="credit_limit"
                    render={({ field }) => (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Credit Limit (€)
                        </label>
                        <Input
                          {...field}
                          type="number"
                          min="0"
                          placeholder="0"
                          onChange={(e) =>
                            field.onChange(parseFloat(e.target.value) || 0)
                          }
                          error={form.formState.errors.credit_limit?.message}
                        />
                      </div>
                    )}
                  />
                )}

                <FormField
                  control={form.control}
                  name="discount_percentage"
                  render={({ field }) => (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Discount (%)
                      </label>
                      <Input
                        {...field}
                        type="number"
                        min="0"
                        max="100"
                        placeholder="0"
                        onChange={(e) =>
                          field.onChange(parseFloat(e.target.value) || 0)
                        }
                        error={
                          form.formState.errors.discount_percentage?.message
                        }
                      />
                    </div>
                  )}
                />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Notes */}
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Additional Notes</h3>
          </CardHeader>
          <CardContent>
            <FormField
              control={form.control}
              name="notes"
              render={({ field }) => (
                <div>
                  <textarea
                    {...field}
                    rows={4}
                    placeholder="Additional notes about this entity..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              )}
            />
          </CardContent>
        </Card>

        {/* Form Actions */}
        <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
          {onCancel && (
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          )}
          <LoadingButton type="submit" loading={loading} disabled={loading}>
            {mode === "create" ? "Create" : "Update"}{" "}
            {initialRole.charAt(0).toUpperCase() + initialRole.slice(1)}
          </LoadingButton>
        </div>
      </form>
    </div>
  );
}
