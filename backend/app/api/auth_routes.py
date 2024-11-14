from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RoleEnum, Employee
from app.auth import create_new_user, login_user, AuthenticationError, role_required, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


# FastAPI route handlers
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        login_result = login_user(db, form_data.username, form_data.password)
        return login_result
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register")
async def register_user(
    employee_id: str,
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    try:
        employee = create_new_user(db, employee_id, username, password)
        return {
            "message": "User created successfully",
            "employee_id": employee.employee_id,
            "username": username,
        }
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Example protected route
@router.get("/protected")
async def protected_route(
    current_user: Employee = Depends(get_current_user)
):
    return {
        "message": "Access granted",
        "employee_id": current_user.employee_id,
        "name": current_user.name,
        "role": current_user.role.value
    }

# Example admin-only route
@router.get("/admin")
async def admin_route(
    authorized: bool = Depends(role_required([RoleEnum.ADMIN])),
    current_user: Employee = Depends(get_current_user)
):
    return {
        "message": "Admin access granted",
        "employee_id": current_user.employee_id,
        "name": current_user.name
    }