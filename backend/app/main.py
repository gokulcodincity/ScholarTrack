from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from app.middleware.cors import setup_cors

from app.config.database import engine
from app.config.mongodb import init_mongodb

from app.models.base import Base

# PostgreSQL Models
from app.models.user import User
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.models.application import Application
from app.models.decision import Decision
from app.models.reviewer_request import ReviewerRequest

# MongoDB ODM Models
from app.models.essay import Essay
from app.models.reviewer_note import ReviewerNote

# Routes
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.student_routes import router as student_router

from app.routes.scholarship_routes import (
    router as scholarship_router
)

from app.routes.application_routes import (
    router as application_router
)

from app.routes.admin_routes import (
    router as admin_router
)

from app.routes.essay_routes import (
    router as essay_router
)

from app.routes.reviewer_note_routes import (
    router as reviewer_note_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize MongoDB ODM when application starts.
    """

    await init_mongodb()

    yield

    print("Application Shutdown")


# Create PostgreSQL Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScholarTrack API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,       # Disable default docs (uses slow unpkg CDN)
    redoc_url=None
)

setup_cors(app)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    """Serve Swagger UI using jsdelivr CDN (much faster than default unpkg)."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="ScholarTrack API - Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# Authentication
app.include_router(auth_router)

# Users
app.include_router(user_router)

# Students
app.include_router(student_router)

# Scholarships
app.include_router(scholarship_router)

# Applications
app.include_router(application_router)

# Admin
app.include_router(admin_router)

# MongoDB ODM
app.include_router(essay_router)
app.include_router(reviewer_note_router)


@app.get("/")
def home():
    return {
        "message": "ScholarTrack Backend Running"
    }