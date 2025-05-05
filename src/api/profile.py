from src import database as db
from src.api import auth
from fastapi import APIRouter, Depends, status
from typing import List, Optional
from pydantic import BaseModel, Field
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

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Bob Smith")
    username: Optional[str] = Field(None, example="new_username")
    email: Optional[str] = Field(None, example="bob@example.com")

@router.get("/profile/{id}", response_model=Profile)
def get_profile():
    """Gets a user's name and when they joined"""
    with db.engine.begin() as connection:
        user = connection.execute(
            sqlalchemy.text(
                "SELECT id, name, username, email, permissions FROM users WHERE users.id = :user_id"
            ),
            {"user_id": id}
        ).one()
    return user


# PATCH endpoint to update username
@router.patch("profile/{id}", response_model=Profile)
def update_profile(id: int, payload: ProfileUpdate):
    """Updates any provided user fields."""
    updates = payload.dict(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    set_clauses = ", ".join(f"{field} = :{field}" for field in updates.keys())
    params = {**updates, "user_id": id}
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(f"UPDATE users SET {set_clauses} WHERE id = :user_id"),
            params
        )
        user = connection.execute(
            sqlalchemy.text(
                "SELECT id, name, username, email FROM users WHERE id = :user_id"
            ),
            {"user_id": id}
        ).one()
    return user