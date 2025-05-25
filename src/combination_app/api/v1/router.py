from fastapi import APIRouter
from . import auth, users, combinations

api_router = APIRouter(prefix='api/v1')

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(combinations.router)