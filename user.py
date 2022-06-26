import base64
import secrets
from typing import List, Optional
from numpy import byte
from pydantic import BaseModel, Field
from objectid import PydanticObjectId
import pydantic
import fastapi
from fastapi.encoders import jsonable_encoder
import bson

class User(BaseModel):
    ID: Optional[PydanticObjectId] = Field(None, alias="_id")
    username: str
    password: str
    role: int
    id_int: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        return data
