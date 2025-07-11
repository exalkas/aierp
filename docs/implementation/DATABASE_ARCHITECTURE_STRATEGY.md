# Database Architecture Strategy - Separate DB per Company

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: Define database architecture strategy for Greek ERP/CRM platform
- **Decision**: Separate database per company with intelligent partitioning

## Executive Summary

Our **Greek ERP/CRM platform** implements a **separate database per company** architecture to eliminate write contention, ensure complete data isolation, and provide unlimited historical data access without fiscal year switching limitations that plagued legacy ERP systems.

**Key Strategy:**

1. 🏢 **Separate Database per Company** - Zero write contention
2. 📊 **Intelligent Partitioning** - Historical data without year switching
3. ⚡ **Smart Resource Pooling** - Cost optimization through shared instances
4. 🔄 **Automated Operations** - Database provisioning, migrations, backups
5. 🇬🇷 **Greek Compliance** - Full historical reporting and AADE integration

---

## 🎯 **Core Architecture Decision**

### **Separate Database per Company**

**Database Naming Convention:**

```
Standard Company: erp_company_12345
Enterprise: erp_company_67890
On-Premises: erp_client_premises
Desktop: local_sqlite_company.db
```

**Why This Approach:**

- ✅ **Zero Write Contention**: No lock conflicts between companies
- ✅ **Complete Data Isolation**: Perfect security and compliance
- ✅ **Performance Isolation**: No "noisy neighbor" problems
- ✅ **Custom Schema Support**: Enterprise clients can modify database schema
- ✅ **Individual Backup/Restore**: Company-specific data management
- ✅ **Greek Compliance**: Easy audit trails for tax authorities

---

## 📊 **Historical Data Strategy (Revolutionary)**

### **Intelligent Partitioning Within Each Company Database**

**The Problem Legacy ERP Systems Had:**

- Users could only access current fiscal year data
- Had to manually switch between "year tables" for historical data
- Reports spanning multiple years were impossible or complex

**Our Solution - Automatic Partitioning:**

```sql
-- Customers: Yearly partitions
CREATE TABLE crm.customers (
    id UUID,
    name VARCHAR(200),
    created_at TIMESTAMP,
    -- other fields
) PARTITION BY RANGE (EXTRACT(YEAR FROM created_at));

-- Invoices: Monthly partitions for high volume
CREATE TABLE erp.invoices (
    id UUID,
    invoice_date DATE,
    total_amount DECIMAL(12,2),
    -- other fields
) PARTITION BY RANGE (invoice_date);

-- Automatic partition creation
CREATE TABLE erp.invoices_2024_01 PARTITION OF erp.invoices
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

**User Experience:**

```sql
-- User queries normally - PostgreSQL handles partitions automatically
SELECT * FROM erp.invoices
WHERE invoice_date BETWEEN '2020-01-01' AND '2025-12-31';

-- PostgreSQL automatically:
-- 1. Identifies relevant partitions (2020-2025)
-- 2. Queries only those partitions
-- 3. Returns unified results
-- 4. User sees ALL historical data seamlessly
```

**Benefits:**

- ✅ **All Historical Data Always Available**
- ✅ **No Manual Year Switching**
- ✅ **Fast Queries via Partition Pruning**
- ✅ **Multi-Year Reports Work Perfectly**
- ✅ **Greek Tax Reports Spanning Decades**

---

## 🏗️ **Smart Resource Pooling Strategy**

### **Cost Optimization Without Compromise**

**Resource Allocation by Company Size:**

```yaml
Small Companies (< 1GB data, < 50 users):
  Infrastructure: Shared PostgreSQL instance
  Resources: 2 vCPU, 8GB RAM, 100GB SSD
  Cost: €50/month shared across 20 companies = €2.5/company
  Performance: Dedicated database, shared instance

Medium Companies (1-10GB data, 50-200 users):
  Infrastructure: Shared PostgreSQL instance
  Resources: 4 vCPU, 16GB RAM, 500GB SSD
  Cost: €150/month shared across 8 companies = €18.75/company
  Performance: Dedicated database, shared instance

Large Companies (10GB+ data, 200+ users):
  Infrastructure: Dedicated PostgreSQL instance
  Resources: 8+ vCPU, 32+ GB RAM, 1TB+ SSD
  Cost: €400+/month per company
  Performance: Completely isolated
```

**Automatic Scaling:**

- Monitor company growth and usage patterns
- Automatically migrate between shared and dedicated instances
- Zero downtime migration process
- Performance-based scaling triggers

---

## 🔄 **Automated Database Operations**

### **Database Lifecycle Management**

**1. Company Onboarding:**

```python
async def provision_new_company_database(company_id: str):
    """Automatically create and configure new company database"""

    # 1. Create database
    db_name = f"erp_company_{company_id}"
    await create_database(db_name)

    # 2. Run all schema migrations
    await run_full_migration_set(db_name)

    # 3. Create partition tables
    await setup_partition_tables(db_name)

    # 4. Seed Greek reference data
    await seed_greek_compliance_data(db_name)

    # 5. Configure backups
    await setup_backup_schedule(db_name)

    # 6. Set up monitoring
    await configure_monitoring(db_name)
```

**2. Migration Management:**

```python
async def migrate_all_company_databases(migration_sql: str):
    """Run migration across all company databases in parallel"""

    companies = await get_all_companies()

    # Execute migrations in parallel batches
    for batch in chunk_companies(companies, batch_size=10):
        tasks = [
            migrate_company_database(company.id, migration_sql)
            for company in batch
        ]
        await asyncio.gather(*tasks)
```

**3. Automatic Partition Management:**

```python
async def manage_partitions():
    """Automatically create and manage partitions"""

    for company in await get_all_companies():
        # Create future partitions
        await create_future_partitions(company.id)

        # Archive old partitions
        await archive_old_partitions(company.id)

        # Optimize partition indexes
        await optimize_partition_indexes(company.id)
```

---

## 💾 **Comprehensive Backup Strategy**

### **Multi-Level Backup Architecture**

**Backup Levels:**

1. **Continuous WAL Streaming** (every 30 seconds)
2. **Daily Full Backups** (3 AM local time)
3. **Weekly Cross-Region Backups**
4. **Monthly Long-Term Archives**

**Storage Strategy:**

```yaml
Hot Backups (last 7 days):
  Location: Local SSD storage
  Access: Instant restore capability
  Retention: 7 days

Warm Backups (last 30 days):
  Location: Regional cloud storage
  Access: < 1 hour restore
  Retention: 30 days

Cold Backups (1+ years):
  Location: Glacier/Archive storage
  Access: < 24 hours restore
  Retention: 5+ years (Greek legal requirement)
```

**Company-Specific Backup Automation:**

```python
async def backup_company_database(company_id: str):
    """Individual company backup with encryption"""

    db_name = f"erp_company_{company_id}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Create backup
    backup_file = f"{db_name}_{timestamp}.sql"
    await run_pg_dump(db_name, backup_file)

    # 2. Encrypt with company-specific key
    encrypted_file = await encrypt_backup(backup_file, company_id)

    # 3. Upload to multiple locations
    await asyncio.gather(
        upload_to_primary_storage(encrypted_file),
        upload_to_secondary_region(encrypted_file),
        upload_to_archive_storage(encrypted_file)
    )

    # 4. Verify backup integrity
    await verify_backup_integrity(encrypted_file)
```

---

## 🇬🇷 **Greek Compliance & Historical Reporting**

### **Multi-Year Greek Tax Reports**

**Historical AADE Reporting:**

```sql
-- Greek tax reports spanning multiple years
SELECT
    EXTRACT(YEAR FROM invoice_date) as tax_year,
    SUM(total_amount) as annual_revenue,
    SUM(vat_amount) as annual_vat,
    COUNT(*) as total_invoices
FROM erp.invoices
WHERE invoice_date >= '2020-01-01'
    AND invoice_date <= '2024-12-31'
GROUP BY EXTRACT(YEAR FROM invoice_date)
ORDER BY tax_year;

-- PostgreSQL automatically queries all relevant partitions
-- Returns complete historical data for tax authorities
```

**AADE Integration with Historical Context:**

```python
async def generate_aade_annual_report(company_id: str, year: int):
    """Generate comprehensive AADE report with historical context"""

    db = await get_company_database(company_id)

    # Query automatically uses partition pruning
    annual_data = await db.execute("""
        SELECT
            invoice_month,
            total_revenue,
            total_vat,
            aade_submissions
        FROM erp.invoices
        WHERE EXTRACT(YEAR FROM invoice_date) = $1
        ORDER BY invoice_month
    """, year)

    return annual_data
```

---

## 🚀 **Deployment Models**

### **Flexible Deployment Options**

**1. Cloud SAAS (Standard):**

```yaml
Basic/Professional Customers:
  Database: Shared PostgreSQL instance
  Partitioning: Yearly for customers, monthly for transactions
  Backup: Automated daily with 30-day retention
  Monitoring: Shared monitoring with company-specific alerts

Enterprise Customers:
  Database: Dedicated PostgreSQL instance
  Partitioning: Monthly for all high-volume tables
  Backup: Custom backup schedules with extended retention
  Monitoring: Dedicated monitoring and alerting
```

**2. On-Premises Deployment:**

```yaml
Enterprise On-Premises:
  Database: Full PostgreSQL installation at client site
  Partitioning: Same strategy as cloud
  Backup: Local backup with optional cloud sync
  Compliance: Complete data sovereignty
  Support: Remote monitoring and support
```

**3. Desktop Application:**

```yaml
Desktop Users:
  Database: Local SQLite with company-specific file
  Partitioning: File-based partitioning strategy
  Backup: Local backup with cloud sync option
  Sync: Optional synchronization with cloud database
```

---

## 📈 **Performance Benefits**

### **Massive Performance Improvements**

**Write Performance:**

- **No Lock Contention**: Companies can't interfere with each other
- **Parallel Writes**: All companies write simultaneously without conflicts
- **Index Efficiency**: Smaller indexes per company database

**Read Performance:**

- **Partition Pruning**: Queries only scan relevant time periods
- **Company-Specific Optimization**: Indexes optimized per company usage
- **Cache Efficiency**: Better cache hit ratios with smaller datasets

**Historical Data Performance:**

```sql
-- Query spanning 5 years of invoices
-- Legacy ERP: Manual year switching, multiple queries
-- Our System: Single query, automatic partition pruning

SELECT customer_name, SUM(total_amount)
FROM erp.invoices i
JOIN crm.customers c ON i.customer_id = c.id
WHERE i.invoice_date >= '2020-01-01'
    AND i.invoice_date <= '2024-12-31'
GROUP BY customer_name
ORDER BY SUM(total_amount) DESC;

-- PostgreSQL automatically:
-- 1. Identifies relevant partitions (2020-2024)
-- 2. Scans only those partitions
-- 3. Returns complete 5-year summary
-- Query time: <2 seconds for millions of records
```

---

## 💰 **Cost Analysis**

### **Smart Resource Allocation Savings**

**Traditional Approach (Dedicated DB per company):**

```
100 companies × €400/month = €40,000/month
Total Annual Cost: €480,000
```

**Our Smart Approach:**

```
60 small companies × €2.5 = €150/month
30 medium companies × €18.75 = €562.5/month
10 large companies × €400 = €4,000/month
Infrastructure automation: €2,000/month
Analytics warehouse: €1,500/month
Backup infrastructure: €1,000/month

Total Monthly Cost: €9,212.5
Total Annual Cost: €110,550

Annual Savings: €369,450 (77% cost reduction!)
```

---

## 🔧 **Implementation Timeline**

### **Phased Implementation Approach**

**Phase 1: Foundation (Months 1-2)**

- Set up automated database provisioning
- Implement partition management automation
- Configure backup orchestration
- Basic monitoring and alerting

**Phase 2: Migration (Months 2-3)**

- Migrate existing data to partitioned structure
- Implement automated migration system
- Set up cross-company analytics warehouse
- Advanced monitoring and optimization

**Phase 3: Advanced Features (Months 3-4)**

- Implement auto-scaling between shared/dedicated instances
- Advanced partition management and archiving
- Complete backup verification and testing
- Performance optimization and tuning

---

## 🎯 **Success Metrics**

**Performance KPIs:**

- Query Response Time: <200ms for simple, <2s for complex
- Write Contention: 0% (impossible with separate databases)
- Historical Data Access: 100% availability without year switching
- Backup Success Rate: >99.9%

**Business KPIs:**

- Cost Reduction: 75%+ compared to traditional approach
- Customer Satisfaction: No performance complaints
- Greek Compliance: 100% successful tax authority audits
- Historical Reporting: Multi-year reports in <5 seconds

---

## 🏆 **Competitive Advantage**

**Our Architecture vs. Legacy ERP Systems:**

- **Historical Data**: ALL years accessible vs. manual year switching
- **Performance**: Zero write contention vs. shared database bottlenecks
- **Compliance**: Per-company isolation vs. shared table risks
- **Scalability**: Automatic scaling vs. manual resource allocation
- **Backup**: Company-specific restore vs. full system restore only

**Result:** Most advanced database architecture in Greek ERP market with unlimited historical data access and perfect performance isolation.

---

**Status**: Database Architecture Strategy Complete ✅  
**Investment**: €500K development + €110K annual infrastructure  
**Savings**: €369K annually in infrastructure costs  
**Timeline**: 4 months for full implementation
