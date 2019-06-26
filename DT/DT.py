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


futures_like = True

if futures_like:
    commission, margin, mult = 2.0, 2000.0, 10.0
else:
    commission, margin, mult = 0.005, None, 1

# Create a Stratey
class DT(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        time = self.datas[0].datetime.time(0)
        print('%s, %s ,%s' % (dt.isoformat(), time, txt))

    def __init__(self,period, order_period, kx, ks):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

        # To keep track of pending orders
        self.trade_amount_percentage = 0.4
        self.is_buy = True
        self.is_sell = True

        self.period = period
        # 1d/4h/1h
        self.order_period = order_period
        self.kx = kx
        self.ks = ks

        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.order_buy = None
        self.order_buy_stop = None
        self.order_sell = None
        self.order_sell_stop = None
        self.order_buy_stop_back_up =None
        self.order_sell_stop_back_up = None

        # self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=1000)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Amount %.3f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm, order.executed.value / order.executed.price))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Amount %.3f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm, order.executed.value / order.executed.price))

            self.bar_executed = len(self)

        elif order.status in [order.Margin, order.Rejected]:
            self.log('Order Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def cancel_all_order(self):
        if self.order_sell:
            self.cancel(self.order_sell)
            self.order_sell = None
        if self.order_buy:
            self.cancel( self.order_buy)
            self.order_buy = None
        # if self.buy_order_one:
        #     self.cancel(self.buy_order_one)
        #     self.buy_order_one = None
        # if self.buy_order_two:
        #     self.cancel(self.buy_order_two)
        #     self.buy_order_two = None
        # if self.stop_loss_order:
        #     self.cancel(self.stop_loss_order)
        #     self.stop_loss_order = None

    def put_order(self, current_state = None):
        if current_state is None:
            self.trade_amount = round(self.cerebro.broker.getcash() / self.dataopen * self.trade_amount_percentage, 2)

            self.cancel_all_order()

            HH = 0
            HC = 0
            LC = 1000000
            LL = 1000000

            for num in range(self.period, -1):
                if HH < self.datahigh[num]:
                    HH = self.datahigh[num]

            for num in range(self.period, -1):
                if HC < self.dataclose[num]:
                    HC = self.dataclose[num]

            for num in range(self.period, -1):
                if LL > self.datalow[num]:
                    LL = self.datalow[num]

            for num in range(self.period, -1):
                if LC < self.dataclose[num]:
                    LC = self.dataclose[num]

            range_here = max(HH - LC, HC - LL)
            up_track = self.dataopen[0] + range_here * self.ks
            down_track = self.dataopen[0] - range_here * self.kx

            self.order_buy = self.buy(exectype=bt.Order.Stop, price=up_track,
                                      size=self.trade_amount)
            self.order_sell = self.sell(exectype=bt.Order.Stop, price=down_track,
                                        size=self.trade_amount)

        if current_state is 'long':
            self.cancel_all_order()
            HH = 0
            HC = 0
            LC = 1000000
            LL = 1000000

            for num in range(self.period, -1):
                if HH < self.datahigh[num]:
                    HH = self.datahigh[num]

            for num in range(self.period, -1):
                if HC < self.dataclose[num]:
                    HC = self.dataclose[num]

            for num in range(self.period, -1):
                if LL > self.datalow[num]:
                    LL = self.datalow[num]

            for num in range(self.period, -1):
                if LC < self.dataclose[num]:
                    LC = self.dataclose[num]

            range_here = max(HH - LC, HC - LL)
            up_track = self.dataopen[0] + range_here * self.ks
            down_track = self.dataopen[0] - range_here * self.kx

            short_amount = abs(self.position.size) + round(
                self.cerebro.broker.getvalue() / self.dataopen * self.trade_amount_percentage, 2)

            self.order_sell = self.sell(exectype=bt.Order.Stop, price=down_track,
                                        size=short_amount)

        if current_state is 'short':
            self.cancel_all_order()
            HH = 0
            HC = 0
            LC = 1000000
            LL = 1000000

            for num in range(self.period, -1):
                if HH < self.datahigh[num]:
                    HH = self.datahigh[num]

            for num in range(self.period, -1):
                if HC < self.dataclose[num]:
                    HC = self.dataclose[num]

            for num in range(self.period, -1):
                if LL > self.datalow[num]:
                    LL = self.datalow[num]

            for num in range(self.period, -1):
                if LC < self.dataclose[num]:
                    LC = self.dataclose[num]

            range_here = max(HH - LC, HC - LL)
            up_track = self.dataopen[0] + range_here * self.ks
            down_track = self.dataopen[0] - range_here * self.kx

            long_amount = abs(self.position.size) + round(
                self.cerebro.broker.getvalue() / self.dataopen * self.trade_amount_percentage, 2)

            self.order_sell = self.buy(exectype=bt.Order.Stop, price=up_track,
                                       size=long_amount)




    def next(self):

        if self.position.size == 0:
            if self.datas[0].datetime.time(0).minute == 00 and len(self) > abs(self.period):

                if self.order_period == '1d':
                    if self.datas[0].datetime.time(0).hour is 0:
                        self.put_order()
                elif self.order_period == '4h':
                    if self.datas[0].datetime.time(0).hour in [0,4,8,12,16,20,24]:
                        self.put_order()
                elif self.order_period == '1h':
                    self.put_order()

        if self.position.size > 0:
            if self.datas[0].datetime.time(0).minute == 00 and len(self) > abs(self.period):

                if self.order_period == '1d':
                    if self.datas[0].datetime.time(0).hour is 0:
                        self.put_order(current_state='long')
                elif self.order_period == '4h':
                    if self.datas[0].datetime.time(0).hour in [0,4,8,12,16,20,24]:
                        self.put_order(current_state='long')
                elif self.order_period == '1h':
                    self.put_order(current_state='long')


        if self.position.size < 0:
            if self.datas[0].datetime.time(0).minute == 00 and len(self) > abs(self.period):

                if self.order_period == '1d':
                    if self.datas[0].datetime.time(0).hour is 0:
                        self.put_order(current_state='short')
                elif self.order_period == '4h':
                    if self.datas[0].datetime.time(0).hour in [0,4,8,12,16,20,24]:
                        self.put_order(current_state='short')
                elif self.order_period == '1h':
                    self.put_order(current_state='short')





if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(DT)

    # Create a Data Feed
    # parase_dates = True是为了读取csv为dataframe的时候能够自动识别datetime格式的字符串，big作为index
    # 注意，这里最后的pandas要符合backtrader的要求的格式
    dataframe = pd.read_csv('../datas/xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)


    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    # set commission scheme -- CHANGE HERE TO PLAY
    cerebro.broker.setcommission(commission=0.0006)

    # Print out the starting conditions

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
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