"""create accesstoken table

Revision ID: 409c8e1ae1f1
Revises: 978424e9d696
Create Date: 2026-03-15 11:33:48.029657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '409c8e1ae1f1'
down_revision: Union[str, Sequence[str], None] = '978424e9d696'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE IF NOT EXISTS accesstoken (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token VARCHAR(43) NOT NULL UNIQUE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL
    )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_accesstoken_created_at ON accesstoken (created_at)")

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS accesstoken CASCADE")