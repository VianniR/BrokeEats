from src import database as db
from src.api import auth
from fastapi import APIRouter, Depends, status

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Tuple
from src.api import auth
from src import database as db
import sqlalchemy
from fastapi import HTTPException


router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(auth.get_api_key)],
)


class Profile():
    id: int
    name: str
    username: str
    email: str
    permissions: int

@router.get("/profiles/{id}", response_model=Profile())
def get_profile():
    """gets a user's name and when they joined"""
    with db.engine.begin() as connection:
        user = connection.execute(
            sqlalchemy.text(
                "SELECT id, name, username, email, permissions FROM users WHERE users.id = :user_id"
            ),
            {"user_id": id}
        ).one()

    return user