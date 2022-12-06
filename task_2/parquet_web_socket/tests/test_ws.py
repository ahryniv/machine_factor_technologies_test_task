import itertools
from typing import TYPE_CHECKING
from fastapi import WebSocketDisconnect

from fastapi.testclient import TestClient
import pandas as pd
import pytest

if TYPE_CHECKING:
    from fastapi import FastAPI

WS_PATH = '/ws'


def test_ws(app: 'FastAPI'):
    client = TestClient(app)
    expected_batches = [
        [
            {'id': 0, 'timestamp': 1111111111111},
            {'id': 1, 'timestamp': 1111111111111},
            {'id': 2, 'timestamp': 1111111111111},
        ],
        [
            {'id': 3, 'timestamp': 2222222222222},
        ],
        [
            {'id': 4, 'timestamp': 3333333333333},
            {'id': 5, 'timestamp': 3333333333333},
        ],
        [
            {'id': 6, 'timestamp': 4444444444444},
        ],
    ]

    app.state.trading_data = pd.DataFrame(itertools.chain.from_iterable(expected_batches))
    with client.websocket_connect(WS_PATH) as websocket:
        for batch in expected_batches:
            data = websocket.receive_json()
            assert data == batch
        with pytest.raises(WebSocketDisconnect) as exc_info:
            websocket.receive_json()
    exc_info.value.args == (1000, 'All data has been given')
