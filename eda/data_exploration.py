# -*- coding: utf-8 -*-
"""data_exploration.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ytCjQMrCo5grWQaXMBp_4GLBsaDTDUGU
"""

import pandas as pd

"""## Load parquet and first check"""

df = pd.read_parquet('/content/drive/MyDrive/data.parquet.gzip')

df.head(10)

df_peru = df[df.country_code == 'Peru']

df['first_order_ts'].apply(str)

"""### Lowercase the country code to match the input easier"""

df_peru.country_code = df_peru.country_code.str.lower()

"""### Exploration"""

df_peru.dtypes

df_peru.head(10)

df_peru.info()

df_peru.count()

df_peru[df_peru.total_orders == '']

count_no_total_orders = df_peru[df_peru.total_orders == ''].shape[0]

df_peru[df_peru.voucher_amount.isna()]

count_no_voucher_amount = df_peru[df_peru.voucher_amount.isna()].shape[0]

print(f'{round(count_no_total_orders/df_peru.shape[0] * 100)}% data with no correct order count')
print(f'{round(count_no_voucher_amount/df_peru.shape[0] * 100)}% data with no voudher amount')

"""### Clean and create dataset"""

df_peru.voucher_amount = df_peru.voucher_amount.fillna(0)

df_peru_update_voucher_amount = df_peru.copy()
df_peru_update_voucher_amount.voucher_amount = df_peru_update_voucher_amount.voucher_amount.astype(int)

df_peru_update_voucher_amount.head(10)

df_peru_total_orders_update = df_peru_update_voucher_amount.copy()
df_peru_total_orders_update.loc[(df_peru_total_orders_update.total_orders == ''), 'total_orders'] = 0

df_peru_total_orders_update.total_orders = df_peru_total_orders_update.total_orders.astype(float).astype(int)

df_peru_total_orders_update.head(10)

df_peru_update_timestamp = df_peru_total_orders_update.copy()
df_peru_update_timestamp.timestamp = pd.to_datetime(df_peru_update_timestamp.timestamp, utc=True)
df_peru_update_timestamp.last_order_ts = pd.to_datetime(df_peru_update_timestamp.last_order_ts, utc=True)

df_peru_update_timestamp.info()

df_peru_update_timestamp[df_peru_update_timestamp.duplicated()]

df_peru_deduplicate = df_peru_update_timestamp.drop_duplicates(keep='first')

df_peru_deduplicate.shape

df_peru_deduplicate.head(10)

df_peru_deduplicate

"""### Create segments"""

add_date = df_peru_deduplicate.copy()
add_date['created_at'] = pd.Timestamp.utcnow()

add_date['time_diff'] = (add_date['created_at'] - add_date['last_order_ts']).dt.days

add_date

df['frequent_segment'] = None
df['recency_segment'] = None

def create_frequent_segment(value):
    if value in range(0, 5):
        frequent_segment = '0-4'
    elif value in range(5, 14):
        frequent_segment = '5-13'
    elif value in range(14, 38):
        frequent_segment = '14-37'
    else:
        frequent_segment = 'undefined'
    return frequent_segment

def create_recency_segment(value):
    value = int(value)
    if value in range(30, 61):
        recency_segment = '30-60'
    elif value in range(61, 91):
        recency_segment = '61-90'
    elif value in range(91, 121):
        recency_segment = '91-120'
    elif value > 180:
        recency_segment = '180+'
    else:
        recency_segment = 'undefined'
    return recency_segment

add_segment = add_date.copy()
add_segment['frequent_segment'] = add_segment['total_orders'].apply(create_frequent_segment)

add_segment['recency_segment'] = add_segment['time_diff'].apply(create_recency_segment)

"""### Search mode value"""

f = add_segment.groupby(['frequent_segment', 'voucher_amount']).count().sort_values(['total_orders'], ascending=False)
f

r = add_segment.groupby(['recency_segment', 'voucher_amount']).count().sort_values(['total_orders'], ascending=False)
r

f['rnum'] = f.groupby(['frequent_segment']).cumcount() + 1
r['rnum'] = r.groupby(['recency_segment']).cumcount() + 1

f.reset_index(inplace=True)
r.reset_index(inplace=True)

new_f = f[f['rnum']== 1][['frequent_segment', 'voucher_amount']]
new_r = r[r['rnum']== 1][['recency_segment', 'voucher_amount']]

new_f.columns = ['segment_name', 'voucher_amount']
new_r.columns = ['segment_name', 'voucher_amount']

new_f

new_r