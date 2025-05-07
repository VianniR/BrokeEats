from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.api import auth
import sqlalchemy
from src import database as db

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
    name: str
    username: str
    email: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Bob Smith")
    username: Optional[str] = Field(None, example="new_username")
    email: Optional[str] = Field(None, example="bob@example.com")

@router.post("/profile", response_model=Profile)
def create_profile(profile: NewUser) -> Profile:
    try:
        with db.engine.begin() as conn:
            user_id = conn.execute(sqlalchemy.text("""
            INSERT INTO users (name, username, email, permissions)
            VALUES (:name, :username, :email, 1)
            RETURNING id
            """),[
                {
                    "name": profile.name,
                    "username": profile.username,
                    "email": profile.email,
                }
            ]).scalar_one()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    return Profile(id=user_id, name=profile.name, username=profile.username, email=profile.email, permissions=1)



@router.get("/profile/{id}", response_model=Profile)
def get_profile(user_id: int):


    try:
        with db.engine.begin() as connection:
            user = connection.execute(
                sqlalchemy.text(
                    "SELECT id, name, username, email, permissions FROM users WHERE users.id = :user_id"
                ),
                {"user_id": user_id}
            ).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# PATCH endpoint to update username
@router.patch("profile/{id}", response_model=Profile)
def update_profile(user_id: int, payload: ProfileUpdate):
    """Updates any provided user fields."""
    updates = payload.dict(exclude_unset=True)

    updates = {k: v for k, v in updates.items() if not (isinstance(v, str) and v.strip() == "")}

    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    set_clauses = ", ".join(f"{field} = :{field}" for field in updates.keys())
    params = {**updates, "user_id": user_id}
    try:
        with db.engine.begin() as connection:
            connection.execute(
                    sqlalchemy.text(f"UPDATE users SET {set_clauses} WHERE id = :user_id"),
                    params
                )
            user = connection.execute(
                sqlalchemy.text(
                    "SELECT id, name, username, email, permissions FROM users WHERE id = :user_id"
                ),
                {"user_id": user_id}
            ).one()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    return user