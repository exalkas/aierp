# 🏢 Client Customization Examples - Enterprise Architecture

## Overview

The versioning system supports **two types** of client-specific customizations:

1. **Client-Specific Custom Modules** - Entire modules only for one client
2. **Client-Specific Module Customizations** - Modifications to existing modules only for one client

---

## 🚢 **Approach 1: Client-Specific Custom Modules**

**Example: ShippingCorp Vessel Management Module**

```typescript
// Custom module that exists ONLY for ShippingCorp
const shippingCorpVesselModule: CustomModule = {
  id: "shippingcorp-vessel-management",
  name: "Vessel Fleet Management",
  clientId: "shippingcorp",
  version: { major: 1, minor: 2, patch: 0 },

  // This module is completely separate from core
  isClientSpecific: true,
  basedOnCoreModule: null, // Not based on any core module

  features: [
    "vessel-registration",
    "crew-management",
    "port-scheduling",
    "maritime-compliance",
    "fuel-tracking",
    "route-optimization",
  ],

  // Greek maritime-specific features
  greekCompliance: {
    portAuthorities: ["Piraeus", "Thessaloniki", "Patras"],
    maritimeRegulations: ["Greek_Coast_Guard", "IMO"],
    vesselRegistry: "Greek_Ship_Registry",
  },

  // Performance isolation
  isolatedDatabase: true,
  dedicatedAPI: "/api/shippingcorp/vessels",

  // Version compatibility with platform
  platformCompatibility: "^2.1.0",
};

// How the system loads this
class ClientSpecificModuleManager {
  async loadClientModules(clientId: string): Promise<CustomModule[]> {
    const modules = await this.getClientModules(clientId);

    // Only ShippingCorp sees vessel management
    if (clientId === "shippingcorp") {
      modules.push(shippingCorpVesselModule);
    }

    return modules;
  }

  async checkModuleAccess(
    clientId: string,
    moduleId: string
  ): Promise<boolean> {
    const module = await this.getModule(moduleId);

    // Client-specific modules only visible to that client
    if (module.isClientSpecific) {
      return module.clientId === clientId;
    }

    // Core modules visible to everyone (based on subscription)
    return this.checkCoreModuleAccess(clientId, moduleId);
  }
}
```

---

## 🏪 **Approach 2: Client-Specific Module Customizations**

**Example: RestaurantChain CRM Customizations**

```typescript
// Customizations to the CORE CRM module, but only for RestaurantChain
const restaurantChainCRMCustomizations: ModuleCustomization = {
  id: "restaurantchain-crm-customizations",
  name: "Restaurant Chain CRM Customizations",
  clientId: "restaurantchain",
  version: { major: 2, minor: 0, patch: 0 },

  // This customizes the existing core CRM module
  isClientSpecific: true,
  basedOnCoreModule: "crm", // Extends core CRM v1.3.0

  customizations: {
    // Custom fields added to Customer entity
    customFields: {
      customer: [
        {
          id: "dietary_restrictions",
          name: "Dietary Restrictions",
          type: "multi-select",
          options: ["Vegetarian", "Vegan", "Gluten-Free", "Keto"],
        },
        {
          id: "loyalty_tier",
          name: "Loyalty Tier",
          type: "select",
          options: ["Bronze", "Silver", "Gold", "Platinum"],
        },
        {
          id: "favorite_locations",
          name: "Favorite Restaurant Locations",
          type: "multi-select-locations",
        },
      ],
    },

    // Custom business rules
    customRules: {
      loyalty_point_calculation: {
        logic: `
          if (customer.loyalty_tier === 'Platinum') {
            return order.amount * 0.05; // 5% back
          } else if (customer.loyalty_tier === 'Gold') {
            return order.amount * 0.03; // 3% back
          } else {
            return order.amount * 0.01; // 1% back
          }
        `,
        appliesTo: ["order_processing"],
      },
    },

    // Custom workflows
    customWorkflows: {
      vip_customer_onboarding: {
        steps: [
          { type: "assign_loyalty_tier", config: { defaultTier: "Gold" } },
          { type: "send_welcome_package", config: { includeVouchers: true } },
          { type: "schedule_manager_call", config: { priority: "high" } },
        ],
      },
    },

    // Custom UI views
    customViews: {
      customer_dashboard: {
        layout: "restaurant_layout",
        widgets: [
          "loyalty_points_widget",
          "favorite_orders_widget",
          "dietary_preferences_widget",
          "location_visits_widget",
        ],
      },
    },
  },

  // Performance settings
  cacheStrategy: "aggressive",
  isolatedQueries: true, // Separate query performance from other clients

  // Version compatibility
  platformCompatibility: "^2.1.0",
  coreModuleCompatibility: "^1.3.0", // Works with CRM v1.3.0+
};

// How the system applies these customizations
class ModuleCustomizationManager {
  async loadModuleForClient(
    moduleId: string,
    clientId: string
  ): Promise<Module> {
    // Start with core module
    const coreModule = await this.getCoreModule(moduleId);

    // Check for client-specific customizations
    const customizations = await this.getClientCustomizations(
      clientId,
      moduleId
    );

    if (customizations.length === 0) {
      // SME Path: Return core module as-is (~50ms)
      return coreModule;
    } else {
      // Enterprise Path: Merge customizations (~85ms)
      return this.mergeCustomizations(coreModule, customizations);
    }
  }

  private async mergeCustomizations(
    coreModule: Module,
    customizations: ModuleCustomization[]
  ): Promise<Module> {
    const customizedModule = { ...coreModule };

    for (const customization of customizations) {
      // Merge custom fields (~10ms)
      if (customization.customizations.customFields) {
        customizedModule.entities = this.mergeCustomFields(
          customizedModule.entities,
          customization.customizations.customFields
        );
      }

      // Merge custom rules (~15ms)
      if (customization.customizations.customRules) {
        customizedModule.businessRules = this.mergeCustomRules(
          customizedModule.businessRules,
          customization.customizations.customRules
        );
      }

      // Merge custom workflows (~10ms)
      if (customization.customizations.customWorkflows) {
        customizedModule.workflows = this.mergeCustomWorkflows(
          customizedModule.workflows,
          customization.customizations.customWorkflows
        );
      }

      // Merge custom views (~10ms)
      if (customization.customizations.customViews) {
        customizedModule.views = this.mergeCustomViews(
          customizedModule.views,
          customization.customizations.customViews
        );
      }
    }

    return customizedModule;
  }
}
```

---

## 🏛️ **Real-World Example: LawFirm Integration**

**Combination of both approaches:**

```typescript
// LawFirm has BOTH custom modules AND module customizations

// 1. Custom Module: Legal Case Management (only for LawFirm)
const lawFirmCaseModule: CustomModule = {
  id: "lawfirm-case-management",
  name: "Legal Case Management",
  clientId: "lawfirm",
  version: { major: 1, minor: 0, patch: 0 },
  isClientSpecific: true,
  basedOnCoreModule: null,
  features: [
    "case-tracking",
    "client-billing",
    "court-scheduling",
    "document-management",
    "time-tracking",
    "billing-integration",
  ],
};

// 2. CRM Customizations: Legal client fields (customizes core CRM)
const lawFirmCRMCustomizations: ModuleCustomization = {
  id: "lawfirm-crm-customizations",
  clientId: "lawfirm",
  basedOnCoreModule: "crm",
  customizations: {
    customFields: {
      customer: [
        {
          id: "case_type",
          name: "Primary Case Type",
          type: "select",
          options: ["Corporate", "Criminal", "Civil", "Family", "Immigration"],
        },
        {
          id: "retainer_amount",
          name: "Retainer Amount",
          type: "currency",
        },
        {
          id: "court_jurisdiction",
          name: "Court Jurisdiction",
          type: "text",
        },
      ],
    },
  },
};

// How LawFirm sees their system
const lawFirmModules = [
  // Core modules (everyone gets these)
  coreAccountingModule, // v1.2.0
  coreInvoicingModule, // v1.2.0

  // Customized core modules (only LawFirm sees the customizations)
  customizedCRMModule, // CRM v1.3.0 + LawFirm customizations

  // Custom modules (only LawFirm gets these)
  lawFirmCaseModule, // v1.0.0
];
```

---

## 📊 **Version Management for Both Approaches**

```typescript
// Enhanced version manager handles both approaches
class EnhancedVersionManager extends CoreVersionManager {
  // Track custom modules per client
  clientCustomModules = new Map<string, Map<string, CustomModule>>();

  // Track module customizations per client
  clientModuleCustomizations = new Map<
    string,
    Map<string, ModuleCustomization[]>
  >();

  async getClientModuleInventory(clientId: string): Promise<ModuleInventory> {
    return {
      // Core modules (everyone gets these based on subscription)
      coreModules: await this.getCoreModulesForClient(clientId),

      // Client-specific custom modules
      customModules: this.clientCustomModules.get(clientId) || new Map(),

      // Customizations to core modules
      moduleCustomizations:
        this.clientModuleCustomizations.get(clientId) || new Map(),
    };
  }

  async checkUpgradeImpact(
    clientId: string,
    from: Version,
    to: Version
  ): Promise<UpgradeImpact> {
    const inventory = await this.getClientModuleInventory(clientId);
    const impact: UpgradeImpact = {
      coreModuleImpact: [],
      customModuleImpact: [],
      customizationImpact: [],
      migrationRequired: false,
    };

    // Check impact on custom modules
    for (const [moduleId, customModule] of inventory.customModules) {
      const compatible = this.isCustomModuleCompatible(customModule, to);
      if (!compatible) {
        impact.customModuleImpact.push({
          moduleId,
          issue: "Platform compatibility issue",
          migrationRequired: true,
        });
      }
    }

    // Check impact on module customizations
    for (const [moduleId, customizations] of inventory.moduleCustomizations) {
      for (const customization of customizations) {
        const compatible = this.isCustomizationCompatible(customization, to);
        if (!compatible) {
          impact.customizationImpact.push({
            customizationId: customization.id,
            moduleId,
            issue: "Customization needs migration",
            migrationRequired: true,
          });
        }
      }
    }

    impact.migrationRequired =
      impact.customModuleImpact.some((i) => i.migrationRequired) ||
      impact.customizationImpact.some((i) => i.migrationRequired);

    return impact;
  }
}
```

---

## 🎯 **Key Benefits of Both Approaches**

### **Custom Modules (Approach 1):**

✅ **Complete isolation** - No impact on other clients
✅ **Independent versioning** - ShippingCorp can upgrade vessel module independently  
✅ **Dedicated performance** - Isolated database and API endpoints
✅ **Full feature control** - Everything custom-built for specific needs

### **Module Customizations (Approach 2):**

✅ **Leverages core features** - Benefits from core CRM improvements
✅ **Easier maintenance** - Core updates automatically flow through
✅ **Performance optimized** - Cached custom fields/rules (~10-15ms)
✅ **Gradual customization** - Start simple, add complexity over time

## 🚀 **Your Enterprise Strategy**

**SME Clients**: Core modules only (fast ~50ms)
**Enterprise Clients**: Core modules + customizations + custom modules (~85ms)
**Premium Enterprise**: Completely custom modules + extensive customizations

This gives you **unlimited customization possibilities** while maintaining performance and upgrade safety! 🎯
