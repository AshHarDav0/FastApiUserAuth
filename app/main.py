import os

from dotenv import load_dotenv
from fastapi import FastAPI
from uvicorn import run
from app.resources import router
from app.database import create_database

load_dotenv()

app = FastAPI(docs_url="/docs", redoc_url="/redoc")


@app.on_event("startup")
def startup_event():
    """
    Function to be called on application startup.
    This will create the database.
    """
    create_database()


app.include_router(router)

if __name__ == "__main__":
    run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True)
