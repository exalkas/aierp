"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Controller } from "react-hook-form";
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
  useTranslation,
  useAuth,
} from "@erp/shared-ui";
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
  Plus,
} from "lucide-react";
import MultiContactManager from "./MultiContactManager";

// Create validation schema with proper translations and conditional validation
const createBusinessEntitySchema = (t: any) =>
  z
    .object({
      entity_type: z.enum([
        "business",
        "individual",
        "government",
        "non_profit",
      ]),
      business_name: z.string().optional(),
      first_name: z.string().optional(),
      last_name: z.string().optional(),
      display_name: z.string().min(
        1,
        t("validation.display_name_required", {
          ns: "business_entities",
          defaultValue: "Display name is required",
        })
      ),
      afm: z.string().optional(),
      doy: z.string().optional(),
      business_activity: z.string().optional(),
      legal_form: z.string().optional(),
      vat_number: z.string().optional(),
      vat_exempt: z.boolean(),
      // Legacy single contact fields for backward compatibility
      email: z.string().optional(),
      phone: z.string().optional(),
      mobile: z.string().optional(),
      website: z
        .string()
        .url(
          t("validation.invalid_url", {
            ns: "business_entities",
            defaultValue: "Invalid website URL",
          })
        )
        .optional()
        .or(z.literal("")),
      // Legacy address fields for backward compatibility
      address_street: z.string().optional(),
      address_number: z.string().optional(),
      address_city: z.string().optional(),
      address_postal_code: z.string().optional(),
      address_region: z.string().optional(),
      // New multi-contact system
      contact_methods: z
        .array(
          z.object({
            id: z.string(),
            type: z.enum(["phone", "email", "address"]),
            subtype_code: z.string(),
            subtype_name: z.string(),
            value: z.union([
              z.string(),
              z.object({
                street: z.string(),
                number: z.string(),
                city: z.string(),
                postalCode: z.string(),
                region: z.string(),
              }),
            ]),
            is_primary: z.boolean(),
            is_verified: z.boolean(),
            quality_score: z.number().optional(),
            notes: z.string().optional(),
          })
        )
        .optional(),
      // Business settings
      entity_category: z.string().optional(),
      payment_terms: z.enum([
        "net_0",
        "net_15",
        "net_30",
        "net_60",
        "net_90",
        "prepaid",
      ]),
      credit_limit: z.number().min(0).optional(),
      discount_percentage: z.number().min(0).max(100).optional(),
      // Notes and tags
      notes: z.string().optional(),
    })
    .superRefine((data, ctx) => {
      // Business entity requires business name
      if (data.entity_type === "business" && !data.business_name?.trim()) {
        ctx.addIssue({
          code: "custom",
          message: t("validation.business_name_required", {
            ns: "business_entities",
            defaultValue: "Business name is required",
          }),
          path: ["business_name"],
        });
      }
      // Individual entity requires first and last name
      if (data.entity_type === "individual") {
        if (!data.first_name?.trim()) {
          ctx.addIssue({
            code: "custom",
            message: t("validation.first_name_required", {
              ns: "business_entities",
              defaultValue: "First name is required",
            }),
            path: ["first_name"],
          });
        }
        if (!data.last_name?.trim()) {
          ctx.addIssue({
            code: "custom",
            message: t("validation.last_name_required", {
              ns: "business_entities",
              defaultValue: "Last name is required",
            }),
            path: ["last_name"],
          });
        }
      }
    });

// Create a type from the schema
type BusinessEntityFormData = z.infer<
  ReturnType<typeof createBusinessEntitySchema>
>;

export interface BusinessEntityFormProps {
  mode: "create" | "edit";
  entityId?: string;
  initialRole?: "customer" | "supplier" | "partner";
  onSuccess?: (entity: any) => void;
  onCancel?: () => void;
  className?: string;
  createAnother?: boolean;
  onCreateAnotherChange?: (value: boolean) => void;
}

export default function BusinessEntityForm({
  mode,
  entityId,
  initialRole = "customer",
  onSuccess,
  onCancel,
  className = "",
  createAnother = false,
  onCreateAnotherChange,
}: BusinessEntityFormProps) {
  const { tokens } = useAuth();
  const { t } = useTranslation();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [validatingAFM, setValidatingAFM] = useState(false);
  const [afmValid, setAfmValid] = useState<boolean | null>(null);
  const [selectedDOY, setSelectedDOY] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const form = useForm<BusinessEntityFormData>({
    resolver: zodResolver(createBusinessEntitySchema(t)),
    defaultValues: {
      entity_type: "business",
      business_name: "",
      first_name: "",
      last_name: "",
      display_name: "",
      afm: "",
      doy: "",
      business_activity: "",
      legal_form: "",
      vat_number: "",
      vat_exempt: false,
      email: "",
      phone: "",
      mobile: "",
      website: "",
      address_street: "",
      address_number: "",
      address_city: "",
      address_postal_code: "",
      address_region: "",
      entity_category: "",
      payment_terms: "net_30",
      credit_limit: 0,
      discount_percentage: 0,
      notes: "",
      contact_methods: [],
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
      setError(null);
      const response = await fetch(`/api/v1/business-entities/${entityId}`, {
        headers: {
          Authorization: `Bearer ${tokens?.accessToken}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(
          t("error_loading_entity", {
            ns: "business_entities",
            defaultValue: "Failed to load entity data",
          })
        );
      }

      const entity = await response.json();

      // Populate form with existing data
      const schema = createBusinessEntitySchema(t);
      Object.keys(entity).forEach((key) => {
        if (key in schema.shape) {
          form.setValue(key as keyof BusinessEntityFormData, entity[key]);
        }
      });
    } catch (error) {
      console.error("Error loading entity data:", error);
      const errorMessage =
        error instanceof Error ? error.message : t("error", { ns: "common" });
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleAFMValidation = async (afm: string) => {
    if (!afm || afm.length !== 9) {
      setAfmValid(null);
      return;
    }

    // Skip external validation in development mode to prevent timeout
    if (process.env.NODE_ENV === "development") {
      console.log("Skipping external AFM validation in development mode");
      setAfmValid(true); // Assume valid in development
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
    console.log("🚀 [FORM] Form submission started", {
      timestamp: new Date().toISOString(),
      mode,
      initialRole,
      dataKeys: Object.keys(data),
      hasAFM: !!data.afm,
      afmValue: data.afm,
    });

    try {
      setLoading(true);
      setError(null);
      setSuccess(null);

      console.log("📝 [FORM] Preparing request data...");

      // Add the initial role to the request
      const requestData = {
        ...data,
        roles: [initialRole],
      };

      // Clean up the request data - remove empty strings for optional fields
      const cleanedData = { ...requestData };

      // List of optional fields that should be omitted if empty
      const optionalFields = [
        "afm",
        "doy",
        "email",
        "phone",
        "mobile",
        "website",
        "address_street",
        "address_city",
        "address_region",
        "address_postal_code",
        "address_country",
        "vat_number",
        "business_activity",
        "notes",
      ];

      // Remove empty optional fields
      optionalFields.forEach((field) => {
        if (
          cleanedData[field] === "" ||
          cleanedData[field] === null ||
          cleanedData[field] === undefined
        ) {
          delete cleanedData[field];
        }
      });

      console.log("📤 [FORM] Request data prepared", {
        timestamp: new Date().toISOString(),
        requestDataKeys: Object.keys(cleanedData),
        roles: cleanedData.roles,
        hasAuthToken: !!tokens?.accessToken,
        removedFields: Object.keys(requestData).filter(
          (key) => !(key in cleanedData)
        ),
      });

      const url =
        mode === "create"
          ? "/api/v1/business-entities/"
          : `/api/v1/business-entities/${entityId}`;

      const method = mode === "create" ? "POST" : "PUT";

      console.log("🌐 [FORM] About to make API request", {
        timestamp: new Date().toISOString(),
        url: "/api/v1/business-entities/",
        method: "POST",
        hasToken: !!tokens?.accessToken,
        tokenLength: tokens?.accessToken?.length,
      });

      console.log("🔧 [FORM] Creating fetch request...");
      const requestStart = performance.now();

      // Remove AbortController for now - might be causing the hang
      // const controller = new AbortController();
      // const timeoutId = setTimeout(() => {
      //   console.log("⏰ [FORM] Fetch timeout after 35 seconds, aborting...");
      //   controller.abort();
      // }, 35000);

      console.log("📡 [FORM] Starting fetch...", {
        timestamp: new Date().toISOString(),
        requestStart: requestStart,
      });

      // Debug the exact request being made
      const requestHeaders = {
        "Content-Type": "application/json",
        ...(tokens?.accessToken && {
          Authorization: `Bearer ${tokens.accessToken}`,
        }),
      };

      const requestBody = JSON.stringify(cleanedData);

      console.log("🔍 [FORM] Request details", {
        timestamp: new Date().toISOString(),
        headers: requestHeaders,
        bodyLength: requestBody.length,
        bodyPreview:
          requestBody.substring(0, 200) +
          (requestBody.length > 200 ? "..." : ""),
        requestDataType: typeof cleanedData,
        requestDataKeys: Object.keys(cleanedData),
      });

      console.log("🚀 [FORM] About to call fetch...");

      // First, try a simple test fetch to see if fetch works at all
      try {
        console.log("🧪 [TEST] Trying simple GET request first...");
        const testResponse = await fetch("/api/v1/greek-reference-data");
        console.log("🧪 [TEST] Simple GET worked:", testResponse.status);
      } catch (testError) {
        console.error("🧪 [TEST] Simple GET failed:", testError);
      }

      // Test 2: Try a minimal POST request
      try {
        console.log("🧪 [TEST2] Trying minimal POST request...");
        const minimalResponse = await fetch("/api/v1/business-entities/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: requestHeaders.Authorization,
          },
          body: JSON.stringify({
            entity_type: "business",
            display_name: "test",
          }),
        });
        console.log("🧪 [TEST2] Minimal POST worked:", minimalResponse.status);
      } catch (minimalError) {
        console.error("🧪 [TEST2] Minimal POST failed:", minimalError);
      }

      console.log("🚀 [FORM] Now trying the real POST...");

      // Log exact request details
      console.log("📋 [DEBUG] Exact POST request config:", {
        url: "/api/v1/business-entities/",
        method: "POST",
        headers: Object.fromEntries(Object.entries(requestHeaders)),
        bodyLength: requestBody.length,
        bodyContent: requestBody,
        timestamp: new Date().toISOString(),
      });

      const response = await fetch("/api/v1/business-entities/", {
        method: "POST",
        headers: requestHeaders,
        body: requestBody,
        // signal: controller.signal, // Removed for now
      });

      // clearTimeout(timeoutId);
      const requestEnd = performance.now();
      const requestDuration = requestEnd - requestStart;

      console.log("📡 [FORM] API request completed", {
        timestamp: new Date().toISOString(),
        status: response.status,
        statusText: response.statusText,
        duration: `${requestDuration.toFixed(2)}ms`,
        ok: response.ok,
        headers: Object.fromEntries(response.headers.entries()),
      });

      if (!response.ok) {
        console.error("❌ [FORM] API request failed", {
          status: response.status,
          statusText: response.statusText,
          url: response.url,
        });

        const errorData = await response.json();
        console.error("❌ [FORM] Error response data", errorData);

        // Display validation errors properly
        if (errorData.detail && Array.isArray(errorData.detail)) {
          console.error("❌ [FORM] Validation errors:");
          errorData.detail.forEach((error: any, index: number) => {
            console.error(
              `  ${index + 1}. Field: ${error.loc?.join(".")}, Error: ${
                error.msg
              }, Input: ${error.input}`
            );
          });
        }

        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      console.log("✅ [FORM] Parsing successful response...");
      const entity = await response.json();

      console.log("🎉 [FORM] Entity created/updated successfully", {
        timestamp: new Date().toISOString(),
        entityId: entity.id,
        entityCode: entity.entity_code,
        displayName: entity.display_name,
      });

      // Show success message
      setSuccess(
        mode === "create"
          ? t("entity_created_success", {
              ns: "business_entities",
              defaultValue: "Business entity created successfully",
            })
          : t("entity_updated_success", {
              ns: "business_entities",
              defaultValue: "Business entity updated successfully",
            })
      );

      console.log("🔄 [FORM] Calling onSuccess callback...");
      if (onSuccess) {
        onSuccess(entity);

        // If createAnother is true, reset the form for next entry
        if (createAnother && mode === "create") {
          console.log("🔄 [FORM] Resetting form for another creation...");
          setTimeout(() => {
            form.reset({
              entity_type: "business",
              display_name: "",
              business_name: "",
              first_name: "",
              last_name: "",
              afm: "",
              doy: "",
              business_activity: "",
              legal_form: "",
              vat_exempt: false,
              email: "",
              phone: "",
              mobile: "",
              website: "",
              address_street: "",
              address_number: "",
              address_city: "",
              address_postal_code: "",
              address_region: "",
              entity_category: "",
              payment_terms: "net_30",
              credit_limit: 0,
              discount_percentage: 0,
              notes: "",
              contact_methods: [],
            });
            setError("");
            // Keep success message for a short time then clear it
            setTimeout(() => setSuccess(""), 3000);
          }, 1000); // Small delay to let user see success message
        }
      } else {
        // Default navigation based on role
        const targetPath =
          initialRole === "customer"
            ? "/dashboard/customers"
            : "/dashboard/suppliers";
        console.log("🧭 [FORM] Navigating to:", targetPath);
        router.push(targetPath);
      }
    } catch (error) {
      const errorEndTime = Date.now();
      console.error("💥 [FORM] Form submission error", {
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : String(error),
        errorType:
          error instanceof Error ? error.constructor.name : typeof error,
        stack: error instanceof Error ? error.stack : undefined,
      });

      const errorMessage =
        error instanceof Error ? error.message : t("error", { ns: "common" });
      setError(errorMessage);
    } finally {
      console.log("🏁 [FORM] Form submission process finished", {
        timestamp: new Date().toISOString(),
        loading: false,
      });
      setLoading(false);
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Error and Success Messages */}
      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <X className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                {t("error", { ns: "common" })}
              </h3>
              <div className="mt-1 text-sm text-red-700 dark:text-red-300">
                <p>{error}</p>
              </div>
            </div>
            <div className="ml-auto">
              <button
                onClick={() => setError(null)}
                className="text-red-400 hover:text-red-600 dark:hover:text-red-300"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Check className="h-5 w-5 text-green-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800 dark:text-green-200">
                {t("success", { ns: "common" })}
              </h3>
              <div className="mt-1 text-sm text-green-700 dark:text-green-300">
                <p>{success}</p>
              </div>
            </div>
            <div className="ml-auto">
              <button
                onClick={() => setSuccess(null)}
                className="text-green-400 hover:text-green-600 dark:hover:text-green-300"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Entity Type Selection */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {t("entity_type", {
                ns: "business_entities",
                defaultValue: "Entity Type",
              })}
            </h3>
          </CardHeader>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                {
                  value: "business",
                  label: t("entity_type_business", { ns: "business_entities" }),
                  icon: Building2,
                },
                {
                  value: "individual",
                  label: t("entity_type_individual", {
                    ns: "business_entities",
                  }),
                  icon: Users,
                },
              ].map(({ value, label, icon: Icon }) => (
                <div
                  key={value}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    entityType === value
                      ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400"
                      : "border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700/50"
                  }`}
                  onClick={() => form.setValue("entity_type", value as any)}
                >
                  <Icon className="w-6 h-6 mb-2 text-gray-600 dark:text-gray-400" />
                  <div className="font-medium text-gray-900 dark:text-white">
                    {label}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Basic Information */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {t("basic_information", {
                ns: "business_entities",
                defaultValue: "Basic Information",
              })}
            </h3>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            {entityType === "business" ? (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {t("business_name", {
                    ns: "business_entities",
                    defaultValue: "Business Name",
                  })}{" "}
                  *
                </label>
                <Controller
                  name="business_name"
                  control={form.control}
                  render={({ field }) => (
                    <Input
                      {...field}
                      placeholder={t("business_name_placeholder", {
                        ns: "business_entities",
                        defaultValue: "Enter business name",
                      })}
                      error={form.formState.errors.business_name?.message}
                      className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                    />
                  )}
                />
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {t("first_name", {
                      ns: "business_entities",
                      defaultValue: "First Name",
                    })}{" "}
                    *
                  </label>
                  <Controller
                    name="first_name"
                    control={form.control}
                    render={({ field }) => (
                      <Input
                        {...field}
                        placeholder={t("first_name_placeholder", {
                          ns: "business_entities",
                          defaultValue: "Enter first name",
                        })}
                        error={form.formState.errors.first_name?.message}
                        className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                      />
                    )}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {t("last_name", {
                      ns: "business_entities",
                      defaultValue: "Last Name",
                    })}{" "}
                    *
                  </label>
                  <Controller
                    name="last_name"
                    control={form.control}
                    render={({ field }) => (
                      <Input
                        {...field}
                        placeholder={t("last_name_placeholder", {
                          ns: "business_entities",
                          defaultValue: "Enter last name",
                        })}
                        error={form.formState.errors.last_name?.message}
                        className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                      />
                    )}
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t("display_name", {
                  ns: "business_entities",
                  defaultValue: "Display Name",
                })}{" "}
                *
              </label>
              <Controller
                name="display_name"
                control={form.control}
                render={({ field }) => (
                  <Input
                    {...field}
                    placeholder={t("display_name_placeholder", {
                      ns: "business_entities",
                      defaultValue: "Display name for lists and reports",
                    })}
                    error={form.formState.errors.display_name?.message}
                    className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                  />
                )}
              />
            </div>
          </CardContent>
        </Card>

        {/* Greek Tax Information */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
            <h3 className="text-lg font-semibold flex items-center gap-2 text-gray-900 dark:text-white">
              <FileText className="w-5 h-5" />
              {t("greek_tax_information", {
                ns: "business_entities",
                defaultValue: "Greek Tax Information",
              })}
            </h3>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {t("afm_label", { ns: "greek" })}
                  {afmValid === true && (
                    <Badge variant="success" className="ml-2">
                      <Check className="w-3 h-3 mr-1" />
                      {t("valid_afm", { ns: "business_entities" })}
                    </Badge>
                  )}
                  {afmValid === false && (
                    <Badge variant="error" className="ml-2">
                      <X className="w-3 h-3 mr-1" />
                      {t("invalid_afm", { ns: "forms" })}
                    </Badge>
                  )}
                </label>
                <Controller
                  name="afm"
                  control={form.control}
                  render={({ field }) => (
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
                      className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                    />
                  )}
                />
              </div>

              <div>
                <Controller
                  name="doy"
                  control={form.control}
                  render={({ field }) => (
                    <DOYSelector
                      value={field.value}
                      onChange={handleDOYSelection}
                      label={t("doy_label", { ns: "greek" })}
                      error={form.formState.errors.doy?.message}
                      className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                    />
                  )}
                />
              </div>
            </div>

            {entityType === "business" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {t("business_activity_label", { ns: "greek" })}
                  </label>
                  <Controller
                    name="business_activity"
                    control={form.control}
                    render={({ field }) => (
                      <Input
                        {...field}
                        placeholder={t("business_activity_placeholder", {
                          ns: "business_entities",
                          defaultValue: "e.g., Software Development",
                        })}
                        error={form.formState.errors.business_activity?.message}
                        className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                      />
                    )}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {t("legal_form_label", { ns: "greek" })}
                  </label>
                  <Controller
                    name="legal_form"
                    control={form.control}
                    render={({ field }) => (
                      <select
                        {...field}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      >
                        <option value="">
                          {t("select_option", { ns: "common" })}
                        </option>
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
                    )}
                  />
                </div>
              </div>
            )}

            <div className="flex items-center space-x-2">
              <Controller
                name="vat_exempt"
                control={form.control}
                render={({ field }) => (
                  <input
                    type="checkbox"
                    id="vat_exempt"
                    checked={field.value}
                    onChange={field.onChange}
                    className="rounded border-gray-300 dark:border-gray-600 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 dark:bg-gray-700"
                  />
                )}
              />
              <label
                htmlFor="vat_exempt"
                className="text-sm text-gray-700 dark:text-gray-300"
              >
                {t("vat_exempt", { ns: "business_entities" })}
              </label>
            </div>
          </CardContent>
        </Card>

        {/* Legacy Website Field */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
            <h3 className="text-lg font-semibold flex items-center gap-2 text-gray-900 dark:text-white">
              <FileText className="w-5 h-5" />
              {t("additional_info", {
                ns: "business_entities",
                defaultValue: "Additional Information",
              })}
            </h3>
          </CardHeader>
          <CardContent className="p-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t("website", {
                  ns: "business_entities",
                  defaultValue: "Website",
                })}
              </label>
              <Controller
                name="website"
                control={form.control}
                render={({ field }) => (
                  <Input
                    {...field}
                    placeholder="https://example.com"
                    error={form.formState.errors.website?.message}
                    className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                  />
                )}
              />
            </div>
          </CardContent>
        </Card>

        {/* Multi-Contact Information */}
        <Controller
          name="contact_methods"
          control={form.control}
          render={({ field }) => (
            <MultiContactManager
              value={(field.value as any[]) || []}
              onChange={field.onChange}
              disabled={loading}
            />
          )}
        />

        {/* Business Settings (for customers/suppliers) */}
        {(initialRole === "customer" || initialRole === "supplier") && (
          <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                {t("business_settings", {
                  ns: "business_entities",
                  defaultValue: "Business Settings",
                })}
              </h3>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {t("payment_terms", {
                      ns: "business_entities",
                      defaultValue: "Payment Terms",
                    })}
                  </label>
                  <Controller
                    name="payment_terms"
                    control={form.control}
                    render={({ field }) => (
                      <select
                        {...field}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      >
                        <option value="net_0">
                          {t("cash_on_delivery", {
                            ns: "business_entities",
                            defaultValue: "Cash on Delivery",
                          })}
                        </option>
                        <option value="net_15">
                          {t("net_15", {
                            ns: "business_entities",
                            defaultValue: "Net 15 days",
                          })}
                        </option>
                        <option value="net_30">
                          {t("net_30", {
                            ns: "business_entities",
                            defaultValue: "Net 30 days",
                          })}
                        </option>
                        <option value="net_60">
                          {t("net_60", {
                            ns: "business_entities",
                            defaultValue: "Net 60 days",
                          })}
                        </option>
                        <option value="net_90">
                          {t("net_90", {
                            ns: "business_entities",
                            defaultValue: "Net 90 days",
                          })}
                        </option>
                        <option value="prepaid">
                          {t("prepaid", {
                            ns: "business_entities",
                            defaultValue: "Prepaid",
                          })}
                        </option>
                      </select>
                    )}
                  />
                </div>

                {initialRole === "customer" && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      {t("credit_limit", {
                        ns: "business_entities",
                        defaultValue: "Credit Limit (€)",
                      })}
                    </label>
                    <Controller
                      name="credit_limit"
                      control={form.control}
                      render={({ field }) => (
                        <Input
                          {...field}
                          type="number"
                          min="0"
                          placeholder="0"
                          onChange={(e) =>
                            field.onChange(parseFloat(e.target.value) || 0)
                          }
                          error={form.formState.errors.credit_limit?.message}
                          className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                        />
                      )}
                    />
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {t("discount_percentage", {
                      ns: "business_entities",
                      defaultValue: "Discount (%)",
                    })}
                  </label>
                  <Controller
                    name="discount_percentage"
                    control={form.control}
                    render={({ field }) => (
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
                        className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                      />
                    )}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Notes */}
        <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {t("additional_notes", {
                ns: "business_entities",
                defaultValue: "Additional Notes",
              })}
            </h3>
          </CardHeader>
          <CardContent className="p-6">
            <Controller
              name="notes"
              control={form.control}
              render={({ field }) => (
                <textarea
                  {...field}
                  rows={4}
                  placeholder={t("notes_placeholder", {
                    ns: "business_entities",
                    defaultValue: "Additional notes about this entity...",
                  })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                />
              )}
            />
          </CardContent>
        </Card>

        {/* Create Another Option - Only show in create mode */}
        {mode === "create" && onCreateAnotherChange && (
          <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="createAnother"
                checked={createAnother}
                onChange={(e) => onCreateAnotherChange(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor="createAnother"
                className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer"
              >
                <Plus className="w-4 h-4 text-green-600" />
                {t("create_another_customer", {
                  ns: "customers",
                  defaultValue: "Create another customer after saving",
                })}
              </label>
            </div>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400 ml-7">
              {t("create_another_description", {
                ns: "customers",
                defaultValue:
                  "Check this to stay on the creation page and add multiple customers quickly",
              })}
            </p>
          </div>
        )}

        {/* Form Actions */}
        <div className="flex flex-col sm:flex-row items-center justify-end space-y-4 sm:space-y-0 sm:space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          {onCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              className="w-full sm:w-auto order-2 sm:order-1"
            >
              {t("cancel", { ns: "common" })}
            </Button>
          )}
          <LoadingButton
            type="submit"
            loading={loading}
            disabled={loading}
            className="w-full sm:w-auto order-1 sm:order-2"
          >
            {mode === "create"
              ? t("create", { ns: "common" })
              : t("update", { ns: "common" })}{" "}
            {t(`role_${initialRole}`, { ns: "business_entities" })}
          </LoadingButton>
        </div>
      </form>
    </div>
  );
}
