# 06. Analytics & Reporting

## Overview

Comprehensive business intelligence platform with real-time dashboards, custom reports, Greek market analytics, and GDPR-compliant data processing.

## Core Features

### 6.1 Dashboard System

- **Executive Dashboard**: High-level KPIs and Greek market insights
- **Sales Dashboard**: Revenue tracking with Greek tax implications
- **Customer Dashboard**: Customer behavior and Greek demographics
- **Service Dashboard**: Support metrics and satisfaction scores
- **Custom Dashboards**: User-configurable widgets and layouts
- **Real-time Updates**: Live data streaming and notifications

### 6.2 Report Builder

- **Drag-and-Drop Interface**: Visual report construction
- **Greek Templates**: Pre-built reports for Greek market
- **Custom Fields**: Support for dynamic user-defined fields
- **Scheduled Reports**: Automated report generation and delivery
- **Export Options**: PDF, Excel, CSV with Greek formatting
- **Data Visualization**: Charts, graphs, and Greek-localized formatting

### 6.3 Advanced Analytics

- **Predictive Analytics**: Sales forecasting with Greek seasonality
- **Customer Segmentation**: Greek demographic and behavioral analysis
- **Trend Analysis**: Market trends and Greek economic indicators
- **Performance Metrics**: KPI tracking and goal management
- **Cohort Analysis**: Customer lifetime value and retention
- **A/B Testing**: Feature testing and optimization

### 6.4 Greek Market Intelligence

- **Economic Indicators**: Greek GDP, inflation, unemployment integration
- **Industry Benchmarks**: Sector-specific Greek market data
- **Regional Analytics**: Prefecture and municipality-level insights
- **Seasonal Patterns**: Greek holiday and tourism season impact
- **Compliance Reporting**: AADE, tax, and regulatory reports
- **Currency Analytics**: EUR fluctuation impact analysis

### 6.5 Data Integration

- **Multi-source Data**: CRM, ERP, external APIs integration
- **Real-time Sync**: Live data pipeline processing
- **Data Warehousing**: Historical data storage and retrieval
- **ETL Processes**: Extract, Transform, Load automation
- **API Integration**: External service data incorporation
- **Greek Data Sources**: AADE, statistical agencies integration

## Data Models

### Dashboard Model

```typescript
interface Dashboard {
  id: string
  name: string
  description?: string
  type: 'executive' | 'sales' | 'customer' | 'service' | 'custom'
  isDefault: boolean
  isPublic: boolean
  isGreekLocalized: boolean
  layout: DashboardLayout
  widgets: DashboardWidget[]
  filters: DashboardFilter[]
  refreshInterval: number // seconds
  lastRefreshed: Date
  customFields: Record<string, any>
  permissions: DashboardPermission[]
  createdAt: Date
  updatedAt: Date
  createdBy: string
  lastUpdatedBy: string
  tags: string[]
}

interface DashboardWidget {
  id: string
  type: WidgetType
  title: string
  description?: string
  position: WidgetPosition
  size: WidgetSize
  configuration: WidgetConfiguration
  dataSource: DataSource
  chartType?: ChartType
  isGreekFormatted: boolean
  customFields: Record<string, any>
  refreshInterval?: number
}

type WidgetType = 
  | 'metric' 
  | 'chart' 
  | 'table' 
  | 'map' 
  | 'list' 
  | 'progress' 
  | 'calendar'
  | 'greek_economic_indicator'
  | 'greek_tax_summary'

interface WidgetPosition {
  x: number
  y: number
  width: number
  height: number
}
```

### Report Model

```typescript
interface Report {
  id: string
  name: string
  description?: string
  type: 'standard' | 'custom' | 'scheduled'
  category: ReportCategory
  isGreekCompliant: boolean
  greekReportType?: GreekReportType
  template?: ReportTemplate
  parameters: ReportParameter[]
  dataSource: DataSource
  filters: ReportFilter[]
  groupBy: string[]
  sortBy: ReportSort[]
  columns: ReportColumn[]
  chartConfiguration?: ChartConfiguration
  formatOptions: ReportFormatOptions
  schedule?: ReportSchedule
  customFields: Record<string, any>
  outputFormats: OutputFormat[]
  isPublic: boolean
  permissions: ReportPermission[]
  executionHistory: ReportExecution[]
  createdAt: Date
  updatedAt: Date
  createdBy: string
  lastUpdatedBy: string
  tags: string[]
}

type GreekReportType = 
  | 'vat_summary'
  | 'aade_compliance'
  | 'employee_summary'
  | 'regional_sales'
  | 'seasonal_analysis'
  | 'customer_demographics'

interface ReportParameter {
  name: string
  type: 'string' | 'number' | 'date' | 'boolean' | 'select' | 'multiselect'
  label: string
  labelInGreek?: string
  required: boolean
  defaultValue?: any
  options?: ParameterOption[]
  validation?: ParameterValidation
}
```

### Analytics Model

```typescript
interface AnalyticsMetric {
  id: string
  name: string
  nameInGreek?: string
  description?: string
  category: MetricCategory
  type: MetricType
  dataType: 'number' | 'percentage' | 'currency' | 'duration'
  calculation: MetricCalculation
  isGreekSpecific: boolean
  greekContext?: GreekMetricContext
  targets: MetricTarget[]
  benchmarks: MetricBenchmark[]
  customFields: Record<string, any>
  createdAt: Date
  updatedAt: Date
  createdBy: string
}

interface GreekMetricContext {
  economicIndicator?: boolean
  taxRelated?: boolean
  complianceMetric?: boolean
  regionalMetric?: boolean
  seasonalAdjusted?: boolean
  currencyAdjusted?: boolean
}

type MetricCategory = 
  | 'sales' 
  | 'customer' 
  | 'service' 
  | 'financial' 
  | 'operational'
  | 'greek_compliance'
  | 'greek_market'

interface DataSource {
  id: string
  name: string
  type: 'database' | 'api' | 'file' | 'external'
  connection: DataConnection
  schema?: DataSchema
  refreshSchedule?: string // cron expression
  lastSync: Date
  isGreekDataSource: boolean
  greekDataType?: 'aade' | 'bank' | 'statistics' | 'economic'
}
```

### Greek Analytics Model

```typescript
interface GreekMarketAnalytics {
  id: string
  period: DatePeriod
  region?: GreekRegion
  industry?: string
  economicIndicators: GreekEconomicIndicator[]
  marketMetrics: GreekMarketMetric[]
  complianceMetrics: GreekComplianceMetric[]
  customFields: Record<string, any>
  createdAt: Date
  updatedAt: Date
}

interface GreekEconomicIndicator {
  indicator: 'gdp' | 'inflation' | 'unemployment' | 'consumer_confidence' | 'tourism_index'
  value: number
  unit: string
  period: DatePeriod
  source: 'elstat' | 'bank_of_greece' | 'eurostat' | 'oecd'
  trend: 'up' | 'down' | 'stable'
  impact: 'positive' | 'negative' | 'neutral'
}

interface GreekRegion {
  type: 'prefecture' | 'municipality' | 'region'
  code: string
  name: string
  nameInGreek: string
}
```

## API Endpoints

### Dashboard APIs

```typescript
// Dashboard Management
GET /api/dashboards
POST /api/dashboards
GET /api/dashboards/:id
PUT /api/dashboards/:id
DELETE /api/dashboards/:id
POST /api/dashboards/:id/duplicate
POST /api/dashboards/:id/share

// Dashboard Widgets
GET /api/dashboards/:id/widgets
POST /api/dashboards/:id/widgets
PUT /api/dashboards/:id/widgets/:widgetId
DELETE /api/dashboards/:id/widgets/:widgetId
POST /api/dashboards/:id/widgets/:widgetId/data

// Dashboard Data
GET /api/dashboards/:id/data
POST /api/dashboards/:id/refresh
GET /api/dashboards/:id/export

// Greek Dashboard Features
GET /api/dashboards/greek-templates
POST /api/dashboards/greek-economic-data
GET /api/dashboards/greek-compliance-widgets
```

### Report APIs

```typescript
// Report Management
GET /api/reports
POST /api/reports
GET /api/reports/:id
PUT /api/reports/:id
DELETE /api/reports/:id
POST /api/reports/:id/execute
POST /api/reports/:id/schedule

// Report Execution
GET /api/reports/:id/executions
GET /api/reports/:id/executions/:executionId
GET /api/reports/:id/executions/:executionId/download
POST /api/reports/:id/executions/:executionId/share

// Report Templates
GET /api/report-templates
POST /api/report-templates
GET /api/report-templates/:id
PUT /api/report-templates/:id
DELETE /api/report-templates/:id

// Greek Report Features
GET /api/reports/greek-templates
POST /api/reports/aade-compliance
GET /api/reports/vat-summary
POST /api/reports/regional-analysis
GET /api/reports/seasonal-patterns
```

### Analytics APIs

```typescript
// Analytics Metrics
GET /api/analytics/metrics
POST /api/analytics/metrics
GET /api/analytics/metrics/:id
PUT /api/analytics/metrics/:id
DELETE /api/analytics/metrics/:id
GET /api/analytics/metrics/:id/data

// Analytics Queries
POST /api/analytics/query
POST /api/analytics/query/saved
GET /api/analytics/query/history
POST /api/analytics/query/export

// Predictive Analytics
POST /api/analytics/forecast
GET /api/analytics/trends
POST /api/analytics/segmentation
GET /api/analytics/cohorts

// Greek Analytics
GET /api/analytics/greek-economic-data
POST /api/analytics/greek-market-analysis
GET /api/analytics/regional-insights
GET /api/analytics/seasonal-analysis
POST /api/analytics/compliance-metrics
```

### Data Integration APIs

```typescript
// Data Sources
GET /api/data-sources
POST /api/data-sources
GET /api/data-sources/:id
PUT /api/data-sources/:id
DELETE /api/data-sources/:id
POST /api/data-sources/:id/test
POST /api/data-sources/:id/sync

// ETL Processes
GET /api/etl/jobs
POST /api/etl/jobs
GET /api/etl/jobs/:id
PUT /api/etl/jobs/:id
POST /api/etl/jobs/:id/run
GET /api/etl/jobs/:id/logs

// Greek Data Integration
GET /api/data-sources/aade-connection
POST /api/data-sources/greek-banks
GET /api/data-sources/elstat-data
POST /api/data-sources/validate-greek-source
```

## UI Components

### DashboardBuilder Component

```typescript
interface DashboardBuilderProps {
  dashboardId?: string
  template?: DashboardTemplate
  onSave?: (dashboard: Dashboard) => void
  showGreekTemplates?: boolean
  allowCustomFields?: boolean
}

const DashboardBuilder: React.FC<DashboardBuilderProps> = ({
  dashboardId,
  template,
  onSave,
  showGreekTemplates = true,
  allowCustomFields = true
}) => {
  // Component implementation
}
```

### ReportBuilder Component

```typescript
interface ReportBuilderProps {
  reportId?: string
  template?: ReportTemplate
  onSave?: (report: Report) => void
  showGreekTemplates?: boolean
  allowScheduling?: boolean
}

const ReportBuilder: React.FC<ReportBuilderProps> = ({
  reportId,
  template,
  onSave,
  showGreekTemplates = true,
  allowScheduling = true
}) => {
  // Component implementation
}
```

### AnalyticsDashboard Component

```typescript
interface AnalyticsDashboardProps {
  dashboardId: string
  filters?: DashboardFilter[]
  realtime?: boolean
  showGreekData?: boolean
  onWidgetClick?: (widget: DashboardWidget) => void
}

const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({
  dashboardId,
  filters,
  realtime = false,
  showGreekData = true,
  onWidgetClick
}) => {
  // Component implementation
}
```

### ChartWidget Component

```typescript
interface ChartWidgetProps {
  widget: DashboardWidget
  data: any[]
  loading?: boolean
  error?: string
  onUpdate?: (widget: DashboardWidget) => void
  useGreekFormatting?: boolean
}

const ChartWidget: React.FC<ChartWidgetProps> = ({
  widget,
  data,
  loading = false,
  error,
  onUpdate,
  useGreekFormatting = true
}) => {
  // Component implementation
}
```

### GreekMarketInsights Component

```typescript
interface GreekMarketInsightsProps {
  region?: GreekRegion
  industry?: string
  period?: DatePeriod
  onRegionChange?: (region: GreekRegion) => void
  showEconomicIndicators?: boolean
}

const GreekMarketInsights: React.FC<GreekMarketInsightsProps> = ({
  region,
  industry,
  period,
  onRegionChange,
  showEconomicIndicators = true
}) => {
  // Component implementation
}
```

## Custom Hooks

### useDashboard Hook

```typescript
interface UseDashboardOptions {
  dashboardId: string
  realtime?: boolean
  refreshInterval?: number
}

const useDashboard = (options: UseDashboardOptions) => {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null)
  const [data, setData] = useState<Record<string, any>>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const refreshDashboard = async () => {
    // Implementation
  }

  const updateWidget = async (widgetId: string, updates: Partial<DashboardWidget>) => {
    // Implementation
  }

  const addWidget = async (widget: Partial<DashboardWidget>) => {
    // Implementation
  }

  const removeWidget = async (widgetId: string) => {
    // Implementation
  }

  return {
    dashboard,
    data,
    loading,
    error,
    refreshDashboard,
    updateWidget,
    addWidget,
    removeWidget,
    refetch: () => {/* Implementation */}
  }
}
```

### useReports Hook

```typescript
interface UseReportsOptions {
  category?: ReportCategory
  filters?: ReportFilter[]
  includeGreekReports?: boolean
}

const useReports = (options: UseReportsOptions) => {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const executeReport = async (reportId: string, parameters?: Record<string, any>) => {
    // Implementation
  }

  const scheduleReport = async (reportId: string, schedule: ReportSchedule) => {
    // Implementation
  }

  const exportReport = async (reportId: string, format: OutputFormat) => {
    // Implementation
  }

  const createReport = async (report: Partial<Report>) => {
    // Implementation
  }

  return {
    reports,
    loading,
    error,
    executeReport,
    scheduleReport,
    exportReport,
    createReport,
    refetch: () => {/* Implementation */}
  }
}
```

### useAnalytics Hook

```typescript
interface UseAnalyticsOptions {
  metrics?: string[]
  period?: DatePeriod
  filters?: AnalyticsFilter[]
  includeGreekData?: boolean
}

const useAnalytics = (options: UseAnalyticsOptions) => {
  const [data, setData] = useState<AnalyticsData[]>([])
  const [insights, setInsights] = useState<AnalyticsInsight[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const runQuery = async (query: AnalyticsQuery) => {
    // Implementation
  }

  const createSegmentation = async (criteria: SegmentationCriteria) => {
    // Implementation
  }

  const generateForecast = async (metric: string, periods: number) => {
    // Implementation
  }

  const analyzeTrends = async (metrics: string[], period: DatePeriod) => {
    // Implementation
  }

  return {
    data,
    insights,
    loading,
    error,
    runQuery,
    createSegmentation,
    generateForecast,
    analyzeTrends,
    refetch: () => {/* Implementation */}
  }
}
```

### useGreekMarketData Hook

```typescript
const useGreekMarketData = () => {
  const [economicIndicators, setEconomicIndicators] = useState<GreekEconomicIndicator[]>([])
  const [regionalData, setRegionalData] = useState<GreekRegionalData[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const getEconomicData = async (period: DatePeriod) => {
    // Fetch from ELSTAT, Bank of Greece APIs
  }

  const getRegionalInsights = async (region: GreekRegion) => {
    // Regional analytics
  }

  const getSeasonalPatterns = async (industry?: string) => {
    // Greek seasonal business patterns
  }

  const getComplianceMetrics = async () => {
    // AADE compliance analytics
  }

  const formatGreekCurrency = (amount: number): string => {
    return new Intl.NumberFormat('el-GR', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount)
  }

  const formatGreekDate = (date: Date): string => {
    return new Intl.DateTimeFormat('el-GR').format(date)
  }

  const formatGreekNumber = (number: number): string => {
    return new Intl.NumberFormat('el-GR').format(number)
  }

  return {
    economicIndicators,
    regionalData,
    loading,
    error,
    getEconomicData,
    getRegionalInsights,
    getSeasonalPatterns,
    getComplianceMetrics,
    formatGreekCurrency,
    formatGreekDate,
    formatGreekNumber
  }
}
```

## Context Providers

### AnalyticsProvider

```typescript
interface AnalyticsContextType {
  // Dashboard state
  dashboards: Dashboard[]
  activeDashboard: Dashboard | null
  
  // Report state
  reports: Report[]
  reportExecutions: ReportExecution[]
  
  // Analytics state
  metrics: AnalyticsMetric[]
  insights: AnalyticsInsight[]
  
  // Greek market state
  economicIndicators: GreekEconomicIndicator[]
  regionalData: GreekRegionalData[]
  seasonalPatterns: SeasonalPattern[]
  
  // Data sources
  dataSources: DataSource[]
  
  // Actions
  createDashboard: (dashboard: Partial<Dashboard>) => Promise<void>
  executeReport: (reportId: string, parameters?: any) => Promise<void>
  runAnalyticsQuery: (query: AnalyticsQuery) => Promise<any>
  
  // Greek analytics actions
  getGreekMarketInsights: (region?: GreekRegion) => Promise<void>
  generateComplianceReport: (type: GreekReportType) => Promise<void>
}

const AnalyticsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Implementation
}
```

## Greek Analytics Features

### Economic Indicator Integration

- Real-time Greek GDP, inflation, unemployment data
- Bank of Greece economic statistics
- ELSTAT (Hellenic Statistical Authority) integration
- Tourism and shipping industry indicators
- Consumer confidence and business sentiment

### Regional Analytics

- Prefecture-level business performance
- Municipality demographic analysis
- Tourism region seasonal patterns
- Shipping route analytics
- Agricultural region productivity

### Compliance Reporting

- AADE tax compliance dashboard
- VAT collection and reporting metrics
- Employee social security compliance
- Environmental compliance tracking
- Industry-specific regulatory metrics

### Seasonal Pattern Analysis

- Orthodox holiday impact analysis
- Summer tourism season effects
- Winter shipping season patterns
- Agricultural season correlations
- School year business impact

### Currency and Economic Impact

- EUR fluctuation impact on business
- Import/export cost analysis
- Energy cost impact (significant in Greece)
- Tourism exchange rate effects
- Inflation impact on pricing strategies

## Testing Specifications

### Unit Tests

```typescript
describe('Analytics Models', () => {
  test('Dashboard model with Greek widgets', () => {})
  test('Report model with Greek templates', () => {})
  test('Analytics metric calculations', () => {})
  test('Greek economic data integration', () => {})
})

describe('Greek Analytics Utils', () => {
  test('Greek currency formatting', () => {})
  test('Greek date formatting', () => {})
  test('Regional data processing', () => {})
  test('Seasonal pattern detection', () => {})
})
```

### Integration Tests

```typescript
describe('Analytics APIs', () => {
  test('Dashboard data aggregation', () => {})
  test('Report execution and export', () => {})
  test('Real-time analytics queries', () => {})
  test('Greek data source integration', () => {})
  test('Compliance report generation', () => {})
})
```

### E2E Tests

```typescript
describe('Analytics Workflows', () => {
  test('Dashboard creation and customization', () => {})
  test('Report building and scheduling', () => {})
  test('Greek market insights generation', () => {})
  test('Predictive analytics execution', () => {})
  test('Multi-source data integration', () => {})
})
```

## Performance Considerations

### Real-time Analytics

- WebSocket connections for live data
- Efficient data aggregation pipelines
- Caching strategies for complex queries
- Background processing for heavy computations
- Optimized chart rendering

### Data Processing

- Incremental data updates
- Parallel query execution
- Memory-efficient data structures
- Compression for large datasets
- Intelligent data partitioning

### Greek Data Sources

- Reliable external API integration
- Fallback mechanisms for data unavailability
- Local caching of economic indicators
- Rate limiting compliance
- Data quality validation

## Success Metrics

### Business Intelligence

- Dashboard adoption rates
- Report usage frequency
- Data-driven decision increase
- Insight generation speed
- User self-service analytics

### Greek Market Insights

- Economic indicator accuracy
- Regional analysis usage
- Seasonal prediction accuracy
- Compliance reporting automation
- Market opportunity identification

### Technical Performance

- Query response times
- Data freshness metrics
- System availability
- Integration reliability
- User experience satisfaction
