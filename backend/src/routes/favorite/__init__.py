from fastapi import APIRouter

router = APIRouter(
    prefix="/papers/{id}/favorites",
    tags=["favorites"],
)
