from typing import TYPE_CHECKING

import pandas as pd
import pytest

from parquet_web_socket.app import create_app
from parquet_web_socket.settings import settings

if TYPE_CHECKING:
    from fastapi import FastAPI


@pytest.fixture(scope='session')
def app() -> 'FastAPI':
    app = create_app(settings)
    app.state.trading_data = pd.DataFrame(columns=['timestamp'])
    return app
