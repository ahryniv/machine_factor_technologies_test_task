import logging
import uvicorn

from parquet_web_socket.app import create_app
from parquet_web_socket.settings import settings

app = create_app()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=settings.PORT,
        log_level=logging.getLevelName(settings.LOG_LEVEL).lower(),
        loop='uvloop'
    )
