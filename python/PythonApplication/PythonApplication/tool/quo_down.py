import requests
import datetime
import sqlite3


conn = sqlite3.connect('sqlite.db')
db = conn.cursor()

try:
    query_sql = 'SELECT 1 FROM `tb_hisbar_day`'
    db.execute(query_sql)
except:
    create_table_sql = """CREATE TABLE `tb_hisbar_day` (
      `date1` date NOT NULL, -- '日期'
      `symbol` char(32) NOT NULL, -- '标的'
      `open` decimal(12,4) NOT NULL, -- '开盘价'
      `high` decimal(12,4) NOT NULL, -- '最高价'
      `low` decimal(12,4) NOT NULL, -- '最低价'
      `close` decimal(12,4) NOT NULL, -- '收盘价'
      `volume` unsigned bigint(20) NOT NULL DEFAULT '0', -- '成交量'
      `turnover` unsigned double(20,2) NOT NULL DEFAULT '0.00', -- '成交额'
      PRIMARY KEY (`date1`,`symbol`)
    )"""
    db.execute(create_table_sql)

db_param = {'host': 'localhost', 'port': 3306,
            'user': 'root', 'password': '123',
            'database': 'test', 'charset': 'utf8mb4',
            'autocommit': True}

symbols = ['003816']

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  + 'Chrome/71.0.3578.98 Safari/537.36'
}


def fetch_his_quo(symbol, is_index=False, startdate='', enddate=''):
    """
    fetch hisquo
    :param symbol:
    :return:
    """
    print(f"Get hisquo of {symbol}")
    symbol = 'cn_' + symbol if not is_index else 'zs_' + symbol

    today = datetime.datetime.today()
    before_3_days = today - datetime.timedelta(days=360)

    today = str(today.date()).replace('-', '')
    before_3_days = str(before_3_days.date()).replace('-', '')

    startdate = startdate or before_3_days
    enddate = enddate or today

    startdate = startdate.replace('-', '')
    enddate = enddate.replace('-', '')

    url = f'http://q.stock.sohu.com/hisHq?code={symbol}' \
          f'&start={startdate}&end={enddate}&stat=1&order=D' \
          '&period=d'
    resp = requests.get(url, headers=req_headers)
    rls = resp.json()
    return rls[0]['hq']


def to_db(hqs, symbol):
    """
    to db
    :param hqs:
    :param symbol:
    :return:
    """
    print(f"Data of {symbol} to db")
    insert_thd_sql = "REPLACE INTO `tb_hisbar_day`" \
                     "(`date1`, `symbol`, `open`, " \
                     "`high`, `low`, `close`, `volume`," \
                     " `turnover`) VALUES('{date1}'," \
                     " '{symbol}', {open}, {high}, {low}," \
                     " {close}, {volume}, {turnover})"
    for day_hq in hqs:
        print(f"...{day_hq[0]}")
        insert_param = {'date1': day_hq[0], 'symbol': symbol,
                        'open': day_hq[1], 'high': day_hq[6],
                        'low': day_hq[5], 'close': day_hq[2],
                        'volume': day_hq[7], 'turnover': day_hq[8]}
        db.execute(insert_thd_sql.format(**insert_param))

    conn.commit()


def his_quo(symbol, startdate=None, enddate=None, num=180, is_index=False):
    """
    history quotation
    :param symbol:
    :return:
    """
    startdate = startdate if startdate else ''
    enddate = enddate if enddate else str(datetime.datetime.today().date())

    query_sql = f'SELECT `date1`, `open`, `high`, `low`, `close` ' \
        f' FROM `tb_hisbar_day` WHERE `symbol` = "{symbol} CH Equity" AND' \
        f' `date1` BETWEEN "{startdate}" AND "{enddate}"' \
        f' ORDER BY `date1` DESC LIMIT {num}'

    db.execute(query_sql)
    hisquo_info = db.fetchall()

    if not hisquo_info:
        hq = fetch_his_quo(symbol, is_index, startdate, enddate)
        to_db(hq, symbol + ' CH Equity')

        db.execute(query_sql)
        hisquo_info = db.fetchall()

    date = [c[0] for c in hisquo_info]
    open = [float(c[1]) for c in hisquo_info]
    high = [float(c[2]) for c in hisquo_info]
    low = [float(c[3]) for c in hisquo_info]
    close = [float(c[4]) for c in hisquo_info]

    date, open, high, low, close = list(reversed(date)), \
                                   list(reversed(open)), \
                                   list(reversed(high)), \
                                   list(reversed(low)), \
                                   list(reversed(close)),

    return date, open, high, low, close


def last_quo(symbol):
    """
    last quotation
    :param symbol:
    :return:
    """
    if symbol.startswith('60'):
        mk_code = 'sh'
    elif symbol.startswith('00') or symbol.startswith('30'):
        mk_code = 'sz'
    else:
        mk_code = ''

    url = f'http://hq.sinajs.cn/list={mk_code}{symbol}'
    resp = requests.get(url, headers=req_headers)
    quo_data = resp.text
    quo_data = quo_data.split(',')

    date, open, high, low, close = quo_data[30], quo_data[1], \
                                   quo_data[4], quo_data[5],\
                                   quo_data[3]

    return date, open, high, low, close


def main():
    rls = his_quo('000001', is_index=False)
    test = 1


if __name__ == '__main__':
    main()
