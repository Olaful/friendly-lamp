from quotool import his_quo
from tushare import get_realtime_quotes


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

    day_bars = his_quo(symbol, startdate=None, enddate=None, num=ma_num - 1, is_index=False)

    last_price = 0.0
    quo = get_realtime_quotes(symbol)
    if quo.empty is not True:
        last_price = float(quo.price.iloc[0])

    closes = [bar['close'] for bar in day_bars]
    closes.append(last_price)

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

    day_bars = his_quo(symbol, startdate=None, enddate=None, num=ma_num + pre_days, is_index=False)

    closes = [bar['close'] for bar in day_bars]

    pre_closes = closes[pre_days - 1:pre_days - 1 + ma_num]

    ma_value = sum(pre_closes) / len(pre_closes)

    return ma_value


if __name__ == '__main__':
    rls = pre_ma('000708', ma_num=5, pre_days=1)
    pass
