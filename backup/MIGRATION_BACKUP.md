# Poetry Workspace Migration Backup

## Migration Date

Generated on: $(Get-Date)

## Original Python Setup

- **6 separate Python services** with individual virtual environments
- **6 separate requirements.txt files** with overlapping dependencies
- **Manual dependency management** across services

## Services Migrated

1. **services/api/** - Main ERP/CRM API service
2. **services/auth/** - Authentication service
3. **services/files/** - File storage service
4. **services/integrations/** - AADE/Banking integrations
5. **packages/ai-services/ai-support-service/** - AI support service
6. **packages/ai-services/voice-service/** - Voice AI service

## Original Requirements Files

- `services/api/requirements.txt` → 63 dependencies
- `services/auth/requirements.txt` → 32 dependencies
- `services/files/requirements.txt` → 27 dependencies
- `services/integrations/requirements.txt` → 30 dependencies
- `packages/ai-services/ai-support-service/requirements.txt` → 28 dependencies
- `packages/ai-services/voice-service/requirements.txt` → 28 dependencies

## Common Dependencies Identified

- fastapi, uvicorn, pydantic (all services)
- sqlalchemy, asyncpg (3 services)
- PyJWT, bcrypt, cryptography (2-3 services)
- phonenumbers, pytz (Greek business support)
- openai (AI services)

## New Poetry Workspace Structure

- **Root pyproject.toml** - Shared dependencies and workspace configuration
- **6 service-specific pyproject.toml files** - Service-specific dependencies only
- **Single Poetry environment** - Replaces 6 separate venvs

## Rollback Instructions

If needed, you can rollback by:

1. Reactivating individual venvs: `cd services/api && venv\Scripts\activate`
2. Using original requirements.txt: `pip install -r requirements.txt`
3. Original files are preserved in their locations

## Next Steps

1. Install Poetry: `pip install poetry`
2. Install workspace: `poetry install`
3. Test services: `poetry run python services/api/main.py`
4. Update npm scripts to use Poetry commands
