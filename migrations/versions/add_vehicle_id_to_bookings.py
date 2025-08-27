"""Add vehicle_id to bookings table

Revision ID: add_vehicle_id_to_bookings
Revises: add_user_id_to_bookings
Create Date: 2025-08-27 09:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_vehicle_id_to_bookings'
down_revision = 'add_user_id_to_bookings'
branch_labels = None
depends_on = None


def upgrade():
    # Add vehicle_id column to bookings table
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_booking_vehicle_id', 'vehicle', ['vehicle_id'], ['id'])


def downgrade():
    # Remove vehicle_id column from bookings table
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_constraint('fk_booking_vehicle_id', type_='foreignkey')
        batch_op.drop_column('vehicle_id')