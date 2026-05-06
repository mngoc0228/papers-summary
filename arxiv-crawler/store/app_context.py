import json
import logging

from config.setting_config import settings
from services.papers.arxiv_service import ArxivService


class AppContext:
    """
    Application context to hold global state and configurations.
    """

    def __init__(self):
        self.settings = settings

    async def start_up(self):
        """
        Initializes the application context, including database connections.
        """
        logging.info("Starting up application context...")

        arxiv_service = ArxivService()
        categories = await arxiv_service.fetch_categories()
        logging.info(f"Fetched categories: {categories}")
        papers = await arxiv_service.fetch_papers(category=categories[0]["code"], max_results=5)
        # debug log json papers
        logging.info(f"Fetched papers")
        print(json.dumps(papers, indent=4))


    async def shut_down(self):
        """
        Cleans up resources before shutting down the application.
        """

        logging.info("Shutting down application context...")


app_context = AppContext()
