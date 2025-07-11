# Main Engine Architecture - Technical Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Priority**: Critical - Core Platform Foundation
- **Dependencies**: All Modules

## Executive Summary

The Main Engine Architecture defines the **core platform foundation** that enables both cloud SAAS and desktop deployment models while providing exceptional customization capabilities. This hybrid architecture balances performance, flexibility, and deployment simplicity.

## 1. Architectural Decision: Modular Monolith + Microservice Capability

### 1.1 Why NOT Pure Microservices?

**Desktop Deployment Challenges:**

- Complex service orchestration on weak machines
- Resource overhead of multiple processes
- Network communication latency
- Difficult installation and maintenance

**Better Approach: Modular Monolith with Service Boundaries**

```typescript
interface MainEngine {
  // Core engine components
  authorizationEngine: AuthorizationEngine;
  dataEngine: DataEngine;
  customizationEngine: CustomizationEngine;
  integrationEngine: IntegrationEngine;

  // Deployment adapters
  cloudAdapter: CloudDeploymentAdapter;
  desktopAdapter: DesktopDeploymentAdapter;

  // Module management
  moduleManager: ModuleManager;
  pluginSystem: PluginSystem;
}
```

## 2. Core Engine Components

### 2.1 Authorization & Licensing Engine (Central Control)

**The Heart of the System:**

```typescript
class CoreAuthorizationEngine {
  // Module access control
  checkModuleAccess(userId: string, moduleId: string): AccessResult;

  // Feature flags and customization
  isFeatureEnabled(feature: string, context: Context): boolean;

  // Subscription validation
  validateSubscription(companyId: string): SubscriptionStatus;

  // Greek compliance enforcement
  enforceGreekCompliance(operation: BusinessOperation): ComplianceResult;
}
```

**Why This is the "Main Engine":**

- Controls access to ALL functionality
- Manages customization and configuration
- Enforces business rules and compliance
- Enables flexible subscription models

### 2.2 Customization Engine (High Flexibility)

**EspoCRM-Style Customization:**

```typescript
class CustomizationEngine {
  // Dynamic entity creation
  createEntity(definition: EntityDefinition): Promise<EntityResult>;

  // Custom field management
  addCustomField(entityId: string, field: FieldDefinition): Promise<void>;

  // Workflow engine
  createWorkflow(workflow: WorkflowDefinition): Promise<WorkflowResult>;

  // Custom views and layouts
  createCustomView(view: ViewDefinition): Promise<ViewResult>;

  // Business rule engine
  defineBusinessRule(rule: BusinessRule): Promise<RuleResult>;
}
```

### 2.3 Data Engine (Performance Optimized)

**Unified Data Layer:**

```typescript
class DataEngine {
  // Database abstraction
  cloud: PostgreSQLAdapter;
  desktop: SQLiteAdapter;

  // Caching layer
  cache: RedisAdapter | MemoryCache;

  // Query optimization
  optimizeQuery(query: Query): OptimizedQuery;

  // Data synchronization (desktop <-> cloud)
  syncData(syncRequest: SyncRequest): Promise<SyncResult>;
}
```

## 3. Deployment Architecture

### 3.1 Cloud Deployment (Full Microservices)

```yaml
# Cloud: Full microservices with container orchestration
version: "3.8"
services:
  # Core engine
  main-engine:
    image: erp-main-engine:latest
    environment:
      - DEPLOYMENT_MODE=cloud
      - DATABASE_TYPE=postgresql

  # Specialized services
  aade-service:
    image: erp-aade-service:latest

  banking-service:
    image: erp-banking-service:latest

  # Message queue
  redis:
    image: redis:7-alpine

  # Database
  postgres:
    image: postgres:16
```

### 3.2 Desktop Deployment (Local Web Server)

**Local Web Server + Browser UI:**

```typescript
class DesktopMainEngine {
  constructor() {
    // All services embedded in single process
    this.authEngine = new AuthorizationEngine();
    this.dataEngine = new DataEngine({
      database: new SQLiteAdapter(),
      cache: new MemoryCache(),
    });
    this.customizationEngine = new CustomizationEngine();

    // Greek compliance services
    this.aadeService = new AADEService();
    this.bankingService = new BankingService();
  }

  async start() {
    // Start local web server (same as cloud, but with SQLite)
    this.server = new LocalWebServer(this);
    await this.server.listen(8080);

    console.log("🚀 Greek ERP Server running at http://localhost:8080");

    // Auto-open browser to local app
    await this.openDefaultBrowser("http://localhost:8080");

    // Optional: System tray for server management
    this.setupSystemTray();
  }

  private async openDefaultBrowser(url: string): Promise<void> {
    const { exec } = require("child_process");
    const command =
      process.platform === "win32"
        ? "start"
        : process.platform === "darwin"
        ? "open"
        : "xdg-open";
    exec(`${command} ${url}`);
  }

  private setupSystemTray(): void {
    // System tray for easy server start/stop
    this.trayIcon = new SystemTrayManager({
      icon: "assets/icon.png",
      menu: [
        {
          label: "Open Greek ERP",
          click: () => this.openDefaultBrowser("http://localhost:8080"),
        },
        { label: "Stop Server", click: () => this.stop() },
        { label: "Exit", click: () => process.exit(0) },
      ],
    });
  }
}
```

## 4. Desktop Installation Strategy (Weak Machine Support)

### 4.1 Lightweight Installation Package

**Local Web Server Executable:**

```nsi
# NSIS installer - web server approach
!define APP_NAME "Greek ERP"
!define APP_SIZE "80MB"  # Much smaller without UI framework

Section "Main Application"
    # Web server executable
    File "greek-erp-server.exe"

    # Web UI assets
    File /r "www\*.*"

    # Embedded SQLite database
    CreateDirectory "$LOCALAPPDATA\GreekERP\data"

    # Desktop shortcut (launches server + opens browser)
    CreateShortcut "$DESKTOP\Greek ERP.lnk" "$INSTDIR\greek-erp-server.exe"

    # Start menu entry
    CreateShortcut "$SMPROGRAMS\Greek ERP.lnk" "$INSTDIR\greek-erp-server.exe"

    # System service registration (optional)
    ExecWait '"$INSTDIR\greek-erp-server.exe" --install-service'
SectionEnd
```

**Installation Benefits:**

- ✅ **Much smaller**: ~80MB vs 150MB (no Electron/Tauri overhead)
- ✅ **Faster startup**: Direct web server launch
- ✅ **Better performance**: Native browser rendering
- ✅ **Easy updates**: Replace web assets without reinstalling
- ✅ **Familiar UI**: Same interface as cloud version

### 4.2 Resource Optimization for Weak Machines

**Memory Management:**

```typescript
class ResourceOptimizer {
  // Lazy loading of modules
  loadModule(moduleId: string): Promise<Module> {
    if (!this.loadedModules.has(moduleId)) {
      this.loadedModules.set(moduleId, await import(`./modules/${moduleId}`));
    }
    return this.loadedModules.get(moduleId);
  }

  // Memory cleanup
  unloadInactiveModules(): void {
    const inactive = this.getInactiveModules();
    inactive.forEach((module) => this.unloadModule(module));
  }

  // Database optimization
  optimizeForLowMemory(): void {
    // Use smaller cache sizes
    this.dataEngine.setCacheSize(50 * 1024 * 1024); // 50MB max

    // Enable SQLite memory-mapped I/O
    this.dataEngine.enableMMAP(true);

    // Use WAL mode for better concurrency
    this.dataEngine.setJournalMode("WAL");
  }
}
```

## 5. Customization Architecture

### 5.1 Plugin System for Maximum Flexibility

**Hot-Pluggable Architecture:**

```typescript
interface Plugin {
  id: string;
  version: string;
  dependencies: string[];

  // Lifecycle hooks
  onInstall(): Promise<void>;
  onEnable(): Promise<void>;
  onDisable(): Promise<void>;
  onUninstall(): Promise<void>;

  // Custom functionality
  getCustomEntities(): EntityDefinition[];
  getCustomFields(): FieldDefinition[];
  getCustomWorkflows(): WorkflowDefinition[];
  getCustomReports(): ReportDefinition[];
}

class PluginManager {
  // Plugin lifecycle
  installPlugin(pluginPackage: PluginPackage): Promise<InstallResult>;
  enablePlugin(pluginId: string): Promise<void>;
  disablePlugin(pluginId: string): Promise<void>;

  // Dependency management
  resolveDependencies(pluginId: string): Promise<Plugin[]>;
  validateCompatibility(plugin: Plugin): Promise<CompatibilityResult>;
}
```

### 5.2 Configuration Management

**Highly Configurable System:**

```typescript
class ConfigurationEngine {
  // Company-specific configuration
  companyConfig: CompanyConfiguration;

  // User preferences
  userPreferences: UserPreferences;

  // Module-specific settings
  moduleSettings: Map<string, ModuleSettings>;

  // Industry customizations
  industryProfiles: Map<Industry, IndustryProfile>;

  // Greek localization
  greekLocalizations: GreekLocalizationSettings;
}

interface CompanyConfiguration {
  // Business rules
  businessRules: BusinessRule[];

  // Custom workflows
  workflows: Workflow[];

  // UI customizations
  branding: BrandingSettings;
  layouts: LayoutConfiguration[];

  // Integration settings
  integrations: IntegrationSettings;

  // Compliance settings
  compliance: ComplianceSettings;
}
```

## 6. Performance Architecture

### 6.1 Caching Strategy

```typescript
class CacheManager {
  // Multi-level caching
  l1Cache: MemoryCache; // In-memory for frequent data
  l2Cache: DiskCache; // Local disk for session data
  l3Cache: CloudCache; // Cloud storage for shared data

  async get<T>(key: string): Promise<T | null> {
    // Try L1 first (fastest)
    let result = await this.l1Cache.get<T>(key);
    if (result) return result;

    // Try L2 (medium speed)
    result = await this.l2Cache.get<T>(key);
    if (result) {
      await this.l1Cache.set(key, result);
      return result;
    }

    // Try L3 (cloud - only if online)
    if (this.isOnline()) {
      result = await this.l3Cache.get<T>(key);
      if (result) {
        await this.l2Cache.set(key, result);
        await this.l1Cache.set(key, result);
      }
    }

    return result;
  }
}
```

### 6.2 Database Optimization

**SQLite for Desktop Performance:**

```sql
-- Desktop database optimization
PRAGMA journal_mode = WAL;         -- Better concurrency
PRAGMA synchronous = NORMAL;       -- Balanced safety/performance
PRAGMA cache_size = 10000;         -- 40MB cache
PRAGMA temp_store = MEMORY;        -- In-memory temporary tables
PRAGMA mmap_size = 268435456;      -- 256MB memory mapping

-- Indexing strategy
CREATE INDEX CONCURRENTLY idx_customers_search
ON customers USING gin(to_tsvector('greek', company_name));

CREATE INDEX idx_invoices_date_customer
ON invoices(issue_date DESC, customer_id);
```

## 7. Inter-Service Communication

### 7.1 Internal Event Bus

```typescript
class EventBus {
  // Internal messaging for modular monolith
  private subscribers: Map<string, EventHandler[]> = new Map();

  subscribe(event: string, handler: EventHandler): void {
    if (!this.subscribers.has(event)) {
      this.subscribers.set(event, []);
    }
    this.subscribers.get(event)!.push(handler);
  }

  async publish(event: string, data: any): Promise<void> {
    const handlers = this.subscribers.get(event) || [];

    // Async execution for non-blocking
    await Promise.all(handlers.map((handler) => handler(data)));
  }
}

// Usage across modules
class CRMModule {
  constructor(private eventBus: EventBus) {
    // Listen for relevant events
    this.eventBus.subscribe("customer.created", this.onCustomerCreated);
    this.eventBus.subscribe("invoice.paid", this.onInvoicePaid);
  }

  async createCustomer(data: CustomerData): Promise<Customer> {
    const customer = await this.customerRepository.create(data);

    // Notify other modules
    await this.eventBus.publish("customer.created", customer);

    return customer;
  }
}
```

## 8. Security Architecture

### 8.1 Unified Security Model

```typescript
class SecurityEngine {
  // Single security context for all modules
  authenticate(credentials: Credentials): Promise<AuthResult>;
  authorize(user: User, resource: Resource, action: Action): Promise<boolean>;

  // Desktop-specific security
  encryptLocalData(data: any): Promise<EncryptedData>;
  validateApplicationIntegrity(): Promise<IntegrityResult>;

  // License validation
  validateLicense(): Promise<LicenseStatus>;
  enforceUsageLimits(): Promise<EnforcementResult>;
}
```

## 9. Implementation Recommendations

### 9.1 **Phase 0: Core Engine Foundation (Months 1-3)**

```typescript
// Implementation priority
1. Authorization & Licensing Engine    // Critical foundation
2. Data Engine & Caching              // Performance foundation
3. Plugin System                       // Customization foundation
4. Desktop Deployment Framework        // Deployment capability
```

### 9.2 **Technology Stack Recommendations**

**Desktop Version (Local Web Server):**

- **Backend**: Node.js/Python FastAPI server
- **Database**: SQLite with encryption
- **Frontend**: React/Next.js (same as cloud)
- **Web Server**: Express.js or built-in server
- **Size**: ~80MB total installation
- **Browser**: User's default browser (Chrome, Firefox, Edge)

**Cloud Version (Full Web Application):**

- **Orchestration**: Docker + Kubernetes
- **Database**: PostgreSQL with Redis
- **Frontend**: Next.js with SSR
- **Backend**: Node.js/Python FastAPI
- **Scalability**: Horizontal scaling

**Shared Components (100% Code Reuse):**

- **UI Components**: Same React components for both
- **Business Logic**: Identical API layer and services
- **Database Models**: Same ORM/schema definitions
- **Authentication**: Same JWT/security implementation

### 9.3 **Development Strategy**

1. **Start with Desktop**: Simpler deployment model
2. **Build Modular**: Each module as self-contained unit
3. **Cloud Adaptation**: Extend desktop modules to cloud
4. **Shared Codebase**: 95% code reuse between deployments

## 10. Success Metrics

### Performance Targets

- **Desktop Startup**: <3 seconds (web server + browser launch)
- **Memory Usage**: <256MB RAM for server + browser handles UI
- **Database Size**: <2GB for typical SME
- **Installation Size**: <80MB total package (no UI framework overhead)

### Customization Targets

- **Entity Creation**: Runtime custom entities in <30 seconds
- **Workflow Setup**: Visual workflow builder
- **Plugin Installation**: One-click plugin deployment
- **Configuration Changes**: No restart required

---

**Key Advantages of This Architecture:**

✅ **Desktop Friendly**: Lightweight web server, minimal resources  
✅ **Highly Customizable**: Plugin system + dynamic entities  
✅ **Cloud Scalable**: Can expand to microservices  
✅ **Easy Installation**: Simple web server executable  
✅ **Shared Codebase**: 100% UI/logic reuse between deployments  
✅ **Performance Optimized**: Multi-level caching + native browser rendering  
✅ **Familiar Experience**: Same UI/UX as cloud version  
✅ **Easy Updates**: Update web assets without reinstalling  
✅ **Browser Compatibility**: Works with any modern browser  
✅ **Development Efficiency**: Single codebase for both deployments

## 🌟 **Web App Approach Benefits:**

### **For Users:**

- 🖥️ **Familiar Interface**: Same experience as cloud version
- ⚡ **Better Performance**: Native browser rendering
- 🔄 **Easy Updates**: Just refresh browser for updates
- 📱 **Multi-Device**: Access from any device on local network
- 🌐 **No Browser Dependency**: Works with user's preferred browser

### **For Development:**

- 📝 **Single Codebase**: 100% code reuse between cloud/desktop
- 🚀 **Faster Development**: No platform-specific UI code
- 🔧 **Easier Debugging**: Standard web dev tools
- 📦 **Smaller Package**: No UI framework bundled
- 🛠️ **Standard Tools**: Use existing web development stack

### **For Deployment:**

- 💿 **Smaller Installation**: ~80MB vs 150MB+ for desktop frameworks
- ⚙️ **Simple Service**: Can run as Windows service for automatic startup
- 🔧 **Easy Maintenance**: Update web assets independently
- 🌐 **Network Access**: Other devices can connect to local server
- 🔒 **Security**: Browser sandboxing + server-side validation

This architecture gives you the **best of both worlds**: simplicity for desktop deployment and scalability for cloud growth, with maximum code reuse and familiar web technologies.
