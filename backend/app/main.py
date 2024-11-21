from app.api import animals
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RoleEnum, Employee
from app.api import auth_routes, employee, medical_records, animal_details, type, breeds, food, meds, adopter, nested, animals_by_type, medicine_inventory



app = FastAPI()

# # Example route to test
# @app.get("/")
# async def root():
#     return {"message": "Hello, World!"}
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; adjust for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_routes.router)  # Adjust this if you are using routers
app.include_router(animals.router)
app.include_router(employee.router)
app.include_router(medical_records.router)
app.include_router(animal_details.router)
app.include_router(type.router)
app.include_router(breeds.router)
app.include_router(food.router)
# app.include_router(meds.router)
app.include_router(adopter.router)
app.include_router(nested.router)
app.include_router(animals_by_type.router)
app.include_router(medicine_inventory.router)

