from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.api import auth
import sqlalchemy
from src import database as db
from datetime import datetime
from src.api.users import RestaurantRecommendation


from src.api.users import RestaurantRecommendation


router = APIRouter(prefix="/restaurants",
                  tags=["restaurants"],
                   dependencies=[Depends(auth.get_api_key)])


class Restaurant(BaseModel):
    name: str = Field(..., min_length=1, description="Restaurant name must be at least 1 character")
    cuisine_id: int = Field(..., gt=0)
    address: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    zipcode: str = Field(..., pattern=r"^\d{5}$", description="5-digit ZIP Code")
    phone: str
    last_updated_by: Optional[int] = Field(None, gt=0)
    last_updated_at: datetime

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    cuisine_id: Optional[int] = Field(None, gt=0)
    address: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, min_length=1)
    state: Optional[str] = Field(None, min_length=1)
    zipcode: Optional[str] = Field(None, pattern=r"^\d{5}$", description="5-digit ZIP Code")
    phone: Optional[str] = None
    last_updated_by: int = Field(None, gt=0)

class RestaurantCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Restaurant name must be at least 1 character")
    cuisine_id: int = Field(..., gt=0)
    address: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    zipcode: str = Field(..., pattern=r"^\d{5}$", description="5-digit ZIP Code")
    phone: str
    last_updated_by: int

class RestaurantFilter(BaseModel):
    city: str
    state: str
    overall_rating: Optional[float] = Field(default=0, ge=0.0, le= 5.0)
    food_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    service_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    price_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    cleanliness_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    cuisine_name: Optional[str] = Field(None, example = '')

@router.get("/", response_model=List[Restaurant])
def get_all_restaurants():
    try:
        with db.engine.begin() as conn:
            rows = conn.execute(sqlalchemy.text(
                """
                SELECT id, name, cuisine_id, address, city, state, zipcode, phone, last_updated_by, last_updated_at
                FROM restaurants
                ORDER BY id
                """
            )).fetchall()

        return [
            {   
                "id": r.id,
                "name": r.name,
                "cuisine_id": r.cuisine_id,
                "address": r.address,
                "city": r.city,
                "state": r.state,
                "zipcode": r.zipcode,
                "phone": r.phone,
                "last_updated_by": r.last_updated_by,
                "last_updated_at": r.last_updated_at,
            }
            for r in rows
        ]
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code = 400, detail = "Error getting restaurants")
    
@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int):
    with db.engine.begin() as conn:
        r = conn.execute(sqlalchemy.text(
            """
            SELECT id, name, cuisine_id, address, city, state, zipcode, phone, last_updated_by, last_updated_at
            FROM restaurants
            WHERE id = :restaurant_id
            
            """
        ), {
            "restaurant_id": restaurant_id
            }
        ).fetchone()

    if r is None:
        raise HTTPException(status_code = 404, detail = "Restaurant does not exist")

    return { 
            "name": r.name,
            "cuisine_id": r.cuisine_id,
            "address": r.address,
            "city": r.city,
            "state": r.state,
            "zipcode": r.zipcode,
            "phone": r.phone,
            "last_updated_by": r.last_updated_by,
            "last_updated_at": r.last_updated_at,
        }

    

class RestaurantFilter(BaseModel):
    city: str
    state: str
    overall_rating: Optional[float] = Field(default=0, ge=0.0, le= 5.0)
    food_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    service_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    price_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    cleanliness_rating: Optional[float] = Field(default=None, ge=0.0, le= 5.0)
    cuisine_name: Optional[str] = Field(None, example = '')



@router.post("/", response_model = Restaurant)
def create_restaurant(restaurant: RestaurantCreate):
    now = datetime.now()
    try:
        with db.engine.begin() as conn:
            res = conn.execute(sqlalchemy.text(
                """
                INSERT INTO restaurants (name, cuisine_id, address, city, state, zipcode, phone, last_updated_by, last_updated_at)
                VALUES (:name, :cuisine_id, :address, :city, :state, :zipcode, :phone, :last_updated_by, :last_updated_at)
                RETURNING id;
                """),
                    {
                        "name": restaurant.name,
                        "cuisine_id": restaurant.cuisine_id,
                        "address": restaurant.address,
                        "city": restaurant.city,
                        "state": restaurant.state,
                        "zipcode": restaurant.zipcode,
                        "phone": restaurant.phone,
                        "last_updated_by": restaurant.last_updated_by,
                        "last_updated_at": now
                    }
                ).scalar()
            
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code = 409, detail = "Restaurant with these details have already been defined")
    
    return Restaurant(
        name = restaurant.name,
        cuisine_id = restaurant.cuisine_id,
        address = restaurant.address,
        city = restaurant.city,
        state = restaurant.state,
        zipcode = restaurant.zipcode,
        phone = restaurant.phone,
        last_updated_by = restaurant.last_updated_by,
        last_updated_at = now
    )

@router.patch("/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: int, payload: RestaurantUpdate):
    updates = payload.model_dump(exclude_unset=True)
    updates = {k: v for k, v in updates.items() if not (isinstance(v, str) and v.strip() == "")}

    column_map = {
        "name": "name",
        "cuisine_id": "cuisine_id",
        "address": "address",
        "city": "city",
        "state": "state",
        "zipcode": "zipcode",
        "phone": "phone",
        "last_updated_by": "last_updated_by",
        "last_updated_at": "last_updated_at",
    }

    
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    
    updates["last_updated_at"] = datetime.now()
    
    set_clauses = ", ".join(f"{column_map[field]} = :{field}" for field in updates.keys())
    params = {**updates, "id": restaurant_id}
    try:
        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.text(
                    f"UPDATE restaurants SET {set_clauses} WHERE id = :id"
                ),
                params
            )
            row = conn.execute(
                sqlalchemy.text(
                    """
                    SELECT name, cuisine_id, address, city, state, zipcode, phone, last_updated_by, last_updated_at
                    FROM restaurants
                    WHERE id = :id
                    """
                ),
                {"id": restaurant_id}
            ).one()

        return Restaurant(
            name=row.name,
            cuisine_id=row.cuisine_id,
            address=row.address,
            city=row.city,
            state=row.state,
            zipcode=row.zipcode,
            phone=row.phone,
            last_updated_by=row.last_updated_by,
            last_updated_at=row.last_updated_at
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail = "Error updating restaurant")
    


@router.delete("/{restaurant_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int):
    try:
        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.text("""
                                DELETE FROM restaurants
                                WHERE id = :id
                            """),
                              {
                                "id": restaurant_id
                            }
            )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code = 404, detail = "Restaurant does not exist")
        
@router.post("/filter", response_model=List[RestaurantRecommendation])
def filter_restaurants(payload: RestaurantFilter, limit: int = 100):
    restaurant_reccs: List[RestaurantRecommendation] = []

    updates = payload.model_dump(exclude_unset=True)
    updates = {k: v for k, v in updates.items() if not (isinstance(v, str) and v.strip() == "")}

    # Map payload fields to actual DB column names
    column_map = {
        "city": "restaurants.city",
        "state": "restaurants.state",
        "cuisine_name": "cuisines.name",

    }
    avg_column_map = {
        "overall_rating": "COALESCE(AVG(reviews.overall_rating), 0)",
        "price_rating": "COALESCE(AVG(reviews.overall_rating), 0)",
        "cleanliness_rating": "COALESCE(AVG(reviews.overall_rating), 0)",
        "food_rating": "COALESCE(AVG(reviews.overall_rating), 0)",
        "service_rating": "COALESCE(AVG(reviews.overall_rating), 0)",
    }



    set_clauses = []
    having_clauses = []
    for field, value in updates.items():
        if field in avg_column_map:
            having_clauses.append(f"{avg_column_map[field]} >= :{field}")
        elif field in column_map:
            set_clauses.append(f"{column_map[field]} = :{field}")

    if not set_clauses and not having_clauses:
        raise HTTPException(status_code=404, detail="No filters found")
    where_sql = " AND ".join(set_clauses) or "TRUE"
    having_sql = " AND ".join(having_clauses)
    params = {**updates, "limit": limit}

    with db.engine.connect() as conn:
        row = conn.execute(sqlalchemy.text(f"""
        SELECT restaurants.id as id, 
        restaurants.name as name, 
        cuisines.name as cuisine, 
        restaurants.address as address, 
        restaurants.city as city, 
        restaurants.state as state, 
        restaurants.zipcode as zipcode, 
        restaurants.phone as phone, 
        COALESCE(AVG(reviews.overall_rating), 0) AS overall_score,
        COALESCE(AVG(reviews.food_rating), 0) AS food_rating,
        COALESCE(AVG(reviews.service_rating), 0) AS service_rating,
        COALESCE(AVG(reviews.price_rating), 0) AS price_rating,
        COALESCE(AVG(reviews.cleanliness_rating), 0) AS cleanliness_rating
        FROM restaurants
        JOIN cuisines ON cuisines.id = restaurants.cuisine_id
        left join reviews ON reviews.restaurant_id = restaurants.id
        WHERE {where_sql}
        GROUP BY restaurants.id, restaurants.name,cuisines.name, restaurants.city, restaurants.state, restaurants.zipcode, restaurants.phone, restaurants.address
        {f'HAVING {having_sql}' if having_sql else ''}
        ORDER BY overall_score DESC, price_rating DESC
        limit :limit
        """),
                                   params)

        for r in row:
            restaurant_reccs.append(RestaurantRecommendation(**r._mapping))

    return restaurant_reccs