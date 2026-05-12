import uuid

from fastapi import Depends

from src.database.models.user import UserModel
from src.core.base_response import http_ok
from src.routes.topic import router
from src.services.dependencies import get_current_user, get_topic_service
from src.services.topic.topic_service import TopicServiceImpl

@router.post('/{topic_id}/follow')
async def follow_topic(
    topic_id: uuid.UUID,
    current_user: UserModel = Depends(get_current_user),
    topic_service: TopicServiceImpl = Depends(get_topic_service)
):
    try:
        user_id = current_user.id
        await topic_service.follow_topic(user_id=user_id, topic_id=topic_id)
        return http_ok(data={"message": "Followed the topic successfully"})
    except Exception as e:
        raise e
