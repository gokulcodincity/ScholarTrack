# ScholarTrack

ScholarTrack is a scholarship management system with a FastAPI backend, React frontend, PostgreSQL relational storage, and MongoDB document storage. It supports student applications, reviewer workflows, admin scholarship management, email verification, JWT authentication, role-based access control, reviewer approval, essay submission, review notes, final decisions, and CI checks through Azure DevOps.

## Features

- Student registration, email verification, login, profile management, scholarship browsing, and application submission.
- Reviewer registration flow with reviewer request form and PDF resume upload.
- Reviewer dashboard for assigned applications, essay review, reviewer notes, scores, and review completion.
- Admin dashboard for pending reviewer approvals, active reviewers, users, scholarships, applications, and decisions.
- PostgreSQL storage for users, students, scholarships, applications, decisions, and reviewer requests.
- MongoDB storage for essays and reviewer notes through Beanie ODM.
- JWT authentication with role-based route guards.
- PostgreSQL database auto-creation and SQLAlchemy table creation during backend startup.
- Redis-backed scholarship list cache when Redis is available.
- SlowAPI rate limiting on authentication endpoints.
- Structured JSON logging with `structlog`.
- Global error response handling.
- Health endpoint at `GET /health`.
- Azure DevOps pipeline for formatting, linting, type checking, security scanning, tests, coverage, and packaging.

## Tech Stack

Backend:
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg2
- MongoDB
- Beanie ODM
- PyMongo async Mongo client usage
- JWT with `python-jose`
- bcrypt
- Redis
- SlowAPI
- structlog
- Uvicorn
- Pytest

Frontend:
- React 19
- Vite
- React Router
- Axios
- Tailwind CSS

Infrastructure:
- nginx reverse proxy
- Azure DevOps pipeline
- uv lockfile and Python project config in `pyproject.toml`

## Folder Structure

```text
ScholarTrack/
  backend/
    app/
      config/          # settings, database, MongoDB, Redis, logging, security
      middleware/      # auth, CORS, error handlers, role middleware
      models/          # SQLAlchemy models and Beanie documents
      repositories/    # user and student repositories
      routes/          # FastAPI routers
      schemas/         # Pydantic request/response schemas
      services/        # business logic
      utils/           # enums, constants, helpers, sanitization
      main.py          # FastAPI app startup and router registration
    alembic/           # Alembic files exist, but runtime uses SQLAlchemy create_all
    tests/             # backend tests
    requirements.txt
    seed_admin.py
  frontend/
    src/
      components/
      context/
      pages/
      services/
      App.jsx
      main.jsx
    package.json
    vite.config.js
  nginx/
    nginx.conf
  pipelines/
    azure-pipelines.yml
  setup.sh
  pyproject.toml
  uv.lock
```

## Environment Variables

The backend reads environment variables from `.env` through `python-dotenv`.

Required backend variables:

```env
SECRET_KEY=your_jwt_secret

# Preferred PostgreSQL variables
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=scholartrack

# Optional; defaults to postgres
POSTGRES_MAINTENANCE_DB=postgres

# Compatibility fallback supported by the code
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/scholartrack

MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=scholartrack

# Optional; defaults to redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0
```

Required frontend variable:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The existing root `.env` contains `VITE_API_BASE_URL`, backend secrets, PostgreSQL configuration, and MongoDB configuration. Do not commit real passwords or production secrets.

## Installation Steps

Prerequisites:
- Python 3.10+
- Node.js and npm
- PostgreSQL
- MongoDB
- Redis optional, but recommended for scholarship cache behavior

From the repository root:

```powershell
cd D:\Codincity\ScholarTrack
```

Create and activate a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install backend dependencies. `backend/requirements.txt` now contains the backend runtime packages plus the test packages needed by the repository pytest configuration.

```powershell
pip install -r backend\requirements.txt
```

Developers who prefer uv can also use `uv sync --dev` from the repository root.

Install frontend dependencies:

```powershell
cd frontend
npm install
```

## Setup Steps

1. Create or update `.env` in the repository root with the variables listed above.
2. Start PostgreSQL.
3. Start MongoDB.
4. Start Redis if you want cache support.
5. Start the backend.
6. Optionally seed the default admin user.
7. Start the frontend.

## Database Setup

The current backend startup sequence handles PostgreSQL database and table setup:

1. `ensure_database_exists()` connects to the PostgreSQL maintenance database and creates `POSTGRES_DB` if missing.
2. `Base.metadata.create_all(bind=engine)` creates missing SQLAlchemy tables.
3. `init_mongodb()` initializes Beanie with `Essay` and `ReviewerNote`.

This means a fresh local database does not require manual SQL table creation.

Alembic files are present under `backend/alembic`, but the existing migration is not the current fresh-install table creation path. Do not rely on Alembic alone for fresh setup unless migrations are repaired and adopted as the source of truth.

## PostgreSQL Setup

Start PostgreSQL locally, then set:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=scholartrack
```

The app will create the `scholartrack` database if it does not exist.

Relevant tables:
- `users`
- `students`
- `scholarships`
- `applications`
- `decisions`
- `reviewer_requests`

## MongoDB Setup

Set:

```env
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=scholartrack
```

MongoDB collections used by the app:
- `essays`
- `reviewer_notes`

The code initializes MongoDB in `backend/app/config/mongodb.py`.

## Running Backend

From the repository root:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend
```

Alternative from the backend folder:

```powershell
cd backend
..\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Backend URLs:
- API root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Creating the Admin User

`seed_admin.py` is not automatically executed. Run it after backend startup has created the PostgreSQL database and tables:

```powershell
cd backend
..\venv\Scripts\python.exe seed_admin.py
```

The script creates `admin@scholartrack.com` with password `admin123` if that email does not already exist. Change this before production use.

## Running Frontend

From the frontend folder:

```powershell
cd frontend
npm run dev
```

The Vite app uses:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Frontend routes:
- `/` login
- `/register`
- `/verify-email`
- `/scholarships`
- `/scholarships/:id`
- `/apply/:scholarshipId`
- `/my-applications`
- `/reviewer`
- `/reviewer-request`
- `/profile`
- `/admin`

## Running Tests

The backend tests are under `backend/tests`.

After installing `backend/requirements.txt`, run:

```powershell
pytest backend/tests
```

Current backend test coverage includes:
- registration and login
- duplicate email prevention
- role restrictions
- student profile and application count
- scholarship CRUD, filtering, and stats
- application creation, duplicate prevention, assignment, detail merge
- decision lifecycle and duplicate decision prevention
- reviewer request validation
- health check

## Running Azure DevOps Pipeline

The pipeline is defined in:

```text
pipelines/azure-pipelines.yml
```

Pipeline trigger:
- `main`
- `master`

Stages:
1. `QualityAndSecurity`
   - installs dependencies with uv
   - runs Black check
   - runs isort check
   - runs flake8
   - runs mypy
   - runs Bandit
   - runs Safety check
2. `Test`
   - starts PostgreSQL, MongoDB, and Redis service containers
   - runs pytest with coverage
   - publishes JUnit test results
   - publishes coverage
3. `Package`
   - archives the backend folder as a zip artifact

Important pipeline note: the pipeline currently exports `MONGO_URI`, but the application reads `MONGO_URL`. Update the pipeline variable name before relying on the test stage in Azure.

## API Documentation

Run the backend and open:

```text
http://127.0.0.1:8000/docs
```

Major API groups:
- `/auth`
- `/users`
- `/students`
- `/scholarships`
- `/applications`
- `/essays`
- `/reviewer-notes`
- `/admin`
- `/health`

## Troubleshooting

### `database "scholartrack" does not exist`

Confirm PostgreSQL variables are set:

```env
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

The backend should auto-create the database at startup.

### `relation "users" does not exist`

The backend must run startup once so `Base.metadata.create_all(bind=engine)` creates tables. Start the backend with Uvicorn, then retry.

### MongoDB connection fails

Confirm:

```env
MONGO_URL
MONGO_DB_NAME
```

If using Atlas, confirm network access and credentials.

### Frontend cannot reach backend

Confirm:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Restart Vite after changing frontend env variables.

## Deployment Notes

- Use real secrets through environment variables, not committed `.env` files.
- Start PostgreSQL and MongoDB before the backend.
- Redis is optional; the app degrades gracefully if Redis is unavailable.
- nginx is configured to proxy port 80 to `backend:8000`.
- Admin seed script is manual.
- Alembic exists but is not currently the fresh-install schema source of truth.
