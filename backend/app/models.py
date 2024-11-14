from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CHAR, Date, Enum, Float
from sqlalchemy.orm import relationship
from .database import Base
import enum
class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    TECHNICIAN = "technician"
    VOLUNTEER = "volunteer"

class Employee(Base):
    __tablename__ = "employee"
    
    employee_id = Column(CHAR(5), primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    date_of_joining = Column(Date, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)  # Define role with Enum
    credentials = relationship("Credentials", back_populates="employee", uselist=False)

class Credentials(Base):
    __tablename__ = "credentials"
    
    employee_id = Column(CHAR(5), ForeignKey("employee.employee_id"), primary_key=True, nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Use hashed password
    employee = relationship("Employee", back_populates="credentials", uselist=False)

class Animal(Base):
    __tablename__ = "animals"
    
    animal_id = Column(CHAR(5), primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum("M", "F"), nullable=False)
    breed_id = Column(CHAR(5), ForeignKey("type.type_id"), nullable=False)
    passive_adopter = Column(Boolean, default=False)    
    breed = relationship("Type", back_populates="animals")
    medical_records = relationship("MedicalRecords", back_populates="animal")
    supplements = relationship("MedicineInventory", secondary="supplements", back_populates="animals")
    adopters = relationship("Adopter", back_populates="animal")

class Type(Base):
    __tablename__ = "type"
    
    type_id = Column(CHAR(5), primary_key=True, nullable=False)
    breed = Column(String(45), nullable=False)
    feed = Column(String(45), nullable=False)
    freq_of_checkup = Column(Integer, nullable=False)
    bath = Column(Date, nullable=True)
    
    animals = relationship("Animal", back_populates="breed")
    food_items = relationship("FoodInventory", secondary="type_for_animals", back_populates="types")

class TypeForAnimals(Base):
    __tablename__ = "type_for_animals"
    
    type_id = Column(CHAR(5), ForeignKey("type.type_id"), primary_key=True)
    feed_id = Column(CHAR(5), ForeignKey("food_inventory.food_id"), primary_key=True)

class FoodInventory(Base):
    __tablename__ = "food_inventory"
    
    food_id = Column(CHAR(5), primary_key=True, nullable=False)
    type = Column(String(45), nullable=False)
    stock = Column(Integer, nullable=False)
    cost_per_kg = Column(Float, nullable=False)
    
    types = relationship("Type", secondary="type_for_animals", back_populates="food_items")

class MedicalRecords(Base):
    __tablename__ = "medical_records"
    
    record_id = Column(CHAR(5), primary_key=True, nullable=False)
    animal_id = Column(CHAR(5), ForeignKey('animals.animal_id', ondelete='CASCADE'))
    name = Column(String(45), nullable=False)
    report = Column(String(255), nullable=True)
    doctor = Column(String(45), nullable=False)
    date = Column(Date, nullable=False)
    diagnosis = Column(String(255), nullable=False)
    medicine = Column(String(45), nullable=False)
    follow_up = Column(Date, nullable=True)
    freq_of_usage = Column(Integer, nullable=True)
    
    animal = relationship("Animal", back_populates="medical_records")
    medicines = relationship("MedicineInventory", secondary="uses", back_populates="medical_records")

class MedicineInventory(Base):
    __tablename__ = "medicine_inventory"
    
    medicine_id = Column(CHAR(5), primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    stock = Column(Integer, nullable=False)
    expiry = Column(Date, nullable=False)
    date_of_buying = Column(Date, nullable=False)
    
    medical_records = relationship("MedicalRecords", secondary="uses", back_populates="medicines")
    animals = relationship("Animal", secondary="supplements", back_populates="supplements")

class Uses(Base):
    __tablename__ = "uses"
    
    animal_id = Column(CHAR(5), ForeignKey("animals.animal_id"), primary_key=True)
    medicine_id = Column(CHAR(5), ForeignKey("medicine_inventory.medicine_id"), primary_key=True)
    record_id = Column(CHAR(5), ForeignKey("medical_records.record_id"), primary_key=True)
    date = Column(Date, nullable=False)

class Supplements(Base):
    __tablename__ = "supplements"
    
    animal_id = Column(CHAR(5), ForeignKey("animals.animal_id"), primary_key=True)
    medicine_id = Column(CHAR(5), ForeignKey("medicine_inventory.medicine_id"), primary_key=True)

class Adopter(Base):
    __tablename__ = "adopter"
    
    adopter_id = Column(CHAR(5), primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    animal_id = Column(CHAR(5), ForeignKey("animals.animal_id"), nullable=False)
    contribution = Column(Float, nullable=False)
    
    animal = relationship("Animal", back_populates="adopters")