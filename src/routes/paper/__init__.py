from fastapi import APIRouter

router = APIRouter(
    prefix="/papers",
    tags=["Papers"],
)
