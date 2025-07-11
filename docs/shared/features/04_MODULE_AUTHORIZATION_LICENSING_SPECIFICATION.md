# Module Authorization & Licensing Engine - Technical Specification

## Document Information

- **Version**: 1.1 (Updated for Master Roadmap)
- **Date**: January 2025
- **Implementation Phase**: Phase 1 (Months 1-2) - CRITICAL FOUNDATION
- **Priority**: Critical - Must Be Implemented First
- **Dependencies**: None (Foundation Infrastructure)

## Executive Summary

The Module Authorization & Licensing Engine is the **core control system** that manages which features, modules, and capabilities are available to specific users, companies, and subscription tiers. This engine enables flexible business models, granular access control, feature rollout management, and compliance enforcement.

## 1. Core Architecture Components

### 1.1 Authorization Engine

```typescript
interface AuthorizationEngine {
  // Module access control
  checkModuleAccess(userId: string, moduleId: string): Promise<ModuleAccessResult>;
  checkFeatureAccess(userId: string, featureId: string): Promise<FeatureAccessResult>;
  
  // Subscription validation
  validateSubscription(companyId: string): Promise<SubscriptionStatus>;
  getAvailableModules(companyId: string): Promise<AvailableModule[]>;
  
  // Role-based permissions
  checkUserPermissions(userId: string, action: string, resource: string): Promise<PermissionResult>;
  
  // License management
  validateLicense(licenseKey: string): Promise<LicenseValidation>;
  checkLicenseUsage(companyId: string): Promise<LicenseUsage>;
  
  // Feature flags
  isFeatureEnabled(featureFlag: string, context: FeatureContext): Promise<boolean>;
}
```

### 1.2 Subscription Tiers & Custom Implementation Support

**Basic Tier (€49/month)**

- Max 5 users
- Core CRM + Basic Invoicing
- 5GB storage, 1000 API calls/month
- Email support
- **Custom Fields**: Up to 10 custom fields
- **Batch Jobs**: 10 concurrent jobs, 100 jobs/day limit
- **Migration Services**: Self-service migration only, up to 5,000 records

**Professional Tier (€149/month)**

- Max 25 users
- All core modules + Field Service + Banking Integration
- 50GB storage, 10,000 API calls/month
- Phone & email support
- **Custom Fields**: Unlimited custom fields
- **Custom Workflows**: Basic workflow automation
- **Batch Jobs**: 25 concurrent jobs, 500 jobs/day limit, priority scheduling
- **Migration Services**: Self-service + basic assisted migration, up to 50,000 records, email consultant support

**Enterprise Tier (€349/month)**

- Unlimited users
- **Full Customization Support**: Custom modules, integrations, business logic
- **Dedicated Implementation Support**: Custom implementation services available
- **Bot Ecosystem Access**: Full access to bot marketplace and premium bots
- **Batch Jobs**: Unlimited concurrent jobs, unlimited daily jobs, highest priority, custom job types
- **Migration Services**: Full migration services including enterprise white-glove migration, unlimited records, dedicated migration consultant

### 1.3 Custom Implementation Tiers

**Configuration Customization (€5,000 - €15,000)**

- No-code customizations, custom fields, workflows
- Timeline: 2-4 weeks
- Self-service + email support
- **Batch Jobs**: Custom job scheduling, up to 50 concurrent jobs

**Module Extensions (€15,000 - €50,000)**

- Custom modules, API integrations, advanced workflows
- Timeline: 4-8 weeks
- Dedicated implementation consultant
- **Batch Jobs**: Custom job types, advanced scheduling, up to 100 concurrent jobs

**Enterprise Solutions (€50,000 - €200,000)**

- Complete custom solutions, complex integrations, custom UI
- Timeline: 3-6 months
- Full implementation team + ongoing support
- All modules including HR, BI Analytics, Industry-specific
- Unlimited storage and API calls
- Dedicated account manager
- **Batch Jobs**: Complete job management platform, unlimited everything, custom job orchestration

### 1.4 Bot Ecosystem Licensing

**Free Community Bots**

- Open-source community contributions
- Basic automation tasks
- Customer acquisition and platform adoption

**Premium Bots (€10-€50/month per bot)**

- Advanced automation functionality
- Industry-specific features
- Professional support and updates
- Available to Professional and Enterprise tier customers

**Enterprise Bots (€100-€500/month per bot)**

- Complex business automation
- Custom integrations and workflows
- White-label options
- Dedicated support and custom development
- Available only to Enterprise tier customers

**Bot Marketplace Revenue Sharing**

- Platform fee: 30% of bot subscription revenue
- Bot certification fee: €500 per bot validation
- Custom bot development: €5K-€50K projects
- Developer tools: Premium SDK features

## 2. Database Schema

### 2.1 Core Tables

```sql
-- Subscription tiers
CREATE TABLE subscription_tiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tier_name VARCHAR(100) UNIQUE NOT NULL,
    tier_level INTEGER NOT NULL,
    monthly_price DECIMAL(10,2),
    annual_price DECIMAL(10,2),
    max_users INTEGER,
    included_modules JSONB,
    feature_limits JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Company subscriptions
CREATE TABLE company_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    subscription_tier_id UUID REFERENCES subscription_tiers(id),
    start_date DATE NOT NULL,
    end_date DATE,
    status subscription_status DEFAULT 'ACTIVE',
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Module licenses
CREATE TABLE module_licenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    module_id VARCHAR(100) NOT NULL,
    license_type license_type, -- SUBSCRIPTION, TRIAL, PERPETUAL
    start_date DATE,
    end_date DATE,
    user_limit INTEGER,
    usage_limit JSONB,
    status license_status DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT NOW()
);

-- User roles and permissions
CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name VARCHAR(100) NOT NULL,
    company_id UUID REFERENCES companies(id),
    permissions JSONB NOT NULL,
    module_access JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Feature flags
CREATE TABLE feature_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    flag_type feature_flag_type,
    default_value BOOLEAN DEFAULT FALSE,
    rollout_percentage INTEGER DEFAULT 0,
    target_users JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage tracking
CREATE TABLE module_usage_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    user_id UUID REFERENCES users(id),
    module_id VARCHAR(100),
    usage_date DATE,
    usage_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Bot marketplace tables
CREATE TABLE bot_marketplace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bot_id VARCHAR(100) UNIQUE NOT NULL,
    bot_name VARCHAR(200) NOT NULL,
    bot_description TEXT,
    developer_id UUID REFERENCES users(id),
    bot_category VARCHAR(100), -- core, industry, workflow, integration
    pricing_tier bot_pricing_tier, -- FREE, PREMIUM, ENTERPRISE
    monthly_price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    certification_status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Bot subscriptions
CREATE TABLE bot_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    bot_id VARCHAR(100) REFERENCES bot_marketplace(bot_id),
    subscription_start DATE NOT NULL,
    subscription_end DATE,
    status subscription_status DEFAULT 'ACTIVE',
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Bot usage tracking
CREATE TABLE bot_usage_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    user_id UUID REFERENCES users(id),
    bot_id VARCHAR(100),
    execution_date DATE,
    execution_count INTEGER DEFAULT 1,
    execution_duration INTEGER, -- in milliseconds
    success_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 3. Module Access Control Logic

### 3.1 Access Control Flow

```typescript
class ModuleAccessController {
  async checkAccess(companyId: string, userId: string, moduleId: string): Promise<AccessResult> {
    // 1. Check subscription tier
    const subscription = await this.getCompanySubscription(companyId);
    if (!subscription || subscription.status !== 'ACTIVE') {
      return { allowed: false, reason: "NO_ACTIVE_SUBSCRIPTION" };
    }
  
    // 2. Check if module included in tier
    const tier = await this.getSubscriptionTier(subscription.subscription_tier_id);
    if (!tier.included_modules.includes(moduleId)) {
      return { allowed: false, reason: "MODULE_NOT_IN_TIER" };
    }
  
    // 3. Check module license
    const license = await this.getModuleLicense(companyId, moduleId);
    if (!license || license.status !== 'ACTIVE') {
      return { allowed: false, reason: "MODULE_NOT_LICENSED" };
    }
  
    // 4. Check user permissions
    const hasPermission = await this.checkUserModulePermission(userId, moduleId);
    if (!hasPermission) {
      return { allowed: false, reason: "INSUFFICIENT_USER_PERMISSIONS" };
    }
  
    // 5. Check usage limits
    const usageStatus = await this.checkUsageLimits(companyId, moduleId);
    if (!usageStatus.allowed) {
      return { allowed: false, reason: "USAGE_LIMIT_EXCEEDED" };
    }
  
    return { allowed: true };
  }
}
```

## 4. Feature Flag System

### 4.1 Feature Flag Types

- **Boolean Flags**: Simple on/off switches
- **Percentage Rollouts**: Gradual rollout to percentage of users
- **User Targeting**: Specific users or companies
- **Geographic Flags**: Region-specific features
- **A/B Testing**: Multiple variants for testing

### 4.2 Greek-Specific Feature Flags

```typescript
const greekFeatureFlags = {
  "greek_banking_integration": {
    type: "percentage",
    rollout: 50, // 50% rollout
    targetRegions: ["GR"],
    requiresCompliance: true
  },
  "aade_mydata_v2": {
    type: "boolean",
    enabled: true,
    requiresCertification: "aade_certified_developer"
  },
  "payroll_ika_integration": {
    type: "user_targeting",
    targetRoles: ["hr_manager", "accountant"],
    requiresCertification: "certified_payroll_specialist"
  }
};
```

## 5. Compliance & Certification Control

### 5.1 Greek Professional Certifications

```typescript
interface GreekComplianceEngine {
  // Professional certifications required for certain modules
  certifications: {
    accountant: "certified_public_accountant_greece";
    tax_consultant: "greek_tax_consultant_license";
    payroll_specialist: "certified_payroll_professional";
    aade_developer: "aade_certified_developer";
    banking_integration: "psd2_certified_developer";
  };
  
  // Module access requirements
  moduleRequirements: {
    hr_payroll: ["accountant", "payroll_specialist"];
    aade_integration: ["accountant", "aade_developer"];
    banking_integration: ["accountant", "banking_integration"];
    tax_reporting: ["accountant", "tax_consultant"];
  };
}
```

## 6. Usage Tracking & Analytics

### 6.1 Real-time Usage Monitoring

```typescript
interface UsageTracker {
  // Track module usage
  trackModuleAccess(companyId: string, userId: string, moduleId: string): Promise<void>;
  trackFeatureUsage(userId: string, featureId: string, duration: number): Promise<void>;
  
  // Monitor limits
  checkAPIQuota(companyId: string): Promise<QuotaStatus>;
  checkStorageUsage(companyId: string): Promise<StorageStatus>;
  checkUserCount(companyId: string): Promise<UserCountStatus>;
  
  // Generate analytics
  getUsageAnalytics(companyId: string, period: DateRange): Promise<UsageAnalytics>;
  getFeatureAdoptionMetrics(): Promise<AdoptionMetrics>;
}
```

## 7. API Middleware Integration

### 7.1 Express Middleware

```typescript
// Module access middleware
const requireModule = (moduleId: string) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const { companyId, userId } = req.user;
    const accessResult = await authEngine.checkModuleAccess(userId, moduleId);
  
    if (!accessResult.allowed) {
      return res.status(403).json({
        error: "MODULE_ACCESS_DENIED",
        reason: accessResult.reason,
        upgradeOptions: await getUpgradeOptions(companyId, moduleId)
      });
    }
  
    next();
  };
};

// Feature flag middleware
const requireFeatureFlag = (flagName: string) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const { companyId, userId } = req.user;
    const isEnabled = await featureFlagEngine.isEnabled(flagName, { companyId, userId });
  
    if (!isEnabled) {
      return res.status(404).json({ error: "FEATURE_NOT_AVAILABLE" });
    }
  
    next();
  };
};
```

## 8. Implementation Timeline

### Phase 1: Core Authorization (Month 1)

- Database schema setup
- Basic subscription tier validation
- Module access control engine
- User role and permission system

### Phase 2: Advanced Features (Month 2)

- Feature flag system
- Usage tracking and analytics
- Greek compliance requirements
- API middleware integration

### Phase 3: Optimization (Month 3)

- Performance optimization
- Caching layer implementation
- Advanced analytics dashboard
- Testing and documentation

## 9. Security Considerations

### 9.1 Authorization Security

- **JWT-based Authentication**: Secure token validation
- **Role-based Access Control**: Granular permission system
- **Audit Logging**: Complete access attempt logging
- **Rate Limiting**: API usage protection
- **Encryption**: Sensitive data protection

### 9.2 Compliance Security

- **Data Privacy**: GDPR compliance for user data
- **Professional Standards**: Greek professional certification validation
- **Regulatory Compliance**: AADE, Bank of Greece requirements
- **Audit Trail**: Complete compliance event logging

## 10. Success Metrics

### Business Metrics

- **85%** trial-to-paid conversion rate
- **60%** basic users upgrade within 12 months
- **80%** feature adoption rate across all modules
- **100%** regulatory compliance maintenance

### Technical Metrics

- **<50ms** average authorization check response time
- **99.99%** authorization service uptime
- **10,000+** concurrent authorization checks support
- **Zero** unauthorized access incidents

---

This Module Authorization & Licensing Engine is **critical infrastructure** that must be implemented first, as all other modules depend on it for access control, subscription management, and feature availability.
