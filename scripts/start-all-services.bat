@echo off
REM Greek ERP/CRM - Start All Backend Services (Batch Version)
echo Starting Greek ERP/CRM Backend Services...
echo =========================================

REM Get script directory and project root
cd /d "%~dp0.."

REM Start API Service (Port 8000)
if exist "services\api\venv" (
    echo Starting API Service on port 8000...
    start "API Service" cmd /k "cd /d services\api && venv\Scripts\activate && uvicorn main:app --reload --port 8000"
    timeout /t 1 /nobreak >nul
) else (
    echo API Service venv not found - run setup first
)

REM Start Auth Service (Port 8001)
if exist "services\auth\venv" (
    echo Starting Auth Service on port 8001...
    start "Auth Service" cmd /k "cd /d services\auth && venv\Scripts\activate && uvicorn main:app --reload --port 8001"
    timeout /t 1 /nobreak >nul
) else (
    echo Auth Service venv not found - run setup first
)

REM Start Files Service (Port 8002)
if exist "services\files\venv" (
    echo Starting Files Service on port 8002...
    start "Files Service" cmd /k "cd /d services\files && venv\Scripts\activate && uvicorn main:app --reload --port 8002"
    timeout /t 1 /nobreak >nul
) else (
    echo Files Service venv not found - run setup first
)

REM Start Integrations Service (Port 8003)
if exist "services\integrations\venv" (
    echo Starting Integrations Service on port 8003...
    start "Integrations Service" cmd /k "cd /d services\integrations && venv\Scripts\activate && uvicorn main:app --reload --port 8003"
    timeout /t 1 /nobreak >nul
) else (
    echo Integrations Service venv not found - run setup first
)

REM Start Voice AI Service (Port 8004)
if exist "packages\ai-services\voice-service\venv" (
    echo Starting Voice AI Service on port 8004...
    start "Voice AI Service" cmd /k "cd /d packages\ai-services\voice-service && venv\Scripts\activate && uvicorn main:app --reload --port 8004"
    timeout /t 1 /nobreak >nul
) else (
    echo Voice AI Service venv not found - run setup first
)

REM Start AI Support Service (Port 8005)
if exist "packages\ai-services\ai-support-service\venv" (
    echo Starting AI Support Service on port 8005...
    start "AI Support Service" cmd /k "cd /d packages\ai-services\ai-support-service && venv\Scripts\activate && uvicorn main:app --reload --port 8005"
    timeout /t 1 /nobreak >nul
) else (
    echo AI Support Service venv not found - run setup first
)

echo.
echo All available services started!
echo.
echo Service URLs:
echo   API Service:        http://localhost:8000
echo   Auth Service:       http://localhost:8001  
echo   Files Service:      http://localhost:8002
echo   Integrations:       http://localhost:8003
echo   Voice AI:           http://localhost:8004
echo   AI Support:         http://localhost:8005
echo.
echo API Documentation:   http://localhost:8000/api/docs
echo.
echo To stop services, close the command prompt windows
pause 