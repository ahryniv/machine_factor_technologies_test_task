from enum import Enum

from pydantic import BaseSettings, FilePath, validator


class LogLevel(int, Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Settings(BaseSettings):
    PARQUET_FILE: FilePath
    PORT: int = 80
    LOG_LEVEL: LogLevel = LogLevel.INFO

    @validator('LOG_LEVEL', pre=True)
    def validate_log_level(cls, value: str) -> int:
        return int(value)


settings = Settings()
