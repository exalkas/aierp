# Greek ERP/CRM Backend Setup Script
# Sets up Python virtual environments for all backend services
# Includes dependency fixes and error handling

Write-Host "Greek ERP/CRM Backend Setup Starting..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ and add to PATH" -ForegroundColor Red
    exit 1
}

# Get project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Service paths and names
$services = @(
    @{Path = "services\api"; Name = "API Service"; Port = 8000},
    @{Path = "services\auth"; Name = "Auth Service"; Port = 8001},
    @{Path = "services\files"; Name = "Files Service"; Port = 8002},
    @{Path = "services\integrations"; Name = "Integrations Service"; Port = 8003},
    @{Path = "packages\ai-services\voice-service"; Name = "Voice AI Service"; Port = 8004},
    @{Path = "packages\ai-services\ai-support-service"; Name = "AI Support Service"; Port = 8005}
)

$failedServices = @()

# Process each service
foreach ($service in $services) {
    $servicePath = $service.Path
    $serviceName = $service.Name
    
    Write-Host ""
    Write-Host "Setting up $serviceName..." -ForegroundColor Yellow
    Write-Host "Path: $servicePath" -ForegroundColor Gray
    
    if (-not (Test-Path $servicePath)) {
        Write-Host "✗ Service directory not found: $servicePath" -ForegroundColor Red
        $failedServices += $serviceName
        continue
    }
    
    # Create virtual environment
    $venvPath = "$servicePath\venv"
    if (Test-Path $venvPath) {
        Write-Host "  Virtual environment already exists" -ForegroundColor Yellow
    } else {
        Write-Host "  Creating virtual environment..." -ForegroundColor Blue
        try {
            python -m venv $venvPath
            Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Failed to create virtual environment" -ForegroundColor Red
            $failedServices += $serviceName
            continue
        }
    }
    
    # Install dependencies
    $requirementsPath = "$servicePath\requirements.txt"
    if (Test-Path $requirementsPath) {
        Write-Host "  Installing dependencies..." -ForegroundColor Blue
        try {
            # Upgrade pip first
            & "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
            
            # Install requirements with error handling
            $installResult = & "$venvPath\Scripts\pip.exe" install -r $requirementsPath 2>&1
            
            # Check for specific dependency issues and fix them
            if ($installResult -match "locale.*0\.1\.0") {
                Write-Host "  ⚠ Fixing locale dependency issue..." -ForegroundColor Yellow
                & "$venvPath\Scripts\pip.exe" uninstall -y locale
            }
            
            if ($installResult -match "torch.*2\.1\.1") {
                Write-Host "  ⚠ Fixing torch dependency issue..." -ForegroundColor Yellow
                & "$venvPath\Scripts\pip.exe" install torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu
            }
            
            if ($installResult -match "polyglot.*encoding") {
                Write-Host "  ⚠ Fixing polyglot encoding issue..." -ForegroundColor Yellow
                & "$venvPath\Scripts\pip.exe" uninstall -y polyglot
                & "$venvPath\Scripts\pip.exe" install polyglot --no-deps
            }
            
            # Ensure uvicorn is properly installed
            Write-Host "  Ensuring uvicorn is properly installed..." -ForegroundColor Blue
            & "$venvPath\Scripts\pip.exe" install uvicorn[standard] --force-reinstall
            
            # Install fastapi if missing (for AI services)
            if ($serviceName -match "AI|Voice") {
                Write-Host "  Installing FastAPI for AI service..." -ForegroundColor Blue
                & "$venvPath\Scripts\pip.exe" install fastapi python-multipart
            }
            
            Write-Host "  ✓ Dependencies installed successfully" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Failed to install dependencies: $($_.Exception.Message)" -ForegroundColor Red
            $failedServices += $serviceName
            continue
        }
    } else {
        Write-Host "  ⚠ No requirements.txt found" -ForegroundColor Yellow
    }
    
    # Verify installation
    Write-Host "  Verifying installation..." -ForegroundColor Blue
    try {
        $uvicornCheck = & "$venvPath\Scripts\uvicorn.exe" --version 2>&1
        Write-Host "  ✓ Uvicorn: $uvicornCheck" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Uvicorn verification failed" -ForegroundColor Red
        $failedServices += $serviceName
    }
    
    Write-Host "  ✓ $serviceName setup complete" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "Backend Setup Summary:" -ForegroundColor Blue
Write-Host "=====================" -ForegroundColor Blue

$successCount = $services.Count - $failedServices.Count
Write-Host "✓ Successful: $successCount/$($services.Count) services" -ForegroundColor Green

if ($failedServices.Count -gt 0) {
    Write-Host "✗ Failed services:" -ForegroundColor Red
    foreach ($failed in $failedServices) {
        Write-Host "  - $failed" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please check the errors above and retry setup for failed services." -ForegroundColor Yellow
} else {
    Write-Host "🎉 All services set up successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Blue
Write-Host "1. Run setup-database-windows.ps1 to set up PostgreSQL" -ForegroundColor Gray
Write-Host "2. Configure .env files in each service directory" -ForegroundColor Gray
Write-Host "3. Run create-superuser.py to create admin user" -ForegroundColor Gray
Write-Host "4. Start services with start-all-services.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "For detailed setup instructions, see README-SETUP.md" -ForegroundColor Gray 