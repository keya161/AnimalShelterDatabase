from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from app.models import RoleEnum
# -------------------------
# Animal Schemas
# -------------------------

class AnimalCreate(BaseModel):
    name: str
    dob: date
    gender: str  # Use "M" or "F"
    passive_adopter: bool
    breed_id: str

class AnimalResponse(AnimalCreate):  # Inherit from AnimalCreate
    animal_id: str  # Corrected to match the database model

    class Config:
        from_attributes = True
class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    passive_adopter: Optional[bool] = None
    breed_id: Optional[str] = None

class AnimalResponse(BaseModel):
    animal_id: str
    name: str
    dob: date
    gender: str
    passive_adopter: bool
    breed_id: str

    class Config:
        from_attributes = True
 
# -------------------------
# Get All details about an animal including reports and adopter
# -------------------------
class AdopterGet(BaseModel):
    adopter_id: str
    name: str
    contribution: float
class MedicalRecordBase(BaseModel):
    record_id: str  # animal_id should be str since it is CHAR(5)
    report: str
    doctor: str
    date: str  # Ensure date is a string in ISO format
    diagnosis: str
    medicine: str
    follow_up: str  # Should also be a string in ISO format
    freq_of_usage: int

class AnimalDetail(BaseModel):
    animal_id: str  # This should match the type in your Animal model
    name: str
    breed: str  # Ensure breed is a string
    passive_adopter: Optional[List[AdopterGet]]  # If it's a string, use Optional
    medical_records: List[MedicalRecordBase]  # List of medical record
        
# -------------------------
# Medical Record Schemas
# -------------------------

class MedicalRecordCreate(BaseModel):
    animal_id: str
    name: str
    report: Optional[str] = None
    doctor: str
    date: date
    diagnosis: str
    medicine: str
    follow_up: Optional[date] = None
    freq_of_usage: Optional[int] = None

    class Config:
        from_attributes = True

class MedicalRecordResponse(MedicalRecordCreate):
    record_id: str

    class Config:
        from_attributes = True
# -------------------------
# Employee Schemas
# -------------------------

class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    date_of_joining: date
    role: RoleEnum

class Employee(EmployeeCreate):
    class Config:
        from_attributes = True
        
class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    date_of_joining: date
    role: RoleEnum
    class Config:
        from_attributes = True

#Type

# Schema for creating a new Type record
class TypeCreate(BaseModel):
    type_id: str
    breed: str
    feed_id: int  # Updated to reference feed_id directly
    freq_of_checkup: int
    bath: Optional[date]

# Schema for updating a Type record
class TypeUpdate(BaseModel):
    breed: Optional[str]
    feed_id: Optional[int]  # Updated to reference feed_id directly
    freq_of_checkup: Optional[int]
    bath: Optional[date]

# Schema for response
class TypeResponse(BaseModel):
    type_id: str
    breed: str
    feed_id: int  # Reflects the direct foreign key reference
    freq_of_checkup: int
    bath: Optional[date]

    class Config:
        from_attributes = True
        

#Dropdowns

# Schema for the dropdown response
class BreedDropdownResponse(BaseModel):
    type_id: str
    breed: str

    class Config:
        from_attributes = True 
        
class RegisterRequest(BaseModel):
    employee_id: str
    username: str
    password: str    
    
#food
# Base schema for food inventory
class FoodInventoryBase(BaseModel):
    type: str
    stock: int
    cost_per_kg: float

# Schema for creating food inventory
class FoodInventoryCreate(FoodInventoryBase):
    pass

# Schema for updating food inventory
class FoodInventoryUpdate(BaseModel):
    stock: Optional[int] = None  # Only stock is required in the update

# Schema for the database model
class FoodInventoryInDB(FoodInventoryBase):
    food_id: int  # Use integer instead of string for food_id
    
    class Config:
        from_attributes = True

class MedicineInventoryBase(BaseModel):
    name: str
    stock: int
    expiry: date
    date_of_buying: date

class MedicineInventoryCreate(MedicineInventoryBase):
    pass  # Same as MedicineInventoryBase for create

class MedicineInventoryUpdate(BaseModel):
    # name: Optional[str]
    stock: Optional[int]
    # expiry: Optional[date]
    # date_of_buying: Optional[date]

class MedicineInventoryInDB(MedicineInventoryBase):
    medicine_id: str  # Include the medicine ID for DB responses

    class Config:
        from_attributes = True
        
class AdopterCreate(BaseModel):
    # adopter_id: str = Field(..., max_length=5)
    name: str
    animal_id: str
    contribution: float

# Schema for updating an adopter
class AdopterUpdate(BaseModel):
    name: Optional[str]
    contribution: Optional[float]

# Schema for reading adopter details
class AdopterBase(BaseModel):
    adopter_id: str
    name: str
    animal_id: str
    contribution: float

    class Config:
        from_attributes = True
        
        
# Nested query -> get all animals who dont have medical records
class AnimalNameResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True
        
