"""create user, review, restaurant tables

Revision ID: 193dbf515a3c
Revises: 
Create Date: 2025-05-04 14:07:20.861324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '193dbf515a3c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("name", sa.String(length=255), nullable=False),
                    sa.Column("username", sa.String(length=255), nullable=False, unique=True),
                    sa.Column("email", sa.String(length=255), nullable=False, unique=True),
                    sa.Column("permissions", sa.Integer, nullable=False, server_default=sa.text("0")),
                    sa.Column("last_updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"),
                              nullable=False),
                    )

    op.create_table("preferences",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("name", sa.String(length=255), nullable=False),

                    sa.UniqueConstraint("name"),
                    )

    op.create_table("cuisines",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("name", sa.String(length=255), nullable=False),

                    sa.UniqueConstraint("name"),
                    )

    op.create_table("restaurants",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("cuisine_id", sa.Integer,sa.ForeignKey("preferences.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("address", sa.String, nullable=False),
                    sa.Column("city", sa.String, nullable=False),
                    sa.Column("state", sa.String, nullable=False),
                    sa.Column("zipcode", sa.String, nullable=False),
                    sa.Column("phone", sa.String, nullable=True),
                    sa.Column("last_updated_by", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
                    sa.Column("last_updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
                    sa.UniqueConstraint("name", "address", "city", "state", "zipcode"),
                    )
    op.create_table("reviews",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("user_id", sa.Integer,sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False,),
                    sa.Column("restaurant_id", sa.Integer, sa.ForeignKey("restaurants.id", ondelete="CASCADE"),nullable=False,),
                    sa.Column("cuisine_id", sa.Integer, sa.ForeignKey("cuisines.id", ondelete="CASCADE"),nullable=False,),
                    sa.Column("overall_rating", sa.Float, nullable=False),
                    sa.Column("food_rating", sa.Float, nullable=True),
                    sa.Column("service_rating", sa.Float, nullable=True),
                    sa.Column("price_rating", sa.Float, nullable=True),
                    sa.Column("cleanliness_rating", sa.Float, nullable=True),
                    sa.Column("written_review", sa.String(length = 2000), nullable=True),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"),
                              nullable=False),

                    sa.Column("last_updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"),
                              nullable=False),
                    sa.CheckConstraint("overall_rating >= 0.0 AND overall_rating <= 5.0", name="overall_rating_check_ge_0_le_5"),
                    sa.CheckConstraint("food_rating >= 0.0 AND food_rating <= 5.0", name="food_rating_check_ge_0_le_5"),
                    sa.CheckConstraint("service_rating >= 0.0 AND service_rating <= 5.0", name="service_rating_check_ge_0_le_5"),
                    sa.CheckConstraint("price_rating >= 0.0 AND price_rating <= 5.0", name="price_rating_check_ge_0_le_5"),
                    sa.CheckConstraint("cleanliness_rating >= 0.0 AND cleanliness_rating <= 5.0",name="cleanliness_rating_check_ge_0_le_5"),

                    sa.UniqueConstraint("restaurant_id", "user_id"),
                    )



    op.create_table("user_preferences",
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False,),
                    sa.Column("preference_id", sa.Integer, sa.ForeignKey("preferences.id", ondelete="CASCADE"), nullable=False,),
                    sa.UniqueConstraint("user_id", "preference_id"),
                    sa.Column("last_updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"),
                              nullable=False),
                    )
    op.create_table("restaurant_preferences",
                    sa.Column("restaurant_id", sa.Integer, sa.ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False,),
                    sa.Column("preference_id", sa.Integer, sa.ForeignKey("preferences.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("last_updated_by", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"),
                              nullable=True),
                    sa.Column("last_updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"),
                              nullable=False),
                    sa.UniqueConstraint("restaurant_id", "preference_id"),
                    )




def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE users CASCADE")
    op.execute("DROP TABLE restaurants CASCADE")
    op.execute("DROP TABLE reviews CASCADE")
    op.execute("DROP TABLE preferences CASCADE")
    op.execute("DROP TABLE cuisines CASCADE")
    op.execute("DROP TABLE user_preferences CASCADE")
    op.execute("DROP TABLE restaurant_preferences CASCADE")
