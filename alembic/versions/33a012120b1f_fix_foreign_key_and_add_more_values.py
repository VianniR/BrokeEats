"""fix foreign key and add more values

Revision ID: 33a012120b1f
Revises: d95d605f5030
Create Date: 2025-05-12 11:02:23.148948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33a012120b1f'
down_revision: Union[str, None] = 'd95d605f5030'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('restaurants_cuisine_id_fkey', 'restaurants', type_='foreignkey')
    op.create_foreign_key('restaurants_cuisine_id_fkey1', 'restaurants', 'cuisines', ['cuisine_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('reviews_cuisine_id_fkey', 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'cuisine_id')

    op.execute("""INSERT INTO user_preferences (user_id, preference_id) VALUES (1, 1)""")
    op.execute("""INSERT INTO user_preferences (user_id, preference_id) VALUES (2, 2)""")

    op.execute(
        """INSERT INTO restaurants (name, cuisine_id, address, city, state, zipcode, phone) VALUES ('El Guero', 1, '1122 Chorro St', 'San Luis Obispo', 'CA', '93401', '805-540-4637')""")
    op.execute(
        """INSERT INTO restaurants (name, cuisine_id, address, city, state, zipcode, phone) VALUES ('Panda Express', 2, '789 Foothill Blvd', 'San Luis Obispo', 'CA', '93405', '805-784-0355')""")

    op.execute(
        """INSERT INTO reviews (user_id, restaurant_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review) VALUES (1, 1, 4.5, 5, 3, 5, 5, 'Nice')""")
    op.execute(
        """INSERT INTO reviews (user_id, restaurant_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review) VALUES (1, 2, 3, 4, 5, 2, 1, 'Good')""")

    op.execute(
        """INSERT INTO restaurant_preferences (restaurant_id, preference_id, last_updated_by) VALUES (2, 1, 1)""")
    op.execute(
        """INSERT INTO restaurant_preferences (restaurant_id, preference_id, last_updated_by) VALUES (1, 1, 1)""")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('restaurants_cuisine_id_fkey1', 'restaurants', type_='foreignkey')
    op.create_foreign_key(
        'restaurants_cuisine_id_fkey', 'restaurants', 'preferences', ['cuisine_id'], ['id'],)
    op.add_column('reviews',sa.Column("cuisine_id", sa.Integer, sa.ForeignKey("cuisines.id", ondelete="CASCADE"),nullable=False,),
 )
    op.execute("""TRUNCATE user_preferences RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE restaurants RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE reviews RESTART IDENTITY CASCADE""")
    op.execute("""TRUNCATE restaurant_preferences RESTART IDENTITY CASCADE""")



