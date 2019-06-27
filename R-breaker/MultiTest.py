from R-breaker import TestStrategy
import time
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import numpy as np
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import logging

def my_run(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201905.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Months)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.addstrategy(TestStrategy, *arg)
    threats = cerebro.run()
    logging.basicConfig(filename='all_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = threats[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = threats[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%.2f,%s,%s' % (arg[0],final_value,sharp,drawdown)
    print(out_message)
    logging.info(out_message)

if __name__ == '__main__':
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=38)
    logging.info('begin')

    start = time.time()
    period = 720
    params = []

    for period in range(720,14400,720):
        params.append([period])


    print(params)
    pool.map(my_run, params)
    logging.info('1.log')

    pool.shutdown(wait=True)
    print(time.time() - start)
