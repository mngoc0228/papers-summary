from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    ## JWT settings
    JWT_SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    EXPIRE_MINUTES: int = 20000  # 20.000 minutes ~ 14 days

    @computed_field  # type: ignore[prop-decorator] 
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
