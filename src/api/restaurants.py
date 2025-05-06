from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(prefix="/restaurants",
                  tags=["restaurants"],
                   dependencies=[Depends(auth.get_api_key)])