from pydantic import BaseSettings

from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    """Reads config from environment variables"""

    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = 'postgres'
    POSTGRES_HOSTNAME: str = 'localhost'
    POSTGRES_PORT: int = 5432

    @property
    def sqlalchemy_database_uri(self) -> URL:
        return URL.create(
            drivername='postgresql',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOSTNAME,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


settings = Settings()
