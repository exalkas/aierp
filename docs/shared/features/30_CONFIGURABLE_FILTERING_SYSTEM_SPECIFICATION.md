# Configurable Filtering System Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: Detailed specification for user-configurable filtering system
- **Scope**: Visual filter builder and advanced filtering across all data tables

---

## 1. OVERVIEW

### 1.1 System Purpose

The **Configurable Filtering System** allows users to create, save, and manage complex data filters through a visual interface without technical knowledge. This system applies to all data tables across the 97 screens in the ERP/CRM system.

### 1.2 Key Features

- **Visual Filter Builder**: Drag-and-drop filter construction
- **Advanced Filter Logic**: AND/OR conditions with grouping
- **Filter Presets**: Save and share commonly used filters
- **Dynamic Field Detection**: Automatically detect filterable fields
- **Multi-language Support**: Filter labels and values in user's language
- **Performance Optimization**: Efficient query generation and caching

---

## 2. FILTER BUILDER COMPONENTS

### 2.1 FilterBuilder Component

**Purpose**: Main visual interface for building complex filters

```typescript
interface FilterBuilder {
  // Core Properties
  entityType: string; // "customers", "invoices", "products", etc.
  availableFields: FilterableField[];
  currentFilter: FilterGroup;
  
  // UI Configuration
  showPresets: boolean;
  showSaveOption: boolean;
  showAdvancedMode: boolean;
  maxNestingLevel: number;
  
  // Callbacks
  onFilterChange: (filter: FilterGroup) => void;
  onFilterApply: (filter: FilterGroup) => void;
  onPresetSave: (name: string, filter: FilterGroup) => void;
  onPresetLoad: (preset: FilterPreset) => void;
}

interface FilterableField {
  key: string; // "customerName", "invoiceDate", "totalAmount"
  label: string; // Translated field label
  type: FieldType; // "text", "number", "date", "boolean", "select", "multiselect"
  
  // Field-specific options
  operators: FilterOperator[]; // Available operators for this field
  suggestions?: string[]; // Auto-complete suggestions
  selectOptions?: SelectOption[]; // For dropdown fields
  
  // Display options
  category?: string; // Group related fields
  icon?: string;
  helpText?: string;
  
  // Greek-specific
  greekValidation?: GreekFieldValidation;
  businessTerms?: GreekBusinessTerm[];
}

interface FilterGroup {
  logic: "AND" | "OR";
  conditions: (FilterCondition | FilterGroup)[];
}

interface FilterCondition {
  field: string;
  operator: FilterOperator;
  value: any;
  displayLabel?: string; // For UI display
}

type FilterOperator = 
  | "equals" | "not_equals"
  | "contains" | "not_contains" | "starts_with" | "ends_with"
  | "greater_than" | "less_than" | "greater_equal" | "less_equal"
  | "between" | "not_between"
  | "in" | "not_in"
  | "is_null" | "is_not_null"
  | "is_empty" | "is_not_empty"
  | "today" | "yesterday" | "this_week" | "last_week" | "this_month" | "last_month"
  | "regex" | "greek_afm" | "greek_phone" | "greek_postal_code";
```

### 2.2 FilterPanel Component

**Purpose**: Sidebar panel with quick filters and advanced options

```typescript
interface FilterPanel {
  // Quick Filters
  quickFilters: QuickFilter[];
  
  // Advanced Filters
  showAdvancedBuilder: boolean;
  currentFilter: FilterGroup;
  
  // Saved Filters
  savedFilters: FilterPreset[];
  
  // Filter State
  activeFilters: ActiveFilter[];
  filterCount: number;
  
  // Actions
  onQuickFilterApply: (filter: QuickFilter) => void;
  onAdvancedFilterApply: (filter: FilterGroup) => void;
  onFilterClear: () => void;
  onFilterReset: () => void;
}

interface QuickFilter {
  id: string;
  label: string;
  icon?: string;
  badge?: number; // Count of items matching this filter
  filter: FilterCondition;
  category?: string;
}

interface FilterPreset {
  id: string;
  name: string;
  description?: string;
  filter: FilterGroup;
  isPublic: boolean;
  createdBy: string;
  createdAt: Date;
  usageCount: number;
  tags: string[];
}
```

### 2.3 FilterTags Component

**Purpose**: Display active filters as removable tags

```typescript
interface FilterTags {
  activeFilters: ActiveFilter[];
  showClearAll: boolean;
  maxDisplayed: number;
  
  onFilterRemove: (filterId: string) => void;
  onClearAll: () => void;
  onEditFilter: (filterId: string) => void;
}

interface ActiveFilter {
  id: string;
  fieldLabel: string;
  operatorLabel: string;
  valueLabel: string;
  displayText: string; // "Customer Name contains 'ACME'"
  isQuickFilter: boolean;
}
```

---

## 3. IMPLEMENTATION EXAMPLES

### 3.1 Customer Filter Examples

**Quick Filters:**

```typescript
const customerQuickFilters: QuickFilter[] = [
  {
    id: "active_customers",
    label: "Active Customers",
    icon: "users",
    badge: 245,
    filter: { field: "status", operator: "equals", value: "active" }
  },
  {
    id: "vip_customers", 
    label: "VIP Customers",
    icon: "star",
    badge: 12,
    filter: { field: "customerType", operator: "equals", value: "vip" }
  },
  {
    id: "greek_customers",
    label: "Greek Customers", 
    icon: "flag-gr",
    badge: 180,
    filter: { field: "country", operator: "equals", value: "GR" }
  },
  {
    id: "recent_customers",
    label: "Added This Month",
    icon: "calendar",
    badge: 23,
    filter: { field: "createdAt", operator: "this_month", value: null }
  }
];
```

**Advanced Filter Example:**

```typescript
const advancedCustomerFilter: FilterGroup = {
  logic: "AND",
  conditions: [
    {
      logic: "OR",
      conditions: [
        { field: "country", operator: "equals", value: "GR" },
        { field: "country", operator: "equals", value: "CY" }
      ]
    },
    { field: "totalOrders", operator: "greater_than", value: 10 },
    { field: "lastOrderDate", operator: "greater_than", value: "2024-01-01" }
  ]
};
```

### 3.2 Invoice Filter Examples

**Quick Filters:**

```typescript
const invoiceQuickFilters: QuickFilter[] = [
  {
    id: "unpaid_invoices",
    label: "Unpaid Invoices",
    icon: "alert-circle",
    badge: 45,
    filter: { field: "paymentStatus", operator: "equals", value: "unpaid" }
  },
  {
    id: "overdue_invoices",
    label: "Overdue",
    icon: "clock",
    badge: 12,
    filter: { field: "dueDate", operator: "less_than", value: "today" }
  },
  {
    id: "aade_pending",
    label: "AADE Pending",
    icon: "upload",
    badge: 8,
    filter: { field: "aadeStatus", operator: "equals", value: "pending" }
  },
  {
    id: "this_month_invoices",
    label: "This Month",
    icon: "calendar",
    badge: 156,
    filter: { field: "invoiceDate", operator: "this_month", value: null }
  }
];
```

**Advanced Filter with Greek-Specific Fields:**

```typescript
const greekInvoiceFilter: FilterGroup = {
  logic: "AND",
  conditions: [
    { field: "customerAFM", operator: "greek_afm", value: "9" },
    { field: "vatAmount", operator: "greater_than", value: 100 },
    {
      logic: "OR", 
      conditions: [
        { field: "aadeStatus", operator: "equals", value: "submitted" },
        { field: "aadeStatus", operator: "equals", value: "accepted" }
      ]
    }
  ]
};
```

---

## 4. USER INTERFACE DESIGN

### 4.1 Filter Builder UI

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│ Filter Builder                                    [Save] [×] │
├─────────────────────────────────────────────────────────────┤
│ Quick Filters: [Active] [VIP] [Greek] [This Month] [+More]  │
├─────────────────────────────────────────────────────────────┤
│ Advanced Filters:                                           │
│                                                             │
│ ┌─ AND ────────────────────────────────────────────────────┐ │
│ │ Customer Name [contains    ▼] [ACME Corp        ] [×]    │ │
│ │ Country       [equals      ▼] [Greece     ▼    ] [×]    │ │
│ │ ┌─ OR ──────────────────────────────────────────────────┐ │ │
│ │ │ Total Orders [greater than ▼] [10            ] [×]   │ │ │
│ │ │ VIP Status   [equals       ▼] [Yes      ▼   ] [×]   │ │ │
│ │ │                                        [+ Add Rule] │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                          [+ Add Group] │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                            [+ Add Rule]    │
├─────────────────────────────────────────────────────────────┤
│ Active Filters: [Customer: contains "ACME"] [Country: GR]  │
│                                            [Clear All]     │
├─────────────────────────────────────────────────────────────┤
│                                    [Reset] [Apply] [Save]  │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Filter Panel Sidebar

**Layout:**

```
┌─ Filters ──────────────────┐
│ 🔍 [Search filters...]    │
├───────────────────────────┤
│ QUICK FILTERS             │
│ ☑ Active Customers    245 │
│ ☐ VIP Customers        12 │
│ ☐ Greek Customers     180 │
│ ☐ Added This Month     23 │
│                           │
│ STATUS                    │
│ ☐ Pending              15 │
│ ☐ Approved            230 │
│ ☐ Suspended             8 │
│                           │
│ GREEK SPECIFIC            │
│ ☐ Valid AFM           195 │
│ ☐ Athens Region       156 │
│ ☐ AADE Compliant      180 │
│                           │
│ [Advanced Builder...]     │
│ [Saved Filters...]        │
│ [Clear All Filters]       │
└───────────────────────────┘
```

---

## 5. TECHNICAL IMPLEMENTATION

### 5.1 API Endpoints

```typescript
// Filter Management
"GET /api/filters/:entityType/fields" - Get filterable fields for entity
"GET /api/filters/:entityType/quick" - Get quick filters for entity
"POST /api/filters/apply" - Apply filter and return results
"POST /api/filters/validate" - Validate filter before applying

// Filter Presets
"GET /api/filters/presets" - Get user's saved filter presets
"POST /api/filters/presets" - Save new filter preset
"PUT /api/filters/presets/:id" - Update filter preset
"DELETE /api/filters/presets/:id" - Delete filter preset
"POST /api/filters/presets/:id/share" - Share filter preset

// Filter Suggestions
"GET /api/filters/:entityType/:field/suggestions" - Get field value suggestions
"POST /api/filters/auto-complete" - Auto-complete filter values
```

### 5.2 Custom Hooks

```typescript
// Filter Management Hooks
const useFilter = (entityType: string) => {
  const [currentFilter, setCurrentFilter] = useState<FilterGroup>();
  const [activeFilters, setActiveFilters] = useState<ActiveFilter[]>([]);
  
  const applyFilter = (filter: FilterGroup) => {
    // Apply filter and update results
  };
  
  const addQuickFilter = (quickFilter: QuickFilter) => {
    // Add quick filter to current filter
  };
  
  const removeFilter = (filterId: string) => {
    // Remove specific filter
  };
  
  const clearAllFilters = () => {
    // Clear all active filters
  };
  
  return {
    currentFilter,
    activeFilters,
    applyFilter,
    addQuickFilter,
    removeFilter,
    clearAllFilters
  };
};

const useFilterBuilder = () => {
  const [builderOpen, setBuilderOpen] = useState(false);
  const [currentFilter, setCurrentFilter] = useState<FilterGroup>();
  
  const openBuilder = (initialFilter?: FilterGroup) => {
    setCurrentFilter(initialFilter);
    setBuilderOpen(true);
  };
  
  const closeBuilder = () => {
    setBuilderOpen(false);
  };
  
  const applyFilter = (filter: FilterGroup) => {
    // Apply the built filter
    closeBuilder();
  };
  
  return {
    builderOpen,
    currentFilter,
    openBuilder,
    closeBuilder,
    applyFilter
  };
};

const useSavedFilters = (entityType: string) => {
  const [savedFilters, setSavedFilters] = useState<FilterPreset[]>([]);
  
  const saveFilter = async (name: string, filter: FilterGroup) => {
    // Save filter preset
  };
  
  const loadFilter = (preset: FilterPreset) => {
    // Load saved filter
  };
  
  const deleteFilter = async (presetId: string) => {
    // Delete filter preset
  };
  
  return {
    savedFilters,
    saveFilter,
    loadFilter,
    deleteFilter
  };
};
```

### 5.3 Greek-Specific Filter Operators

```typescript
const greekFilterOperators = {
  greek_afm: {
    label: "Valid Greek AFM",
    validate: (value: string) => validateGreekAFM(value),
    query: (field: string, value: string) => `${field} = '${value}' AND isValidAFM(${field})`
  },
  
  greek_phone: {
    label: "Valid Greek Phone",
    validate: (value: string) => validateGreekPhone(value),
    query: (field: string, value: string) => `${field} LIKE '+30%' AND LENGTH(${field}) = 13`
  },
  
  greek_postal_code: {
    label: "Greek Postal Code",
    validate: (value: string) => /^\d{5}$/.test(value),
    query: (field: string, value: string) => `${field} ~ '^[0-9]{5}$'`
  },
  
  aade_status: {
    label: "AADE Status",
    options: ["pending", "submitted", "accepted", "rejected"],
    query: (field: string, value: string) => `aadeSubmission.status = '${value}'`
  }
};
```

---

## 6. PERFORMANCE OPTIMIZATION

### 6.1 Query Optimization

**Indexed Filtering:**

- Create database indexes for commonly filtered fields
- Optimize complex filter queries with proper JOIN strategies
- Cache filter results for repeated queries

**Client-Side Optimization:**

- Debounce filter input changes
- Virtualize large result sets
- Implement progressive loading for filter suggestions

### 6.2 Caching Strategy

```typescript
// Cache filter results
const useFilterCache = () => {
  const cache = new Map<string, FilterResult>();
  
  const getCachedResult = (filterHash: string) => {
    return cache.get(filterHash);
  };
  
  const setCachedResult = (filterHash: string, result: FilterResult) => {
    cache.set(filterHash, result);
  };
  
  return { getCachedResult, setCachedResult };
};
```

---

## 7. MULTILINGUAL SUPPORT

### 7.1 Filter Translations

```typescript
// Translation keys for filter components
const filterTranslations = {
  "filter.builder.title": "Filter Builder",
  "filter.quick.active": "Active",
  "filter.quick.recent": "Recent",
  "filter.operator.equals": "equals",
  "filter.operator.contains": "contains",
  "filter.operator.greater_than": "greater than",
  "filter.field.customerName": "Customer Name",
  "filter.field.invoiceDate": "Invoice Date",
  "filter.field.totalAmount": "Total Amount",
  "filter.preset.save": "Save Filter",
  "filter.preset.load": "Load Filter",
  "filter.clear.all": "Clear All Filters"
};

// Greek translations
const greekFilterTranslations = {
  "filter.builder.title": "Δημιουργός Φίλτρων",
  "filter.quick.active": "Ενεργοί",
  "filter.quick.recent": "Πρόσφατοι",
  "filter.operator.equals": "ισούται με",
  "filter.operator.contains": "περιέχει",
  "filter.operator.greater_than": "μεγαλύτερο από",
  "filter.field.customerName": "Όνομα Πελάτη",
  "filter.field.invoiceDate": "Ημερομηνία Τιμολογίου",
  "filter.field.totalAmount": "Συνολικό Ποσό"
};
```

---

## 8. USER EXPERIENCE FLOWS

### 8.1 Quick Filter Flow

1. User opens customer list
2. Sees quick filter buttons with badges (counts)
3. Clicks "Greek Customers" quick filter
4. Results instantly filter to Greek customers
5. Filter tag appears showing "Country: Greece"
6. User can remove filter by clicking tag's × button

### 8.2 Advanced Filter Flow

1. User clicks "Advanced Filters" button
2. Filter builder modal opens
3. User drags "Customer Name" field to builder
4. Selects "contains" operator
5. Types "ACME" in value field
6. Adds another condition with "AND" logic
7. Previews results count (15 matches)
8. Clicks "Apply" to see filtered results
9. Optionally saves filter as "ACME Customers" preset

### 8.3 Saved Filter Flow

1. User creates complex filter for monthly reports
2. Clicks "Save Filter" and names it "Monthly Revenue Report"
3. Filter appears in "Saved Filters" dropdown
4. Next month, user selects saved filter from dropdown
5. Filter instantly applies with updated date ranges
6. User can share filter with team members

---

## 9. CONCLUSION

This configurable filtering system provides:

**✅ User-Friendly Interface:**

- Visual drag-and-drop filter builder
- Quick filter buttons for common scenarios
- Clear display of active filters

**✅ Advanced Functionality:**

- Complex logic with AND/OR grouping
- Custom operators for Greek-specific validation
- Saved filter presets for reusability

**✅ Performance Optimized:**

- Efficient query generation
- Client-side caching
- Progressive loading for large datasets

**✅ Greek Market Specialized:**

- AFM, phone, postal code validation operators
- AADE status filtering
- Greek business terminology

**✅ Multilingual Support:**

- Filter labels and operators in user's language
- Localized field names and values
- Cultural adaptation for business concepts

This system transforms data filtering from a technical task into an intuitive, powerful tool that Greek businesses can use to gain insights from their ERP/CRM data while maintaining the flexibility to expand internationally.
