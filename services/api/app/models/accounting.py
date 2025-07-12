"""
Accounting models for Greek ERP/CRM System
Chart of accounts, journal entries, and financial accounting
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey, Enum, Numeric, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from typing import Optional, Dict, Any, List
from decimal import Decimal
from datetime import datetime

from ..core.database import Base


class AccountType(enum.Enum):
    """Chart of accounts type classification"""
    ASSET = "asset"                 # Ενεργητικό
    LIABILITY = "liability"         # Παθητικό
    EQUITY = "equity"              # Ίδια κεφάλαια
    REVENUE = "revenue"            # Έσοδα
    EXPENSE = "expense"            # Έξοδα
    OTHER_INCOME = "other_income"  # Άλλα έσοδα
    OTHER_EXPENSE = "other_expense" # Άλλα έξοδα


class AccountSubType(enum.Enum):
    """Account sub-type classification"""
    # Assets
    CURRENT_ASSET = "current_asset"             # Κυκλοφορούν ενεργητικό
    FIXED_ASSET = "fixed_asset"                 # Πάγιο ενεργητικό
    INTANGIBLE_ASSET = "intangible_asset"       # Άυλα στοιχεία
    INVESTMENT = "investment"                   # Επενδύσεις
    
    # Liabilities
    CURRENT_LIABILITY = "current_liability"     # Βραχυπρόθεσμες υποχρεώσεις
    LONG_TERM_LIABILITY = "long_term_liability" # Μακροπρόθεσμες υποχρεώσεις
    
    # Equity
    SHARE_CAPITAL = "share_capital"             # Μετοχικό κεφάλαιο
    RETAINED_EARNINGS = "retained_earnings"     # Κέρδη εις νέον
    
    # Revenue
    SALES_REVENUE = "sales_revenue"             # Έσοδα πωλήσεων
    SERVICE_REVENUE = "service_revenue"         # Έσοδα υπηρεσιών
    
    # Expenses
    COST_OF_GOODS_SOLD = "cost_of_goods_sold"   # Κόστος πωληθέντων
    OPERATING_EXPENSE = "operating_expense"     # Λειτουργικά έξοδα
    ADMINISTRATIVE_EXPENSE = "administrative_expense" # Διοικητικά έξοδα


class JournalType(enum.Enum):
    """Journal entry type"""
    GENERAL = "general"                 # Γενικό ημερολόγιο
    SALES = "sales"                     # Ημερολόγιο πωλήσεων
    PURCHASES = "purchases"             # Ημερολόγιο αγορών
    CASH_RECEIPTS = "cash_receipts"     # Ημερολόγιο εισπράξεων
    CASH_PAYMENTS = "cash_payments"     # Ημερολόγιο πληρωμών
    PAYROLL = "payroll"                 # Ημερολόγιο μισθοδοσίας
    ADJUSTING = "adjusting"             # Προσαρμοστικές εγγραφές
    CLOSING = "closing"                 # Εγγραφές κλεισίματος
    OPENING = "opening"                 # Εγγραφές ανοίγματος


class JournalStatus(enum.Enum):
    """Journal entry status"""
    DRAFT = "draft"             # Προσχέδιο
    POSTED = "posted"           # Καταχωρημένο
    REVERSED = "reversed"       # Αντιστραμμένο
    CANCELLED = "cancelled"     # Ακυρωμένο


class ChartOfAccounts(Base):
    """
    Chart of accounts for Greek accounting
    """
    __tablename__ = "chart_of_accounts"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Account identification
    account_code = Column(String(20), nullable=False, index=True)
    account_name = Column(String(255), nullable=False)
    account_name_en = Column(String(255))  # English name
    description = Column(Text)
    
    # Account classification
    account_type = Column(Enum(AccountType), nullable=False)
    account_subtype = Column(Enum(AccountSubType))
    
    # Greek accounting specifics
    greek_account_code = Column(String(20))  # Greek GAAP account code
    is_greek_required = Column(Boolean, default=False)  # Required by Greek law
    
    # Account hierarchy
    parent_account_id = Column(UUID(as_uuid=True), ForeignKey('chart_of_accounts.id'), index=True)
    account_level = Column(Integer, default=1)
    account_path = Column(String(500))  # Full path like "1/11/1101"
    
    # Account properties
    is_active = Column(Boolean, default=True)
    is_header_account = Column(Boolean, default=False)  # Summary account
    allow_posting = Column(Boolean, default=True)      # Allow direct posting
    
    # Balance tracking
    normal_balance = Column(String(10), nullable=False)  # "debit" or "credit"
    current_balance = Column(Numeric(15, 2), default=0)
    ytd_balance = Column(Numeric(15, 2), default=0)
    opening_balance = Column(Numeric(15, 2), default=0)
    
    # Financial statement presentation
    balance_sheet_section = Column(String(100))  # Where to show on balance sheet
    income_statement_section = Column(String(100))  # Where to show on P&L
    statement_order = Column(Integer, default=0)
    
    # VAT and tax settings
    default_vat_code = Column(String(20))
    is_vat_account = Column(Boolean, default=False)
    vat_rate = Column(Numeric(5, 2))
    
    # Bank account details (for bank accounts)
    bank_name = Column(String(255))
    bank_branch = Column(String(255))
    iban = Column(String(34))
    swift_bic = Column(String(11))
    account_number = Column(String(50))
    
    # Reconciliation settings
    requires_reconciliation = Column(Boolean, default=False)
    last_reconciled_date = Column(DateTime)
    
    # Budget and control
    budget_amount = Column(Numeric(15, 2))
    budget_period = Column(String(20))  # "monthly", "quarterly", "annual"
    
    # Custom fields
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    
    # Relationships
    parent_account = relationship("ChartOfAccounts", remote_side=[id], foreign_keys=[parent_account_id])
    child_accounts = relationship("ChartOfAccounts", foreign_keys=[parent_account_id])
    journal_entries = relationship("JournalEntryLine", back_populates="account")
    
    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('company_id', 'account_code', name='uq_account_company_code'),
        Index('idx_account_company', 'company_id'),
        Index('idx_account_code', 'account_code'),
        Index('idx_account_type', 'account_type'),
        Index('idx_account_subtype', 'account_subtype'),
        Index('idx_account_active', 'is_active'),
        Index('idx_account_parent', 'parent_account_id'),
        Index('idx_account_level', 'account_level'),
        Index('idx_account_greek_code', 'greek_account_code'),
    )
    
    def __repr__(self):
        return f"<ChartOfAccounts(id={self.id}, code='{self.account_code}', name='{self.account_name}')>"
    
    @property
    def full_account_name(self) -> str:
        """Get full account name with code"""
        return f"{self.account_code} - {self.account_name}"
    
    @property
    def is_asset_account(self) -> bool:
        """Check if account is an asset account"""
        return self.account_type == AccountType.ASSET
    
    @property
    def is_liability_account(self) -> bool:
        """Check if account is a liability account"""
        return self.account_type == AccountType.LIABILITY
    
    @property
    def is_equity_account(self) -> bool:
        """Check if account is an equity account"""
        return self.account_type == AccountType.EQUITY
    
    @property
    def is_revenue_account(self) -> bool:
        """Check if account is a revenue account"""
        return self.account_type == AccountType.REVENUE
    
    @property
    def is_expense_account(self) -> bool:
        """Check if account is an expense account"""
        return self.account_type == AccountType.EXPENSE
    
    @property
    def is_balance_sheet_account(self) -> bool:
        """Check if account appears on balance sheet"""
        return self.account_type in [AccountType.ASSET, AccountType.LIABILITY, AccountType.EQUITY]
    
    @property
    def is_income_statement_account(self) -> bool:
        """Check if account appears on income statement"""
        return self.account_type in [AccountType.REVENUE, AccountType.EXPENSE, AccountType.OTHER_INCOME, AccountType.OTHER_EXPENSE]
    
    def update_balance(self, amount: Decimal, is_debit: bool) -> None:
        """Update account balance based on journal entry"""
        if self.normal_balance == "debit":
            if is_debit:
                self.current_balance += amount
            else:
                self.current_balance -= amount
        else:  # credit normal balance
            if is_debit:
                self.current_balance -= amount
            else:
                self.current_balance += amount


class JournalEntry(Base):
    """
    Journal entry header
    """
    __tablename__ = "journal_entries"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Journal entry identification
    entry_number = Column(String(50), nullable=False, unique=True, index=True)
    reference_number = Column(String(100))
    
    # Entry classification
    journal_type = Column(Enum(JournalType), nullable=False, default=JournalType.GENERAL)
    status = Column(Enum(JournalStatus), nullable=False, default=JournalStatus.DRAFT)
    
    # Entry dates
    entry_date = Column(DateTime, nullable=False)
    posting_date = Column(DateTime)
    period = Column(String(7), nullable=False)  # YYYY-MM format
    
    # Entry description
    description = Column(Text, nullable=False)
    memo = Column(Text)
    
    # Source document reference
    source_type = Column(String(50))  # "invoice", "payment", "adjustment", etc.
    source_id = Column(UUID(as_uuid=True))
    source_number = Column(String(100))
    
    # Entry totals
    total_debit = Column(Numeric(15, 2), nullable=False, default=0)
    total_credit = Column(Numeric(15, 2), nullable=False, default=0)
    
    # User tracking
    created_by_user = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    posted_by_user = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    
    # Approval workflow (for significant entries)
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approved_at = Column(DateTime)
    
    # Reversal tracking
    is_reversing_entry = Column(Boolean, default=False)
    reversed_entry_id = Column(UUID(as_uuid=True), ForeignKey('journal_entries.id'))
    reversal_reason = Column(Text)
    
    # Period closing
    is_closing_entry = Column(Boolean, default=False)
    is_adjusting_entry = Column(Boolean, default=False)
    fiscal_year = Column(Integer)
    
    # Greek accounting compliance
    greek_book_reference = Column(String(100))  # Greek book keeping reference
    supports_greek_reports = Column(Boolean, default=True)
    
    # Custom fields
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_user])
    posted_by = relationship("User", foreign_keys=[posted_by_user])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    reversed_entry = relationship("JournalEntry", remote_side=[id], foreign_keys=[reversed_entry_id])
    journal_lines = relationship("JournalEntryLine", back_populates="journal_entry", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_journal_company', 'company_id'),
        Index('idx_journal_number', 'entry_number'),
        Index('idx_journal_type', 'journal_type'),
        Index('idx_journal_status', 'status'),
        Index('idx_journal_date', 'entry_date'),
        Index('idx_journal_period', 'period'),
        Index('idx_journal_created_by', 'created_by_user'),
        Index('idx_journal_source', 'source_type', 'source_id'),
        Index('idx_journal_fiscal_year', 'fiscal_year'),
    )
    
    def __repr__(self):
        return f"<JournalEntry(id={self.id}, number='{self.entry_number}', date='{self.entry_date}')>"
    
    @property
    def is_balanced(self) -> bool:
        """Check if journal entry is balanced (debits = credits)"""
        return abs(self.total_debit - self.total_credit) < Decimal('0.01')
    
    @property
    def is_posted(self) -> bool:
        """Check if entry is posted"""
        return self.status == JournalStatus.POSTED
    
    @property
    def can_be_posted(self) -> bool:
        """Check if entry can be posted"""
        return (
            self.status == JournalStatus.DRAFT and
            self.is_balanced and
            len(self.journal_lines) >= 2  # Minimum 2 lines
        )
    
    def post_entry(self, posted_by_user_id: str) -> bool:
        """Post the journal entry"""
        if not self.can_be_posted:
            return False
        
        self.status = JournalStatus.POSTED
        self.posting_date = func.now()
        self.posted_by_user = posted_by_user_id
        
        # Update account balances
        for line in self.journal_lines:
            if line.account and line.account.allow_posting:
                line.account.update_balance(line.amount, line.is_debit)
        
        return True
    
    def reverse_entry(self, reversal_reason: str, created_by_user_id: str) -> 'JournalEntry':
        """Create a reversing journal entry"""
        if self.status != JournalStatus.POSTED:
            raise ValueError("Only posted entries can be reversed")
        
        # Create reversing entry
        reversing_entry = JournalEntry(
            company_id=self.company_id,
            entry_number=f"REV-{self.entry_number}",
            journal_type=self.journal_type,
            entry_date=func.now(),
            period=datetime.now().strftime("%Y-%m"),
            description=f"Reversal of {self.entry_number}: {reversal_reason}",
            is_reversing_entry=True,
            reversed_entry_id=self.id,
            reversal_reason=reversal_reason,
            created_by_user=created_by_user_id
        )
        
        # Create reversing lines (flip debits and credits)
        for line in self.journal_lines:
            reversing_line = JournalEntryLine(
                journal_entry=reversing_entry,
                account_id=line.account_id,
                description=f"Reversal: {line.description}",
                amount=line.amount,
                is_debit=not line.is_debit,  # Flip debit/credit
                reference_number=line.reference_number
            )
        
        # Calculate totals
        reversing_entry.calculate_totals()
        
        # Mark original entry as reversed
        self.status = JournalStatus.REVERSED
        
        return reversing_entry
    
    def calculate_totals(self) -> None:
        """Calculate entry totals from lines"""
        self.total_debit = sum(line.amount for line in self.journal_lines if line.is_debit)
        self.total_credit = sum(line.amount for line in self.journal_lines if not line.is_debit)


class JournalEntryLine(Base):
    """
    Journal entry line items
    """
    __tablename__ = "journal_entry_lines"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Journal entry association
    journal_entry_id = Column(UUID(as_uuid=True), ForeignKey('journal_entries.id'), nullable=False, index=True)
    
    # Account information
    account_id = Column(UUID(as_uuid=True), ForeignKey('chart_of_accounts.id'), nullable=False, index=True)
    
    # Line details
    line_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    reference_number = Column(String(100))
    
    # Amount and type
    amount = Column(Numeric(15, 2), nullable=False)
    is_debit = Column(Boolean, nullable=False)
    
    # Additional references
    business_entity_id = Column(UUID(as_uuid=True), ForeignKey('business_entities.id'), index=True)
    project_id = Column(UUID(as_uuid=True))  # Project reference
    cost_center = Column(String(100))
    department = Column(String(100))
    
    # VAT information
    vat_code = Column(String(20))
    vat_rate = Column(Numeric(5, 2))
    vat_amount = Column(Numeric(15, 2))
    
    # Currency (for multi-currency)
    currency = Column(String(3), default="EUR")
    exchange_rate = Column(Numeric(10, 6), default=1.0)
    base_amount = Column(Numeric(15, 2))  # Amount in company currency
    
    # Greek specifics
    greek_classification = Column(String(100))  # Greek classification code
    
    # Custom fields
    custom_fields = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    journal_entry = relationship("JournalEntry", back_populates="journal_lines")
    account = relationship("ChartOfAccounts", back_populates="journal_entries")
    business_entity = relationship("BusinessEntity")
    
    # Indexes
    __table_args__ = (
        Index('idx_journal_line_entry', 'journal_entry_id'),
        Index('idx_journal_line_account', 'account_id'),
        Index('idx_journal_line_entity', 'business_entity_id'),
        Index('idx_journal_line_number', 'line_number'),
        Index('idx_journal_line_debit', 'is_debit'),
    )
    
    def __repr__(self):
        return f"<JournalEntryLine(id={self.id}, account='{self.account_id}', amount={self.amount}, debit={self.is_debit})>"
    
    @property
    def debit_amount(self) -> Decimal:
        """Get debit amount (0 if credit)"""
        return self.amount if self.is_debit else Decimal('0.00')
    
    @property
    def credit_amount(self) -> Decimal:
        """Get credit amount (0 if debit)"""
        return self.amount if not self.is_debit else Decimal('0.00')


class AccountingPeriod(Base):
    """
    Accounting periods for financial reporting
    """
    __tablename__ = "accounting_periods"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Period identification
    period_code = Column(String(20), nullable=False, index=True)  # "2024-01", "2024-Q1"
    period_name = Column(String(100), nullable=False)
    period_type = Column(String(20), nullable=False)  # "monthly", "quarterly", "annual"
    
    # Period dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Period status
    is_current = Column(Boolean, default=False)
    is_closed = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    
    # Closing information
    closed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    closed_date = Column(DateTime)
    closing_notes = Column(Text)
    
    # Fiscal year
    fiscal_year = Column(Integer, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    closed_by_user = relationship("User")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'period_code', name='uq_period_company_code'),
        Index('idx_period_company', 'company_id'),
        Index('idx_period_dates', 'start_date', 'end_date'),
        Index('idx_period_fiscal_year', 'fiscal_year'),
        Index('idx_period_status', 'is_current', 'is_closed'),
    ) 