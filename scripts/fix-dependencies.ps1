# Fix Dependencies Script
# Reinstalls dependencies for services that had package conflicts

Write-Host "Fixing dependencies for affected services..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Get project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Services that had issues
$problemServices = @(
    @{
        Name = "API Service"
        Path = "services\api"
        Issue = "locale package not found"
    },
    @{
        Name = "Voice AI Service"
        Path = "packages\ai-services\voice-service"
        Issue = "torch version conflict"
    },
    @{
        Name = "AI Support Service"
        Path = "packages\ai-services\ai-support-service"
        Issue = "polyglot encoding error"
    }
)

foreach ($service in $problemServices) {
    if (Test-Path $service.Path) {
        Write-Host "Fixing $($service.Name)..." -ForegroundColor Yellow
        Write-Host "  Issue: $($service.Issue)" -ForegroundColor Cyan
        
        Push-Location $service.Path
        
        try {
            if (Test-Path "venv") {
                Write-Host "  Reinstalling dependencies..."
                
                # Install uvicorn first to ensure it's available
                & "venv\Scripts\pip.exe" install uvicorn[standard]==0.24.0
                
                # Then install the rest
                if (Test-Path "requirements.txt") {
                    & "venv\Scripts\pip.exe" install -r requirements.txt
                }
                
                Write-Host "  $($service.Name) dependencies fixed!" -ForegroundColor Green
            } else {
                Write-Host "  Virtual environment not found - run setup-backend.ps1 first" -ForegroundColor Red
            }
        }
        catch {
            Write-Host "  Error fixing $($service.Name): $_" -ForegroundColor Red
        }
        finally {
            Pop-Location
        }
    } else {
        Write-Host "$($service.Name) directory not found: $($service.Path)" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host "Dependency fixes complete!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run:" -ForegroundColor Blue
Write-Host "  .\scripts\start-all-services.ps1" -ForegroundColor Cyan 