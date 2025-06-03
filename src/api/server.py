from fastapi import FastAPI

from src.api import restaurants, preferences, users, reviews, cuisines

description = """
BrokeEats, suggestions by broke college students for broke college students.
"""

tags_metadata = [
        {"name": "restaurants", "description": "View restaurants"},
        {"name": "users", "description": "User profiles" },
        {"name": "reviews", "description": "Restaurant reviews"}
]

app = FastAPI(
  title = "BrokeEats",
  description = description,
  version = "0.0.1",
  contact = {
      "name": "Josh, Rafael, Uriel, Vianni"
  }, 
  openapi_tags = tags_metadata,
  )


app.include_router(restaurants.router)
app.include_router(preferences.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(cuisines.router)

@app.get("/")
async def root():
    return {"message": "BrokeEats online"}
