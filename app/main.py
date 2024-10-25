from fastapi import FastAPI
from app.routes import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Air Quality API"}
