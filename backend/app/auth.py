from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Employee, RoleEnum,Credentials
from app.database import get_db

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key"  # Change this to a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthenticationError(Exception):
    pass

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    try:
        # Query the credentials table
        credentials = (
            db.query(Credentials)
            .filter(Credentials.username == username)
            .first()
        )
        
        if not credentials or not verify_password(password, credentials.password):
            raise AuthenticationError("Invalid username or password")
        
        # Get the associated employee
        employee = credentials.employee
        if not employee:
            raise AuthenticationError("Employee not found")
            
        return employee
        
    except SQLAlchemyError as e:
        raise AuthenticationError(f"Database error: {str(e)}")

def create_new_user( #register
    db: Session,
    employee_id: str,
    username: str,
    password: str,
):
    try:
        existing_credentials = (
            db.query(Credentials)
            .filter(Credentials.username == username)
            .first()
        )
        if existing_credentials:
            raise AuthenticationError("Username already registered")

        # Create credentials with hashed password
        credentials = Credentials(
            employee_id=employee_id,
            username=username,
            password=get_password_hash(password)
        )
        
        db.add(credentials)
        db.commit()
        
        return credentials
        
    except SQLAlchemyError as e:
        db.rollback()
        raise AuthenticationError(f"Error creating user: {str(e)}")

def login_user(db: Session, username: str, password: str):
    employee = authenticate_user(db, username, password)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": employee.employee_id,
            "username": username,
            "role": employee.role.value
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": employee.role.value,
        "employee_id": employee.employee_id
    }

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Employee:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        employee_id: str = payload.get("sub")
        if employee_id is None:
            raise credentials_exception
            
        # Get employee from database
        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )
        
        if employee is None:
            raise credentials_exception
            
        return employee
        
    except JWTError:
        raise credentials_exception

def role_required(allowed_roles: list[RoleEnum]):
    async def role_checker(
        current_user: Employee = Security(get_current_user)
    ) -> bool:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return True
    return role_checker

