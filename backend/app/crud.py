from sqlalchemy.orm import Session
from . import models, schemas

def create_animal(db: Session, animal: schemas.AnimalCreate):
    # Step 1: Get the last animal_ID
    last_animal = db.query(models.Animal).order_by(models.Animal.animal_ID.desc()).first()
    
    if last_animal:
        # Extract the numeric part and increment it
        last_id = int(last_animal.animal_ID[2:])  # Extract number part from "ANXXX"
        new_id = f"AN{last_id + 1:03d}"  # Increment and format to "ANXXX"
    else:
        new_id = "AN001"  # Starting value if no records exist

    # Step 2: Create a new animal record with the new ID
    db_animal = models.Animal(
        animal_ID=new_id,  # Use the dynamically generated ID
        name=animal.name,
        DOB=animal.DOB,
        gender=animal.gender,
        passive_adopter=animal.passive_adopter,
        breed_id=animal.breed_id  # This is the foreign key reference
    )
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    
    return db_animal
