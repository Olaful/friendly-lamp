import backtrader as bt


# create broker instantce in the backgroud
cerebro = bt.Cerebro()


def run():
    print("run")
    cerebro.run()


def basic_setup():
    print("Starting Portfolio Value: %.2f" % cerebro.broker.get_value())
    cerebro.run()
    print("Final Portfolio Value: %.2f" % cerebro.broker.get_value())

    # set cash for broker
    cerebro.broker.setcash(100000.0)
    print("New Portfolio Value: %.2f" % cerebro.broker.get_value())


def start_value():
    print("Starting Portfolio Value: %.2f" % cerebro.broker.get_value())


def final_value():
    """
    finale value determine by everyday return
    finale value = sum(pnlcomm of day) + start value
    """
    print("Final Portfolio Value: %.2f" % cerebro.broker.get_value())


def set_cash(cash=0):
    cash = cash or 100000.0
    print("set cash: ", cash)
    cerebro.broker.setcash(cash)


def set_commission(commission=0.001):
    cerebro.broker.setcommission(commission=commission)


def add_data_feed():
    import datetime, os
    modpath = os.path.dirname(__file__)
    data_path = r'datas/orcl-1995-2014.txt'
    full_name = os.path.join(modpath, data_path)

    data = bt.feeds.YahooFinanceCSVData(
        dataname = full_name,
        fromdate = datetime.datetime(2000, 1, 1),
        todate = datetime.datetime(2001, 1, 3),
        reverse=False
    )

    print("add data")

    cerebro.adddata(data)


def add_strategy():
    cerebro.addstrategy(TestStrategy)


class TestStrategy(bt.Strategy):
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # first data change everyday
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def falling_buy(self):
        """
        self.dataclose[0] current
        self.dataclose[-1] pre
        self.dataclose[-2] pre of pre
        len(self.dataclose) tell you how
        many bars passed
        """
        if not (self.dataclose[0] < self.dataclose[-1]):
            return
        if self.dataclose[-1] < self.dataclose[-2]:
            self.log('Buy create, %.2f' % self.dataclose[0])
            # if order at the last day, executed next trading day 
            self.order = self.buy()

    def notify_order(self, order):
        # nofify order next day

        if order.status in [order.Submitted, order.Accepted]:
            """
            Pending order
            Buy/Sell order submitted/accepted
            to/by broker - Nothing to do
            """
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Buy executed, Price: %.2f, Cost:%.2f, Comm: %.2f' % 
                (order.executed.price, order.executed.value, order.executed.comm)
                )
            if order.issell():
                self.log('Sell executed, Price: %.2f, Cost:%.2f, Comm: %.2f' % 
                (order.executed.price, order.executed.value, order.executed.comm)
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        # pnl: profit and loss
        self.log('Operation Profit, Gross %.2f, Net %.2f' % 
        (trade.pnl, trade.pnlcomm)
        )

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        # cannot send a 2nd one
        if self.order:
            return

        # if not yet in market, might buy
        if not self.position:
            self.falling_buy()
        else:
            # pos up to 5 d
            if len(self) >= self.bar_executed + 5:
                self.log('Sell Create, %.2f' % self.dataclose[0])
                self.order = self.sell()


def main():
    start_value()
    add_strategy()
    add_data_feed()
    set_cash(100000.0)
    set_commission(0.001)

    run()

    final_value()


if __name__ == '__main__':
    main()
