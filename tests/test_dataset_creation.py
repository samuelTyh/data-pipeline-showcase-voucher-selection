import pytest
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
from data_pipeline import Dataset, create_frequent_segment, create_recency_segment, calculate_datediff


@pytest.fixture()
def initialized_dataset() -> Dataset:
    dataset = Dataset(country_code='peru')
    return dataset


def test_dataset_initialization(initialized_dataset):
    assert isinstance(initialized_dataset.clean_data, pd.DataFrame)


def test_update_field_voucher_amount(initialized_dataset):
    initialized_dataset.update_field_voucher_amount()
    assert initialized_dataset.clean_data[initialized_dataset.clean_data.voucher_amount.isna()].shape[0] == 0


def test_update_field_total_orders(initialized_dataset):
    initialized_dataset.update_field_total_orders()
    assert initialized_dataset.clean_data[initialized_dataset.clean_data.total_orders == ''].shape[0] == 0


def test_update_field_timestamp(initialized_dataset):
    initialized_dataset.update_field_timestamp()
    assert is_datetime64_any_dtype(initialized_dataset.clean_data['timestamp'])


def test_update_field_last_order_ts(initialized_dataset):
    initialized_dataset.update_field_last_order_ts()
    assert is_datetime64_any_dtype(initialized_dataset.clean_data['last_order_ts'])


def test_deduplication(initialized_dataset):
    if initialized_dataset.clean_data[initialized_dataset.clean_data.duplicated()].shape[0] != 0:
        before_count = initialized_dataset.clean_data.shape[0]
        initialized_dataset.deduplication()
        after_count = initialized_dataset.clean_data.shape[0]
        assert before_count != after_count
