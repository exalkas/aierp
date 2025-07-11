#!/bin/bash

# Greek ERP/CRM Backend Setup Script
# Sets up virtual environments for all Python services

set -e  # Exit on any error

echo "🏛️  Setting up Greek ERP/CRM Backend Services..."
echo "================================================"

# Function to create virtual environment and install dependencies
setup_service() {
    local service_path=$1
    local service_name=$2
    
    echo "📦 Setting up $service_name..."
    
    cd "$service_path"
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "  Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "  Installing dependencies..."
        pip install -r requirements.txt
    fi
    
    echo "  ✅ $service_name setup complete"
    
    # Deactivate virtual environment
    deactivate
    
    cd - > /dev/null
}

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📁 Project root: $PROJECT_ROOT"

# Setup API Service
if [ -d "services/api" ]; then
    setup_service "services/api" "API Service"
else
    echo "⚠️  API service directory not found"
fi

# Setup Auth Service
if [ -d "services/auth" ]; then
    setup_service "services/auth" "Auth Service"
else
    echo "⚠️  Auth service directory not found"
fi

# Setup Files Service
if [ -d "services/files" ]; then
    setup_service "services/files" "Files Service"
else
    echo "⚠️  Files service directory not found"
fi

# Setup Integrations Service
if [ -d "services/integrations" ]; then
    setup_service "services/integrations" "Integrations Service"
else
    echo "⚠️  Integrations service directory not found"
fi

# Setup AI Services
if [ -d "packages/ai-services/voice-service" ]; then
    setup_service "packages/ai-services/voice-service" "Voice AI Service"
else
    echo "⚠️  Voice AI service directory not found"
fi

if [ -d "packages/ai-services/ai-support-service" ]; then
    setup_service "packages/ai-services/ai-support-service" "AI Support Service"
else
    echo "⚠️  AI Support service directory not found"
fi

echo ""
echo "🎉 Backend setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Copy .env.example to .env in each service"
echo "   2. Configure database connections"
echo "   3. Run database migrations"
echo "   4. Start the services"
echo ""
echo "🚀 To start API service:"
echo "   cd services/api"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload"
echo "" 