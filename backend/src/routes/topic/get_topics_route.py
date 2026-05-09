from fastapi import Depends, Query

from src.core.base_response import http_ok
from src.routes.topic import router
from src.services.dependencies import get_topic_service
from src.services.topic.topic_service import TopicServiceImpl

@router.get('')
async def get_topics(
    topic_service: TopicServiceImpl = Depends(get_topic_service)
):
    try:
        topics = await topic_service.get_topics()
        return http_ok(data=topics)
    except Exception as e:
        raise e
