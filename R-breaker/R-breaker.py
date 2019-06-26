from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader.analyzers as btanalyzers
import datetime, time
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor

import backtrader as bt
from backtrader import indicators

class TestStrategy(bt.Strategy):

    def __init__(self,period = 1440*2):

        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.other_break_rate = None
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sellprice = None
        self.sellcomm = None
        self.order_buy = None
        self.order_buy_stop = None
        self.order_sell = None
        self.order_sell_stop = None
        self.order_buy_stop_back_up = None
        self.order_sell_stop_back_up = None
        self.trade_amount_percentage = 0.4

        self.period = period
        self.time = 0
        self.signal = 0
        self.Ssetup = 0
        self.Bsetup = 0
        self.Senter = 0
        self.Benter = 0
        self.Bbreak = 0
        self.Sbreak = 0

        self.is_buy = is_buy
        self.is_sell = is_sell
        self.is_print = True

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        time = self.datas[0].datetime.time(0)
        if self.is_print:
            print('%s, %s ,%s' % (dt.isoformat(), time, txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
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
                self.sellprice = order.executed.price
                self.sellcomm = order.executed.comm

            self.bar_executed = len(self)

        elif order.status in [order.Margin, order.Rejected]:
            self.log('Order Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        '''self.last_trade_length = len(self)
        self.trade_pnlcom = trade.pnlcomm'''

    def cancel_all_orders(self):
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

    def next(self):
        if len(self)-self.time == self.period:

            self.HH = 0
            self.LL = 1000000
            for num in range(-self.period, -1):
                if self.HH < self.datahigh[num]:
                    self.HH = self.datahigh[num]
            for num in range(-self.period, -1):
                if self.LL > self.datalow[num]:
                    self.LL = self.datalow[num]

            self.Ssetup = self.HH + 0.35*(self.dataclose[-1]- self.LL)
            self.Bsetup = self.LL - 0.35*(self.HH - self.dataclose[-1])
            self.Senter = 1.07/2*(self.HH + self.LL) - 0.07*self.LL
            self.Benter = 1.07/2*(self.HH + self.LL) - 0.07*self.HH
            self.Bbreak = self.Ssetup + 0.25*(self.Ssetup - self.Bsetup)
            self.Sbreak = self.Bsetup - 0.25*(self.Ssetup - self.Bsetup)

            self.signal = 0

            self.time = len(self)

        if len(self) > self.period and len(self)-self.time > 0 and len(self)-self.time < self.period:
            self.trade_amount = round(self.cerebro.broker.getcash() / self.dataopen * self.trade_amount_percentage)
            if self.dataclose > self.Bbreak:
                if self.position.size == 0:
                    self.order_buy = self.buy(size = self.trade_amount)
                elif self.position.size < 0:
                    self.order_buy = self.buy(size = -self.position.size + self.trade_amount)
                else:
                    pass
            if self.dataclose > self.Ssetup:
                self.signal = 1
            if self.dataclose < self.Senter and self.signal == 1:
                self.signal = 0
                if self.position.size == 0:
                    self.order_sell = self.sell(size = self.trade_amount)
                elif self.position.size > 0:
                    self.order_sell = self.sell(size = self.position.size + self.trade_amount)
                else:
                    pass

            if self.dataclose < self.Sbreak:
                if self.position.size == 0:
                    self.order_sell = self.sell(size = self.trade_amount)
                elif self.position.size >0:
                    self.order_sell = self.sell(size = self.position.size + self.trade_amount)
                else:
                    pass
            if self.dataclose < self.Bsetup:
                self.signal = -1
            if self.dataclose > self.Benter and self.signal == -1:
                self.signal = 0
                if self.position.size == 0:
                    self.order_buy = self.buy(size= self.trade_amount)
                elif self.position.size < 0 :
                    self.order_buy = self.buy(size = -self.position.size + self.trade_amount)
                else:
                    pass


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    #dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    dataframe = pd.read_csv('xbtusd_data_201701-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('2019-05.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe = bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    thestrats = cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Sharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis()['sharperatio'])
    print('DrawDown:', thestrats[0].analyzers.mydrawdown.get_analysis().max.drawdown)
    cerebro.plot()
