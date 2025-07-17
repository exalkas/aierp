"use client";

import React, { useState } from "react";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Input,
  Badge,
  Checkbox,
  useTranslation,
} from "@erp/shared-ui";
import {
  Filter,
  X,
  ChevronDown,
  ChevronUp,
  Calendar,
  MapPin,
  Building2,
  CreditCard,
  FileText,
  RotateCcw,
} from "lucide-react";

export interface AdvancedFilters {
  // Basic filters
  search?: string;
  entityTypes?: string[];
  statuses?: string[];
  roles?: string[];

  // Greek-specific filters
  hasValidAFM?: boolean;
  doyRegions?: string[];
  legalForms?: string[];
  vatExempt?: boolean;

  // Business filters
  creditLimitMin?: number;
  creditLimitMax?: number;
  totalSalesMin?: number;
  totalSalesMax?: number;

  // Date filters
  createdAfter?: string;
  createdBefore?: string;
  lastContactAfter?: string;
  lastContactBefore?: string;

  // Location filters
  regions?: string[];
  cities?: string[];
}

export interface BusinessEntityAdvancedFiltersProps {
  filters: AdvancedFilters;
  onFiltersChange: (filters: AdvancedFilters) => void;
  onClearAll: () => void;
  className?: string;
}

export default function BusinessEntityAdvancedFilters({
  filters,
  onFiltersChange,
  onClearAll,
  className = "",
}: BusinessEntityAdvancedFiltersProps) {
  const { t } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  const updateFilter = (key: keyof AdvancedFilters, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value,
    });
  };

  const toggleArrayFilter = (key: keyof AdvancedFilters, value: string) => {
    const currentArray = (filters[key] as string[]) || [];
    const newArray = currentArray.includes(value)
      ? currentArray.filter((item) => item !== value)
      : [...currentArray, value];

    updateFilter(key, newArray.length > 0 ? newArray : undefined);
  };

  const getActiveFiltersCount = () => {
    let count = 0;

    if (filters.search) count++;
    if (filters.entityTypes?.length) count++;
    if (filters.statuses?.length) count++;
    if (filters.roles?.length) count++;
    if (filters.hasValidAFM !== undefined) count++;
    if (filters.doyRegions?.length) count++;
    if (filters.legalForms?.length) count++;
    if (filters.vatExempt !== undefined) count++;
    if (
      filters.creditLimitMin !== undefined ||
      filters.creditLimitMax !== undefined
    )
      count++;
    if (
      filters.totalSalesMin !== undefined ||
      filters.totalSalesMax !== undefined
    )
      count++;
    if (filters.createdAfter || filters.createdBefore) count++;
    if (filters.lastContactAfter || filters.lastContactBefore) count++;
    if (filters.regions?.length) count++;
    if (filters.cities?.length) count++;

    return count;
  };

  const activeFiltersCount = getActiveFiltersCount();

  return (
    <Card
      className={`${className} bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700`}
    >
      <CardHeader className="bg-white dark:bg-gray-800 dark:text-white">
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-2 dark:border-gray-600 dark:text-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700"
          >
            <Filter size={16} />
            {t("advanced_filters", { ns: "business_entities" })}
            {activeFiltersCount > 0 && (
              <Badge variant="secondary" size="sm" className="ml-1">
                {activeFiltersCount}
              </Badge>
            )}
            {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </Button>

          {activeFiltersCount > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearAll}
              className="flex items-center gap-1 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              <RotateCcw size={14} />
              {t("clear_all", { ns: "common" })}
            </Button>
          )}
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="space-y-6 bg-white dark:bg-gray-800">
          {/* Entity Types */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <Building2 size={16} />
              {t("entity_types", { ns: "business_entities" })}
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {["business", "individual", "government", "non_profit"].map(
                (type) => (
                  <label
                    key={type}
                    className="flex items-center space-x-2 text-sm cursor-pointer"
                  >
                    <Checkbox
                      checked={filters.entityTypes?.includes(type) || false}
                      onChange={() => toggleArrayFilter("entityTypes", type)}
                      className="dark:border-gray-600"
                    />
                    <span className="text-gray-700 dark:text-gray-300">
                      {t(`entity_type_${type}`, { ns: "business_entities" })}
                    </span>
                  </label>
                )
              )}
            </div>
          </div>

          {/* Status */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <FileText size={16} />
              {t("status", { ns: "business_entities" })}
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
              {["active", "inactive", "suspended", "prospect", "blocked"].map(
                (status) => (
                  <label
                    key={status}
                    className="flex items-center space-x-2 text-sm cursor-pointer"
                  >
                    <Checkbox
                      checked={filters.statuses?.includes(status) || false}
                      onChange={() => toggleArrayFilter("statuses", status)}
                      className="dark:border-gray-600"
                    />
                    <span className="text-gray-700 dark:text-gray-300">
                      {t(`status_${status}`, { ns: "business_entities" })}
                    </span>
                  </label>
                )
              )}
            </div>
          </div>

          {/* Roles */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <CreditCard size={16} />
              {t("roles", { ns: "business_entities" })}
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {["customer", "supplier", "partner"].map((role) => (
                <label
                  key={role}
                  className="flex items-center space-x-2 text-sm cursor-pointer"
                >
                  <Checkbox
                    checked={filters.roles?.includes(role) || false}
                    onChange={() => toggleArrayFilter("roles", role)}
                    className="dark:border-gray-600"
                  />
                  <span className="text-gray-700 dark:text-gray-300">
                    {t(`role_${role}`, { ns: "business_entities" })}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Greek-specific Filters */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <MapPin size={16} />
              {t("greek_filters", { ns: "business_entities" })}
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className="flex items-center space-x-2 text-sm cursor-pointer">
                <Checkbox
                  checked={filters.hasValidAFM === true}
                  onChange={() =>
                    updateFilter(
                      "hasValidAFM",
                      filters.hasValidAFM === true ? undefined : true
                    )
                  }
                  className="dark:border-gray-600"
                />
                <span className="text-gray-700 dark:text-gray-300">
                  {t("has_valid_afm", { ns: "business_entities" })}
                </span>
              </label>

              <label className="flex items-center space-x-2 text-sm cursor-pointer">
                <Checkbox
                  checked={filters.vatExempt === true}
                  onChange={() =>
                    updateFilter(
                      "vatExempt",
                      filters.vatExempt === true ? undefined : true
                    )
                  }
                  className="dark:border-gray-600"
                />
                <span className="text-gray-700 dark:text-gray-300">
                  {t("vat_exempt", { ns: "business_entities" })}
                </span>
              </label>
            </div>
          </div>

          {/* Date Filters */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <Calendar size={16} />
              {t("date_filters", { ns: "business_entities" })}
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 dark:text-gray-300 mb-1">
                  {t("created_after", { ns: "business_entities" })}
                </label>
                <Input
                  type="date"
                  value={filters.createdAfter || ""}
                  onChange={(e) =>
                    updateFilter("createdAfter", e.target.value || undefined)
                  }
                  className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-700 dark:text-gray-300 mb-1">
                  {t("created_before", { ns: "business_entities" })}
                </label>
                <Input
                  type="date"
                  value={filters.createdBefore || ""}
                  onChange={(e) =>
                    updateFilter("createdBefore", e.target.value || undefined)
                  }
                  className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
            </div>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
