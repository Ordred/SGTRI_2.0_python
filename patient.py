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

class Patient(BaseModel):
    ID: Optional[PydanticObjectId] = Field(None, alias="_id")
    id_int: int
    gender: str
    name: str
    description: str
    age: int
    degree: int
    glasgow: int
    pupilles: str
    tas: List[int]
    tad: List[int]
    spo2: float
    peak_flowMin: float
    peak_flowCM: float
    glycemie: float
    frequenceRespiratoire: float
    cetonemie: float
    douleurs: int
    pulse: int
    temperature: float
    motifs: List
    questions: List

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        return data
