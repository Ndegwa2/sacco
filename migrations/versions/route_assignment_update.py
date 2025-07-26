"""Route assignment update

Revision ID: route_assignment_update
Revises: 272698cc9673
Create Date: 2025-07-26 03:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'route_assignment_update'
down_revision = '272698cc9673'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to assigned_route table
    op.add_column('assigned_route', sa.Column('vehicle_id', sa.Integer(), nullable=True))
    op.add_column('assigned_route', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('assigned_route', sa.Column('end_date', sa.Date(), nullable=True))
    op.add_column('assigned_route', sa.Column('status', sa.String(20), nullable=True, server_default='active'))
    op.add_column('assigned_route', sa.Column('shift', sa.String(20), nullable=True))
    op.add_column('assigned_route', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('assigned_route', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('assigned_route', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('assigned_route', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Add foreign key constraints
    op.create_foreign_key('fk_assigned_route_vehicle', 'assigned_route', 'vehicle', ['vehicle_id'], ['id'])
    op.create_foreign_key('fk_assigned_route_created_by', 'assigned_route', 'user', ['created_by'], ['id'])
    
    # Update existing records to set default values
    op.execute("UPDATE assigned_route SET status = 'active' WHERE status IS NULL")
    op.execute("UPDATE assigned_route SET start_date = date_assigned WHERE start_date IS NULL")
    op.execute("UPDATE assigned_route SET created_at = date_assigned WHERE created_at IS NULL")
    op.execute("UPDATE assigned_route SET updated_at = date_assigned WHERE updated_at IS NULL")
    
    # Make vehicle_id nullable=False after migration
    # We're setting it to nullable=True initially to avoid errors with existing records
    # In a production environment, you might want to handle this differently


def downgrade():
    # Remove foreign key constraints first
    op.drop_constraint('fk_assigned_route_vehicle', 'assigned_route', type_='foreignkey')
    op.drop_constraint('fk_assigned_route_created_by', 'assigned_route', type_='foreignkey')
    
    # Remove columns
    op.drop_column('assigned_route', 'vehicle_id')
    op.drop_column('assigned_route', 'start_date')
    op.drop_column('assigned_route', 'end_date')
    op.drop_column('assigned_route', 'status')
    op.drop_column('assigned_route', 'shift')
    op.drop_column('assigned_route', 'notes')
    op.drop_column('assigned_route', 'created_by')
    op.drop_column('assigned_route', 'created_at')
    op.drop_column('assigned_route', 'updated_at')