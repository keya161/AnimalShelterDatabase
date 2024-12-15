# Animal Shelter Database

## Overview

This is a comprehensive Animal Shelter Management System built with FastAPI (backend), SQLAlchemy (database ORM), and Streamlit (frontend). The application provides a robust solution for managing animal shelters, supporting multiple user roles with different access levels.

## Features

### User Roles
- **Admin**: Full system access
  - Manage animals, types, food inventory, medicine inventory
  - Create and manage employees
  - View detailed animal records
- **Volunteer**: Limited access
  - Update food and medicine inventory
- **Doctor**: Medical record management
  - Add and view medical records

### Key Functionalities
- Animal Management
  - Add, update, delete, and view animal records
  - Track animal details (name, breed, gender, age)
- Medical Records
  - Create and track medical history for each animal
  - Record diagnoses, treatments, and follow-ups
- Food and Medicine Inventory
  - Track stock levels
  - Update inventory
- Adopter Management
  - Record adopter information
  - Track animal adoptions

## Technology Stack

- **Backend**: 
  - FastAPI
  - SQLAlchemy
  - Pydantic
- **Frontend**:
  - Streamlit
- **Database**:
  - MySQL

## Prerequisites

- Python 3.8+
- MySQL
- pip (Python package manager)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/AnimalShelterDatabase.git
cd AnimalShelterDatabase
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
# Make sure to install MySQL connector
pip install mysqlclient  # or mysql-connector-python
```

4. Set up your MySQL database
```sql
CREATE DATABASE animal_shelter;
```

5. Configure database connection
- Update your database connection string in the configuration file
- Typical MySQL connection string format:
  ```
  mysql+pymysql://username:password@localhost/AnimalShelterDatabase
  ```

6. Start the FastAPI backend
```bash
uvicorn app.main:app --reload
```

7. Start the Streamlit frontend
```bash
streamlit run main.py
```

## Environment Variables

Create a `.env` file with the following variables:
```
DATABASE_URL=mysql+pymysql://shelter_admin:your_password@localhost/animal_shelter
SECRET_KEY=your_secret_key
```

## Authentication

The system uses role-based authentication:
- Employees are registered with a unique employee ID
- Passwords are securely stored
- Different roles have different dashboard access


## Troubleshooting MySQL Setup
- Ensure MySQL server is running
- Check database connection credentials
- Install necessary MySQL Python drivers
- Verify database permissions

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [MySQL](https://www.mysql.com/)
