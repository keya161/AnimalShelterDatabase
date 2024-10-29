from pydantic import BaseModel
from datetime import date

class AnimalCreate(BaseModel):
    name: str
    DOB: date
    gender: str
    passive_adopter: str 
    breed_id: str

class Animal(AnimalCreate):
    animal_ID: str

    class Config:
        from_attributes = True  # Update this line
