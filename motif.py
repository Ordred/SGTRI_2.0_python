import secrets
from typing import List, Optional
from pydantic import BaseModel, Field
from objectid import PydanticObjectId
import pydantic
import fastapi
from fastapi.encoders import jsonable_encoder

class Motif(BaseModel):
    ID: Optional[PydanticObjectId] = Field(None, alias="_id")
    id_int: int
    category: str
    degrees: List[str]
    glasgow: bool
    pupilles: bool
    pouls: bool
    tah: bool
    index_de_choc: bool
    fr: bool
    spo2: bool
    peak_flow: bool
    t_c: bool
    glyceme: bool
    acetonurie: bool
    douleurs: bool
    cyanose: bool
    conditions: List

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        return data