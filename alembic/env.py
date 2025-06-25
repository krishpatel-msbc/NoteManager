import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context



# Add the project root directory to sys.path so we can import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Import app settings and models for Alembic's autogenerate support
from backend.core.config import settings
from backend.models.base import Base  
from backend.models.user import User
from backend.models.note import Note, Tag


# Alembic Config object, provides access to values within alembic.ini
config = context.config

# Set up Python logging according to alembic.ini configuration
fileConfig(config.config_file_name)

# Override sqlalchemy.url in alembic config with the DATABASE_URL from our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# Target metadata for Alembic to know which models to reflect in migrations
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL, without a DB connection.
    Useful for generating SQL scripts without executing them.
    """
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
    """Run migrations in 'online' mode.
    This connects to the database and applies migrations directly.
    """
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

# Decide which migration mode to run based on Alembic context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
