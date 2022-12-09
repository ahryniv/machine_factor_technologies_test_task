import logging

from src.db.config import engine
from src.conf.logger import init_logging
from src.task_1_1 import (
    get_more_than_avg_40_rows,
    get_avg_dollar_volume,
    get_avg_abs_daily_percent_change,
    get_positive_volumes,
)

logger = logging.getLogger(__name__)


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
