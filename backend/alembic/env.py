from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.db.base import Base
from app.core.config import settings

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Use correct DB URL depending on environment
db_url = settings.DB_URL

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
