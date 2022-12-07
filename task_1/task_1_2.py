"""NOT FINISHED.

I didn't find a way how to analyse batch of 20000 rows in 30 seconds.
"""


from decimal import Decimal
import logging
from time import time
from typing import TYPE_CHECKING, List, Optional, Set

from sqlalchemy import select, distinct, delete

from src.conf.logger import init_logging
from src.db.models import Bars2, Bars1, ErrorLog
from src.db.config import DBSession

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
BATCH_COUNT = 20_000


class Errors:
    SYMBOL_NOT_PRESENT = '{symbol} not present in tables_bars_1 on {date}'
    NOT_BIGGER_THAN_MINIMUM = '{symbol} close price is not bigger than the minimum over the past 10 days on {date}'
    NO_RECORDS_FOUND = 'No values available in bars_2'

    def __init__(self, db_session: 'Session') -> None:
        self._errors: List[ErrorLog] = []
        self.db_session = db_session

    def add(self, row: Optional[Bars2], message: str) -> None:
        """Add new error"""
        self._errors.append(ErrorLog(
            message=message,
            symbol=row.symbol if row else None,
            date=row.date if row else None,
        ))

    def flush(self) -> None:
        self.db_session.add_all(self._errors)


class Worker:
    def __init__(self, batch_count: int, db_session: 'Session'):
        self.batch_count = batch_count
        self.db_session = db_session
        self._bars_1_symbols: Set[str] = set()
        self._add_bars_1: List[Bars1] = []
        self._rows: List[Bars2] = []
        self._rows_ids: List[int] = []
        self._errors = Errors(db_session)

    def run(self) -> None:
        """Run the analysis for next batch of rows"""
        t0 = time()

        self._prepare()
        if not self._rows:
            logger.info('No rows found')
            self._errors.add(None, Errors.NO_RECORDS_FOUND)
        else:
            for idx, row in enumerate(self._rows):
                self._handle_row(row)
                if (idx + 1) % 1000 == 0:
                    logger.info(f'Analyzed {idx + 1} rows')

            self._delete_rows()
            self._errors.flush()
            self.db_session.add_all(self._add_bars_1)

        self.db_session.commit()
        logger.info(f'Finished analyzing {len(self._rows_ids)} rows in {time() - t0} seconds')

    def _handle_row(self, row: Bars2):
        """Run the analysis for one row from the batch"""
        self._rows_ids.append(row.id)
        if row.symbol not in self._bars_1_symbols:
            self._errors.add(row, Errors.SYMBOL_NOT_PRESENT.format(symbol=row.symbol, date=row.date))

        min_last_10_days = self._get_min_for_last_n_days(row)
        if not min_last_10_days.is_nan() and row.close and row.close > min_last_10_days:
            self._add_bars_1.append(Bars1.from_bars_2(row))
        else:
            self._errors.add(row, Errors.NOT_BIGGER_THAN_MINIMUM.format(symbol=row.symbol, date=row.date))

    def _prepare(self) -> None:
        """Prepare and cache data that is needed for further calculations"""
        self._bars_1_symbols = self._get_bars_1_symbols()
        self._rows = self._get_next_rows()

    def _get_min_for_last_n_days(self, row: Bars2, days: int = 10) -> Decimal:
        """TODO: Finish"""
        return Decimal()

    def _delete_rows(self) -> None:
        """Delete rows after analysis"""
        query = delete(Bars2).where(Bars2.id.in_(self._rows_ids))
        self.db_session.execute(query)
        logger.info(f'Deleted {len(self._rows_ids)} rows')

    def _get_bars_1_symbols(self) -> Set[str]:
        """Get distinct symbols from bars_1"""
        query = select(distinct(Bars1.symbol))
        result = self.db_session.execute(query)
        r = result.scalars().fetchall()
        return set(r)

    def _get_next_rows(self) -> List[Bars2]:
        """Get next batch of rows from the table"""
        query = select(Bars2).limit(BATCH_COUNT)
        result = self.db_session.execute(query)
        return result.scalars().fetchall()


if __name__ == '__main__':
    init_logging()

    with DBSession() as db_session:
        worker = Worker(BATCH_COUNT, db_session)
        worker.run()
