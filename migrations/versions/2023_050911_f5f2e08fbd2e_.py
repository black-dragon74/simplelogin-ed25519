"""empty message

Revision ID: f5f2e08fbd2e
Revises: 2634b41f54db
Create Date: 2023-05-09 11:52:41.100335

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5f2e08fbd2e'
down_revision = '2634b41f54db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mailbox', sa.Column('verification_code', sa.String(length=128), nullable=True))
    op.add_column('mailbox', sa.Column('verification_expiration', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True))
    op.add_column('mailbox', sa.Column('verification_tries', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mailbox', 'verification_tries')
    op.drop_column('mailbox', 'verification_expiration')
    op.drop_column('mailbox', 'verification_code')
    # ### end Alembic commands ###