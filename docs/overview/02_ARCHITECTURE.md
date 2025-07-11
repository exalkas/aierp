# Greek ERP/CRM System - Technical Architecture Document

## Version Information

- **Document Version**: 1.1
- **Last Updated**: January 2025
- **Target Year**: 2025-2027 Implementation

## Executive Summary

This document outlines the technical architecture for a revenue-focused Greek ERP/CRM system, designed with a **modular monolith + microservice capability** approach. The architecture prioritizes core business functionality first (invoicing, customer management, basic accounting) with AADE compliance, then scales systematically to specialized Greek market features and industry-specific solutions.

**Key Architectural Principles:**

- **Revenue-First Design**: Core business functionality accessible by Month 6
- **Greek Compliance Foundation**: AADE MyDATA integration built into core architecture
- **Modular Expansion**: Systematic addition of HR, banking, analytics, and industry modules
- **Deployment Flexibility**: Cloud SAAS and local desktop web application deployment
- **Enterprise Customization**: Multi-level versioning and custom implementation framework
- **Version Management**: Automated upgrade compatibility and rollback capabilities
- **Bot Ecosystem Integration**: Comprehensive automation framework with Greek business intelligence

## 1. High-Level System Architecture

### 1.1 Microservices Architecture

```
┌─────────────────┐
│   Web Frontend  │
│   (Next.js 15+) │
└─────────────────┘
         │
         │
         │
         ┌─────────────────────────────────────────────────────┐
         │              API Gateway (Nginx + JWT)              │
         └─────────────────────────────────────────────────────┘
                                 │
    ┌─────────────┬─────────────┼─────────────┬─────────────┬─────────────┬─────────────┬─────────────────┐
    │             │             │             │             │             │             │                 │
┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌────▼────┐
│ Core  │    │ CRM   │    │ ERP   │    │ Bot   │    │ Job   │    │ Migr  │    │ Integ │    │ Support │
│Service│    │Service│    │Service│    │Service│    │Service│    │Service│    │Service│    │Platform │
└───────┘    └───────┘    └───────┘    └───────┘    └───────┘    └───────┘    └───────┘    └─────────┘
                                                          │
                            ┌─────────────────────────────┼─────────────────────────────┐
                            │                             │                             │
                     ┌─────▼─────┐               ┌─────▼─────┐               ┌─────▼─────┐
                     │AI Assistant│               │Live Chat  │               │Knowledge  │
                     │  Service   │               │ Service   │               │Base Service│
                     └───────────┘               └───────────┘               └───────────┘
    │             │             │             │            │
    └─────────────┼─────────────┼─────────────┼────────────┘
                  │             │             │
         ┌─────────────────────────────────────────────────────┐
         │     Database Layer (PostgreSQL 15+ + Redis 7+)     │
         └─────────────────────────────────────────────────────┘
```

## 2. Technology Stack (2025 Current)

### 2.1 Backend Technologies (2025 Updated Stack)

- **Runtime**: Python 3.12+ with FastAPI 0.104+
- **Database**: PostgreSQL 16+ (primary), Redis 7.2+ (caching/sessions)
- **Message Queue**: Redis with Celery for background tasks
- **File Storage**: S3-compatible cloud storage (SAAS) / Local encrypted storage (desktop)
- **Authentication**: JWT with refresh tokens, OAuth 2.0
- **Encryption**: AES-256 with PBKDF2 key derivation
- **API Performance**: <200ms average response time

### 2.2 Frontend Technologies (2025 Current)

- **Web Framework**: Next.js 15+ with App Router and Server Components
- **UI Framework**: React 19+ with enhanced concurrent features
- **Language**: TypeScript 5.3+ with improved type inference
- **Styling**: Tailwind CSS 4.0+ with container queries and shadcn/ui components
- **State Management**: Zustand or React Query for data fetching
- **Forms**: React Hook Form with Zod validation
- **Charts**: Recharts or Chart.js for analytics visualization

### 2.4 External APIs (2025 Current)

- **Speech-to-Text**: OpenAI Whisper API or Google Speech-to-Text
- **NLP**: OpenAI GPT-4 Turbo or Google Gemini Pro
- **Messaging**: WhatsApp Business API 2.0, Telegram Bot API 7.0, Viber REST API
- **Greek Tax**: AADE MyDATA API v1.0.11 (2025 requirements)

## 3. System Components

### 3.1 Core Services

#### 3.1.1 Authentication & Authorization Service

```python
# Modern JWT implementation with refresh tokens
class AuthService:
    def authenticate_user(self, credentials)
    def refresh_token(self, refresh_token)
    def validate_permissions(self, user, resource, action)
    def manage_sessions(self, user_id)
```

**Features**:

- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Single sign-on (SSO) capabilities
- Session management with Redis

#### 3.1.2 User Management Service

```python
class UserService:
    def create_user(self, user_data)
    def manage_roles(self, user_id, roles)
    def handle_user_preferences(self, user_id)
    def audit_user_actions(self, user_id, action)
```

### 3.2 CRM Service (EspoCRM-Style Customization)

#### 3.2.1 Entity Management System

```python
class EntityManager:
    def create_custom_entity(self, entity_definition)
    def add_custom_fields(self, entity_id, field_definitions)
    def manage_relationships(self, entity1, entity2, relationship_type)
    def configure_workflows(self, entity_id, workflow_definition)
```

**EspoCRM-Level Features**:

- **Dynamic Entity Creation**: Create custom business objects at runtime
- **Custom Field Types**: Text, Number, Date, Dropdown, Multi-select, Currency, etc.
- **Advanced Relationships**: One-to-One, One-to-Many, Many-to-Many with custom join tables
- **Workflow Automation**: Visual workflow builder with conditions and actions
- **Custom Views**: List, Detail, Kanban, Calendar, Timeline views
- **Advanced Filters**: Complex filtering with AND/OR logic
- **Mass Operations**: Bulk update, merge, export, delete
- **Activity Streams**: Real-time feed of record changes
- **Document Generation**: Custom PDF templates with merge fields

#### 3.2.2 Lead Management

```python
class LeadService:
    def capture_leads(self, source, lead_data)
    def qualify_leads(self, lead_id, criteria)
    def convert_to_opportunity(self, lead_id)
    def assign_lead_scoring(self, lead_id)
```

#### 3.2.3 Customer Relationship Management

```python
class CustomerService:
    def manage_customer_lifecycle(self, customer_id)
    def track_interactions(self, customer_id, interaction_data)
    def manage_support_tickets(self, customer_id)
    def calculate_clv(self, customer_id)  # Customer Lifetime Value
```

### 3.3 ERP Service

#### 3.3.1 Financial Management

```python
class FinancialService:
    def process_invoice(self, invoice_data)
    def manage_payments(self, payment_data)
    def generate_reports(self, report_type, parameters)
    def handle_tax_calculations(self, transaction_data)
```

#### 3.3.2 Inventory Management

```python
class InventoryService:
    def track_stock_levels(self, product_id)
    def process_stock_movements(self, movement_data)
    def manage_suppliers(self, supplier_data)
    def handle_procurement(self, procurement_request)
```

### 3.4 Bot Service (Greek Business Automation)

#### 3.4.1 Bot Orchestration Engine

```python
class BotOrchestrationEngine:
    def execute_workflow(self, workflow_definition)
    def execute_sequential_bots(self, bots)
    def execute_parallel_bots(self, bots)
    def execute_conditional_bots(self, condition, bots)
    def handle_workflow_error(self, workflow, error)
```

#### 3.4.2 Core Greek Business Bots

```python
class AADEComplianceBot:
    def auto_submit_invoice(self, invoice_data)
    def monitor_compliance_changes(self)
    def generate_compliance_qr(self, invoice_data, tax_data)

class BankingReconciliationBot:
    def daily_reconciliation(self)
    def detect_fraud(self, transaction)
    def match_transactions(self, transactions, invoices)

class HRAutomationBot:
    def process_monthly_payroll(self)
    def manage_employee_leave(self, leave_request)
    def calculate_ika_contributions(self, employee, gross_pay)

class InvoiceProcessingBot:
    def process_incoming_invoice(self, invoice_file)
    def auto_create_recurring_invoices(self)
    def extract_invoice_data(self, invoice_file)

class EcommerceSyncBot:
    def sync_inventory_realtime(self)
    def optimize_pricing_daily(self)
    def process_orders_automatically(self)
```

#### 3.4.3 Bot Marketplace Management

```python
class BotMarketplaceService:
    def register_bot(self, bot_definition)
    def install_bot(self, company_id, bot_id)
    def manage_bot_subscriptions(self, company_id)
    def track_bot_usage(self, company_id, bot_id)
    def process_bot_payments(self, subscription_data)
```

### 3.5 Job Management Service (Batch Job & Scheduling)

#### 3.5.1 Greek Business Calendar

```python
class GreekBusinessCalendar:
    def __init__(self):
        self.orthodox_holidays = self.load_orthodox_calendar()
        self.national_holidays = self.load_national_holidays()
        self.banking_hours = self.load_banking_schedule()

    def is_business_day(self, date):
        """Check if date is a Greek business day"""
        return self.is_working_day_with_greek_context(date)

    def schedule_before_tax_deadline(self, deadline_date):
        """Schedule job before Greek tax deadline with safety margin"""
        return self.calculate_safe_execution_time(deadline_date)
```

#### 3.5.2 Job Execution Engine

```python
class JobExecutionEngine:
    def __init__(self):
        self.scheduler = AdvancedScheduler()
        self.executor = JobExecutor()
        self.monitor = JobMonitor()
        self.retry_engine = RetryEngine()
        self.greek_calendar = GreekBusinessCalendar()

    async def execute_job(self, job_definition):
        """Execute job with Greek business context awareness"""
        # Pre-execution validation with Greek business rules
        await self.validate_greek_business_context(job_definition)

        # Execute with comprehensive monitoring
        result = await self.executor.run_job(job_definition)

        # Handle success/failure with intelligent retry
        await self.handle_job_completion(job_definition, result)
```

#### 3.5.3 Critical Greek Business Jobs

```python
class GreekBusinessJobs:
    # AADE Compliance Jobs
    async def daily_aade_submission(self):
        """Submit pending invoices to MyDATA"""
        pass

    async def monthly_tax_declarations(self):
        """Automated tax filing preparation"""
        pass

    # Banking Reconciliation Jobs
    async def daily_bank_sync(self):
        """Fetch transactions from all Greek banks"""
        pass

    async def transaction_matching(self):
        """AI-powered invoice-payment matching"""
        pass

    # HR Automation Jobs
    async def monthly_payroll_processing(self):
        """IKA, EFKA, OAED automated processing"""
        pass

    # E-commerce Integration Jobs
    async def inventory_sync(self):
        """Real-time stock synchronization"""
        pass

    async def price_optimization(self):
        """Daily competitive pricing analysis"""
        pass
```

### 3.6 Migration Service (Automated ETL & Data Migration)

#### 3.6.1 Greek ERP Data Intelligence

```python
class GreekDataIntelligence:
    def __init__(self):
        self.greek_validators = GreekValidators()
        self.aade_compliance = AADECompliance()
        self.banking_formats = GreekBankingFormats()

    async def process_greek_data(self, raw_data):
        """Intelligent processing of Greek business data"""
        # Validate Greek business identifiers (AFM, VAT)
        customers = await self.process_customers_with_afm_validation(raw_data)

        # Process Greek tax and compliance data
        invoices = await self.process_aade_compliant_invoices(raw_data)

        # Process Greek banking formats
        bank_accounts = await self.process_greek_bank_accounts(raw_data)

        return {
            'customers': customers,
            'invoices': invoices,
            'bank_accounts': bank_accounts
        }
```

#### 3.6.2 Advanced Field Mapping System

```python
class AdvancedFieldMapping:
    def __init__(self):
        self.mapping_templates = self.load_greek_erp_templates()
        self.ai_mapper = AIFieldMapper()

    async def create_migration_mapping(self, source_system, source_data):
        """Create intelligent field mapping for Greek ERP systems"""
        # Load pre-configured templates for Megasoft, Epsilon, SAP, etc.
        base_mapping = self.mapping_templates.get(source_system, {})

        # AI-powered field detection and mapping
        ai_suggestions = await self.ai_mapper.suggest_mappings(source_data)

        # Merge mappings with Greek business validation
        final_mapping = await self.merge_with_greek_validation(base_mapping, ai_suggestions)

        return final_mapping
```

#### 3.6.3 Three-Tier Migration Architecture

```python
class MigrationOrchestrator:
    def __init__(self):
        self.self_service = SelfServiceMigration()
        self.assisted = AssistedMigration()
        self.enterprise = EnterpriseMigration()

    async def execute_migration(self, migration_request):
        """Route migration to appropriate tier based on complexity"""
        if migration_request.complexity == 'basic':
            return await self.self_service.migrate(migration_request)
        elif migration_request.complexity == 'standard':
            return await self.assisted.migrate(migration_request)
        else:
            return await self.enterprise.migrate(migration_request)
```

#### 3.6.4 Supported Migration Sources

**Greek ERP Systems:**

- **Megasoft**: Complete data export and mapping
- **Epsilon**: Accounting and invoicing data migration
- **SingularLogic**: Enterprise ERP full migration
- **Softone**: Business management data transfer

**International ERP Systems:**

- **SAP**: Complex multi-module data migration
- **Oracle**: Enterprise data and workflow migration
- **Microsoft Dynamics**: CRM and ERP integration migration

#### 3.6.5 Migration Quality Assurance

```python
class MigrationQualityAssurance:
    async def validate_migration(self, migration_id):
        """Comprehensive migration validation"""
        # Data integrity validation
        data_integrity = await self.validate_data_integrity(migration_id)

        # Greek compliance validation
        compliance = await self.validate_greek_compliance(migration_id)

        # Business logic validation
        business_logic = await self.validate_business_logic(migration_id)

        return {
            'data_integrity': data_integrity,
            'compliance': compliance,
            'business_logic': business_logic,
            'overall_success': all([data_integrity, compliance, business_logic])
        }
```

### 3.7 Support Platform (Greek Speed Support Strategy)

#### 3.7.1 AI Assistant Service

```python
class GreekAIAssistant:
    def process_greek_query(self, query, customer_context):
        """Process customer queries in Greek with business context"""
        # Greek NLP processing
        intent = self.extract_intent(query, language='el')
        business_context = self.load_business_context(customer_context)

        # AADE/IKA/EFKA specific knowledge
        if intent.category in ['aade', 'tax', 'compliance']:
            return self.handle_compliance_query(intent, business_context)
        elif intent.category in ['technical', 'system']:
            return self.handle_technical_query(intent, business_context)
        else:
            return self.handle_general_query(intent, business_context)

    def escalate_to_human(self, conversation_id, reason):
        """Seamlessly transfer to human agent with full context"""
        pass

    def learn_from_interactions(self, successful_resolutions):
        """Continuous learning from resolved issues"""
        pass
```

**Features**:

- **Greek Language Processing**: Native Greek understanding and responses
- **Business Context Awareness**: Customer setup, history, customizations
- **AADE/IKA/EFKA Knowledge**: Specific Greek compliance expertise
- **Instant Response**: < 5 seconds response time
- **Smart Escalation**: Automatic handoff to humans when needed

#### 3.4.2 Live Chat Service

```python
class LiveChatService:
    def initiate_chat(self, customer_id, issue_priority):
        """Start live chat with context pre-loading"""
        agent = self.route_to_expert(customer_id, issue_priority)
        context = self.load_customer_context(customer_id)
        return self.create_chat_session(agent, context)

    def enable_screen_sharing(self, session_id):
        """Enable screen sharing for complex issues"""
        pass

    def co_browse_customer_system(self, session_id):
        """Agent can navigate customer's system to help"""
        pass

    def escalate_to_developer(self, session_id, technical_issue):
        """Direct escalation to development team"""
        pass
```

**Features**:

- **WebSocket Real-time**: Instant messaging and status updates
- **Smart Agent Routing**: Match customer to specialist (accounting, HR, technical)
- **Screen Sharing**: WebRTC for visual assistance
- **Customer Context**: Pre-loaded history, setup, and recent activity
- **Response Time Tracking**: Monitor and enforce < 2 minute SLA

#### 3.4.3 Knowledge Base Service

```python
class KnowledgeBaseService:
    def search_in_greek(self, query, customer_industry):
        """Semantic search in Greek with industry filtering"""
        results = self.semantic_search(query, language='el')
        return self.filter_by_industry(results, customer_industry)

    def get_video_tutorials(self, topic, industry):
        """Industry-specific video tutorials in Greek"""
        return self.load_videos(topic, industry, language='el')

    def track_article_effectiveness(self, article_id, resolved_issue):
        """Monitor which articles actually solve problems"""
        pass
```

**Content Structure**:

```
Knowledge Base/
├── AADE_Procedures/
│   ├── invoice_submission.mp4
│   ├── qr_code_generation.md
│   └── common_errors.md
├── IKA_EFKA_HR/
│   ├── payroll_submission.mp4
│   ├── employee_registration.md
│   └── leave_management.md
├── Industry_Specific/
│   ├── shipping_operations/
│   ├── tourism_procedures/
│   ├── restaurant_management/
│   └── retail_workflows/
└── Technical_Guides/
    ├── system_setup.mp4
    ├── data_backup.md
    └── troubleshooting.md
```

#### 3.4.4 Proactive Monitoring Service

```python
class ProactiveMonitoring:
    def monitor_system_health(self, customer_id):
        """Monitor customer's system for potential issues"""
        checks = {
            'aade_connection': self.check_aade_status(customer_id),
            'database_performance': self.check_db_performance(customer_id),
            'failed_operations': self.check_failed_operations(customer_id),
            'custom_conflicts': self.check_customizations(customer_id)
        }

        for check, status in checks.items():
            if status == 'warning' or status == 'error':
                self.proactive_outreach(customer_id, check, status)

    def predict_issues(self, customer_usage_patterns):
        """AI-powered issue prediction"""
        pass

    def auto_create_tickets(self, detected_issues):
        """Automatically create support tickets for critical issues"""
        pass
```

**Monitoring Capabilities**:

- **AADE Integration Health**: Monitor MyDATA connection status
- **Performance Tracking**: Database query times, API response times
- **Error Detection**: Failed operations, system errors
- **Usage Analytics**: Unusual patterns that might indicate problems
- **Predictive Alerts**: AI-powered early warning system

#### 3.4.5 Support Analytics & SLA Monitoring

```python
class SupportAnalytics:
    def track_response_times(self, ticket_id, response_time):
        """Monitor SLA compliance"""
        sla_target = self.get_sla_target(ticket_id)
        if response_time > sla_target:
            self.alert_management(ticket_id, response_time)

    def measure_customer_satisfaction(self, ticket_id, csat_score):
        """Track CSAT and NPS scores"""
        pass

    def analyze_agent_performance(self, agent_id):
        """Agent performance metrics and coaching opportunities"""
        pass

    def generate_support_insights(self):
        """Business intelligence for support operations"""
        pass
```

**Analytics Features**:

- **Real-time SLA Monitoring**: Track response times against targets
- **Customer Satisfaction Tracking**: CSAT, NPS, resolution effectiveness
- **Agent Performance Metrics**: Response times, resolution rates, customer feedback
- **Support ROI Analysis**: Revenue impact of support excellence
- **Trend Analysis**: Issue patterns, knowledge gaps, improvement opportunities

### 3.5 Integration Services

#### 3.5.1 AADE MyDATA Integration (2025 Current Requirements)

```python
class AADEService:
    # Currently Active (Mandatory since Jan 2024)
    def submit_invoice_realtime(self, invoice_data)  # < 5 seconds response time
    def generate_qr_code(self, invoice_mark)  # URL encoding with invoice mark

    # Upcoming 2025 Requirements
    def handle_digital_delivery_note(self, delivery_data)  # Digital control: Oct 1, 2025
    def mandate_delivery_note_issuance(self, goods_data)  # Mandatory: Dec 1, 2025
    def process_b2b_einvoicing(self, b2b_invoice)  # EU approved: July 1, 2025
    def enhanced_b2g_integration(self, government_transaction)  # PEPPOL-based

    # Current API v1.0.11 features
    def validate_invoice_format(self, invoice_xml)
    def retrieve_invoice_status(self, mark_id)
    def handle_classification(self, transaction_data)
    def audit_compliance_events(self, event_data)
```

**2025 AADE Compliance Features**:

- **✅ Real-time Invoice Submission**: All invoices submitted immediately upon creation (mandatory since Jan 2024)
- **✅ QR Code Integration**: Automatic QR code generation for all PDF invoices (mandatory)
- **📅 Digital Delivery Notes**: Electronic tracking of goods movement
  - Digital Control: October 1, 2025
  - Mandatory Issuance: December 1, 2025
- **📅 B2B Electronic Invoicing**: EU Council approved for July 1, 2025 implementation
- **🔄 Enhanced B2G Integration**: PEPPOL-based system for public administration
- **⚡ Enhanced Validation**: Real-time validation with immediate feedback (<5 seconds)
- **📋 Complete Audit Trail**: Full transaction history for tax audits

#### 3.4.2 Messaging Platform Integration

```python
class MessagingService:
    def process_whatsapp_messages(self, webhook_data)
    def send_telegram_notifications(self, chat_id, message)
    def handle_viber_interactions(self, viber_data)
    def process_voice_commands(self, audio_data)
```

**Voice Command Processing**:

```python
class VoiceProcessor:
    def transcribe_audio(self, audio_file)  # Whisper API
    def extract_intent(self, transcription)  # GPT-4 Turbo
    def execute_command(self, intent, parameters)
    def respond_to_user(self, response_text)
```

#### 3.4.3 Remote Support Service

```python
class SupportService:
    def initiate_remote_session(self, customer_id)
    def capture_screen_share(self, session_id)
    def provide_guided_assistance(self, issue_type)
    def log_support_interaction(self, session_data)
```

### 3.5 E-shop Integration Services

#### 3.5.1 Multi-Platform E-commerce Integration

Our system provides comprehensive integration with popular e-commerce platforms used in the Greek market, ensuring seamless synchronization between online sales and ERP operations.

```python
class EshopIntegrationService:
    def __init__(self):
        self.supported_platforms = {
            "shopie": ShopieConnector(),
            "woocommerce": WooCommerceConnector(),
            "shopify": ShopifyConnector(),
            "prestashop": PrestaShopConnector(),
            "eshoprobot": EshopRobotConnector(),
            "custom": CustomEshopConnector()
        }
        self.sync_manager = SyncManager()
        self.aade_service = AADEService()

    async def sync_products(self, platform: str, direction: str = "bidirectional"):
        """Synchronize products between ERP and e-shop"""
        connector = self.supported_platforms[platform]

        if direction in ["erp_to_eshop", "bidirectional"]:
            # Sync from ERP to e-shop
            erp_products = await self.get_erp_products()
            for product in erp_products:
                eshop_product = self.transform_product_for_eshop(product)
                await connector.update_product(eshop_product)

        if direction in ["eshop_to_erp", "bidirectional"]:
            # Sync from e-shop to ERP
            eshop_products = await connector.get_products()
            for product in eshop_products:
                erp_product = self.transform_product_for_erp(product)
                await self.update_erp_product(erp_product)

    async def process_eshop_order(self, platform: str, order_data: dict):
        """Process incoming e-shop order"""
        # Create order in ERP
        erp_order = await self.create_erp_order(order_data)

        # Update inventory
        await self.update_inventory(erp_order.items)

        # Generate AADE compliant invoice
        if order_data["requires_invoice"]:
            invoice = await self.generate_invoice(erp_order)
            aade_response = await self.aade_service.submit_invoice_realtime(invoice)

            # Update e-shop with invoice details
            connector = self.supported_platforms[platform]
            await connector.update_order_invoice(order_data["order_id"], {
                "invoice_number": invoice.number,
                "aade_mark": aade_response.mark,
                "qr_code": aade_response.qr_code
            })

        return erp_order
```

#### 3.5.2 Greek Market E-commerce Integrations

**Shopie.gr Integration**

```python
class ShopieConnector:
    def __init__(self):
        self.api_base = "https://api.shopie.gr/v1"
        self.features = {
            "marketplace_sync": True,  # Skroutz, Bestprice, Public
            "facebook_commerce": True,
            "automatic_translations": True,
            "cloud_native": True
        }

    async def sync_with_marketplaces(self, product_data):
        """Sync products with Greek marketplaces"""
        marketplaces = ["skroutz", "bestprice", "public"]

        for marketplace in marketplaces:
            marketplace_data = self.transform_for_marketplace(product_data, marketplace)
            await self.update_marketplace_product(marketplace, marketplace_data)

    async def handle_facebook_commerce(self, product_data):
        """Sync with Facebook Shop"""
        fb_product = self.transform_for_facebook(product_data)
        await self.update_facebook_product(fb_product)
```

**WooCommerce Integration**

```python
class WooCommerceConnector:
    def __init__(self):
        self.api_base = "wp-json/wc/v3"
        self.auth_method = "oauth"

    async def sync_products(self, products):
        """Sync products with WooCommerce store"""
        for product in products:
            woo_product = {
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock_quantity": product.stock,
                "manage_stock": True,
                "meta_data": [
                    {"key": "erp_product_id", "value": str(product.id)},
                    {"key": "tax_class", "value": self.get_greek_tax_class(product.tax_rate)}
                ]
            }
            await self.api_call("POST", "/products", woo_product)
```

#### 3.5.3 Built-in E-commerce Module

In addition to integrations, our system includes a native e-commerce module specifically designed for Greek businesses.

```python
class NativeEcommerceModule:
    def __init__(self):
        self.product_catalog = ProductCatalogService()
        self.order_processing = OrderProcessingService()
        self.payment_gateway = GreekPaymentGateway()
        self.shipping_integration = GreekShippingService()
        self.seo_engine = GreekSEOEngine()

    async def create_online_store(self, business_config):
        """Create a native online store"""
        store_config = {
            "theme": business_config.get("theme", "modern_greek"),
            "languages": ["el", "en"],
            "currency": "EUR",
            "tax_regime": "greek_vat",
            "payment_methods": self.get_greek_payment_methods(),
            "shipping_methods": self.get_greek_shipping_methods(),
            "marketplace_integration": True,
            "aade_compliance": True
        }

        return await self.deploy_store(store_config)

    def get_greek_payment_methods(self):
        """Configure Greek payment methods"""
        return {
            "credit_cards": {
                "provider": "viva_payments",  # Popular in Greece
                "accepted_cards": ["visa", "mastercard", "american_express"],
                "3d_secure": True
            },
            "bank_transfer": {
                "supported_banks": ["national_bank", "eurobank", "alpha_bank", "piraeus"],
                "iban_validation": True
            },
            "cash_on_delivery": {
                "enabled": True,
                "fee": 2.00,
                "max_amount": 500.00
            },
            "paypal": {
                "enabled": True,
                "currency": "EUR"
            }
        }

    def get_greek_shipping_methods(self):
        """Configure Greek shipping providers"""
        return {
            "elta_courier": {
                "name": "ΕΛΤΑ Courier",
                "api_integration": True,
                "tracking": True,
                "cod_support": True
            },
            "acs": {
                "name": "ACS Courier",
                "api_integration": True,
                "tracking": True,
                "cod_support": True
            },
            "speedex": {
                "name": "Speedex",
                "api_integration": True,
                "tracking": True,
                "cod_support": True
            },
            "local_pickup": {
                "name": "Παραλαβή από κατάστημα",
                "locations": [],  # Configured per business
                "scheduling": True
            }
        }
```

#### 3.5.4 Advanced E-commerce Features

**Multi-channel Inventory Management**

```python
class MultiChannelInventory:
    def __init__(self):
        self.channels = {}
        self.stock_allocator = StockAllocator()
        self.reorder_engine = ReorderEngine()

    async def allocate_stock(self, product_id: str, channel: str, quantity: int):
        """Allocate stock to specific sales channel"""
        available_stock = await self.get_available_stock(product_id)

        if available_stock >= quantity:
            allocation = await self.stock_allocator.allocate(
                product_id, channel, quantity
            )

            # Update all connected channels
            await self.sync_stock_across_channels(product_id)

            # Check if reorder needed
            if available_stock - quantity <= self.get_reorder_point(product_id):
                await self.reorder_engine.trigger_reorder(product_id)

            return allocation
        else:
            raise InsufficientStockError(f"Not enough stock for {product_id}")

    async def sync_stock_across_channels(self, product_id: str):
        """Sync stock levels across all sales channels"""
        current_stock = await self.get_total_available_stock(product_id)

        for channel_name, channel_connector in self.channels.items():
            await channel_connector.update_stock(product_id, current_stock)
```

**Greek Marketplace Integration**

```python
class GreekMarketplaceManager:
    def __init__(self):
        self.marketplaces = {
            "skroutz": SkroutzConnector(),
            "bestprice": BestPriceConnector(),
            "public": PublicConnector(),
            "plaisio": PlaisioConnector(),
            "kotsovolos": KotsovolosConnector()
        }

    async def publish_to_marketplaces(self, product_data):
        """Publish products to Greek marketplaces"""
        for marketplace_name, connector in self.marketplaces.items():
            # Transform product for marketplace requirements
            marketplace_product = await self.transform_for_marketplace(
                product_data, marketplace_name
            )

            # Validate marketplace requirements
            if await self.validate_marketplace_product(marketplace_product, marketplace_name):
                await connector.publish_product(marketplace_product)

    async def sync_marketplace_orders(self):
        """Sync orders from all marketplaces"""
        for marketplace_name, connector in self.marketplaces.items():
            orders = await connector.get_new_orders()

            for order in orders:
                # Convert marketplace order to ERP order
                erp_order = await self.convert_marketplace_order(order, marketplace_name)
                await self.process_order(erp_order)
```

#### 3.5.5 E-commerce Analytics & Reporting

```python
class EcommerceAnalytics:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.report_generator = ReportGenerator()
        self.ai_insights = AIInsightsEngine()

    async def generate_ecommerce_dashboard(self, business_id: str):
        """Generate comprehensive e-commerce analytics dashboard"""
        metrics = await self.collect_metrics(business_id)

        dashboard_data = {
            "sales_overview": {
                "total_revenue": metrics["total_revenue"],
                "orders_count": metrics["orders_count"],
                "average_order_value": metrics["average_order_value"],
                "conversion_rate": metrics["conversion_rate"]
            },
            "channel_performance": {
                "online_store": metrics["online_store_sales"],
                "marketplaces": metrics["marketplace_sales"],

                "social_media": metrics["social_sales"]
            },
            "customer_insights": {
                "new_customers": metrics["new_customers"],
                "returning_customers": metrics["returning_customers"],
                "customer_lifetime_value": metrics["clv"],
                "churn_rate": metrics["churn_rate"]
            },
            "product_performance": {
                "top_selling_products": metrics["top_products"],
                "low_stock_alerts": metrics["low_stock"],
                "product_reviews": metrics["reviews_summary"]
            },
            "ai_recommendations": await self.ai_insights.generate_recommendations(metrics)
        }

        return dashboard_data

    async def track_customer_journey(self, customer_id: str):
        """Track complete customer journey across channels"""
        journey_data = {
            "discovery": await self.get_discovery_touchpoints(customer_id),
            "consideration": await self.get_consideration_behavior(customer_id),
            "purchase": await self.get_purchase_history(customer_id),
            "loyalty": await self.get_loyalty_metrics(customer_id),
            "advocacy": await self.get_advocacy_actions(customer_id)
        }

        return journey_data
```

#### 3.5.6 SEO & Digital Marketing Integration

```python
class DigitalMarketingService:
    def __init__(self):
        self.seo_optimizer = SEOOptimizer()
        self.social_media_manager = SocialMediaManager()
        self.email_marketing = EmailMarketingService()
        self.analytics_tracker = AnalyticsTracker()

    async def optimize_for_greek_market(self, product_data):
        """Optimize products for Greek market SEO"""
        greek_optimization = {
            "meta_title": await self.seo_optimizer.generate_greek_title(product_data),
            "meta_description": await self.seo_optimizer.generate_greek_description(product_data),
            "greek_keywords": await self.seo_optimizer.extract_greek_keywords(product_data),
            "schema_markup": self.generate_greek_schema(product_data),
            "local_seo": {
                "business_location": product_data.get("business_location"),
                "greek_business_categories": await self.get_greek_business_categories(product_data),
                "local_keywords": await self.generate_local_keywords(product_data)
            }
        }

        return greek_optimization

    async def create_marketing_campaigns(self, campaign_config):
        """Create integrated digital marketing campaigns"""
        campaigns = {}

        # Google Ads campaign for Greek market
        if campaign_config.get("google_ads"):
            campaigns["google_ads"] = await self.create_google_ads_campaign(
                campaign_config["google_ads"],
                target_country="GR",
                languages=["el", "en"]
            )

        # Facebook/Instagram campaigns
        if campaign_config.get("social_media"):
            campaigns["facebook"] = await self.social_media_manager.create_facebook_campaign(
                campaign_config["social_media"]
            )

        # Email marketing for Greek customers
        if campaign_config.get("email_marketing"):
            campaigns["email"] = await self.email_marketing.create_campaign(
                campaign_config["email_marketing"],
                localization="greek"
            )

        return campaigns
```

## 4. Database Design

### 4.1 Multi-Schema Architecture

```sql
-- Core schemas
CREATE SCHEMA core;      -- User management, authentication
CREATE SCHEMA crm;       -- Customer relationship management
CREATE SCHEMA erp;       -- Enterprise resource planning
CREATE SCHEMA config;    -- System configuration
CREATE SCHEMA audit;     -- Audit trails and logging
CREATE SCHEMA custom;    -- Custom entities and fields (EspoCRM-style)
```

### 4.2 Custom Entity Framework (EspoCRM-Style)

```sql
-- Dynamic entity definitions
CREATE TABLE custom.entity_definitions (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    label VARCHAR(200) NOT NULL,
    description TEXT,
    is_system BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Dynamic field definitions
CREATE TABLE custom.field_definitions (
    id UUID PRIMARY KEY,
    entity_id UUID REFERENCES custom.entity_definitions(id),
    name VARCHAR(100) NOT NULL,
    label VARCHAR(200) NOT NULL,
    field_type VARCHAR(50) NOT NULL, -- text, number, date, dropdown, etc.
    is_required BOOLEAN DEFAULT FALSE,
    is_unique BOOLEAN DEFAULT FALSE,
    validation_rules JSONB,
    options JSONB, -- For dropdown, multi-select fields
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dynamic data storage
CREATE TABLE custom.entity_data (
    id UUID PRIMARY KEY,
    entity_id UUID REFERENCES custom.entity_definitions(id),
    record_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    updated_by UUID REFERENCES core.users(id)
);

-- Workflow definitions
CREATE TABLE custom.workflows (
    id UUID PRIMARY KEY,
    entity_id UUID REFERENCES custom.entity_definitions(id),
    name VARCHAR(200) NOT NULL,
    trigger_conditions JSONB NOT NULL,
    actions JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.3 Core CRM Tables

```sql
-- Leads
CREATE TABLE crm.leads (
    id UUID PRIMARY KEY,
    company_name VARCHAR(200),
    contact_person VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    source VARCHAR(100),
    status VARCHAR(50),
    score INTEGER,
    assigned_to UUID REFERENCES core.users(id),
    custom_data JSONB,  -- For custom fields
    created_at TIMESTAMP DEFAULT NOW()
);

-- Customers
CREATE TABLE crm.customers (
    id UUID PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    tax_number VARCHAR(50),
    contact_person VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    address JSONB,
    status VARCHAR(50),
    customer_type VARCHAR(50),
    custom_data JSONB,  -- For custom fields
    created_at TIMESTAMP DEFAULT NOW()
);

-- Interactions
CREATE TABLE crm.interactions (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES crm.customers(id),
    interaction_type VARCHAR(100),
    description TEXT,
    interaction_date TIMESTAMP,
    user_id UUID REFERENCES core.users(id),
    custom_data JSONB,  -- For custom fields
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.4 ERP Tables

```sql
-- Products
CREATE TABLE erp.products (
    id UUID PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id UUID,
    unit_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    tax_rate DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    custom_data JSONB,  -- For custom fields
    created_at TIMESTAMP DEFAULT NOW()
);

-- Invoices
CREATE TABLE erp.invoices (
    id UUID PRIMARY KEY,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    customer_id UUID REFERENCES crm.customers(id),
    issue_date DATE NOT NULL,
    due_date DATE,
    total_amount DECIMAL(12,2),
    tax_amount DECIMAL(12,2),
    status VARCHAR(50),
    aade_mark VARCHAR(200), -- AADE MyDATA mark
    qr_code TEXT, -- Generated QR code for PDF
    mydata_status VARCHAR(50), -- Submission status to AADE
    custom_data JSONB,  -- For custom fields
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 5. API Design

### 5.1 RESTful API Architecture

```python
# Base API structure
@app.get("/api/v1/{entity_type}")
async def list_entities(entity_type: str, filters: dict = None)

@app.post("/api/v1/{entity_type}")
async def create_entity(entity_type: str, data: dict)

@app.get("/api/v1/{entity_type}/{id}")
async def get_entity(entity_type: str, id: UUID)

@app.put("/api/v1/{entity_type}/{id}")
async def update_entity(entity_type: str, id: UUID, data: dict)

@app.delete("/api/v1/{entity_type}/{id}")
async def delete_entity(entity_type: str, id: UUID)
```

### 5.2 Custom Entity API (EspoCRM-Style)

```python
# Dynamic entity management
@app.post("/api/v1/admin/entities")
async def create_entity_definition(definition: EntityDefinition)

@app.post("/api/v1/admin/entities/{entity_id}/fields")
async def add_custom_field(entity_id: UUID, field: FieldDefinition)

@app.post("/api/v1/admin/entities/{entity_id}/workflows")
async def create_workflow(entity_id: UUID, workflow: WorkflowDefinition)

# Dynamic data operations
@app.get("/api/v1/custom/{entity_name}")
async def list_custom_records(entity_name: str, filters: dict = None)

@app.post("/api/v1/custom/{entity_name}")
async def create_custom_record(entity_name: str, data: dict)
```

### 5.3 Voice Command API

```python
@app.post("/api/v1/voice/process")
async def process_voice_command(audio_file: UploadFile):
    # Transcribe audio using Whisper
    transcription = await whisper_service.transcribe(audio_file)

    # Extract intent using GPT-4
    intent = await nlp_service.extract_intent(transcription)

    # Execute command
    result = await command_executor.execute(intent)

    return {"transcription": transcription, "result": result}
```

### 5.4 AADE MyDATA API Integration

```python
@app.post("/api/v1/aade/submit-invoice")
async def submit_invoice_to_aade(invoice_id: UUID):
    # Real-time submission (mandatory since Jan 2024)
    invoice = await get_invoice(invoice_id)
    xml_data = generate_mydata_xml(invoice)

    response = await aade_client.submit_invoice(xml_data)

    if response.success:
        # Generate QR code for PDF
        qr_code = generate_qr_code(response.mark)
        await update_invoice(invoice_id, {
            "aade_mark": response.mark,
            "qr_code": qr_code,
            "mydata_status": "submitted"
        })

    return response
```

## 6. Deployment Architecture

### 6.1 SAAS Deployment (Cloud)

```yaml
# Docker Compose for SAAS
version: "3.8"
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs

  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/erp_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=erp_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

### 6.2 Desktop Web Application Deployment

#### 6.2.1 Local PostgreSQL Database with Encryption

```python
# Local PostgreSQL instance for desktop deployment
import psycopg2
import subprocess
import os
import shutil
from pathlib import Path

class LocalPostgreSQLManager:
    def __init__(self, data_dir: str = "data/postgresql"):
        self.data_dir = Path(data_dir)
        self.port = 5433  # Use different port to avoid conflicts
        self.database_name = "erp_crm_local"
        self.username = "erp_user"
        self.password = self.generate_secure_password()

    def initialize_database(self):
        """Initialize local PostgreSQL instance"""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)

        # Initialize PostgreSQL data directory
        init_cmd = [
            "initdb",
            "-D", str(self.data_dir),
            "-U", self.username,
            "--auth-local=md5",
            "--auth-host=md5",
            "--encoding=UTF8",
            "--locale=en_US.UTF-8"
        ]
        subprocess.run(init_cmd, check=True)

        # Configure PostgreSQL for local use
        self.configure_postgresql()

    def configure_postgresql(self):
        """Configure PostgreSQL for secure local use"""
        config_file = self.data_dir / "postgresql.conf"
        hba_file = self.data_dir / "pg_hba.conf"

        # PostgreSQL configuration
        config_content = f"""
# Local desktop PostgreSQL configuration
port = {self.port}
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 128MB
effective_cache_size = 512MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200

# Encryption and security
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
password_encryption = scram-sha-256
row_security = on

# Logging
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'all'
log_min_error_statement = error
"""

        with open(config_file, 'w') as f:
            f.write(config_content)

        # Host-based authentication
        hba_content = f"""
# Local connections only
local   all             {self.username}                                md5
host    all             {self.username}        127.0.0.1/32            md5
host    all             {self.username}        ::1/128                 md5
"""

        with open(hba_file, 'w') as f:
            f.write(hba_content)

    def start_server(self):
        """Start local PostgreSQL server"""
        start_cmd = [
            "pg_ctl",
            "-D", str(self.data_dir),
            "-l", str(self.data_dir / "log" / "postgresql.log"),
            "start"
        ]
        result = subprocess.run(start_cmd, capture_output=True, text=True)
        return result.returncode == 0

    def stop_server(self):
        """Stop local PostgreSQL server"""
        stop_cmd = [
            "pg_ctl",
            "-D", str(self.data_dir),
            "stop"
        ]
        subprocess.run(stop_cmd)

    def create_application_database(self):
        """Create the application database and schema"""
        conn = psycopg2.connect(
            host="localhost",
            port=self.port,
            user=self.username,
            password=self.password,
            database="postgres"  # Connect to default database first
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            # Create application database
            cur.execute(f"CREATE DATABASE {self.database_name}")

            # Create schemas
            cur.execute("CREATE SCHEMA IF NOT EXISTS core")
            cur.execute("CREATE SCHEMA IF NOT EXISTS crm")
            cur.execute("CREATE SCHEMA IF NOT EXISTS erp")
            cur.execute("CREATE SCHEMA IF NOT EXISTS config")
            cur.execute("CREATE SCHEMA IF NOT EXISTS audit")
            cur.execute("CREATE SCHEMA IF NOT EXISTS custom")

        conn.close()

    def get_connection_string(self):
        """Get connection string for application"""
        return f"postgresql://{self.username}:{self.password}@localhost:{self.port}/{self.database_name}"

class EncryptedLocalDatabase:
    def __init__(self, pg_manager: LocalPostgreSQLManager):
        self.pg_manager = pg_manager
        self.connection_string = pg_manager.get_connection_string()

    def setup_encryption(self):
        """Setup transparent data encryption for sensitive fields"""
        conn = psycopg2.connect(self.connection_string)

        with conn.cursor() as cur:
            # Install pgcrypto extension for encryption functions
            cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

            # Create encryption key table (encrypted itself)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS core.encryption_keys (
                    key_id VARCHAR(50) PRIMARY KEY,
                    encrypted_key TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

        conn.commit()
        conn.close()

    def encrypt_sensitive_field(self, data: str, key_id: str = "default") -> str:
        """Encrypt sensitive data using PostgreSQL pgcrypto"""
        conn = psycopg2.connect(self.connection_string)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT pgp_sym_encrypt(%s, %s)",
                (data, self.get_encryption_key(key_id))
            )
            result = cur.fetchone()[0]

        conn.close()
        return result

    def decrypt_sensitive_field(self, encrypted_data: str, key_id: str = "default") -> str:
        """Decrypt sensitive data using PostgreSQL pgcrypto"""
        conn = psycopg2.connect(self.connection_string)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT pgp_sym_decrypt(%s, %s)",
                (encrypted_data, self.get_encryption_key(key_id))
            )
            result = cur.fetchone()[0]

        conn.close()
        return result
```

#### 6.2.2 Periodic Licensing System

```python
# Licensing system that contacts server periodically, not on every request
class DesktopLicenseManager:
    def __init__(self):
        self.license_server = "https://licensing.yourdomain.com"
        self.last_validation = None
        self.validation_interval = 24 * 60 * 60  # 24 hours
        self.grace_period = 7 * 24 * 60 * 60  # 7 days offline grace period

    async def validate_license_periodic(self, license_key: str) -> bool:
        """Validate license periodically, not on every request"""
        now = time.time()

        # Check if we need to validate (every 24 hours)
        if (self.last_validation and
            now - self.last_validation < self.validation_interval):
            return self.get_cached_license_status()

        try:
            # Contact server for validation
            response = await self.license_client.validate(license_key)

            if response.is_valid and not response.is_expired:
                self.cache_license_status(True, now)
                self.last_validation = now
                return True
            else:
                self.cache_license_status(False, now)
                return False

        except (ConnectionError, TimeoutError):
            # Server unreachable - use grace period
            return self.handle_offline_validation(now)

    def handle_offline_validation(self, current_time: float) -> bool:
        """Handle license validation when server is unreachable"""
        if self.last_validation:
            offline_duration = current_time - self.last_validation
            if offline_duration < self.grace_period:
                # Still within grace period
                return self.get_cached_license_status()

        # Grace period expired
        return False

    async def check_renewal_needed(self, license_key: str) -> bool:
        """Check if license renewal is needed (warn 30 days before expiry)"""
        try:
            response = await self.license_client.get_status(license_key)
            expiry_date = datetime.fromisoformat(response.expiry_date)
            days_until_expiry = (expiry_date - datetime.now()).days
            return days_until_expiry <= 30
        except:
            return False  # Can't check online, assume renewal not needed
```

#### 6.2.3 Desktop Update System

```python
class DesktopUpdateManager:
    def __init__(self):
        self.update_server = "https://updates.yourdomain.com"
        self.current_version = self.get_current_version()
        self.update_check_interval = 24 * 60 * 60  # Check daily

    async def check_for_updates_periodic(self) -> dict:
        """Check for updates periodically, not continuously"""
        try:
            response = await self.update_client.check_version()
            latest_version = response.get('latest_version')

            if self.is_newer_version(latest_version, self.current_version):
                return {
                    'update_available': True,
                    'latest_version': latest_version,
                    'release_notes': response.get('release_notes'),
                    'download_url': response.get('download_url'),
                    'is_critical': response.get('is_critical', False)
                }

            return {'update_available': False}

        except (ConnectionError, TimeoutError):
            # Server unreachable - continue with current version
            return {'update_available': False, 'offline': True}

    async def download_and_apply_update(self, update_info: dict) -> bool:
        """Download and apply update with user consent"""
        try:
            # Download update package
            update_package = await self.download_update_package(
                update_info['download_url']
            )

            # Verify digital signature
            if not self.verify_update_signature(update_package):
                raise UpdateError("Invalid update signature")

            # Create backup of current installation
            backup_path = self.create_backup()

            # Apply update (delta patch or full replacement)
            success = self.apply_update(update_package)

            if success:
                # Schedule restart to complete update
                self.schedule_restart()
                return True
            else:
                # Restore from backup
                self.restore_from_backup(backup_path)
                return False

        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False

    def is_newer_version(self, latest: str, current: str) -> bool:
        """Compare version strings"""
        from packaging import version
        return version.parse(latest) > version.parse(current)
```

#### 6.2.4 Desktop Application Architecture

```python
# Desktop web application architecture (not Electron - pure web app)
class DesktopWebApp:
    def __init__(self):
        self.pg_manager = LocalPostgreSQLManager()
        self.local_db = EncryptedLocalDatabase(self.pg_manager)
        self.license_manager = DesktopLicenseManager()
        self.update_manager = DesktopUpdateManager()
        self.web_server = LocalWebServer()  # Local Flask/FastAPI server

    async def startup(self):
        """Initialize desktop application"""
        # Initialize and start local PostgreSQL
        if not self.pg_manager.is_initialized():
            self.pg_manager.initialize_database()

        if not self.pg_manager.is_running():
            pg_started = self.pg_manager.start_server()
            if not pg_started:
                return self.show_database_error()

        # Setup database encryption
        await self.local_db.setup_encryption()

        # Run database migrations
        await self.run_database_migrations()

        # Validate license (periodic check)
        license_valid = await self.license_manager.validate_license_periodic()
        if not license_valid:
            return self.show_license_error()

        # Check for updates (daily check)
        update_info = await self.update_manager.check_for_updates_periodic()
        if update_info.get('update_available'):
            self.notify_update_available(update_info)

        # Start local web server
        await self.web_server.start(port=8080)

        # Open browser to local application
        self.open_browser("http://localhost:8080")

    async def shutdown(self):
        """Graceful shutdown"""
        await self.web_server.stop()
        self.pg_manager.stop_server()

    def open_browser(self, url: str):
        """Open system default browser to local application"""
        import webbrowser
        webbrowser.open(url)

    async def run_database_migrations(self):
        """Run database migrations for desktop deployment"""
        # Same migration scripts as cloud, but on local PostgreSQL
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", self.pg_manager.get_connection_string())
        command.upgrade(alembic_cfg, "head")

class LocalWebServer:
    """Local web server for desktop deployment"""
    def __init__(self, pg_manager: LocalPostgreSQLManager):
        self.app = FastAPI()
        self.pg_manager = pg_manager
        self.setup_routes()

    def setup_routes(self):
        """Setup API routes for local deployment"""
        @self.app.get("/")
        async def serve_frontend():
            return FileResponse("frontend/index.html")

        @self.app.get("/api/health")
        async def health_check():
            return {
                "status": "healthy",
                "mode": "desktop",
                "database": "postgresql_local",
                "database_port": self.pg_manager.port
            }

        # All other API routes same as cloud version
        # but using local PostgreSQL database instead of cloud PostgreSQL

    async def start(self, port: int = 8080):
        """Start the local web server"""
        import uvicorn
        config = uvicorn.Config(
            app=self.app,
            host="127.0.0.1",  # Localhost only for security
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def stop(self):
        """Stop the local web server"""
        # Graceful shutdown implementation
        pass
```

#### 6.2.5 Desktop vs Cloud Feature Differences

```python
class DeploymentConfiguration:
    def __init__(self, deployment_type: str):
        self.deployment_type = deployment_type  # "cloud" or "desktop"

    def get_database_config(self):
        if self.deployment_type == "cloud":
            return {
                "type": "postgresql",
                "host": os.getenv("DB_HOST"),
                "port": 5432,
                "database": os.getenv("DB_NAME"),
                "username": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "ssl_mode": "require"
            }
        else:  # desktop
            return {
                "type": "postgresql",
                "host": "localhost",
                "port": 5433,  # Different port to avoid conflicts
                "database": "erp_crm_local",
                "username": "erp_user",
                "data_directory": "data/postgresql",
                "encryption": True
            }

    def get_file_storage_config(self):
        if self.deployment_type == "cloud":
            return {
                "type": "s3",
                "bucket": os.getenv("S3_BUCKET"),
                "region": os.getenv("AWS_REGION")
            }
        else:  # desktop
            return {
                "type": "local",
                "path": "data/files/",
                "encryption": True
            }

    def requires_internet_features(self) -> list:
        """Features that require internet connection"""
        return [
            "aade_mydata_submission",  # Always requires internet
            "license_validation",      # Periodic internet required
            "system_updates",         # Periodic internet required
            "cloud_backup",           # Optional internet feature
            "remote_support"          # Optional internet feature
        ]
```

#### 6.2.6 Desktop PostgreSQL Benefits

**Why PostgreSQL for Desktop:**

- **Feature Consistency**: Identical database features between cloud and desktop deployments
- **Complex Queries**: Advanced SQL capabilities for complex ERP reporting and analytics
- **JSONB Support**: Essential for custom fields and dynamic entity framework (EspoCRM-style)
- **Full-Text Search**: Built-in search capabilities for customers, products, invoices
- **Concurrent Access**: Multiple application processes can access database safely
- **Data Integrity**: ACID compliance, foreign keys, constraints, triggers
- **Extensions**: pgcrypto for encryption, uuid-ossp for UUIDs, etc.
- **Scalability**: Can handle enterprise-level data volumes locally
- **Backup/Restore**: Enterprise-grade backup and point-in-time recovery

**Desktop Installation Requirements:**

```yaml
# Desktop Installation Package Requirements
postgresql_version: "16.x"
required_extensions:
  - pgcrypto # Encryption functions
  - uuid-ossp # UUID generation
  - pg_trgm # Trigram matching for search
  - unaccent # Text search without accents

disk_space:
  minimum: 2GB # PostgreSQL + application
  recommended: 10GB # Including data growth

memory:
  minimum: 4GB RAM # System requirement
  postgresql_shared_buffers: 128MB
  postgresql_effective_cache: 512MB

network_ports:
  postgresql: 5433 # Local PostgreSQL instance
  application: 8080 # Local web server
  both_localhost_only: true # Security requirement
```

**Desktop Database Management:**

```python
class DesktopDatabaseManager:
    def __init__(self):
        self.pg_manager = LocalPostgreSQLManager()

    async def backup_database(self, backup_path: str):
        """Create full database backup"""
        backup_cmd = [
            "pg_dump",
            "-h", "localhost",
            "-p", "5433",
            "-U", "erp_user",
            "-d", "erp_crm_local",
            "-f", backup_path,
            "--verbose",
            "--no-password"
        ]
        result = subprocess.run(backup_cmd, capture_output=True, text=True)
        return result.returncode == 0

    async def restore_database(self, backup_path: str):
        """Restore database from backup"""
        restore_cmd = [
            "psql",
            "-h", "localhost",
            "-p", "5433",
            "-U", "erp_user",
            "-d", "erp_crm_local",
            "-f", backup_path,
            "--no-password"
        ]
        result = subprocess.run(restore_cmd, capture_output=True, text=True)
        return result.returncode == 0

    async def vacuum_analyze(self):
        """Optimize database performance"""
        conn = psycopg2.connect(self.pg_manager.get_connection_string())
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute("VACUUM ANALYZE")

        conn.close()

    async def check_database_health(self) -> dict:
        """Check database health and performance"""
        conn = psycopg2.connect(self.pg_manager.get_connection_string())

        health_check = {}

        with conn.cursor() as cur:
            # Check database size
            cur.execute("SELECT pg_size_pretty(pg_database_size('erp_crm_local'))")
            health_check['database_size'] = cur.fetchone()[0]

            # Check active connections
            cur.execute("SELECT count(*) FROM pg_stat_activity WHERE datname = 'erp_crm_local'")
            health_check['active_connections'] = cur.fetchone()[0]

            # Check table sizes
            cur.execute("""
                SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
                FROM pg_tables
                WHERE schemaname IN ('core', 'crm', 'erp', 'custom')
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
                LIMIT 10
            """)
            health_check['largest_tables'] = cur.fetchall()

        conn.close()
        return health_check
```

#### 6.2.7 Document Printing & Template Management System

**Strategic Impact**: Solve the #1 daily pain point for Greek businesses - professional document printing

```python
class DocumentPrintingService:
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.pdf_generator = PDFGenerator()
        self.print_manager = PrintManager()
        self.aade_compliance = AADEComplianceManager()

    async def generate_invoice_pdf(self, invoice_data: dict, template_id: str = "default") -> bytes:
        """Generate AADE-compliant invoice PDF with QR code"""
        # Load template
        template = await self.template_engine.load_template(template_id)

        # Add AADE compliance data
        aade_data = await self.aade_compliance.prepare_invoice_data(invoice_data)

        # Generate QR code for AADE compliance
        qr_code = await self.generate_aade_qr_code(aade_data['mark'])

        # Merge data with template
        merged_data = {
            **invoice_data,
            **aade_data,
            'qr_code': qr_code,
            'generation_timestamp': datetime.now().isoformat()
        }

        # Generate PDF
        pdf_bytes = await self.pdf_generator.generate_pdf(template, merged_data)

        return pdf_bytes

    async def print_document(self, document_data: dict, printer_name: str = None) -> bool:
        """Print document directly to printer"""
        pdf_bytes = await self.generate_document_pdf(document_data)

        return await self.print_manager.print_pdf(
            pdf_bytes,
            printer_name=printer_name,
            copies=document_data.get('copies', 1)
        )

    async def batch_print_invoices(self, invoice_ids: list, printer_name: str = None) -> dict:
        """Batch print multiple invoices"""
        results = {'success': [], 'failed': []}

        for invoice_id in invoice_ids:
            try:
                invoice_data = await self.get_invoice_data(invoice_id)
                success = await self.print_document(invoice_data, printer_name)

                if success:
                    results['success'].append(invoice_id)
                else:
                    results['failed'].append(invoice_id)

            except Exception as e:
                results['failed'].append({'invoice_id': invoice_id, 'error': str(e)})

        return results

class TemplateEngine:
    def __init__(self):
        self.template_cache = {}
        self.supported_formats = ['html', 'jinja2', 'mustache']

    async def load_template(self, template_id: str) -> dict:
        """Load document template"""
        if template_id in self.template_cache:
            return self.template_cache[template_id]

        template = await self.get_template_from_db(template_id)

        # Cache template for performance
        self.template_cache[template_id] = template

        return template

    async def get_greek_invoice_templates(self) -> list:
        """Get pre-built Greek invoice templates"""
        return [
            {
                'id': 'greek_standard',
                'name': 'Τυπικό Τιμολόγιο',
                'description': 'Πρότυπο τιμολόγιο σύμφωνα με ΑΑΔΕ',
                'preview_url': '/templates/previews/greek_standard.png',
                'compliant_with': ['AADE', 'MyDATA', 'Greek_Tax_Code']
            },
            {
                'id': 'greek_retail',
                'name': 'Λιανικό Τιμολόγιο',
                'description': 'Για λιανικές επιχειρήσεις',
                'preview_url': '/templates/previews/greek_retail.png',
                'compliant_with': ['AADE', 'MyDATA', 'POS_Integration']
            },
            {
                'id': 'greek_b2b',
                'name': 'Επιχειρηματικό Τιμολόγιο',
                'description': 'Για B2B συναλλαγές',
                'preview_url': '/templates/previews/greek_b2b.png',
                'compliant_with': ['AADE', 'MyDATA', 'Advanced_Tax_Rules']
            },
            {
                'id': 'greek_export',
                'name': 'Τιμολόγιο Εξαγωγής',
                'description': 'Για εξαγωγικές συναλλαγές',
                'preview_url': '/templates/previews/greek_export.png',
                'compliant_with': ['AADE', 'MyDATA', 'EU_VAT_Rules', 'Export_Regulations']
            }
        ]

class PDFGenerator:
    def __init__(self):
        self.engine = "weasyprint"  # Better for Greek fonts and complex layouts
        self.fonts_path = "assets/fonts/"
        self.greek_fonts = {
            'primary': 'Roboto',
            'secondary': 'Arial Unicode MS',
            'fallback': 'DejaVu Sans'
        }

    async def generate_pdf(self, template: dict, data: dict) -> bytes:
        """Generate PDF from template and data"""
        # Render HTML with Greek text support
        html_content = await self.render_html(template, data)

        # Configure PDF settings
        pdf_config = {
            'page_size': 'A4',
            'margin': {
                'top': '2cm',
                'right': '1.5cm',
                'bottom': '2cm',
                'left': '1.5cm'
            },
            'font_size': '10pt',
            'encoding': 'utf-8',
            'greek_font_support': True
        }

        # Generate PDF
        pdf_bytes = await self.html_to_pdf(html_content, pdf_config)

        return pdf_bytes

    def format_greek_date(self, date_obj) -> str:
        """Format date in Greek format"""
        greek_months = {
            1: 'Ιανουάριος', 2: 'Φεβρουάριος', 3: 'Μάρτιος', 4: 'Απρίλιος',
            5: 'Μάιος', 6: 'Ιούνιος', 7: 'Ιούλιος', 8: 'Αύγουστος',
            9: 'Σεπτέμβριος', 10: 'Οκτώβριος', 11: 'Νοέμβριος', 12: 'Δεκέμβριος'
        }

        return f"{date_obj.day} {greek_months[date_obj.month]} {date_obj.year}"

    def format_greek_currency(self, amount: float) -> str:
        """Format currency in Greek format"""
        return f"{amount:,.2f} €".replace(",", ".")

class PrintManager:
    def __init__(self):
        self.available_printers = self.get_available_printers()
        self.default_printer = self.get_default_printer()
        self.print_queue = []

    def get_available_printers(self) -> list:
        """Get list of available printers"""
        import cups  # CUPS for Linux/Mac
        import win32print  # Windows printing

        printers = []

        if platform.system() == "Windows":
            # Windows printer discovery
            for printer in win32print.EnumPrinters(2):
                printers.append({
                    'name': printer[2],
                    'status': 'available',
                    'type': 'local' if 'USB' in printer[2] else 'network'
                })
        else:
            # Linux/Mac printer discovery
            conn = cups.Connection()
            for printer_name in conn.getPrinters():
                printers.append({
                    'name': printer_name,
                    'status': 'available',
                    'type': 'cups'
                })

        return printers

    async def print_pdf(self, pdf_bytes: bytes, printer_name: str = None, copies: int = 1) -> bool:
        """Print PDF document"""
        if not printer_name:
            printer_name = self.default_printer

        try:
            # Create temporary PDF file
            temp_pdf_path = f"/tmp/invoice_{uuid.uuid4().hex}.pdf"

            with open(temp_pdf_path, 'wb') as f:
                f.write(pdf_bytes)

            # Print document
            success = await self.send_to_printer(temp_pdf_path, printer_name, copies)

            # Clean up temporary file
            os.remove(temp_pdf_path)

            return success

        except Exception as e:
            logger.error(f"Print job failed: {e}")
            return False

class AADEComplianceManager:
    def __init__(self):
        self.qr_generator = QRCodeGenerator()

    async def prepare_invoice_data(self, invoice_data: dict) -> dict:
        """Prepare invoice data for AADE compliance"""
        # Add required AADE fields
        aade_data = {
            'mark': invoice_data.get('aade_mark', ''),
            'uid': invoice_data.get('aade_uid', ''),
            'qr_code_url': f"https://mydata.aade.gr/invoices/{invoice_data.get('aade_mark', '')}",
            'submission_date': invoice_data.get('aade_submission_date', ''),
            'compliance_version': '1.0.11',
            'digital_signature': await self.generate_digital_signature(invoice_data)
        }

        return aade_data

    async def generate_aade_qr_code(self, mark: str) -> str:
        """Generate QR code for AADE compliance"""
        qr_url = f"https://mydata.aade.gr/invoices/{mark}"
        qr_code_base64 = await self.qr_generator.generate_qr_base64(qr_url)

        return qr_code_base64

# Greek Document Types Support
class GreekDocumentTypes:
    def __init__(self):
        self.document_types = {
            'invoice': {
                'greek_name': 'Τιμολόγιο',
                'aade_type': 'invoice',
                'required_fields': ['company_vat', 'customer_vat', 'line_items'],
                'template_variants': ['b2b', 'b2c', 'retail', 'export']
            },
            'receipt': {
                'greek_name': 'Απόδειξη',
                'aade_type': 'receipt',
                'required_fields': ['company_vat', 'line_items'],
                'template_variants': ['pos', 'service', 'retail']
            },
            'delivery_note': {
                'greek_name': 'Δελτίο Αποστολής',
                'aade_type': 'delivery_note',
                'required_fields': ['company_vat', 'customer_vat', 'items'],
                'template_variants': ['standard', 'detailed', 'export']
            },
            'credit_note': {
                'greek_name': 'Πιστωτικό Σημείωμα',
                'aade_type': 'credit_note',
                'required_fields': ['original_invoice', 'reason', 'amount'],
                'template_variants': ['refund', 'adjustment', 'return']
            },
            'proforma': {
                'greek_name': 'Προτιμολόγιο',
                'aade_type': 'proforma',
                'required_fields': ['company_vat', 'customer_vat', 'line_items'],
                'template_variants': ['quote', 'estimate', 'preview']
            }
        }
```

#### 6.2.8 Template Management Database Schema

```sql
-- Document Templates
CREATE TABLE IF NOT EXISTS erp.document_templates (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    template_type VARCHAR(50) NOT NULL, -- invoice, receipt, delivery_note, etc.
    html_content TEXT NOT NULL,
    css_content TEXT,
    required_fields JSONB NOT NULL,
    custom_settings JSONB,
    is_aade_compliant BOOLEAN DEFAULT FALSE,
    is_default BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES core.users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Print Job Queue
CREATE TABLE IF NOT EXISTS erp.print_jobs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES core.users(id),
    document_type VARCHAR(50) NOT NULL,
    document_id UUID NOT NULL,
    template_id UUID REFERENCES erp.document_templates(id),
    printer_name VARCHAR(200),
    copies INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'pending', -- pending, printing, completed, failed
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_templates_type ON erp.document_templates(template_type);
CREATE INDEX idx_print_jobs_status ON erp.print_jobs(status);
CREATE INDEX idx_print_jobs_user ON erp.print_jobs(user_id);
```

#### 6.2.9 Printing System Benefits

**Key Features:**

- **🇬🇷 Greek Compliance**: AADE-compliant templates with automatic QR codes
- **🎨 Professional Templates**: Pre-built templates for all Greek document types
- **🖨️ Direct Printing**: Print to any local or network printer
- **📄 Batch Processing**: Print multiple documents at once
- **⚡ Template Caching**: Fast template loading and rendering
- **🔧 Customizable**: Visual template editor for business branding
- **📱 Multi-format**: PDF, HTML, and direct printer support

**Greek Document Types Supported:**

- Τιμολόγιο (Invoice) - B2B, B2C, Retail, Export variants
- Απόδειξη (Receipt) - POS, Service, Retail variants
- Δελτίο Αποστολής (Delivery Note) - Standard, Detailed, Export
- Πιστωτικό Σημείωμα (Credit Note) - Refund, Adjustment, Return
- Προτιμολόγιο (Proforma) - Quote, Estimate, Preview

**Competitive Advantage:**

- **Zero Setup**: Works out-of-the-box with Greek compliance
- **Professional Quality**: Enterprise-grade PDF generation
- **Local Printing**: Direct printer integration (no cloud dependency)
- **Template Library**: 20+ pre-built Greek business templates
- **Custom Branding**: Logo, colors, layout customization

## 7. Security Architecture

### 7.1 Authentication & Authorization

```python
# JWT-based authentication with refresh tokens
class SecurityService:
    def generate_access_token(self, user_id: UUID, permissions: List[str]) -> str:
        payload = {
            "user_id": str(user_id),
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(minutes=15),  # Short-lived
            "type": "access"
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def generate_refresh_token(self, user_id: UUID) -> str:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + timedelta(days=7),  # Longer-lived
            "type": "refresh"
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
```

### 7.2 Data Encryption

```python
# AES-256 encryption for sensitive data
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like tax numbers, bank details"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted_bytes)
        return decrypted.decode()
```

## 8. Integration Architecture

### 8.1 AADE MyDATA Integration (2025 Current)

```python
class AADEMyDataClient:
    def __init__(self, environment: str = "production"):
        self.base_url = {
            "production": "https://mydata.aade.gr",
            "sandbox": "https://mydata-dev.aade.gr"
        }[environment]

        self.endpoints = {
            "submit_invoice": "/invoicesDoc",
            "get_status": "/requestedDoc",
            "classification": "/incomeClassification",
            "expense_classification": "/expensesClassification"
        }

    async def submit_invoice_realtime(self, invoice_xml: str) -> AADEResponse:
        """Submit invoice in real-time (mandatory since Jan 2024)"""
        headers = {
            "Content-Type": "application/xml",
            "aade-user-id": self.user_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}{self.endpoints['submit_invoice']}",
                data=invoice_xml,
                headers=headers
            ) as response:
                result = await response.text()
                return self.parse_aade_response(result)

    def generate_qr_code(self, mark: str) -> str:
        """Generate QR code for PDF invoices (mandatory 2025)"""
        qr_data = f"https://mydata.aade.gr/invoices/{mark}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Convert to base64 for embedding in PDF
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
```

## 9. Performance Architecture

### 9.1 Caching Strategy

```python
# Redis-based caching
class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.cache_ttl = {
            "user_sessions": 3600,  # 1 hour
            "customer_data": 1800,  # 30 minutes
            "product_catalog": 7200,  # 2 hours
            "reports": 600  # 10 minutes
        }

    async def get_or_set(self, key: str, fetch_func: callable, ttl: int = None):
        """Get from cache or fetch and set"""
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)

        data = await fetch_func()
        await self.redis.setex(
            key,
            ttl or self.cache_ttl.get(key.split(":")[0], 300),
            json.dumps(data, default=str)
        )
        return data
```

### 9.2 Database Optimization

```sql
-- Indexing strategy for performance
CREATE INDEX CONCURRENTLY idx_invoices_customer_date
ON erp.invoices(customer_id, issue_date DESC);

CREATE INDEX CONCURRENTLY idx_customers_search
ON crm.customers USING gin(to_tsvector('english', company_name || ' ' || contact_person));

CREATE INDEX CONCURRENTLY idx_products_category
ON erp.products(category_id) WHERE is_active = true;

-- Partitioning for large tables
CREATE TABLE erp.invoices_y2025 PARTITION OF erp.invoices
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

## 10. Monitoring and Observability

### 10.1 Application Monitoring

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
active_users = Gauge('active_users_total', 'Number of active users')

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    request_count.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    request_duration.observe(time.time() - start_time)

    return response
```

### 10.2 Error Tracking

```python
# Sentry integration for error tracking
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FastApiIntegration(auto_enabling=True)],
    traces_sample_rate=0.1,
    release="erp-crm@1.0.0"
)
```

## 11. Technical Support Architecture

### 11.1 Remote Support System

```python
class RemoteSupportService:
    def __init__(self):
        self.screen_share_client = ScreenShareClient()
        self.remote_control_client = RemoteControlClient()
        self.chat_service = ChatService()

    async def initiate_support_session(self, customer_id: UUID) -> str:
        """Initialize remote support session"""
        session_id = str(uuid4())
        session_token = self.generate_session_token(customer_id, session_id)

        # Create secure tunnel
        tunnel_url = await self.create_secure_tunnel(session_id)

        # Log support session
        await self.log_support_session(customer_id, session_id, "initiated")

        return {
            "session_id": session_id,
            "tunnel_url": tunnel_url,
            "session_token": session_token
        }

    async def provide_guided_assistance(self, session_id: str, issue_type: str):
        """Provide step-by-step guidance"""
        guidance_steps = await self.get_guidance_steps(issue_type)

        for step in guidance_steps:
            await self.send_guidance_message(session_id, step)
            await self.wait_for_user_confirmation(session_id)
```

## 12. Database Architecture Strategy

### 12.1 Separate Database Per Company Architecture

**Strategic Decision**: Each company gets its own dedicated database with intelligent resource pooling and automated management.

```python
# Company Database Management
class CompanyDatabaseManager:
    def __init__(self):
        self.resource_pools = {
            'small': PostgreSQLPool(max_connections=50),
            'medium': PostgreSQLPool(max_connections=200),
            'large': DedicatedPostgreSQLInstance()
        }

    async def provision_company_database(self, company_id: str, tier: str):
        """Provision new company database with intelligent resource allocation"""
        db_config = await self.calculate_resource_needs(company_id, tier)

        # Create dedicated database
        db_name = f"company_{company_id}"
        await self.create_database(db_name, db_config)

        # Apply company-specific partitioning
        await self.setup_partitioning_strategy(db_name, company_id)

        # Configure automated backups
        await self.setup_backup_strategy(db_name, tier)

        return db_config

    async def setup_partitioning_strategy(self, db_name: str, company_id: str):
        """Setup intelligent partitioning within company database"""

        # Customer data: Yearly partitions for historical access
        await self.create_yearly_partitions(db_name, 'customers', years=10)

        # Transactions: Monthly partitions for performance
        await self.create_monthly_partitions(db_name, 'invoices', months=60)
        await self.create_monthly_partitions(db_name, 'payments', months=60)

        # Analytics: Quarterly partitions for reporting
        await self.create_quarterly_partitions(db_name, 'analytics_data', quarters=20)
```

**Benefits of This Architecture**:

- **Complete Company Isolation**: No data leakage between companies
- **Historical Data Access**: No fiscal year switching - all data always accessible
- **Optimal Performance**: No write contention between companies
- **Flexible Scaling**: Small companies share resources, large get dedicated infrastructure
- **77% Cost Reduction**: Vs traditional dedicated database approach

### 12.2 Intelligent Resource Pooling

```yaml
# Resource Pool Configuration
resource_pools:
  small_companies:
    max_companies_per_instance: 50
    postgresql_config:
      shared_buffers: "256MB"
      max_connections: 100
      work_mem: "4MB"

  medium_companies:
    max_companies_per_instance: 10
    postgresql_config:
      shared_buffers: "1GB"
      max_connections: 200
      work_mem: "8MB"

  large_companies:
    dedicated_instance: true
    postgresql_config:
      shared_buffers: "4GB"
      max_connections: 500
      work_mem: "16MB"
```

## 13. AI Infrastructure & Voice Commands

### 13.1 Containerized AI Services Architecture

**Development Setup**: Containerized microservices leveraging RTX 4080 GPU for AI workloads.

```yaml
# AI Services Docker Compose
version: "3.8"
services:
  # Core ERP Stack
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_VOICE_API_URL=http://localhost:8002

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  # AI Services Stack
  voice-service:
    build: ./ai-services/voice
    ports:
      - "8002:8002"
    environment:
      - WHISPER_MODEL=medium
      - CUDA_VISIBLE_DEVICES=0
      - GPU_MEMORY_FRACTION=0.6
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./ai-models:/app/models

  ai-support-service:
    build: ./ai-services/support
    ports:
      - "8003:8003"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - CUDA_VISIBLE_DEVICES=0
      - GPU_MEMORY_FRACTION=0.4
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

### 13.2 Voice Command Service

```python
# Voice Command Processing Service
class GreekVoiceCommandService:
    def __init__(self):
        self.whisper_model = whisper.load_model("medium")
        self.greek_intent_classifier = GreekIntentClassifier()
        self.business_context = GreekBusinessContext()

    async def process_voice_command(self, audio_data: bytes, company_id: str) -> dict:
        """Process Greek voice command with business context"""

        # 1. Speech to Text (Greek language optimized)
        transcription = await self.transcribe_greek_audio(audio_data)

        # 2. Intent Classification with Greek business terms
        intent = await self.greek_intent_classifier.classify(
            transcription,
            business_context=await self.business_context.get_company_context(company_id)
        )

        # 3. Execute business action
        result = await self.execute_business_action(intent, company_id)

        return {
            "transcription": transcription,
            "intent": intent,
            "action_result": result,
            "confidence": intent.confidence
        }

    async def transcribe_greek_audio(self, audio_data: bytes) -> str:
        """Whisper transcription optimized for Greek business terms"""

        # Load audio
        audio = whisper.load_audio(io.BytesIO(audio_data))

        # Transcribe with Greek language preference
        result = self.whisper_model.transcribe(
            audio,
            language="el",  # Greek language code
            task="transcribe",
            # Add Greek business terminology hints
            initial_prompt="Τιμολόγιο, πελάτης, παραγγελία, πληρωμή, ΑΦΜ, ΦΠΑ"
        )

        return result["text"]

# Greek Voice Commands Examples
greek_voice_commands = {
    "δημιουργία_τιμολογίου": {
        "patterns": [
            "δημιούργησε τιμολόγιο για {customer}",
            "νέο τιμολόγιο {customer}",
            "τιμολόγιο για τον {customer}"
        ],
        "action": "create_invoice",
        "entities": ["customer"]
    },
    "αναζήτηση_πελάτη": {
        "patterns": [
            "βρες τον πελάτη {customer_name}",
            "αναζήτηση {customer_name}",
            "πελάτης {customer_name}"
        ],
        "action": "search_customer",
        "entities": ["customer_name"]
    },
    "κατάσταση_πληρωμών": {
        "patterns": [
            "εκκρεμείς πληρωμές",
            "τι οφείλουν οι πελάτες",
            "πληρωμές που περιμένω"
        ],
        "action": "show_outstanding_payments",
        "entities": []
    }
}
```

### 13.3 Production AI Infrastructure

**Production Scaling Strategy**: Separate dedicated machines for AI workloads.

```yaml
# Production Infrastructure
production_infrastructure:
  main_app_server:
    specs: "16 CPU, 32GB RAM, 1TB SSD"
    services: [api, frontend, postgres, redis]
    location: "Primary datacenter"

  gpu_voice_server:
    specs: "8 CPU, 16GB RAM, RTX 4080/A6000, 500GB SSD"
    services: [voice-service, whisper-models]
    location: "AI processing datacenter"
    gpu_memory: "16GB dedicated for Whisper"

  ai_support_server:
    specs: "12 CPU, 24GB RAM, RTX 4070/A5000, 500GB SSD"
    services: [ai-support-service, llm-models]
    location: "AI processing datacenter"
    gpu_memory: "12GB for LLM inference"
```

## 14. Deployment & DevOps Architecture

### 14.1 SAAS Deployment (Cloud)

```yaml
# Enhanced Docker Compose for SAAS with AI Services
version: "3.8"
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs

  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/erp_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
      - NEXT_PUBLIC_VOICE_API_URL=https://voice.yourdomain.com

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=erp_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  # AI Services for production
  voice-service:
    build: ./ai-services/voice
    ports:
      - "8002:8002"
    environment:
      - WHISPER_MODEL=medium
    volumes:
      - ai_models:/app/models

  ai-support-service:
    build: ./ai-services/support
    ports:
      - "8003:8003"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
  ai_models:
```

This architecture provides a comprehensive foundation for building a modern, scalable, and compliant ERP/CRM system specifically designed for the Greek market, incorporating the latest 2025 technologies, revolutionary database architecture, and cutting-edge AI capabilities including Greek voice commands.
