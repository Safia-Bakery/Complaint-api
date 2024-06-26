"""Edit table columns

Revision ID: cbd1c7283aea
Revises: 
Create Date: 2024-06-26 17:09:32.891187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbd1c7283aea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('complaints', sa.Column('is_telegram', sa.Integer(), nullable=True))
    op.add_column('hrcategories', sa.Column('hrsphere_id', sa.BIGINT(), nullable=True))
    op.create_foreign_key(None, 'hrcategories', 'hrspheras', ['hrsphere_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'hrcategories', type_='foreignkey')
    op.drop_column('hrcategories', 'hrsphere_id')
    op.drop_column('complaints', 'is_telegram')
    # ### end Alembic commands ###
