"""Add album column to contents table"""

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add album column to contents table
    op.add_column('contents', sa.Column('album', sa.String(length=100), nullable=True))


def downgrade():
    # Remove album column from contents table
    op.drop_column('contents', 'album')