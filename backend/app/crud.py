from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List, Optional
from . import models, schemas
from app.models import Animal, MedicalRecords, Employee, Adopter, Type
from app.schemas import AnimalCreate, EmployeeCreate, MedicalRecordCreate, AnimalDetail, MedicalRecordBase, AdopterBase

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
                report=row.MedicalRecords.report,
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
            adopters_dict[row.Adopter.adopter_id] = AdopterBase(
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
    animal = db.query(Animal).filter(Animal.name == record.name).first()

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

    # Step 3: Create the medical record with the found animal ID and generated record ID
    db_record = MedicalRecords(
        record_id=new_record_id,  # Use the dynamically generated ID
        animal_id=animal.animal_id,  # Fill in the animal ID automatically
        name=record.name,
        report=record.report,
        doctor=record.doctor,
        date=record.date,
        diagnosis=record.diagnosis,
        medicine=record.medicine,
        follow_up=record.follow_up,
        freq_of_usage=record.freq_of_usage
    )
    
    # Step 4: Add and commit the new medical record to the database
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record
def get_medical_records( db: Session, name: Optional[str] = None) -> List[schemas.MedicalRecordResponse]:
    # Step 1: Query the MedicalRecords
    query = db.query(models.MedicalRecords)

    # Step 2: Filter by animal_id if provided
    if name:
        query = query.filter(models.MedicalRecords.name == name)

    # Step 3: Fetch all medical records
    medical_records = query.all()

    # Step 4: Check if any records were found
    if not medical_records:
        raise HTTPException(status_code=404, detail="No medical records found")

    # Step 5: Return the medical records as a list of MedicalRecordResponse
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
