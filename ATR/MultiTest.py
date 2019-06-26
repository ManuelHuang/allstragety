from ATR import TestStrategy
from ATR_sell import TestStrategy_sell
# from run_sell import TestStrategy_sell
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
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Weeks)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')

    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.run()
    logging.basicConfig(filename='ATR_buy_2017_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%s,%s,%.2f,%s,%s' % (arg[0], arg[1], arg[2], arg[3],arg[4], arg[5],final_value,sharp,drawdown)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message) 
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

def my_run2(arg):

    dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Weeks)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')

    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.run()
    logging.basicConfig(filename='ATR_buy_2018_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%s,%s,%.2f,%s,%s' % (arg[0], arg[1], arg[2], arg[3],arg[4], arg[5],final_value,sharp,drawdown)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

def my_run3(arg):

    dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Weeks)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')

    cerebro.addstrategy(TestStrategy_sell, *arg)
    cerebro.run()
    logging.basicConfig(filename='ATR_sell_2018_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%s,%s,%.2f,%s,%s' % (arg[0], arg[1], arg[2], arg[3],arg[4], arg[5],final_value,sharp,drawdown)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()


def my_run4(arg):
    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Weeks)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')

    cerebro.addstrategy(TestStrategy_sell, *arg)
    cerebro.run()
    logging.basicConfig(filename='ATR_sell_2017_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()['sharperatio']
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis().max.drawdown

    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%s,%s,%.2f,%s,%s' % (
    arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], final_value, sharp, drawdown)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

if __name__ == '__main__':
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=38)
    logging.info('begin')

    start = time.time()
    period_atr = 60
    period_sma = 60
    b = 1
    backup_percentage = 0.01
    trail_percentage = 0.01
    back_stop_order_percentage = 1.01
    params = []

    while period_atr <=2220:
        while b <= 2:
            while trail_percentage <= 0.05:
                while back_stop_order_percentage <= 1.05:
                    params.append([period_atr, period_atr, b, 0.01, trail_percentage,
                                   back_stop_order_percentage])
                    back_stop_order_percentage +=0.01
                back_stop_order_percentage = 1.01
                trail_percentage += 0.01
            back_stop_order_percentage = 1.01
            trail_percentage = 0.01
            b += 1
        back_stop_order_percentage = 1.01
        trail_percentage = 0.01
        b = 1
        period_atr += 120


    '''for period_atr in range(60,781,120):
        for period_sma in range (60,781,120):
            for b in [1,2]:
                for backup_percentage in [0.01]:
                    for trail_percentage in np.arange(0.01,0.06,0.01):
                        for back_stop_order_percentage in np.arange(1.01,1.06,0.01):
                            params.append([period_atr,period_sma,b,backup_percentage,trail_percentage,back_stop_order_percentage])'''

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


# start = time.time()
# test1 = [0.021, 1.01, 1 .021]
# cerebro.addstrategy(TestStrategy, *test1)
# cerebro.run()
# print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# test2 = [0.021, 1.01, 1.031]
# cerebro.addstrategy(TestStrategy, *test2)
# cerebro.run()
# print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
# print(time.time() - start)
