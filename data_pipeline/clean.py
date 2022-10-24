import os
import pandas as pd


class Dataset:
    def __init__(self, country_code: str = None):
        """
        Create a dataset for voucher selection
        :param country_code: selected country code, optional
        :return:
        """
        self._path = os.getcwd() + '/data/data.parquet.gzip'
        self._raw_data = None
        self.clean_data = None
        self._read_data()
        self._filter_country_code(country_code)

    def update_field_voucher_amount(self):
        if 'voucher_amount' in self.clean_data.columns:
            self.clean_data.voucher_amount = self.clean_data.voucher_amount.fillna(0)
        self.convert_string_or_float_to_integer('voucher_amount')

    def update_field_total_orders(self):
        if 'total_orders' in self.clean_data.columns:
            self.clean_data.loc[(self.clean_data.total_orders == ''), 'total_orders'] = 0
        self.convert_string_or_float_to_integer('total_orders')

    def update_field_timestamp(self):
        self.convert_string_to_timestamp('timestamp')

    def update_field_last_order_ts(self):
        self.convert_string_to_timestamp('last_order_ts')

    def convert_string_to_timestamp(self, column_name):
        if column_name not in ('timestamp', 'last_order_ts', 'first_order_ts'):
            raise TypeError(f"Perform conversion on the wrong column: {column_name}")
        self.clean_data[column_name] = pd.to_datetime(self.clean_data[column_name], utc=True)

    def convert_string_or_float_to_integer(self, column_name):
        if column_name not in ('total_orders', 'voucher_amount'):
            raise TypeError(f"Perform conversion on the wrong column: {column_name}")
        self.clean_data[column_name] = self.clean_data[column_name].astype(float).astype(int)

    def deduplication(self):
        self.clean_data.drop_duplicates(keep='first', inplace=True)

    def _read_data(self):
        try:
            self._raw_data = pd.read_parquet(self._path, engine='pyarrow')
        except Exception as e:
            raise e
        self._country_code_lowercase()

    def _country_code_lowercase(self):
        self._raw_data.country_code = self._raw_data.country_code.str.lower()

    def _filter_country_code(self, country):
        if country:
            self.clean_data = self._raw_data[self._raw_data.country_code == country.lower()]
        else:
            self.clean_data = self._raw_data

    def add_date_diff(self):
        self.clean_data['created_at'] = pd.Timestamp.utcnow()
        self.clean_data['date_diff'] = (self.clean_data['created_at'] - self.clean_data['last_order_ts']).dt.days
