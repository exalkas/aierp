# 08. Customization Management

## Overview

Comprehensive customization platform enabling dynamic entity creation, custom fields, layouts, business rules, and Greek market-specific adaptations without code changes.

## Core Features

### 8.1 Dynamic Entity Management

- **Custom Entities**: Create new business objects with relationships
- **Field Management**: Add, modify, remove fields dynamically
- **Greek Entity Types**: Pre-configured Greek business entities (AFM, AMKA, DOY)
- **Relationship Builder**: Define complex entity relationships
- **Entity Templates**: Industry-specific entity templates
- **Data Migration**: Safe entity structure changes

### 8.2 Custom Field System

- **Field Types**: Text, number, date, boolean, select, multi-select, lookup, Greek-specific
- **Greek Field Types**: AFM, AMKA, DOY, Greek address, Greek phone
- **Field Validation**: Built-in and custom validation rules
- **Conditional Fields**: Dynamic field visibility and requirements
- **Calculated Fields**: Formula-based field calculations
- **Field Permissions**: Role-based field access control

### 8.3 Layout Customization

- **Form Layouts**: Drag-and-drop form builder
- **List Views**: Customizable table layouts with Greek formatting
- **Detail Views**: Configurable record detail layouts
- **Mobile Layouts**: Responsive design customization
- **Greek Layouts**: Right-to-left support, Greek typography
- **Print Layouts**: Custom document and report layouts

### 8.4 Business Rules Engine

- **Validation Rules**: Complex business logic enforcement
- **Greek Business Rules**: VAT, tax, compliance rule templates
- **Workflow Triggers**: Rule-based workflow automation
- **Field Updates**: Automatic field value updates
- **Notifications**: Rule-based alert system
- **Approval Processes**: Multi-stage approval workflows

### 8.5 Theme and Branding

- **Color Schemes**: Company branding customization
- **Logo Integration**: Custom logo placement and sizing
- **Greek Typography**: Support for Greek fonts and character sets
- **Custom CSS**: Advanced styling customization
- **White-label Options**: Complete rebranding capabilities
- **Regional Themes**: Greek cultural design elements

## Data Models

### Custom Entity Model

```typescript
interface CustomEntity {
  id: string
  name: string
  nameInGreek?: string
  label: string
  labelInGreek?: string
  pluralLabel: string
  pluralLabelInGreek?: string
  tableName: string
  description?: string
  isSystemEntity: boolean
  isGreekSpecific: boolean
  greekEntityType?: GreekEntityType
  fields: CustomField[]
  relationships: EntityRelationship[]
  layouts: EntityLayout[]
  permissions: EntityPermission[]
  businessRules: BusinessRule[]
  customSettings: Record<string, any>
  isActive: boolean
  version: string
  createdAt: Date
  updatedAt: Date
  createdBy: string
  lastUpdatedBy: string
}

type GreekEntityType = 
  | 'business_entity'
  | 'individual_entity'
  | 'government_entity'
  | 'tax_entity'
  | 'compliance_entity'

interface CustomField {
  id: string
  name: string
  nameInGreek?: string
  label: string
  labelInGreek?: string
  type: FieldType
  dataType: DataType
  isRequired: boolean
  isUnique: boolean
  isIndexed: boolean
  isGreekSpecific: boolean
  greekFieldType?: GreekFieldType
  defaultValue?: any
  validation: FieldValidation
  options?: FieldOption[]
  formula?: FieldFormula
  permissions: FieldPermission[]
  displaySettings: FieldDisplaySettings
  customSettings: Record<string, any>
  order: number
  isActive: boolean
  createdAt: Date
  updatedAt: Date
}

type FieldType = 
  | 'text'
  | 'textarea'
  | 'number'
  | 'decimal'
  | 'currency'
  | 'date'
  | 'datetime'
  | 'time'
  | 'boolean'
  | 'select'
  | 'multiselect'
  | 'lookup'
  | 'multilookup'
  | 'file'
  | 'image'
  | 'url'
  | 'email'
  | 'phone'
  | 'address'
  | 'json'
  | 'greek_afm'
  | 'greek_amka'
  | 'greek_doy'
  | 'greek_address'
  | 'greek_phone'

type GreekFieldType = 
  | 'afm'
  | 'amka'
  | 'doy'
  | 'greek_address'
  | 'greek_phone'
  | 'greek_postal_code'
  | 'greek_vat_number'
  | 'greek_social_security'
  | 'greek_tax_office'

interface FieldValidation {
  rules: ValidationRule[]
  customValidation?: string // JavaScript code
  errorMessage?: string
  errorMessageInGreek?: string
  greekValidation?: GreekValidationRule[]
}

interface GreekValidationRule {
  type: 'afm' | 'amka' | 'doy' | 'phone' | 'postal_code'
  strict: boolean
  checkOnline?: boolean // Validate against AADE/government databases
}
```

### Layout Model

```typescript
interface EntityLayout {
  id: string
  entityId: string
  name: string
  nameInGreek?: string
  type: LayoutType
  isDefault: boolean
  isGreekOptimized: boolean
  configuration: LayoutConfiguration
  sections: LayoutSection[]
  permissions: LayoutPermission[]
  responsiveSettings: ResponsiveSettings
  customSettings: Record<string, any>
  version: string
  createdAt: Date
  updatedAt: Date
  createdBy: string
}

type LayoutType = 
  | 'form'
  | 'list'
  | 'detail'
  | 'search'
  | 'print'
  | 'mobile'
  | 'greek_invoice'
  | 'greek_report'

interface LayoutSection {
  id: string
  name: string
  nameInGreek?: string
  order: number
  columns: number
  isCollapsible: boolean
  isCollapsed: boolean
  fields: LayoutField[]
  customSettings: Record<string, any>
}

interface LayoutField {
  fieldId: string
  order: number
  width?: number
  isVisible: boolean
  isReadonly: boolean
  isRequired?: boolean
  customLabel?: string
  customLabelInGreek?: string
  displaySettings: FieldDisplaySettings
  conditionalDisplay?: ConditionalDisplayRule[]
}
```

### Business Rule Model

```typescript
interface BusinessRule {
  id: string
  entityId: string
  name: string
  nameInGreek?: string
  description?: string
  type: BusinessRuleType
  isActive: boolean
  isGreekSpecific: boolean
  greekRuleType?: GreekBusinessRuleType
  trigger: RuleTrigger
  conditions: RuleCondition[]
  actions: RuleAction[]
  priority: number
  customSettings: Record<string, any>
  createdAt: Date
  updatedAt: Date
  createdBy: string
}

type BusinessRuleType = 
  | 'validation'
  | 'calculation'
  | 'notification'
  | 'workflow'
  | 'field_update'
  | 'approval'

type GreekBusinessRuleType = 
  | 'vat_calculation'
  | 'tax_validation'
  | 'aade_compliance'
  | 'greek_address_validation'
  | 'working_hours_validation'
  | 'holiday_scheduling'

interface RuleTrigger {
  event: 'create' | 'update' | 'delete' | 'field_change' | 'schedule'
  fields?: string[] // For field_change events
  schedule?: string // Cron expression for scheduled rules
}

interface RuleCondition {
  field: string
  operator: ConditionOperator
  value: any
  dataType: DataType
  isGreekSpecific?: boolean
}

interface RuleAction {
  type: ActionType
  configuration: ActionConfiguration
  order: number
  isGreekSpecific?: boolean
}

type ActionType = 
  | 'set_field_value'
  | 'send_notification'
  | 'create_record'
  | 'update_record'
  | 'start_workflow'
  | 'send_email'
  | 'calculate_greek_vat'
  | 'validate_aade'
```

### Theme Model

```typescript
interface Theme {
  id: string
  name: string
  nameInGreek?: string
  description?: string
  isDefault: boolean
  isGreekOptimized: boolean
  colorScheme: ColorScheme
  typography: Typography
  branding: Branding
  greekDesignElements: GreekDesignElements
  customCSS?: string
  components: ComponentStyles
  layouts: LayoutStyles
  customSettings: Record<string, any>
  version: string
  createdAt: Date
  updatedAt: Date
  createdBy: string
}

interface ColorScheme {
  primary: string
  secondary: string
  accent: string
  background: string
  surface: string
  text: string
  textSecondary: string
  border: string
  success: string
  warning: string
  error: string
  info: string
  greekBlue?: string // Traditional Greek blue
  greekWhite?: string // Greek white
}

interface Typography {
  fontFamily: string
  greekFontFamily?: string
  headingFont?: string
  bodyFont?: string
  fontSize: {
    small: string
    medium: string
    large: string
    xlarge: string
  }
  lineHeight: number
  letterSpacing: string
  greekCharacterSpacing?: string
}

interface GreekDesignElements {
  useGreekPatterns: boolean
  greekBorderStyle?: string
  orthodoxCrossIntegration?: boolean
  greekFlagColors?: boolean
  ancientGreekMotifs?: boolean
  modernGreekDesign?: boolean
}
```

## API Endpoints

### Entity Management APIs

```typescript
// Custom Entity CRUD
GET /api/custom-entities
POST /api/custom-entities
GET /api/custom-entities/:id
PUT /api/custom-entities/:id
DELETE /api/custom-entities/:id
POST /api/custom-entities/:id/activate
POST /api/custom-entities/:id/deactivate

// Entity Fields
GET /api/custom-entities/:id/fields
POST /api/custom-entities/:id/fields
PUT /api/custom-entities/:id/fields/:fieldId
DELETE /api/custom-entities/:id/fields/:fieldId
POST /api/custom-entities/:id/fields/reorder

// Entity Relationships
GET /api/custom-entities/:id/relationships
POST /api/custom-entities/:id/relationships
PUT /api/custom-entities/:id/relationships/:relationshipId
DELETE /api/custom-entities/:id/relationships/:relationshipId

// Greek Entity Features
GET /api/custom-entities/greek-templates
POST /api/custom-entities/greek-validation
GET /api/custom-entities/greek-field-types
POST /api/custom-entities/migrate-to-greek
```

### Layout Management APIs

```typescript
// Layout CRUD
GET /api/layouts
POST /api/layouts
GET /api/layouts/:id
PUT /api/layouts/:id
DELETE /api/layouts/:id
POST /api/layouts/:id/duplicate

// Layout Sections and Fields
GET /api/layouts/:id/sections
POST /api/layouts/:id/sections
PUT /api/layouts/:id/sections/:sectionId
DELETE /api/layouts/:id/sections/:sectionId
POST /api/layouts/:id/sections/:sectionId/fields

// Layout Preview and Testing
POST /api/layouts/:id/preview
POST /api/layouts/:id/validate
GET /api/layouts/:id/responsive-preview

// Greek Layout Features
GET /api/layouts/greek-templates
POST /api/layouts/greek-optimize
GET /api/layouts/greek-typography
```

### Business Rules APIs

```typescript
// Business Rules CRUD
GET /api/business-rules
POST /api/business-rules
GET /api/business-rules/:id
PUT /api/business-rules/:id
DELETE /api/business-rules/:id
POST /api/business-rules/:id/activate
POST /api/business-rules/:id/deactivate

// Rule Testing and Validation
POST /api/business-rules/:id/test
POST /api/business-rules/:id/validate
GET /api/business-rules/:id/execution-history
POST /api/business-rules/bulk-test

// Greek Business Rules
GET /api/business-rules/greek-templates
POST /api/business-rules/greek-validation
GET /api/business-rules/vat-calculation-rules
POST /api/business-rules/aade-compliance-rules
```

### Theme Management APIs

```typescript
// Theme CRUD
GET /api/themes
POST /api/themes
GET /api/themes/:id
PUT /api/themes/:id
DELETE /api/themes/:id
POST /api/themes/:id/activate
POST /api/themes/:id/duplicate

// Theme Preview and Export
GET /api/themes/:id/preview
POST /api/themes/:id/export
POST /api/themes/import
GET /api/themes/:id/css

// Greek Theme Features
GET /api/themes/greek-templates
POST /api/themes/greek-optimize
GET /api/themes/greek-fonts
GET /api/themes/greek-colors
```

## UI Components

### EntityBuilder Component

```typescript
interface EntityBuilderProps {
  entityId?: string
  template?: EntityTemplate
  onSave?: (entity: CustomEntity) => void
  showGreekFeatures?: boolean
  allowAdvanced?: boolean
}

const EntityBuilder: React.FC<EntityBuilderProps> = ({
  entityId,
  template,
  onSave,
  showGreekFeatures = true,
  allowAdvanced = true
}) => {
  // Component implementation
}
```

### FieldManager Component

```typescript
interface FieldManagerProps {
  entityId: string
  fields: CustomField[]
  onFieldAdd?: (field: CustomField) => void
  onFieldUpdate?: (fieldId: string, updates: Partial<CustomField>) => void
  onFieldDelete?: (fieldId: string) => void
  showGreekFieldTypes?: boolean
}

const FieldManager: React.FC<FieldManagerProps> = ({
  entityId,
  fields,
  onFieldAdd,
  onFieldUpdate,
  onFieldDelete,
  showGreekFieldTypes = true
}) => {
  // Component implementation
}
```

### LayoutDesigner Component

```typescript
interface LayoutDesignerProps {
  layoutId?: string
  entityId: string
  layoutType: LayoutType
  onSave?: (layout: EntityLayout) => void
  useGreekOptimization?: boolean
}

const LayoutDesigner: React.FC<LayoutDesignerProps> = ({
  layoutId,
  entityId,
  layoutType,
  onSave,
  useGreekOptimization = true
}) => {
  // Component implementation
}
```

### BusinessRuleBuilder Component

```typescript
interface BusinessRuleBuilderProps {
  ruleId?: string
  entityId: string
  onSave?: (rule: BusinessRule) => void
  showGreekRules?: boolean
  allowAdvanced?: boolean
}

const BusinessRuleBuilder: React.FC<BusinessRuleBuilderProps> = ({
  ruleId,
  entityId,
  onSave,
  showGreekRules = true,
  allowAdvanced = true
}) => {
  // Component implementation
}
```

### ThemeCustomizer Component

```typescript
interface ThemeCustomizerProps {
  themeId?: string
  onSave?: (theme: Theme) => void
  showGreekElements?: boolean
  allowCustomCSS?: boolean
}

const ThemeCustomizer: React.FC<ThemeCustomizerProps> = ({
  themeId,
  onSave,
  showGreekElements = true,
  allowCustomCSS = true
}) => {
  // Component implementation
}
```

## Custom Hooks

### useCustomEntities Hook

```typescript
interface UseCustomEntitiesOptions {
  includeSystem?: boolean
  includeGreek?: boolean
  activeOnly?: boolean
}

const useCustomEntities = (options: UseCustomEntitiesOptions) => {
  const [entities, setEntities] = useState<CustomEntity[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createEntity = async (entity: Partial<CustomEntity>) => {
    // Implementation
  }

  const updateEntity = async (entityId: string, updates: Partial<CustomEntity>) => {
    // Implementation
  }

  const deleteEntity = async (entityId: string) => {
    // Implementation
  }

  const addField = async (entityId: string, field: Partial<CustomField>) => {
    // Implementation
  }

  const updateField = async (entityId: string, fieldId: string, updates: Partial<CustomField>) => {
    // Implementation
  }

  const deleteField = async (entityId: string, fieldId: string) => {
    // Implementation
  }

  return {
    entities,
    loading,
    error,
    createEntity,
    updateEntity,
    deleteEntity,
    addField,
    updateField,
    deleteField,
    refetch: () => {/* Implementation */}
  }
}
```

### useLayoutBuilder Hook

```typescript
interface UseLayoutBuilderOptions {
  entityId: string
  layoutType: LayoutType
}

const useLayoutBuilder = (options: UseLayoutBuilderOptions) => {
  const [layout, setLayout] = useState<EntityLayout | null>(null)
  const [sections, setSections] = useState<LayoutSection[]>([])
  const [availableFields, setAvailableFields] = useState<CustomField[]>([])

  const addSection = (section: Partial<LayoutSection>) => {
    // Implementation
  }

  const updateSection = (sectionId: string, updates: Partial<LayoutSection>) => {
    // Implementation
  }

  const deleteSection = (sectionId: string) => {
    // Implementation
  }

  const addFieldToSection = (sectionId: string, field: LayoutField) => {
    // Implementation
  }

  const removeFieldFromSection = (sectionId: string, fieldId: string) => {
    // Implementation
  }

  const reorderSections = (newOrder: string[]) => {
    // Implementation
  }

  const previewLayout = () => {
    // Implementation
  }

  return {
    layout,
    sections,
    availableFields,
    addSection,
    updateSection,
    deleteSection,
    addFieldToSection,
    removeFieldFromSection,
    reorderSections,
    previewLayout
  }
}
```

### useGreekCustomization Hook

```typescript
const useGreekCustomization = () => {
  const [greekFieldTypes, setGreekFieldTypes] = useState<GreekFieldType[]>([])
  const [greekValidators, setGreekValidators] = useState<GreekValidator[]>([])
  const [greekTemplates, setGreekTemplates] = useState<GreekTemplate[]>([])

  const validateAFM = (afm: string): ValidationResult => {
    // AFM validation algorithm
    const digits = afm.replace(/\D/g, '')
    if (digits.length !== 9) return { isValid: false, error: 'AFM must be 9 digits' }
  
    // AFM checksum validation
    let sum = 0
    for (let i = 0; i < 8; i++) {
      sum += parseInt(digits[i]) * Math.pow(2, 8 - i)
    }
    const remainder = sum % 11
    const checkDigit = remainder < 2 ? remainder : 11 - remainder
  
    return {
      isValid: parseInt(digits[8]) === checkDigit,
      error: parseInt(digits[8]) !== checkDigit ? 'Invalid AFM checksum' : undefined
    }
  }

  const validateAMKA = (amka: string): ValidationResult => {
    // AMKA validation algorithm
    const digits = amka.replace(/\D/g, '')
    if (digits.length !== 11) return { isValid: false, error: 'AMKA must be 11 digits' }
  
    // AMKA checksum validation (Luhn algorithm)
    let sum = 0
    for (let i = 0; i < 10; i++) {
      let digit = parseInt(digits[i])
      if (i % 2 === 1) {
        digit *= 2
        if (digit > 9) digit -= 9
      }
      sum += digit
    }
    const checkDigit = (10 - (sum % 10)) % 10
  
    return {
      isValid: parseInt(digits[10]) === checkDigit,
      error: parseInt(digits[10]) !== checkDigit ? 'Invalid AMKA checksum' : undefined
    }
  }

  const validateGreekPhone = (phone: string): ValidationResult => {
    // Greek phone number validation
    const digits = phone.replace(/\D/g, '')
  
    // Mobile: 69XXXXXXXX (10 digits)
    // Landline: 2XXXXXXXXX (10 digits)
    if (digits.length !== 10) {
      return { isValid: false, error: 'Greek phone must be 10 digits' }
    }
  
    if (!digits.startsWith('2') && !digits.startsWith('69')) {
      return { isValid: false, error: 'Invalid Greek phone format' }
    }
  
    return { isValid: true }
  }

  const formatGreekAddress = (address: GreekAddress): string => {
    const parts = [
      address.street,
      address.number,
      address.postalCode,
      address.city,
      address.region
    ].filter(Boolean)
  
    return parts.join(', ')
  }

  const getGreekEntityTemplates = (): GreekEntityTemplate[] => {
    return [
      {
        id: 'greek_customer',
        name: 'Greek Customer',
        nameInGreek: 'Ελληνας Πελάτης',
        fields: [
          { name: 'afm', type: 'greek_afm', required: true },
          { name: 'doy', type: 'greek_doy', required: true },
          { name: 'address', type: 'greek_address', required: true },
          { name: 'phone', type: 'greek_phone', required: false }
        ]
      },
      {
        id: 'greek_supplier',
        name: 'Greek Supplier',
        nameInGreek: 'Ελληνας Προμηθευτής',
        fields: [
          { name: 'afm', type: 'greek_afm', required: true },
          { name: 'doy', type: 'greek_doy', required: true },
          { name: 'business_activity', type: 'text', required: true }
        ]
      }
    ]
  }

  return {
    greekFieldTypes,
    greekValidators,
    greekTemplates,
    validateAFM,
    validateAMKA,
    validateGreekPhone,
    formatGreekAddress,
    getGreekEntityTemplates
  }
}
```

### useBusinessRules Hook

```typescript
interface UseBusinessRulesOptions {
  entityId?: string
  includeGreek?: boolean
  activeOnly?: boolean
}

const useBusinessRules = (options: UseBusinessRulesOptions) => {
  const [rules, setRules] = useState<BusinessRule[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createRule = async (rule: Partial<BusinessRule>) => {
    // Implementation
  }

  const updateRule = async (ruleId: string, updates: Partial<BusinessRule>) => {
    // Implementation
  }

  const deleteRule = async (ruleId: string) => {
    // Implementation
  }

  const testRule = async (ruleId: string, testData: any) => {
    // Implementation
  }

  const executeRule = async (ruleId: string, record: any) => {
    // Implementation
  }

  return {
    rules,
    loading,
    error,
    createRule,
    updateRule,
    deleteRule,
    testRule,
    executeRule,
    refetch: () => {/* Implementation */}
  }
}
```

## Context Providers

### CustomizationProvider

```typescript
interface CustomizationContextType {
  // Entity state
  customEntities: CustomEntity[]
  entityLayouts: EntityLayout[]
  businessRules: BusinessRule[]
  
  // Theme state
  currentTheme: Theme
  availableThemes: Theme[]
  
  // Greek features
  greekFieldTypes: GreekFieldType[]
  greekTemplates: GreekTemplate[]
  greekValidators: GreekValidator[]
  
  // Actions
  createEntity: (entity: Partial<CustomEntity>) => Promise<void>
  updateLayout: (layoutId: string, updates: Partial<EntityLayout>) => Promise<void>
  applyTheme: (themeId: string) => Promise<void>
  
  // Greek actions
  validateGreekField: (fieldType: GreekFieldType, value: string) => ValidationResult
  applyGreekTemplate: (templateId: string, entityId: string) => Promise<void>
  generateGreekLayout: (entityId: string, layoutType: LayoutType) => Promise<EntityLayout>
}

const CustomizationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Implementation
}
```

## Greek Customization Features

### Greek Field Types

- **AFM Field**: Automatic validation and formatting
- **AMKA Field**: Social security number validation
- **DOY Field**: Tax office selection with validation
- **Greek Address**: Multi-line address with postal code validation
- **Greek Phone**: Mobile and landline format validation
- **VAT Number**: Business VAT number validation

### Greek Entity Templates

- **Greek Customer**: AFM, DOY, Greek address, phone
- **Greek Supplier**: Business information with tax details
- **Greek Employee**: AMKA, AFM, insurance details
- **Greek Product**: With VAT categories and tax codes
- **Greek Invoice**: Compliant with AADE requirements

### Greek Business Rules

- **VAT Calculation**: Automatic tax calculation based on product type
- **AADE Compliance**: Validation before invoice submission
- **Working Hours**: Greek business hours validation
- **Holiday Scheduling**: Orthodox calendar integration
- **Regional Variations**: Prefecture-specific business rules

### Greek Layout Optimization

- **Right-to-Left Support**: For mixed Greek/English content
- **Greek Typography**: Proper font selection and spacing
- **Cultural Elements**: Design patterns familiar to Greek users
- **Government Forms**: Layouts matching Greek official documents
- **Print Layouts**: Greek business document formatting

## Testing Specifications

### Unit Tests

```typescript
describe('Customization Models', () => {
  test('Custom entity validation', () => {})
  test('Field type validation', () => {})
  test('Layout structure validation', () => {})
  test('Business rule condition evaluation', () => {})
})

describe('Greek Customization Utils', () => {
  test('AFM validation algorithm', () => {})
  test('AMKA validation algorithm', () => {})
  test('Greek phone validation', () => {})
  test('Greek address formatting', () => {})
})
```

### Integration Tests

```typescript
describe('Customization APIs', () => {
  test('Entity creation and field addition', () => {})
  test('Layout design and preview', () => {})
  test('Business rule execution', () => {})
  test('Theme application', () => {})
  test('Greek template application', () => {})
})
```

### E2E Tests

```typescript
describe('Customization Workflows', () => {
  test('Complete entity customization process', () => {})
  test('Layout design and form generation', () => {})
  test('Business rule creation and testing', () => {})
  test('Greek entity template application', () => {})
  test('Theme customization and application', () => {})
})
```

## Performance Considerations

### Dynamic Field Processing

- Efficient field type resolution
- Optimized validation processing
- Cached layout rendering
- Minimal DOM manipulation
- Lazy loading of complex fields

### Greek Validation Performance

- Cached AFM/AMKA validation results
- Optimized Greek character processing
- Efficient address validation
- Batch validation for bulk operations
- Local validation before server calls

### Layout Rendering Optimization

- Component reuse for similar layouts
- Efficient responsive design calculation
- Minimal re-renders on field changes
- Optimized Greek font loading
- CSS optimization for Greek typography

## Success Metrics

### Customization Adoption

- Custom entity creation rates
- Field customization usage
- Layout modification frequency
- Business rule implementation
- Theme customization adoption

### Greek Market Adaptation

- Greek field type usage
- Greek template adoption
- Validation accuracy rates
- Cultural design element usage
- User satisfaction with Greek features

### System Flexibility

- Customization without code changes
- User self-service customization
- Configuration migration success
- Performance impact measurement
- Developer productivity improvement
