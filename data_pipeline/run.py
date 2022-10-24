from .clean import Dataset
from .db import DB
from .utils import create_frequent_segment, create_recency_segment


class Run:
    """
    Run data pipeline
    """

    def __init__(self):
        self.db = DB()
        self.db.create_main_table()
        self.db.create_segment_table()
        self.dataset = Dataset(country_code='peru')
        self._generate_dataset()
        self.db.insert_into_main_table(self.dataset.clean_data.to_dict(orient='records'))

    def _voucher_segments(self):
        self.dataset.add_date_diff()
        self.dataset.clean_data['frequent_segment'] = \
            self.dataset.clean_data['total_orders'].apply(create_frequent_segment)
        self.dataset.clean_data['recency_segment'] = self.dataset.clean_data['date_diff'].apply(create_recency_segment)

    def build_segment_data(self, segment_name):
        """
        Build segment data of each segment name
        :param segment_name: frequent_segment or recency_segment
        :return:
        """
        self.dataset.add_date_diff()
        self._voucher_segments()
        segment = self.dataset.clean_data.groupby([segment_name, 'voucher_amount']).count()\
            .sort_values(['total_orders'], ascending=False)
        segment['row_num'] = segment.groupby([segment_name]).cumcount() + 1
        segment.reset_index(inplace=True)
        segemnt_table = segment[segment['row_num'] == 1][[segment_name, 'voucher_amount']]
        segemnt_table.columns = ['segment_name', 'voucher_amount']
        self.db.insert_into_segment_table(segemnt_table.to_dict(orient='records'))

    def _generate_dataset(self):
        self.dataset.update_field_voucher_amount()
        self.dataset.update_field_total_orders()
        self.dataset.update_field_timestamp()
        self.dataset.update_field_last_order_ts()
        self.dataset.deduplication()

