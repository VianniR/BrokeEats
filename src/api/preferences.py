from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List
from src.api import auth
import sqlalchemy
from src import database as db



router = APIRouter(
    tags=["preferences"],
    dependencies=[Depends(auth.get_api_key)],
)


class NewPreference(BaseModel):
  name: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z]+$", example = '')

class Preferences(BaseModel):
    id: int
    name: str

@router.post("/preferences", response_model=Preferences)
def create_preferences(preferences: NewPreference):
    try:
        with db.engine.begin() as conn:
            pref_id = conn.execute(sqlalchemy.text("""
            INSERT INTO preferences (name)
            VALUES (LOWER(:name))
            RETURNING id;
            """), [
                {
                    "name": preferences.name,
                }
            ]).scalar()
    except sqlalchemy.exc.IntegrityError:
        with db.engine.connect() as conn:
            pref_id = conn.execute(sqlalchemy.text("""
            SELECT id FROM preferences WHERE LOWER(name) = LOWER(:name)"""),[
                {
                    "name": preferences.name,
                }
            ]).scalar_one()
    return Preferences(id=pref_id, name=preferences.name)



@router.get("/preferences", response_model=List[Preferences])
def get_preferences() -> List[Preferences]:

    pref_list: List[Preferences] = []

    with db.engine.connect() as conn:
        row = conn.execute(
            sqlalchemy.text("""
        SELECT id, name
        FROM preferences
        ORDER BY id DESC
        """)
        )
        for pref_id, name in row:
            pref_list.append(Preferences(id=pref_id, name=name))

    return pref_list


@router.post("/profiles/preferences/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_user_preference(preference_name: str, user_id: int):
    with db.engine.begin() as conn:
        name_found = conn.execute(
            sqlalchemy.text("""
        SELECT preferences.name
        from preferences
        WHERE LOWER(name) = LOWER(:name)
        """),
                {
                    "name": preference_name,
                },
        ).scalar_one_or_none()

        if name_found is None:
            raise HTTPException(status_code=404, detail="preference not found")

        id_found = conn.execute(
            sqlalchemy.text("""
        SELECT id
        FROM users
        where id = :id
        """),
                {
                    "id": user_id,
                },
        ).scalar_one_or_none()
        if id_found is None:
            raise HTTPException(status_code=404, detail="user does not exist")

        try:
            conn.execute(
                sqlalchemy.text("""
            INSERT INTO user_preferences (user_id, preference_id)
            SELECT :user_id, id 
            from preferences 
            WHERE LOWER(name) = LOWER(:name)
            """),
                {"user_id": user_id, "name": preference_name},
            )
        except sqlalchemy.exc.IntegrityError:
            # done already
            pass


@router.get("/profiles/preferences/{user_id}", response_model=List[Preferences])
def get_user_preferences(user_id: int) -> List[Preferences]:
    preferences: List[Preferences] = []
    with db.engine.begin() as conn:
        row = conn.execute(
            sqlalchemy.text("""
        SELECT preferences.id as preference_id, preferences.name as preference
        from preferences
        join user_preferences on preferences.id = user_preferences.preference_id
        where user_preferences.user_id = :user_id
        """),
                {
                    "user_id": user_id,
                },
        )
        for pref_id, name in row:
            preferences.append(Preferences(id=pref_id, name=name))

        return preferences



@router.post("/restaurants/preferences/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_restaurant_preference(restaurant_id: int, preference_name: str, user_id: int):
    with db.engine.begin() as conn:

        name_found = conn.execute(
            sqlalchemy.text("""
                SELECT preferences.name
                from preferences
                WHERE LOWER(name) = LOWER(:name)
                """),
                {
                    "name": preference_name,
                },
        ).scalar_one_or_none()
        if name_found is None:
            raise HTTPException(status_code=404, detail="preference not found")

        id_found = conn.execute(
            sqlalchemy.text("""
                SELECT id
                FROM users
                where id = :id
                """),
                {
                    "id": user_id,
                },
        ).scalar_one_or_none()

        if id_found is None:
            raise HTTPException(status_code=404, detail="user does not exist")

        id_found = conn.execute(
            sqlalchemy.text("""
                SELECT id
                FROM restaurants
                where id = :id
                """),
                {
                    "id": restaurant_id,
                },
        ).scalar_one_or_none()

        if id_found is None:
            raise HTTPException(status_code=404, detail="restaurant does not exist")


        try:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO restaurant_preferences (restaurant_id, preference_id, last_updated_by)
                    SELECT :restaurant_id, id, :user_id 
                    from preferences 
                    WHERE LOWER(name) = LOWER(:name)
                    """),
                    {
                        "restaurant_id": restaurant_id,
                        "name": preference_name,
                        "user_id": user_id,
                    },
            )
        except sqlalchemy.exc.IntegrityError:
            #already done
            pass


@router.get(
    "/restaurants/preferences/{restaurant_id}", response_model=List[Preferences]
)
def get_restaurant_preferences(restaurant_id: int) -> List[Preferences]:
    preferences: List[Preferences] = []
    with db.engine.begin() as conn:
        row = conn.execute(
            sqlalchemy.text("""
                SELECT preferences.id as preference_id, preferences.name as preference
                from preferences
                join restaurant_preferences on preferences.id = restaurant_preferences.preference_id
                where restaurant_preferences.restaurant_id = :restaurant_id
                """),
                {
                    "restaurant_id": restaurant_id,
                },
        )
        for pref_id, name in row:
            preferences.append(Preferences(id=pref_id, name=name))

        return preferences
