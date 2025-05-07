from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(prefix="/reviews",
                  tags=["reviews"],
                   dependencies=[Depends(auth.get_api_key)])


class Review(BaseModel):
    user_id: int
    restaurant_id: int
    cuisine_id: int
    overall: float
    food: Optional[float] = None
    service: Optional[float] = None
    price: Optional[float] = None
    cleanliness: Optional[float] = None
    note: Optional[str] = Field(None, example = "Great Place")


@router.post("/reviews", response_model = Review)
def create_review(review : Review):
    try:
        with db.engine.begin() as conn:
            rev = conn.execute(sqlalchemy.text("""
            INSERT INTO reviews (user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review )
            VALUES (:user, :restaurant, :cuisine,:overall, :food, :service, :price, :cleanliness, :written)
            RETURNING id;                                   
            """), 
                 {
                      "user": review.user_id,
                      "restaurant": review.restaurant_id,
                      "cuisine": review.cuisine_id,
                      "overall": review.overall,
                      "food": review.food,
                      "service": review.service,
                      "price": review.price,
                      "cleanliness": review.cleanliness,
                      "written": review.note
                 }
            ).scalar()
        
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(detail="Test")
    
    return Review(
        user_id=review.user_id,
        restaurant_id=review.restaurant_id,
        cuisine_id=review.cuisine_id,
        overall=review.overall,
        food=review.food,
        service=review.service,
        price=review.price,
        cleanliness=review.cleanliness,
        note=review.note
    )

@router.get("/reviews/{restaurant_id}", response_model = List[Review])
def get_reviews(restaurant_id: int):
    with db.engine.begin() as conn:
        revs = conn.execute(
            sqlalchemy.text("""SELECT user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review 
                                FROM reviews
                                WHERE restaurant_id = :restaurant_id
                            """), {"restaurant_id" : restaurant_id}
                            ).fetchall()
        
    reviews = []
    for rev in revs:
        reviews.append(Review(
            user_id=rev[0],
            restaurant_id=rev[1],
            cuisine_id=rev[2],
            overall=rev[3],
            food=rev[4],
            service=rev[5],
            price=rev[6],
            cleanliness=rev[7],
            note=rev[8]
         ))
    return reviews
