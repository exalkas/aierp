# Greek ERP/CRM Database Setup Script for Windows
# Based on actual working setup process

Write-Host "Greek ERP/CRM Database Setup" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

# PostgreSQL 17 path that we know works
$PSQL_PATH = "C:\Program Files\PostgreSQL\17\bin\psql.exe"

# Load credentials
$DB_NAME = "erp_maritime_hellenic_4007"
$DB_USER = "erp_admin_315"
$DB_PASSWORD = ""

Write-Host "Database: $DB_NAME" -ForegroundColor Gray
Write-Host "User: $DB_USER" -ForegroundColor Gray

# Check if PostgreSQL is installed
if (-not (Test-Path $PSQL_PATH)) {
    Write-Host "PostgreSQL 17 not found at expected location." -ForegroundColor Red
    Write-Host "Expected: $PSQL_PATH" -ForegroundColor Gray
    Write-Host "Please install PostgreSQL 17 from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found PostgreSQL: $PSQL_PATH" -ForegroundColor Green

# Get postgres password
Write-Host ""
Write-Host "You will be prompted for the postgres superuser password once:" -ForegroundColor Blue
Write-Host "1. To create database, user, and set permissions" -ForegroundColor Gray
Write-Host ""

# Step 1: Create database, user, and set permissions
Write-Host "Step 1: Creating database, user, and setting permissions..." -ForegroundColor Blue
try {
    & $PSQL_PATH -U postgres -d postgres -f scripts/create-db-user.sql
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database, user, and permissions configured successfully" -ForegroundColor Green
    } else {
        throw "Database setup failed"
    }
} catch {
    Write-Host "Failed to set up database: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 2: Test connection
Write-Host ""
Write-Host "Step 2: Testing connection..." -ForegroundColor Blue
$env:PGPASSWORD = $DB_PASSWORD
try {
    $testResult = & $PSQL_PATH -U $DB_USER -d $DB_NAME -c "SELECT current_user, current_database();" -t
    if ($testResult -match "$DB_USER") {
        Write-Host "Connection test successful!" -ForegroundColor Green
    } else {
        throw "Connection test failed"
    }
} catch {
    Write-Host "Connection test failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    $env:PGPASSWORD = $null
}

Write-Host ""
Write-Host "SUCCESS! Database setup complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "Database: $DB_NAME" -ForegroundColor Gray
Write-Host "User: $DB_USER" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Blue
Write-Host "1. Initialize schema: scripts\init-database-schema.ps1" -ForegroundColor Gray
Write-Host "2. Create admin user: scripts\create-admin-user.ps1" -ForegroundColor Gray
Write-Host "3. Start services: scripts\start-all-services.ps1" -ForegroundColor Gray 