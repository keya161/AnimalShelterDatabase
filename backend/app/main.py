from fastapi import FastAPI
from app.api import animals


app = FastAPI()

# # Example route to test
# @app.get("/")
# async def root():
#     return {"message": "Hello, World!"}

app.include_router(animals.router)
