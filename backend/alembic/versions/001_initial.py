"""Initial migration: create all core tables"""

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Folders table
    op.create_table(
        'folders',
        sa.Column('folder_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('path', sa.String(length=500), nullable=False),
        sa.Column('parent_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('folder_id')
    )

    # Contents table
    op.create_table(
        'contents',
        sa.Column('content_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=True),
        sa.Column('series', sa.String(length=100), nullable=True),
        sa.Column('path', sa.String(length=500), nullable=False),
        sa.Column('file_format', sa.String(length=20), nullable=False),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('cover_path', sa.String(length=500), nullable=True),
        sa.Column('content_metadata', sa.JSON(), nullable=True),
        sa.Column('folder_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('content_id')
    )
    op.create_foreign_key(None, 'contents', 'folders', ['folder_id'], ['folder_id'])

    # Permissions table (user permissions per folder)
    op.create_table(
        'user_permissions',
        sa.Column('permission_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('folder_id', sa.String(length=36), nullable=False),
        sa.Column('permission_type', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('permission_id')
    )
    op.create_foreign_key(None, 'user_permissions', 'users', ['user_id'], ['user_id'])
    op.create_foreign_key(None, 'user_permissions', 'folders', ['folder_id'], ['folder_id'])

    # Play limits table
    op.create_table(
        'play_limits',
        sa.Column('limit_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('daily_minutes', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('weekly_minutes', sa.Integer(), nullable=True),
        sa.Column('monthly_minutes', sa.Integer(), nullable=True),
        sa.Column('yearly_minutes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('limit_id')
    )
    op.create_foreign_key(None, 'play_limits', 'users', ['user_id'], ['user_id'])

    # Play records table
    op.create_table(
        'play_records',
        sa.Column('record_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('content_id', sa.String(length=36), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('play_position_seconds', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('record_id')
    )
    op.create_foreign_key(None, 'play_records', 'users', ['user_id'], ['user_id'])
    op.create_foreign_key(None, 'play_records', 'contents', ['content_id'], ['content_id'])

    # Daily statistics table
    op.create_table(
        'daily_stats',
        sa.Column('statistics_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('total_duration_seconds', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('content_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('most_played_content_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('statistics_id')
    )
    op.create_foreign_key(None, 'daily_stats', 'users', ['user_id'], ['user_id'])
    op.create_foreign_key(None, 'daily_stats', 'contents', ['most_played_content_id'], ['content_id'])


def downgrade():
    op.drop_table('daily_stats')
    op.drop_table('play_records')
    op.drop_table('play_limits')
    op.drop_table('user_permissions')
    op.drop_table('contents')
    op.drop_table('folders')
    op.drop_table('users')
