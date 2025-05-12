from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.api import auth
import sqlalchemy
from src import database as db
from datetime import datetime

router = APIRouter(prefix="/restaurants",
                  tags=["restaurants"],
                   dependencies=[Depends(auth.get_api_key)])


class Restaurant(BaseModel):
    name: str
    cuisine_id: int
    address: str
    city: str
    state: str
    zipcode: str
    phone: str
    last_updated_by: int
    last_updated_at: datetime

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine_id: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    phone: Optional[str] = None
    last_updated_by: int
    last_updated_at: datetime


@router.post("/restaurants", response_model = Restaurant)
def create_restaurant(restaurant: Restaurant):
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
                        "last_updated_at": restaurant.last_updated_at
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
        last_updated_at = restaurant.last_updated_at
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