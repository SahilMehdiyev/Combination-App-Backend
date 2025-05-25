from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import logging
from combination_app.config.settings import get_settings
from combination_app.api.v1.router import api_router
from combination_app.utils.helpers import create_response

from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from combination_app.config.database import SessionLocal, engine, get_db

settings = get_settings()


load_dotenv()


app = FastAPI(
    title=settings.app_name,
    description="API for managing combinations",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Combination App API is running!"}
