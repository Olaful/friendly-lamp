import itertools
import backtrader as bt
import datetime
import util


class MyCSVData1(bt.CSVDataBase):
    def start(self):
        "will run more times if optimization will be run"
        pass

    def stop(self):
        "Your clen-up code here"

    def _loadline(self, linetokens):
        i = itertools.count(0)

        dt_txt = linetokens[next(i)]

        y = int(dt_txt[0:4])
        m = int(dt_txt[5:7])
        d = int(dt_txt[8:10])

        dt = datetime.datetime(y, m, d)
        dt_num = dt.timestamp()

        # value in place with linetokens
        self.lines.datetime[0] = dt_num
        self.lines.open[0] = float(linetokens[next(i)])
        self.lines.high[0] = float(linetokens[next(i)])
        self.lines.low[0] = float(linetokens[next(i)])
        self.lines.close[0] = float(linetokens[next(i)])
        self.lines.volume[0] = float(linetokens[next(i)])
        self.lines.openinterest[0] = float(linetokens[next(i)])

        # will return false if you don't want the data
        return True


class MyCVData2(bt.feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y/%m/%d'), # change the formatting of date
    )


class MyCSVData3(bt.feeds.BacktraderCSVData):
    params = (
        ("dataname", util.absolute_path('datas', '2006-day-001.txt')),
    )


class MyCSVData4(bt.feeds.BacktraderCSVData):
    params = (
        ("dataname", util.absolute_path('datas', '2006-week-001.txt')),
    )


class MyData3(bt.feed.DataBase):
    def __init__(self):
        ''

    def start(self):
        ''

    def stop(self):
        ''

    def _load(self):
        ''
