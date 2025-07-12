# Greek ERP/CRM Hybrid Monorepo Setup Script
# Sets up Poetry workspace for all Python services + npm workspaces
# Modern unified dependency management approach

Write-Host "Greek ERP/CRM Hybrid Monorepo Setup Starting..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+ and add to PATH" -ForegroundColor Red
    exit 1
}

# Check if Poetry is available
try {
    $poetryVersion = poetry --version 2>&1
    Write-Host "✓ Poetry found: $poetryVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Poetry not found. Installing Poetry..." -ForegroundColor Yellow
    try {
        pip install poetry
        Write-Host "✓ Poetry installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install Poetry. Please install manually: pip install poetry" -ForegroundColor Red
        exit 1
    }
}

# Check if npm is available
try {
    $npmVersion = npm --version 2>&1
    Write-Host "✓ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ npm not found. Please install Node.js 18+ and add to PATH" -ForegroundColor Red
    exit 1
}

# Get project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host ""
Write-Host "Setting up hybrid monorepo architecture..." -ForegroundColor Yellow
Write-Host "✓ npm workspaces for JavaScript/TypeScript" -ForegroundColor Gray
Write-Host "✓ Poetry workspace for Python services" -ForegroundColor Gray

# Verify pyproject.toml exists
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "✗ pyproject.toml not found. Poetry workspace not configured." -ForegroundColor Red
    exit 1
}

# Install JavaScript dependencies (npm workspaces)
Write-Host ""
Write-Host "1. Installing JavaScript dependencies (npm workspaces)..." -ForegroundColor Blue
try {
    npm run install:js
    Write-Host "✓ JavaScript dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install JavaScript dependencies" -ForegroundColor Red
    Write-Host "Please run: npm install" -ForegroundColor Yellow
}

# Install Python dependencies (Poetry workspace)
Write-Host ""
Write-Host "2. Installing Python dependencies (Poetry workspace)..." -ForegroundColor Blue
try {
    poetry install --no-root
    Write-Host "✓ Poetry workspace created successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create Poetry workspace" -ForegroundColor Red
    Write-Host "Please run: poetry install --no-root" -ForegroundColor Yellow
}

# Verify Poetry workspace
Write-Host ""
Write-Host "3. Verifying Poetry workspace..." -ForegroundColor Blue
try {
    $poetryEnv = poetry env info --path 2>&1
    Write-Host "✓ Poetry environment: $poetryEnv" -ForegroundColor Green
    
    # Test shared dependencies
    $fastApiVersion = poetry run python -c "import fastapi; print(fastapi.__version__)" 2>&1
    Write-Host "✓ FastAPI: $fastApiVersion" -ForegroundColor Green
    
    $sqlAlchemyVersion = poetry run python -c "import sqlalchemy; print(sqlalchemy.__version__)" 2>&1
    Write-Host "✓ SQLAlchemy: $sqlAlchemyVersion" -ForegroundColor Green
    
} catch {
    Write-Host "✗ Poetry workspace verification failed" -ForegroundColor Red
    Write-Host "Run 'poetry env info' to debug" -ForegroundColor Yellow
}

# Verify service structure
Write-Host ""
Write-Host "4. Verifying service structure..." -ForegroundColor Blue

$services = @(
    @{Path = "services\api"; Name = "API Service"; Port = 8000},
    @{Path = "services\auth"; Name = "Auth Service"; Port = 8001},
    @{Path = "services\files"; Name = "Files Service"; Port = 8002},
    @{Path = "services\integrations"; Name = "Integrations Service"; Port = 8003},
    @{Path = "packages\ai-services\ai-support-service"; Name = "AI Support Service"; Port = 8004},
    @{Path = "packages\ai-services\voice-service"; Name = "Voice AI Service"; Port = 8005}
)

$missingServices = @()

foreach ($service in $services) {
    $servicePath = $service.Path
    $serviceName = $service.Name
    
    if (Test-Path $servicePath) {
        Write-Host "✓ $serviceName ($servicePath)" -ForegroundColor Green
        
        # Check for pyproject.toml
        $pyprojectPath = "$servicePath\pyproject.toml"
        if (Test-Path $pyprojectPath) {
            Write-Host "  ✓ pyproject.toml found" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ pyproject.toml missing (service-specific deps not configured)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ $serviceName ($servicePath) - directory missing" -ForegroundColor Red
        $missingServices += $serviceName
    }
}

# Summary
Write-Host ""
Write-Host "Hybrid Monorepo Setup Summary:" -ForegroundColor Blue
Write-Host "==============================" -ForegroundColor Blue

$foundServices = $services.Count - $missingServices.Count
Write-Host "npm workspaces: JavaScript/TypeScript ecosystem" -ForegroundColor Green
Write-Host "Poetry workspace: Python services ($foundServices/$($services.Count) services found)" -ForegroundColor Green

if ($missingServices.Count -gt 0) {
    Write-Host "⚠ Missing services:" -ForegroundColor Yellow
    foreach ($missing in $missingServices) {
        Write-Host "  - $missing" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Missing services will be skipped but won't prevent development." -ForegroundColor Gray
} else {
    Write-Host "All services found and configured!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Development Commands:" -ForegroundColor Blue
Write-Host "===================" -ForegroundColor Blue
Write-Host "npm run dev:all           # Start all services (frontend + backend)" -ForegroundColor Gray
Write-Host "npm run dev:js            # Start frontend applications" -ForegroundColor Gray  
Write-Host "npm run dev:python        # Start backend services" -ForegroundColor Gray
Write-Host "npm run dev:api           # Start individual API service" -ForegroundColor Gray
Write-Host "npm run test              # Run all tests (JS + Python)" -ForegroundColor Gray
Write-Host "npm run format            # Format all code (JS + Python)" -ForegroundColor Gray
Write-Host "npm run lint              # Lint all code (JS + Python)" -ForegroundColor Gray

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Blue
Write-Host "1. Run setup-database-windows.ps1 to set up PostgreSQL" -ForegroundColor Gray
Write-Host "2. Configure .env files (shared and service-specific)" -ForegroundColor Gray
Write-Host "3. Run 'poetry run python create-superuser.py' to create admin user" -ForegroundColor Gray
Write-Host "4. Start development with 'npm run dev:all'" -ForegroundColor Gray
Write-Host ""
Write-Host "For detailed workflow, see DEVELOPER-WORKFLOW.md" -ForegroundColor Gray
Write-Host "For setup instructions, see README-SETUP.md" -ForegroundColor Gray 