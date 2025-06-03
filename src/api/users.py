from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.api import auth
import sqlalchemy
from src import database as db
import re

router = APIRouter(prefix="/users",
                  tags=["users"],
                   dependencies=[Depends(auth.get_api_key)])


class Profile(BaseModel):
        id: int
        name: str
        username: str
        email: str
        permissions: int

class NewUser(BaseModel):
    name: str = Field(..., max_length=100)
    username: str = Field(..., max_length=50, pattern=r'^\w+$')
    email: str = Field(..., max_length=100, pattern=r'^\S+@\S+\.\S+$')

    @field_validator('name', 'username', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, example="", max_length=100)
    username: Optional[str] = Field(None, example="", max_length=50, pattern=r'^\w+$')
    email: Optional[str] = Field(None, example="", max_length=100, pattern=r'^\S+@\S+\.\S+$')

    @field_validator('name', 'username', 'email', mode='before')
    def empty_str_to_none(cls, v):
        if v is not None and isinstance(v, str) and not v.strip():
            return None
        return v

def ensure_user_exists(user_id: int):
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 1 FROM users WHERE id = :user_id"), {"user_id": user_id})
        if result.first() is None:
            raise HTTPException(status_code=404, detail="User not found")
        
class RestaurantRecommendation(BaseModel):
    id: int
    name: str
    cuisine: str
    address: str
    city: str
    state: str
    zipcode: str
    phone: Optional[str]
    overall_score: Optional[float]
    food_rating: Optional[float]
    service_rating: Optional[float]
    price_rating: Optional[float]
    cleanliness_rating: Optional[float]

@router.post("/profile", response_model=Profile)
def create_profile(profile: NewUser) -> Profile:
    try:
        with db.engine.begin() as conn:
            user_id = conn.execute(sqlalchemy.text(
                "INSERT INTO users (name, username, email, permissions) VALUES (:name, :username, :email, 1) RETURNING id"
            ),
            {
                "name": profile.name,
                "username": profile.username,
                "email": profile.email,
            }).scalar_one()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    return Profile(id=user_id, name=profile.name, username=profile.username, email=profile.email, permissions=1)


@router.get("/profile/{user_name}", response_model=Profile)
def get_profile(user_name: str) -> Profile:
    try:
        with db.engine.begin() as connection:
            user = connection.execute(
                sqlalchemy.text(
                    "SELECT id, name, username, email, permissions FROM users WHERE LOWER(users.username) = LOWER(:user_name)"
                ),
                {"user_name": user_name}
            ).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# PATCH endpoint to update username
@router.patch("/profile/{id}", response_model=Profile)
def update_profile(id: int, payload: ProfileUpdate):
    """Updates any provided user fields."""
    ensure_user_exists(id)
    updates = payload.model_dump(exclude_unset=True)

    updates = {k: v for k, v in updates.items() if v is not None and not (isinstance(v, str) and v.strip() == "")}

    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    set_clauses = ", ".join(f"{field} = :{field}" for field in updates.keys())
    params = {**updates, "user_id": id}
    try:
        with db.engine.begin() as connection:
            connection.execute(
                    sqlalchemy.text("UPDATE users SET " + set_clauses + " WHERE id = :user_id"),
                    params
                )
            user = connection.execute(
                sqlalchemy.text(
                    "SELECT id, name, username, email, permissions FROM users WHERE id = :user_id"
                ),
                {"user_id": id}
            ).one()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    return user


@router.get("/users/recommendations", response_model=List[RestaurantRecommendation])
def get_preference_recc_id(user_id: int, limit: int) -> List[RestaurantRecommendation]:
    restaurants: List[RestaurantRecommendation] = []

    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("""
        SELECT DISTINCT 
        restaurants.id as id, 
        restaurants.name as name, 
        cuisines.name as cuisine, 
        address, 
        city, 
        state, 
        zipcode, 
        phone, 
        AVG(overall_rating) as overall_score, 
        AVG(food_rating) as food_rating, 
        AVG(service_rating) as service_rating, 
        AVG(price_rating) as price_rating, 
        AVG(cleanliness_rating) as cleanliness_rating
        FROM restaurants
        JOIN cuisines ON cuisines.id = restaurants.cuisine_id
        JOIN restaurant_preferences ON restaurant_preferences.restaurant_id = restaurants.id
        JOIN preferences ON preferences.id = restaurant_preferences.preference_id
        JOIN user_preferences ON user_preferences.preference_id = preferences.id
        JOIN users on users.id = user_preferences.user_id
        JOIN reviews ON reviews.restaurant_id = restaurants.id
        WHERE users.id = :user_id
        group by restaurants.id, restaurants.name, cuisines.name, address, city, state, zipcode, phone
        ORDER BY AVG(overall_rating) DESC
        LIMIT :limit
        """),
            {
                "user_id": user_id,
                "limit": limit,
            })
        for row in result.mappings():
            restaurants.append(RestaurantRecommendation(**row))

    return restaurants