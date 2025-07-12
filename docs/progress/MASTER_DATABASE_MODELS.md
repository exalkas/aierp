# Master Database Models - Greek ERP/CRM System

## Overview

This document outlines the models that were missing from the master database and have been added to support the multi-tenant architecture of the Greek ERP/CRM system.

## Architecture Summary

**Multi-Tenant Setup:**

- **Master Database**: Contains shared reference data and system configuration
- **Company Databases**: Each company has its own database (e.g., `erp_company_12345`) for operational data

## Previously Existing Models

✅ **Company** - Multi-tenant company registry
✅ **User** - User authentication and authorization  
✅ **Voice Command Models** - SystemVoiceCommand, UserVoiceCommand, VoiceCommandLog, VoiceCommandTemplate

## Newly Added Models

### 1. Greek Reference Data Models

These models contain shared reference data that all companies use:

#### 🏛️ **GreekRegion**

- Greek regions and prefectures
- VAT zones and location types
- Geographic coordinates
- Tourist area classifications
- **Use case**: Address validation, VAT rate determination

#### 🏢 **GreekTaxOffice**

- Greek Tax Offices (DOY) directory
- Contact information and operating hours
- Regional associations
- **Use case**: Company registration, tax filing

#### 💰 **GreekVATRate**

- VAT rates by business type and location
- Context-specific rates (takeaway vs dine-in)
- Legal references and effective dates
- **Use case**: Automatic VAT calculation

#### 🏭 **GreekBusinessActivity**

- Greek business activity codes (KAD)
- Hierarchical classification system
- VAT and tax implications
- **Use case**: Business registration, tax compliance

#### 🏛️ **GreekLegalForm**

- Greek legal forms (AE, EPE, OE, EE, IKE, AT)
- Capital requirements and liability types
- Tax rates and legal requirements
- **Use case**: Company setup, legal compliance

#### 🏦 **GreekBank**

- Greek banks directory
- SWIFT codes and payment capabilities
- SEPA and instant payment support
- **Use case**: Payment processing, bank account validation

#### 📍 **PostalCode**

- Greek postal codes with geographic data
- Municipality and region mapping
- **Use case**: Address validation, shipping

### 2. System Configuration Models

These models manage system-wide settings and operations:

#### ⚙️ **SystemConfiguration**

- System-wide configuration settings
- Feature flags and integration settings
- Encrypted and public configuration options
- **Use case**: Global system management

#### 💳 **SubscriptionPlanDefinition**

- Available subscription plans
- Pricing, limits, and features
- Greek-specific features (AADE, tax reports)
- **Use case**: Subscription management

#### 🏢 **CompanySubscription**

- Company subscription tracking
- Billing cycles and payment information
- Usage limits and custom features
- **Use case**: Billing, feature access control

#### 📊 **UsageMetric**

- Usage tracking across companies
- Metrics for billing and analytics
- **Use case**: Usage monitoring, billing

#### 🔔 **SystemNotification**

- System-wide notifications
- Targeted delivery to specific companies/plans
- **Use case**: System announcements, alerts

#### 🔑 **ApiKey**

- API keys for system integrations
- Service-specific permissions and rate limiting
- **Use case**: External integrations, security

## Database Migration

**Migration File**: `0005_master_database_models.py`

- Creates all new tables with proper indexes
- Establishes foreign key relationships
- Sets up enums for Greek-specific types

## Data Seeding

**Seeding Script**: `seed_greek_reference_data.py`

- Populates Greek reference data with real data
- Includes 13 regions, major tax offices, VAT rates
- Sample business activities and postal codes

### Sample Data Included:

**Regions**: 13 Greek regions with proper VAT zones
**Tax Offices**: Athens and Thessaloniki DOY offices
**VAT Rates**: 8 different VAT scenarios including:

- Standard 24% (mainland)
- Reduced 17% (islands)
- Food 13% (takeaway) / 24% (dine-in)
- Healthcare 0% (exempt)
- Books 6% (reduced)

**Banks**: 6 major Greek banks with SWIFT codes
**Legal Forms**: 6 Greek legal forms with requirements

## Key Benefits

### 1. **Centralized Reference Data**

- All companies use the same Greek reference data
- Consistent VAT calculations across tenants
- Easy updates to tax rates and regulations

### 2. **Intelligent VAT System**

- Context-aware VAT calculation
- Business type and location considerations
- Automatic rate suggestions

### 3. **Multi-Tenant Management**

- Subscription and billing management
- Usage tracking and limits
- System-wide notifications

### 4. **Greek Compliance**

- Complete DOY and legal form data
- AADE integration support
- Tax regulation compliance

## Usage Examples

### VAT Rate Lookup:

```python
# Get VAT rate for takeaway coffee in Athens
vat_rate = await get_vat_rate(
    business_type="food_service",
    product_category="beverages",
    location_type="mainland",
    context={"takeaway": True}
)
# Returns: 13% rate
```

### Company Setup:

```python
# Validate company data against Greek reference
legal_form = await get_legal_form("EPE")
tax_office = await get_tax_office("1101")  # Athens A'
region = await get_region("ATT")  # Attica
```

### Subscription Management:

```python
# Check company limits
subscription = await get_company_subscription(company_id)
if subscription.max_users > current_users:
    # Allow new user creation
```

## Next Steps

1. **Run Migration**: `alembic upgrade head`
2. **Seed Data**: `python -m app.scripts.seed_greek_reference_data`
3. **Test Integration**: Verify VAT calculations work correctly
4. **Update Frontend**: Add Greek reference data to UI components
5. **API Integration**: Expose reference data through API endpoints

## Files Created

- `services/api/app/models/greek_reference_data.py` - Greek reference models
- `services/api/app/models/system_configuration.py` - System configuration models
- `services/api/alembic/versions/0005_master_database_models.py` - Database migration
- `services/api/app/scripts/seed_greek_reference_data.py` - Data seeding script

## Technical Implementation

The models follow the existing patterns with:

- UUID primary keys
- Proper indexing for performance
- Audit fields (created_at, updated_at)
- Enum types for Greek-specific classifications
- JSON fields for flexible data storage
- Foreign key relationships where appropriate

This completes the master database model requirements for the Greek ERP/CRM system's multi-tenant architecture.
