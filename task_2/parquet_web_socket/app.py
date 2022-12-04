import logging
import logging.config
import sys
from typing import Optional

from fastapi import FastAPI

from parquet_web_socket import __version__
from parquet_web_socket.api import base, ws
from parquet_web_socket.settings import Settings, settings, LogLevel
from parquet_web_socket.utils import read_parquet_file

logger = logging.getLogger(__name__)


def init_logging(level: LogLevel) -> None:
    """Configure root logger to stdout"""
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)


def prepare_trading_data(app: FastAPI, app_settings: Settings) -> None:
    """Prepares trading data for future requests and save it in the app state"""
    logger.info(f'Preparing parquet trading data from file "{app_settings.PARQUET_FILE}"')
    df = read_parquet_file(app_settings.PARQUET_FILE)
    app.state.trading_data = df.sort_values(by=['timestamp'])


def create_app(app_settings: Optional[Settings] = None) -> FastAPI:
    """Creates FastAPI application instance"""
    app_settings = app_settings if app_settings is not None else settings
    app = FastAPI(
        title='Parquet WebSocket',
        description='Streaming data from parquet file',
        version=__version__,
    )
    init_logging(app_settings.LOG_LEVEL)

    @app.on_event('startup')
    def startup():
        prepare_trading_data(app, app_settings)

    # routes
    app.include_router(base.router, tags=['Base'])
    app.include_router(ws.router, tags=['WebSocket'])
    return app
