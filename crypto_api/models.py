from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
            if not ObjectId.is_valid(v):
                raise ValueError('Invalid ObjectId')
            return ObjectId(v)
    

class CryptoCurrencyModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    coin_id: int
    name: str
    symbol: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }