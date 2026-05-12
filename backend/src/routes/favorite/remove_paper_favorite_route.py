import uuid

from fastapi import Depends

from src.core.base_response import http_ok
from src.database.models.user import UserModel
from src.services.dependencies import get_current_user, get_paper_service
from src.services.paper.paper_service import PaperServiceImpl
from src.routes.favorite import router

@router.delete("/{id}/favorites")
async def remove_paper_favorite(
    id: uuid.UUID,
    current_user: UserModel = Depends(get_current_user),
    paper_service: PaperServiceImpl = Depends(get_paper_service)
):
    try:
        user_id = current_user.id
        await paper_service.remove_favorite_paper(user_id=user_id, paper_id=id)
        return http_ok(data={"message": "Removed paper from favorites successfully"})
    except Exception as e:
        raise e
