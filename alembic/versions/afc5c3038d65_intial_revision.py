"""intial revision

Revision ID: afc5c3038d65
Revises: 
Create Date: 2023-12-11 16:25:40.637501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afc5c3038d65'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('preference_survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('heading', sa.String(), nullable=True),
    sa.Column('subheading', sa.String(), nullable=True),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('preference_list', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('task_list', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee_function',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('touchpoint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('touchpoint_cluster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('touchpoint_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['touchpoint_id'], ['touchpoint.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('touchpoint_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.Column('touchpoint_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['touchpoint_id'], ['touchpoint.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('touchpoint_role')
    op.drop_table('touchpoint_cluster')
    op.drop_table('touchpoint')
    op.drop_table('employee_function')
    op.drop_table('role')
    op.drop_table('preference_survey')
    op.drop_table('employee')
    op.drop_table('department')
    op.drop_table('user')
    op.drop_table('business')
    # ### end Alembic commands ###
