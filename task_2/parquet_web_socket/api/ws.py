import pandas as pd
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed

router = APIRouter()


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
        for _, row in trading_data.iterrows():
            # TODO: WIP
            await websocket.send_text(row.to_json())
    except (WebSocketDisconnect, ConnectionClosed):
        pass
