from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import animals


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

app.include_router(animals.router)
