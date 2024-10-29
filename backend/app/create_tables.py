from .database import engine  # Adjust the import based on your directory structure
from .models import Base

# Create the tables in the database
Base.metadata.create_all(engine)
