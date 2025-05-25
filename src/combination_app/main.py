from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from combination_app.config.database import SessionLocal, engine, get_db
# from . import models

load_dotenv()

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Combination App API",
    description="API for managing combinations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Combination App API is running!"}
