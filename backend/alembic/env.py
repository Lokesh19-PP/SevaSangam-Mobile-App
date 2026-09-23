"""
Alembic environment configuration.

Imports all models via backend.app.models so Base.metadata contains every table,
then uses the synchronous DB URL from backend.app.db.session.

Excludes PostGIS internal tables (tiger geocoder, topology, spatial_ref_sys)
from autogenerate comparison so they aren't accidentally dropped.
"""

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Make sure backend package is importable ──────────────────────────────────
# When running `alembic` from the backend/ directory, the repo root isn't on
# sys.path by default.  Add the repo root so `from backend.app...` works.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# ── Load all models so Base.metadata is fully populated ──────────────────────
from backend.app.models import Base          # noqa: E402
from backend.app.db.session import SYNC_DATABASE_URL  # noqa: E402

# Alembic Config object (reads alembic.ini)
config = context.config

# Override the URL from env vars (not the placeholder in alembic.ini)
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Set up Python logging from the ini file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata

# ── PostGIS exclusion ────────────────────────────────────────────────────────
# The postgis/postgis Docker image creates many internal tables in the
# public schema (tiger geocoder, topology helpers, spatial_ref_sys, etc.).
# We must exclude them so autogenerate doesn't try to drop them.

# Tables that belong to our app (everything else is PostGIS internal)
_OUR_TABLES = set(target_metadata.tables.keys())


def include_object(object, name, type_, reflected, compare_to):
    """Only include our own tables in autogenerate diffs."""
    if type_ == "table":
        return name in _OUR_TABLES
    # Include columns, indexes etc. that belong to our tables
    return True


def run_migrations_offline():
    """Run migrations in 'offline' mode — generates SQL without a live DB."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode — connects to the DB."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
