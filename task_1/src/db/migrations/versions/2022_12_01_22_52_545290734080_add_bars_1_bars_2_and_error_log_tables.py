"""Add bars_1, bars_2 and error_log tables

Revision ID: 545290734080
Revises: 
Create Date: 2022-12-01 22:52:46.323673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '545290734080'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'bars_1',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('adj_close', sa.DECIMAL(), nullable=True),
        sa.Column('close', sa.DECIMAL(), nullable=True),
        sa.Column('high', sa.DECIMAL(), nullable=True),
        sa.Column('low', sa.DECIMAL(), nullable=True),
        sa.Column('open', sa.DECIMAL(), nullable=True),
        sa.Column('volume', sa.DECIMAL(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bars_2',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('adj_close', sa.DECIMAL(), nullable=True),
        sa.Column('close', sa.DECIMAL(), nullable=True),
        sa.Column('high', sa.DECIMAL(), nullable=True),
        sa.Column('low', sa.DECIMAL(), nullable=True),
        sa.Column('open', sa.DECIMAL(), nullable=True),
        sa.Column('volume', sa.DECIMAL(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'error_log',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('launch_timestamp', sa.DateTime(), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('symbol', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('error_log')
    op.drop_table('bars_2')
    op.drop_table('bars_1')
    # ### end Alembic commands ###
