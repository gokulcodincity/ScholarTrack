from fastapi import FastAPI

from app.config.database import Base, engine

from app.routes.user_routes import router as user_router
from app.routes.student_routes import router as student_router
from app.models.user import User
from app.models.student import Student

from app.routes.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScholarTrack API"
)

app.include_router(auth_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(student_router)


@app.get("/")
def home():

    return {
        "message": "ScholarTrack Backend Running"
    }