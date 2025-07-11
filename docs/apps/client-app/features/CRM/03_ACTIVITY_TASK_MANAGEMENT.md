# 03_ACTIVITY_TASK_MANAGEMENT - Productivity Engine

## Document Information
- **Feature**: Activity & Task Management (Calendar, Tasks, Communications)
- **Priority**: ⭐ PRODUCTIVITY - Team organization and efficiency
- **Implementation**: Month 2-3 (Phase 1)
- **Dependencies**: 01_Customer_Management, 02_Sales_Management
- **Impact**: Team productivity and customer engagement tracking

## 🎯 Feature Overview

Activity & Task Management provides comprehensive scheduling, task tracking, and communication logging with Greek business calendar integration and full customization.

### Core Capabilities
- **Dynamic Calendar System**: Greek holidays, business hours, custom scheduling
- **Flexible Task Management**: Custom task types, priorities, and workflows
- **Communication Tracking**: Calls, emails, meetings with CRM integration
- **Team Collaboration**: Shared calendars, task assignments, notifications
- **Greek Integration**: Orthodox calendar, Greek business practices

---

## 📋 Screens & User Interface

### 1. Calendar Management

#### Calendar Dashboard (`/calendar`)
```typescript
interface CalendarDashboardScreen {
  // Multi-view calendar (day, week, month, agenda)
  // Greek holiday integration (Orthodox calendar)
  // Custom activity types and colors
  // Team calendar overlay
  // Quick activity creation and editing
}
```

#### Activity Detail (`/activities/:id`)
```typescript
interface ActivityDetailScreen {
  // Dynamic activity forms with custom fields
  // Related records (contacts, accounts, opportunities)
  // Communication history and outcomes
  // Follow-up scheduling and reminders
  // Greek date/time formatting
}
```

### 2. Task Management

#### Task Board (`/tasks/board`)
```typescript
interface TaskBoardScreen {
  // Kanban-style task organization
  // Custom task statuses and workflows
  // Team assignment and collaboration
  // Priority management and deadlines
  // Custom field display in cards
}
```

#### Task List (`/tasks`)
```typescript
interface TaskListScreen {
  // Filterable task grid with custom columns
  // Bulk operations and assignments
  // Due date tracking and notifications
  // Performance metrics and analytics
  // Greek business hour calculations
}
```

---

## 🗄️ Data Models (Dynamic Schema)

### Activity Model
```typescript
interface Activity {
  id: string;
  type: 'call' | 'email' | 'meeting' | 'task' | 'note' | string; // Extensible types
  subject: string;
  description?: string;
  
  // Scheduling (Greek timezone aware)
  startDate: Date;
  endDate?: Date;
  allDay?: boolean;
  timezone: string;              // Default: Europe/Athens
  
  // Greek Calendar Integration
  respectGreekHolidays?: boolean;
  businessHoursOnly?: boolean;
  
  // Relationships
  contactId?: string;
  accountId?: string;
  opportunityId?: string;
  
  // Status and Management
  status: 'planned' | 'in-progress' | 'completed' | 'cancelled' | string;
  priority: 'low' | 'medium' | 'high' | 'urgent' | string;
  
  // Assignment
  assignedUserId: string;
  teamIds?: string[];
  
  // Communication Tracking
  outcome?: string;
  nextAction?: string;
  followUpDate?: Date;
  
  // Dynamic Custom Fields
  customFields: Record<string, any>;
  
  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

interface ActivityType {
  id: string;
  name: string;
  color: string;
  icon: string;
  defaultDuration: number;       // Minutes
  requiresLocation?: boolean;
  allowsRecurrence?: boolean;
  customFields?: CustomField[];  // Type-specific fields
  
  // Greek Business Rules
  respectBusinessHours?: boolean;
  blockOnHolidays?: boolean;
}
```

### Task Model
```typescript
interface Task {
  id: string;
  name: string;
  description?: string;
  
  // Task Management
  status: string;                // Customizable statuses
  priority: string;              // Customizable priorities
  dueDate?: Date;
  estimatedHours?: number;
  actualHours?: number;
  
  // Greek Business Context
  workingDaysOnly?: boolean;     // Exclude weekends/holidays
  businessHoursRequired?: boolean;
  
  // Relationships
  parentTaskId?: string;         // Subtasks
  projectId?: string;
  contactId?: string;
  accountId?: string;
  opportunityId?: string;
  
  // Assignment and Collaboration
  assignedUserId?: string;
  reporterId: string;
  watcherIds?: string[];
  teamIds?: string[];
  
  // Progress Tracking
  percentComplete: number;
  blockedBy?: string[];          // Dependency tracking
  blocking?: string[];
  
  // Dynamic Custom Fields
  customFields: Record<string, any>;
  
  // Audit
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  updatedBy: string;
}

interface TaskStatus {
  id: string;
  name: string;
  order: number;
  color: string;
  isCompleted: boolean;
  isBlocked: boolean;
  // Custom validation rules per status
  requiredFields?: string[];
}
```

---

## 🔌 API Specifications

### Calendar APIs
```typescript
// GET /api/calendar/activities - Get calendar activities
interface GetActivitiesRequest {
  startDate: Date;
  endDate: Date;
  types?: string[];
  assignedUserId?: string;
  includeGreekHolidays?: boolean;
}

interface GetActivitiesResponse {
  activities: Activity[];
  greekHolidays?: GreekHoliday[];
  businessHours: BusinessHours;
}

// POST /api/calendar/check-availability - Check time slot availability
interface CheckAvailabilityRequest {
  startDate: Date;
  endDate: Date;
  userIds: string[];
  respectBusinessHours?: boolean;
  respectHolidays?: boolean;
}

// GET /api/calendar/greek-holidays - Greek Orthodox calendar
interface GreekHoliday {
  date: Date;
  name: string;
  type: 'fixed' | 'moveable' | 'orthodox';
  isBusinessDay: boolean;
}
```

### Task APIs
```typescript
// GET /api/tasks/board - Get task board data
interface GetTaskBoardResponse {
  statuses: TaskStatus[];
  tasks: Record<string, Task[]>; // Grouped by status
  customFields: CustomField[];
}

// POST /api/tasks/:id/time-log - Log time against task
interface TimeLogRequest {
  hours: number;
  description?: string;
  date?: Date;
  billable?: boolean;
}

// GET /api/tasks/analytics - Task performance analytics
interface TaskAnalyticsResponse {
  averageCompletionTime: number;
  overdueTasks: number;
  productivityMetrics: {
    userId: string;
    tasksCompleted: number;
    averageTime: number;
    efficiency: number;
  }[];
}
```

---

## ⚛️ React Components

### Calendar Components
```typescript
// Greek Calendar Component
interface GreekCalendarProps {
  activities: Activity[];
  greekHolidays: GreekHoliday[];
  onActivityCreate: (activity: Partial<Activity>) => void;
  customFields: CustomField[];
}

const GreekCalendar: React.FC<GreekCalendarProps> = ({ activities, greekHolidays, customFields }) => {
  const { formatGreekDate, isGreekHoliday } = useGreekCalendar();
  
  const eventStyleGetter = (event: Activity) => ({
    style: {
      backgroundColor: getActivityColor(event.type),
      borderColor: isGreekHoliday(event.startDate) ? '#ff6b6b' : undefined
    }
  });
  
  return (
    <BigCalendar
      localizer={greekLocalizer}
      events={activities}
      eventPropGetter={eventStyleGetter}
      components={{
        event: ({ event }) => (
          <ActivityEvent
            activity={event}
            customFields={customFields}
          />
        ),
        month: {
          dateHeader: ({ date }) => (
            <GreekDateHeader
              date={date}
              isHoliday={isGreekHoliday(date)}
            />
          )
        }
      }}
    />
  );
};

// Dynamic Activity Form
interface ActivityFormProps {
  activity?: Activity;
  activityTypes: ActivityType[];
  onSave: (activity: Activity) => void;
}

const ActivityForm: React.FC<ActivityFormProps> = ({ activity, activityTypes }) => {
  const [selectedType, setSelectedType] = useState<ActivityType>();
  const { form, updateField } = useDynamicForm(activity, selectedType?.customFields || []);
  const { checkGreekBusinessHours } = useGreekCalendar();
  
  const handleTypeChange = (typeId: string) => {
    const type = activityTypes.find(t => t.id === typeId);
    setSelectedType(type);
    
    if (type?.defaultDuration) {
      const endDate = new Date(form.startDate);
      endDate.setMinutes(endDate.getMinutes() + type.defaultDuration);
      updateField('endDate', endDate);
    }
  };
  
  return (
    <FormBuilder>
      <Select
        label="Τύπος Δραστηριότητας"
        options={activityTypes}
        onChange={handleTypeChange}
      />
      
      <GreekDateTimePicker
        label="Ημερομηνία & Ώρα"
        value={form.startDate}
        onChange={(date) => updateField('startDate', date)}
        businessHoursOnly={selectedType?.respectBusinessHours}
        excludeHolidays={selectedType?.blockOnHolidays}
      />
      
      {/* Dynamic Custom Fields for Selected Type */}
      {selectedType?.customFields?.map(field => (
        <DynamicFieldInput
          key={field.name}
          field={field}
          value={form.customFields[field.name]}
          onChange={(value) => updateField(field.name, value)}
        />
      ))}
    </FormBuilder>
  );
};
```

### Task Management Components
```typescript
// Dynamic Task Board
interface TaskBoardProps {
  statuses: TaskStatus[];
  tasks: Record<string, Task[]>;
  customFields: CustomField[];
  onTaskMove: (taskId: string, statusId: string) => void;
}

const TaskBoard: React.FC<TaskBoardProps> = ({ statuses, tasks, customFields }) => {
  const { handleDragEnd } = useTaskDragDrop();
  
  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <BoardContainer>
        {statuses.map(status => (
          <TaskColumn
            key={status.id}
            status={status}
            tasks={tasks[status.id] || []}
            customFields={customFields.filter(f => f.showInBoard)}
          />
        ))}
      </BoardContainer>
    </DragDropContext>
  );
};

// Greek Time Tracking Component
interface TimeTrackingProps {
  task: Task;
  onTimeLog: (hours: number, description: string) => void;
}

const GreekTimeTracking: React.FC<TimeTrackingProps> = ({ task, onTimeLog }) => {
  const { calculateWorkingHours } = useGreekWorkingTime();
  const [timeEntry, setTimeEntry] = useState({ hours: 0, description: '' });
  
  const handleSubmit = () => {
    const workingHours = calculateWorkingHours(timeEntry.hours, new Date());
    onTimeLog(workingHours, timeEntry.description);
  };
  
  return (
    <TimeTrackingForm>
      <Input
        label="Ώρες Εργασίας"
        type="number"
        step="0.25"
        value={timeEntry.hours}
        onChange={(e) => setTimeEntry(prev => ({ ...prev, hours: +e.target.value }))}
      />
      
      <TextArea
        label="Περιγραφή"
        value={timeEntry.description}
        onChange={(e) => setTimeEntry(prev => ({ ...prev, description: e.target.value }))}
      />
      
      <Button onClick={handleSubmit}>
        Καταγραφή Χρόνου
      </Button>
    </TimeTrackingForm>
  );
};
```

---

## 🪝 Custom Hooks

### Greek Calendar Hooks
```typescript
const useGreekCalendar = () => {
  const [greekHolidays, setGreekHolidays] = useState<GreekHoliday[]>([]);
  
  useEffect(() => {
    loadGreekHolidays(new Date().getFullYear());
  }, []);
  
  const isGreekHoliday = (date: Date): boolean => {
    return greekHolidays.some(holiday => 
      isSameDay(holiday.date, date)
    );
  };
  
  const isGreekBusinessDay = (date: Date): boolean => {
    const dayOfWeek = date.getDay();
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6; // Sunday or Saturday
    return !isWeekend && !isGreekHoliday(date);
  };
  
  const formatGreekDate = (date: Date): string => {
    return new Intl.DateTimeFormat('el-GR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };
  
  const addBusinessDays = (startDate: Date, days: number): Date => {
    let currentDate = new Date(startDate);
    let addedDays = 0;
    
    while (addedDays < days) {
      currentDate.setDate(currentDate.getDate() + 1);
      if (isGreekBusinessDay(currentDate)) {
        addedDays++;
      }
    }
    
    return currentDate;
  };
  
  return {
    greekHolidays,
    isGreekHoliday,
    isGreekBusinessDay,
    formatGreekDate,
    addBusinessDays
  };
};

const useGreekWorkingTime = () => {
  const businessHours = {
    start: 9,  // 9:00 AM
    end: 17,   // 5:00 PM
    lunchStart: 13, // 1:00 PM
    lunchEnd: 14,   // 2:00 PM
  };
  
  const calculateWorkingHours = (totalHours: number, date: Date): number => {
    const { isGreekBusinessDay } = useGreekCalendar();
    
    if (!isGreekBusinessDay(date)) {
      return 0; // No work on holidays/weekends
    }
    
    const maxDailyHours = businessHours.end - businessHours.start - 1; // Excluding lunch
    return Math.min(totalHours, maxDailyHours);
  };
  
  const isWithinBusinessHours = (date: Date): boolean => {
    const hour = date.getHours();
    return (hour >= businessHours.start && hour < businessHours.lunchStart) ||
           (hour >= businessHours.lunchEnd && hour < businessHours.end);
  };
  
  return {
    businessHours,
    calculateWorkingHours,
    isWithinBusinessHours
  };
};
```

### Task Management Hooks
```typescript
const useTaskStatuses = () => {
  return useQuery({
    queryKey: ['task-statuses'],
    queryFn: () => taskApi.getStatuses(),
    staleTime: 15 * 60 * 1000, // 15 minutes
  });
};

const useTaskDragDrop = () => {
  const { mutate: moveTask } = useMoveTask();
  
  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;
    
    const taskId = result.draggableId;
    const newStatusId = result.destination.droppableId;
    
    moveTask({ taskId, statusId: newStatusId });
  };
  
  return { handleDragEnd };
};

const useActivityReminders = () => {
  const { mutate: scheduleReminder } = useScheduleReminder();
  
  const scheduleGreekBusinessReminder = (activity: Activity, reminderMinutes: number) => {
    const { addBusinessDays } = useGreekCalendar();
    
    let reminderDate = new Date(activity.startDate);
    reminderDate.setMinutes(reminderDate.getMinutes() - reminderMinutes);
    
    // If reminder falls on non-business time, move to previous business day
    if (!isGreekBusinessDay(reminderDate)) {
      reminderDate = addBusinessDays(reminderDate, -1);
      reminderDate.setHours(16, 0, 0, 0); // 4 PM previous business day
    }
    
    scheduleReminder({
      activityId: activity.id,
      reminderDate,
      type: 'email',
      message: `Υπενθύμιση: ${activity.subject}`
    });
  };
  
  return { scheduleGreekBusinessReminder };
};
```

---

## 🧪 Testing Specifications

### Greek Calendar Tests
```typescript
describe('Greek Calendar Integration', () => {
  it('identifies Greek Orthodox holidays correctly', () => {
    const { isGreekHoliday } = useGreekCalendar();
    
    // Test fixed holidays
    const epiphany2024 = new Date('2024-01-06');
    expect(isGreekHoliday(epiphany2024)).toBe(true);
    
    // Test moveable holidays (Easter-dependent)
    const easter2024 = new Date('2024-05-05'); // Orthodox Easter 2024
    expect(isGreekHoliday(easter2024)).toBe(true);
  });
  
  it('calculates business days excluding Greek holidays', () => {
    const { addBusinessDays } = useGreekCalendar();
    
    const startDate = new Date('2024-01-04'); // Thursday before Epiphany
    const result = addBusinessDays(startDate, 2);
    
    // Should skip weekend and Epiphany (Jan 6), land on Tuesday Jan 9
    expect(result.toDateString()).toBe(new Date('2024-01-09').toDateString());
  });
  
  it('respects Greek business hours in scheduling', () => {
    const { isWithinBusinessHours } = useGreekWorkingTime();
    
    expect(isWithinBusinessHours(new Date('2024-01-01 10:00'))).toBe(true);  // 10 AM
    expect(isWithinBusinessHours(new Date('2024-01-01 13:30'))).toBe(false); // Lunch time
    expect(isWithinBusinessHours(new Date('2024-01-01 18:00'))).toBe(false); // After hours
  });
});

describe('Dynamic Task Management', () => {
  it('validates required fields per task status', async () => {
    const taskStatus = {
      id: 'in-review',
      name: 'Σε Αναθεώρηση',
      requiredFields: ['reviewerId', 'estimatedHours']
    };
    
    const task = {
      id: '1',
      name: 'Test Task',
      customFields: { reviewerId: 'user1' } // Missing estimatedHours
    };
    
    const validation = validateTaskForStatus(task, taskStatus);
    
    expect(validation.valid).toBe(false);
    expect(validation.errors).toContain({
      field: 'estimatedHours',
      message: 'Εκτιμώμενες ώρες απαιτούνται για Σε Αναθεώρηση'
    });
  });
  
  it('handles task drag and drop with status validation', async () => {
    const { handleDragEnd } = useTaskDragDrop();
    
    const dragResult = {
      draggableId: 'task-1',
      destination: { droppableId: 'completed' }
    };
    
    // Mock task that doesn't meet completion requirements
    mockTask.mockReturnValue({
      id: 'task-1',
      customFields: { percentComplete: 50 } // Not 100% complete
    });
    
    await expect(handleDragEnd(dragResult))
      .rejects.toThrow('Task must be 100% complete');
  });
});

describe('Activity E2E Workflows', () => {
  it('creates activity with Greek business hour validation', async () => {
    await page.goto('/calendar');
    await page.click('[data-testid="new-activity"]');
    
    // Try to schedule during lunch time
    await page.fill('[data-testid="activity-name"]', 'Σύσκεψη με πελάτη');
    await page.fill('[data-testid="start-time"]', '13:30'); // Lunch time
    
    await page.click('[data-testid="save-activity"]');
    
    // Should show business hours warning
    await expect(page.locator('.business-hours-warning'))
      .toContainText('Η ώρα είναι εκτός εργάσιμων ωρών');
    
    // Correct the time
    await page.fill('[data-testid="start-time"]', '15:00'); // 3 PM
    await page.click('[data-testid="save-activity"]');
    
    await expect(page.locator('.success-message'))
      .toContainText('Επιτυχής δημιουργία δραστηριότητας');
  });
});
```

---

## 📋 Implementation Checklist

### Phase 1: Calendar Foundation (Week 1-2)
- [ ] **Greek Calendar Engine**: Orthodox holidays, business days
- [ ] **Activity CRUD**: Dynamic activity types with custom fields
- [ ] **Calendar Views**: Day/Week/Month with Greek formatting
- [ ] **Business Hours**: Greek working time validation

### Phase 2: Task Management (Week 3-4)
- [ ] **Task Board**: Kanban with custom statuses
- [ ] **Task CRUD**: Dynamic task types and workflows
- [ ] **Time Tracking**: Greek working hours calculation
- [ ] **Team Collaboration**: Assignment and notifications

### Phase 3: Advanced Features (Week 5-6)
- [ ] **Recurrence Engine**: Recurring activities and tasks
- [ ] **Reminder System**: Business-aware notifications
- [ ] **Analytics Dashboard**: Productivity metrics
- [ ] **Mobile Calendar**: Responsive calendar interface

---

**Status**: Specification Complete  
**Next**: 04_COMMUNICATION_COLLABORATION.md  
**Key Features**: Greek calendar integration, dynamic custom fields  
**Dependencies**: Customer & Sales Management 