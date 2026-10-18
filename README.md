# Greek ERP/CRM

A business-management application in development for Greek businesses. It brings customer and supplier records, contacts, CRM workflows, and ERP features together around a shared business-entity model, so one organization can have multiple business roles.

Built with Next.js, React, TypeScript, Python/FastAPI, SQLAlchemy, and PostgreSQL. The repository includes a main client, administration and support applications at different stages of development, shared UI packages, authentication and API services, database utilities, and optional AI/voice service scaffolding.

## Status

The existing code covers customer/supplier interfaces, business entities, shared components, authentication, and database models and migrations. The planning documents describe a broader product; they do not establish that every feature is complete. Tax integrations, optional AI services, and production operation need separate configuration and validation.

## Layout

| Folder | Purpose |
| --- | --- |
| `apps/client/` | Main business application |
| `apps/admin/`, `apps/setup/` | Administration and onboarding |
| `apps/user-support/`, `apps/staff-support/`, `apps/marketing/` | Support and marketing applications |
| `packages/shared/`, `packages/standard-modules/` | Shared UI, authentication, CRM, ERP, and reporting packages |
| `services/api/`, `services/auth/` | Main API and authentication |
| `services/files/`, `services/integrations/` | File and integration service scaffolding |
| `packages/ai-services/` | Optional support and voice services |
| `scripts/`, `docs/` | Database utilities and development documentation |

## Local development

Install Node.js with npm, Python 3.11, Poetry, and PostgreSQL. The root Python environment also includes optional AI/audio dependencies, which can require additional platform-specific libraries.

```sh
npm install
poetry install --no-root
```

Copy `env.example` to the ignored root `.env`. Set `DATABASE_URL`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`, and `JWT_SECRET_KEY` there using your own local database settings. The individual DB fields are used by the PowerShell database utilities; the Python services and administrator utilities use `DATABASE_URL`. Keep these values consistent.

Generate independent signing secrets locally by running this command twice:

```sh
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the configured `.env` into the core service folders that you use: `services/api/`, `services/auth/`, `services/files/`, and `services/integrations/`. Authentication and API services must use the same JWT signing key. The administrator-creation utilities read the root `.env`; set `SUPERUSER_PASSWORD` privately before using them.

Required credentials are read from environment variables; the services have no embedded database password or signing-secret fallback. Root Python utilities load `.env` with `python-dotenv`, and PowerShell database scripts load it with `scripts/load-local-env.ps1`. Existing exported environment variables take precedence. Empty template entries are instructions to supply local configuration, not working credentials.

Review database scripts before using a **new, disposable development database**. Some reset and migration utilities recreate tables or users. Generated data exports are deliberately excluded. The Windows setup utility and its SQL script require PostgreSQL client tools version 15 or newer and a configured `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

Start these in separate terminals from the repository root:

```sh
npm run dev:auth
npm run dev:api
npm run dev:client
```

Authentication normally runs on port 8001, the API on 8000, and the client on 3000. Development API docs are normally at `http://localhost:8000/api/docs` and authentication docs at `http://localhost:8001/docs`.

Optional provider credentials belong only in the ignored local environment. Code should read the corresponding environment variable; never embed provider keys in source or expose them through frontend variables.

## Validation and plans

See [ROADMAP.md](ROADMAP.md) for proposed follow-up work. Existing setup and architecture documents are retained as development references and may describe older configuration or incomplete features.

The publication checks cover secret removal, Python/JSON syntax, settings loading, and setup-script parsing. No Python automated test files were found in the tracked project; full frontend builds, database migrations, and end-to-end business workflows have not been validated in this preparation.

## Credentials and data

Commit source code and safe templates only. Real passwords, signing secrets, tokens, private keys, local environments, database exports, logs, and customer data must remain excluded. Scan both the working files and complete Git history before pushing. Do not merge an old, uncleaned clone into the sanitized repository.

## License

Released under the [MIT License](LICENSE), matching the existing Python metadata. Third-party dependencies retain their own licenses.
