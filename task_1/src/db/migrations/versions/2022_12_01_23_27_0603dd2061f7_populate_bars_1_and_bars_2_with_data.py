"""Populate bars_1 and bars_2 with data

Revision ID: 0603dd2061f7
Revises: 545290734080
Create Date: 2022-12-01 23:27:54.039555

"""
from decimal import Decimal, InvalidOperation
import logging
from time import time
import csv
from itertools import islice
from typing import Optional
import threading

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0603dd2061f7'
down_revision = '545290734080'
branch_labels = None
depends_on = None

logger = logging.getLogger(__name__)

LOAD_CHUNK_SIZE = 50000
BARS_1_TABLENAME = 'bars_1'
BARS_2_TABLENAME = 'bars_2'


def _to_decimal(value: str) -> Optional[Decimal]:
    """Tries to convert string value to Decimal. If fails return None"""
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def populate_bars_from_csv(
    filename: str,
    table: sa.Table,
    conn: sa.engine.Connection,
) -> None:
    """Populates bars table with data from the CSV file"""

    t_start = time()
    rows_populated = 0

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        while True:
            rows = [{
                'date': row['Date'],
                'symbol': row['Symbol'],
                'adj_close': _to_decimal(row['Adj Close']),
                'close': _to_decimal(row['Close']),
                'high': _to_decimal(row['High']),
                'low': _to_decimal(row['Low']),
                'open': _to_decimal(row['Open']),
                'volume': _to_decimal(row['Volume']),
            } for row in islice(reader, LOAD_CHUNK_SIZE)]
            if not rows:
                break
            rows_populated += len(rows)
            conn.execute(table.insert(), rows)

    logger.info(f'Populated {rows_populated} rows to table "{table}" '
                f'in {time() - t_start} seconds.')


def upgrade() -> None:
    """Load data to bars tables from CSV files"""

    conn = op.get_bind()
    meta = sa.MetaData(bind=conn)
    meta.reflect()

    threads = []
    for tablename, filename in (
        (BARS_1_TABLENAME, 'src/data/bars_1.csv'),
        (BARS_2_TABLENAME, 'src/data/bars_2.csv'),
    ):
        table = sa.Table(tablename, meta)
        thread = threading.Thread(
            target=populate_bars_from_csv,
            args=(filename, table, conn)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def downgrade() -> None:
    """Truncate bars tables"""

    conn = op.get_bind()
    meta = sa.MetaData(bind=conn)
    meta.reflect()
    for tablename in [BARS_1_TABLENAME, BARS_2_TABLENAME]:
        table = sa.Table(tablename, meta)
        conn.execute(table.delete())
