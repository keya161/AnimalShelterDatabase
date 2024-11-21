from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.nested import get_animals_without_medical_records
from app.schemas import AnimalNameResponse
from app.models import Animal, MedicalRecords, Adopter

router = APIRouter(prefix="/queries", tags=["Queries"])

@router.get("/", response_model=list[AnimalNameResponse])
def get_animals_without_medical_records_endpoint(db: Session = Depends(get_db)):
    # Get the list of animals without medical records using the query function
    result = get_animals_without_medical_records(db=db)
    
    # If no animals are found, raise a 404 error
    if not result:
        raise HTTPException(status_code=404, detail="No animals without medical records found")
    
    # Map the result to the AnimalNameResponse model
    return [AnimalNameResponse(name=row[0]) for row in result]

@router.get("/animals_with_medical_records_and_adopters")
def get_animals_with_medical_records_and_adopters(db: Session = Depends(get_db)):
    # Perform the query to fetch animals with medical records and adopters
    query = db.query(Animal).join(MedicalRecords, Animal.animal_id == MedicalRecords.animal_id) \
        .join(Adopter, Animal.animal_id == Adopter.animal_id) \
        .all()

    # Convert the result into a list of dictionaries with relevant information
    animals = [
        {
            "animal_id": animal.animal_id,
            "name": animal.name,
            "dob": animal.dob,
            "gender": animal.gender,
            "medical_records": [
                {
                    "record_id": record.record_id,
                    "name": record.name,
                    "date": record.date,
                    "diagnosis": record.diagnosis,
                    "medicine": record.medicine,
                    "follow_up": record.follow_up,
                    "freq_of_usage": record.freq_of_usage
                }
                for record in animal.medical_records
            ],
            "adopters": [
                {
                    "adopter_id": adopter.adopter_id,
                    "name": adopter.name,
                    "contribution": adopter.contribution
                }
                for adopter in animal.adopters
            ]
        }
        for animal in query
    ]
    
    return animals