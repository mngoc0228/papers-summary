from src.routes.topic import router

from src.routes.topic.get_topics_route import get_topics
from src.routes.topic.get_followed_topics_route import get_followed_topics
from src.routes.topic.follow_topic_route import follow_topic
from src.routes.topic.unfollow_topic_route import unfollow_topic

topic_route = router
