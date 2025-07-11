# Comprehensive Testing Specification - Greek ERP/CRM System

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: Define comprehensive testing requirements for all features
- **Scope**: Unit, Integration, E2E tests across all 4 applications

---

## 🎯 TESTING PHILOSOPHY

### Testing Pyramid Strategy

```
       🔺 E2E Tests (20%)
      🔻🔻 Integration Tests (30%)
    🔻🔻🔻🔻 Unit Tests (50%)
```

**Core Principles:**

- **Test-Driven Development**: Write tests before implementation
- **Greek Business Context**: All tests include Greek compliance scenarios
- **Real-World Data**: Use actual Greek business data in tests
- **Performance First**: Every test includes performance assertions
- **Multi-Language**: Test both Greek and English language scenarios

---

## 🧪 TESTING TYPES & REQUIREMENTS

### 1. Unit Tests (50% of test coverage)

**Purpose**: Test individual functions, components, and classes in isolation

**Requirements:**

- **Coverage**: Minimum 90% code coverage
- **Speed**: Each test must run in <100ms
- **Isolation**: No external dependencies (mock all APIs, databases)
- **Greek Validation**: All Greek-specific validation functions

**Technologies:**

- **Frontend**: Jest + React Testing Library + MSW (Mock Service Worker)
- **Backend**: pytest + pytest-mock + factory-boy
- **Database**: In-memory SQLite for fast tests

### 2. Integration Tests (30% of test coverage)

**Purpose**: Test interactions between components, API endpoints, and database operations

**Requirements:**

- **Real Database**: Use PostgreSQL test database
- **API Testing**: Test all endpoints with real HTTP requests
- **Greek Services**: Test AADE integration, banking APIs (sandbox mode)
- **Authentication**: Test JWT, permissions, role-based access

**Technologies:**

- **Frontend**: Jest + @testing-library/react + MSW + Cypress Component Testing
- **Backend**: pytest + httpx + SQLAlchemy test fixtures
- **Database**: PostgreSQL test database with migrations

### 3. End-to-End Tests (20% of test coverage)

**Purpose**: Test complete user workflows across all applications

**Requirements:**

- **User Journeys**: Complete business processes from start to finish
- **Multi-App Testing**: Test workflows that span multiple applications
- **Greek Compliance**: Full AADE submission workflows
- **Performance**: Page load times, API response times

**Technologies:**

- **E2E Framework**: Playwright (better than Cypress for multi-app testing)
- **Visual Testing**: Percy or Chromatic for UI regression
- **Performance**: Lighthouse CI for performance testing

---

## 📱 APPLICATION-SPECIFIC TESTING REQUIREMENTS

### CLIENT APP Testing Requirements

#### Core Business Logic Tests

```typescript
// Unit Tests (80+ tests)
describe("Greek Tax Calculations", () => {
  test("calculates VAT for mainland Greece business", () => {
    const result = calculateGreekVAT({
      amount: 100,
      businessType: "B2B",
      location: "athens",
      vatZone: "mainland",
    });
    expect(result.vat).toBe(24);
    expect(result.total).toBe(124);
  });

  test("calculates reduced VAT for islands", () => {
    const result = calculateGreekVAT({
      amount: 100,
      businessType: "B2C",
      location: "mykonos",
      vatZone: "reduced_islands",
    });
    expect(result.vat).toBe(13);
    expect(result.total).toBe(113);
  });
});

describe("AFM Validation", () => {
  test("validates correct AFM format", () => {
    expect(validateGreekAFM("9")).toBe(true);
  });

  test("rejects invalid AFM checksum", () => {
    expect(validateGreekAFM("8")).toBe(false);
  });
});
```

#### Integration Tests (40+ tests)

```typescript
describe("Customer Management API", () => {
  test("creates customer with Greek address validation", async () => {
    const customerData = {
      name: "Γιάννης Παπαδόπουλος",
      afm: "9",
      address: {
        street: "Ερμού 15",
        city: "Αθήνα",
        postalCode: "10563",
      },
    };

    const response = await api.post("/customers", customerData);
    expect(response.status).toBe(201);
    expect(response.data.afm).toBe("9");
  });
});
```

#### E2E Tests (15+ scenarios)

```typescript
describe("Invoice Creation Workflow", () => {
  test("complete invoice workflow with AADE submission", async () => {
    await page.goto("/invoices/new");

    // Select customer
    await page.click('[data-testid="customer-select"]');
    await page.click('[data-testid="customer-option-1"]');

    // Add products
    await page.click('[data-testid="add-product"]');
    await page.fill('[data-testid="product-quantity"]', "2");

    // Calculate totals (Greek VAT)
    await page.click('[data-testid="calculate-totals"]');
    await expect(page.locator('[data-testid="vat-amount"]')).toContainText(
      "24.00"
    );

    // Submit to AADE
    await page.click('[data-testid="submit-aade"]');
    await expect(page.locator('[data-testid="aade-status"]')).toContainText(
      "Submitted"
    );
  });
});
```

### ADMIN APP Testing Requirements

#### System Administration Tests

```typescript
// Unit Tests (60+ tests)
describe("Subscription Management", () => {
  test("calculates subscription limits correctly", () => {
    const subscription = {
      plan: "professional",
      features: ["aade_integration", "hr_module"],
      limits: { max_users: 25, max_customers: 5000 },
    };

    expect(getSubscriptionLimits(subscription)).toEqual({
      canCreateUsers: true,
      canEnableAADE: true,
      maxCustomers: 5000,
    });
  });
});

// Integration Tests (25+ tests)
describe("Feature Flag Management", () => {
  test("enables feature for specific companies", async () => {
    const response = await api.post("/admin/feature-flags/hr_module/enable", {
      companyIds: ["company-1", "company-2"],
    });

    expect(response.status).toBe(200);

    // Verify feature is enabled
    const company1Features = await api.get(
      "/admin/companies/company-1/features"
    );
    expect(company1Features.data.features).toContain("hr_module");
  });
});

// E2E Tests (8+ scenarios)
describe("Admin Dashboard Workflow", () => {
  test("manages user permissions across companies", async () => {
    await adminPage.goto("/admin/users");
    await adminPage.click('[data-testid="create-user"]');

    // Set permissions
    await adminPage.fill('[data-testid="user-email"]', "test@example.com");
    await adminPage.check('[data-testid="permission-manage-customers"]');

    await adminPage.click('[data-testid="save-user"]');
    await expect(
      adminPage.locator('[data-testid="success-message"]')
    ).toBeVisible();
  });
});
```

### USER-SUPPORT APP Testing Requirements

#### Customer Portal & Self-Service Tests

```typescript
// Unit Tests (30+ tests)
describe("Customer Support Portal", () => {
  test("renders support portal in customer's language", () => {
    const { getByText } = render(<SupportPortal locale="el" />);
    expect(getByText("Υποστήριξη")).toBeInTheDocument();
  });

  test("shows relevant knowledge base articles", () => {
    const customer = { businessType: "retail", language: "el" };
    const articles = getRelevantArticles(customer);

    expect(articles).toContain("AADE submission guide");
    expect(articles).toContain("Greek VAT calculator");
  });
});

// Integration Tests (15+ tests)
describe("AI Assistant Integration", () => {
  test("escalates complex queries to human support", async () => {
    const query = "Έχω πρόβλημα με το MyDATA που δεν μπορώ να λύσω";
    const response = await aiAssistant.processQuery(query);

    expect(response.requiresHumanSupport).toBe(true);
    expect(response.escalationReason).toBe("complex_aade_issue");
  });
});
```

### STAFF-SUPPORT APP Testing Requirements

#### Staff Ticket Management & Team Collaboration Tests

```typescript
// Unit Tests (40+ tests)
describe("Staff Ticket Management", () => {
  test("assigns tickets based on agent expertise", () => {
    const ticket = { category: "aade_integration", priority: "high" };
    const assignment = autoAssignTicket(ticket);

    expect(assignment.agentId).toBe("agent-aade-specialist");
    expect(assignment.estimatedResolutionTime).toBeLessThan(240); // 4 hours
  });

  test("tracks SLA compliance for Greek business hours", () => {
    const ticket = createTicket({
      createdAt: "2024-01-15T09:00:00+02:00", // Greek time
      priority: "high",
    });

    const slaStatus = checkSLAStatus(ticket);
    expect(slaStatus.businessHoursRemaining).toBeGreaterThan(0);
    expect(slaStatus.timezone).toBe("Europe/Athens");
  });
});

// Integration Tests (15+ tests)
describe("Team Collaboration", () => {
  test("escalates complex issues to L2 support", async () => {
    const l1Ticket = await createTicket({
      category: "complex_integration",
      attempts: 3,
      status: "escalation_required",
    });

    await escalateToL2(l1Ticket.id);

    const escalatedTicket = await api.get(
      `/staff-support/tickets/${l1Ticket.id}`
    );
    expect(escalatedTicket.data.assignedTeam).toBe("L2_technical");
    expect(escalatedTicket.data.escalationReason).toBeDefined();
  });
});

// E2E Tests (8+ scenarios)
describe("Staff Support Dashboard", () => {
  test("manages high-priority customer escalation", async () => {
    await staffPage.goto("/staff-support/dashboard");
    await staffPage.click('[data-testid="high-priority-queue"]');

    // Accept escalated ticket
    await staffPage.click('[data-testid="accept-ticket-123"]');

    // Review customer context
    await expect(
      staffPage.locator('[data-testid="customer-business-type"]')
    ).toContainText("Manufacturing");

    // Provide resolution
    await staffPage.fill(
      '[data-testid="resolution-notes"]',
      "AADE credentials updated"
    );
    await staffPage.click('[data-testid="resolve-ticket"]');

    await expect(
      staffPage.locator('[data-testid="ticket-status"]')
    ).toContainText("Resolved");
  });
});
```

### SETUP APP Testing Requirements

#### Onboarding Workflow Tests

```typescript
// Unit Tests (40+ tests)
describe("Greek Business Setup Validation", () => {
  test("validates Greek business registration data", () => {
    const businessData = {
      afm: "9",
      doy: "1101",
      legalForm: "ΑΕ",
      businessType: "manufacturing",
    };

    const validation = validateGreekBusinessSetup(businessData);
    expect(validation.isValid).toBe(true);
    expect(validation.requiredDocuments).toContain("registration_certificate");
  });
});

// Integration Tests (15+ tests)
describe("Onboarding Progress Tracking", () => {
  test("tracks setup completion across steps", async () => {
    const setupSession = await api.post("/onboarding/start", {
      companyId: "company-1",
      businessType: "retail",
    });

    // Complete step 1
    await api.post(`/onboarding/steps/company-info/complete`, {
      sessionId: setupSession.data.id,
      data: { name: "Test Company", afm: "9" },
    });

    const progress = await api.get(
      `/onboarding/progress/${setupSession.data.id}`
    );
    expect(progress.data.completedSteps).toContain("company-info");
    expect(progress.data.currentStep).toBe("aade-integration");
  });
});

// E2E Tests (6+ scenarios)
describe("Complete Onboarding Flow", () => {
  test("new user completes full setup", async () => {
    await setupPage.goto("/setup");

    // Company information
    await setupPage.fill('[data-testid="company-name"]', "Νέα Εταιρεία ΑΕ");
    await setupPage.fill('[data-testid="afm"]', "9");
    await setupPage.selectOption('[data-testid="doy"]', "1101");
    await setupPage.click('[data-testid="next-step"]');

    // AADE integration
    await setupPage.fill('[data-testid="aade-username"]', "testuser");
    await setupPage.fill('[data-testid="aade-password"]', "testpass");
    await setupPage.click('[data-testid="test-connection"]');
    await expect(
      setupPage.locator('[data-testid="connection-status"]')
    ).toContainText("Success");

    // Complete setup
    await setupPage.click('[data-testid="finish-setup"]');
    await expect(
      setupPage.locator('[data-testid="setup-complete"]')
    ).toBeVisible();
  });
});
```

---

## 🇬🇷 GREEK-SPECIFIC TESTING REQUIREMENTS

### 1. Tax Calculation Testing

```typescript
describe("Greek Tax Engine", () => {
  const taxScenarios = [
    { location: "athens", businessType: "B2B", expectedVAT: 24 },
    { location: "thessaloniki", businessType: "B2C", expectedVAT: 24 },
    { location: "mykonos", businessType: "B2B", expectedVAT: 13 },
    { location: "rhodes", businessType: "tourism", expectedVAT: 13 },
    { location: "crete", businessType: "agriculture", expectedVAT: 13 },
  ];

  taxScenarios.forEach((scenario) => {
    test(`calculates correct VAT for ${scenario.location} ${scenario.businessType}`, () => {
      const result = calculateGreekVAT(100, scenario);
      expect(result.vatRate).toBe(scenario.expectedVAT);
    });
  });
});
```

### 2. AADE Integration Testing

```typescript
describe("AADE MyDATA Integration", () => {
  test("submits invoice to AADE sandbox", async () => {
    const invoice = createTestInvoice();
    const submission = await submitToAADE(invoice, { sandbox: true });

    expect(submission.status).toBe("submitted");
    expect(submission.mark).toBeDefined();
    expect(submission.qrCodeUrl).toMatch(/^https:\/\/mydataaade/);
  });

  test("handles AADE validation errors", async () => {
    const invalidInvoice = createTestInvoice({ afm: "invalid" });

    await expect(submitToAADE(invalidInvoice)).rejects.toThrow(
      "Invalid AFM format"
    );
  });
});
```

### 3. Greek Language Testing

```typescript
describe("Greek Language Support", () => {
  test("displays Greek text correctly", async () => {
    await page.goto("/customers?lang=el");

    await expect(page.locator("h1")).toContainText("Πελάτες");
    await expect(page.locator('[data-testid="add-customer"]')).toContainText(
      "Προσθήκη Πελάτη"
    );
  });

  test("validates Greek phone numbers", () => {
    const greekMobile = "+3069";
    const greekLandline = "+302101234567";

    expect(validateGreekPhone(greekMobile)).toBe(true);
    expect(validateGreekPhone(greekLandline)).toBe(true);
    expect(validateGreekPhone("+90")).toBe(false);
  });
});
```

---

## 🚀 PERFORMANCE TESTING REQUIREMENTS

### Performance Targets

| Operation       | Target     | Test Method       |
| --------------- | ---------- | ----------------- |
| Page Load       | <2 seconds | Lighthouse CI     |
| API Response    | <500ms     | Load testing      |
| Database Query  | <100ms     | Query profiling   |
| File Upload     | >10MB/s    | Performance tests |
| AADE Submission | <5 seconds | Integration tests |

### Load Testing Scenarios

```typescript
describe("Load Testing", () => {
  test("handles 100 concurrent users", async () => {
    const loadTest = await runLoadTest({
      concurrent: 100,
      duration: "5m",
      scenarios: [
        { endpoint: "/api/customers", weight: 30 },
        { endpoint: "/api/invoices", weight: 40 },
        { endpoint: "/api/products", weight: 20 },
        { endpoint: "/api/greek/validate-afm", weight: 10 },
      ],
    });

    expect(loadTest.avgResponseTime).toBeLessThan(500);
    expect(loadTest.errorRate).toBeLessThan(0.01);
  });
});
```

---

## 🔧 TESTING INFRASTRUCTURE

### Test Environment Setup

```yaml
# Test Database Configuration
test_database:
  host: localhost
  port: 5432
  name: greek_erp_test
  fixtures:
    - greek_tax_offices.sql
    - sample_companies.sql
    - test_users.sql

# External Service Mocks
mock_services:
  aade_api:
    sandbox_mode: true
    mock_responses: true
  banking_apis:
    mock_transactions: true
  email_service:
    capture_emails: true
```

### Continuous Integration

```yaml
# GitHub Actions Testing Pipeline
name: Test Suite
on: [push, pull_request]

jobs:
  unit_tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Unit Tests
        run: |
          npm run test:unit
          pytest tests/unit/

  integration_tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: greek_erp_test
    steps:
      - name: Run Integration Tests
        run: |
          npm run test:integration
          pytest tests/integration/

  e2e_tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E Tests
        run: |
          npx playwright test
```

---

## 📊 TESTING METRICS & REPORTING

### Required Metrics

- **Code Coverage**: Minimum 90% for unit tests, 70% for integration tests
- **Test Execution Time**: Unit tests <5 minutes, Integration tests <15 minutes, E2E tests <30 minutes
- **Greek Compliance Coverage**: 100% of AADE workflows tested
- **Performance Benchmarks**: All targets met in CI/CD pipeline

### Test Reporting

- **Coverage Reports**: Istanbul/nyc for frontend, pytest-cov for backend
- **Performance Reports**: Lighthouse CI reports for each PR
- **Greek Compliance Reports**: Custom reports for AADE integration testing
- **Test Results**: Integration with GitHub PR status checks

This comprehensive testing specification ensures every feature has appropriate test coverage with special attention to Greek business requirements and compliance.
