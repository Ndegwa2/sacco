"""Add user_id to bookings table

Revision ID: add_user_id_to_bookings
Revises: 
Create Date: 2025-01-05 10:54:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_user_id_to_bookings'
down_revision = None
depends_on = None


def upgrade():
    # Add user_id column to bookings table
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key('fk_booking_user_id', 'user', ['user_id'], ['id'])
    
    # Convert existing string date/time columns to proper types
    # Note: This is a simplified approach for SQLite. In production, you might need more complex migration
    with op.batch_alter_table('booking', schema=None) as batch_op:
        # Add new columns with proper types
        batch_op.add_column(sa.Column('date_new', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('time_new', sa.Time(), nullable=True))
    
    # Migrate data from string columns to proper date/time columns
    connection = op.get_bind()
    
    # Update date_new and time_new columns with converted values
    connection.execute("""
        UPDATE booking 
        SET date_new = date(date),
            time_new = time(time)
        WHERE date IS NOT NULL AND time IS NOT NULL
    """)
    
    # Drop old columns and rename new ones
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_column('date')
        batch_op.drop_column('time')
        batch_op.alter_column('date_new', new_column_name='date', nullable=False)
        batch_op.alter_column('time_new', new_column_name='time', nullable=False)


def downgrade():
    # Reverse the migration
    with op.batch_alter_table('booking', schema=None) as batch_op:
        # Convert back to string columns
        batch_op.add_column(sa.Column('date_old', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('time_old', sa.String(50), nullable=True))
    
    # Convert data back to strings
    connection = op.get_bind()
    connection.execute("""
        UPDATE booking 
        SET date_old = date,
            time_old = time
        WHERE date IS NOT NULL AND time IS NOT NULL
    """)
    
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_column('date')
        batch_op.drop_column('time')
        batch_op.alter_column('date_old', new_column_name='date', nullable=False)
        batch_op.alter_column('time_old', new_column_name='time', nullable=False)
        batch_op.drop_constraint('fk_booking_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
        batch_op.drop_column('created_at')