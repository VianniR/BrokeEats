from fastapi import FastAPI

description = """
BrokeEats, suggestions by broke college students for broke college students.
"""
app = FastAPI(
  title = "BrokeEats",
  description = description,
  version = "0.0.1")

@app.get("/")
async def root():
    return {"message": "BrokeEats online"}
