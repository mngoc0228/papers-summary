import uuid

from fastapi import Depends, Query

from src.core.base_response import http_ok
from src.routes.paper import router
from src.services.dependencies import get_paper_service
from src.services.paper.paper_service import PaperServiceImpl

@router.get('')
async def get_papers(
    q: str = Query(None, description="Search query for paper title or abstract"),
    topic_id: str = Query(None, description="Filter papers by topic ID"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Items per page"),
    paper_service: PaperServiceImpl = Depends(get_paper_service)
):
    try:
        papers = await paper_service.get_papers(q=q, topic_id=topic_id, page=page, size=size)
        return http_ok(
            data=papers.items,
            page=papers.page,
            size=papers.size,
            total=papers.total,
            pages=papers.pages
        )
    except Exception as e:
        raise e
