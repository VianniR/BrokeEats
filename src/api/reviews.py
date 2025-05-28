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
    overall: float
    food: Optional[float] = None
    service: Optional[float] = None
    price: Optional[float] = None
    cleanliness: Optional[float] = None
    note: Optional[str] = Field(None, example = "Great Place")


# ReviewUpdate schema for PATCH endpoint
class ReviewUpdate(BaseModel):
    overall: Optional[float] = Field(None, example=4.5)
    food: Optional[float] = Field(None, example=4.0)
    service: Optional[float] = Field(None, example=5.0)
    price: Optional[float] = Field(None, example=3.5)
    cleanliness: Optional[float] = Field(None, example=4.0)
    note: Optional[str] = Field(None, example='')

class filteredReview(BaseModel):
    restaurant_id: Optional[int] = None
    user_id: Optional[int] = None
    cuisine_id: Optional[int] = None
    overall_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    food_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    service_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    price_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    cleanliness_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    

class RecsReview(BaseModel):
    restaurant_id: int
    user_id: int
    cuisine_id: int
    overall_rating: Optional[float]
    food_rating: Optional[float]
    service_rating: Optional[float]
    price_rating: Optional[float]
    cleanliness_rating: Optional[float]
    written_review: Optional[str]
    

@router.post("/reviews", response_model = Review)
def create_review(review : Review):
    try:
        with db.engine.begin() as conn:
            rev = conn.execute(sqlalchemy.text("""
            INSERT INTO reviews (user_id, restaurant_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review )
            VALUES (:user, :restaurant,:overall, :food, :service, :price, :cleanliness, :written)
            RETURNING id;                                   
            """), 
                 {
                      "user": review.user_id,
                      "restaurant": review.restaurant_id,
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
            sqlalchemy.text("""SELECT user_id, restaurant_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review 
                                FROM reviews
                                WHERE restaurant_id = :restaurant_id
                            """), {"restaurant_id" : restaurant_id}
                            )
        for review in revs:
            reviews.append(Review(
            user_id=review.user_id,
            restaurant_id=review.restaurant_id,
            overall=review.overall_rating,
            food=review.food_rating,
            service=review.service_rating,
            price=review.price_rating,
            cleanliness=review.cleanliness_rating,
            note=review.written_review
            ))

    return reviews

@router.delete("/reviews/delete/{restaurant_id}/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
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


# PATCH endpoint for updating a review
@router.patch("/{restaurant_id}/{user_id}", response_model=Review)
def update_review(restaurant_id: int, user_id: int, payload: ReviewUpdate):
    """Updates any provided fields of a review."""
    updates = payload.model_dump(exclude_unset=True)
    updates = {k: v for k, v in updates.items() if not (isinstance(v, str) and v.strip() == "")}
    
    # Map payload fields to actual DB column names
    column_map = {
        "overall": "overall_rating",
        "food": "food_rating",
        "service": "service_rating",
        "price": "price_rating",
        "cleanliness": "cleanliness_rating",
        "note": "written_review"
    }
    
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    
    set_clauses = ", ".join(f"{column_map[field]} = :{field}" for field in updates.keys())
    params = {**updates, "restaurant_id": restaurant_id, "user_id": user_id}
    try:
        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.text(
                    f"UPDATE reviews SET {set_clauses} WHERE restaurant_id = :restaurant_id AND user_id = :user_id"
                ),
                params
            )
            row = conn.execute(
                sqlalchemy.text(
                    """
                    SELECT user_id, restaurant_id, overall_rating, food_rating, service_rating,
                           price_rating, cleanliness_rating, written_review
                    FROM reviews
                    WHERE restaurant_id = :restaurant_id AND user_id = :user_id
                    """
                ),
                {"restaurant_id": restaurant_id, "user_id": user_id}
            ).one()
        return Review(
            user_id=row.user_id,
            restaurant_id=row.restaurant_id,
            overall=row.overall_rating,
            food=row.food_rating,
            service=row.service_rating,
            price=row.price_rating,
            cleanliness=row.cleanliness_rating,
            note=row.written_review
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Error updating review")
    
@router.post("/filter/", response_model = List[RecsReview])
def filter_review(payload: filteredReview, limit: int = 25):

    conditions = payload.model_dump(exclude_unset = True)
    conditions = {k: v for k, v in conditions.items() if not (isinstance(v, str) and v.strip() == "")}

    column_map = {
        "restaurant_id": "restaurant_id",
        "user_id": "user_id",
        "cuisine_id": "cuisine_id",
        "overall_rating": "overall_rating",
        "food_rating": "food_rating",
        "service_rating": "service_rating",
        "price_rating": "price_rating",
        "cleanliness_rating": "cleanliness_rating",
        
}
    where_clauses = []
    for field, value in conditions.items():
        if field in column_map:
            where_clauses.append(f"{column_map[field]} >= :{field}")
    if not where_clauses:
        raise HTTPException(status_code=404, detail="No filters found")
    
    where_SQL = " AND ".join(where_clauses)
    params = {**conditions, "limit": limit}

    filtered: List[RecsReview] = []

    with db.engine.begin() as conn:
        filters = conn.execute(sqlalchemy.text(f"""
                SELECT  restaurants.id,
                        users.id,
                        cuisines.id,
                        overall_rating,
                        food_rating,
                        service_rating,
                        price_rating,
                        cleanliness_rating,
                        written_review
                FROM reviews
                JOIN restaurants ON restaurants.id = reviews.restaurant_id
                JOIN users ON users.id = reviews.user_id
                JOIN cuisines ON cuisines.id = restaurants.cuisine_id
                WHERE {where_SQL}
                ORDER BY overall_rating DESC, price_rating DESC, food_rating DESC
                limit :limit                               
            """),
                params
            )
        for f in filters:
            filtered.append(RecsReview(**f._mapping))

    return filtered
