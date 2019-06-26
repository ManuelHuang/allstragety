from DT import DT
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

    dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_06.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')

    cerebro.addstrategy(DT, *arg)
    cerebro.run()
    logging.basicConfig(filename='all_results.log', level=logging.DEBUG)

    final_value = cerebro.broker.getvalue()
    sharp = cerebro.run()[0].analyzers.mysharpe.get_analysis()
    drawdown = cerebro.run()[0].analyzers.mydrawdown.get_analysis()
    print(final_value)
    print(sharp)
    print(drawdown)


    # 以csv格式输出，以逗号分割，五个值分别为trail_percentage, back_stop_order_percentage, ks_kx, period和Final Portfolio Value
    out_message = '%s,%s,%s,%s,%.2f,%s,%s' % (arg[0], arg[1], arg[2], arg[3], final_value,sharp,drawdown)
    # out_message = str(arg) + ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(out_message)
    logging.info(out_message)
    # return out_message
    # print(out_message) 
    # logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # return 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

def my_run2(arg):
    dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_05.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addstrategy(TestStrategy_sell, *arg)
    cerebro.run()
    logging.basicConfig(filename='test_12_05_buy.log', level=logging.DEBUG)

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

def my_run3(arg):
    dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_05.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0006)

    cerebro.addstrategy(TestStrategy, *arg)
    cerebro.run()
    logging.basicConfig(filename='test_12_05_sell.log', level=logging.DEBUG)

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
    dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_2019_06.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0006)
    cerebro.addstrategy(TestStrategy_sell, *arg)
    cerebro.run()
    logging.basicConfig(filename='test_08_12_buy.log', level=logging.DEBUG)

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
    pool = ProcessPoolExecutor(max_workers=16)
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
    i = -7200 #period
    j = '1d' #order_period
    k = 0.2 #kx
    l = 0.2 #ks
    params = []
    # while i < -1439:
    #     while k <1.046:
    #             while l < 2:
    params.append([i,j,k,l])
        #             l+= 0.2
        #         l = 0.2
        #         k+=0.2
        # l = 0.2
        # k = 0.2
        # i+=1440


    pool.map(my_run, params)
    logging.info('1.log')
    # pool.map(my_run2, params)
    # logging.info('2.log')
    # pool.map(my_run3, params)
    # logging.info('3.log')
    # pool.map(my_run4, params)
    # logging.info('4.log')

    pool.shutdown(wait=True)
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
