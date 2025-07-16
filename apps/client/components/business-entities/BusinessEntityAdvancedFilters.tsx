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

  const entityTypeOptions = [
    { value: "business", label: "Business" },
    { value: "individual", label: "Individual" },
    { value: "government", label: "Government" },
    { value: "non_profit", label: "Non-Profit" },
  ];

  const statusOptions = [
    { value: "active", label: "Active" },
    { value: "inactive", label: "Inactive" },
    { value: "suspended", label: "Suspended" },
    { value: "prospect", label: "Prospect" },
    { value: "blocked", label: "Blocked" },
  ];

  const roleOptions = [
    { value: "customer", label: "Customer" },
    { value: "supplier", label: "Supplier" },
    { value: "partner", label: "Partner" },
    { value: "competitor", label: "Competitor" },
    { value: "lead", label: "Lead" },
  ];

  const legalFormOptions = [
    { value: "AE", label: "ΑΕ (Ανώνυμη Εταιρεία)" },
    { value: "EPE", label: "ΕΠΕ (Εταιρεία Περιορισμένης Ευθύνης)" },
    { value: "OE", label: "ΟΕ (Ομόρρυθμη Εταιρεία)" },
    { value: "EE", label: "ΕΕ (Ετερόρρυθμη Εταιρεία)" },
    { value: "IKE", label: "ΙΚΕ (Ιδιωτική Κεφαλαιουχική Εταιρεία)" },
    { value: "AT", label: "ΑΤ (Ατομική Επιχείρηση)" },
  ];

  const greekRegions = [
    "Αττική",
    "Κεντρική Μακεδονία",
    "Θεσσαλία",
    "Κρήτη",
    "Δυτική Ελλάδα",
    "Πελοπόννησος",
    "Ήπειρος",
    "Ανατολική Μακεδονία και Θράκη",
    "Δυτική Μακεδονία",
    "Στερεά Ελλάδα",
    "Βόρειο Αιγαίο",
    "Νότιο Αιγαίο",
    "Ιόνια Νησιά",
  ];

  const FilterSection = ({
    title,
    icon: Icon,
    sectionKey,
    children,
  }: {
    title: string;
    icon: any;
    sectionKey: string;
    children: React.ReactNode;
  }) => (
    <div className="border border-gray-200 rounded-lg">
      <button
        className="w-full p-3 flex items-center justify-between text-left hover:bg-gray-50"
        onClick={() =>
          setActiveSection(activeSection === sectionKey ? null : sectionKey)
        }
      >
        <div className="flex items-center gap-2">
          <Icon className="w-4 h-4 text-gray-600" />
          <span className="font-medium text-gray-700">{title}</span>
        </div>
        {activeSection === sectionKey ? (
          <ChevronUp className="w-4 h-4 text-gray-500" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-500" />
        )}
      </button>
      {activeSection === sectionKey && (
        <div className="p-3 border-t border-gray-200 bg-gray-50">
          {children}
        </div>
      )}
    </div>
  );

  const CheckboxGroup = ({
    options,
    selectedValues,
    onChange,
  }: {
    options: { value: string; label: string }[];
    selectedValues?: string[];
    onChange: (value: string) => void;
  }) => (
    <div className="space-y-2">
      {options.map((option) => (
        <label
          key={option.value}
          className="flex items-center space-x-2 cursor-pointer"
        >
          <Checkbox
            checked={selectedValues?.includes(option.value) || false}
            onChange={() => onChange(option.value)}
          />
          <span className="text-sm text-gray-700">{option.label}</span>
        </label>
      ))}
    </div>
  );

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Filter Toggle and Active Count */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2"
        >
          <Filter className="w-4 h-4" />
          Advanced Filters
          {getActiveFiltersCount() > 0 && (
            <Badge variant="info">{getActiveFiltersCount()}</Badge>
          )}
          {isExpanded ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </Button>

        {getActiveFiltersCount() > 0 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onClearAll}
            className="flex items-center gap-1"
          >
            <RotateCcw className="w-3 h-3" />
            Clear All
          </Button>
        )}
      </div>

      {/* Active Filters Summary */}
      {getActiveFiltersCount() > 0 && (
        <div className="flex flex-wrap gap-2">
          {filters.search && (
            <Badge variant="outline" className="flex items-center gap-1">
              Search: {filters.search}
              <X
                className="w-3 h-3 cursor-pointer"
                onClick={() => updateFilter("search", undefined)}
              />
            </Badge>
          )}
          {filters.entityTypes?.map((type) => (
            <Badge
              key={type}
              variant="outline"
              className="flex items-center gap-1"
            >
              Type: {type}
              <X
                className="w-3 h-3 cursor-pointer"
                onClick={() => toggleArrayFilter("entityTypes", type)}
              />
            </Badge>
          ))}
          {filters.statuses?.map((status) => (
            <Badge
              key={status}
              variant="outline"
              className="flex items-center gap-1"
            >
              Status: {status}
              <X
                className="w-3 h-3 cursor-pointer"
                onClick={() => toggleArrayFilter("statuses", status)}
              />
            </Badge>
          ))}
          {filters.roles?.map((role) => (
            <Badge
              key={role}
              variant="outline"
              className="flex items-center gap-1"
            >
              Role: {role}
              <X
                className="w-3 h-3 cursor-pointer"
                onClick={() => toggleArrayFilter("roles", role)}
              />
            </Badge>
          ))}
          {filters.hasValidAFM !== undefined && (
            <Badge variant="outline" className="flex items-center gap-1">
              Valid AFM: {filters.hasValidAFM ? "Yes" : "No"}
              <X
                className="w-3 h-3 cursor-pointer"
                onClick={() => updateFilter("hasValidAFM", undefined)}
              />
            </Badge>
          )}
        </div>
      )}

      {/* Expanded Filters */}
      {isExpanded && (
        <Card>
          <CardContent className="space-y-4">
            {/* Basic Search */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <Input
                type="text"
                placeholder="Search by name, email, AFM, or entity code..."
                value={filters.search || ""}
                onChange={(e) =>
                  updateFilter("search", e.target.value || undefined)
                }
              />
            </div>

            {/* Filter Sections */}
            <div className="space-y-3">
              {/* Entity Types */}
              <FilterSection
                title="Entity Types"
                icon={Building2}
                sectionKey="entityTypes"
              >
                <CheckboxGroup
                  options={entityTypeOptions}
                  selectedValues={filters.entityTypes}
                  onChange={(value) => toggleArrayFilter("entityTypes", value)}
                />
              </FilterSection>

              {/* Status */}
              <FilterSection
                title="Status"
                icon={Building2}
                sectionKey="status"
              >
                <CheckboxGroup
                  options={statusOptions}
                  selectedValues={filters.statuses}
                  onChange={(value) => toggleArrayFilter("statuses", value)}
                />
              </FilterSection>

              {/* Roles */}
              <FilterSection
                title="Business Roles"
                icon={Building2}
                sectionKey="roles"
              >
                <CheckboxGroup
                  options={roleOptions}
                  selectedValues={filters.roles}
                  onChange={(value) => toggleArrayFilter("roles", value)}
                />
              </FilterSection>

              {/* Greek Tax Information */}
              <FilterSection
                title="Greek Tax Information"
                icon={FileText}
                sectionKey="greek"
              >
                <div className="space-y-4">
                  <div>
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <Checkbox
                        checked={filters.hasValidAFM === true}
                        onChange={() =>
                          updateFilter(
                            "hasValidAFM",
                            filters.hasValidAFM === true ? undefined : true
                          )
                        }
                      />
                      <span className="text-sm text-gray-700">
                        Has Valid AFM
                      </span>
                    </label>
                  </div>

                  <div>
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <Checkbox
                        checked={filters.vatExempt === true}
                        onChange={() =>
                          updateFilter(
                            "vatExempt",
                            filters.vatExempt === true ? undefined : true
                          )
                        }
                      />
                      <span className="text-sm text-gray-700">VAT Exempt</span>
                    </label>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Legal Forms
                    </label>
                    <CheckboxGroup
                      options={legalFormOptions}
                      selectedValues={filters.legalForms}
                      onChange={(value) =>
                        toggleArrayFilter("legalForms", value)
                      }
                    />
                  </div>
                </div>
              </FilterSection>

              {/* Location */}
              <FilterSection
                title="Location"
                icon={MapPin}
                sectionKey="location"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Greek Regions
                  </label>
                  <CheckboxGroup
                    options={greekRegions.map((region) => ({
                      value: region,
                      label: region,
                    }))}
                    selectedValues={filters.regions}
                    onChange={(value) => toggleArrayFilter("regions", value)}
                  />
                </div>
              </FilterSection>

              {/* Financial Filters */}
              <FilterSection
                title="Financial Information"
                icon={CreditCard}
                sectionKey="financial"
              >
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Credit Limit (€)
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <Input
                        type="number"
                        placeholder="Min"
                        value={filters.creditLimitMin || ""}
                        onChange={(e) =>
                          updateFilter(
                            "creditLimitMin",
                            e.target.value
                              ? parseFloat(e.target.value)
                              : undefined
                          )
                        }
                      />
                      <Input
                        type="number"
                        placeholder="Max"
                        value={filters.creditLimitMax || ""}
                        onChange={(e) =>
                          updateFilter(
                            "creditLimitMax",
                            e.target.value
                              ? parseFloat(e.target.value)
                              : undefined
                          )
                        }
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Total Sales (€)
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <Input
                        type="number"
                        placeholder="Min"
                        value={filters.totalSalesMin || ""}
                        onChange={(e) =>
                          updateFilter(
                            "totalSalesMin",
                            e.target.value
                              ? parseFloat(e.target.value)
                              : undefined
                          )
                        }
                      />
                      <Input
                        type="number"
                        placeholder="Max"
                        value={filters.totalSalesMax || ""}
                        onChange={(e) =>
                          updateFilter(
                            "totalSalesMax",
                            e.target.value
                              ? parseFloat(e.target.value)
                              : undefined
                          )
                        }
                      />
                    </div>
                  </div>
                </div>
              </FilterSection>

              {/* Date Filters */}
              <FilterSection
                title="Date Filters"
                icon={Calendar}
                sectionKey="dates"
              >
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Created Date
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <Input
                        type="date"
                        placeholder="From"
                        value={filters.createdAfter || ""}
                        onChange={(e) =>
                          updateFilter(
                            "createdAfter",
                            e.target.value || undefined
                          )
                        }
                      />
                      <Input
                        type="date"
                        placeholder="To"
                        value={filters.createdBefore || ""}
                        onChange={(e) =>
                          updateFilter(
                            "createdBefore",
                            e.target.value || undefined
                          )
                        }
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Last Contact Date
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <Input
                        type="date"
                        placeholder="From"
                        value={filters.lastContactAfter || ""}
                        onChange={(e) =>
                          updateFilter(
                            "lastContactAfter",
                            e.target.value || undefined
                          )
                        }
                      />
                      <Input
                        type="date"
                        placeholder="To"
                        value={filters.lastContactBefore || ""}
                        onChange={(e) =>
                          updateFilter(
                            "lastContactBefore",
                            e.target.value || undefined
                          )
                        }
                      />
                    </div>
                  </div>
                </div>
              </FilterSection>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
