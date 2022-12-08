from decimal import Decimal
import logging
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.sql import text

from src.db.config import engine
from src.conf.logger import init_logging

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection, Row

logger = logging.getLogger(__name__)


def get_more_than_avg_40_rows(conn: 'Connection', year: int) -> Optional[Decimal]:
    """Get % of symbols for which at least one row has bigger close price that avg of previous 40 rows"""
    query = text('''
        SELECT COUNT(sub2.more_than_prev_40_avg)::float / COUNT(*)::float * 100 as percents
        FROM (
            SELECT distinct on (sub.symbol)
                sub.symbol,
                more_than_prev_40_avg
            FROM (
                SELECT
                    b.symbol,
                    b.close > avg(b.close) OVER (
                        PARTITION BY b.symbol
                        ORDER BY b.date
                        ROWS BETWEEN 40 PRECEDING AND CURRENT ROW
                    ) as more_than_prev_40_avg
                FROM bars_1 b
                WHERE date_part('year', b.date) = :year
            ) as sub
            ORDER BY sub.symbol, more_than_prev_40_avg DESC
        ) as sub2
    ''')
    res = conn.execute(query, year=year).fetchone()
    if not res:
        return None
    return res.percents


def get_avg_dollar_volume(conn: 'Connection', year: int) -> Optional[Decimal]:
    """Get average dollar volume for the year"""
    query = text('''
        SELECT AVG(b.adj_close * b.volume) as avg_dollar_volume
        FROM bars_1 b
        WHERE DATE_PART('year', b.date) = :year
        GROUP BY date_part('year', b.date)
    ''')
    res = conn.execute(query, year=year).fetchone()
    if not res:
        return None
    return res.avg_dollar_volume


def get_positive_volumes(conn: 'Connection', year: int) -> List['Row']:
    """Get Positive Volume"""
    query = text('''
        SELECT sub.symbol, SUM(sub.positive_volume) as positive_volume
        FROM (
            SELECT
                b.symbol,
                CASE
                    WHEN
                        b.close >= (LAG(b.close, 1) over(
                            PARTITION BY b.symbol
                            ORDER BY b.date
                        ))
                    THEN b.volume
                    ELSE 0
                END
                AS positive_volume
            FROM bars_1 b
            WHERE DATE_PART('year', b.date) = :year
        ) as sub
        GROUP BY sub.symbol
        ORDER BY SUM(sub.positive_volume)
    ''')
    return conn.execute(query, year=year).fetchall()


def get_avg_abs_daily_percent_change(conn: 'Connection') -> List['Row']:
    """Get Average Absolute Daily Percent Change"""
    query = text('''
        SELECT sub.symbol, AVG(sub.daily_change) as avg_daily_change
        FROM (
            SELECT
                b.symbol,
                ABS((LAG(b.close, 1) over(
                    PARTITION BY b.symbol
                    ORDER BY b.date
                ) - b.close) / b.close * 100)
                as daily_change
            FROM bars_1 b
        ) as sub
        GROUP BY sub.symbol
    ''')
    return conn.execute(query).fetchall()


if __name__ == '__main__':
    init_logging()
    more_than_avg_40_rows_year = 2019
    avg_dollar_volume_year = 2019
    positive_volumes_year = 2015
    percents_ = 2015

    with engine.connect() as con:
        more_than_avg_40_rows = get_more_than_avg_40_rows(con, more_than_avg_40_rows_year)
        avg_dollar_volume = get_avg_dollar_volume(con, avg_dollar_volume_year)
        avg_daily_change = get_avg_abs_daily_percent_change(con)
        positive_volumes = get_positive_volumes(con, year=positive_volumes_year)

    for row in avg_daily_change:
        logger.info(f'[Average Absolute Daily Percent Change] - {row.symbol}: {row.avg_daily_change}')
    for row in positive_volumes:
        logger.info(f'[Positive Volume] - {row.symbol}: {row.positive_volume}')
    logger.info(f'[Average dollar volume] - in {avg_dollar_volume_year} was {avg_dollar_volume}')
    logger.info(f'[% Symbols with price bigger than previous 40 rows] in {more_than_avg_40_rows_year}'
                f' was {more_than_avg_40_rows}')
