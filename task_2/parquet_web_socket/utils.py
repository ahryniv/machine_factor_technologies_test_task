from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


def read_parquet_file(filename: Path) -> pd.DataFrame:
    """Reads data from parquet file to pandas DataFrame"""
    table2 = pq.read_table(filename)
    return table2.to_pandas()
