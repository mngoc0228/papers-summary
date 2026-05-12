from fastapi import Depends, Query

from src.database.models.user import UserModel
from src.core.base_response import http_ok
from src.routes.topic import router
from src.services.dependencies import get_current_user, get_topic_service
from src.services.topic.topic_service import TopicServiceImpl

@router.get('/followed')
async def get_followed_topics(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Items per page"),
    current_user: UserModel = Depends(get_current_user),
    topic_service: TopicServiceImpl = Depends(get_topic_service)
):
    try:
        user_id = current_user.id
        followed_topics = await topic_service.get_followed_topics(user_id=user_id, page=page, size=size)
        return http_ok(
            data=followed_topics.items,
            page=followed_topics.page,
            size=followed_topics.size,
            total=followed_topics.total,
            pages=followed_topics.pages
        )
    except Exception as e:
        raise e
