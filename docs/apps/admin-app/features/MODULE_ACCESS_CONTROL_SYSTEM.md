# 🛡️ Module Access Control System - Admin App

## Overview

Sophisticated system to control which modules are available to which clients, with multiple permission levels, bulk operations, and audit trails.

---

## 🏗️ **Multi-Level Access Control Architecture**

### **1. Permission Hierarchy**

```typescript
// Permission levels for module access control
enum AdminRole {
  SUPER_ADMIN = "super_admin",           // Can do everything
  PLATFORM_ADMIN = "platform_admin",    // Can manage core modules
  CLIENT_ADMIN = "client_admin",         // Can only manage their client
  MODULE_ADMIN = "module_admin"          // Can manage specific modules
}

enum ModuleAccessLevel {
  FORBIDDEN = "forbidden",               // Cannot see or use
  READ_ONLY = "read_only",              // Can see but not modify
  STANDARD = "standard",                // Full access to standard features
  CUSTOMIZABLE = "customizable",        // Can add customizations
  FULL_CONTROL = "full_control"         // Can create custom modules
}

interface ModulePermission {
  clientId: string;
  moduleId: string;
  accessLevel: ModuleAccessLevel;
  customizations: CustomizationPermission[];
  expiresAt?: Date;
  assignedBy: string;
  assignedAt: Date;
  notes?: string;
}

interface CustomizationPermission {
  type: "custom_fields" | "custom_rules" | "custom_workflows" | "custom_views";
  allowed: boolean;
  restrictions?: string[];
}
```

### **2. Module Assignment Templates**

```typescript
// Pre-configured templates for different business types
interface ModuleTemplate {
  id: string;
  name: string;
  description: string;
  targetIndustry: string[];
  modules: ModuleTemplateItem[];
  customizationLimits: CustomizationLimits;
}

interface ModuleTemplateItem {
  moduleId: string;
  accessLevel: ModuleAccessLevel;
  required: boolean;
  customizations: CustomizationPermission[];
}

// Predefined templates
const moduleTemplates: ModuleTemplate[] = [
  {
    id: "sme_basic",
    name: "SME Basic Package", 
    description: "Essential modules for small businesses",
    targetIndustry: ["retail", "services", "general"],
    modules: [
      { moduleId: "crm", accessLevel: ModuleAccessLevel.STANDARD, required: true, customizations: [] },
      { moduleId: "invoicing", accessLevel: ModuleAccessLevel.STANDARD, required: true, customizations: [] },
      { moduleId: "accounting", accessLevel: ModuleAccessLevel.READ_ONLY, required: false, customizations: [] }
    ],
    customizationLimits: {
      maxCustomFields: 5,
      maxCustomRules: 2,
      maxCustomWorkflows: 1
    }
  },
  {
    id: "enterprise_shipping",
    name: "Enterprise Shipping Package",
    description: "Full shipping industry solution", 
    targetIndustry: ["shipping", "logistics", "maritime"],
    modules: [
      { moduleId: "crm", accessLevel: ModuleAccessLevel.CUSTOMIZABLE, required: true, customizations: [
        { type: "custom_fields", allowed: true },
        { type: "custom_rules", allowed: true }
      ]},
      { moduleId: "vessel_management", accessLevel: ModuleAccessLevel.FULL_CONTROL, required: true, customizations: [
        { type: "custom_fields", allowed: true },
        { type: "custom_rules", allowed: true },
        { type: "custom_workflows", allowed: true },
        { type: "custom_views", allowed: true }
      ]}
    ],
    customizationLimits: {
      maxCustomFields: 50,
      maxCustomRules: 25,
      maxCustomWorkflows: 10
    }
  }
];
```

---

## 🎛️ **Admin App Interface Design**

### **1. Module Management Dashboard**

```typescript
// Admin App: Module Management Dashboard
export const ModuleManagementDashboard: React.FC = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [permissions, setPermissions] = useState<ModulePermission[]>([]);

  return (
    <div className="module-management-dashboard">
      <div className="dashboard-header">
        <h1>Module Access Control</h1>
        <div className="quick-actions">
          <button onClick={() => openBulkAssignmentModal()}>
            Bulk Assignment
          </button>
          <button onClick={() => openTemplateManager()}>
            Manage Templates
          </button>
          <button onClick={() => exportPermissions()}>
            Export Permissions
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Client Selection */}
        <div className="client-selector">
          <h3>Select Client</h3>
          <ClientSelector 
            clients={clients}
            selectedClient={selectedClient}
            onSelect={setSelectedClient}
          />
        </div>

        {selectedClient && (
          <div className="module-permissions">
            <ModulePermissionMatrix
              client={selectedClient}
              modules={modules}
              permissions={permissions}
              onPermissionChange={handlePermissionChange}
            />
          </div>
        )}
      </div>
    </div>
  );
};
```

### **2. Module Permission Matrix**

```typescript
// Interactive matrix showing all modules vs clients
export const ModulePermissionMatrix: React.FC<{
  client: Client;
  modules: Module[];
  permissions: ModulePermission[];
  onPermissionChange: (permission: ModulePermission) => void;
}> = ({ client, modules, permissions, onPermissionChange }) => {
  
  const getPermissionLevel = (moduleId: string): ModuleAccessLevel => {
    const permission = permissions.find(p => 
      p.clientId === client.id && p.moduleId === moduleId
    );
    return permission?.accessLevel || ModuleAccessLevel.FORBIDDEN;
  };

  const updatePermission = (moduleId: string, accessLevel: ModuleAccessLevel) => {
    const permission: ModulePermission = {
      clientId: client.id,
      moduleId,
      accessLevel,
      customizations: getDefaultCustomizations(accessLevel),
      assignedBy: getCurrentUser().id,
      assignedAt: new Date()
    };
    onPermissionChange(permission);
  };

  return (
    <div className="permission-matrix">
      <div className="matrix-header">
        <h3>Module Permissions for {client.name}</h3>
        <div className="client-info">
          <span>Industry: {client.industry}</span>
          <span>Plan: {client.subscriptionPlan}</span>
          <span>Users: {client.userCount}</span>
        </div>
      </div>

      <div className="matrix-grid">
        <table className="permission-table">
          <thead>
            <tr>
              <th>Module</th>
              <th>Current Access</th>
              <th>Actions</th>
              <th>Customizations</th>
              <th>Last Modified</th>
            </tr>
          </thead>
          <tbody>
            {modules.map(module => {
              const currentLevel = getPermissionLevel(module.id);
              const permission = permissions.find(p => 
                p.clientId === client.id && p.moduleId === module.id
              );

              return (
                <tr key={module.id} className={`access-level-${currentLevel}`}>
                  <td>
                    <div className="module-info">
                      <span className="module-name">{module.name}</span>
                      <span className="module-type">{module.type}</span>
                    </div>
                  </td>
                
                  <td>
                    <AccessLevelBadge level={currentLevel} />
                  </td>
                
                  <td>
                    <AccessLevelSelector
                      currentLevel={currentLevel}
                      availableLevels={getAvailableLevels(client, module)}
                      onChange={(level) => updatePermission(module.id, level)}
                    />
                  </td>
                
                  <td>
                    {currentLevel !== ModuleAccessLevel.FORBIDDEN && (
                      <CustomizationManager
                        permission={permission}
                        onUpdate={onPermissionChange}
                      />
                    )}
                  </td>
                
                  <td>
                    {permission && (
                      <div className="last-modified">
                        <span>{formatDate(permission.assignedAt)}</span>
                        <span>by {permission.assignedBy}</span>
                      </div>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
```

### **3. Bulk Operations Interface**

```typescript
// Bulk assignment for multiple clients
export const BulkModuleAssignment: React.FC = () => {
  const [selectedClients, setSelectedClients] = useState<string[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<ModuleTemplate | null>(null);
  const [customPermissions, setCustomPermissions] = useState<ModulePermission[]>([]);

  const applyBulkAssignment = async () => {
    const assignment: BulkAssignment = {
      clientIds: selectedClients,
      template: selectedTemplate,
      customPermissions,
      assignedBy: getCurrentUser().id,
      assignedAt: new Date()
    };

    await bulkAssignmentService.execute(assignment);
  };

  return (
    <div className="bulk-assignment-modal">
      <div className="modal-header">
        <h2>Bulk Module Assignment</h2>
      </div>

      <div className="assignment-steps">
        {/* Step 1: Select Clients */}
        <div className="step">
          <h3>1. Select Clients</h3>
          <ClientMultiSelect
            clients={availableClients}
            selected={selectedClients}
            onChange={setSelectedClients}
            filters={{
              industry: true,
              subscriptionPlan: true,
              userCount: true
            }}
          />
        </div>

        {/* Step 2: Choose Template or Custom */}
        <div className="step">
          <h3>2. Assignment Method</h3>
          <div className="assignment-method">
            <div className="method-option">
              <input 
                type="radio" 
                id="template" 
                name="method" 
                onChange={() => setAssignmentMethod('template')}
              />
              <label htmlFor="template">Use Template</label>
              <TemplateSelector 
                templates={moduleTemplates}
                selected={selectedTemplate}
                onChange={setSelectedTemplate}
              />
            </div>
          
            <div className="method-option">
              <input 
                type="radio" 
                id="custom" 
                name="method" 
                onChange={() => setAssignmentMethod('custom')}
              />
              <label htmlFor="custom">Custom Assignment</label>
              <CustomPermissionBuilder
                permissions={customPermissions}
                onChange={setCustomPermissions}
              />
            </div>
          </div>
        </div>

        {/* Step 3: Preview and Apply */}
        <div className="step">
          <h3>3. Preview Changes</h3>
          <BulkAssignmentPreview
            clients={selectedClients}
            assignment={selectedTemplate || customPermissions}
          />
        
          <div className="apply-actions">
            <button 
              onClick={applyBulkAssignment}
              className="btn-primary"
            >
              Apply to {selectedClients.length} Clients
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
```

---

## 🔄 **Backend API & Business Logic**

### **1. Module Permission Service**

```typescript
// Backend service for managing module permissions
export class ModulePermissionService {
  
  async getClientPermissions(clientId: string): Promise<ModulePermission[]> {
    return await this.db.modulePermissions.findMany({
      where: { clientId },
      include: { module: true, assignedByUser: true }
    });
  }

  async updatePermission(permission: ModulePermission): Promise<void> {
    // Validate permission based on admin role
    await this.validatePermissionUpdate(permission);
  
    // Check subscription limits
    await this.checkSubscriptionLimits(permission);
  
    // Update permission
    await this.db.modulePermissions.upsert({
      where: {
        clientId_moduleId: {
          clientId: permission.clientId,
          moduleId: permission.moduleId
        }
      },
      update: permission,
      create: permission
    });

    // Log the change
    await this.auditService.logPermissionChange(permission);
  
    // Invalidate client cache
    await this.cacheService.invalidateClientModules(permission.clientId);
  }

  async bulkAssignPermissions(assignment: BulkAssignment): Promise<BulkAssignmentResult> {
    const results: BulkAssignmentResult = {
      successful: [],
      failed: [],
      warnings: []
    };

    for (const clientId of assignment.clientIds) {
      try {
        // Apply template or custom permissions
        const permissions = assignment.template 
          ? this.generatePermissionsFromTemplate(clientId, assignment.template)
          : assignment.customPermissions.map(p => ({ ...p, clientId }));

        for (const permission of permissions) {
          await this.updatePermission(permission);
          results.successful.push({ clientId, moduleId: permission.moduleId });
        }
      } catch (error) {
        results.failed.push({ 
          clientId, 
          error: error.message 
        });
      }
    }

    return results;
  }

  private async validatePermissionUpdate(permission: ModulePermission): Promise<void> {
    const currentUser = getCurrentUser();
  
    // Super admin can do anything
    if (currentUser.role === AdminRole.SUPER_ADMIN) {
      return;
    }
  
    // Platform admin can manage core modules
    if (currentUser.role === AdminRole.PLATFORM_ADMIN) {
      const module = await this.getModule(permission.moduleId);
      if (module.type !== 'core') {
        throw new Error('Platform admin can only manage core modules');
      }
      return;
    }
  
    // Client admin can only manage their own client
    if (currentUser.role === AdminRole.CLIENT_ADMIN) {
      if (permission.clientId !== currentUser.clientId) {
        throw new Error('Client admin can only manage their own client');
      }
      return;
    }
  
    // Module admin can only manage specific modules
    if (currentUser.role === AdminRole.MODULE_ADMIN) {
      if (!currentUser.managedModules.includes(permission.moduleId)) {
        throw new Error('Module admin can only manage assigned modules');
      }
      return;
    }
  
    throw new Error('Insufficient permissions');
  }

  private async checkSubscriptionLimits(permission: ModulePermission): Promise<void> {
    const client = await this.getClient(permission.clientId);
    const subscription = await this.getSubscription(client.subscriptionId);
  
    // Check if module is allowed in subscription
    if (!subscription.allowedModules.includes(permission.moduleId)) {
      throw new Error(`Module ${permission.moduleId} not allowed in ${subscription.plan} plan`);
    }
  
    // Check customization limits
    if (permission.accessLevel === ModuleAccessLevel.CUSTOMIZABLE || 
        permission.accessLevel === ModuleAccessLevel.FULL_CONTROL) {
    
      const currentCustomizations = await this.getClientCustomizations(permission.clientId);
      const limits = subscription.customizationLimits;
    
      if (currentCustomizations.customFields >= limits.maxCustomFields) {
        throw new Error('Custom field limit exceeded');
      }
    
      if (currentCustomizations.customRules >= limits.maxCustomRules) {
        throw new Error('Custom rule limit exceeded');
      }
    }
  }
}
```

### **2. Real-Time Permission Enforcement**

```typescript
// Middleware to check module access in real-time
export const moduleAccessMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  const { clientId, moduleId } = req.params;
  const { userId } = req.user;
  
  // Get user's client
  const user = await userService.getUser(userId);
  if (user.clientId !== clientId) {
    return res.status(403).json({ error: 'Access denied to client data' });
  }
  
  // Check module permission
  const permission = await modulePermissionService.getPermission(clientId, moduleId);
  if (!permission || permission.accessLevel === ModuleAccessLevel.FORBIDDEN) {
    return res.status(403).json({ error: 'Module access denied' });
  }
  
  // Check if permission expired
  if (permission.expiresAt && permission.expiresAt < new Date()) {
    return res.status(403).json({ error: 'Module access expired' });
  }
  
  // Add permission context to request
  req.modulePermission = permission;
  next();
};
```

---

## 📊 **Advanced Features**

### **1. Permission Templates & Inheritance**

```typescript
// Template inheritance system
interface PermissionTemplate {
  id: string;
  name: string;
  parentTemplate?: string;          // Inherit from another template
  overrides: ModulePermission[];    // Override parent permissions
  conditions: TemplateCondition[];  // When to apply this template
}

interface TemplateCondition {
  field: "industry" | "userCount" | "revenue" | "region";
  operator: "equals" | "greater_than" | "less_than" | "in";
  value: any;
}

// Auto-apply templates based on client characteristics
export const autoApplyTemplates = async (client: Client): Promise<void> => {
  const applicableTemplates = await getApplicableTemplates(client);
  
  for (const template of applicableTemplates) {
    await applyTemplate(client.id, template);
  }
};
```

### **2. Audit Trail & Compliance**

```typescript
// Complete audit trail for permissions
interface PermissionAuditLog {
  id: string;
  clientId: string;
  moduleId: string;
  action: "granted" | "revoked" | "modified" | "expired";
  previousPermission?: ModulePermission;
  newPermission?: ModulePermission;
  adminUserId: string;
  timestamp: Date;
  reason?: string;
  ipAddress: string;
  userAgent: string;
}

export const PermissionAuditTrail: React.FC<{ clientId: string }> = ({ clientId }) => {
  const [auditLogs, setAuditLogs] = useState<PermissionAuditLog[]>([]);

  return (
    <div className="audit-trail">
      <h3>Permission Change History</h3>
      <div className="audit-filters">
        <DateRangePicker onChange={filterByDate} />
        <ModuleFilter onChange={filterByModule} />
        <ActionFilter onChange={filterByAction} />
      </div>
    
      <div className="audit-logs">
        {auditLogs.map(log => (
          <div key={log.id} className="audit-entry">
            <div className="audit-header">
              <span className={`action-badge ${log.action}`}>{log.action}</span>
              <span className="timestamp">{formatDateTime(log.timestamp)}</span>
              <span className="admin">{log.adminUserId}</span>
            </div>
            <div className="audit-details">
              <span>Module: {log.moduleId}</span>
              {log.previousPermission && (
                <span>From: {log.previousPermission.accessLevel}</span>
              )}
              {log.newPermission && (
                <span>To: {log.newPermission.accessLevel}</span>
              )}
            </div>
            {log.reason && (
              <div className="audit-reason">Reason: {log.reason}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## 🎯 **Key Benefits of This System**

### **✅ Multi-Level Control:**

- Super Admin: Complete control
- Platform Admin: Core modules only
- Client Admin: Their client only
- Module Admin: Specific modules only

### **✅ Scalability:**

- Bulk operations for multiple clients
- Template system for common patterns
- Inheritance and overrides
- Auto-application based on client characteristics

### **✅ Enterprise Features:**

- Complete audit trail
- Permission expiration
- Subscription limit enforcement
- Real-time access control

### **✅ User Experience:**

- Visual permission matrix
- Template-based assignment
- Bulk operations with preview
- Rich filtering and search

## 🚀 **Implementation Strategy**

1. **Start with basic CRUD** in admin app
2. **Add permission matrix** for visual management
3. **Implement templates** for common patterns
4. **Add bulk operations** for scalability
5. **Build audit trail** for compliance
6. **Add advanced features** as needed

This gives you **enterprise-grade module access control** that scales from small setups to large multi-client deployments! 🎯
