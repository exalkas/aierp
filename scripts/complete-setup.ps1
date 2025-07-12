# Greek ERP/CRM Complete Setup Script
# Runs the entire setup process in the correct order

Write-Host "Greek ERP/CRM Complete Setup" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host ""
Write-Host "This script will set up the complete Greek ERP/CRM system:" -ForegroundColor Blue
Write-Host "1. Backend services setup" -ForegroundColor Gray
Write-Host "2. Database creation" -ForegroundColor Gray
Write-Host "3. Schema initialization" -ForegroundColor Gray
Write-Host "4. Admin user creation" -ForegroundColor Gray
Write-Host "5. Start all services" -ForegroundColor Gray
Write-Host ""

$confirmation = Read-Host "Continue with complete setup? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "Setup cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "STEP 1: Backend Services Setup" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

try {
    powershell -ExecutionPolicy Bypass -File scripts\setup-backend.ps1
    if ($LASTEXITCODE -ne 0) {
        throw "Backend setup failed"
    }
    Write-Host "Backend setup completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Backend setup failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "STEP 2: Database Setup" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

try {
    powershell -ExecutionPolicy Bypass -File scripts\setup-database-windows.ps1
    if ($LASTEXITCODE -ne 0) {
        throw "Database setup failed"
    }
    Write-Host "Database setup completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Database setup failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "STEP 3: Database Schema Initialization" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

try {
    powershell -ExecutionPolicy Bypass -File scripts\init-database-schema.ps1
    if ($LASTEXITCODE -ne 0) {
        throw "Schema initialization failed"
    }
    Write-Host "Schema initialization completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Schema initialization failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "STEP 4: Admin User Creation" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

try {
    powershell -ExecutionPolicy Bypass -File scripts\create-admin-user.ps1
    if ($LASTEXITCODE -ne 0) {
        throw "Admin user creation failed"
    }
    Write-Host "Admin user creation completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Admin user creation failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "STEP 5: Starting All Services" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

try {
    powershell -ExecutionPolicy Bypass -File scripts\start-all-services.ps1
    Write-Host "All services started!" -ForegroundColor Green
} catch {
    Write-Host "Failed to start services: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "You can start them manually later with: scripts\start-all-services.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "COMPLETE SETUP FINISHED!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your Greek ERP/CRM system is now ready!" -ForegroundColor Blue
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit: http://localhost:8000/docs (API Documentation)" -ForegroundColor Cyan
Write-Host "2. Visit: http://localhost:8000/health (Health Check)" -ForegroundColor Cyan
Write-Host "3. Begin Week 1 development tasks" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services running on:" -ForegroundColor Blue
Write-Host "- API Service: http://localhost:8000" -ForegroundColor Gray
Write-Host "- Auth Service: http://localhost:8001" -ForegroundColor Gray
Write-Host "- Files Service: http://localhost:8002" -ForegroundColor Gray
Write-Host "- Integrations: http://localhost:8003" -ForegroundColor Gray
Write-Host "- Voice AI: http://localhost:8004" -ForegroundColor Gray
Write-Host "- AI Support: http://localhost:8005" -ForegroundColor Gray 