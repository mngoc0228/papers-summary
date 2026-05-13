import uuid
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
        followed_topics = await topic_service.get_followed_topics_by_user_id(user_id=user_id, page=page, size=size)
        return http_ok(
            data=followed_topics.items,
            page=followed_topics.page,
            size=followed_topics.size,
            total=followed_topics.total,
            pages=followed_topics.pages
        )
    except Exception as e:
        raise e


@router.get('/{topic_id}/followed')
async def is_following_topic(
    topic_id: uuid.UUID,
    current_user: UserModel = Depends(get_current_user),
    topic_service: TopicServiceImpl = Depends(get_topic_service)
):
    try:
        user_id = current_user.id
        topic = await topic_service.get_followed_topic_by_user_id_and_topic_id(user_id=user_id, topic_id=topic_id)
        if not topic:
            return http_ok(data={"is_following": False})
        is_following = any(follower.id == user_id for follower in topic.followers)
        return http_ok(data={"is_following": is_following})
    except Exception as e:
        raise e
