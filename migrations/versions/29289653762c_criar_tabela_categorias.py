"""criar tabela categorias

Revision ID: 29289653762c
Revises: df2f53a964a6
Create Date: 2026-03-16 19:24:56.616602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29289653762c'
down_revision: Union[str, Sequence[str], None] = 'df2f53a964a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'categorias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=50), nullable=False),
        sa.Column('descricao', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome')
    )
    op.create_index(op.f('ix_categorias_id'), 'categorias', ['id'], unique=False)

    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_produtos_categoria_id',
            'categorias',
            ['categoria_id'],
            ['id']
        )
        batch_op.drop_column('categoria')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.String(length=50), nullable=False))
        batch_op.drop_constraint('fk_produtos_categoria_id', type_='foreignkey')
        batch_op.drop_column('categoria_id')

    op.drop_index(op.f('ix_categorias_id'), table_name='categorias')
    op.drop_table('categorias')