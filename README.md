# SkillSetu 2.0

SkillSetu 2.0 is a role-based skill-to-career platform for students, employers, colleges, employees, and admins. This repository is being bootstrapped into a production-oriented FastAPI + SQLAlchemy foundation with PostgreSQL-ready configuration and secure authentication.

## Current status

- Repository was inspected and found to be effectively empty aside from the MIT license and a minimal README.
- The repository is now being initialized with the foundation required for the build-out: database models, authentication, RBAC, and protected admin APIs.
- The implementation focuses first on the required backend foundation and is designed to scale toward the full platform.

## Tech stack

- Backend: FastAPI
- Database: PostgreSQL-ready SQLAlchemy models with SQLite fallback for local development/tests
- Auth: JWT + password hashing
- Migrations: Alembic scaffolding
- Testing: pytest

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## API documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Core authentication flows

- Student register: `POST /api/v1/auth/register`
- Student login: `POST /api/v1/auth/login`
- Admin login: `POST /api/v1/auth/admin/login`
- Restricted admin dashboard: `GET /api/v1/admin/dashboard`

## Notes

This repository intentionally begins with the authentication and database foundation required before moving into the public website, student portal, company portal, college portal, employee portal, and admin portal modules.
