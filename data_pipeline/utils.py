from datetime import datetime


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


def calculate_datediff(last_order_ts, dt=None):
    if not dt:
        dt = datetime.utcnow()
    else:
        dt = datetime.strptime(dt.split('.')[0], '%Y-%m-%d %H:%M:%S')
    last_order_ts = last_order_ts.split('.')[0]
    last_order = datetime.strptime(last_order_ts, '%Y-%m-%d %H:%M:%S')
    datediff = (dt - last_order).days
    return datediff
