# -*- coding: utf-8 -*-
import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import time



def crawl_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n') 
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    close = pd.DataFrame({k: d['收盤價'] for k, d in data.items()}).transpose()
    close.index = pd.to_datetime(close.index)
    close
    return ret

data = {}
n_days = 2000
date = datetime.datetime.now()
fail_count = 0
allow_continuous_fail_count = 5
while len(data) < n_days:

    print('parsing', date)
    try:
        data[date] = crawl_price(date)
        print('success!')
        fail_count = 0
    except:
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break

    date -= datetime.timedelta(days=1)
    time.sleep(10)
