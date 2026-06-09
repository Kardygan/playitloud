"""add composite primary keys to order and supplier order items

Revision ID: 3caaa3a33bea
Revises: 60f8d579e516
Create Date: 2026-06-09 17:28:21.118225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3caaa3a33bea'
down_revision: Union[str, Sequence[str], None] = '60f8d579e516'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_primary_key('order_items_pkey', 'order_items', ['order_id', 'album_id'])
    op.create_primary_key(
        'supplier_order_items_pkey', 'supplier_order_items', ['supplier_order_id', 'album_id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('supplier_order_items_pkey', 'supplier_order_items', type_='primary')
    op.drop_constraint('order_items_pkey', 'order_items', type_='primary')
