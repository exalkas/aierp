# List & Filter Configuration UX Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: UX specification for list configuration and filter placement
- **Scope**: All data tables across 97 screens

---

## 1. CONFIGURATION PLACEMENT STRATEGY

### 1.1 Two-Tier Configuration Approach

**Quick Access (Always Visible):**

- List controls in table header
- Quick filters in sidebar/toolbar
- Common actions always accessible

**Advanced Configuration (On-Demand):**

- Advanced list settings in drawer/modal
- Complex filter builder in modal
- Saved presets and sharing options

### 1.2 Screen Layout Structure

```
┌─ Application Header ──────────────────────────────────────────┐
│ [Logo] [Navigation] [Search] [Language] [User] [Notifications]│
└───────────────────────────────────────────────────────────────┘
┌─ Page Content ────────────────────────────────────────────────┐
│ ┌─ Page Header ───────────────────────────────────────────────┐ │
│ │ [Breadcrumb] → Customers                          [+ New]  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─ Data Management Toolbar ──────────────────────────────────┐ │
│ │ [🔍 Search] [Filter ▼] [Sort ▼] [Columns ▼] [Export ▼]    │ │
│ │ Active: [Country: GR ×] [Status: Active ×] [Clear All]    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─ Filter Sidebar ─┐ ┌─ Data Table ─────────────────────────┐ │
│ │ QUICK FILTERS     │ │ ☐ [Name ↕] [Country ↕] [Status ↕]  │ │
│ │ ☑ Active (245)    │ │ ☐ ACME Corp   Greece    Active     │ │
│ │ ☐ VIP (12)        │ │ ☐ Beta Ltd    Cyprus    Pending    │ │
│ │ ☐ Greek (180)     │ │ ☐ Gamma SA    Greece    Active     │ │
│ │                   │ │ ... (showing 1-25 of 245)         │ │
│ │ [Advanced...]     │ │ [← Previous] [1] [2] [3] [Next →]  │ │
│ │ [Saved Filters]   │ │                                    │ │
│ └───────────────────┘ └─────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

---

## 2. LIST CONFIGURATION PLACEMENT

### 2.1 Primary Controls (Always Visible)

**Location: Data Management Toolbar**

```
┌─ Data Management Toolbar ──────────────────────────────────────┐
│ [🔍 Search...] [Filter ▼] [Sort ▼]    [Columns ▼] [View ▼] [↓] │
│ Active: [Country: Greece ×] [Status: Active ×] [Clear All]    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Column Configuration Dropdown

**Triggered by: [Columns ▼] button**

```
[Columns ▼] → Dropdown Menu:
┌─ Show/Hide Columns ───────────────┐
│ ☑ Customer Name                   │
│ ☑ Country                         │
│ ☑ Status                          │
│ ☑ Total Orders                    │
│ ☐ Phone Number                    │
│ ☐ Last Contact                    │
│ ☐ Created Date                    │
│ ☐ AFM (Greek Tax Number)          │
│ ────────────────────────────────  │
│ [Select All] [Select None]        │
│ [Reset to Default]                │
│ ────────────────────────────────  │
│ [Advanced Column Settings...]     │
└───────────────────────────────────┘
```

### 2.3 Quick Sorting Controls

**Location: Column Headers**

```
Table Headers with Sorting:
┌─────────────────────────────────────────────────────────────┐
│ ☐ [Customer Name ↕] [Country ↕] [Status ↕] [Orders ↓] [⚙]  │
│ ─────────────────────────────────────────────────────────── │
│ ☐ ACME Corporation    Greece     Active      15       Edit  │
│ ☐ Beta Enterprises    Cyprus     Pending      8       Edit  │
└─────────────────────────────────────────────────────────────┘
```

**Column Header Interaction:**

- **Single Click**: Sort ascending
- **Double Click**: Sort descending
- **Triple Click**: Remove sort
- **Right Click**: Column options menu

---

## 3. FILTER CONFIGURATION PLACEMENT

### 3.1 Filter Sidebar (Default State)

**Location: Left sidebar, collapsible**

```
┌─ Filters ──────────────────┐
│ [🔍 Search filters...]    │
│ ───────────────────────── │
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
│ COUNTRY                   │
│ ☐ Greece              180 │
│ ☐ Cyprus               45 │
│ ☐ Germany              20 │
│                           │
│ GREEK SPECIFIC            │
│ ☐ Valid AFM           195 │
│ ☐ Athens Region       156 │
│ ☐ AADE Compliant      180 │
│                           │
│ [Advanced Builder...]     │
│ [Saved Filters...]        │
│ [Clear All Filters]       │
│ ───────────────────────── │
│ [◀ Collapse Sidebar]      │
└───────────────────────────┘
```

### 3.2 Advanced Filter Builder Modal

**Triggered by: "Advanced Filter Builder..." button**

```
┌─ Advanced Filter Builder ────────────────────────────────────┐
│ Building filter for: Customers                    [Save] [×] │
│ ─────────────────────────────────────────────────────────── │
│ Quick Filters: [Active] [VIP] [Greek] [This Month] [+More]  │
│ ─────────────────────────────────────────────────────────── │
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
│ ─────────────────────────────────────────────────────────── │
│ Preview: 15 customers match this filter                    │
│ Active: [Customer: contains "ACME"] [Country: Greece]      │
│ ─────────────────────────────────────────────────────────── │
│ Save as: [Monthly Report Filter ____________] [Public ☐]   │
│                              [Reset] [Apply] [Save & Apply]│
└─────────────────────────────────────────────────────────────┘
```

---

## 4. CONFIGURATION ACCESS POINTS

### 4.1 User Access Methods

**1. Primary Access (Most Common):**

- **Columns**: Toolbar → [Columns ▼] → Quick selection
- **Filters**: Sidebar quick filters + search
- **Sorting**: Column header clicks

**2. Advanced Access (Power Users):**

- **Columns**: Toolbar → [Columns ▼] → "Advanced Settings..."
- **Filters**: Sidebar → "Advanced Builder..."
- **Presets**: Sidebar → "Saved Filters..." / Column → "Saved Layouts"

**3. Settings Access (Preferences):**

- **User Menu** → "Table & Filter Preferences"
- **Per-screen settings** via [⚙] gear icon in table header

### 4.2 Configuration Persistence

**Where configurations are saved:**

```typescript
interface UserConfiguration {
  // Per-entity defaults
  defaultLayouts: Record<string, string>; // customers → "detailed_view"
  defaultFilters: Record<string, string>; // invoices → "this_month"

  // UI preferences
  sidebarCollapsed: boolean;
  filterPanelPosition: "left" | "right";
  tableRowHeight: "compact" | "comfortable" | "spacious";

  // Recent usage
  recentLayouts: string[];
  recentFilters: string[];
}
```

**Settings Access Location:**

- **User Menu** → "Display Preferences"
- **Quick access** via [⚙] gear icon in any table header

---

## 5. MOBILE & RESPONSIVE BEHAVIOR

### 5.1 Mobile Layout Adaptation

**Mobile Filter Interface:**

```
Mobile Filter Drawer:
┌─ Filters ─────────────────────┐
│ [× Close]           [Apply]   │
│ ───────────────────────────── │
│ 🔍 [Search filters...]       │
│ ───────────────────────────── │
│ QUICK FILTERS                 │
│ [Active 245] [VIP 12]         │
│ [Greek 180] [Recent 23]       │
│                               │
│ STATUS                        │
│ ○ All ● Active ○ Pending      │
│                               │
│ COUNTRY                       │
│ ☐ Greece (180)                │
│ ☐ Cyprus (45)                 │
│ ☐ Germany (20)                │
│                               │
│ [Advanced Builder]            │
│ [Saved Filters]               │
│ [Clear All]                   │
│ ───────────────────────────── │
│ [Cancel]            [Apply]   │
└───────────────────────────────┘
```

---

## 6. IMPLEMENTATION SUMMARY

### 6.1 Configuration Access Points

**Quick Access (Always Visible):**

- **Column configuration**: Data toolbar → [Columns ▼]
- **Filter configuration**: Left sidebar (collapsible)
- **Sorting**: Column header clicks

**Advanced Configuration:**

- **Advanced columns**: Modal via "Advanced Settings..."
- **Complex filters**: Modal via "Advanced Builder..."
- **Saved presets**: Dedicated preset managers

**Settings & Preferences:**

- **Default layouts**: User Menu → "Display Preferences"
- **UI preferences**: User settings with per-entity defaults
- **Quick settings**: [⚙] gear icon in table headers

This approach provides **intuitive progressive disclosure** where common tasks are immediately accessible, while advanced features are available on-demand without cluttering the interface.
