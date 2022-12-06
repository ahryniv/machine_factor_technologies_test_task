import pandas as pd
import pytest

from parquet_web_socket.data_iterator import HistoricalDataIterator


def test_timestamp_required():
    """Test that 'timestamp' column is required in HistoricalDataIterator"""
    df = pd.DataFrame(data=[
        {'id': 0, 'not_timestamp': 1111111111111, 'some_value': 3},
        {'id': 1, 'not_timestamp': 1111111111111, 'some_value': 123},
        {'id': 2, 'not_timestamp': 1111111111111, 'some_value': 3312312},
        {'id': 3, 'not_timestamp': 1111111111111, 'some_value': 312322},
    ])
    with pytest.raises(AssertionError) as err_info:
        HistoricalDataIterator(df)
    assert err_info.value.args[0] == '"timestamp" column is expected in DataFrame'


def test_data_iterator():
    """Test that HistoricalDataIterator yields proped data"""
    df = pd.DataFrame(data=[
        {'id': 0, 'timestamp': 1111111111111, 'expected_batch_count': 3},
        {'id': 1, 'timestamp': 1111111111111, 'expected_batch_count': 3},
        {'id': 2, 'timestamp': 1111111111111, 'expected_batch_count': 3},
        {'id': 3, 'timestamp': 2222222222222, 'expected_batch_count': 1},
        {'id': 4, 'timestamp': 3333333333333, 'expected_batch_count': 2},
        {'id': 5, 'timestamp': 3333333333333, 'expected_batch_count': 2},
        {'id': 6, 'timestamp': 4444444444444, 'expected_batch_count': 2},
        {'id': 7, 'timestamp': 4444444444444, 'expected_batch_count': 2},
    ])
    data_iter = HistoricalDataIterator(df)
    ids_iterated = set()
    for trades in data_iter:
        assert len(trades) == trades[0].expected_batch_count
        assert {trade.timestamp for trade in trades} == {trades[0].timestamp}
        ids_iterated.update([trade.id for trade in trades])
    assert ids_iterated == {0, 1, 2, 3, 4, 5, 6, 7}
