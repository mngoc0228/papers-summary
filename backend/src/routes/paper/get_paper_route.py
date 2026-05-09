import uuid

from fastapi import Depends

from src.core.base_response import http_ok
from src.routes.paper import router
from src.services.dependencies import get_paper_service
from src.services.paper.paper_service import PaperServiceImpl

@router.get('/{id}')
async def get_paper(
    id: uuid.UUID,
    paper_service: PaperServiceImpl = Depends(get_paper_service)
):
    try:
        paper = await paper_service.get_paper_by_id(id=id)
        if not paper:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Paper not found")
        return http_ok(data=paper)
    except Exception as e:
        raise e
