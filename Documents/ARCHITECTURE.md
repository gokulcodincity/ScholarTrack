# ScholarTrack Architecture

## System Overview

ScholarTrack is split into:

- React frontend served by Vite during development.
- FastAPI backend exposing REST endpoints.
- PostgreSQL for relational business records.
- MongoDB for essay and reviewer note documents.
- Redis for optional scholarship list caching.
- nginx reverse proxy configuration for backend forwarding.
- Azure DevOps pipeline for quality, security, tests, and packaging.

## Component Diagram

```mermaid
flowchart LR
    Browser["React Frontend"]
    API["FastAPI Backend"]
    PG["PostgreSQL"]
    Mongo["MongoDB"]
    Redis["Redis Cache"]
    Nginx["nginx Reverse Proxy"]
    Pipeline["Azure DevOps Pipeline"]

    Browser -->|Axios REST calls with JWT| API
    Nginx -->|proxy_pass backend:8000| API
    API -->|SQLAlchemy| PG
    API -->|Beanie ODM| Mongo
    API -->|Scholarship cache| Redis
    Pipeline -->|lint, type check, security, tests, package| API
```

## Data Flow

1. The frontend stores JWT in `localStorage`.
2. Axios interceptor adds `Authorization: Bearer <token>`.
3. FastAPI decodes JWT and applies role guards.
4. SQLAlchemy reads and writes relational data in PostgreSQL.
5. Beanie reads and writes essays and reviewer notes in MongoDB.
6. Responses are returned as JSON.
7. Global error handlers format errors as `{ success: false, error: ... }`.

## Frontend Architecture

Frontend files live in `frontend/src`.

Key folders:
- `pages`: route-level screens.
- `components`: shared layout, navbar, sidebar, loader, error message.
- `services`: Axios API wrappers.
- `context`: auth token context.

Routing is defined in `frontend/src/App.jsx`.

API integration is centralized in `frontend/src/services/api.js`, which sets `baseURL` from `VITE_API_BASE_URL` and attaches the JWT token from `localStorage`.

## Backend Architecture

Backend files live in `backend/app`.

Key folders:
- `config`: environment settings, database setup, MongoDB setup, Redis, logging, rate limiter, security.
- `models`: SQLAlchemy models and MongoDB Beanie documents.
- `schemas`: Pydantic request and response models.
- `routes`: API routers.
- `services`: business logic.
- `repositories`: user and student data access helpers.
- `middleware`: auth, role checks, CORS, global errors.
- `utils`: enums, sanitization, constants, helpers.

`backend/app/main.py` creates the FastAPI app, configures logging, initializes startup, registers middleware, and includes all routers.

## PostgreSQL Architecture

PostgreSQL stores the main relational workflow.

Entities:
- `users`
- `students`
- `scholarships`
- `applications`
- `decisions`
- `reviewer_requests`

Relationships:
- `students.user_id` references `users.id`
- `applications.student_id` references `users.id`
- `applications.scholarship_id` references `scholarships.id`
- `applications.reviewer_id` references `users.id`
- `decisions.application_id` references `applications.id`
- `decisions.decided_by` references `users.id`
- `reviewer_requests.user_id` references `users.id`

The application has a unique rule preventing the same student from applying to the same scholarship twice.

## MongoDB Architecture

MongoDB stores document-like application content:

- `essays`
- `reviewer_notes`

Both documents connect to the relational application using `application_id`.

## Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant PostgreSQL

    User->>Frontend: Submit login form
    Frontend->>API: POST /auth/login
    API->>PostgreSQL: Find user by email
    API->>API: Verify bcrypt password
    API->>API: Check verified_email and role
    API-->>Frontend: JWT access_token
    Frontend->>Frontend: Store token in localStorage
    Frontend->>API: Later requests with Bearer token
```

## Application Lifecycle

FastAPI startup runs through `lifespan` in `backend/app/main.py`:

1. Ensure PostgreSQL database exists.
2. Create missing SQLAlchemy tables with `Base.metadata.create_all(bind=engine)`.
3. Initialize MongoDB Beanie documents.
4. Serve requests.
5. Log shutdown.

## Request Flow

```mermaid
flowchart TD
    Request["HTTP Request"]
    CORS["CORS Middleware"]
    Auth["JWT / Role Dependency"]
    Route["FastAPI Route"]
    Service["Service Layer"]
    Store{"Storage Needed"}
    PG["PostgreSQL via SQLAlchemy"]
    Mongo["MongoDB via Beanie"]
    Response["JSON Response"]
    Error["Global Error Handler"]

    Request --> CORS --> Auth --> Route --> Service --> Store
    Store --> PG --> Response
    Store --> Mongo --> Response
    Route --> Error --> Response
```

## Review Workflow

```mermaid
sequenceDiagram
    participant Admin
    participant API
    participant PostgreSQL
    participant Reviewer
    participant MongoDB

    Admin->>API: PATCH /applications/{id}/assign
    API->>PostgreSQL: Set reviewer_id and UNDER_REVIEW
    Reviewer->>API: GET assigned application
    API->>PostgreSQL: Load application
    API->>MongoDB: Load essay
    API-->>Reviewer: Application detail
    Reviewer->>API: POST /applications/{id}/review
    API->>MongoDB: Save reviewer note and score
    API->>PostgreSQL: Mark REVIEW_DONE
```

## Decision Workflow

```mermaid
sequenceDiagram
    participant Admin
    participant API
    participant PostgreSQL
    participant MongoDB

    Admin->>API: POST /admin/decisions
    API->>PostgreSQL: Load application
    API->>API: Check review_completed
    API->>MongoDB: Check reviewer note and score
    API->>PostgreSQL: Check no existing decision
    API->>PostgreSQL: Insert decision and update application status
    API-->>Admin: Decision response
```

## CI/CD Workflow

```mermaid
flowchart TD
    Commit["Push to main or master"]
    Quality["QualityAndSecurity Stage"]
    Format["Black and isort checks"]
    Lint["flake8"]
    Type["mypy"]
    Security["Bandit and Safety"]
    Test["Test Stage"]
    Services["Postgres, Mongo, Redis services"]
    Pytest["pytest with coverage"]
    Package["Package Stage"]
    Artifact["Backend zip artifact"]

    Commit --> Quality
    Quality --> Format --> Lint --> Type --> Security
    Security --> Test
    Test --> Services --> Pytest
    Pytest --> Package --> Artifact
```

## Database Relationship Diagram

```mermaid
erDiagram
    USERS ||--o| STUDENTS : "has profile"
    USERS ||--o{ APPLICATIONS : "submits"
    USERS ||--o{ APPLICATIONS : "reviews"
    USERS ||--o| REVIEWER_REQUESTS : "submits"
    USERS ||--o{ DECISIONS : "decides"
    SCHOLARSHIPS ||--o{ APPLICATIONS : "receives"
    APPLICATIONS ||--o| DECISIONS : "has final decision"
    APPLICATIONS ||--o| ESSAYS : "has document"
    APPLICATIONS ||--o| REVIEWER_NOTES : "has document"

    USERS {
        int id
        string name
        string email
        string password
        string role
        boolean verified_email
    }

    STUDENTS {
        int id
        int user_id
        string department
        float cgpa
        string academic_year
    }

    SCHOLARSHIPS {
        int id
        string title
        string field
        decimal amount
        text eligibility
        date deadline
    }

    APPLICATIONS {
        int id
        int student_id
        int scholarship_id
        int reviewer_id
        string status
        boolean review_completed
        datetime created_at
    }

    DECISIONS {
        int id
        int application_id
        string decision_status
        int decided_by
        datetime decided_at
    }

    REVIEWER_REQUESTS {
        int id
        int user_id
        string university
        string department
        int years_of_experience
        string institution_email
        string resume_filename
        string status
    }

    ESSAYS {
        objectId id
        int application_id
        string essay
        string supporting_content
    }

    REVIEWER_NOTES {
        objectId id
        int application_id
        string reviewer_notes
        int score
        string scoring_rationale
    }
```

## High Level Architecture

```mermaid
flowchart TB
    subgraph Client
        React["React + Vite UI"]
    end

    subgraph Backend
        FastAPI["FastAPI App"]
        Auth["JWT and Role Guards"]
        Services["Service Layer"]
        Errors["Global Error Handler"]
    end

    subgraph Data
        Postgres["PostgreSQL"]
        Mongo["MongoDB"]
        Redis["Redis"]
    end

    React -->|REST API| FastAPI
    FastAPI --> Auth
    FastAPI --> Services
    FastAPI --> Errors
    Services --> Postgres
    Services --> Mongo
    Services --> Redis
```

## Application Submission Flow

```mermaid
sequenceDiagram
    participant Student
    participant Frontend
    participant API
    participant PostgreSQL
    participant MongoDB

    Student->>Frontend: Opens scholarship detail
    Frontend->>API: GET /scholarships/{id}
    API->>PostgreSQL: Load scholarship
    Student->>Frontend: Submits application and essay
    Frontend->>API: POST /applications/
    API->>PostgreSQL: Create PENDING application
    Frontend->>API: POST /essays/
    API->>MongoDB: Save essay document
```
