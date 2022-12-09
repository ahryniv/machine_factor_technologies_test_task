"""NOT FINISHED.
This solution is not working correctly.

I didn't find a proper way how to analyze the part with min of 10 records from bars_1 table
and do it efficiently to fit into 30 seconds.
"""

from src.conf.logger import init_logging
from src.db.config import DBSession
from src.task_1_2 import Worker

BATCH_COUNT = 20_000


if __name__ == '__main__':
    init_logging()

    with DBSession() as db_session:
        worker = Worker(BATCH_COUNT, db_session)
        worker.run()
