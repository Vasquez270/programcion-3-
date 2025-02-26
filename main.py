from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Pet(BaseModel):
    id_pet: int
    name: str
    age: int


pets_db = {}

@app.post("/pets/", response_model=Pet)
async def create_pet(pet: Pet):
    if pet.id_pet in pets_db:
        raise HTTPException(status_code=400, detail="Pet ID already exists")
    pets_db[pet.id_pet] = pet
    return pet


@app.get("/pets/", response_model=List[Pet])
async def list_pets():
    return list(pets_db.values())


@app.get("/pets/{pet_id}/", response_model=Pet)
async def get_pet(pet_id: int):
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pets_db[pet_id]


@app.put("/pets/{pet_id}/", response_model=Pet)
async def update_pet(pet_id: int, pet: Pet):
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found")
    pets_db[pet_id] = pet
    return pet


@app.delete("/pets/{pet_id}/")
async def delete_pet(pet_id: int):
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found")
    del pets_db[pet_id]
    return {"message": "Pet deleted successfully"}


@app.get("/pets/{pet_id}/age_percentage/")
async def age_percentage(pet_id: int):
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet = pets_db[pet_id]
    percentage = (pet.age / 15) * 100
    return {"pet_id": pet.id_pet, "name": pet.name, "age_percentage": percentage}


@app.get("/")
async def root():
    return {"message": "Welcome to the Pet API!"}
