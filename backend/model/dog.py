from pydantic import BaseModel, Field
from .object import PyObjectId
from bson import ObjectId


class DogModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    age: int = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Marcel",
                "age": 3,
            }
        }


class UpdateDogModel(BaseModel):
    name: str = Field(...)
    age: int = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Marcel",
                "age": 3,
            }
        }
