import pandas as pd
from quotool import his_quo
from tushare import get_realtime_quotes
from baostock import query_dividend_data
from baostock import login as bao_stk_login


_BAOSTOCK_LOGIN = False


def ma(symbol, freq='D', ma_num=10):
    """
    ma
    :param symbol:
    :param freq:
    :param ma_num:
    :return:
    """
    if freq != 'D':
        print("Only support dayline")
        return None

    day_line_bars = day_bars(symbol, num=ma_num, qfq=True)

    closes = [bar['close'] for bar in day_line_bars]

    ma_value = sum(closes) / len(closes)

    return ma_value


def pre_ma(symbol, freq='D', ma_num=10, pre_days=1):
    """
    ma of sepcify previous days
    :param symbol:
    :param ma_num:
    :param pre_days:
    :param freq
    :return:
    """
    if freq != 'D':
        print("Only support dayline")
        return None

    day_line_bars = day_bars(symbol, num=ma_num + pre_days, qfq=True)

    closes = [bar['close'] for bar in day_line_bars]

    pre_closes = closes[pre_days - 1:pre_days - 1 + ma_num]

    ma_value = sum(pre_closes) / len(pre_closes)

    return ma_value


def day_bars(symbol, num=180, qfq=True):
    """
    day bar
    """
    quo = get_realtime_quotes(symbol)
    last_date = quo.date.iloc[0]

    day_line_bars = his_quo(symbol, num=num)
    first_his_date = str(day_line_bars[0]['date'])

    if first_his_date < last_date:
        day_line_bars.insert(
            0,
            {
                'date': last_date, 
                'open': float(quo.open.iloc[0]),
                'high': float(quo.high.iloc[0]),
                'low': float(quo.low.iloc[0]),
                'close': float(quo.price.iloc[0]),
                'volume': float(quo.volume.iloc[0]) / 100,
            }
        )

    if not qfq:
        return day_line_bars[:num]

    global _BAOSTOCK_LOGIN
    if not _BAOSTOCK_LOGIN:
        _BAOSTOCK_LOGIN = bao_stk_login()

    year = first_his_date[:4]
    rs_list = []
    code = f"sh.{symbol}" if symbol.startswith('60') else f"sz.{symbol}"
    rs_dividend = query_dividend_data(code=code, year=year, yearType="report")

    while (rs_dividend.error_code == '0') & rs_dividend.next():
        rs_list.append(rs_dividend.get_row_data())

    if not rs_list:
        return day_line_bars[:num]

    result_dividend = pd.DataFrame(rs_list, columns=rs_dividend.fields)
    cash_dividend = result_dividend.dividCashPsBeforeTax.iloc[0]
    cash_dividend = float(cash_dividend) if cash_dividend else 0.0
    stock_dividend = result_dividend.dividReserveToStockPs.iloc[0]
    stock_dividend = float(stock_dividend) if stock_dividend else 0.0

    if not stock_dividend:
        stock_dividend = result_dividend.dividStocksPs.iloc[0]
        stock_dividend = float(stock_dividend) if stock_dividend else 0.0

    date_dividend = result_dividend.dividPayDate.iloc[0]

    for day_bar in day_line_bars:
        if not day_bar['date'] < date_dividend:
            continue
        day_bar['open'] = round((day_bar['open'] - cash_dividend) / (1 + stock_dividend), 2)
        day_bar['high'] = round((day_bar['high'] - cash_dividend) / (1 + stock_dividend), 2)
        day_bar['low'] = round((day_bar['low'] - cash_dividend) / (1 + stock_dividend), 2)
        day_bar['close'] = round((day_bar['close'] - cash_dividend) / (1 + stock_dividend), 2)

    return day_line_bars[:num]


if __name__ == '__main__':
    rls = day_bars('603707', qfq=True)
    pass
