from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader.analyzers as btanalyzers
import datetime, time
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor

# Import the backtrader platform
import backtrader as bt
from backtrader import indicators

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        time = self.datas[0].datetime.time(0)
        print('%s, %s ,%s' % (dt.isoformat(), time, txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.bolling = bt.indicators.BBands(period = 60, devfactor = 5) #period测试范围 1440-2880 步长120  devfactor 测试范围 3-7 步长0.5
        self.bolling_order = bt.indicators.BBands(period = 20, devfactor = 5)
        self.other_break_rate = None
        self.trail_percentage_sell = 0.01
        self.trail_percentage_buy = 0.01
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.order_buy = None
        self.order_buy_stop = None
        self.order_sell = None
        self.order_sell_stop = None
        self.order_buy_stop_back_up = None
        self.order_sell_stop_back_up = None
        self.order_bolling_profit_backup = None
        self.trade_amount_percentage = 0.6
        self.is_buy = True
        self.is_sell = False
        self.order_completed_time = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            #self.order_completed_time = len(self)
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Margin, order.Rejected]:
            self.log('Order Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        if self.position.size == 0 and self.datas[0].datetime.time().minute == 00 and len(self) > 59:
            self.trade_amount = round(self.cerebro.broker.getcash() / self.dataopen * self.trade_amount_percentage)

            if self.order_sell:
                self.cancel(self.order_sell)
                self.order_sell = None
            if self.order_sell_stop:
                self.cancel(self.order_sell_stop)
                self.order_sell_stop = None
            if self.order_buy:
                self.cancel(self.order_buy)
                self.order_buy = None
            if self.order_buy_stop:
                self.cancel(self.order_buy_stop)
                self.order_buy_stop = None
            if self.order_buy_stop_back_up:
                self.cancel(self.order_buy_stop_back_up)
                self.order_buy_stop_back_up = None
            if self.order_sell_stop_back_up:
                self.cancel(self.order_sell_stop_back_up)
                self.order_sell_stop_back_up = None

            if self.is_buy:
                self.order_buy = self.buy(exectype=bt.Order.Stop, price= self.bolling.top,
                                          size=self.trade_amount)
            if self.is_sell:
                self.order_sell = self.sell(exectype=bt.Order.Stop, price= self.bolling.bot,
                                            size=self.trade_amount)



        elif self.position.size < 0:
            self.order_sell = None
            '''if self.order_buy:
                self.cancel(self.order_buy)
                self.order_buy = None
            if self.order_sell_stop is None and self.order_sell_stop_back_up is None:
                # self.log(self.position)
                self.order_sell_stop_back_up = self.buy(size=abs(self.position.size), exectype=bt.Order.Stop,
                                                        price=self.position.price * self.back_stop_order_percentage_sell)
                self.order_sell_stop = self.buy(size=abs(self.position.size), exectype=bt.Order.StopTrail,
                                                trailpercent=self.trail_percentage_sell
                                                , oco=self.order_sell_stop_back_up)'''

            if self.order_bolling_profit_backup is not None:
                self.cancel(self.order_bolling_profit_backup)
                self.order_bolling_profit_backup =  None

            if self.datas[0].datetime.time().minute in range(0,60,5) and self.order_bolling_profit_backup is not None:
                self.cancel(self.order_bolling_profit_backup)
                self.order_bolling_profit_backup =  None
                self.order_bolling_profit_backup = self.sell(size = abs(self.position.size),exectype = bt.Order.Stop,
                                                            price = self.bolling_order.top)

            if self.order_sell_stop is None:
                self.order_sell_stop = self.buy(size=abs(self.position.size), exectype=bt.Order.StopTrail,
                                                trailpercent= self.trail_percentage_sell,oco = self.order_bolling_profit_backup)

        elif self.position.size > 0:
            self.order_buy = None
            '''if self.order_sell:
                self.cancel(self.order_sell)
                self.order_sell = None
            if not self.order_buy_stop and not self.order_buy_stop_back_up:
                self.order_buy_stop_back_up = self.sell(size=abs(self.position.size), exectype=bt.Order.Stop,
                                                        price=self.position.price / self.back_stop_order_percentage_buy)
                self.order_buy_stop = self.sell(size=abs(self.position.size), exectype=bt.Order.StopTrail,
                                                trailpercent=self.trail_percentage_buy
                                                , oco=self.order_buy_stop_back_up)'''
            '''if self.order_bolling_profit_backup is None:
                self.order_bolling_profit_backup = self.sell(size = abs(self.position.size),exectype = bt.Order.Stop,
                                                            price = self.bolling_order.top)

            if self.datas[0].datetime.time().minute in range(0,60,5) and self.order_bolling_profit_backup is not None:
                self.cancel(self.order_bolling_profit_backup)
                self.order_bolling_profit_backup =  None
                self.order_bolling_profit_backup = self.sell(size = abs(self.position.size),exectype = bt.Order.Stop,
                                                            price = self.bolling_order.top)'''

            if self.order_buy_stop is None:
                self.order_buy_stop = self.sell(size=abs(self.position.size), exectype=bt.Order.StopTrail,
                                                trailpercent= self.trail_percentage_buy
                                                , oco=self.order_bolling_profit_backup)

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Create a Data Feed
    # parase_dates = True是为了读取csv为dataframe的时候能够自动识别datetime格式的字符串，big作为index
    # 注意，这里最后的pandas要符合backtrader的要求的格式
    dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    #data = bt.feeds.PandasData(dataname=dataframe)
    data = bt.feeds.PandasData(dataname=dataframe)


    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000000.0)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    # set commission scheme -- CHANGE HERE TO PLAY
    cerebro.broker.setcommission(commission=0.0006)

    # Print out the starting conditions

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe = bt.TimeFrame.Months)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    # Run over everything
    # pool = ProcessPoolExecutor(max_workers=6)
    thestrats = cerebro.run()

    # Print out the final result
    '''以下是需要记录的结果'''
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Sharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis())
    print('DrawDown:', thestrats[0].analyzers.mydrawdown.get_analysis())
    # Plot the result
    '''以上是需要记录的结果'''
    cerebro.plot()
