from typing import List

import sqlalchemy
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from src import database as db
from src.api import auth

router = APIRouter(prefix="/cuisines",
                   tags=["cuisines"],
                   dependencies=[Depends(auth.get_api_key)])


class NewCuisine(BaseModel):
    name: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z]+$", example='')


class Cuisine(BaseModel):
    id: int
    name: str



@router.post("/", response_model=Cuisine)
def create_cuisine(cuisine: NewCuisine) -> Cuisine:
    try:
        with db.engine.begin() as conn:
            cuisine_id = conn.execute(sqlalchemy.text("""
            INSERT INTO cuisines (name)
            VALUES (LOWER(:name))
            RETURNING id;
            """), [
                {
                    "name": cuisine.name,
                }
            ]).scalar()
    except sqlalchemy.exc.IntegrityError:
        with db.engine.connect() as conn:
            cuisine_id = conn.execute(sqlalchemy.text("""
            SELECT id FROM cuisines WHERE LOWER(name) = LOWER(:name)"""), [
                {
                    "name": cuisine.name,
                }
            ]).scalar_one()
    return Cuisine(id=cuisine_id, name=cuisine.name)

@router.get("/", response_model=List[Cuisine])
def get_cuisines() -> List[Cuisine]:
    cuisine_list = []
    with db.engine.connect() as conn:
        row = conn.execute(
            sqlalchemy.text("""
            SELECT id, name
            FROM cuisines
            ORDER BY id DESC
            """)
        )
        for pref_id, name in row:
            cuisine_list.append(Cuisine(id=pref_id, name=name))

    return cuisine_list
