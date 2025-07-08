import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env.test or .env
from backend.core.config import settings
from backend.models.base import Base
from backend.models.user import User
from backend.models.note import Note, Tag

# Get Alembic configuration
config = context.config
fileConfig(config.config_file_name)

# Override URL from settings (from .env or .env.test)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 🚨 Ensure this runs only on the test DB when testing
if os.getenv("PYTEST_CURRENT_TEST") and "test" not in settings.DATABASE_URL:
    raise RuntimeError(f"[ABORTED] Alembic tried to run on a non-test DB: {settings.DATABASE_URL}")

# Metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
