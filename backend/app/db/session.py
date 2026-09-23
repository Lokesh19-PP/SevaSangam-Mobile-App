"""
Database connection helpers.

Provides both a synchronous engine (for Alembic migrations and seed scripts)
and an async engine (for the FastAPI app at runtime).
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load .env from the backend/ directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

POSTGRES_USER = os.getenv("POSTGRES_USER", "sevasangam")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "sevasangam_dev")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sevasangam")

# Synchronous URL (psycopg2) — used by Alembic and seed scripts
SYNC_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Async URL (asyncpg) — used by the FastAPI app
ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Synchronous engine + session (migrations, seeds)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)
SyncSessionLocal = sessionmaker(bind=sync_engine)
