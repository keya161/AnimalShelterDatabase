from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List, Optional
from . import models, schemas
from app.models import Animal, MedicalRecords, Employee, Adopter, Type, MedicineInventory
from app.schemas import AnimalCreate, EmployeeCreate, MedicalRecordCreate, AnimalDetail, MedicalRecordBase, AdopterGet, TypeCreate, TypeResponse, TypeUpdate, BreedDropdownResponse, AdopterCreate, AdopterUpdate, MedicineInventoryCreate, MedicalRecordResponse

#Animals
def create_animal(db: Session, animal: schemas.AnimalCreate):
    # Step 1: Get the last animal ID
    last_animal = db.query(models.Animal).order_by(models.Animal.animal_id.desc()).first()
    
    if last_animal:
        # Extract the numeric part and increment it
        last_id = int(last_animal.animal_id[2:])  # Extract number part from "ANXXX"
        new_id = f"AN{last_id + 1:03d}"  # Increment and format to "ANXXX"
    else:
        new_id = "AN001"  # Starting value if no records exist

    # Step 2: Create a new animal record with the new ID
    db_animal = models.Animal(
        animal_id=new_id,  # Use the dynamically generated ID
        name=animal.name,
        dob=animal.dob,
        gender=animal.gender,
        passive_adopter=animal.passive_adopter,
        breed_id=animal.breed_id  # This is the foreign key reference
    )
    
    # Step 3: Add and commit the new animal to the database
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)

    return db_animal

def get_animal(db: Session, animal_id: str):
    db_animal = db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal

def update_animal(db: Session, animal_id: str, animal_data: schemas.AnimalUpdate):
    db_animal = db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Update animal fields
    for key, value in animal_data.dict(exclude_unset=True).items():
        setattr(db_animal, key, value)
    
    db.commit()
    db.refresh(db_animal)
    return db_animal

def delete_animal(db: Session, animal_id: str):
    db_animal = db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    db.delete(db_animal)
    db.commit()
    return {"detail": "Animal deleted successfully"}

#get all details about an animal

def get_animal_by_name(name: str, db: Session):
    # Build a query with all necessary joins
    query = (
        db.query(
            Animal,
            Type.breed,
            MedicalRecords,
            Adopter
        )
        .outerjoin(Type, Animal.breed_id == Type.type_id)
        .outerjoin(MedicalRecords, Animal.animal_id == MedicalRecords.animal_id)
        .outerjoin(Adopter, Animal.animal_id == Adopter.animal_id)
        .filter(Animal.name == name)
    )
    
    # Execute the query
    results = query.all()
    
    # If no results found, raise 404
    if not results:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Since all rows will have the same animal details, we can take them from the first result
    first_row = results[0]
    animal = first_row.Animal
    breed = first_row.breed
    
    # Process medical records, avoiding duplicates
    medical_records_dict = {}
    for row in results:
        if row.MedicalRecords and row.MedicalRecords.record_id not in medical_records_dict:
            medical_records_dict[row.MedicalRecords.record_id] = MedicalRecordBase(
                record_id=row.MedicalRecords.record_id,
                report=row.MedicalRecords.report or "",
                doctor=row.MedicalRecords.doctor,
                date=row.MedicalRecords.date.isoformat(),
                diagnosis=row.MedicalRecords.diagnosis,
                medicine=row.MedicalRecords.medicine,
                follow_up=row.MedicalRecords.follow_up.isoformat(),
                freq_of_usage=row.MedicalRecords.freq_of_usage
            )
    
    # Process adopters, avoiding duplicates
    adopters_dict = {}
    for row in results:
        if row.Adopter and row.Adopter.adopter_id not in adopters_dict:
            adopters_dict[row.Adopter.adopter_id] = AdopterGet(
                adopter_id=row.Adopter.adopter_id,
                name=row.Adopter.name,
                contribution=row.Adopter.contribution              
            )
    
    return AnimalDetail(
        animal_id=animal.animal_id,
        name=animal.name,
        breed=breed,
        passive_adopter=list(adopters_dict.values()),
        medical_records=list(medical_records_dict.values())
    )
#medical records

def create_medical_record(db: Session, record: MedicalRecordCreate):
    # Step 1: Look up the animal by name to get its ID
    print(f"Searching for Animal with ID:{record.animal_id}")
    animal = db.query(Animal).filter(Animal.animal_id == record.animal_id).first()

    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Step 2: Get the last record ID
    last_record = db.query(MedicalRecords).order_by(MedicalRecords.record_id.desc()).first()

    if last_record:
        # Extract the numeric part and increment it
        last_id = int(last_record.record_id[2:])  # Extract number part from "MRXXX"
        new_record_id = f"MR{last_id + 1:03d}"  # Increment and format to "MRXXX"
    else:
        new_record_id = "MR001"  # Starting value if no records exist
    db_record = MedicalRecords(
        record_id=new_record_id,# Automatically generate record_id
        animal_id=record.animal_id,
        name=record.name,
        report=record.report,
        doctor=record.doctor,
        date=record.date,
        diagnosis=record.diagnosis,
        medicine=record.medicine,
        follow_up=record.follow_up,
        freq_of_usage=record.freq_of_usage,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_medical_records(db: Session, animal_id: Optional[str] = None) -> List[schemas.MedicalRecordResponse]:
    # Step 1: Query the MedicalRecords
    query = db.query(models.MedicalRecords)

    # Step 2: If animal_id is provided, filter records by the given animal_id
    if animal_id:
        query = query.filter(models.MedicalRecords.animal_id == animal_id)

    # Step 3: Fetch all medical records (filtered or all)
    medical_records = query.all()

    # Step 4: Check if any records were found
    if not medical_records:
        # If no records found, raise a 404 HTTP exception
        raise HTTPException(status_code=404, detail="No medical records found for the given animal_id")

    # Step 5: Return the records as a list of MedicalRecordResponse
    return [schemas.MedicalRecordResponse.from_orm(record) for record in medical_records]

#employees
def create_employee(db: Session, employee_data: EmployeeCreate):
    db_employee = Employee(
        employee_id=employee_data.employee_id,
        name=employee_data.name,
        date_of_joining=employee_data.date_of_joining,
        role=employee_data.role,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session, name: Optional[str]=None):
    query = db.query(models.Employee)

    # Step 2: Filter by animal_id if provided
    if name:
        query = query.filter(models.Employee.name == name)

    # Step 3: Fetch all medical records
    medical_records = query.all()

    # Step 4: Check if any records were found
    if not medical_records:
        raise HTTPException(status_code=404, detail="No employees found")

    # Step 5: Return the medical records as a list of MedicalRecordResponse
    return [schemas.EmployeeResponse.from_orm(record) for record in medical_records]

#Type

def create_type(db: Session, type_data: TypeCreate):
    db_type = Type(**type_data.dict())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def get_type(db: Session, type_id: str):
    type_record = db.query(Type).filter(Type.type_id == type_id).first()
    if not type_record:
        raise HTTPException(status_code=404, detail="Type not found")
    return type_record

def update_type(db: Session, type_id: str, type_data: TypeUpdate):
    type_record = db.query(Type).filter(Type.type_id == type_id).first()
    if not type_record:
        raise HTTPException(status_code=404, detail="Type not found")

    for key, value in type_data.dict(exclude_unset=True).items():
        setattr(type_record, key, value)

    db.commit()
    db.refresh(type_record)
    return type_record

def delete_type(db: Session, type_id: str):
    type_record = db.query(Type).filter(Type.type_id == type_id).first()
    if not type_record:
        raise HTTPException(status_code=404, detail="Type not found")

    db.delete(type_record)
    db.commit()
    return {"detail": "Type deleted successfully"}

#Drop downs
def get_breeds_from_db(db: Session):
    # Fetch all breeds from the database
    breeds = db.query(Type.type_id, Type.breed).all()
    if not breeds:
        raise HTTPException(status_code=404, detail="No breeds found")
    # Return the list of breeds in the correct format
    return [BreedDropdownResponse(type_id=breed[0], breed=breed[1]) for breed in breeds]

#food
def get_food_inventory(db: Session, food_id: int):
    return db.query(models.FoodInventory).filter(models.FoodInventory.food_id == food_id).first()

# Get a list of food inventory items with pagination (skip, limit)
def get_food_inventories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FoodInventory).offset(skip).limit(limit).all()

# Create a new food inventory item
def create_food_inventory(db: Session, food_inventory: schemas.FoodInventoryCreate):
    db_food_inventory = models.FoodInventory(**food_inventory.dict())
    db.add(db_food_inventory)
    db.commit()
    db.refresh(db_food_inventory)
    return db_food_inventory

# Update an existing food inventory item
def update_food_inventory(db: Session, food_id: int, stock: int):
    # Fetch the existing food inventory item by food_id
    db_food_inventory = db.query(models.FoodInventory).filter(models.FoodInventory.food_id == food_id).first()
    
    if db_food_inventory:
        # Update only the stock value, leaving other values unchanged
        db_food_inventory.stock = stock
        
        # Commit the change to the database
        db.commit()
        db.refresh(db_food_inventory)
        
        return db_food_inventory
    
    return None

# Delete a food inventory item by food_id
def delete_food_inventory(db: Session, food_id: int):
    db_food_inventory = db.query(models.FoodInventory).filter(models.FoodInventory.food_id == food_id).first()
    if db_food_inventory:
        db.delete(db_food_inventory)
        db.commit()
        return db_food_inventory
    return None

# adopters

def create_adopter(db: Session, adopter_data: AdopterCreate):
    # Step 1: Get the last adopter ID
    last_adopter = db.query(models.Adopter).order_by(models.Adopter.adopter_id.desc()).first()
    
    if last_adopter:
        # Extract the numeric part and increment it
        last_id = int(last_adopter.adopter_id[2:])  # Extract number part from "ADXXX"
        new_id = f"AD{last_id + 1:03d}"  # Increment and format to "ADXXX"
    else:
        new_id = "AD001"  # Starting value if no records exist

    # Step 2: Create a new adopter record with the new ID
    adopter = models.Adopter(
        adopter_id=new_id,  # Use the dynamically generated ID
        name=adopter_data.name,
        animal_id=adopter_data.animal_id,
        contribution=adopter_data.contribution
    )

    # Add the new adopter to the database
    db.add(adopter)
    db.commit()
    db.refresh(adopter)
    return adopter

# Get all adopters
def get_all_adopters(db: Session):
    return db.query(Adopter).all()

# Get adopter by ID
def get_adopter_by_id(db: Session, adopter_id: str):
    return db.query(Adopter).filter(Adopter.adopter_id == adopter_id).first()

# Update adopter
def update_adopter(db: Session, adopter_id: str, update_data: AdopterUpdate):
    adopter = db.query(Adopter).filter(Adopter.adopter_id == adopter_id).first()
    if not adopter:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(adopter, key, value)
    db.commit()
    db.refresh(adopter)
    return adopter

# Delete adopter
def delete_adopter(db: Session, adopter_id: str):
    adopter = db.query(Adopter).filter(Adopter.adopter_id == adopter_id).first()
    if not adopter:
        return None
    db.delete(adopter)
    db.commit()
    return adopter

#medicine
# Create a new medicine and generate a medicine_id
def create_medicine(db: Session, medicine: schemas.MedicineInventoryCreate):
    # Step 1: Get the last medicine ID
    last_medicine = db.query(MedicineInventory).order_by(MedicineInventory.medicine_id.desc()).first()
    
    if last_medicine:
        # Extract the numeric part and increment it
        last_id = int(last_medicine.medicine_id[3:])  # Extract number part from "MEDXXX"
        new_id = f"M{last_id + 1:03d}"  # Increment and format to "MEDXXX"
    else:
        new_id = "M001"  # Starting value if no records exist

    # Step 2: Create a new medicine record with the new ID
    db_medicine = MedicineInventory(
        medicine_id=new_id,  # Use the dynamically generated ID
        name=medicine.name,
        stock=medicine.stock,
        expiry=medicine.expiry,
        date_of_buying=medicine.date_of_buying
    )
    
    # Step 3: Add and commit the new medicine to the database
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    return db_medicine


# Get medicine by medicine_id
def get_medicine(db: Session, medicine_id: str):
    return db.query(MedicineInventory).filter(MedicineInventory.medicine_id == medicine_id).first()


# Update the stock of an existing medicine
def update_medicine_stock(db: Session, medicine_id: str, new_stock: int):
    db_medicine = db.query(MedicineInventory).filter(MedicineInventory.medicine_id == medicine_id).first()
    
    if db_medicine:
        db_medicine.stock = new_stock
        db.commit()
        db.refresh(db_medicine)
        return db_medicine
    return None


# Delete a medicine by medicine_id
def delete_medicine(db: Session, medicine_id: str):
    db_medicine = db.query(MedicineInventory).filter(MedicineInventory.medicine_id == medicine_id).first()
    
    if db_medicine:
        db.delete(db_medicine)
        db.commit()
        return True
    return False