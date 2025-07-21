"""
Database models for Greek ERP/CRM System
"""

from .company import Company
from .user import User
from .business_entity import BusinessEntity, BusinessEntityType, BusinessEntityStatus, BusinessEntityRole, PaymentTerms
from .contact import Contact, ContactType, ContactStatus
from .contact_method import ContactMethod, ContactMethodType, ContactMethodStatus
from .contact_method_subtype import ContactMethodSubType, SYSTEM_DEFAULT_SUBTYPES
from .contact_company_history import ContactCompanyHistory, RelationshipType, RelationshipStatus
from .product import (
    Product, ProductCategory, ProductAttribute, ProductAttributeValue, 
    ProductVariant, ProductInventory, VatCategory, ProductType, ProductStatus
)
from .invoice import Invoice, InvoiceItem
from .audit_log import AuditLog, AuditService, AuditAction, AuditEntityType
from .product_vat_config import (
    ProductVATConfig, VATSuggestionRule, SupplierInvoiceVATValidation,
    VATConfigStatus, VATSuggestionConfidence, ProductServiceTemplate
)
from .document_state_machine import (
    DocumentState, DocumentAction, StateTransitionRule, DocumentWorkflowInstance,
    DocumentStateHistory, DocumentAutomationRule, GreekDocumentWorkflowTemplate,
    GREEK_DOCUMENT_WORKFLOWS
)

# CRM Models
from .lead import (
    Lead, LeadStatus, LeadSource, LeadRating, LeadQualificationCriteria,
    LeadQualificationHistory
)
from .opportunity import (
    Opportunity, OpportunityStage, OpportunityType, OpportunityPriority,
    OpportunitySource, OpportunityStageHistory, OpportunityProduct
)
from .activity import (
    Activity, ActivityType, ActivityStatus, ActivityPriority, CallDirection,
    CallOutcome, MeetingType, ActivityTemplate
)
from .campaign import (
    Campaign, CampaignType, CampaignStatus, CampaignPriority, CampaignObjective,
    CampaignMetrics
)
from .case import (
    Case, CaseType, CaseStatus, CasePriority, CaseSeverity, CaseSource,
    ResolutionType, CaseComment, CaseAttachment
)

# ERP Models
from .purchase_order import (
    PurchaseOrder, PurchaseOrderItem, PurchaseRequisition,
    PurchaseOrderStatus, PurchaseOrderType, PurchaseOrderPriority, DeliveryTerm
)
from .inventory import (
    Location, InventoryItem, StockMovement, PhysicalCount, PhysicalCountLine,
    StockMovementType, InventoryStatus, LocationType, CountType
)
from .accounting import (
    ChartOfAccounts, JournalEntry, JournalEntryLine, AccountingPeriod,
    AccountType, AccountSubType, JournalType, JournalStatus
)

# Voice Command Models
from .voice_command import (
    SystemVoiceCommand, UserVoiceCommand, VoiceCommandLog, VoiceCommandTemplate,
    VoiceCommandType, VoiceCommandStatus, VoiceActionType, DEFAULT_VOICE_COMMANDS
)

# Greek Reference Data Models (Master Database)
from .greek_reference_data import (
    GreekRegion, GreekTaxOffice, GreekVATRate, GreekBusinessActivity,
    GreekLegalForm, GreekBank, PostalCode, VATZone, LocationType
)

# System Configuration Models (Master Database)
from .system_configuration import (
    SystemConfiguration, SubscriptionPlanDefinition, CompanySubscription,
    UsageMetric, SystemNotification, ApiKey, ConfigurationType,
    SubscriptionPlan, SubscriptionStatus
)

# Dynamic Entities Models
from .dynamic_entity import DynamicEntity, EntityScope, EntityStatus
from .dynamic_field import DynamicField, FieldType, FieldWidgetType
from .entity_layout import EntityLayout, LayoutType, LayoutStatus, ResponsiveBreakpoint

__all__ = [
    # Core Models
    "Company",
    "User", 
    "BusinessEntity",
    "BusinessEntityType", 
    "BusinessEntityStatus", 
    "BusinessEntityRole", 
    "PaymentTerms",
    "Contact",
    "ContactType", 
    "ContactStatus",
    "ContactMethod",
    "ContactMethodType",
    "ContactMethodStatus",
    "ContactMethodSubType",
    "SYSTEM_DEFAULT_SUBTYPES",
    "ContactCompanyHistory",
    "RelationshipType",
    "RelationshipStatus",
    "Product",
    "ProductCategory",
    "ProductAttribute",
    "ProductAttributeValue",
    "ProductVariant", 
    "ProductInventory",
    "VatCategory",
    "ProductType",
    "ProductStatus",
    "Invoice",
    "InvoiceItem",
    "AuditLog",
    "AuditService",
    "AuditAction",
    "AuditEntityType",
    "ProductVATConfig",
    "VATSuggestionRule",
    "SupplierInvoiceVATValidation",
    "VATConfigStatus",
    "VATSuggestionConfidence",
    "ProductServiceTemplate",
    "DocumentState",
    "DocumentAction",
    "StateTransitionRule",
    "DocumentWorkflowInstance",
    "DocumentStateHistory",
    "DocumentAutomationRule",
    "GreekDocumentWorkflowTemplate",
    "GREEK_DOCUMENT_WORKFLOWS",
    
    # CRM Models
    "Lead",
    "LeadStatus",
    "LeadSource", 
    "LeadRating",
    "LeadQualificationCriteria",
    "LeadQualificationHistory",
    "Opportunity",
    "OpportunityStage",
    "OpportunityType",
    "OpportunityPriority",
    "OpportunitySource",
    "OpportunityStageHistory",
    "OpportunityProduct",
    "Activity",
    "ActivityType",
    "ActivityStatus",
    "ActivityPriority",
    "CallDirection",
    "CallOutcome",
    "MeetingType",
    "ActivityTemplate",
    "Campaign",
    "CampaignType",
    "CampaignStatus",
    "CampaignPriority",
    "CampaignObjective",
    "CampaignMetrics",
    "Case",
    "CaseType",
    "CaseStatus",
    "CasePriority",
    "CaseSeverity",
    "CaseSource",
    "ResolutionType",
    "CaseComment",
    "CaseAttachment",
    
    # ERP Models
    "PurchaseOrder",
    "PurchaseOrderItem",
    "PurchaseRequisition",
    "PurchaseOrderStatus",
    "PurchaseOrderType",
    "PurchaseOrderPriority",
    "DeliveryTerm",
    "Location",
    "InventoryItem",
    "StockMovement",
    "PhysicalCount",
    "PhysicalCountLine",
    "StockMovementType",
    "InventoryStatus",
    "LocationType",
    "CountType",
    "ChartOfAccounts",
    "JournalEntry",
    "JournalEntryLine",
    "AccountingPeriod",
    "AccountType",
    "AccountSubType",
    "JournalType",
    "JournalStatus",
    
    # Voice Command Models
    "SystemVoiceCommand",
    "UserVoiceCommand",
    "VoiceCommandLog",
    "VoiceCommandTemplate",
    "VoiceCommandType",
    "VoiceCommandStatus",
    "VoiceActionType",
    "DEFAULT_VOICE_COMMANDS",
    
    # Greek Reference Data Models (Master Database)
    "GreekRegion",
    "GreekTaxOffice",
    "GreekVATRate",
    "GreekBusinessActivity",
    "GreekLegalForm",
    "GreekBank",
    "PostalCode",
    "VATZone",
    "LocationType",
    
    # System Configuration Models (Master Database)
    "SystemConfiguration",
    "SubscriptionPlanDefinition",
    "CompanySubscription",
    "UsageMetric",
    "SystemNotification",
    "ApiKey",
    "ConfigurationType",
    "SubscriptionPlan",
    "SubscriptionStatus",
    
    # Dynamic Entities Models
    "DynamicEntity",
    "EntityScope", 
    "EntityStatus",
    "DynamicField",
    "FieldType",
    "FieldWidgetType",
    "EntityLayout",
    "LayoutType",
    "LayoutStatus",
    "ResponsiveBreakpoint",
] 