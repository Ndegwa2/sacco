"""Add capacity to vehicle table

Revision ID: add_capacity_to_vehicle
Revises: add_vehicle_id_to_bookings
Create Date: 2025-08-27 09:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_capacity_to_vehicle'
down_revision = 'add_vehicle_id_to_bookings'
branch_labels = None
depends_on = None


def upgrade():
    # Add capacity column to vehicle table
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('capacity', sa.Integer(), nullable=False, server_default='33'))


def downgrade():
    # Remove capacity column from vehicle table
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.drop_column('capacity')