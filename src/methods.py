import pandas as pd
from time import strptime
from datetime import datetime, timedelta


def apply_strptime(data_list: list, format: str):
    [strptime(x, format) for x in data_list]


def apply_strptime_with_memos(data_list: list, format: str):
    memos = dict()
    for x in data_list:
        if x in memos:
            r = memos[x]
        else:
            d = strptime(x, format)
            memos[x] = d


def apply_prebuilt_memos(data_list: list, format: str, start_time: datetime, end_time: datetime):

    memos = dict()
    timestamp = start_time
    while timestamp <= end_time:
        timestamp += timedelta(seconds=1)
        memos[timestamp.strftime(format)] = timestamp

    r = list(map(lambda x: memos.get(x, None), data_list))


def apply_pd_to_datetime(data_list: list, infer=False, format=None, split=1):
    split_n = int(len(data_list) / split)
    for i in range(0, split):
        out = pd.to_datetime(data_list[(i)*split_n : (i+1)*(split_n)], infer_datetime_format=infer, format=format)
