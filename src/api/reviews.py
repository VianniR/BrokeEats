from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.api import auth
import sqlalchemy
from src import database as db
from datetime import datetime

router = APIRouter(prefix="/reviews",
                  tags=["reviews"],
                   dependencies=[Depends(auth.get_api_key)])


class Review(BaseModel):
    user_id: int
    restaurant_id: int
    cuisine_id: int
    overall_rating: float = Field(ge = 0.0, le = 5.0)
    food_rating: Optional[float] = Field(None, ge = 0.0, le = 5.0)
    service_rating: Optional[float] = Field(None, ge = 0.0, le = 5.0)
    price_rating: Optional[float] = Field(None, ge = 0.0, le = 5.0)
    cleanliness_rating: Optional[float] = Field(None, ge = 0.0, le = 5.0)
    written_review: Optional[str] = Field(None, example = "Great Place")

class ReviewOut(Review):
    created_at: datetime

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
    cuisine_name: Optional[str] = None
    overall_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    food_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    service_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    price_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    cleanliness_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)

    

class RecsReview(BaseModel):
    restaurant_id: int
    user_id: int
    cuisine_name: str
    overall_rating: Optional[float]
    food_rating: Optional[float]
    service_rating: Optional[float]
    price_rating: Optional[float]
    cleanliness_rating: Optional[float]
    written_review: Optional[str]
    

@router.post("", response_model = ReviewOut)
def create_review(review : Review):
     
    
    with db.engine.begin() as conn:
        existing = conn.execute(
            sqlalchemy.text("""
                SELECT 1 FROM reviews 
                WHERE user_id = :user_id AND restaurant_id = :restaurant_id
            """),
            {"user_id": review.user_id, "restaurant_id": review.restaurant_id}
        ).fetchone()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Review from that user already exists for this restaurant"
            )
        
        rev = conn.execute(sqlalchemy.text("""
        INSERT INTO reviews (user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review)
        VALUES (:user, :restaurant, :cuisine_id, :overall, :food, :service, :price, :cleanliness, :written)
        RETURNING id, created_at                                  
        """), 
                {
                    "user": review.user_id,
                    "restaurant": review.restaurant_id,
                    "cuisine_id": review.cuisine_id,
                    "overall": review.overall_rating,
                    "food": review.food_rating,
                    "service": review.service_rating,
                    "price": review.price_rating,
                    "cleanliness": review.cleanliness_rating,
                    "written": review.written_review,
                }
        ).mappings().fetchone()
  
    return ReviewOut(**review.dict(), created_at = rev["created_at"])


@router.get("/{restaurant_id}", response_model = List[ReviewOut])
def get_reviews(restaurant_id: int):
    reviews = []
    with db.engine.begin() as conn:
        revs = conn.execute(
            sqlalchemy.text("""SELECT user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating, price_rating, cleanliness_rating, written_review, created_at
                                FROM reviews
                                WHERE restaurant_id = :restaurant_id
                            """), {"restaurant_id" : restaurant_id}
                            ).fetchall() 
    

    for review in revs:
        reviews.append(ReviewOut(
            user_id=review.user_id,
            restaurant_id=review.restaurant_id,
            cuisine_id = review.cuisine_id,
            overall_rating=review.overall_rating,
            food_rating=review.food_rating,
            service_rating=review.service_rating,
            price_rating=review.price_rating,
            cleanliness_rating=review.cleanliness_rating,
            written_review=review.written_review,
            created_at=review.created_at  
        ))

    return reviews

@router.delete("/delete/{restaurant_id}/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_review(restaurant_id:int, user_id:int ):
    
    with db.engine.begin() as conn:
        rev = conn.execute(
                    sqlalchemy.text(""" 
                                    DELETE FROM reviews 
                                    WHERE restaurant_id = :restaurant_id AND user_id = :user_id
                                    RETURNING id
                            """), {
                                    "restaurant_id": restaurant_id,
                                    "user_id": user_id
                                }
                    ).scalar_one_or_none()
    if rev is None:
        raise HTTPException(status_code = 404, detail = "Review does not exist ")


# PATCH endpoint for updating a review
@router.patch("/{restaurant_id}/{user_id}", response_model=ReviewOut)
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
                    SELECT user_id, restaurant_id, cuisine_id, overall_rating, food_rating, service_rating,
                           price_rating, cleanliness_rating, written_review, created_at
                    FROM reviews
                    WHERE restaurant_id = :restaurant_id AND user_id = :user_id
                    """
                ),
                {"restaurant_id": restaurant_id, "user_id": user_id}
            ).one()
        return ReviewOut(**row._mapping)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Error updating review")
    
@router.post("/filter/", response_model = List[RecsReview])
def filter_review(payload: filteredReview, limit: int = 25):

    conditions = {
    k: v for k, v in payload.model_dump(exclude_unset=True).items()
    if not (
        (isinstance(v, str) and v.strip() in ["", "string"]) or  
        (isinstance(v, (int, float)) and v == 0)
    )
}


    column_map = {
        "restaurant_id": "restaurant_id",
        "user_id": "user_id",
        "cuisine_name": "cuisines.name",
        "overall_rating": "overall_rating",
        "food_rating": "food_rating",
        "service_rating": "service_rating",
        "price_rating": "price_rating",
        "cleanliness_rating": "cleanliness_rating",
        
}
    where_clauses = []
    for field, value in conditions.items():
         if field in column_map:
            if field == "cuisine_name":
                where_clauses.append(f"{column_map[field]} ILIKE :{field}")
                conditions[field] = f"%{value}%"
            elif field in {"restaurant_id", "user_id"}:
                where_clauses.append(f"{column_map[field]} = :{field}")
            else:
                where_clauses.append(f"{column_map[field]} >= :{field}")
    if not where_clauses:
        raise HTTPException(status_code=404, detail="No filters found")
    
    where_SQL = " AND ".join(where_clauses)
    params = {**conditions, "limit": limit}

    filtered: List[RecsReview] = []

    with db.engine.begin() as conn:
        filters = conn.execute(sqlalchemy.text(f"""
                SELECT  restaurants.id AS restaurant_id,
                        users.id AS user_id,
                        cuisines.name AS cuisine_name,
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
    return [RecsReview(**f._mapping) for f in filters]

