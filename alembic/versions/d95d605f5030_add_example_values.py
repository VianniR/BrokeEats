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

    op.execute("""INSERT INTO user_preferences (user_id, preference_id) VALUES (1, 1)""")
    op.execute("""INSERT INTO user_preferences (user_id, preference_id) VALUES (2, 2)""")

    op.execute("""INSERT INTO restaurants (name, cuisine_id, address, city, state, zipcode, phone, last_updated_by) VALUES ('El Guero', 1, '1122 Chorro St', 'San Luis Obispo', 'CA', '93401', '805-540-4637', 1)""")
    op.execute("""INSERT INTO restaurants (name, cuisine_id, address, city, state, zipcode, phone, last_updated_by) VALUES ('Panda Express', 2, '789 Foothill Blvd', 'San Luis Obispo', 'CA', '93405', '805-784-0355', 1)""")

    op.execute("""INSERT INTO reviews (user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review) VALUES (1, 1, 1, 4.5, 5, 3, 5, 5, 'Nice')""")
    op.execute("""INSERT INTO reviews (user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review) VALUES (1, 2, 2, 3, 4, 5, 2, 1, 'Good')""")

    op.execute("""INSERT INTO restaurant_preferences (restaurant_id, preference_id, last_updated_by) VALUES (2, 1, 1)""")
    op.execute("""INSERT INTO restaurant_preferences (restaurant_id, preference_id, last_updated_by) VALUES (1, 1, 1)""")









def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""TRUNCATE cuisines RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE restaurant_preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE restaurants RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE reviews RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE user_preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE users RESTART IDENTITY CASCADE""")






