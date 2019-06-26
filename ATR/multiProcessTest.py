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

# class multirunner():
#     def __init__(self):
#         dataframe = pd.read_csv('../datas/ethusd_data.csv', index_col=0, parse_dates=[0])
#         dataframe['openinterest'] = 0
#         data = bt.feeds.PandasData(dataname=dataframe)
#         self.cerebro = bt.Cerebro()
#         self.cerebro.adddata(data)
#         self.cerebro.broker.setcash(100000.0)
#         self.cerebro.broker.setcommission(commission=0.0006)
#
#     def multirun(self, message):
#         self.cerebro.addstrategy(TestStrategy, *message)
#         self.cerebro.run()
#         print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
#
#     if __name__ == '__main__':
#         start = time.time()
#         pool = ProcessPoolExecutor(max_workers=2)
#         future1 = pool.submit(multirun, [0.021, 1.01, 1.021])
#         future2 = pool.submit(multirun, [0.021, 1.01, 1.031])
#         print(time.time()-start)

def my_run(arg):

    dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe,fromdate = datetime.datetime(2018,1,1),todate = datetime.datetime(2018,12,30))
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
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()'''

def my_run2(arg):

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
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

if __name__ == '__main__':
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=38)
    logging.info('begin')
    # pool = multiprocessing.Pool(processes=2)
    # params = [[0.021, 1.01, i] for i in np.arange(1.015, 1.019, 0.002)]
    # pool.map(my_run, params)
    # for param in params:
    #     print(param)
    #     pool.submit(my_run, (param))
    # pool.shutdown(wait=True)
    # # results = pool.map(my_run, params)
    # for result in results:
    #     print(result)
    # for result in pool.map(my_run, params):
    #     print(result)
    # future_to_result = {pool.submit(my_run, param): param for param in params}
    # for param in params:
    #     pool.apply_async(my_run, (param,))
    # pool.close()
    # pool.join()
    start = time.time()
    i = 0.01 #trail_percentage
    j = 1.01 #back stop percentage
    k = 3 #devfactors
    l = 1440 #periods
    params = []
    while i < 0.051:
        while j < 1.041:
            while k <7.1:
                while l < 2881:
                    params.append([i,j,k,l])
                    l+= 120
                l = 1440
                k+=1
            l= 1440
            k= 3
            j+=0.01
        l = 1440
        k = 3
        j = 1.01
        i+=0.01


    '''pool.map(my_run, params)
    logging.info('1.log')'''
    pool.map(my_run2, params)
    '''pool.map(my_run3, params)
    logging.info('3.log')
    pool.map(my_run4, params)
    logging.info('4.log')
    pool.shutdown(wait=True)'''
    print(time.time() - start)
    # for i in [1.015, 1.017, 1.019]:
    #     pool.submit(my_run, ([0.021, 1.01, i]))
    # future1 = pool.submit(my_run, ([0.021, 1.01, 1.015]))
    # future2 = pool.submit(my_run, ([0.021, 1.01, 1.017]))
    # future2 = pool.submit(my_run, ([0.021, 1.01, 1.019]))
    # print(time.time() - start)

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
