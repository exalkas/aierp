# Proposed follow-up work

The owner should prioritize and confirm these tasks before describing them as planned work in a project submission.

- Validate a fresh installation against an isolated PostgreSQL database and simplify optional AI dependencies in the root development environment.
- Exercise customer, supplier, and contact workflows across the client, API, and authentication service.
- Add automated tests for authentication, company isolation, business-entity roles, and database migrations with synthetic fixtures.
- Review and test Greek tax-validation and integration behavior against sandbox services before relying on it.
- Replace historical setup scripts that expect local credential files or database snapshots with reproducible, safe onboarding steps.
- Validate the TypeScript workspace builds, complete partially implemented modules, and reconcile documentation with the actual implementation.
- Add automated secret scanning and deployment validation before production use.
