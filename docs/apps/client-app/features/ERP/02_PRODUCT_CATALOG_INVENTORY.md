# 02. Product Catalog & Inventory Module - Technical Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Module**: Product Catalog & Inventory (€29/month)
- **Dependencies**: Basic Invoicing Module
- **Target Users**: Retail businesses, Restaurants, Small manufacturers, E-commerce stores

## Overview

The Product Catalog & Inventory Module enables businesses to manage their product inventory, track stock levels, handle suppliers, and seamlessly integrate with invoicing. This module is essential for businesses that sell physical products and need to track inventory movement.

---

## 🖥️ Screens & User Interface

### 1. Inventory Dashboard (`/erp/inventory/dashboard`)

**Purpose**: Overview of inventory status and key metrics

```typescript
const InventoryDashboard: React.FC = () => {
  const { summary, loading } = useInventorySummary();

  return (
    <DashboardLayout>
      <DashboardHeader title="Inventory Overview" />

      <MetricsGrid>
        <MetricCard
          title="Total Products"
          value={summary.totalProducts}
          subtitle="Active SKUs"
          icon={<PackageIcon />}
        />
        <MetricCard
          title="Total Stock Value"
          value={formatEuro(summary.stockValue)}
          change="+5.2%"
          icon={<EuroIcon />}
        />
        <MetricCard
          title="Low Stock Items"
          value={summary.lowStockCount}
          status="warning"
          icon={<AlertIcon />}
        />
        <MetricCard
          title="Out of Stock"
          value={summary.outOfStockCount}
          status="danger"
          icon={<XCircleIcon />}
        />
      </MetricsGrid>

      <InventoryAlertsWidget />
      <TopProductsWidget />
      <StockMovementChart />
    </DashboardLayout>
  );
};
```

### 2. Product Catalog (`/erp/inventory/products`)

**Purpose**: Manage product catalog and detailed product information

```typescript
const ProductCatalog: React.FC = () => {
  const { products, loading, filters, updateFilter } = useProducts();

  return (
    <PageLayout>
      <PageHeader title="Product Catalog" actions={<CreateProductButton />} />

      <FilterBar>
        <CategoryFilter
          value={filters.category}
          onChange={(cat) => updateFilter("category", cat)}
        />
        <StockStatusFilter
          value={filters.stockStatus}
          onChange={(status) => updateFilter("stockStatus", status)}
        />
        <SupplierFilter
          value={filters.supplierId}
          onChange={(id) => updateFilter("supplierId", id)}
        />
      </FilterBar>

      <ProductGrid
        products={products}
        loading={loading}
        viewMode="grid" // or "list"
        onProductClick={(product) =>
          navigate(`/erp/inventory/products/${product.id}`)
        }
      />
    </PageLayout>
  );
};
```

### 3. Product Detail (`/erp/inventory/products/:id`)

**Purpose**: Detailed product view with inventory tracking

```typescript
const ProductDetail: React.FC<{ productId: string }> = ({ productId }) => {
  const { product, stockHistory, loading } = useProduct(productId);

  return (
    <DetailLayout>
      <ProductHeader product={product} />

      <ProductDetailTabs>
        <TabPanel label="Overview">
          <ProductInfoCard product={product} />
          <StockLevelsCard product={product} />
          <PricingCard product={product} />
        </TabPanel>

        <TabPanel label="Stock History">
          <StockMovementHistory
            movements={stockHistory}
            productId={productId}
          />
        </TabPanel>

        <TabPanel label="Suppliers">
          <ProductSuppliers product={product} />
        </TabPanel>

        <TabPanel label="Sales Analytics">
          <ProductSalesAnalytics productId={productId} />
        </TabPanel>
      </ProductDetailTabs>
    </DetailLayout>
  );
};
```

### 4. Stock Management (`/erp/inventory/stock`)

**Purpose**: Track and adjust inventory levels

```typescript
const StockManagement: React.FC = () => {
  return (
    <PageLayout>
      <PageHeader title="Stock Management" />

      <StockActionBar>
        <AdjustStockButton />
        <StockTakeButton />
        <ImportStockButton />
        <ExportStockButton />
      </StockActionBar>

      <StockGrid
        products={products}
        columns={[
          "product",
          "sku",
          "currentStock",
          "reorderLevel",
          "lastMovement",
          "actions",
        ]}
        allowInlineEdit
      />
    </PageLayout>
  );
};
```

### 5. Suppliers (`/erp/inventory/suppliers`)

**Purpose**: Manage supplier relationships and purchase orders

```typescript
const Suppliers: React.FC = () => {
  const { suppliers, loading } = useSuppliers();

  return (
    <PageLayout>
      <PageHeader title="Suppliers" actions={<CreateSupplierButton />} />

      <SupplierList
        suppliers={suppliers}
        loading={loading}
        showMetrics={["totalProducts", "avgDeliveryTime", "reliabilityScore"]}
      />
    </PageLayout>
  );
};
```

---

## 🔗 API Endpoints

### Product Management APIs

```typescript
// GET /api/erp/inventory/products
interface GetProductsRequest {
  page?: number;
  limit?: number;
  category?: string;
  supplierId?: string;
  stockStatus?: "in_stock" | "low_stock" | "out_of_stock";
  search?: string;
}

// POST /api/erp/inventory/products
interface CreateProductRequest {
  name: string;
  sku: string;
  description?: string;
  categoryId: string;
  unitPrice: number;
  costPrice: number;
  vatRate: number;
  minStockLevel: number;
  maxStockLevel?: number;
  supplierId?: string;
  barcode?: string;
  greekTaxInfo: ProductGreekTaxInfo;
}

// PUT /api/erp/inventory/products/:id/stock
interface UpdateStockRequest {
  newQuantity: number;
  movementType: "adjustment" | "restock" | "sale" | "damage" | "transfer";
  reason: string;
  referenceNumber?: string;
}
```

### Inventory APIs

```typescript
// GET /api/erp/inventory/stock-movements
interface GetStockMovementsRequest {
  productId?: string;
  dateFrom?: Date;
  dateTo?: Date;
  movementType?: StockMovementType[];
}

// POST /api/erp/inventory/stock-take
interface CreateStockTakeRequest {
  products: StockTakeItem[];
  locationId?: string;
  notes?: string;
}

// GET /api/erp/inventory/low-stock
interface GetLowStockResponse {
  products: LowStockProduct[];
  recommendations: RestockRecommendation[];
}
```

---

## 🗃️ Data Models

### Core Product Model

```typescript
interface Product {
  id: string;
  name: string;
  sku: string;
  description?: string;

  // Categorization
  categoryId: string;
  category: ProductCategory;
  tags: string[];

  // Pricing
  unitPrice: number; // Selling price
  costPrice: number; // Cost/purchase price
  currency: string;

  // Inventory
  currentStock: number;
  minStockLevel: number;
  maxStockLevel?: number;
  reorderPoint: number;

  // Physical attributes
  weight?: number;
  dimensions?: ProductDimensions;
  barcode?: string;

  // Greek tax information
  greekTaxInfo: ProductGreekTaxInfo;

  // Supplier information
  primarySupplierId?: string;
  primarySupplier?: Supplier;
  alternativeSuppliers: ProductSupplier[];

  // Status
  status: ProductStatus;
  isActive: boolean;

  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;

  // Calculated fields
  stockValue: number; // currentStock * costPrice
  stockStatus: StockStatus;
  lastMovementDate?: Date;
}

interface ProductCategory {
  id: string;
  name: string;
  parentId?: string;
  vatRate: number;
  greekTaxCategory: GreekTaxCategory;
}

type ProductStatus = "active" | "discontinued" | "draft";
type StockStatus = "in_stock" | "low_stock" | "out_of_stock";
```

### Stock Movement Model

```typescript
interface StockMovement {
  id: string;
  productId: string;

  // Movement details
  movementType: StockMovementType;
  quantity: number;
  previousStock: number;
  newStock: number;

  // Cost information
  unitCost?: number;
  totalCost?: number;

  // Reference information
  referenceType?: "invoice" | "purchase_order" | "adjustment" | "transfer";
  referenceId?: string;
  reason: string;

  // Location (for multi-location businesses)
  locationId?: string;
  fromLocationId?: string;
  toLocationId?: string;

  // Audit
  createdAt: Date;
  createdBy: string;
}

type StockMovementType =
  | "sale" // Product sold to customer
  | "purchase" // Product purchased from supplier
  | "adjustment" // Manual stock adjustment
  | "damage" // Product damaged/expired
  | "transfer" // Transfer between locations
  | "restock" // Restocking from supplier
  | "return"; // Customer return
```

### Supplier Model

```typescript
interface Supplier {
  id: string;
  name: string;
  contactPerson?: string;

  // Contact information
  email?: string;
  phone?: string;
  address: Address;

  // Greek business information
  greekTaxInfo: SupplierGreekTaxInfo;

  // Business relationship
  paymentTerms: string;
  defaultLeadTime: number; // Days
  minimumOrderValue?: number;

  // Performance metrics
  reliabilityScore: number; // 1-5
  averageDeliveryTime: number;
  qualityRating: number; // 1-5

  // Status
  status: SupplierStatus;
  isPreferred: boolean;

  // Products
  products: ProductSupplier[];

  // Audit
  createdAt: Date;
  updatedAt: Date;
}

interface ProductSupplier {
  productId: string;
  supplierId: string;
  supplierSKU?: string;
  costPrice: number;
  minimumQuantity?: number;
  leadTime: number;
  isPrimary: boolean;
}

type SupplierStatus = "active" | "inactive" | "blocked";
```

---

## 🧩 UI Components

### Product Components

```typescript
// Product display components
export const ProductCard: React.FC<ProductCardProps>;
export const ProductGrid: React.FC<ProductGridProps>;
export const ProductList: React.FC<ProductListProps>;
export const ProductSelector: React.FC<ProductSelectorProps>;

// Product forms
export const ProductForm: React.FC<ProductFormProps>;
export const QuickProductCreate: React.FC<QuickProductCreateProps>;
export const ProductPriceEditor: React.FC<ProductPriceEditorProps>;

// Stock components
export const StockLevelIndicator: React.FC<StockLevelIndicatorProps>;
export const StockMovementHistory: React.FC<StockMovementHistoryProps>;
export const StockAdjustmentForm: React.FC<StockAdjustmentFormProps>;

// Supplier components
export const SupplierCard: React.FC<SupplierCardProps>;
export const SupplierSelector: React.FC<SupplierSelectorProps>;
export const SupplierProductList: React.FC<SupplierProductListProps>;
```

### Inventory Analytics Components

```typescript
export const InventoryDashboard: React.FC<InventoryDashboardProps>;
export const StockValueChart: React.FC<StockValueChartProps>;
export const TopProductsWidget: React.FC<TopProductsWidgetProps>;
export const LowStockAlert: React.FC<LowStockAlertProps>;
export const InventoryTurnoverChart: React.FC<InventoryTurnoverChartProps>;
```

---

## 🪝 Custom Hooks

### Product Management Hooks

```typescript
export const useProducts = (filters?: ProductFilters) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  // Implementation includes pagination, filtering, sorting

  return {
    products,
    loading,
    error,
    createProduct,
    updateProduct,
    deleteProduct,
    refetch,
  };
};

export const useProduct = (productId: string) => {
  return {
    product,
    stockHistory,
    salesData,
    loading,
    updateStock,
    updatePrice,
    updateDetails,
  };
};

export const useInventorySummary = () => {
  return {
    totalProducts,
    stockValue,
    lowStockCount,
    outOfStockCount,
    topMovingProducts,
    slowMovingProducts,
  };
};
```

### Stock Management Hooks

```typescript
export const useStockMovements = (productId?: string) => {
  return {
    movements,
    loading,
    createMovement,
    getMovementHistory,
  };
};

export const useStockLevels = () => {
  return {
    lowStockProducts,
    outOfStockProducts,
    restockRecommendations,
    updateStockLevels,
  };
};

export const useStockAdjustment = () => {
  const adjustStock = useCallback(
    async (productId: string, adjustment: StockAdjustment) => {
      try {
        const result = await stockAPI.adjustStock(productId, adjustment);
        // Update local state and trigger refetch
        return result;
      } catch (error) {
        throw new StockAdjustmentError(error.message);
      }
    },
    []
  );

  return { adjustStock, bulkAdjustStock };
};
```

### Supplier Hooks

```typescript
export const useSuppliers = (filters?: SupplierFilters) => {
  return {
    suppliers,
    loading,
    createSupplier,
    updateSupplier,
  };
};

export const useSupplier = (supplierId: string) => {
  return {
    supplier,
    products,
    performanceMetrics,
    updateSupplier,
  };
};

export const useSupplierPerformance = (supplierId: string) => {
  return {
    deliveryPerformance,
    qualityMetrics,
    reliabilityScore,
    costAnalysis,
  };
};
```

---

## 🌐 Context Providers

### Inventory Context

```typescript
interface InventoryContextValue {
  // Current settings
  defaultUnit: string;
  currency: string;
  stockAlertThreshold: number;

  // Business rules
  allowNegativeStock: boolean;
  requireStockAdjustmentReasons: boolean;
  autoGenerateSKU: boolean;

  // Location settings (for multi-location)
  currentLocationId?: string;
  locations: Location[];

  // Functions
  updateStockSettings: (settings: StockSettings) => void;
  getProductAvailability: (productId: string) => ProductAvailability;
}

export const InventoryProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { company } = useCompany();
  const [settings, setSettings] = useState<InventorySettings>();

  useEffect(() => {
    loadInventorySettings(company.id).then(setSettings);
  }, [company.id]);

  const value: InventoryContextValue = {
    defaultUnit: settings?.defaultUnit || "pieces",
    currency: settings?.currency || "EUR",
    stockAlertThreshold: settings?.stockAlertThreshold || 10,
    allowNegativeStock: settings?.allowNegativeStock || false,
    requireStockAdjustmentReasons:
      settings?.requireStockAdjustmentReasons || true,
    autoGenerateSKU: settings?.autoGenerateSKU || true,
    currentLocationId: settings?.defaultLocationId,
    locations: settings?.locations || [],
    updateStockSettings: (newSettings) => {
      setSettings((prev) => ({ ...prev, ...newSettings }));
      saveInventorySettings(company.id, newSettings);
    },
    getProductAvailability: (productId) => {
      // Calculate availability across locations
      return calculateAvailability(productId, settings);
    },
  };

  return (
    <InventoryContext.Provider value={value}>
      {children}
    </InventoryContext.Provider>
  );
};
```

---

## 🔗 Integration with Other Modules

### Integration with Basic Invoicing

```typescript
// Product selection in invoice creation
interface InvoiceProductIntegration {
  // When creating invoices, products can be selected from catalog
  // Stock is automatically reduced when invoice is marked as delivered
  // Product prices are pre-filled from catalog

  onInvoiceProductSelect: (productId: string) => {
    const product = getProduct(productId);
    return {
      description: product.name,
      unitPrice: product.unitPrice,
      vatRate: product.greekTaxInfo.vatRate,
      availableStock: product.currentStock
    };
  };

  onInvoiceDelivered: (invoiceId: string) => {
    // Automatically reduce stock for delivered products
    const invoice = getInvoice(invoiceId);
    invoice.items.forEach(item => {
      if (item.productId) {
        reduceStock(item.productId, item.quantity, {
          movementType: 'sale',
          referenceType: 'invoice',
          referenceId: invoiceId
        });
      }
    });
  };
}
```

### CRM Integration

```typescript
// Customer purchase history and preferences
interface CustomerProductIntegration {
  getCustomerPurchaseHistory: (customerId: string) => CustomerPurchaseHistory;
  getCustomerProductPreferences: (customerId: string) => ProductPreference[];
  suggestProductsForCustomer: (customerId: string) => ProductRecommendation[];
}
```

---

## 📋 Implementation Checklist

### Phase 1: Core Product Management (Week 1-2)

- [ ] Product data models and database schema
- [ ] Product CRUD APIs
- [ ] Product catalog interface
- [ ] Product categories and organization
- [ ] Basic stock tracking

### Phase 2: Inventory Management (Week 3-4)

- [ ] Stock movement tracking
- [ ] Stock adjustment functionality
- [ ] Low stock alerts and notifications
- [ ] Inventory reporting
- [ ] Barcode support

### Phase 3: Supplier Management (Week 5-6)

- [ ] Supplier data management
- [ ] Supplier-product relationships
- [ ] Purchase order basics
- [ ] Supplier performance tracking
- [ ] Cost analysis

### Phase 4: Advanced Features (Week 7-8)

- [ ] Multi-location support
- [ ] Advanced analytics and reporting
- [ ] Integration with invoicing module
- [ ] Bulk operations
- [ ] Import/export functionality

### Phase 5: Testing & Polish (Week 9-10)

- [ ] Comprehensive testing
- [ ] Performance optimization
- [ ] Mobile responsiveness
- [ ] Documentation
- [ ] User training materials

This Product Catalog & Inventory Module provides comprehensive inventory management while seamlessly integrating with the invoicing system for a complete business solution.
