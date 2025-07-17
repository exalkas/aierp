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
  title = "Business Entities",
  showCreateButton = true,
  onCreateClick,
  onEntityClick,
  className = "",
}: BusinessEntityListProps) {
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
      filters.entityTypes.forEach((type) => {
        params.append("entity_type", type);
      });
    }

    // Statuses
    if (filters.statuses?.length) {
      filters.statuses.forEach((status) => {
        params.append("status", status);
      });
    }

    // Additional roles (beyond the main roleFilter)
    if (filters.roles?.length) {
      filters.roles.forEach((role) => {
        params.append("additional_roles", role);
      });
    }

    // Greek-specific filters
    if (filters.hasValidAFM !== undefined) {
      params.append("has_valid_afm", filters.hasValidAFM.toString());
    }

    if (filters.vatExempt !== undefined) {
      params.append("vat_exempt", filters.vatExempt.toString());
    }

    if (filters.legalForms?.length) {
      filters.legalForms.forEach((form) => {
        params.append("legal_form", form);
      });
    }

    // Financial filters
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

    // Location filters
    if (filters.regions?.length) {
      filters.regions.forEach((region) => {
        params.append("region", region);
      });
    }

    return params;
  };

  // Fetch business entities from API
  const fetchEntities = async (filters: AdvancedFilters, page: number = 1) => {
    if (!tokens?.accessToken) {
      setError("Authentication required");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const params = buildAPIParams(filters, page);

      console.log("BusinessEntityList - Making API call:", {
        url: `/api/v1/business-entities/?${params}`,
        hasToken: !!tokens.accessToken,
        tokenLength: tokens.accessToken?.length,
        tokenExpiry: tokens.expiresAt,
      });

      const response = await fetch(`/api/v1/business-entities/?${params}`, {
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
      <Badge variant={variants[status] || "info"}>{status.toUpperCase()}</Badge>
    );
  };

  const getRoleBadges = (roles: string[]) => {
    return roles.map((role) => (
      <Badge key={role} variant="outline">
        {role.charAt(0).toUpperCase() + role.slice(1)}
      </Badge>
    ));
  };

  if (error) {
    return (
      <Card className={className}>
        <CardContent>
          <EmptyState
            title="Error Loading Entities"
            description={error}
            variant="error"
            actions={[
              {
                label: "Retry",
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
          <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
          <p className="text-gray-600">
            Manage your business relationships and contacts
          </p>
        </div>
        {showCreateButton && (
          <Button onClick={onCreateClick} className="flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Add New
          </Button>
        )}
      </div>

      {/* Quick Search */}
      <Card>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  type="text"
                  placeholder="Quick search by name, email, AFM, or entity code..."
                  value={quickSearch}
                  onChange={(e) => setQuickSearch(e.target.value)}
                  className="pl-10"
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
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">
              {totalCount} {totalCount === 1 ? "Entity" : "Entities"} Found
            </h3>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              {roleFilter !== "all" && (
                <Badge variant="outline">
                  Filter:{" "}
                  {roleFilter.charAt(0).toUpperCase() + roleFilter.slice(1)}
                </Badge>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <LoadingButton loading={true}>Loading entities...</LoadingButton>
            </div>
          ) : entities.length === 0 ? (
            <EmptyState
              title="No Business Entities Found"
              description={
                Object.keys(advancedFilters).length > 0 || quickSearch
                  ? "Try adjusting your search criteria or filters"
                  : "Create your first business entity to get started"
              }
              actions={
                showCreateButton
                  ? [
                      {
                        label: "Create Entity",
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
                    className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors cursor-pointer"
                    onClick={() => onEntityClick?.(entity)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {getEntityTypeIcon(entity.entity_type)}
                        <h4 className="font-semibold text-gray-900">
                          {entity.display_name}
                        </h4>
                        {entity.has_valid_afm && (
                          <Badge variant="success" size="sm">
                            Valid AFM
                          </Badge>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusBadge(entity.status)}
                        <Button variant="ghost" size="sm">
                          <Eye className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm text-gray-600">
                      <div>
                        <span className="font-medium">Contact:</span>
                        <div>{entity.email || "No email"}</div>
                        <div>{entity.phone || "No phone"}</div>
                      </div>
                      <div>
                        <span className="font-medium">Greek Info:</span>
                        <div>AFM: {entity.afm || "N/A"}</div>
                        <div>DOY: {entity.doy || "N/A"}</div>
                      </div>
                      <div>
                        <span className="font-medium">Address:</span>
                        <div>{entity.primary_address || "No address"}</div>
                      </div>
                      <div>
                        <span className="font-medium">Roles:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {getRoleBadges(entity.roles)}
                        </div>
                      </div>
                    </div>

                    {(entity.total_sales > 0 || entity.total_purchases > 0) && (
                      <div className="mt-3 pt-3 border-t border-gray-100">
                        <div className="flex justify-between text-sm">
                          {entity.total_sales > 0 && (
                            <span>
                              Sales: €{entity.total_sales.toLocaleString()}
                            </span>
                          )}
                          {entity.total_purchases > 0 && (
                            <span>
                              Purchases: €
                              {entity.total_purchases.toLocaleString()}
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <div className="text-sm text-gray-600">
                    Showing {entities.length} of {totalCount} entities
                    {currentPage > 1 &&
                      ` (Page ${currentPage} of ${totalPages})`}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={currentPage === 1}
                      onClick={() => handlePageChange(currentPage - 1)}
                    >
                      Previous
                    </Button>

                    {/* Page numbers for larger screens */}
                    <div className="hidden sm:flex gap-1">
                      {Array.from(
                        { length: Math.min(5, totalPages) },
                        (_, i) => {
                          const pageNum = Math.max(1, currentPage - 2) + i;
                          if (pageNum > totalPages) return null;

                          return (
                            <Button
                              key={pageNum}
                              variant={
                                currentPage === pageNum ? "primary" : "outline"
                              }
                              size="sm"
                              onClick={() => handlePageChange(pageNum)}
                            >
                              {pageNum}
                            </Button>
                          );
                        }
                      )}
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      disabled={currentPage === totalPages}
                      onClick={() => handlePageChange(currentPage + 1)}
                    >
                      Next
                    </Button>
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
