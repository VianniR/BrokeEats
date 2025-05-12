"""add example values

Revision ID: d95d605f5030
Revises: 193dbf515a3c
Create Date: 2025-05-12 10:27:13.462475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'd95d605f5030'
down_revision: Union[str, None] = '193dbf515a3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""INSERT INTO cuisines (name) VALUES ('mexican')""")
    op.execute("""INSERT INTO cuisines (name) VALUES ('chinese')""")
    op.execute("""INSERT INTO cuisines (name) VALUES ('greek')""")

    op.execute("""INSERT INTO preferences (name) VALUES ('gluten free')""")
    op.execute("""INSERT INTO preferences (name) VALUES ('dairy free')""")
    op.execute("""INSERT INTO preferences (name) VALUES ('vegan')""")

    op.execute("""INSERT INTO users (name, username, email, permissions) VALUES ('Bob', 'SpongeBob2Loco', 'bob12@calpoly.edu', 1)""")
    op.execute("""INSERT INTO users (name, username, email, permissions) VALUES ('Dave', 'D_ave', 'dave#calpoly.edu', 1)""")










def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""TRUNCATE cuisines RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE restaurant_preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE restaurants RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE reviews RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE user_preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE users RESTART IDENTITY CASCADE""")






