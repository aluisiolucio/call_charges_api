"""create relationship

Revision ID: 1d106380f117
Revises: 003fbda943bc
Create Date: 2024-11-17 12:13:12.117536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d106380f117'
down_revision: Union[str, None] = '003fbda943bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Verificar se o banco é SQLite
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        # Usar o batch mode para alterações no SQLite
        with op.batch_alter_table('call_records') as batch_op:
            batch_op.add_column(sa.Column('phone_bill_id', sa.Uuid(), nullable=True))
            batch_op.create_foreign_key(
                'fk_call_records_phone_bills', 
                'phone_bills', 
                ['phone_bill_id'], 
                ['id']
            )
    else:
        # Alterações normais para outros bancos
        op.add_column('call_records', sa.Column('phone_bill_id', sa.Uuid(), nullable=True))
        op.create_foreign_key(
            'fk_call_records_phone_bills', 
            'call_records', 
            'phone_bills', 
            ['phone_bill_id'], 
            ['id']
        )


def downgrade() -> None:
    # Verificar se o banco é SQLite
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        # Usar o batch mode para alterações no SQLite
        with op.batch_alter_table('call_records') as batch_op:
            batch_op.drop_constraint('fk_call_records_phone_bills', type_='foreignkey')
            batch_op.drop_column('phone_bill_id')
    else:
        # Alterações normais para outros bancos
        op.drop_constraint('fk_call_records_phone_bills', 'call_records', type_='foreignkey')
        op.drop_column('call_records', 'phone_bill_id')
