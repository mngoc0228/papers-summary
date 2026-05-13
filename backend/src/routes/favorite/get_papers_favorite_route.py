import uuid
from fastapi import Depends, Query

from src.core.base_response import http_ok
from src.database.models.user import UserModel
from src.services.dependencies import get_current_user, get_paper_service
from src.services.paper.paper_service import PaperServiceImpl
from src.routes.favorite import router

@router.get("/favorites")
async def get_papers_favorite(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Items per page"),
    current_user: UserModel = Depends(get_current_user),
    paper_service: PaperServiceImpl = Depends(get_paper_service)
):
    try:
        user_id = current_user.id
        favorite_papers = await paper_service.get_favorite_papers_by_user_id(user_id=user_id, page=page, size=size)
        return http_ok(
            data=favorite_papers.items,
            page=favorite_papers.page,
            size=favorite_papers.size,
            total=favorite_papers.total
        )
    except Exception as e:
        raise e

@router.get("/{id}/favorites")
async def is_favorite_paper(
    id: uuid.UUID,
    current_user: UserModel = Depends(get_current_user),
    paper_service: PaperServiceImpl = Depends(get_paper_service)
):
    try:
        user_id = current_user.id
        paper = await paper_service.get_favorite_paper_by_user_id_and_paper_id(user_id=user_id, paper_id=id)
        if not paper:
            return http_ok(data={"is_favorite": False})
        return http_ok(data={"is_favorite": True})
    except Exception as e:
        raise e
