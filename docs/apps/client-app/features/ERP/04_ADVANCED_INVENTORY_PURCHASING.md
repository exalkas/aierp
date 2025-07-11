# 04. Advanced Inventory & Purchasing Module - Technical Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Module**: Advanced Inventory & Purchasing (€49/month)
- **Dependencies**: Product Catalog & Inventory, Financial Management
- **Target Users**: Multi-location businesses, Manufacturers, Distributors, Wholesalers

## Overview

The Advanced Inventory & Purchasing Module extends basic inventory with sophisticated features including multi-location management, automated purchasing workflows, advanced supplier management, demand forecasting, and comprehensive purchasing analytics. This module is designed for complex businesses that need automated procurement and advanced inventory optimization.

---

## 🖥️ Screens & User Interface

### 1. Advanced Inventory Dashboard (`/erp/inventory/advanced-dashboard`)

**Purpose**: Comprehensive overview with multi-location insights and predictive analytics

```typescript
const AdvancedInventoryDashboard: React.FC = () => {
  const { multiLocationSummary, predictions, loading } =
    useAdvancedInventoryData();

  return (
    <DashboardLayout>
      <DashboardHeader title="Advanced Inventory Management" />

      <MetricsGrid>
        <MetricCard
          title="Total Inventory Value"
          value={formatEuro(multiLocationSummary.totalValue)}
          breakdown="Across all locations"
          trend="up"
          change="+3.2%"
        />
        <MetricCard
          title="Predicted Stockouts"
          value={predictions.stockoutCount}
          subtitle="Next 30 days"
          status="warning"
          actionButton={<ViewPredictionsButton />}
        />
        <MetricCard
          title="Purchase Orders"
          value={multiLocationSummary.activePOs}
          subtitle="Active orders"
          status="info"
        />
        <MetricCard
          title="Automation Rate"
          value={`${multiLocationSummary.automationRate}%`}
          subtitle="Auto-generated orders"
          status="success"
        />
      </MetricsGrid>

      <Row>
        <Col md={8}>
          <InventoryForecastChart
            data={predictions.demandForecast}
            showConfidenceInterval
          />
        </Col>
        <Col md={4}>
          <LocationInventoryWidget />
          <AutomationStatusWidget />
        </Col>
      </Row>

      <MultiLocationInventoryGrid />
      <PurchaseOrdersWidget />
    </DashboardLayout>
  );
};
```

### 2. Multi-Location Inventory (`/erp/inventory/locations`)

**Purpose**: Manage inventory across multiple locations with transfer capabilities

```typescript
const MultiLocationInventory: React.FC = () => {
  const { locations, inventoryByLocation, loading } =
    useMultiLocationInventory();
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(
    null
  );

  return (
    <PageLayout>
      <PageHeader
        title="Multi-Location Inventory"
        actions={
          <LocationActions>
            <CreateLocationButton />
            <InventoryTransferButton />
            <LocationReportsButton />
          </LocationActions>
        }
      />

      <LocationSelector
        locations={locations}
        selectedLocation={selectedLocation}
        onChange={setSelectedLocation}
        showAll
      />

      <LocationInventoryTabs>
        <TabPanel label="Stock Levels">
          <LocationStockGrid
            location={selectedLocation}
            inventory={inventoryByLocation}
            allowTransfers
            showReorderLevels
          />
        </TabPanel>

        <TabPanel label="Transfers">
          <InventoryTransfers
            location={selectedLocation}
            showPending
            allowCreate
          />
        </TabPanel>

        <TabPanel label="Analytics">
          <LocationAnalytics location={selectedLocation} showComparisons />
        </TabPanel>
      </LocationInventoryTabs>
    </PageLayout>
  );
};
```

### 3. Purchase Orders (`/erp/purchasing/orders`)

**Purpose**: Comprehensive purchase order management with automation

```typescript
const PurchaseOrders: React.FC = () => {
  const { orders, loading, filters, updateFilter } = usePurchaseOrders();

  return (
    <PageLayout>
      <PageHeader
        title="Purchase Orders"
        actions={
          <PurchaseOrderActions>
            <CreatePOButton />
            <AutoGeneratePOButton />
            <BulkActionsButton />
          </PurchaseOrderActions>
        }
      />

      <FilterBar>
        <StatusFilter
          value={filters.status}
          onChange={(status) => updateFilter("status", status)}
          options={[
            "draft",
            "sent",
            "confirmed",
            "partial",
            "completed",
            "cancelled",
          ]}
        />
        <SupplierFilter
          value={filters.supplierId}
          onChange={(id) => updateFilter("supplierId", id)}
        />
        <LocationFilter
          value={filters.locationId}
          onChange={(id) => updateFilter("locationId", id)}
        />
        <DateRangeFilter
          value={filters.dateRange}
          onChange={(range) => updateFilter("dateRange", range)}
        />
        <AutoGeneratedFilter
          value={filters.autoGenerated}
          onChange={(auto) => updateFilter("autoGenerated", auto)}
        />
      </FilterBar>

      <PurchaseOrderGrid
        orders={orders}
        loading={loading}
        columns={[
          "poNumber",
          "supplier",
          "orderDate",
          "expectedDelivery",
          "totalAmount",
          "status",
          "location",
          "automation",
          "actions",
        ]}
        allowBulkActions
        showAutomationIndicators
      />
    </PageLayout>
  );
};
```

### 4. Supplier Management (`/erp/purchasing/suppliers`)

**Purpose**: Advanced supplier relationship management with performance analytics

```typescript
const AdvancedSupplierManagement: React.FC = () => {
  const { suppliers, performance, loading } = useAdvancedSuppliers();

  return (
    <PageLayout>
      <PageHeader
        title="Supplier Management"
        actions={
          <SupplierActions>
            <CreateSupplierButton />
            <SupplierAnalyticsButton />
            <PerformanceReportButton />
          </SupplierActions>
        }
      />

      <SupplierPerformanceOverview
        metrics={performance.overall}
        topPerformers={performance.topPerformers}
        issues={performance.issues}
      />

      <SupplierTabs>
        <TabPanel label="All Suppliers">
          <SupplierGrid
            suppliers={suppliers}
            showPerformanceMetrics
            allowBulkActions
          />
        </TabPanel>

        <TabPanel label="Performance Analytics">
          <SupplierPerformanceAnalytics
            suppliers={suppliers}
            showTrends
            allowComparisons
          />
        </TabPanel>

        <TabPanel label="Contracts & Terms">
          <SupplierContracts
            suppliers={suppliers}
            showExpirations
            allowRenewals
          />
        </TabPanel>

        <TabPanel label="Quality Management">
          <SupplierQualityTracking
            suppliers={suppliers}
            showIssues
            allowRatings
          />
        </TabPanel>
      </SupplierTabs>
    </PageLayout>
  );
};
```

### 5. Purchasing Automation (`/erp/purchasing/automation`)

**Purpose**: Configure and manage automated purchasing workflows

```typescript
const PurchasingAutomation: React.FC = () => {
  const { rules, automationStats, loading } = usePurchasingAutomation();

  return (
    <PageLayout>
      <PageHeader
        title="Purchasing Automation"
        subtitle="Configure automatic purchase order generation"
        actions={<CreateAutomationRuleButton />}
      />

      <AutomationOverview>
        <AutomationStatsCard stats={automationStats} showEfficiency />
        <RecentAutomationActivity
          activities={automationStats.recentActivities}
          limit={10}
        />
      </AutomationOverview>

      <AutomationRulesTabs>
        <TabPanel label="Reorder Rules">
          <ReorderRules rules={rules.reorderRules} allowEdit showPerformance />
        </TabPanel>

        <TabPanel label="Supplier Selection">
          <SupplierSelectionRules
            rules={rules.supplierRules}
            showDecisionTree
          />
        </TabPanel>

        <TabPanel label="Approval Workflows">
          <ApprovalWorkflows
            workflows={rules.approvalWorkflows}
            showProcesses
          />
        </TabPanel>

        <TabPanel label="Smart Forecasting">
          <DemandForecastingConfig
            settings={rules.forecastingSettings}
            showAccuracy
          />
        </TabPanel>
      </AutomationRulesTabs>
    </PageLayout>
  );
};
```

### 6. Demand Forecasting (`/erp/inventory/forecasting`)

**Purpose**: AI-powered demand prediction and inventory optimization

```typescript
const DemandForecasting: React.FC = () => {
  const { forecasts, accuracy, recommendations, loading } =
    useDemandForecasting();

  return (
    <PageLayout>
      <PageHeader
        title="Demand Forecasting"
        subtitle="AI-powered inventory optimization"
        actions={<RecalculateForecastsButton />}
      />

      <ForecastingOverview>
        <AccuracyMetrics accuracy={accuracy} showTrends />
        <ForecastingRecommendations
          recommendations={recommendations}
          allowImplement
        />
      </ForecastingOverview>

      <ForecastingTabs>
        <TabPanel label="Product Forecasts">
          <ProductForecastGrid
            forecasts={forecasts.products}
            showConfidenceIntervals
            allowAdjustments
          />
        </TabPanel>

        <TabPanel label="Category Analysis">
          <CategoryForecastAnalysis
            forecasts={forecasts.categories}
            showSeasonality
          />
        </TabPanel>

        <TabPanel label="Model Performance">
          <ForecastingModelPerformance
            models={forecasts.models}
            showComparisons
          />
        </TabPanel>

        <TabPanel label="External Factors">
          <ExternalFactorsAnalysis
            factors={forecasts.externalFactors}
            allowConfiguration
          />
        </TabPanel>
      </ForecastingTabs>
    </PageLayout>
  );
};
```

---

## 🔗 API Endpoints

### Multi-Location APIs

```typescript
// GET /api/erp/inventory/locations
interface GetLocationsResponse {
  locations: Location[];
  inventorySummary: LocationInventorySummary[];
  transfersPending: number;
}

// POST /api/erp/inventory/transfers
interface CreateInventoryTransferRequest {
  fromLocationId: string;
  toLocationId: string;
  items: TransferItem[];
  reason: string;
  expectedDate?: Date;
  priority: TransferPriority;
}

// GET /api/erp/inventory/locations/:id/stock
interface GetLocationStockRequest {
  locationId: string;
  includeReorderLevels?: boolean;
  includeForecasts?: boolean;
}
```

### Purchase Order APIs

```typescript
// GET /api/erp/purchasing/orders
interface GetPurchaseOrdersRequest {
  status?: PurchaseOrderStatus[];
  supplierId?: string;
  locationId?: string;
  autoGenerated?: boolean;
  dateFrom?: Date;
  dateTo?: Date;
}

// POST /api/erp/purchasing/orders
interface CreatePurchaseOrderRequest {
  supplierId: string;
  locationId: string;
  items: PurchaseOrderItem[];
  expectedDeliveryDate?: Date;
  paymentTerms?: string;
  notes?: string;
  autoGenerated?: boolean;
  automationRuleId?: string;
}

// POST /api/erp/purchasing/orders/auto-generate
interface AutoGeneratePurchaseOrdersRequest {
  locationIds?: string[];
  supplierIds?: string[];
  productIds?: string[];
  urgentOnly?: boolean;
}
```

### Automation APIs

```typescript
// GET /api/erp/purchasing/automation/rules
interface GetAutomationRulesResponse {
  reorderRules: ReorderRule[];
  supplierRules: SupplierSelectionRule[];
  approvalWorkflows: ApprovalWorkflow[];
  forecastingSettings: ForecastingSettings;
}

// POST /api/erp/purchasing/automation/rules/reorder
interface CreateReorderRuleRequest {
  productId: string;
  locationId?: string;
  reorderPoint: number;
  reorderQuantity: number;
  preferredSupplierId: string;
  autoApprove: boolean;
  conditions: ReorderCondition[];
}

// POST /api/erp/purchasing/automation/execute
interface ExecuteAutomationRequest {
  ruleType: "reorder" | "forecast" | "supplier_selection";
  productIds?: string[];
  locationIds?: string[];
  urgentOnly?: boolean;
}
```

### Forecasting APIs

```typescript
// GET /api/erp/inventory/forecasting/demand
interface GetDemandForecastRequest {
  productIds?: string[];
  locationIds?: string[];
  forecastPeriod: number; // days
  includeConfidenceInterval?: boolean;
}

// POST /api/erp/inventory/forecasting/calculate
interface CalculateForecastRequest {
  modelType:
    | "moving_average"
    | "exponential_smoothing"
    | "arima"
    | "machine_learning";
  historicalPeriod: number; // days
  seasonalityAdjustment: boolean;
  externalFactors?: ExternalFactor[];
}

// GET /api/erp/inventory/forecasting/accuracy
interface GetForecastAccuracyResponse {
  overallAccuracy: number;
  productAccuracy: ProductForecastAccuracy[];
  modelComparison: ModelAccuracyComparison[];
  recommendations: AccuracyRecommendation[];
}
```

---

## 🗃️ Data Models

### Location Model

```typescript
interface Location {
  id: string;
  code: string;
  name: string;
  type: LocationType;

  // Address and contact
  address: Address;
  contactPerson?: string;
  phone?: string;
  email?: string;

  // Operational details
  isActive: boolean;
  isWarehouse: boolean;
  isRetailLocation: boolean;
  canReceiveTransfers: boolean;
  canSendTransfers: boolean;

  // Capacity and constraints
  maxCapacity?: number;
  storageConstraints: StorageConstraint[];
  operatingHours?: OperatingHours;

  // Greek business details
  greekLocationInfo?: GreekLocationInfo;

  // Current inventory summary
  totalItems: number;
  totalValue: number;
  utilizationRate: number;

  // Audit
  createdAt: Date;
  updatedAt: Date;
}

type LocationType =
  | "warehouse"
  | "store"
  | "distribution_center"
  | "manufacturing";

interface LocationInventory {
  locationId: string;
  productId: string;
  quantity: number;
  reservedQuantity: number;
  availableQuantity: number;
  reorderPoint: number;
  maxStock: number;

  // Location-specific costs
  averageCost: number;
  lastCost: number;

  // Movement tracking
  lastMovementDate?: Date;
  lastCountDate?: Date;

  // Storage details
  storageZone?: string;
  bin?: string;
  position?: string;
}
```

### Purchase Order Model

```typescript
interface PurchaseOrder {
  id: string;
  poNumber: string;

  // Supplier and location
  supplierId: string;
  supplier: Supplier;
  locationId: string;
  location: Location;

  // Order details
  orderDate: Date;
  expectedDeliveryDate?: Date;
  actualDeliveryDate?: Date;

  // Items
  items: PurchaseOrderItem[];

  // Financial
  subtotal: number;
  vatAmount: number;
  total: number;
  currency: string;

  // Terms
  paymentTerms: string;
  deliveryTerms?: string;

  // Status tracking
  status: PurchaseOrderStatus;
  approvalStatus: ApprovalStatus;
  deliveryStatus: DeliveryStatus;

  // Automation
  autoGenerated: boolean;
  automationRuleId?: string;
  generatedReason?: string;

  // Quality and performance
  qualityRating?: number;
  deliveryPerformance?: DeliveryPerformance;

  // Notes and attachments
  notes?: string;
  internalNotes?: string;
  attachments: Attachment[];

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  approvedBy?: string;
  approvedAt?: Date;
}

interface PurchaseOrderItem {
  id: string;
  productId: string;
  product: Product;

  // Quantities
  orderedQuantity: number;
  receivedQuantity: number;
  remainingQuantity: number;

  // Pricing
  unitCost: number;
  totalCost: number;

  // Delivery
  expectedDeliveryDate?: Date;
  actualDeliveryDate?: Date;

  // Quality
  qualityIssues: QualityIssue[];
  accepted: boolean;
  rejectionReason?: string;
}

type PurchaseOrderStatus =
  | "draft"
  | "sent"
  | "confirmed"
  | "partial"
  | "completed"
  | "cancelled";
type ApprovalStatus = "pending" | "approved" | "rejected" | "auto_approved";
type DeliveryStatus = "pending" | "partial" | "delivered" | "overdue";
```

### Automation Rule Models

```typescript
interface ReorderRule {
  id: string;
  name: string;
  isActive: boolean;

  // Trigger conditions
  productId: string;
  locationId?: string;
  reorderPoint: number;
  reorderQuantity: number;

  // Supplier selection
  preferredSupplierId: string;
  alternativeSuppliers: string[];
  supplierSelectionCriteria: SupplierSelectionCriteria;

  // Automation settings
  autoApprove: boolean;
  maxOrderValue?: number;
  requireManagerApproval: boolean;

  // Conditions and constraints
  conditions: ReorderCondition[];
  seasonalAdjustments: SeasonalAdjustment[];

  // Performance tracking
  timesTriggered: number;
  lastTriggered?: Date;
  averageLeadTime: number;
  successRate: number;

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}

interface ReorderCondition {
  type:
    | "stock_level"
    | "forecast_demand"
    | "seasonal"
    | "supplier_availability";
  operator: "less_than" | "greater_than" | "equals" | "between";
  value: number | string;
  additionalValue?: number; // for 'between' operator
}

interface SupplierSelectionCriteria {
  priorityFactors: {
    price: number; // weight 0-100
    leadTime: number; // weight 0-100
    quality: number; // weight 0-100
    reliability: number; // weight 0-100
  };
  maximumLeadTime?: number;
  minimumQualityRating?: number;
  priceTolerancePercent?: number;
}
```

### Demand Forecasting Models

```typescript
interface DemandForecast {
  id: string;
  productId: string;
  locationId?: string;

  // Forecast details
  forecastDate: Date;
  forecastPeriod: number; // days
  modelUsed: ForecastModel;

  // Predictions
  predictions: ForecastPrediction[];
  confidence: number; // 0-100
  accuracy?: number; // Based on historical comparison

  // Input data
  historicalPeriod: number;
  dataPoints: number;
  seasonalityDetected: boolean;
  trendDirection: "up" | "down" | "stable";

  // External factors
  externalFactors: ExternalFactor[];
  adjustments: ForecastAdjustment[];

  // Performance
  mapeError?: number; // Mean Absolute Percentage Error
  rmseError?: number; // Root Mean Square Error

  // Audit
  createdAt: Date;
  lastUpdated: Date;
}

interface ForecastPrediction {
  date: Date;
  predictedDemand: number;
  confidenceLower: number;
  confidenceUpper: number;
  actualDemand?: number; // Filled in after the date passes
}

type ForecastModel =
  | "moving_average"
  | "exponential_smoothing"
  | "arima"
  | "machine_learning"
  | "ensemble";

interface ExternalFactor {
  type: "weather" | "holidays" | "promotions" | "market_events" | "economic";
  name: string;
  impact: "positive" | "negative" | "neutral";
  weight: number; // 0-100
  startDate?: Date;
  endDate?: Date;
}
```

---

## 🧩 UI Components

### Multi-Location Components

```typescript
// Location management
export const LocationSelector: React.FC<LocationSelectorProps>;
export const LocationInventoryGrid: React.FC<LocationInventoryGridProps>;
export const InventoryTransferForm: React.FC<InventoryTransferFormProps>;
export const LocationStockComparison: React.FC<LocationStockComparisonProps>;

// Transfer management
export const TransferRequestForm: React.FC<TransferRequestFormProps>;
export const TransferStatus: React.FC<TransferStatusProps>;
export const TransferHistory: React.FC<TransferHistoryProps>;
export const BulkTransferTool: React.FC<BulkTransferToolProps>;
```

### Purchase Order Components

```typescript
// Purchase order creation and management
export const PurchaseOrderForm: React.FC<PurchaseOrderFormProps>;
export const PurchaseOrderGrid: React.FC<PurchaseOrderGridProps>;
export const POItemEditor: React.FC<POItemEditorProps>;
export const SupplierQuoteComparison: React.FC<SupplierQuoteComparisonProps>;

// Automation indicators
export const AutoGeneratedBadge: React.FC<AutoGeneratedBadgeProps>;
export const AutomationRuleIndicator: React.FC<AutomationRuleIndicatorProps>;
export const ApprovalWorkflowStatus: React.FC<ApprovalWorkflowStatusProps>;
```

### Forecasting Components

```typescript
// Demand forecasting displays
export const DemandForecastChart: React.FC<DemandForecastChartProps>;
export const ForecastAccuracyMeter: React.FC<ForecastAccuracyMeterProps>;
export const SeasonalityIndicator: React.FC<SeasonalityIndicatorProps>;
export const ForecastRecommendations: React.FC<ForecastRecommendationsProps>;

// Model configuration
export const ForecastModelSelector: React.FC<ForecastModelSelectorProps>;
export const ExternalFactorEditor: React.FC<ExternalFactorEditorProps>;
export const ForecastParameterTuner: React.FC<ForecastParameterTunerProps>;
```

### Automation Components

```typescript
// Rule management
export const AutomationRuleBuilder: React.FC<AutomationRuleBuilderProps>;
export const ReorderRuleForm: React.FC<ReorderRuleFormProps>;
export const SupplierSelectionCriteriaEditor: React.FC<SupplierSelectionCriteriaEditorProps>;
export const AutomationPerformanceWidget: React.FC<AutomationPerformanceWidgetProps>;

// Workflow management
export const ApprovalWorkflowDesigner: React.FC<ApprovalWorkflowDesignerProps>;
export const WorkflowStepEditor: React.FC<WorkflowStepEditorProps>;
export const ApprovalHistory: React.FC<ApprovalHistoryProps>;
```

---

## 🪝 Custom Hooks

### Multi-Location Hooks

```typescript
export const useMultiLocationInventory = () => {
  const [locations, setLocations] = useState<Location[]>([]);
  const [inventoryByLocation, setInventoryByLocation] =
    useState<LocationInventoryMap>({});

  const transferInventory = useCallback(
    async (transfer: InventoryTransferRequest) => {
      try {
        const result = await inventoryAPI.createTransfer(transfer);

        // Update local state optimistically
        updateLocationInventory(
          transfer.fromLocationId,
          transfer.items,
          "subtract"
        );
        updateLocationInventory(transfer.toLocationId, transfer.items, "add");

        return result;
      } catch (error) {
        // Revert optimistic update
        updateLocationInventory(transfer.fromLocationId, transfer.items, "add");
        updateLocationInventory(
          transfer.toLocationId,
          transfer.items,
          "subtract"
        );
        throw new TransferError(error.message);
      }
    },
    []
  );

  const getProductAvailability = useCallback(
    (productId: string) => {
      const availability: ProductLocationAvailability = {};

      Object.entries(inventoryByLocation).forEach(([locationId, inventory]) => {
        const productInventory = inventory.find(
          (item) => item.productId === productId
        );
        if (productInventory) {
          availability[locationId] = {
            quantity: productInventory.quantity,
            available: productInventory.availableQuantity,
            reserved: productInventory.reservedQuantity,
          };
        }
      });

      return availability;
    },
    [inventoryByLocation]
  );

  return {
    locations,
    inventoryByLocation,
    loading,
    transferInventory,
    getProductAvailability,
    optimizeInventoryDistribution,
  };
};

export const useInventoryTransfers = (locationId?: string) => {
  return {
    transfers,
    pendingTransfers,
    loading,
    createTransfer,
    approveTransfer,
    completeTransfer,
  };
};
```

### Purchase Order Hooks

```typescript
export const usePurchaseOrders = (filters?: POFilters) => {
  const [orders, setOrders] = useState<PurchaseOrder[]>([]);

  const createPurchaseOrder = useCallback(
    async (orderData: CreatePurchaseOrderRequest) => {
      try {
        const newOrder = await purchaseAPI.create(orderData);
        setOrders((prev) => [newOrder, ...prev]);

        // If auto-generated, track automation performance
        if (orderData.autoGenerated && orderData.automationRuleId) {
          trackAutomationSuccess(orderData.automationRuleId);
        }

        return newOrder;
      } catch (error) {
        throw new PurchaseOrderError(error.message);
      }
    },
    []
  );

  const autoGenerateOrders = useCallback(
    async (criteria: AutoGenerationCriteria) => {
      try {
        const generatedOrders = await purchaseAPI.autoGenerate(criteria);
        setOrders((prev) => [...generatedOrders, ...prev]);
        return generatedOrders;
      } catch (error) {
        throw new AutoGenerationError(error.message);
      }
    },
    []
  );

  return {
    orders,
    loading,
    createPurchaseOrder,
    autoGenerateOrders,
    approvePurchaseOrder,
    receivePurchaseOrder,
  };
};

export const usePurchaseOrderReceiving = (orderId: string) => {
  const [order, setOrder] = useState<PurchaseOrder | null>(null);

  const receiveItems = useCallback(
    async (receivedItems: ReceivedItem[]) => {
      try {
        const updatedOrder = await purchaseAPI.receiveItems(
          orderId,
          receivedItems
        );
        setOrder(updatedOrder);

        // Update inventory levels
        receivedItems.forEach((item) => {
          updateInventoryLevel(
            item.productId,
            order!.locationId,
            item.quantityReceived,
            "add"
          );
        });

        return updatedOrder;
      } catch (error) {
        throw new ReceivingError(error.message);
      }
    },
    [orderId, order]
  );

  return {
    order,
    loading,
    receiveItems,
    reportQualityIssue,
    completeReceiving,
  };
};
```

### Automation Hooks

```typescript
export const usePurchasingAutomation = () => {
  const [rules, setRules] = useState<AutomationRules>({});
  const [automationStats, setAutomationStats] = useState<AutomationStats>();

  const createReorderRule = useCallback(
    async (ruleData: CreateReorderRuleRequest) => {
      try {
        const newRule = await automationAPI.createReorderRule(ruleData);
        setRules((prev) => ({
          ...prev,
          reorderRules: [...(prev.reorderRules || []), newRule],
        }));
        return newRule;
      } catch (error) {
        throw new AutomationRuleError(error.message);
      }
    },
    []
  );

  const executeAutomation = useCallback(
    async (criteria: ExecuteAutomationRequest) => {
      try {
        const results = await automationAPI.execute(criteria);

        // Update stats
        setAutomationStats((prev) => ({
          ...prev!,
          executionsToday: prev!.executionsToday + results.length,
          lastExecution: new Date(),
        }));

        return results;
      } catch (error) {
        throw new AutomationExecutionError(error.message);
      }
    },
    []
  );

  return {
    rules,
    automationStats,
    loading,
    createReorderRule,
    executeAutomation,
    updateRule,
    deleteRule,
    testRule,
  };
};

export const useSupplierPerformance = () => {
  const [performance, setPerformance] = useState<SupplierPerformanceMap>({});

  const calculatePerformance = useCallback(
    async (supplierId: string, period: DateRange) => {
      try {
        const metrics = await supplierAPI.getPerformanceMetrics(
          supplierId,
          period
        );
        setPerformance((prev) => ({
          ...prev,
          [supplierId]: metrics,
        }));
        return metrics;
      } catch (error) {
        throw new PerformanceCalculationError(error.message);
      }
    },
    []
  );

  const updateQualityRating = useCallback(
    async (supplierId: string, orderId: string, rating: QualityRating) => {
      try {
        await supplierAPI.updateQualityRating(supplierId, orderId, rating);

        // Recalculate performance metrics
        const updatedMetrics = await calculatePerformance(supplierId, {
          start: subMonths(new Date(), 12),
          end: new Date(),
        });

        return updatedMetrics;
      } catch (error) {
        throw new QualityRatingError(error.message);
      }
    },
    [calculatePerformance]
  );

  return {
    performance,
    loading,
    calculatePerformance,
    updateQualityRating,
    getTopPerformers,
    getUnderperformers,
  };
};
```

### Demand Forecasting Hooks

```typescript
export const useDemandForecasting = () => {
  const [forecasts, setForecasts] = useState<DemandForecastMap>({});
  const [accuracy, setAccuracy] = useState<ForecastAccuracy>();
  const [recommendations, setRecommendations] = useState<
    ForecastRecommendation[]
  >([]);

  const calculateForecast = useCallback(
    async (params: CalculateForecastRequest) => {
      try {
        const forecast = await forecastingAPI.calculate(params);
        setForecasts((prev) => ({
          ...prev,
          [`${params.productId}_${params.locationId || "all"}`]: forecast,
        }));
        return forecast;
      } catch (error) {
        throw new ForecastingError(error.message);
      }
    },
    []
  );

  const adjustForecast = useCallback(
    async (forecastId: string, adjustments: ForecastAdjustment[]) => {
      try {
        const adjustedForecast = await forecastingAPI.adjust(
          forecastId,
          adjustments
        );

        // Update local state
        const key = Object.keys(forecasts).find(
          (k) => forecasts[k].id === forecastId
        );
        if (key) {
          setForecasts((prev) => ({
            ...prev,
            [key]: adjustedForecast,
          }));
        }

        return adjustedForecast;
      } catch (error) {
        throw new ForecastAdjustmentError(error.message);
      }
    },
    [forecasts]
  );

  const implementRecommendations = useCallback(
    async (recommendationIds: string[]) => {
      try {
        const results = await forecastingAPI.implementRecommendations(
          recommendationIds
        );

        // Remove implemented recommendations
        setRecommendations((prev) =>
          prev.filter((rec) => !recommendationIds.includes(rec.id))
        );

        return results;
      } catch (error) {
        throw new RecommendationImplementationError(error.message);
      }
    },
    []
  );

  return {
    forecasts,
    accuracy,
    recommendations,
    loading,
    calculateForecast,
    adjustForecast,
    implementRecommendations,
    recalculateAllForecasts,
  };
};
```

---

## 📋 Implementation Checklist

### Phase 1: Multi-Location Foundation (Week 1-2)

- [ ] Location management system
- [ ] Multi-location inventory tracking
- [ ] Inventory transfer functionality
- [ ] Location-based stock levels and alerts
- [ ] Transfer approval workflows

### Phase 2: Advanced Purchase Orders (Week 3-4)

- [ ] Enhanced purchase order system
- [ ] Supplier performance tracking
- [ ] Quality management integration
- [ ] Advanced receiving processes
- [ ] Purchase analytics and reporting

### Phase 3: Automation Engine (Week 5-7)

- [ ] Reorder rule engine
- [ ] Automated purchase order generation
- [ ] Supplier selection automation
- [ ] Approval workflow automation
- [ ] Performance monitoring and optimization

### Phase 4: Demand Forecasting (Week 8-10)

- [ ] AI/ML forecasting models
- [ ] Historical data analysis
- [ ] Seasonality detection
- [ ] External factor integration
- [ ] Forecast accuracy tracking

### Phase 5: Advanced Analytics & Integration (Week 11-12)

- [ ] Comprehensive purchasing analytics
- [ ] Supplier relationship management
- [ ] Integration with financial module
- [ ] Mobile applications for receiving
- [ ] Performance optimization and testing

This Advanced Inventory & Purchasing Module provides enterprise-level functionality with intelligent automation, multi-location support, and predictive analytics to optimize inventory investment and supplier relationships.
