import json
import requests
import pymysql
import datetime

db_param = {'host': 'localhost', 'port': 3306,
            'user': 'root', 'password': '123',
            'database': 'test', 'charset': 'utf8mb4',
            'autocommit': True}

mysql = pymysql.connect(**db_param)
db = mysql.cursor()

symbols = ['000300']


def get_his_quo(symbol):
    """
    get hisquo
    :param symbol:
    :return:
    """
    print(f"Get hisquo of {symbol}")
    symbol = 'cn_' + symbol if symbol.find('000300') == -1 else 'zs_' + symbol

    today = datetime.datetime.today()
    before_3_days = today - datetime.timedelta(days=90)

    today = str(today.date()).replace('-', '')
    before_3_days = str(before_3_days.date()).replace('-', '')

    url = f'http://q.stock.sohu.com/hisHq?code={symbol}' \
          f'&start={before_3_days}&end={today}&stat=1&order=D' \
          '&period=d'
    resp = requests.get(url)
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


def main():
    for symbol in symbols:
        hq = get_his_quo(symbol)
        to_db(hq, symbol + ' CH Equity')


if __name__ == '__main__':
    main()
