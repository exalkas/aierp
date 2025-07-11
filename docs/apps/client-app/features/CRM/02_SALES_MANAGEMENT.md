# 02_SALES_MANAGEMENT - Revenue Engine

## Document Information

- **Feature**: Sales Management (Opportunities, Quotes, Pipeline)
- **Priority**: ⭐ CORE REVENUE - Direct revenue generation
- **Implementation**: Month 2 (Phase 1)
- **Dependencies**: 01_Customer_Management
- **Impact**: Primary revenue generation and sales productivity

## 🎯 Feature Overview

Sales Management provides comprehensive opportunity tracking, quote generation, and visual pipeline management with full customization capabilities and Greek market specialization.

### Core Capabilities

- **Dynamic Opportunity Management**: Customizable sales pipeline with user-defined stages
- **Professional Quote Generation**: Greek-formatted quotes with standard pricing
- **Visual Pipeline**: Drag-and-drop deal progression with custom fields
- **Sales Analytics**: Performance tracking and forecasting
- **Greek Integration**: Greek currency formatting, business hours, cultural adaptations

---

## 📋 Screens & User Interface

### 1. Opportunity Management

#### Opportunity Pipeline Screen (`/opportunities/pipeline`)

```typescript
interface OpportunityPipelineScreen {
  // Visual Kanban-style pipeline with custom stages
  // Drag-and-drop deal progression
  // Custom field display per stage
  // Filtering by user, team, time period
  // Real-time collaboration and updates
}
```

#### Opportunity List Screen (`/opportunities`)

```typescript
interface OpportunityListScreen {
  // Customizable grid with user-defined columns
  // Advanced filtering with custom fields
  // Bulk operations (assign, update stage, etc.)
  // Sales performance metrics
  // Forecasting and quota tracking
}
```

#### Opportunity Detail Screen (`/opportunities/:id`)

```typescript
interface OpportunityDetailScreen {
  // Dynamic layout with custom sections
  // Activity timeline and communication history
  // Related quotes and proposals
  // Custom field groups and tabs
  // Greek compliance information (VAT, invoicing)
}
```

### 2. Quote & Proposal Management

#### Quote Builder Screen (`/quotes/builder/:id?`)

```typescript
interface QuoteBuilderScreen {
  // Drag-and-drop quote designer
  // Product/service catalog integration
  // Greek VAT and tax calculations
  // Template management with custom fields
  // Multi-currency support (EUR default)
}
```

#### Quote List Screen (`/quotes`)

```typescript
interface QuoteListScreen {
  // Quote status tracking (draft, sent, accepted, expired)
  // Template management and versioning
  // Custom approval workflows
  // Performance analytics (acceptance rates)
}
```

### 3. Sales Analytics

#### Sales Dashboard Screen (`/sales/dashboard`)

```typescript
interface SalesDashboardScreen {
  // Customizable widgets with dynamic metrics
  // Pipeline analytics and conversion rates
  // Individual and team performance
  // Greek market specific KPIs
  // Forecasting with custom formulas
}
```

---

## 🗄️ Data Models (Dynamic Schema)

### Opportunity Model

```typescript
interface Opportunity {
  // Core Fields
  id: string;
  name: string;
  accountId: string;
  contactId?: string;
  amount: number;
  currency: string;

  // Dynamic Stage Management
  stageId: string; // References custom stage
  stageName: string; // Current stage name
  stageOrder: number; // Stage position in pipeline
  probability: number; // Success probability (0-100)

  // Greek Business Context
  currency: string; // Default: EUR
  greekBusinessHours?: boolean; // Respect Greek business scheduling

  // Sales Process Fields
  leadSource?: string;
  competitorId?: string;
  lossReason?: string;
  winReason?: string;

  // Dates
  closeDate: Date;
  lastActivityDate?: Date;

  // Assignment
  assignedUserId: string;
  teamIds?: string[];

  // Dynamic Custom Fields (EspoCRM-style)
  customFields: Record<string, any>;

  // Audit Fields
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

interface OpportunityStage {
  id: string;
  name: string;
  order: number;
  probability: number;
  color: string;
  isWon: boolean;
  isLost: boolean;
  // Dynamic requirements per stage
  requiredFields?: string[];
  customValidation?: any;
}
```

### Quote Model

```typescript
interface Quote {
  // Core Fields
  id: string;
  number: string; // Auto-generated quote number
  name: string;
  opportunityId?: string;
  accountId: string;
  contactId: string;

  // Quote Details
  status: "draft" | "sent" | "accepted" | "rejected" | "expired";
  validUntil: Date;

  // Greek Customer Data
  afm?: string; // Customer AFM
  billingAddress: GreekAddress;

  // Financial
  subtotal: number;
  discount?: number;
  total: number;
  currency: string;

  // Quote Items (Dynamic)
  items: QuoteItem[];

  // Template and Customization
  templateId?: string;
  customSections?: QuoteSection[];

  // Dynamic Custom Fields
  customFields: Record<string, any>;

  // Audit Fields
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

interface QuoteItem {
  id: string;
  productId?: string;
  name: string;
  description?: string;
  quantity: number;
  unitPrice: number;
  total: number;
  // Dynamic item fields
  customFields?: Record<string, any>;
}
```

---

## 🔌 API Specifications

### Opportunity APIs

```typescript
// GET /api/opportunities/pipeline - Get pipeline data
interface GetPipelineResponse {
  stages: OpportunityStage[];
  opportunities: Record<string, Opportunity[]>; // Grouped by stage
  metrics: {
    totalValue: number;
    weightedValue: number;
    count: number;
  };
}

// POST /api/opportunities/:id/move-stage - Move to different stage
interface MoveStageRequest {
  targetStageId: string;
  customFieldUpdates?: Record<string, any>;
}

// GET /api/opportunities/forecast - Sales forecasting
interface ForecastRequest {
  period: "month" | "quarter" | "year";
  teamId?: string;
  userId?: string;
}

interface ForecastResponse {
  forecast: {
    period: string;
    committed: number;
    bestCase: number;
    worstCase: number;
    quota?: number;
  }[];
  accuracy: number;
}
```

### Quote APIs

```typescript
// POST /api/quotes/generate - Generate quote from opportunity
interface GenerateQuoteRequest {
  opportunityId: string;
  templateId?: string;
  includeProducts?: boolean;
}

// POST /api/quotes/:id/calculate-total - Calculate quote totals
interface CalculateTotalRequest {
  items: QuoteItem[];
  discount?: number;
}

interface CalculateTotalResponse {
  items: QuoteItem[];
  subtotal: number;
  discount: number;
  total: number;
}

// POST /api/quotes/:id/send - Send quote to customer
interface SendQuoteRequest {
  emailTemplate?: string;
  customMessage?: string;
  attachPdf?: boolean;
}
```

---

## ⚛️ React Components (Dynamic UI)

### Pipeline Components

```typescript
// Dynamic Pipeline Board
interface PipelineBoardProps {
  stages: OpportunityStage[];
  opportunities: Record<string, Opportunity[]>;
  customFields: CustomField[];
  onStageMove: (opportunityId: string, stageId: string) => void;
}

const PipelineBoard: React.FC<PipelineBoardProps> = ({
  stages,
  opportunities,
  customFields,
}) => {
  const { handleDragEnd } = usePipelineDragDrop();

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <PipelineContainer>
        {stages.map((stage) => (
          <PipelineStage
            key={stage.id}
            stage={stage}
            opportunities={opportunities[stage.id] || []}
            customFields={customFields}
          />
        ))}
      </PipelineContainer>
    </DragDropContext>
  );
};

// Dynamic Opportunity Card
interface OpportunityCardProps {
  opportunity: Opportunity;
  customFields: CustomField[];
  onEdit?: () => void;
}

const OpportunityCard: React.FC<OpportunityCardProps> = ({
  opportunity,
  customFields,
}) => {
  const displayFields = customFields.filter((f) => f.showInPipeline);

  return (
    <Card>
      <CardHeader>
        <Title>{opportunity.name}</Title>
        <Amount>{formatGreekCurrency(opportunity.totalWithVat)}</Amount>
      </CardHeader>
      <CardBody>
        <Account>{opportunity.accountName}</Account>
        <CloseDate>{formatGreekDate(opportunity.closeDate)}</CloseDate>

        {/* Dynamic Custom Fields Display */}
        {displayFields.map((field) => (
          <CustomFieldDisplay
            key={field.name}
            field={field}
            value={opportunity.customFields[field.name]}
          />
        ))}
      </CardBody>
    </Card>
  );
};
```

### Quote Builder Components

```typescript
// Dynamic Quote Builder
interface QuoteBuilderProps {
  quote?: Quote;
  templates: QuoteTemplate[];
  customFields: CustomField[];
  onSave: (quote: Quote) => void;
}

const QuoteBuilder: React.FC<QuoteBuilderProps> = ({
  quote,
  templates,
  customFields,
}) => {
  const { form, updateForm } = useQuoteForm(quote);
  const { calculateTotal } = useQuoteCalculation();

  return (
    <QuoteBuilderLayout>
      <QuoteHeader>
        <DynamicForm
          fields={customFields.filter((f) => f.section === "header")}
          data={form}
          onChange={updateForm}
        />
      </QuoteHeader>

      <QuoteItems>
        <QuoteItemGrid items={form.items} onItemChange={handleItemChange} />
      </QuoteItems>

      <QuoteTotals>
        <QuoteSummary
          subtotal={form.subtotal}
          discount={form.discount}
          total={form.total}
          currency={form.currency}
        />
      </QuoteTotals>

      <QuoteActions>
        <Button onClick={calculateTotal}>Υπολογισμός Συνόλου</Button>
        <Button onClick={() => onSave(form)}>Αποθήκευση</Button>
      </QuoteActions>
    </QuoteBuilderLayout>
  );
};

// Greek Currency Formatter Component
const GreekCurrencyFormatter: React.FC<CurrencyFormatterProps> = ({
  amount,
  currency = "EUR",
}) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("el-GR", {
      style: "currency",
      currency: currency,
      minimumFractionDigits: 2,
    }).format(value);
  };

  return <CurrencyDisplay>{formatCurrency(amount)}</CurrencyDisplay>;
};
```

---

## 🪝 Custom Hooks (Dynamic Support)

### Sales Management Hooks

```typescript
const usePipelineStages = () => {
  return useQuery({
    queryKey: ["pipeline-stages"],
    queryFn: () => salesApi.getPipelineStages(),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

const usePipelineOpportunities = (filters?: PipelineFilters) => {
  return useQuery({
    queryKey: ["pipeline-opportunities", filters],
    queryFn: () => salesApi.getPipelineOpportunities(filters),
    refetchInterval: 30 * 1000, // Real-time updates every 30s
  });
};

const usePipelineDragDrop = () => {
  const { mutate: moveOpportunity } = useMoveOpportunityStage();

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const { draggableId, destination } = result;
    const opportunityId = draggableId;
    const targetStageId = destination.droppableId;

    moveOpportunity({ opportunityId, targetStageId });
  };

  return { handleDragEnd };
};

// Dynamic Custom Fields Hook
const useCustomFields = (entityType: "opportunity" | "quote") => {
  return useQuery({
    queryKey: ["custom-fields", entityType],
    queryFn: () => customFieldApi.getFields(entityType),
    staleTime: 15 * 60 * 1000, // 15 minutes
  });
};

const useDynamicForm = <T>(initialData: T, customFields: CustomField[]) => {
  const [form, setForm] = useState<T & Record<string, any>>({
    ...initialData,
    customFields: {},
  });

  const updateField = (fieldName: string, value: any) => {
    if (customFields.find((f) => f.name === fieldName)) {
      setForm((prev) => ({
        ...prev,
        customFields: {
          ...prev.customFields,
          [fieldName]: value,
        },
      }));
    } else {
      setForm((prev) => ({ ...prev, [fieldName]: value }));
    }
  };

  const validateForm = () => {
    const errors: ValidationError[] = [];

    // Validate custom fields
    customFields.forEach((field) => {
      if (field.required && !form.customFields[field.name]) {
        errors.push({
          field: field.name,
          message: `${field.label} είναι υποχρεωτικό`,
        });
      }

      // Type-specific validation
      if (form.customFields[field.name] && field.validation) {
        const fieldValue = form.customFields[field.name];
        if (field.type === "email" && !isValidEmail(fieldValue)) {
          errors.push({
            field: field.name,
            message: `Μη έγκυρο email`,
          });
        }
        // Add more validation rules...
      }
    });

    return { valid: errors.length === 0, errors };
  };

  return { form, updateField, validateForm };
};
```

### Quote Calculation Hooks

```typescript
const useQuoteCalculation = () => {
  const calculateTotal = async (items: QuoteItem[], discount: number = 0) => {
    // Calculate subtotal from all items
    const subtotal = items.reduce(
      (sum, item) => sum + item.quantity * item.unitPrice,
      0
    );

    // Apply discount
    const discountAmount = subtotal * (discount / 100);
    const total = subtotal - discountAmount;

    return {
      subtotal,
      discount: discountAmount,
      total,
    };
  };

  const validateQuoteItems = (items: QuoteItem[]) => {
    const errors: ValidationError[] = [];

    items.forEach((item, index) => {
      if (!item.name) {
        errors.push({
          field: `item[${index}].name`,
          message: "Το όνομα είναι υποχρεωτικό",
        });
      }
      if (item.quantity <= 0) {
        errors.push({
          field: `item[${index}].quantity`,
          message: "Η ποσότητα πρέπει να είναι μεγαλύτερη από 0",
        });
      }
      if (item.unitPrice <= 0) {
        errors.push({
          field: `item[${index}].unitPrice`,
          message: "Η τιμή πρέπει να είναι μεγαλύτερη από 0",
        });
      }
    });

    return { valid: errors.length === 0, errors };
  };

  const formatGreekCurrency = (amount: number, currency: string = "EUR") => {
    return new Intl.NumberFormat("el-GR", {
      style: "currency",
      currency: currency,
      minimumFractionDigits: 2,
    }).format(amount);
  };

  return { calculateTotal, validateQuoteItems, formatGreekCurrency };
};
```

---

## 🧪 Testing Specifications

### Dynamic Field Tests

```typescript
describe("Dynamic Opportunity Management", () => {
  it("renders custom fields in pipeline cards", async () => {
    const customFields = [
      {
        name: "priority",
        type: "select",
        label: "Προτεραιότητα",
        showInPipeline: true,
      },
      {
        name: "notes",
        type: "textarea",
        label: "Σημειώσεις",
        showInPipeline: false,
      },
    ];

    const opportunity = {
      id: "1",
      name: "Test Deal",
      customFields: { priority: "high" },
    };

    const { getByText } = render(
      <OpportunityCard opportunity={opportunity} customFields={customFields} />
    );

    expect(getByText("Προτεραιότητα: high")).toBeInTheDocument();
    expect(() => getByText("Σημειώσεις")).toThrow(); // Should not show
  });

  it("handles stage movement with custom field validation", async () => {
    const stageWithRequiredFields = {
      id: "proposal",
      name: "Proposal",
      requiredFields: ["budget", "timeline"],
    };

    const opportunity = {
      id: "1",
      customFields: { budget: 50000 }, // Missing timeline
    };

    const { moveOpportunity } = usePipelineDragDrop();

    await expect(
      moveOpportunity(opportunity.id, stageWithRequiredFields.id)
    ).rejects.toThrow("Timeline is required for Proposal stage");
  });
});

describe("Quote Calculations", () => {
  it("calculates quote totals correctly", async () => {
    const items = [
      { quantity: 2, unitPrice: 100, name: "Service A", total: 200 },
      { quantity: 1, unitPrice: 50, name: "Service B", total: 50 },
    ];

    const { calculateTotal } = useQuoteCalculation();
    const result = await calculateTotal(items, 10); // 10% discount

    expect(result.subtotal).toBe(250);
    expect(result.discount).toBe(25); // 10% of 250
    expect(result.total).toBe(225); // 250 - 25
  });

  it("validates quote items correctly", () => {
    const { validateQuoteItems } = useQuoteCalculation();

    const validItems = [
      { name: "Service", quantity: 1, unitPrice: 100, total: 100 },
    ];

    const invalidItems = [{ name: "", quantity: 0, unitPrice: -10, total: 0 }];

    expect(validateQuoteItems(validItems).valid).toBe(true);
    expect(validateQuoteItems(invalidItems).valid).toBe(false);
  });
});

describe("Quote Builder E2E", () => {
  it("creates complete Greek quote", async () => {
    await page.goto("/quotes/builder");

    // Fill quote details
    await page.fill('[data-testid="quote-name"]', "Προσφορά για Υπηρεσίες");
    await page.selectOption('[data-testid="account"]', "test-account-1");

    // Add quote items
    await page.click('[data-testid="add-item"]');
    await page.fill('[data-testid="item-name-0"]', "Υπηρεσίες Συμβουλευτικής");
    await page.fill('[data-testid="item-quantity-0"]', "10");
    await page.fill('[data-testid="item-price-0"]', "100");

    // Apply discount
    await page.fill('[data-testid="discount"]', "10");

    // Calculate total
    await page.click('[data-testid="calculate-total"]');

    // Verify calculations
    await expect(page.locator('[data-testid="subtotal"]')).toContainText(
      "1.000,00 €"
    );
    await expect(page.locator('[data-testid="discount-amount"]')).toContainText(
      "100,00 €"
    );
    await expect(page.locator('[data-testid="total"]')).toContainText(
      "900,00 €"
    );

    // Save quote
    await page.click('[data-testid="save-quote"]');

    await expect(page.locator(".success-message")).toContainText(
      "Επιτυχής αποθήκευση προσφοράς"
    );
  });
});
```

---

## 📋 Implementation Checklist

### Phase 1: Opportunity Management (Week 1-2)

- [ ] **Dynamic Pipeline**: Customizable stages with drag-and-drop
- [ ] **Opportunity CRUD**: Full lifecycle with custom fields
- [ ] **Greek Integration**: Currency formatting and business hours
- [ ] **Real-time Updates**: WebSocket for pipeline collaboration

### Phase 2: Quote Management (Week 3-4)

- [ ] **Quote Builder**: Dynamic template system
- [ ] **Quote Calculations**: Subtotal, discount, and total calculations
- [ ] **PDF Generation**: Professional Greek quotes
- [ ] **Approval Workflows**: Custom approval processes

### Phase 3: Sales Analytics (Week 5-6)

- [ ] **Performance Dashboards**: Custom metrics and KPIs
- [ ] **Forecasting Engine**: Predictive sales analytics
- [ ] **Reporting System**: Dynamic report generation
- [ ] **Greek Market Analytics**: Localized business intelligence

---

**Status**: Specification Complete  
**Next**: 03_ACTIVITY_TASK_MANAGEMENT.md  
**Dependencies**: 01_Customer_Management  
**Key Feature**: Dynamic custom fields throughout
