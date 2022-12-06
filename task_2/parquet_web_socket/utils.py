from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq


def read_parquet_file(filename: Path) -> pd.DataFrame:
    """Reads data from parquet file to pandas DataFrame"""
    table = pq.read_table(filename)
    return table.to_pandas()


def pandas_json_encoder(obj: Any) -> Any:
    """Returns ready for json encoding value for pandas types"""
    if type(obj) == pd.Series:
        return obj.to_dict()
    elif type(obj) == pd.Timestamp:
        return obj.timestamp()
    raise
