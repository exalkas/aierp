# Greek ERP/CRM Backend Setup Script (PowerShell)
# Sets up virtual environments for all Python services

Write-Host "Setting up Greek ERP/CRM Backend Services..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Get the project root directory
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Project root: $ProjectRoot" -ForegroundColor Blue

$services = @(
    "services\api",
    "services\auth", 
    "services\files",
    "services\integrations",
    "packages\ai-services\voice-service",
    "packages\ai-services\ai-support-service"
)

$serviceNames = @(
    "API Service",
    "Auth Service",
    "Files Service", 
    "Integrations Service",
    "Voice AI Service",
    "AI Support Service"
)

for ($i = 0; $i -lt $services.Length; $i++) {
    $servicePath = $services[$i]
    $serviceName = $serviceNames[$i]
    
    if (Test-Path $servicePath) {
        Write-Host "Setting up $serviceName..." -ForegroundColor Yellow
        
        Push-Location $servicePath
        
        try {
            # Create virtual environment
            if (-Not (Test-Path "venv")) {
                Write-Host "  Creating virtual environment..."
                python -m venv venv
            }
            
            # Activate virtual environment and install dependencies
            if (Test-Path "requirements.txt") {
                Write-Host "  Installing dependencies..."
                & "venv\Scripts\python.exe" -m pip install --upgrade pip
                & "venv\Scripts\pip.exe" install -r requirements.txt
            }
            
            Write-Host "  $serviceName setup complete" -ForegroundColor Green
        }
        catch {
            Write-Host "  Error setting up $serviceName : $_" -ForegroundColor Red
        }
        finally {
            Pop-Location
        }
    } else {
        Write-Host "$serviceName directory not found: $servicePath" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Backend setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Blue
Write-Host "   1. Configure environment variables in each service"
Write-Host "   2. Setup PostgreSQL database"
Write-Host "   3. Run database migrations"  
Write-Host "   4. Start the services"
Write-Host ""
Write-Host "To start API service:" -ForegroundColor Blue
Write-Host "   cd services\api"
Write-Host "   venv\Scripts\Activate.ps1"
Write-Host "   uvicorn main:app --reload" 