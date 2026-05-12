from fastapi import APIRouter

router = APIRouter(
    prefix="/papers",
    tags=["favorites"],
)
