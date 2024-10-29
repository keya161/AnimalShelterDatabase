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
