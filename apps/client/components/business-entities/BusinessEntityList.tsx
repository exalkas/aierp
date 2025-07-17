"use client";

import React, { useState, useEffect } from "react";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Input,
  Badge,
  EmptyState,
  LoadingButton,
  useTranslation,
} from "@erp/shared-ui";
import {
  Search,
  Plus,
  Building2,
  Users,
  Briefcase,
  Filter,
  Eye,
  Edit,
} from "lucide-react";
import { useAuth } from "@erp/shared-ui";
import BusinessEntityAdvancedFilters, {
  AdvancedFilters,
} from "./BusinessEntityAdvancedFilters";

interface BusinessEntity {
  id: string;
  display_name: string;
  business_name?: string;
  first_name?: string;
  last_name?: string;
  afm?: string;
  doy?: string;
  email?: string;
  phone?: string;
  entity_type: "business" | "individual" | "government" | "non_profit";
  status: "active" | "inactive" | "suspended" | "prospect" | "blocked";
  roles: string[];
  primary_address: string;
  total_sales: number;
  total_purchases: number;
  has_valid_afm: boolean;
  created_at: string;
}

interface BusinessEntityListResponse {
  entities: BusinessEntity[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface BusinessEntityListProps {
  roleFilter?: "customer" | "supplier" | "partner" | "all";
  title?: string;
  showCreateButton?: boolean;
  onCreateClick?: () => void;
  onEntityClick?: (entity: BusinessEntity) => void;
  className?: string;
}

export default function BusinessEntityList({
  roleFilter = "all",
  title,
  showCreateButton = true,
  onCreateClick,
  onEntityClick,
  className = "",
}: BusinessEntityListProps) {
  const { t } = useTranslation();
  const { tokens } = useAuth();
  const [entities, setEntities] = useState<BusinessEntity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Advanced filters state
  const [advancedFilters, setAdvancedFilters] = useState<AdvancedFilters>({});
  const [quickSearch, setQuickSearch] = useState("");

  // Convert advanced filters to API parameters
  const buildAPIParams = (filters: AdvancedFilters, page: number = 1) => {
    const params = new URLSearchParams();

    // Pagination
    params.append("skip", ((page - 1) * 20).toString());
    params.append("limit", "20");

    // Role filter from props
    if (roleFilter !== "all") {
      params.append("role_filter", roleFilter);
    }

    // Search
    const searchTerm = filters.search || quickSearch;
    if (searchTerm) {
      params.append("search", searchTerm);
    }

    // Entity types
    if (filters.entityTypes?.length) {
      filters.entityTypes.forEach((type) =>
        params.append("entity_types", type)
      );
    }

    // Status
    if (filters.statuses?.length) {
      filters.statuses.forEach((status) => params.append("statuses", status));
    }

    // Roles
    if (filters.roles?.length) {
      filters.roles.forEach((role) => params.append("roles", role));
    }

    // Greek-specific filters
    if (filters.hasValidAFM !== undefined) {
      params.append("has_valid_afm", filters.hasValidAFM.toString());
    }

    if (filters.doyRegions?.length) {
      filters.doyRegions.forEach((region) =>
        params.append("doy_regions", region)
      );
    }

    if (filters.legalForms?.length) {
      filters.legalForms.forEach((form) => params.append("legal_forms", form));
    }

    if (filters.vatExempt !== undefined) {
      params.append("vat_exempt", filters.vatExempt.toString());
    }

    // Business filters
    if (filters.creditLimitMin !== undefined) {
      params.append("credit_limit_min", filters.creditLimitMin.toString());
    }

    if (filters.creditLimitMax !== undefined) {
      params.append("credit_limit_max", filters.creditLimitMax.toString());
    }

    if (filters.totalSalesMin !== undefined) {
      params.append("total_sales_min", filters.totalSalesMin.toString());
    }

    if (filters.totalSalesMax !== undefined) {
      params.append("total_sales_max", filters.totalSalesMax.toString());
    }

    // Date filters
    if (filters.createdAfter) {
      params.append("created_after", filters.createdAfter);
    }

    if (filters.createdBefore) {
      params.append("created_before", filters.createdBefore);
    }

    if (filters.lastContactAfter) {
      params.append("last_contact_after", filters.lastContactAfter);
    }

    if (filters.lastContactBefore) {
      params.append("last_contact_before", filters.lastContactBefore);
    }

    // Location filters
    if (filters.regions?.length) {
      filters.regions.forEach((region) => params.append("regions", region));
    }

    if (filters.cities?.length) {
      filters.cities.forEach((city) => params.append("cities", city));
    }

    return params.toString();
  };

  const fetchEntities = async (filters: AdvancedFilters, page: number = 1) => {
    if (!tokens?.accessToken) {
      setError("Authentication required");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const queryParams = buildAPIParams(filters, page);
      const apiUrl = `/api/v1/business-entities${
        queryParams ? `?${queryParams}` : ""
      }`;

      console.log("BusinessEntityList - Fetching:", {
        url: apiUrl,
        roleFilter,
        page,
        filters,
      });

      const response = await fetch(apiUrl, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${tokens.accessToken}`,
          "Content-Type": "application/json",
        },
      });

      console.log("BusinessEntityList - API Response:", {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
      });

      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}`;

        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;

          console.log("BusinessEntityList - Error details:", {
            status: response.status,
            errorData,
          });

          // If it's a 401 or 403, might be a token issue
          if (response.status === 401 || response.status === 403) {
            errorMessage += " - Please try logging out and logging back in.";
          }
        } catch (parseError) {
          console.log("BusinessEntityList - Could not parse error response");
        }

        throw new Error(errorMessage);
      }

      const data: BusinessEntityListResponse = await response.json();
      setEntities(data.entities || []);
      setTotalCount(data.total_count || 0);
      setCurrentPage(data.page || 1);
      setTotalPages(data.total_pages || 1);

      console.log("BusinessEntityList - Success:", {
        entitiesCount: data.entities?.length || 0,
        totalCount: data.total_count,
      });
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Failed to fetch business entities";
      setError(errorMessage);
      console.error("BusinessEntityList - Error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Debounced search effect
  useEffect(() => {
    const delayedSearch = setTimeout(() => {
      fetchEntities(advancedFilters, 1);
    }, 300);

    return () => clearTimeout(delayedSearch);
  }, [tokens, advancedFilters, quickSearch, roleFilter]);

  const handlePageChange = (page: number) => {
    fetchEntities(advancedFilters, page);
  };

  const handleFiltersChange = (newFilters: AdvancedFilters) => {
    setAdvancedFilters(newFilters);
    setCurrentPage(1); // Reset to first page when filters change
  };

  const handleClearAllFilters = () => {
    setAdvancedFilters({});
    setQuickSearch("");
    setCurrentPage(1);
  };

  const getEntityTypeIcon = (entityType: string) => {
    switch (entityType) {
      case "business":
        return <Building2 className="w-4 h-4" />;
      case "individual":
        return <Users className="w-4 h-4" />;
      default:
        return <Briefcase className="w-4 h-4" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "success" | "warning" | "error" | "info"> = {
      active: "success",
      inactive: "warning",
      suspended: "error",
      prospect: "info",
      blocked: "error",
    };

    return (
      <Badge variant={variants[status] || "info"}>
        {t(`status_${status}`, { ns: "business_entities" })}
      </Badge>
    );
  };

  const getRoleBadges = (roles: string[]) => {
    return roles.map((role) => (
      <Badge key={role} variant="outline">
        {t(`role_${role}`, { ns: "business_entities" })}
      </Badge>
    ));
  };

  // Get contextual button text and title
  const getContextualText = () => {
    // All translation keys are in the business_entities namespace
    const namespace = "business_entities";

    const defaultTitle =
      title || t(`${roleFilter}_directory`, { ns: namespace });
    const defaultDescription = t(`manage_${roleFilter}_relationships`, {
      ns: namespace,
    });
    const buttonText = t(`add_new_${roleFilter}`, { ns: namespace });
    const createButtonText = t(`create_${roleFilter}`, { ns: namespace });

    return {
      title: defaultTitle,
      description: defaultDescription,
      buttonText,
      createButtonText,
    };
  };

  const contextualText = getContextualText();

  if (error) {
    return (
      <Card
        className={`${className} bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700`}
      >
        <CardContent>
          <EmptyState
            title={t("error_loading_entities", { ns: "business_entities" })}
            description={error}
            variant="error"
            actions={[
              {
                label: t("retry", { ns: "common" }),
                onClick: () => fetchEntities(advancedFilters, currentPage),
                variant: "primary",
              },
            ]}
          />
        </CardContent>
      </Card>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {contextualText.title}
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            {contextualText.description}
          </p>
        </div>
        {showCreateButton && (
          <Button
            onClick={onCreateClick}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white dark:bg-blue-700 dark:hover:bg-blue-600"
          >
            <Plus className="w-4 h-4" />
            {contextualText.buttonText}
          </Button>
        )}
      </div>

      {/* Quick Search */}
      <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-4 h-4" />
                <Input
                  type="text"
                  placeholder={t("quick_search_placeholder", {
                    ns: "business_entities",
                  })}
                  value={quickSearch}
                  onChange={(e) => setQuickSearch(e.target.value)}
                  className="pl-10 bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Filters */}
      <BusinessEntityAdvancedFilters
        filters={advancedFilters}
        onFiltersChange={handleFiltersChange}
        onClearAll={handleClearAllFilters}
      />

      {/* Results */}
      <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardHeader>
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {(() => {
                // Determine the correct translation key based on role filter
                let singularKey, pluralKey;

                if (roleFilter === "customer") {
                  singularKey = "customer_found";
                  pluralKey = "customers_found";
                } else if (roleFilter === "supplier") {
                  singularKey = "supplier_found";
                  pluralKey = "suppliers_found";
                } else {
                  singularKey = "entity_found";
                  pluralKey = "entities_found";
                }

                const key = totalCount === 1 ? singularKey : pluralKey;
                return t(key, { ns: "business_entities" }).replace(
                  "{{count}}",
                  String(totalCount)
                );
              })()}
            </h3>
            <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              {/* Remove confusing filter badge */}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <LoadingButton loading={true}>
                {t("loading_entities", { ns: "business_entities" })}
              </LoadingButton>
            </div>
          ) : entities.length === 0 ? (
            <EmptyState
              title={(() => {
                if (roleFilter === "customer") {
                  return t("no_customers_found", { ns: "business_entities" });
                } else if (roleFilter === "supplier") {
                  return t("no_suppliers_found", { ns: "business_entities" });
                } else {
                  return t("no_entities_found", { ns: "business_entities" });
                }
              })()}
              description={
                Object.keys(advancedFilters).length > 0 || quickSearch
                  ? t("try_adjusting_filters", { ns: "business_entities" })
                  : (() => {
                      if (roleFilter === "customer") {
                        return t("create_first_customer", {
                          ns: "business_entities",
                        });
                      } else if (roleFilter === "supplier") {
                        return t("create_first_supplier", {
                          ns: "business_entities",
                        });
                      } else {
                        return t("create_first_entity", {
                          ns: "business_entities",
                        });
                      }
                    })()
              }
              className="text-gray-600 dark:text-gray-300"
              actions={
                showCreateButton
                  ? [
                      {
                        label: contextualText.createButtonText,
                        onClick: onCreateClick,
                        variant: "primary",
                        icon: <Plus className="w-4 h-4" />,
                      },
                    ]
                  : undefined
              }
            />
          ) : (
            <div className="space-y-4">
              {/* Entity List */}
              <div className="grid gap-4">
                {entities.map((entity) => (
                  <div
                    key={entity.id}
                    className="p-4 border border-gray-200 dark:border-gray-600 rounded-lg hover:border-gray-300 dark:hover:border-gray-500 transition-colors cursor-pointer bg-white dark:bg-gray-700"
                    onClick={() => onEntityClick?.(entity)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {getEntityTypeIcon(entity.entity_type)}
                        <h4 className="font-semibold text-gray-900 dark:text-white">
                          {entity.display_name}
                        </h4>
                        {entity.has_valid_afm && (
                          <Badge variant="success" size="sm">
                            {t("valid_afm", { ns: "business_entities" })}
                          </Badge>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(entity.status)}
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500 dark:text-gray-400">
                          {t("contact_info", { ns: "business_entities" })}:
                        </span>
                        <div className="text-gray-900 dark:text-white">
                          {entity.email && <div>{entity.email}</div>}
                          {entity.phone && <div>{entity.phone}</div>}
                        </div>
                      </div>

                      <div>
                        <span className="text-gray-500 dark:text-gray-400">
                          {t("business_details", { ns: "business_entities" })}:
                        </span>
                        <div className="text-gray-900 dark:text-white">
                          {entity.afm && <div>AFM: {entity.afm}</div>}
                          {entity.doy && <div>DOY: {entity.doy}</div>}
                        </div>
                      </div>

                      <div>
                        <span className="text-gray-500 dark:text-gray-400">
                          {t("roles", { ns: "business_entities" })}:
                        </span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {getRoleBadges(entity.roles)}
                        </div>
                      </div>
                    </div>

                    {entity.primary_address && (
                      <div className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                        <span>
                          {t("address", { ns: "business_entities" })}:{" "}
                        </span>
                        {entity.primary_address}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
                    >
                      {t("previous", { ns: "common" })}
                    </Button>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {t("page_of", {
                        ns: "common",
                        variables: { current: currentPage, total: totalPages },
                      })}
                    </span>
                    <Button
                      variant="outline"
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                      className="dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
                    >
                      {t("next", { ns: "common" })}
                    </Button>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {t("showing_results", {
                      ns: "common",
                      variables: {
                        start: (currentPage - 1) * 20 + 1,
                        end: Math.min(currentPage * 20, totalCount),
                        total: totalCount,
                      },
                    })}
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
