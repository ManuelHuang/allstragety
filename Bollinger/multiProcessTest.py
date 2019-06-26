from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from Stragety import TestStrategy
from Stragety2 import TestStrategy2
import backtrader as bt
import pandas as pd
import numpy as np
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import logging
import backtrader.analyzers as btanalyzers
import datetime, time
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])


def my_run(arg):

    #dataframe = pd.read_csv('xbtusd_data_201701-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_06.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    dataframe = pd.read_csv('2019-05.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addstrategy(TestStrategy2, *arg)
    cerebro.run()
    logging.basicConfig(filename='all_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    out_message = '%s,%s,%s,%s,%s,%s,%s,%s,%.2f' % (arg[0], arg[1], arg[2], arg[3],arg[4], arg[5], arg[6], arg[7], final_value)
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()'''

'''def my_run2(arg):

    dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addstrategy(TestStrategy2, *arg)
    cerebro.run()
    logging.basicConfig(filename='all_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%.2f' % (arg[0], arg[1], arg[2], arg[3], final_value)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()'''
'''def my_run3(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_06.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe,fromdate = datetime.datetime(2017,1,1),todate = datetime.datetime(2017,12,30))
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.run()
    logging.basicConfig(filename='all_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%.2f' % (arg[0], arg[1], arg[2], arg[3], final_value)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

def my_run4(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_06.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe,fromdate = datetime.datetime(2017,1,1),todate = datetime.datetime(2017,12,30))
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addstrategy(TestStrategy2, *arg)
    cerebro.run()
    logging.basicConfig(filename='all_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%.2f' % (arg[0], arg[1], arg[2], arg[3], final_value)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message)
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()'''

if __name__ == '__main__':
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=38)
    logging.info('begin')

    start = time.time()
    trail_percentage_sell = 0.03
    trail_percentage_buy = 0.04
    back_stop_order_percentage_sell = 1.03
    back_stop_order_percentage_buy = 1.02
    period_buy = 1680
    period_sell = 2040
    devfactors_buy = 2.5
    devfactors_sell = 2.5
    params = []
    #params.append( [0.04,0.05,1.04,1.03,1800,2160,3,3])
    for trail_percentage_sell in np.arange(0.03,0.05,0.005):
        for trail_percentage_buy in np.arange(0.04,0.06,0.005):
            for back_stop_order_percentage_sell in np.arange(1.03,1.05,0.005):
                for back_stop_order_percentage_buy in np.arange(1.02,1.04,0.005):
                    for period_buy in range(1680,1920,60):
                        for period_sell in range(2040,2280):
                            for devfactors_buy in np.arange(2.5,4,0.5):
                                for devfactors_sell in np.arange(2.5, 4, 0.5):
                                    params.append([trail_percentage_sell,trail_percentage_buy,back_stop_order_percentage_sell,back_stop_order_percentage_buy,period_buy,period_sell,devfactors_buy,devfactors_sell])
                                    print(params)
    #print(params)
    pool.map(my_run, params)
    logging.info('1.log')
    '''pool.map(my_run2, params)
    pool.map(my_run3, params)
    logging.info('3.log')
    pool.map(my_run4, params)
    logging.info('4.log')
    pool.shutdown(wait=True)'''
    print(time.time() - start)

