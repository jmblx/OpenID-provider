import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, engine_from_config, pool

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from infrastructure.db.config import (
    DB_HOST,
    DB_PORT,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
)
from infrastructure.db.models.registry import mapper_registry

config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_USER", POSTGRES_USER)
config.set_section_option(section, "DB_NAME", POSTGRES_DB)
config.set_section_option(section, "DB_PASS", POSTGRES_PASSWORD)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = mapper_registry.metadata


def get_url():
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """Выполнение миграций в 'офлайн' режиме."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Выполнение миграций в 'онлайн' режиме."""
    url = get_url()

    if "asyncpg" in url:
        sync_url = url.replace("asyncpg", "psycopg2").replace(
            "?async_fallback=True", ""
        )
        connectable = create_engine(sync_url, poolclass=pool.NullPool)
    else:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
