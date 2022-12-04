from enum import Enum

from pydantic import BaseSettings, FilePath


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


settings = Settings()
