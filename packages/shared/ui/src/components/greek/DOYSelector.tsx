import React, { useState, useEffect, useMemo } from "react";
import { useTranslation } from "../../contexts/TranslationContext";
import { useGreekLocalization } from "../../hooks/useGreekLocalization";

export interface DOYOption {
  id: string;
  code: string;
  name: string;
  address: string;
  city: string;
  region: string;
  postal_code: string;
  phone?: string;
  email?: string;
  is_active: boolean;
}

export interface DOYSelectorProps {
  value?: string;
  onChange: (value: string, doyData: DOYOption | null) => void;
  placeholder?: string;
  error?: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  regionFilter?: string; // Filter by region
  searchPlaceholder?: string;
  showCode?: boolean;
  showAddress?: boolean;
  fullWidth?: boolean;
  className?: string;
}

export const DOYSelector: React.FC<DOYSelectorProps> = ({
  value,
  onChange,
  placeholder,
  error,
  label,
  required = false,
  disabled = false,
  regionFilter,
  searchPlaceholder,
  showCode = true,
  showAddress = false,
  fullWidth = true,
  className = "",
}) => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [doyOptions, setDoyOptions] = useState<DOYOption[]>([]);
  const [selectedDOY, setSelectedDOY] = useState<DOYOption | null>(null);
  const [loading, setLoading] = useState(false);

  // Load DOY options
  useEffect(() => {
    const loadDOYOptions = async () => {
      setLoading(true);
      try {
        // In a real implementation, this would fetch from the API
        // For now, we'll simulate the data structure
        const mockDOYData: DOYOption[] = [
          {
            id: "1",
            code: "A001",
            name: "ΔΟΥ ΑΘΗΝΩΝ",
            address: "Πειραιώς 10",
            city: "Αθήνα",
            region: "Αττική",
            postal_code: "10552",
            phone: "213 1234567",
            email: "a001@aade.gr",
            is_active: true,
          },
          {
            id: "2",
            code: "B002",
            name: "ΔΟΥ ΘΕΣΣΑΛΟΝΙΚΗΣ",
            address: "Τσιμισκή 15",
            city: "Θεσσαλονίκη",
            region: "Κεντρική Μακεδονία",
            postal_code: "54624",
            phone: "2310 123456",
            email: "b002@aade.gr",
            is_active: true,
          },
          {
            id: "3",
            code: "C003",
            name: "ΔΟΥ ΠΑΤΡΩΝ",
            address: "Κολοκοτρώνη 25",
            city: "Πάτρα",
            region: "Δυτική Ελλάδα",
            postal_code: "26221",
            phone: "2610 123456",
            email: "c003@aade.gr",
            is_active: true,
          },
        ];

        let filteredData = mockDOYData;

        if (regionFilter) {
          filteredData = mockDOYData.filter((doy) =>
            doy.region.toLowerCase().includes(regionFilter.toLowerCase())
          );
        }

        setDoyOptions(filteredData);
      } catch (error) {
        console.error("Error loading DOY data:", error);
      } finally {
        setLoading(false);
      }
    };

    loadDOYOptions();
  }, [regionFilter]);

  // Filter options based on search term
  const filteredOptions = useMemo(() => {
    if (!searchTerm) return doyOptions;

    const term = searchTerm.toLowerCase();
    return doyOptions.filter(
      (doy) =>
        doy.name.toLowerCase().includes(term) ||
        doy.code.toLowerCase().includes(term) ||
        doy.city.toLowerCase().includes(term) ||
        doy.address.toLowerCase().includes(term)
    );
  }, [doyOptions, searchTerm]);

  // Find selected DOY by value
  useEffect(() => {
    if (value) {
      const selected = doyOptions.find(
        (doy) => doy.id === value || doy.code === value
      );
      setSelectedDOY(selected || null);
    } else {
      setSelectedDOY(null);
    }
  }, [value, doyOptions]);

  const handleSelect = (doy: DOYOption) => {
    setSelectedDOY(doy);
    onChange(doy.id, doy);
    setIsOpen(false);
    setSearchTerm("");
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    if (!isOpen) setIsOpen(true);
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleInputBlur = () => {
    // Delay closing to allow for option selection
    setTimeout(() => setIsOpen(false), 200);
  };

  const getDisplayValue = () => {
    if (!selectedDOY) return "";

    let display = selectedDOY.name;
    if (showCode) {
      display = `${selectedDOY.code} - ${display}`;
    }
    if (showAddress) {
      display += ` (${selectedDOY.city})`;
    }

    return display;
  };

  const getPlaceholder = () => {
    if (placeholder) return placeholder;
    return t("doy_selector_placeholder");
  };

  const getSearchPlaceholder = () => {
    if (searchPlaceholder) return searchPlaceholder;
    return t("doy_search_placeholder");
  };

  return (
    <div className={`relative ${fullWidth ? "w-full" : ""} ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        <input
          type="text"
          value={isOpen ? searchTerm : getDisplayValue()}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onBlur={handleInputBlur}
          placeholder={isOpen ? getSearchPlaceholder() : getPlaceholder()}
          disabled={disabled}
          className={`
            w-full px-3 py-2 border rounded-md transition-colors
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            disabled:opacity-50 disabled:cursor-not-allowed
            ${error ? "border-red-500" : "border-gray-300"}
            ${fullWidth ? "w-full" : ""}
          `}
        />

        {/* Dropdown arrow */}
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
          <svg
            className={`w-4 h-4 text-gray-400 transition-transform ${
              isOpen ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </div>
      </div>

      {/* Dropdown options */}
      {isOpen && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-y-auto">
          {loading ? (
            <div className="px-3 py-2 text-sm text-gray-500">
              {t("loading")}...
            </div>
          ) : filteredOptions.length === 0 ? (
            <div className="px-3 py-2 text-sm text-gray-500">
              {t("no_results_found")}
            </div>
          ) : (
            filteredOptions.map((doy) => (
              <div
                key={doy.id}
                onClick={() => handleSelect(doy)}
                className={`
                  px-3 py-2 cursor-pointer hover:bg-gray-50 text-sm
                  ${
                    selectedDOY?.id === doy.id ? "bg-blue-50 text-blue-700" : ""
                  }
                `}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="font-medium">
                      {showCode && (
                        <span className="text-gray-500 text-xs mr-2">
                          {doy.code}
                        </span>
                      )}
                      {doy.name}
                    </div>
                    {showAddress && (
                      <div className="text-xs text-gray-500 mt-1">
                        {doy.address}, {doy.city}
                      </div>
                    )}
                  </div>
                  {selectedDOY?.id === doy.id && (
                    <svg
                      className="w-4 h-4 text-blue-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {error && <div className="mt-1 text-sm text-red-600">{error}</div>}
    </div>
  );
};

export default DOYSelector;
