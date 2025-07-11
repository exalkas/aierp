# 🚀 Greek ERP/CRM Monorepo

A comprehensive Enterprise Resource Planning and Customer Relationship Management system specifically designed for Greek businesses, built with modern technologies and AI integration.

## 🏗️ Project Structure

```
greek-erp-crm/
├── apps/                      # Applications
│   ├── client/               # Main business app (ERP/CRM)
│   ├── admin/                # Admin interface
│   ├── user-support/         # Customer support portal
│   ├── staff-support/        # Staff support management
│   └── setup/                # Onboarding wizard
├── packages/                  # Shared packages
│   ├── shared/               # Common utilities
│   │   ├── auth/            # Authentication system
│   │   ├── ui/              # UI components library
│   │   └── ...
│   ├── standard-modules/     # Standard SaaS modules
│   │   ├── dashboard/       # Dashboard components
│   │   ├── crm/            # CRM modules
│   │   └── ...
│   ├── ai-services/         # AI Infrastructure
│   │   ├── voice-service/   # Greek voice commands
│   │   ├── ai-support-service/  # AI business assistant
│   │   └── shared-ai/       # Shared AI utilities
│   └── custom-modules/      # Enterprise custom modules
│       ├── pet-management/  # Pet shop modules
│       └── ...
└── services/                # Backend services
    ├── api/                 # FastAPI backend
    ├── auth/                # Authentication service
    ├── files/               # File storage service
    └── integrations/        # Third-party integrations
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (for AI services)
- NVIDIA GPU (for AI voice commands)

### Installation

1. **Install dependencies**

   ```bash
   npm install
   ```

2. **Start development servers**

   ```bash
   # Start all applications
   npm run dev

   # Or start individual applications
   npm run dev:client         # Main business app (port 3000)
   npm run dev:admin          # Admin interface (port 3001)
   npm run dev:user-support   # Customer support (port 3002)
   npm run dev:staff-support  # Staff support (port 3003)
   npm run dev:setup          # Setup wizard (port 3004)
   ```

3. **Start AI services** (requires GPU)

   ```bash
   docker-compose -f docker-compose.ai-services.yml up -d
   ```

## 🎯 Applications

### 📊 Client App (Port 3000)

- Main business application
- ERP and CRM functionality
- Greek business compliance (AADE, VAT, etc.)
- Voice commands integration

### 👤 Admin App (Port 3001)

- System administration
- User management
- Multi-tenant configuration
- Analytics and monitoring

### 💬 User Support App (Port 3002)

- Customer-facing support portal
- AI-powered chat assistant
- Knowledge base and self-service
- Ticket submission

### 🛠️ Staff Support App (Port 3003)

- Internal support management
- Ticket management and routing
- Team collaboration tools
- Performance analytics

### ⚙️ Setup App (Port 3004)

- Company onboarding wizard
- Greek business setup and compliance
- AADE integration configuration
- Training and guidance

## 🤖 AI Services

### 🎙️ Voice Service (Port 8002)

- Greek voice command processing
- Whisper-based speech recognition
- Business intent classification
- Real-time voice interactions

### 🧠 AI Support Service (Port 8003)

- Business intelligence and insights
- Predictive analytics
- Greek business context understanding
- Automated support assistance

## 🔧 Development

### Adding a New Package

1. Create the package directory in the appropriate location
2. Add `package.json` with proper dependencies
3. Export functionality through `src/index.ts`
4. Add to the consuming app's dependencies

### Building and Testing

```bash
# Build all packages
npm run build

# Test all packages
npm run test

# Build specific package
npm run build --workspace=packages/shared-auth
```

## 🐳 Docker Support

- **AI Services**: GPU-accelerated containers for voice and AI processing
- **Development**: Full containerized development environment
- **Production**: Scalable deployment with separate databases per company

## 📝 Architecture Features

- **Monorepo**: npm workspaces for unified dependency management
- **Shared Code**: Common packages across all applications
- **AI Integration**: Cutting-edge voice commands and business intelligence
- **Greek Compliance**: Built-in AADE, VAT, and tax compliance
- **Scalable**: Separate database per company architecture
- **Modern Stack**: Next.js 15, React 18, TypeScript 5, Python 3.11

## 🇬🇷 Greek Business Features

- **AADE Integration**: MyDATA submission and compliance
- **VAT Calculations**: Location-aware Greek VAT rates
- **Tax Office Support**: All 13 Greek tax offices
- **Multi-language**: Greek and English support
- **Business Types**: SA, EPE, OE, EE compliance

## 🚀 Next Steps

1. **Complete Package Implementation**: Add remaining shared packages
2. **AI Services Setup**: Configure Whisper models and GPU acceleration
3. **Database Architecture**: Implement separate database per company
4. **Greek Compliance**: Add AADE integration and validation
5. **Testing**: Comprehensive test suite for all packages

---

**Built with ❤️ for Greek businesses**
