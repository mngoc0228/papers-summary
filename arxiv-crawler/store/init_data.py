import asyncio
import logging
import random

from services.openai.openai_service import OpenAIService
from services.papers.arxiv_service import ArxivService
from models.paper import PaperModel
from models.topic import TopicModel
from services.topic.topic_service import TopicService
from services.papers.paper_service import PaperService
from services.genai.google_genai import GoogleGenAIService

from config.setting_config import settings

async def initialize_data(engine):
    """
    Initializes the application data by fetching categories and papers from the arXiv API
    and storing them in the database.
    """

    try:
        logging.info("Initializing application data...")

        is_topics_exist = await TopicService(engine).is_topic_exists()
        if is_topics_exist:
            logging.info("Topics already exist in the database. Skipping initialization.")
            return

        arxiv_service = ArxivService()
        categories = await arxiv_service.fetch_categories()
        if categories is None:
            return

        # prepare topics to be stored in database
        topics = []
        for category in categories:
            topic = TopicModel(
                name=category["name"],
                code=category["code"]
            )
            topics.append(topic)
        
        topic_service = TopicService(engine)
        saved_topics = await topic_service.create_topics(topics)

        # fetch papers for each topic and store in database
        await fetch_and_store_papers_for_topics(engine, saved_topics)
        logging.info("Data initialization completed.")
    except Exception as e:
        logging.error(f"Error initializing data: {e}")

async def fetch_and_store_papers_for_topics(engine, topics: list[TopicModel]):
    """
    Fetches papers for a given topic and stores them in the database.
    """
    try:
        arxiv_service = ArxivService()
        openai_service = OpenAIService()
        paper_service = PaperService(engine)
        topic_service = TopicService(engine, openai_service=openai_service)
        for topic in topics:
            # slow request to avoid too many requests to arxiv api in a short time
            # When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request every three seconds, and limit requests to a single connection at a time.
            await asyncio.sleep(10.0)
            papers = await arxiv_service.fetch_papers(topic.code, max_results=10)
            papers_exist_with_title = await paper_service.find_papers_by_titles([paper["title"] for paper in papers])
            papers = [paper for paper in papers if paper["title"] not in [p.title for p in papers_exist_with_title]]
            paper_models = []
            for paper in papers:
                paper_model = PaperModel(
                    title=paper["title"],
                    abstract=paper["abstract"],
                    authors=paper["authors"],
                    published_date=paper["published"],
                    url=paper["url"],
                    summary=""
                )
                paper_models.append(paper_model)
            
            await topic_service.create_papers_via_topic(topic, paper_models)
    except Exception as e:
        logging.error(f"Error fetching and storing papers for topic {topic.name}: {e}")