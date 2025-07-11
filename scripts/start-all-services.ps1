# Greek ERP/CRM - Start All Backend Services
# Starts all services simultaneously in separate PowerShell windows

Write-Host "Starting Greek ERP/CRM Backend Services..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Get project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Service definitions
$services = @(
    @{
        Name = "API Service"
        Path = "services\api"
        Port = 8000
        Command = "uvicorn main:app --reload --port 8000"
        Color = "Blue"
    },
    @{
        Name = "Auth Service" 
        Path = "services\auth"
        Port = 8001
        Command = "uvicorn main:app --reload --port 8001"
        Color = "Green"
    },
    @{
        Name = "Files Service"
        Path = "services\files" 
        Port = 8002
        Command = "uvicorn main:app --reload --port 8002"
        Color = "Yellow"
    },
    @{
        Name = "Integrations Service"
        Path = "services\integrations"
        Port = 8003
        Command = "uvicorn main:app --reload --port 8003"
        Color = "Cyan"
    },
    @{
        Name = "Voice AI Service"
        Path = "packages\ai-services\voice-service"
        Port = 8004
        Command = "uvicorn main:app --reload --port 8004"
        Color = "Magenta"
    },
    @{
        Name = "AI Support Service"
        Path = "packages\ai-services\ai-support-service"
        Port = 8005
        Command = "uvicorn main:app --reload --port 8005"
        Color = "Red"
    }
)

# Function to check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

# Start each service
foreach ($service in $services) {
    if (Test-Path $service.Path) {
        # Check if port is already in use
        if (Test-Port $service.Port) {
            Write-Host "Port $($service.Port) is already in use - skipping $($service.Name)" -ForegroundColor Yellow
            continue
        }

        Write-Host "Starting $($service.Name) on port $($service.Port)..." -ForegroundColor $service.Color
        
        # Create the command to run in new PowerShell window
        $fullPath = Join-Path $ProjectRoot $service.Path
        $activateCommand = "& '$fullPath\venv\Scripts\Activate.ps1'"
        $startCommand = $service.Command
        
        $scriptBlock = @"
Set-Location '$fullPath'
$activateCommand
Write-Host '$($service.Name) starting...' -ForegroundColor $($service.Color)
$startCommand
"@
        
        # Start in new PowerShell window
        Start-Process PowerShell -ArgumentList "-NoExit", "-Command", $scriptBlock
        
        Start-Sleep -Milliseconds 500  # Small delay between starts
    } else {
        Write-Host "$($service.Name) directory not found: $($service.Path)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "All available services started!" -ForegroundColor Green
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor Blue
Write-Host "  API Service:        http://localhost:8000" 
Write-Host "  Auth Service:       http://localhost:8001"
Write-Host "  Files Service:      http://localhost:8002"
Write-Host "  Integrations:       http://localhost:8003"
Write-Host "  Voice AI:           http://localhost:8004"
Write-Host "  AI Support:         http://localhost:8005"
Write-Host ""
Write-Host "API Documentation:   http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop all services, close the PowerShell windows or press Ctrl+C in each" -ForegroundColor Yellow 