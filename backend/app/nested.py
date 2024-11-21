from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

def get_animals_without_medical_records(db: Session):
    query = """
    SELECT name
    FROM animals
    WHERE animal_id NOT IN (
        SELECT DISTINCT animal_id
        FROM medical_records
    );
    """
    result = db.execute(text(query)).fetchall()
    return result