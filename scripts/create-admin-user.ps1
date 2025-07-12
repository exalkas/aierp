# Greek ERP/CRM Admin User Creation
# Creates company and admin user account

Write-Host "Greek ERP/CRM Admin User Creation" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if virtual environment exists
$VENV_PATH = "services\api\venv\Scripts\Activate.ps1"
if (-not (Test-Path $VENV_PATH)) {
    Write-Host "Virtual environment not found. Please run scripts\setup-backend.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if superuser script exists
$SUPERUSER_SCRIPT = "create-superuser-simple.py"
if (-not (Test-Path $SUPERUSER_SCRIPT)) {
    Write-Host "Superuser script not found: $SUPERUSER_SCRIPT" -ForegroundColor Red
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Blue
try {
    # Activate virtual environment and run superuser creation
    & $VENV_PATH
    
    Write-Host "Starting company and user creation..." -ForegroundColor Blue
    Write-Host ""
    Write-Host "You will be prompted to enter:" -ForegroundColor Yellow
    Write-Host "1. Company information (name, AFM, address, etc.)" -ForegroundColor Gray
    Write-Host "2. Admin user details (username, email, password)" -ForegroundColor Gray
    Write-Host ""
    
    # Run the superuser creation script
    python $SUPERUSER_SCRIPT
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS! Company and admin user created!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next step: scripts\start-all-services.ps1" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Then visit: http://localhost:8000/docs" -ForegroundColor Cyan
    } else {
        throw "User creation failed"
    }
} catch {
    Write-Host "Failed to create admin user: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} 