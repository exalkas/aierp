# Greek ERP/CRM Hybrid Monorepo Setup Script
# Simple script that uses our working npm commands

Write-Host "Greek ERP/CRM Hybrid Monorepo Setup" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Get project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

try {
    $poetryVersion = poetry --version 2>&1
    Write-Host "Poetry: $poetryVersion" -ForegroundColor Green
} catch {
    Write-Host "Poetry not found. Installing..." -ForegroundColor Yellow
    pip install poetry
}

try {
    $npmVersion = npm --version 2>&1
    Write-Host "npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "npm not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Install dependencies using our working commands
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Blue

Write-Host "1. Installing JavaScript dependencies..." -ForegroundColor Gray
npm run install:js

Write-Host "2. Installing Python dependencies..." -ForegroundColor Gray  
npm run install:python

# Verify setup
Write-Host ""
Write-Host "Verifying setup..." -ForegroundColor Blue

try {
    $poetryEnv = poetry env info --path 2>&1
    Write-Host "Poetry environment: $poetryEnv" -ForegroundColor Green
} catch {
    Write-Host "Poetry environment verification failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Blue
Write-Host "1. Setup database: scripts\setup-database-windows.ps1" -ForegroundColor Gray
Write-Host "2. Create superuser: poetry run python create-superuser.py" -ForegroundColor Gray
Write-Host "3. Start development: npm run dev:all" -ForegroundColor Gray
Write-Host ""
Write-Host "See DEVELOPER-WORKFLOW.md for detailed workflow" -ForegroundColor Gray 