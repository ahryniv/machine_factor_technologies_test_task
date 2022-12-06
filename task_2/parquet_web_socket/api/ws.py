import logging
from time import time
import json

import pandas as pd
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed

from parquet_web_socket.data_iterator import HistoricalDataIterator
from parquet_web_socket.utils import pandas_json_encoder

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_trading_data(websocket: WebSocket) -> pd.DataFrame:
    """Dependency to get trading data for the request"""
    return websocket.app.state.trading_data


@router.websocket('/ws')
async def ws(
    websocket: WebSocket,
    trading_data: pd.DataFrame = Depends(_get_trading_data),
):
    """WebSocket connection handler"""
    await websocket.accept()
    try:
        data_wrapper = HistoricalDataIterator(trading_data)
        t0 = time()
        count = 0
        for trades in data_wrapper:
            count += len(trades)
            json_ = json.dumps(trades, default=pandas_json_encoder)
            await websocket.send_text(json_)
        logger.info(f'WebSocket has given {count} trades in {time() - t0} seconds')
    except (WebSocketDisconnect, ConnectionClosed):
        pass
    await websocket.close(reason='All data has been given')
