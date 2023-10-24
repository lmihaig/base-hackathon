from model.dog import DogModel, UpdateDogModel
import os
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client["shelter"]
collection = db["dogs"]

router = APIRouter()


@router.post("/", response_description="Add new dog", response_model=DogModel)
async def create_dog(dog: DogModel = Body(...)):
    dog = jsonable_encoder(dog)
    new_dog = await collection.insert_one(dog)
    created_dog = await collection.find_one({"_id": new_dog.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_dog)


@router.get("/", response_description="List all dogs", response_model=List[DogModel])
async def list_dogs():
    dogs = await collection.find().to_list(1000)
    return dogs


@router.get("/{id}", response_description="Get a single dog", response_model=DogModel)
async def show_dog(id: str):
    if (dog := await collection.find_one({"_id": id})) is not None:
        return dog

    raise HTTPException(status_code=404, detail=f"Dog {id} not found")


@router.put("/{id}", response_description="Update a dog", response_model=DogModel)
async def update_dog(id: str, dog: UpdateDogModel = Body(...)):
    dog = {k: v for k, v in dog.dict().items() if v is not None}

    if len(dog) >= 1:
        update_result = await collection.update_one({"_id": id}, {"$set": dog})

        if update_result.modified_count == 1:
            if (updated_dog := await collection.find_one({"_id": id})) is not None:
                return updated_dog

    if (existing_dog := await collection.find_one({"_id": id})) is not None:
        return existing_dog

    raise HTTPException(status_code=404, detail=f"Dog {id} not found")


@router.delete("/{id}", response_description="Delete a dog")
async def delete_dog(id: str):
    delete_result = await collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Dog {id} not found")
