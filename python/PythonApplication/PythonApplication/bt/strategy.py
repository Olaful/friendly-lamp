import backtrader as bt
import backtrader.indicators as btind
from indicator import TestInd


class DataLenStrategy(bt.Strategy):
    params = (
        ('datalines', False),
        ('lendetails', False),
    )

    def __init__(self):
        bt.indicators.SMA()
        bt.indicators.Stochastic()
        bt.indicators.RSI()
        bt.indicators.MACD()
        bt.indicators.CCI()
        TestInd().plotinfo.plot = False

    def next(self):
        if self.p.datalines:
            txt = ','.join(
                [
                    '%04d' % len(self),
                    '%04d' % len(self.data0),
                    self.datetime.date(0).isoformat()
                ]
            )

            print(txt)

    def loglendetails(self, msg):
        if self.p.lendetails:
            print(msg)

    def stop(self):
        super(DataLenStrategy, self).stop()

        tlen = 0
        tline = 0

        self.loglendetails('-- Evaluating datas')
        for i, data in enumerate(self.datas):
            tdata = 0
            for line in data.lines:
                tdata += len(line.array)
                tline = len(line.array)

            tlen += tdata
            logtxt = '---- Data {} Total Cells {} Cells per Line {}'
            self.loglendetails(logtxt.format(i, tdata, tline))

        self.loglendetails('-- Evaluating Indicators')
        for i, ind in enumerate(self.getindicators()):
            tlen += self.rindicator(ind, i, 0)

        self.loglendetails('-- Evaluating Observers')
        for i, obs in enumerate(self.getobservers()):
            tobs = 0
            for line in obs.lines:
                tobs += len(line.array)
                tline = len(line.array)

            tlen += tobs
            logtxt = '---- Observer {} Total Cells {} Cells per Line {}'
            self.loglendetails(logtxt.format(i, tobs, tline))

        print("Total memory cells used: {}".format(tlen))

    def rindicator(self, ind, i, deep):
        tind = 0
        tline = 0
        for line in ind.lines:
            tind += len(line.array)
            tline = len(line.array)

        tsub = 0
        for j, sind in enumerate(ind.getindicators()):
            tsub += self.rindicator(sind, j, deep+1)

        iname = ind.__class__.__name__.split('.')[-1]
        logtxt = '---- Indicator {}.{} {} Total Cells {} Cells per Line {}'
        self.loglendetails(logtxt.format(deep, i, iname, tind, tline))

        logtxt = '---- SubIndicators {}.{} {} Total Cells {}'
        self.loglendetails(logtxt.format(deep, i, iname, tsub))

        return tind + tsub


class SMAStrategy(bt.Strategy):
    params = (
        ('period', 10),
        ('onlydaily', False),
    )

    def __init__(self):
        self.sma_small_tf = btind.SMA(self.data, period=self.p.period)
        if not self.p.onlydaily:
            self.sma_large_tf = btind.SMA(self.data1, period=self.p.period)

    def nextstart(self):
        """
        get called if the larger period products a values
        :return:
        """
        print("-" * 20)
        print("nextstart called with len", len(self))
        print("-" * 20)

        super(SMAStrategy, self).nextstart()


class SMAStragegy2(bt.Strategy):
    params = (
        ('period', 10),
    )

    def __init__(self):
        self.sma = btind.SMA(self.data, period=self.p.period)

    def start(self):
        self.counter = 0

    def prenext(self):
        self.counter += 1
        print("prenext len %d - counter %d" % (len(self), self.counter))

    def next(self):
        self.counter += 1
        print("--next len %d - counter %d" % (len(self), self.counter))

