# 07. Workflow Automation

## Overview

Advanced workflow automation system with visual process builder, Greek business rule engine, GDPR compliance automation, and integration with Greek regulatory processes.

## Core Features

### 7.1 Visual Workflow Builder

- **Drag-and-Drop Interface**: Visual process design with Greek business templates
- **Process Templates**: Pre-built Greek business workflows (invoicing, HR, compliance)
- **Conditional Logic**: Complex branching with Greek business rules
- **Parallel Processing**: Multi-path workflows for efficiency
- **Error Handling**: Comprehensive error management and recovery
- **Version Control**: Workflow versioning and rollback capabilities

### 7.2 Trigger System

- **Time-based Triggers**: Scheduled execution with Greek calendar awareness
- **Event-based Triggers**: Database changes, API calls, user actions
- **Greek Business Triggers**: Holiday scheduling, business hours, calendar events
- **Webhook Integration**: External system event processing
- **Email Triggers**: Automated email processing and routing
- **Form Submissions**: Lead capture and processing automation

### 7.3 Action Engine

- **Database Operations**: CRUD operations with audit trails
- **Communication Actions**: Email, SMS, notifications with Greek templates
- **Document Generation**: PDF, Word documents with Greek formatting
- **API Integrations**: External service calls and data synchronization
- **Approval Workflows**: Multi-level approval with Greek hierarchy
- **Task Assignment**: Automated task creation and assignment

### 7.4 Greek Business Rules

- **Holiday Management**: Orthodox calendar integration for scheduling
- **Working Hours**: Greek business hours enforcement
- **Data Privacy**: GDPR compliance and Greek data protection
- **Regional Rules**: Prefecture-specific business rule variations
- **Communication Standards**: Greek business communication patterns
- **Customer Service Rules**: Greek customer service best practices

### 7.5 Process Monitoring

- **Real-time Tracking**: Live workflow execution monitoring
- **Performance Metrics**: Execution time, success rates, bottleneck analysis
- **Error Reporting**: Detailed error logs with resolution suggestions
- **Audit Trails**: Complete process execution history
- **SLA Monitoring**: Service level agreement tracking
- **Greek Standards Monitoring**: Data privacy and communication standard adherence

## Data Models

### Workflow Model

```typescript
interface Workflow {
  id: string;
  name: string;
  description?: string;
  category: WorkflowCategory;
  type: "standard" | "template" | "system";
  status: "draft" | "active" | "paused" | "archived";
  version: string;
  isGreekCompliant: boolean;
  greekBusinessType?: GreekBusinessType;
  definition: WorkflowDefinition;
  triggers: WorkflowTrigger[];
  variables: WorkflowVariable[];
  permissions: WorkflowPermission[];
  settings: WorkflowSettings;
  customFields: Record<string, any>;
  statistics: WorkflowStatistics;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  lastUpdatedBy: string;
  tags: string[];
}

type WorkflowCategory =
  | "sales"
  | "customer_service"
  | "hr"
  | "marketing"
  | "data_management"
  | "greek_business"
  | "communication";

type GreekBusinessType =
  | "customer_onboarding"
  | "employee_onboarding"
  | "appointment_scheduling"
  | "communication_workflow"
  | "data_privacy_check"
  | "holiday_scheduling";

interface WorkflowDefinition {
  nodes: WorkflowNode[];
  connections: WorkflowConnection[];
  startNode: string;
  endNodes: string[];
  errorHandling: ErrorHandlingConfig;
}

interface WorkflowNode {
  id: string;
  type: NodeType;
  name: string;
  description?: string;
  position: NodePosition;
  configuration: NodeConfiguration;
  inputs: NodeInput[];
  outputs: NodeOutput[];
  customFields: Record<string, any>;
}

type NodeType =
  | "start"
  | "end"
  | "action"
  | "condition"
  | "delay"
  | "approval"
  | "notification"
  | "integration"
  | "greek_holiday_check"
  | "greek_business_hours"
  | "data_privacy_check";
```

### Workflow Execution Model

```typescript
interface WorkflowExecution {
  id: string;
  workflowId: string;
  workflowVersion: string;
  status: ExecutionStatus;
  startedAt: Date;
  completedAt?: Date;
  duration?: number; // milliseconds
  triggeredBy: ExecutionTrigger;
  context: ExecutionContext;
  currentNode?: string;
  processedNodes: ProcessedNode[];
  variables: Record<string, any>;
  errors: ExecutionError[];
  isGreekCompliant: boolean;
  greekComplianceChecks: GreekComplianceCheck[];
  customFields: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

type ExecutionStatus =
  | "running"
  | "waiting"
  | "paused"
  | "completed"
  | "failed"
  | "cancelled";

interface ProcessedNode {
  nodeId: string;
  nodeName: string;
  status: "completed" | "failed" | "skipped";
  startedAt: Date;
  completedAt?: Date;
  duration?: number;
  input: any;
  output?: any;
  error?: string;
  retryCount: number;
}

interface GreekComplianceCheck {
  type:
    | "gdpr"
    | "data_privacy"
    | "business_hours"
    | "holiday_check"
    | "communication";
  status: "passed" | "failed" | "warning";
  message: string;
  details?: any;
  checkedAt: Date;
}
```

### Workflow Trigger Model

```typescript
interface WorkflowTrigger {
  id: string;
  workflowId: string;
  type: TriggerType;
  name: string;
  description?: string;
  isActive: boolean;
  configuration: TriggerConfiguration;
  conditions: TriggerCondition[];
  isGreekSpecific: boolean;
  greekTriggerType?: GreekTriggerType;
  customFields: Record<string, any>;
  lastTriggered?: Date;
  triggerCount: number;
  createdAt: Date;
  updatedAt: Date;
}

type TriggerType =
  | "schedule"
  | "database_change"
  | "api_call"
  | "email_received"
  | "form_submission"
  | "file_upload"
  | "user_action"
  | "webhook"
  | "greek_holiday"
  | "business_hours"
  | "customer_service";

type GreekTriggerType =
  | "orthodox_holiday"
  | "business_hours"
  | "customer_service_hours"
  | "appointment_scheduling"
  | "communication_window"
  | "holiday_notification";

interface TriggerConfiguration {
  schedule?: ScheduleConfig;
  databaseConfig?: DatabaseTriggerConfig;
  apiConfig?: ApiTriggerConfig;
  emailConfig?: EmailTriggerConfig;
  greekConfig?: GreekTriggerConfig;
}

interface GreekTriggerConfig {
  respectHolidays: boolean;
  businessHoursOnly: boolean;
  excludeOrthodoxHolidays: boolean;
  regionSpecific?: string;
  aadeIntegration?: boolean;
}
```

### Workflow Action Model

```typescript
interface WorkflowAction {
  id: string;
  type: ActionType;
  name: string;
  description?: string;
  configuration: ActionConfiguration;
  isGreekSpecific: boolean;
  greekActionType?: GreekActionType;
  requiredPermissions: string[];
  customFields: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

type ActionType =
  | "send_email"
  | "send_sms"
  | "create_record"
  | "update_record"
  | "delete_record"
  | "api_call"
  | "generate_document"
  | "assign_task"
  | "send_notification"
  | "calculate_tax"
  | "submit_to_aade"
  | "generate_invoice";

type GreekActionType =
  | "calculate_greek_vat"
  | "submit_mydata"
  | "generate_greek_invoice"
  | "check_afm_validity"
  | "calculate_withholding_tax"
  | "generate_payroll"
  | "submit_ergani";

interface ActionConfiguration {
  emailConfig?: EmailActionConfig;
  databaseConfig?: DatabaseActionConfig;
  apiConfig?: ApiActionConfig;
  documentConfig?: DocumentActionConfig;
  greekConfig?: GreekActionConfig;
}

interface GreekActionConfig {
  vatRates: GreekVATRates;
  aadeCredentials?: AADECredentials;
  regionSettings?: GreekRegionSettings;
  complianceChecks: string[];
  documentLanguage: "el" | "en" | "both";
}
```

## API Endpoints

### Workflow Management APIs

```typescript
// Workflow CRUD
GET /api/workflows
POST /api/workflows
GET /api/workflows/:id
PUT /api/workflows/:id
DELETE /api/workflows/:id
POST /api/workflows/:id/activate
POST /api/workflows/:id/pause
POST /api/workflows/:id/archive

// Workflow Versions
GET /api/workflows/:id/versions
POST /api/workflows/:id/versions
GET /api/workflows/:id/versions/:version
POST /api/workflows/:id/versions/:version/restore

// Workflow Templates
GET /api/workflow-templates
GET /api/workflow-templates/greek
POST /api/workflows/from-template/:templateId

// Workflow Testing
POST /api/workflows/:id/test
POST /api/workflows/:id/validate
POST /api/workflows/:id/simulate
```

### Workflow Execution APIs

```typescript
// Execution Management
GET /api/workflow-executions
POST /api/workflow-executions
GET /api/workflow-executions/:id
PUT /api/workflow-executions/:id
DELETE /api/workflow-executions/:id
POST /api/workflow-executions/:id/pause
POST /api/workflow-executions/:id/resume
POST /api/workflow-executions/:id/cancel

// Execution Monitoring
GET /api/workflow-executions/:id/status
GET /api/workflow-executions/:id/logs
GET /api/workflow-executions/:id/variables
PUT /api/workflow-executions/:id/variables

// Execution Analytics
GET /api/workflow-executions/statistics
GET /api/workflow-executions/performance
GET /api/workflow-executions/errors
```

### Trigger Management APIs

```typescript
// Trigger CRUD
GET /api/workflow-triggers
POST /api/workflow-triggers
GET /api/workflow-triggers/:id
PUT /api/workflow-triggers/:id
DELETE /api/workflow-triggers/:id
POST /api/workflow-triggers/:id/activate
POST /api/workflow-triggers/:id/deactivate

// Trigger Testing
POST /api/workflow-triggers/:id/test
GET /api/workflow-triggers/:id/history
POST /api/workflow-triggers/manual/:workflowId

// Greek Triggers
GET /api/workflow-triggers/greek-holidays
GET /api/workflow-triggers/business-hours
POST /api/workflow-triggers/aade-deadline
GET /api/workflow-triggers/tax-calendar
```

### Greek Business APIs

```typescript
// Greek Workflow Actions
POST / api / workflows / actions / calculate - greek - vat;
POST / api / workflows / actions / submit - mydata;
POST / api / workflows / actions / validate - afm;
POST / api / workflows / actions / calculate - withholding - tax;
POST / api / workflows / actions / generate - greek - document;

// Greek Compliance
POST / api / workflows / compliance / check;
GET / api / workflows / compliance / requirements;
POST / api / workflows / compliance / validate;

// AADE Integration
POST / api / workflows / aade / authenticate;
POST / api / workflows / aade / submit;
GET / api / workflows / aade / status;
POST / api / workflows / aade / cancel;
```

## UI Components

### WorkflowBuilder Component

```typescript
interface WorkflowBuilderProps {
  workflowId?: string;
  template?: WorkflowTemplate;
  onSave?: (workflow: Workflow) => void;
  showGreekTemplates?: boolean;
  allowGreekActions?: boolean;
}

const WorkflowBuilder: React.FC<WorkflowBuilderProps> = ({
  workflowId,
  template,
  onSave,
  showGreekTemplates = true,
  allowGreekActions = true,
}) => {
  // Component implementation
};
```

### WorkflowCanvas Component

```typescript
interface WorkflowCanvasProps {
  workflow: Workflow;
  isEditable?: boolean;
  onNodeAdd?: (node: WorkflowNode) => void;
  onNodeUpdate?: (nodeId: string, updates: Partial<WorkflowNode>) => void;
  onNodeDelete?: (nodeId: string) => void;
  showGreekActions?: boolean;
}

const WorkflowCanvas: React.FC<WorkflowCanvasProps> = ({
  workflow,
  isEditable = true,
  onNodeAdd,
  onNodeUpdate,
  onNodeDelete,
  showGreekActions = true,
}) => {
  // Component implementation
};
```

### WorkflowExecutionMonitor Component

```typescript
interface WorkflowExecutionMonitorProps {
  workflowId?: string;
  executionId?: string;
  realtime?: boolean;
  onExecutionSelect?: (execution: WorkflowExecution) => void;
  showGreekCompliance?: boolean;
}

const WorkflowExecutionMonitor: React.FC<WorkflowExecutionMonitorProps> = ({
  workflowId,
  executionId,
  realtime = true,
  onExecutionSelect,
  showGreekCompliance = true,
}) => {
  // Component implementation
};
```

### GreekWorkflowTemplates Component

```typescript
interface GreekWorkflowTemplatesProps {
  category?: GreekBusinessType;
  onTemplateSelect?: (template: WorkflowTemplate) => void;
  showDescription?: boolean;
}

const GreekWorkflowTemplates: React.FC<GreekWorkflowTemplatesProps> = ({
  category,
  onTemplateSelect,
  showDescription = true,
}) => {
  // Component implementation
};
```

### WorkflowTriggerManager Component

```typescript
interface WorkflowTriggerManagerProps {
  workflowId: string;
  triggers: WorkflowTrigger[];
  onTriggerUpdate?: (trigger: WorkflowTrigger) => void;
  showGreekTriggers?: boolean;
}

const WorkflowTriggerManager: React.FC<WorkflowTriggerManagerProps> = ({
  workflowId,
  triggers,
  onTriggerUpdate,
  showGreekTriggers = true,
}) => {
  // Component implementation
};
```

## Custom Hooks

### useWorkflows Hook

```typescript
interface UseWorkflowsOptions {
  category?: WorkflowCategory;
  status?: WorkflowStatus;
  includeGreek?: boolean;
}

const useWorkflows = (options: UseWorkflowsOptions) => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createWorkflow = async (workflow: Partial<Workflow>) => {
    // Implementation
  };

  const updateWorkflow = async (
    workflowId: string,
    updates: Partial<Workflow>
  ) => {
    // Implementation
  };

  const activateWorkflow = async (workflowId: string) => {
    // Implementation
  };

  const pauseWorkflow = async (workflowId: string) => {
    // Implementation
  };

  const executeWorkflow = async (workflowId: string, context?: any) => {
    // Implementation
  };

  return {
    workflows,
    loading,
    error,
    createWorkflow,
    updateWorkflow,
    activateWorkflow,
    pauseWorkflow,
    executeWorkflow,
    refetch: () => {
      /* Implementation */
    },
  };
};
```

### useWorkflowExecution Hook

```typescript
interface UseWorkflowExecutionOptions {
  executionId: string;
  realtime?: boolean;
}

const useWorkflowExecution = (options: UseWorkflowExecutionOptions) => {
  const [execution, setExecution] = useState<WorkflowExecution | null>(null);
  const [logs, setLogs] = useState<ExecutionLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const pauseExecution = async () => {
    // Implementation
  };

  const resumeExecution = async () => {
    // Implementation
  };

  const cancelExecution = async () => {
    // Implementation
  };

  const retryExecution = async () => {
    // Implementation
  };

  const updateVariables = async (variables: Record<string, any>) => {
    // Implementation
  };

  return {
    execution,
    logs,
    loading,
    error,
    pauseExecution,
    resumeExecution,
    cancelExecution,
    retryExecution,
    updateVariables,
    refetch: () => {
      /* Implementation */
    },
  };
};
```

### useGreekWorkflows Hook

```typescript
const useGreekWorkflows = () => {
  const [templates, setTemplates] = useState<GreekWorkflowTemplate[]>([]);
  const [holidays, setHolidays] = useState<GreekHoliday[]>([]);
  const [businessRules, setBusinessRules] = useState<GreekBusinessRule[]>([]);

  const calculateGreekVAT = (amount: number, vatRate: GreekVATRate): number => {
    const rates = {
      standard: 0.24,
      reduced: 0.13,
      super_reduced: 0.06,
      exempt: 0,
    };
    return amount * rates[vatRate];
  };

  const checkAADECompliance = async (
    invoice: any
  ): Promise<AADEComplianceResult> => {
    // AADE compliance validation
    return {
      isCompliant: true,
      issues: [],
      recommendations: [],
    };
  };

  const submitToMyDATA = async (
    invoice: any
  ): Promise<MyDATASubmissionResult> => {
    // myDATA submission
    return {
      success: true,
      mark: "",
      uid: "",
    };
  };

  const getOrthodoxHolidays = (year: number): GreekHoliday[] => {
    // Calculate Orthodox holidays for given year
    return [];
  };

  const isGreekBusinessDay = (date: Date): boolean => {
    const day = date.getDay();
    const hour = date.getHours();

    // Monday-Friday, 9-17, excluding lunch 13-14
    return (
      day >= 1 &&
      day <= 5 &&
      ((hour >= 9 && hour < 13) || (hour >= 14 && hour < 17))
    );
  };

  const validateAFM = async (afm: string): Promise<AFMValidationResult> => {
    // AFM validation logic
    return {
      isValid: true,
      businessName: "",
      status: "active",
    };
  };

  return {
    templates,
    holidays,
    businessRules,
    calculateGreekVAT,
    checkAADECompliance,
    submitToMyDATA,
    getOrthodoxHolidays,
    isGreekBusinessDay,
    validateAFM,
  };
};
```

### useWorkflowBuilder Hook

```typescript
interface UseWorkflowBuilderOptions {
  workflowId?: string;
  template?: WorkflowTemplate;
}

const useWorkflowBuilder = (options: UseWorkflowBuilderOptions) => {
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [nodes, setNodes] = useState<WorkflowNode[]>([]);
  const [connections, setConnections] = useState<WorkflowConnection[]>([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const addNode = (nodeType: NodeType, position: NodePosition) => {
    // Implementation
  };

  const updateNode = (nodeId: string, updates: Partial<WorkflowNode>) => {
    // Implementation
  };

  const deleteNode = (nodeId: string) => {
    // Implementation
  };

  const connectNodes = (fromNodeId: string, toNodeId: string) => {
    // Implementation
  };

  const disconnectNodes = (connectionId: string) => {
    // Implementation
  };

  const validateWorkflow = (): WorkflowValidationResult => {
    // Implementation
  };

  const saveWorkflow = async () => {
    // Implementation
  };

  return {
    workflow,
    nodes,
    connections,
    selectedNode,
    addNode,
    updateNode,
    deleteNode,
    connectNodes,
    disconnectNodes,
    validateWorkflow,
    saveWorkflow,
    setSelectedNode,
  };
};
```

## Context Providers

### WorkflowProvider

```typescript
interface WorkflowContextType {
  // Workflow state
  workflows: Workflow[];
  activeWorkflows: Workflow[];
  workflowTemplates: WorkflowTemplate[];

  // Execution state
  executions: WorkflowExecution[];
  runningExecutions: WorkflowExecution[];

  // Trigger state
  triggers: WorkflowTrigger[];
  activeTriggers: WorkflowTrigger[];

  // Greek features
  greekTemplates: GreekWorkflowTemplate[];
  greekHolidays: GreekHoliday[];
  greekBusinessHours: GreekBusinessHours[];

  // Actions
  createWorkflow: (workflow: Partial<Workflow>) => Promise<void>;
  executeWorkflow: (workflowId: string, context?: any) => Promise<void>;
  pauseExecution: (executionId: string) => Promise<void>;

  // Greek actions
  validateGreekHoliday: (date: Date) => Promise<boolean>;
  checkBusinessHours: (date: Date) => Promise<boolean>;
  validateDataPrivacy: (workflow: Workflow) => Promise<ComplianceResult>;
}

const WorkflowProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  // Implementation
};
```

## Greek CRM Workflow Features

### Orthodox Calendar Integration

- Automatic holiday detection and scheduling
- Business day calculations for appointments
- Seasonal communication adjustments
- Religious holiday awareness for customer outreach
- Greek business hours validation

### Greek Communication Workflows

- Greek language email template automation
- SMS messaging with Greek formatting
- Customer follow-up scheduling around holidays
- Greek customer service hour enforcement
- Cultural communication pattern automation

### Greek Customer Process Templates

- Customer onboarding with AFM validation
- Lead qualification with Greek business context
- Appointment scheduling around Greek holidays
- Customer service escalation with Greek business rules
- Data privacy consent management (GDPR compliance)

### Data Privacy Automation

- GDPR data processing workflows
- Customer consent management
- Data retention policy enforcement
- Privacy impact assessment automation
- Audit trail generation for data handling

## Testing Specifications

### Unit Tests

```typescript
describe("Workflow Models", () => {
  test("Workflow definition validation", () => {});
  test("Greek workflow template structure", () => {});
  test("Trigger condition evaluation", () => {});
  test("Action configuration validation", () => {});
});

describe("Greek Workflow Utils", () => {
  test("Orthodox holiday calculation", () => {});
  test("Business hours validation", () => {});
  test("Greek communication formatting", () => {});
  test("Data privacy compliance checking", () => {});
});
```

### Integration Tests

```typescript
describe("Workflow APIs", () => {
  test("Workflow creation and execution", () => {});
  test("Trigger activation and firing", () => {});
  test("Greek action execution", () => {});
  test("Holiday awareness workflows", () => {});
  test("Error handling and recovery", () => {});
});
```

### E2E Tests

```typescript
describe("Workflow End-to-End", () => {
  test("Customer onboarding workflow with Greek validation", () => {});
  test("Lead qualification workflow", () => {});
  test("Customer service escalation workflow", () => {});
  test("Greek communication workflow", () => {});
  test("Holiday-aware scheduling workflow", () => {});
});
```

## Performance Considerations

### Execution Engine

- Parallel node execution where possible
- Efficient state management
- Memory optimization for long-running workflows
- Queue management for high-volume execution
- Resource limit enforcement

### Greek CRM Performance

- Holiday calendar cache optimization
- Business hours calculation efficiency
- Greek text processing performance
- Communication template rendering speed
- Customer data validation performance

### Monitoring and Optimization

- Real-time performance metrics
- Bottleneck identification
- Resource usage tracking
- Execution time optimization
- Error rate monitoring

## Success Metrics

### Automation Efficiency

- Process automation percentage
- Manual task reduction
- Execution time improvement
- Error rate reduction
- User productivity increase

### Greek CRM Standards

- Data privacy compliance rate
- Greek communication standard adherence
- Holiday scheduling accuracy
- Business hours compliance
- Customer satisfaction with Greek service standards

### Business Process Improvement

- Workflow adoption rates
- Process standardization
- Quality consistency
- Cost reduction through automation
- Customer satisfaction improvement
