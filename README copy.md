# Smart Electricity Utility Management System

FastAPI + SQLAlchemy + MySQL/PyMySQL + OAuth2 Password Flow + JWT + Alembic.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a MySQL database named `electricity_utility_db`, copy `.env.example` to `.env`, and update the password.

## Run

```powershell
uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

## OAuth2 / Swagger

1. `POST /auth/register`
2. Click `Authorize` in Swagger.
3. Enter the registered email in the username field and the password.
4. Swagger sends the OAuth2 password-form request to `/auth/login`.
5. Use the returned Bearer token for protected endpoints.

## Database

For the assignment, create tables with:

```powershell
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

The project also includes `run.py`.

## Quick OpenAPI verification

```powershell
python verify_swagger.py
```

This verifies that FastAPI can import the application and generate `/openapi.json` without requiring a live database connection.
