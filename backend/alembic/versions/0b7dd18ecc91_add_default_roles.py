"""add_default_roles

Revision ID: [um_novo_hash_aqui]
Revises: 0c5ad5a3c4a1
Create Date: 2025-11-12 22:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '0b7dd18ecc91'
down_revision: Union[str, None] = '2d02e984f9cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Roles table reference
    roles_table = sa.table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Insert default roles
    op.bulk_insert(roles_table,
        [
            {'name': 'admin', 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'user', 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()}
        ]
    )

def downgrade():
    # Remove default roles
    op.execute("DELETE FROM roles WHERE name IN ('admin', 'user')")