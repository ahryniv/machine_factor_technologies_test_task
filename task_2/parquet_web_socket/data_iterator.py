from typing import List, Iterator, Optional, Hashable, Any, Tuple

import pandas as pd


class HistoricalDataIterator:
    """Iterator wrapper for the Pandas Dataframe

    Yields list of next rows from DataFrame with same "timestamp" value
    """

    def __init__(self, data: pd.DataFrame):
        assert 'timestamp' in data.columns, '"timestamp" column is expected in DataFrame'
        self._iter: Iterator[Tuple[Optional[Hashable], pd.Series[Any]]] = data.iterrows()  # type: ignore
        self._next_value: Optional[pd.Series[Any]] = self._get_next_value()

    def _get_next_value(self) -> Optional[pd.Series]:
        try:
            _, next_series = next(self._iter)
        except StopIteration:
            return None
        else:
            return next_series

    def __iter__(self) -> 'HistoricalDataIterator':
        return self

    def __next__(self) -> List[pd.Series]:
        if self._next_value is None:
            raise StopIteration()

        buffer: List[pd.Series] = [self._next_value]
        ts = self._next_value.timestamp

        while True:
            self._next_value = self._get_next_value()
            if self._next_value is None or self._next_value.timestamp != ts:
                break
            buffer.append(self._next_value)

        return buffer
