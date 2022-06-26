import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host=os.environ["POSTGRES_HOST"], 
            database=os.environ["POSTGRES_DATABASE"], 
            user=os.environ["POSTGRES_USER"], 
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\n>>> Status:\nConnection established with database.\n")
        break

    except Exception as err:
        print("\n>>> Status:\nFailed to connect to database.\n")
        print(f"--> Error: {err}")
        time.sleep(2)

@app.get("/health", tags=["Global"])
def health_check():
    return "Welcome to my API, I'm alive!"

app.include_router(post.router)
app.include_router(user.router)
