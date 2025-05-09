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
        raise HTTPException(status_code = 409, detail = "Review from that user already exists for this restaurant")
    
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
    reviews = []
    with db.engine.begin() as conn:
        revs = conn.execute(
            sqlalchemy.text("""SELECT user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review 
                                FROM reviews
                                WHERE restaurant_id = :restaurant_id
                            """), {"restaurant_id" : restaurant_id}
                            )
        for review in revs:
            reviews.append(Review(
            user_id=review.user_id,
            restaurant_id=review.restaurant_id,
            cuisine_id=review.cuisine_id,
            overall=review.overall_rating,
            food=review.food_rating,
            service=review.service_rating,
            price=review.price_rating,
            cleanliness=review.cleanliness_rating,
            note=review.written_review
            ))

    return reviews

@router.patch("/reviews/delete/{restaurant_id}/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_review(restaurant_id:int, user_id:int ):
    try:
        with db.engine.begin() as conn:
            conn.execute(
                        sqlalchemy.text(""" 
                                        DELETE FROM reviews 
                                        WHERE restaurant_id = :restaurant_id AND user_id = :user_id
                                """), {
                                        "restaurant_id": restaurant_id,
                                        "user_id": user_id
                                    }
                        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code = 409, detail = "Review does not exitst ")
    
