from MovingAverage import TestStrategy
from MovingAverage_sell import TestStrategy_sell
import time
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import numpy as np
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import logging

def my_run(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.run()
    logging.basicConfig(filename='MovingAverage_buy_2017_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%s,%s,%s,%.2f,%s,%s' % (arg[0], arg[2], arg[4], arg[6],final_value,sharp,drawdown)
    print(out_message)
    logging.info(out_message)

def my_run2(arg):

    dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.run()
    logging.basicConfig(filename='MovingAverage_buy_2018_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%s,%s,%s,%.2f,%s,%s' % (arg[0], arg[2], arg[4], arg[6],final_value,sharp,drawdown)
    print(out_message)
    logging.info(out_message)


def my_run3(arg):

    dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy_sell, *arg)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.run()
    logging.basicConfig(filename='MovingAverage_Sell_2018_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%s,%s,%s,%.2f,%s,%s' % (arg[1],arg[3],arg[5],arg[7],final_value,sharp,drawdown)
    print(out_message)
    logging.info(out_message)


def my_run4(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy_sell, *arg)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.run()
    logging.basicConfig(filename='MovingAverage_Sell_2017_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    out_message = '%s,%s,%s,%s,%.2f,%s,%s' % (arg[1],arg[3],arg[5],arg[7],final_value,sharp,drawdown)
    print(out_message)
    logging.info(out_message)

if __name__ == '__main__':
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=38)
    logging.info('begin')

    start = time.time()
    period = 60
    b = 2
    trail_percentage = 0.01
    back_stop_order_percentage = 1.01
    params = []

    while period <= 2220:
        while b <= 5:
            while trail_percentage <= 0.05:
                while back_stop_order_percentage <= 1.05:
                    params.append([period, period, b, b, trail_percentage,trail_percentage,back_stop_order_percentage,back_stop_order_percentage])
                    back_stop_order_percentage +=0.01
                back_stop_order_percentage = 1.01
                trail_percentage += 0.01
            back_stop_order_percentage = 1.01
            trail_percentage = 0.01
            b += 1
        back_stop_order_percentage = 1.01
        trail_percentage = 0.01
        b = 1
        period += 120

    print(params)
    pool.map(my_run, params)
    logging.info('1.log')
    pool.map(my_run2, params)
    logging.info('2.log')
    pool.map(my_run3, params)
    logging.info('3.log')
    pool.map(my_run4, params)
    logging.info('4.log')


    pool.shutdown(wait=True)
    print(time.time() - start)
