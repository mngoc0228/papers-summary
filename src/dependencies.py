"""
    Dependencies which can be used for DI
"""

from collections.abc import Generator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.config import Settings
from src.database.db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_db)]


@lru_cache()
def get_settings():
    return Settings()
