from fastapi import APIRouter

from app.api.v1 import endpoints
from app.api.v1 import payments


api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="", tags=["api"])
api_router.include_router(payments.router, prefix="", tags=["payments"])

