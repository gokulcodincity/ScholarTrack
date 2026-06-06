from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import DATABASE_URL


# PostgreSQL engine
engine = create_engine(DATABASE_URL)

# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Provide a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()