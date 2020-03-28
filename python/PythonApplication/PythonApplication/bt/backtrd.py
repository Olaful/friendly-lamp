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


def set_cash(cash=0.0):
    cash = cash or 100000.0
    print("set cash: ", cash)
    cerebro.broker.setcash(cash)


def add_sizer(sizer=None, stake=10):
    cerebro.addsizer(sizer, stake=stake)


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


def add_strategy(add_type=0, **kwargs):
    if add_type == 0:
        cerebro.addstrategy(TestStrategy)
    else:
        # opt strategy
        cerebro.optstrategy(
            TestStrategy,
            **kwargs
        )


def plot():
    cerebro.plot()


class TestStrategy(bt.Strategy):
    """ 
    use param with self.params.name,
    you can try any param value
    until found the best value
    """
    params = (
        ('exitbars', 5),
        ('maperiod', 15),
        ('emaperiod', 25),
        ('wmaperiod', 25),
        ('smarsiperiod', 10),
        ('tmprsi', None),
        ('printlog', False),
    )
    
    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # first data change everyday
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = None

        self._init_indicator()

    def _init_indicator(self):
        indicator_enabled = {
            'sma': 1,
            'ema': 0,
            'wma': 0,
            'stochastic_slow': 0,
            'macd': 0,
            'rsi': 0,
            'smarsi': 0,
            'atr': 0
        }

        for ind, enabled in indicator_enabled.items():
            if not enabled:
                continue
            init_ind_method = getattr(self, '_init_'+ind, None)
            if callable(init_ind_method):
                init_ind_method()
            else:
                self.log('_init_%s method is not callable' % ind)

    def _init_sma(self):
        """
        sma indicator added to the strategy
        so the first trading day will be maperiod bars occurs
        """
        self.sma = bt.indicators.MovingAverageSimple(
            self.datas[0],
            period=self.params.maperiod
        )

    def _init_ema(self):
        """
        because of using self.datas, so indicators will autoregister with the strategy
        and will have a influence to the first trading day
        """
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.emaperiod)

    def _init_wma(self):
        bt.indicators.WeightedMovingAverage(self.datas[0], period=self.params.wmaperiod, subplot=True)

    def _init_stochastic_slow(self):
        """
        RSV = (CLOSE-MIN(N)) / (MAX(N) - MIN(N))*100
        MARSV = EMA(RSV)
        K = MA(MARSV)
        D = MA(K)
        general param: N = 9, M = 3
        """
        bt.indicators.StochasticSlow(self.datas[0])

    def _init_macd(self):
        bt.indicators.MACDHisto(self.datas[0])

    def _init_rsi(self):
        self.params.tmprsi = bt.indicators.RSI(self.datas[0])

    def _init_smarsi(self):
        bt.indicators.SmoothedMovingAverage(self.params.tmprsi, period=self.params.smarsiperiod)

    def _init_atr(self):
        bt.indicators.RSI(self.datas[0], plot=False)

    def falling_buy(self):
        """
        self.dataclose[0] current
        self.dataclose[-1] pre
        self.dataclose[-2] pre of pre
        len(self.dataclose) tell you how
        many bars passed
        """
        if not (self.dataclose[0] < self.dataclose[-1]):
            return False
        if self.dataclose[-1] < self.dataclose[-2]:
            return True
        
        return False

    def gt_sma_buy(self):
        if self.dataclose[0] > self.sma[0]:
            self.log('Sma: %.2f' % self.sma[0])
            return True
        return False

    def pass_bars_sell(self):
        # pos up to 5 d
        if len(self) >= self.bar_executed + self.params.exitbars:
            return True
        return False

    def lt_sma_sell(self):
        if self.dataclose[0] < self.sma[0]:
            self.log('Sma: %.2f' % self.sma[0])
            return True
        return False

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
        # broker could reject order if not enough cash
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

    def stop(self):
        self.log('(MA period %2d) Ending Value %.2f'
        % (self.params.maperiod, self.broker.getvalue()), doprint=True)

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        # cannot send a 2nd one
        if self.order:
            return

        # if not yet in market, might buy
        if not self.position:
            if self.gt_sma_buy():
                self.log('Buy create, %.2f' % self.dataclose[0])
                # if order at the last day, executed next trading day 
                self.order = self.buy()
        else:
            if self.lt_sma_sell():
                self.log('Sell Create, %.2f' % self.dataclose[0])
                self.order = self.sell()


def main():
    start_value()
    """
    The system will execute the strategy for each value of the range
    """
    add_strategy(add_type=1, maperiod=range(10, 31))
    add_data_feed()
    set_cash(cash=1000.0)
    """
    Multiplied cash for order, so the profit and loss
    will mutiplied
    """
    add_sizer(sizer=bt.sizers.FixedSize, stake=10)
    set_commission(commission=0.00)

    run()

    final_value()


if __name__ == '__main__':
    main()
