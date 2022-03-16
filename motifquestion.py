import secrets
from typing import List, Optional
from pydantic import BaseModel, Field
from objectid import PydanticObjectId
import pydantic
import fastapi
from fastapi.encoders import jsonable_encoder

class MotifQuestion(BaseModel):
    ID: Optional[PydanticObjectId] = Field(None, alias="_id")
    id: str
    idMotif: int
    questions: List[str]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data