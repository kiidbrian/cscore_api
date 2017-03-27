"""empty message

Revision ID: eb4746788e26
Revises: 
Create Date: 2017-03-20 09:20:54.437194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb4746788e26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('fullname', sa.String(length=255), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('weekly_income', sa.String(length=255), nullable=False),
    sa.Column('home_address', sa.String(length=255), nullable=True),
    sa.Column('work_address', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=255), nullable=False),
    sa.Column('pin_hash', sa.String(length=255), nullable=False),
    sa.Column('occupation', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_logout_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('fullname', sa.String(length=255), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('signed_up', sa.Boolean(), nullable=True),
    sa.Column('phone_number', sa.String(length=255), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loanrequests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.String(length=255), nullable=False),
    sa.Column('installment_amount', sa.String(length=255), nullable=True),
    sa.Column('referral', sa.String(length=255), nullable=True),
    sa.Column('id_type', sa.String(length=255), nullable=False),
    sa.Column('id_number', sa.String(length=255), nullable=False),
    sa.Column('interest_rate', sa.String(length=255), nullable=True),
    sa.Column('processing_officer', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('phoneNumber', sa.String(length=255), nullable=True),
    sa.Column('momoNumber', sa.String(length=255), nullable=True),
    sa.Column('mno', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('paymentPlan', sa.String(length=255), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loanpayments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('amount_paid', sa.String(length=255), nullable=False),
    sa.Column('amount_remaining', sa.String(length=255), nullable=False),
    sa.Column('loan_request_id', sa.Integer(), nullable=True),
    sa.Column('paymentPlan', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['loan_request_id'], ['loanrequests.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loanpayments')
    op.drop_table('loanrequests')
    op.drop_table('invites')
    op.drop_table('activities')
    op.drop_table('users')
    op.drop_table('clients')
    # ### end Alembic commands ###
