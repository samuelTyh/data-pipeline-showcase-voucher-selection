from data_pipeline import create_frequent_segment, create_recency_segment, calculate_datediff


def test_create_frequent_segment_0():
    value = 0
    assert create_frequent_segment(value) == '0-4'


def test_create_frequent_segment_undefined():
    value = 50
    assert create_frequent_segment(value) == 'undefined'


def test_create_recency_segment_0():
    value = 0
    assert create_recency_segment(value) == 'undefined'


def test_create_recency_segment_100():
    value = 100
    assert create_recency_segment(value) == '91-120'


def test_calculate_datediff():
    ts1 = '2020-04-03 19:21:46.175011+00:00'
    ts2 = '2020-04-08 19:21:46.175011+00:00'
    assert calculate_datediff(ts1, ts2) == 5


def test_calculate_datediff_int():
    ts = '2020-04-03 19:21:46.175011+00:00'
    assert isinstance(calculate_datediff(ts), int)
