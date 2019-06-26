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

    def __init__(self,period = 1860,period_sell = 1380,b = 1,b_sell = 1,trail_percentage = 0.03,trail_percentage_sell = 0.04,back_stop_order_percentage = 1.02,back_stop_order_percentage_sell = 1.05):
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
        self.trade_amount_percentage = 0.6
        self.is_buy = True
        self.is_sell = False
        self.period = max(period,period_sell)
        self.smaband =  bt.indicators.SMAEnvelope(period = period,perc = b)
        self.smaband_sell =  bt.indicators.SMAEnvelope(period = period_sell,perc = b_sell)
        self.trail_percentage_sell = trail_percentage_sell  # 测试范围 0.015-0.03，步长0.001
        self.trail_percentage_buy = trail_percentage
        self.back_stop_order_percentage_sell = back_stop_order_percentage_sell  # 测试范围 1.005-1.02，步长0.001
        self.back_stop_order_percentage_buy = back_stop_order_percentage
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
        if self.position.size == 0 and len(self) > self.period and self.datas[0].datetime.time().hour == 00:
            self.cancel_all_orders()
            self.trade_amount = round(self.cerebro.broker.getcash() / self.dataopen * self.trade_amount_percentage)

            if self.is_buy:
                self.order_buy = self.buy(exectype=bt.Order.Stop, price= self.smaband.top,
                                          size=self.trade_amount)
            if self.is_sell:
                self.order_sell = self.sell(exectype=bt.Order.Stop, price=self.smaband_sell.bot,
                                            size=self.trade_amount)

        elif self.position.size < 0:
            self.order_sell = None
            '''if self.order_sell_stop_back_up is None:
                self.order_sell_stop_back_up = self.buy(size = abs(self.position.size),exectype= bt.Order.Stop, price = self.sellprice* (self.backup_percent + 1))

            self.cancel(self.order_sell_stop)
            self.order_sell_stop =  self.buy(size=abs(self.position.size),exectype= bt.Order.Stop, price = self.sma.sma,oco = self.order_sell_stop_back_up)'''
            if self.order_buy:
                self.cancel(self.order_buy)
                self.order_buy = None
            if self.order_sell_stop is None and self.order_sell_stop_back_up is None:
                self.order_sell_stop_back_up = self.buy(size=abs(self.position.size), exectype=bt.Order.Stop,
                                                        price=self.position.price * self.back_stop_order_percentage_sell)
                self.order_sell_stop = self.buy(size=abs(self.position.size), exectype=bt.Order.StopTrail,
                                                trailpercent=self.trail_percentage_sell
                                                , oco=self.order_sell_stop_back_up)

        elif self.position.size > 0:
            self.order_buy = None
            '''if self.order_buy_stop_back_up is None:
                self.order_buy_stop_back_up = self.sell(size = abs(self.position.size),exectype= bt.Order.Stop,price = self.buyprice * (1-self.backup_percent))

            self.cancel(self.order_buy_stop)
            self.order_buy_stop =  self.sell(size=abs(self.position.size),exectype= bt.Order.Stop, price = self.sma.sma,oco = self.order_buy_stop_back_up)'''
            if self.order_sell:
                self.cancel(self.order_sell)
                self.order_sell = None
            if not self.order_buy_stop and not self.order_buy_stop_back_up:
                self.order_buy_stop_back_up = self.sell(size=abs(self.position.size), exectype=bt.Order.Stop,
                                                        price=self.position.price / self.back_stop_order_percentage_buy)
                self.order_buy_stop = self.sell(size=abs(self.position.size), exectype=bt.Order.StopTrail,
                                                trailpercent=self.trail_percentage_buy
                                                , oco=self.order_buy_stop_back_up)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    #dataframe = pd.read_csv('xbtusd_data_201701-201712.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201701-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201801-201812.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('xbtusd_data_201901-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('ethusd_data_201808-201905.csv', index_col=0, parse_dates=[0])
    #dataframe = pd.read_csv('2019-05.csv', index_col=0, parse_dates=[0])
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0006)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe = bt.TimeFrame.Months)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    thestrats = cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Sharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis()['sharperatio'])
    print('DrawDown:', thestrats[0].analyzers.mydrawdown.get_analysis().max.drawdown)
    cerebro.plot()
