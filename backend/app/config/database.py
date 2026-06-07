import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.logger import logger
from app.config.settings import (
    DATABASE_URL,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_MAINTENANCE_DB,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)


def ensure_database_exists():
    connection = None

    try:
        connection = psycopg2.connect(
            dbname=POSTGRES_MAINTENANCE_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (POSTGRES_DB,),
            )

            if cursor.fetchone():
                logger.info("PostgreSQL database exists", database=POSTGRES_DB)
                return

            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(POSTGRES_DB)
                )
            )
            logger.info(
                "PostgreSQL database created successfully",
                database=POSTGRES_DB,
            )

    except Exception as exc:
        logger.error(
            "PostgreSQL database creation failure",
            database=POSTGRES_DB,
            error=str(exc),
        )
        raise

    finally:
        if connection is not None:
            connection.close()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
