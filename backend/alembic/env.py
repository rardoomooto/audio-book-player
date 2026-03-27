"""Alembic environment for autogenerate/migrate with sync engine.

This environment uses a synchronous SQLAlchemy engine to run migrations,
while the application uses an async engine at runtime.
"""

from __future__ import annotations

import os
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from alembic import context

# this is the path to the directory containing this file's parent
BASE = Path(__file__).resolve().parents[1]
config = context.config
fileConfig(config.config_file_name)

# import Base from the application so that Alembic can pick up metadata
import sys
sys.path.insert(0, str(BASE))

from backend.app.core.database import Base  # noqa: E402  # re-exported metadata

target_metadata = Base.metadata


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./sqlite.db")


def run_migrations_offline():
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable: Engine = create_engine(get_database_url())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def main():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


if __name__ == "__main__":
    main()
