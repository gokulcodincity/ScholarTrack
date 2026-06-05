from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import engine
from app.config.mongodb import init_mongodb

from app.models.base import Base

# PostgreSQL Models
from app.models.user import User
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.models.application import Application
from app.models.decision import Decision

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
    lifespan=lifespan
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