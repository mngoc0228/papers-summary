from datetime import datetime
import logging

from sqlmodel import SQLModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.setting_config import settings
from infra.db import connect_to_database
from store.init_data import initialize_data, fetch_and_store_papers_for_topics
from services.topic.topic_service import TopicService


class AppContext:
    """
    Application context to hold global state and configurations.
    """

    def __init__(self):
        self.settings = settings
        self.scheduler = AsyncIOScheduler()

    async def start_up(self):
        """
        Initializes the application context, including database connections.
        """
        logging.info("Starting up application context...")

        # Initialize database connection
        database_connection = connect_to_database()
        SQLModel.metadata.create_all(database_connection)

        # Initialize application data
        await initialize_data(database_connection)

        topic_service = TopicService(database_connection)
        topics = await topic_service.get_all_topics()
        if topics is not None and len(topics) > 0:
            self.scheduler.start()
            self.scheduler.add_job(fetch_and_store_papers_for_topics, 'cron', args=[database_connection, topics], hour=1, minute=0, next_run_time=datetime.now())  # run every day at 1 AM

    async def shut_down(self):
        """
        Cleans up resources before shutting down the application.
        """
        self.scheduler.shutdown()
        logging.info("Shutting down application context...")


app_context = AppContext()
