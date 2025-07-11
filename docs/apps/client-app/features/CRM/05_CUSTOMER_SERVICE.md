# 05. Customer Service Management

## Overview

Comprehensive customer service platform with ticketing, knowledge base, live chat, and Greek customer protection compliance (consumer rights, warranty laws, return policies).

## Core Features

### 5.1 Ticket Management System

- **Multi-channel Tickets**: Email, phone, chat, web form, social media
- **Greek Priority Levels**: Based on Greek consumer protection urgency
- **SLA Management**: Response times aligned with Greek business standards
- **Escalation Rules**: Automatic escalation with Greek management hierarchy
- **Ticket Categories**: Greek industry-specific categorization
- **Resolution Tracking**: Time-to-resolution metrics

### 5.2 Knowledge Base System

- **Multilingual Content**: Greek and English knowledge articles
- **FAQ Management**: Common Greek customer queries
- **Video Tutorials**: Screen recordings with Greek subtitles
- **Document Library**: Greek legal documents, warranty terms
- **Search Engine**: Advanced search with Greek language support
- **Usage Analytics**: Article popularity and effectiveness

### 5.3 Live Chat & Support

- **Real-time Chat**: WebSocket-based messaging
- **Chat Routing**: Skills-based routing with Greek language preference
- **Canned Responses**: Greek customer service templates
- **File Sharing**: Secure document exchange
- **Chat History**: Complete conversation tracking
- **Visitor Tracking**: Anonymous visitor support

### 5.4 Customer Portal

- **Self-service Portal**: Greek interface for common tasks
- **Ticket Submission**: Easy ticket creation forms
- **Status Tracking**: Real-time ticket status updates
- **Knowledge Access**: Customer-facing knowledge base
- **Account Management**: Profile and preference management
- **Communication History**: All customer interactions

### 5.5 Greek Compliance Features

- **Consumer Rights**: Greek consumer protection law compliance
- **Warranty Management**: Greek warranty law implementation
- **Return Processing**: Greek return policy automation
- **GDPR Compliance**: Data protection and privacy rights
- **Dispute Resolution**: Greek ADR (Alternative Dispute Resolution)
- **Legal Documentation**: Greek terms and conditions templates

## Data Models

### Ticket Model

```typescript
interface Ticket {
  id: string
  number: string // Auto-generated unique number
  subject: string
  description: string
  status: TicketStatus
  priority: TicketPriority
  category: TicketCategory
  subcategory?: string
  source: TicketSource
  assignedTo?: string
  assignedTeam?: string
  customerId?: string
  contactId?: string
  customerEmail: string
  customerPhone?: string
  isGreekCustomer: boolean
  greekConsumerRights?: GreekConsumerRights
  slaTarget: Date
  responseTarget: Date
  resolutionTarget: Date
  firstResponseAt?: Date
  resolvedAt?: Date
  closedAt?: Date
  reopenedCount: number
  escalationLevel: number
  escalatedAt?: Date
  escalatedTo?: string
  satisfaction?: CustomerSatisfaction
  estimatedHours?: number
  actualHours?: number
  tags: string[]
  customFields: Record<string, any>
  relatedTickets: string[]
  attachments: Attachment[]
  activities: TicketActivity[]
  createdAt: Date
  updatedAt: Date
  createdBy: string
  lastUpdatedBy: string
}

type TicketStatus = 
  | 'new' 
  | 'open' 
  | 'pending' 
  | 'waiting_customer' 
  | 'waiting_vendor' 
  | 'resolved' 
  | 'closed' 
  | 'cancelled'

type TicketPriority = 
  | 'low' 
  | 'normal' 
  | 'high' 
  | 'urgent' 
  | 'critical'
  | 'greek_consumer_urgent' // Special Greek consumer protection priority

type TicketSource = 
  | 'email' 
  | 'phone' 
  | 'chat' 
  | 'web_form' 
  | 'social_media' 
  | 'walk_in'
  | 'greek_consumer_center' // Greek consumer protection center

interface GreekConsumerRights {
  isConsumerComplaint: boolean
  consumerRightType?: 'warranty' | 'return' | 'refund' | 'dispute'
  warrantyPeriod?: number // months
  purchaseDate?: Date
  isWithinWarranty: boolean
  isWithinReturnPeriod: boolean
  requiresLegalNotice: boolean
  adrRequired: boolean // Alternative Dispute Resolution
}
```

### Knowledge Article Model

```typescript
interface KnowledgeArticle {
  id: string
  title: string
  content: string
  summary: string
  language: 'el' | 'en' | 'both'
  category: string
  subcategory?: string
  tags: string[]
  status: 'draft' | 'published' | 'archived'
  visibility: 'public' | 'internal' | 'customer_portal'
  isGreekLegal: boolean // Greek legal/compliance content
  greekLegalCategory?: 'consumer_rights' | 'warranty' | 'returns' | 'privacy'
  attachments: Attachment[]
  views: number
  helpfulVotes: number
  notHelpfulVotes: number
  lastReviewed: Date
  reviewedBy?: string
  customFields: Record<string, any>
  relatedArticles: string[]
  createdAt: Date
  updatedAt: Date
  createdBy: string
  lastUpdatedBy: string
}
```

### Chat Session Model

```typescript
interface ChatSession {
  id: string
  visitorId?: string
  customerId?: string
  contactId?: string
  agentId?: string
  status: 'waiting' | 'active' | 'transferred' | 'ended'
  priority: 'low' | 'normal' | 'high' | 'urgent'
  queue?: string
  isGreekLanguage: boolean
  preferredLanguage: 'el' | 'en'
  startedAt: Date
  endedAt?: Date
  transferredAt?: Date
  transferredFrom?: string
  transferredTo?: string
  waitTime?: number // seconds
  duration?: number // seconds
  messages: ChatMessage[]
  satisfaction?: CustomerSatisfaction
  tags: string[]
  customFields: Record<string, any>
  relatedTicketId?: string
  createdAt: Date
  updatedAt: Date
}

interface ChatMessage {
  id: string
  sessionId: string
  senderId: string
  senderType: 'visitor' | 'customer' | 'agent' | 'system'
  message: string
  messageType: 'text' | 'file' | 'image' | 'system_notification'
  attachments?: Attachment[]
  isGreekText: boolean
  translatedMessage?: string
  timestamp: Date
  readAt?: Date
}
```

### Customer Satisfaction Model

```typescript
interface CustomerSatisfaction {
  rating: 1 | 2 | 3 | 4 | 5
  feedback?: string
  feedbackInGreek?: string
  categories: SatisfactionCategory[]
  submittedAt: Date
  followUpRequired: boolean
  followUpDate?: Date
}

interface SatisfactionCategory {
  category: 'response_time' | 'resolution_quality' | 'agent_helpfulness' | 'communication'
  rating: 1 | 2 | 3 | 4 | 5
}
```

## API Endpoints

### Ticket APIs

```typescript
// Ticket Management
GET /api/tickets
POST /api/tickets
GET /api/tickets/:id
PUT /api/tickets/:id
DELETE /api/tickets/:id
POST /api/tickets/:id/assign
POST /api/tickets/:id/escalate
POST /api/tickets/:id/resolve
POST /api/tickets/:id/close
POST /api/tickets/:id/reopen

// Ticket Activities
GET /api/tickets/:id/activities
POST /api/tickets/:id/activities
PUT /api/tickets/:id/activities/:activityId

// Ticket Attachments
GET /api/tickets/:id/attachments
POST /api/tickets/:id/attachments
DELETE /api/tickets/:id/attachments/:attachmentId

// SLA Management
GET /api/tickets/sla/overview
GET /api/tickets/:id/sla
POST /api/tickets/:id/sla/extend

// Greek Compliance
POST /api/tickets/validate-greek-consumer-rights
GET /api/tickets/greek-legal-templates
POST /api/tickets/generate-greek-response
GET /api/tickets/warranty-check
```

### Knowledge Base APIs

```typescript
// Knowledge Articles
GET /api/knowledge/articles
POST /api/knowledge/articles
GET /api/knowledge/articles/:id
PUT /api/knowledge/articles/:id
DELETE /api/knowledge/articles/:id
POST /api/knowledge/articles/:id/publish
POST /api/knowledge/articles/:id/archive

// Article Search
GET /api/knowledge/search
POST /api/knowledge/articles/:id/view
POST /api/knowledge/articles/:id/vote

// Categories
GET /api/knowledge/categories
POST /api/knowledge/categories
PUT /api/knowledge/categories/:id
DELETE /api/knowledge/categories/:id

// Greek Content
GET /api/knowledge/greek-legal-articles
GET /api/knowledge/greek-templates
POST /api/knowledge/translate-to-greek
```

### Chat APIs

```typescript
// Chat Sessions
GET /api/chat/sessions
POST /api/chat/sessions
GET /api/chat/sessions/:id
PUT /api/chat/sessions/:id
POST /api/chat/sessions/:id/transfer
POST /api/chat/sessions/:id/end

// Chat Messages
GET /api/chat/sessions/:id/messages
POST /api/chat/sessions/:id/messages
PUT /api/chat/messages/:id

// Chat Management
GET /api/chat/agents/online
POST /api/chat/agents/:id/status
GET /api/chat/queues
GET /api/chat/analytics

// Greek Chat Features
POST /api/chat/translate-message
GET /api/chat/greek-canned-responses
POST /api/chat/greek-language-detect
```

### Customer Portal APIs

```typescript
// Portal Authentication
POST /api/portal/auth/login
POST /api/portal/auth/logout
POST /api/portal/auth/register
POST /api/portal/auth/reset-password

// Customer Portal
GET /api/portal/profile
PUT /api/portal/profile
GET /api/portal/tickets
POST /api/portal/tickets
GET /api/portal/tickets/:id
GET /api/portal/knowledge
GET /api/portal/satisfaction/:ticketId

// Greek Portal Features
GET /api/portal/greek-consumer-rights
GET /api/portal/warranty-status
POST /api/portal/return-request
GET /api/portal/greek-legal-documents
```

## UI Components

### TicketManager Component

```typescript
interface TicketManagerProps {
  view: 'all' | 'assigned' | 'unassigned' | 'overdue'
  filters?: TicketFilters
  onTicketSelect?: (ticket: Ticket) => void
  showGreekCompliance?: boolean
}

const TicketManager: React.FC<TicketManagerProps> = ({
  view,
  filters,
  onTicketSelect,
  showGreekCompliance = true
}) => {
  // Component implementation
}
```

### TicketDetail Component

```typescript
interface TicketDetailProps {
  ticketId: string
  onUpdate?: (ticket: Ticket) => void
  showGreekConsumerRights?: boolean
  allowEdit?: boolean
}

const TicketDetail: React.FC<TicketDetailProps> = ({
  ticketId,
  onUpdate,
  showGreekConsumerRights = true,
  allowEdit = true
}) => {
  // Component implementation
}
```

### LiveChat Component

```typescript
interface LiveChatProps {
  sessionId?: string
  isAgent?: boolean
  preferredLanguage?: 'el' | 'en'
  showTranslation?: boolean
  onSessionEnd?: (session: ChatSession) => void
}

const LiveChat: React.FC<LiveChatProps> = ({
  sessionId,
  isAgent = false,
  preferredLanguage = 'el',
  showTranslation = true,
  onSessionEnd
}) => {
  // Component implementation
}
```

### KnowledgeBase Component

```typescript
interface KnowledgeBaseProps {
  view: 'customer' | 'agent'
  language?: 'el' | 'en' | 'both'
  category?: string
  onArticleSelect?: (article: KnowledgeArticle) => void
  showGreekLegal?: boolean
}

const KnowledgeBase: React.FC<KnowledgeBaseProps> = ({
  view,
  language = 'both',
  category,
  onArticleSelect,
  showGreekLegal = true
}) => {
  // Component implementation
}
```

### CustomerPortal Component

```typescript
interface CustomerPortalProps {
  customerId: string
  showGreekRights?: boolean
  enableSelfService?: boolean
  onTicketCreate?: (ticket: Partial<Ticket>) => void
}

const CustomerPortal: React.FC<CustomerPortalProps> = ({
  customerId,
  showGreekRights = true,
  enableSelfService = true,
  onTicketCreate
}) => {
  // Component implementation
}
```

## Custom Hooks

### useTickets Hook

```typescript
interface UseTicketsOptions {
  view: 'all' | 'assigned' | 'unassigned'
  filters?: TicketFilters
  realtime?: boolean
}

const useTickets = (options: UseTicketsOptions) => {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createTicket = async (ticket: Partial<Ticket>) => {
    // Implementation
  }

  const updateTicket = async (ticketId: string, updates: Partial<Ticket>) => {
    // Implementation
  }

  const assignTicket = async (ticketId: string, agentId: string) => {
    // Implementation
  }

  const escalateTicket = async (ticketId: string, reason: string) => {
    // Implementation
  }

  const resolveTicket = async (ticketId: string, resolution: string) => {
    // Implementation
  }

  return {
    tickets,
    loading,
    error,
    createTicket,
    updateTicket,
    assignTicket,
    escalateTicket,
    resolveTicket,
    refetch: () => {/* Implementation */}
  }
}
```

### useKnowledgeBase Hook

```typescript
interface UseKnowledgeBaseOptions {
  language?: 'el' | 'en' | 'both'
  category?: string
  searchQuery?: string
}

const useKnowledgeBase = (options: UseKnowledgeBaseOptions) => {
  const [articles, setArticles] = useState<KnowledgeArticle[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const searchArticles = async (query: string) => {
    // Implementation
  }

  const createArticle = async (article: Partial<KnowledgeArticle>) => {
    // Implementation
  }

  const updateArticle = async (articleId: string, updates: Partial<KnowledgeArticle>) => {
    // Implementation
  }

  const publishArticle = async (articleId: string) => {
    // Implementation
  }

  const voteArticle = async (articleId: string, helpful: boolean) => {
    // Implementation
  }

  return {
    articles,
    loading,
    error,
    searchArticles,
    createArticle,
    updateArticle,
    publishArticle,
    voteArticle,
    refetch: () => {/* Implementation */}
  }
}
```

### useLiveChat Hook

```typescript
interface UseLiveChatOptions {
  sessionId?: string
  isAgent?: boolean
  realtime?: boolean
}

const useLiveChat = (options: UseLiveChatOptions) => {
  const [session, setSession] = useState<ChatSession | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startSession = async (customerId?: string) => {
    // Implementation
  }

  const sendMessage = async (message: string, attachments?: File[]) => {
    // Implementation
  }

  const transferSession = async (toAgentId: string, reason: string) => {
    // Implementation
  }

  const endSession = async (satisfaction?: CustomerSatisfaction) => {
    // Implementation
  }

  return {
    session,
    messages,
    loading,
    error,
    startSession,
    sendMessage,
    transferSession,
    endSession,
    refetch: () => {/* Implementation */}
  }
}
```

### useGreekCustomerService Hook

```typescript
const useGreekCustomerService = () => {
  const checkConsumerRights = (ticket: Ticket): GreekConsumerRights => {
    // Greek consumer protection law validation
    return {
      isConsumerComplaint: false,
      isWithinWarranty: false,
      isWithinReturnPeriod: false,
      requiresLegalNotice: false,
      adrRequired: false
    }
  }

  const calculateWarrantyPeriod = (purchaseDate: Date, productType: string): number => {
    // Greek warranty law calculations
    const defaultWarranty = 24 // months
    const extendedWarranty = {
      'electronics': 24,
      'appliances': 24,
      'furniture': 6,
      'clothing': 6,
      'digital_goods': 0
    }
  
    return extendedWarranty[productType] || defaultWarranty
  }

  const isWithinReturnPeriod = (purchaseDate: Date): boolean => {
    // 14 days for online purchases, 7 days for in-store (Greek law)
    const now = new Date()
    const diffTime = Math.abs(now.getTime() - purchaseDate.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
    return diffDays <= 14 // Assuming online purchase
  }

  const generateGreekLegalResponse = (ticket: Ticket): string => {
    // Generate appropriate legal response based on Greek consumer law
    return "Σύμφωνα με τον ελληνικό νόμο προστασίας καταναλωτή..."
  }

  const translateToGreek = async (text: string): Promise<string> => {
    // Translation service integration
    return text
  }

  return {
    checkConsumerRights,
    calculateWarrantyPeriod,
    isWithinReturnPeriod,
    generateGreekLegalResponse,
    translateToGreek
  }
}
```

## Context Providers

### CustomerServiceProvider

```typescript
interface CustomerServiceContextType {
  // Ticket state
  tickets: Ticket[]
  ticketStats: TicketStats
  slaMetrics: SLAMetrics
  
  // Knowledge base state
  articles: KnowledgeArticle[]
  articleCategories: string[]
  
  // Chat state
  activeSessions: ChatSession[]
  agentStatus: AgentStatus
  
  // Greek features
  greekConsumerRights: GreekConsumerRights[]
  greekLegalTemplates: LegalTemplate[]
  
  // Actions
  createTicket: (ticket: Partial<Ticket>) => Promise<void>
  updateTicket: (ticketId: string, updates: Partial<Ticket>) => Promise<void>
  startChatSession: (customerId?: string) => Promise<ChatSession>
  searchKnowledge: (query: string) => Promise<KnowledgeArticle[]>
  
  // Greek actions
  checkWarranty: (productId: string, purchaseDate: Date) => Promise<WarrantyInfo>
  generateGreekResponse: (ticket: Ticket) => Promise<string>
}

const CustomerServiceProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Implementation
}
```

## Greek Customer Service Features

### Consumer Protection Compliance

- Automatic warranty period calculation based on Greek law
- Return policy enforcement (14 days online, 7 days in-store)
- Consumer rights notification in all communications
- Alternative Dispute Resolution (ADR) integration
- Legal template generation for disputes

### Greek Language Support

- Complete Greek interface for customer portal
- Greek canned responses for common issues
- Real-time translation between Greek and English
- Greek legal document templates
- Cultural adaptation of communication style

### Business Standards Integration

- Greek business hours for response time calculation
- Orthodox holiday awareness for SLA management
- VAT-related support queries handling
- AFM/DOY validation for business customers
- Integration with Greek consumer protection agencies

### GDPR and Privacy

- Data subject rights implementation
- Consent management for communications
- Right to be forgotten compliance
- Data portability features
- Privacy impact assessments

## Testing Specifications

### Unit Tests

```typescript
describe('Customer Service Models', () => {
  test('Ticket model with Greek consumer rights', () => {})
  test('Knowledge article multilingual support', () => {})
  test('Chat session Greek language detection', () => {})
  test('SLA calculation with Greek holidays', () => {})
})

describe('Greek Customer Service Utils', () => {
  test('Warranty period calculation', () => {})
  test('Return period validation', () => {})
  test('Consumer rights checking', () => {})
  test('Greek legal response generation', () => {})
})
```

### Integration Tests

```typescript
describe('Customer Service APIs', () => {
  test('Ticket lifecycle management', () => {})
  test('Knowledge base search functionality', () => {})
  test('Live chat real-time messaging', () => {})
  test('Greek compliance validation', () => {})
  test('Customer portal self-service', () => {})
})
```

### E2E Tests

```typescript
describe('Customer Service Workflows', () => {
  test('Complete ticket resolution process', () => {})
  test('Multi-language customer support', () => {})
  test('Live chat with escalation', () => {})
  test('Knowledge base article creation and publication', () => {})
  test('Greek consumer complaint handling', () => {})
})
```

## Performance Considerations

### Real-time Features

- WebSocket connections for live chat
- Real-time ticket updates
- Live SLA monitoring
- Instant notification delivery
- Real-time agent status tracking

### Scalability

- Efficient ticket indexing and search
- Knowledge base content caching
- Chat message pagination
- File attachment optimization
- Multi-language content delivery

### Greek Market Optimization

- Greek language search optimization
- Local timezone handling
- Holiday calendar integration
- Cultural communication preferences
- Legal compliance automation

## Success Metrics

### Service Quality

- First response time improvement
- Resolution time reduction
- Customer satisfaction scores
- SLA compliance rates
- Escalation rate reduction

### Greek Market Success

- Greek language adoption rates
- Consumer rights compliance
- Warranty handling accuracy
- Return processing efficiency
- Legal dispute reduction

### Operational Efficiency

- Agent productivity metrics
- Knowledge base usage statistics
- Self-service adoption rates
- Chat resolution rates
- Multi-channel integration success
