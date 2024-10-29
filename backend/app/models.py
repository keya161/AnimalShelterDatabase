from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CHAR, Date, Enum
from sqlalchemy.orm import relationship
from .database import Base

class Animal(Base):
    __tablename__ = "animals"

    animal_ID = Column(CHAR(5), primary_key=True, nullable=False)
    name = Column(String(40), nullable=False)
    DOB = Column(Date, nullable=True)
    gender = Column(Enum("M", "F"), nullable=False)
    passive_adopter = Column(String(45), nullable=True)
    breed_id = Column(CHAR(5), ForeignKey("type.type_id"), nullable=False)
    breed = relationship("Type", back_populates="animals")

class Type(Base):
    __tablename__ = "type"

    type_id = Column(CHAR(5), primary_key=True, nullable=False)
    breed_name = Column(String(45), nullable=False)
    freq_of_checkup_days = Column(INT, nullable=True)  
    Bath = Column(Date, nullable=True)
    animals = relationship("Animal", back_populates="breed")
