# Greek ERP/CRM Environment Setup Script
# Copies .env files to each service directory

Write-Host "Setting up environment files..." -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

# Get project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Source environment file
$EnvSource = "scripts\env.example"

if (-not (Test-Path $EnvSource)) {
    Write-Host "Error: env.example not found in scripts directory" -ForegroundColor Red
    exit 1
}

# Service directories that need .env files
$servicePaths = @(
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

for ($i = 0; $i -lt $servicePaths.Length; $i++) {
    $servicePath = $servicePaths[$i]
    $serviceName = $serviceNames[$i]
    $envTarget = Join-Path $servicePath ".env"
    
    if (Test-Path $servicePath) {
        if (Test-Path $envTarget) {
            $choice = Read-Host "$serviceName already has .env file. Overwrite? (y/N)"
            if ($choice -ne 'y' -and $choice -ne 'Y') {
                Write-Host "  Skipped $serviceName" -ForegroundColor Yellow
                continue
            }
        }
        
        Copy-Item $EnvSource $envTarget
        Write-Host "  Created .env for $serviceName" -ForegroundColor Green
    } else {
        Write-Host "  $serviceName directory not found: $servicePath" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Blue
Write-Host "  1. Edit .env files in each service directory"
Write-Host "  2. Configure your database connection"
Write-Host "  3. Set your secret keys"
Write-Host "  4. Configure AADE credentials (if needed)"
Write-Host ""
Write-Host "IMPORTANT: Update these values in each .env file:" -ForegroundColor Yellow
Write-Host "  - DATABASE_URL (your PostgreSQL connection)"
Write-Host "  - SECRET_KEY (generate a secure key)"
Write-Host "  - JWT_SECRET_KEY (generate a secure key)"
Write-Host "  - AADE_SUBSCRIPTION_KEY (for Greek tax integration)" 