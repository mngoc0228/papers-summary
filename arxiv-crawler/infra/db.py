from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine

from config.setting_config import settings

engine: Engine | None = None

def connect_to_database() -> Engine:
    """
    Initializes the global database connection. This function should be called at the startup of the application.
    """
    try:
        global engine
        if engine is None:
            engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True, pool_pre_ping=True)
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)
    """    # Create initial data"""
