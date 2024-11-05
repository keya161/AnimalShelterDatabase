# app/routers/employee.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Employee as EmployeeModel
from app.schemas import Employee as EmployeeSchema, EmployeeCreate
from app.crud import create_employee, get_employees

router = APIRouter()

@router.post("/employees", response_model=EmployeeSchema)
def api_create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db=db, employee_data=employee)

@router.get("/employees", response_model = List[EmployeeSchema])
def api_get_employee(name: Optional[str] = None, db: Session = Depends(get_db)):
    return get_employees(db=db, name=name)