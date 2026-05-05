from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    PORT: int = 8000

    class Config:
        ignore_extra = True


settings = Settings()
