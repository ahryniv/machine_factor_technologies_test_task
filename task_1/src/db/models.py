from datetime import datetime, date
from decimal import Decimal
from typing import Optional

import sqlalchemy as sa

from src.db.config import BaseModelID


class Bars1(BaseModelID):
    __tablename__ = 'bars_1'

    date: date = sa.Column(sa.Date(), nullable=False)
    symbol: str = sa.Column(sa.String(), nullable=False)
    adj_close: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    close: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    high: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    low: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    open: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    volume: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)

    @classmethod
    def from_bars_2(cls, bars_2_row: 'Bars2') -> 'Bars1':
        return cls(
            date=bars_2_row.date,
            symbol=bars_2_row.symbol,
            adj_close=bars_2_row.adj_close,
            close=bars_2_row.close,
            high=bars_2_row.high,
            low=bars_2_row.low,
            open=bars_2_row.open,
            volume=bars_2_row.volume,
        )


class Bars2(BaseModelID):
    __tablename__ = 'bars_2'

    date: date = sa.Column(sa.Date(), nullable=False)
    symbol: str = sa.Column(sa.String(), nullable=False)
    adj_close: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    close: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    high: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    low: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    open: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)
    volume: Optional[Decimal] = sa.Column(sa.DECIMAL(), nullable=True)


class ErrorLog(BaseModelID):
    __tablename__ = 'error_log'

    launch_timestamp: datetime = sa.Column(sa.TIMESTAMP(), nullable=False, default=datetime.utcnow)
    date: date = sa.Column(sa.Date(), nullable=True)
    symbol: Optional[str] = sa.Column(sa.String(), nullable=True)
    message: str = sa.Column(sa.String(), nullable=False)
