import pandas as pd
from tushare import get_realtime_quotes
from quotool import his_quo, last_quo
from stk_data import ma, pre_ma


def is_look_up_from_bottom(symbol, down_days=4):
    """
    if look up from the bottom
    """
    last_quo = get_realtime_quotes(symbol)
    last_price = float(last_quo.price.iloc[0])
    last_open = float(last_quo.open.iloc[0])

    if last_price < last_open:
        return False

    last_date = last_quo.date.iloc[0] 
    day_bars = his_quo(symbol, num=4+down_days)
    first_his_date = str(day_bars[0]['date'])

    if first_his_date < last_date:
        day_bars.insert(
            {
                'date': last_date, 
                'open': last_open,
                'close': last_price
            },
            0
        )

    last_1_bar = day_bars[0]
    last_2_bar = day_bars[1]

    if last_1_bar['close'] > last_1_bar['open'] and \
     last_2_bar['close'] > last_2_bar['open']:
        pre_bars = day_bars[2:]
    else:
        pre_bars = day_bars[1:]

    closes = [bar['close'] for bar in pre_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))
    
    decline_days = 0
    for p_c in pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        if day_rtn > 0:
            return False

        decline_days += 1
        if decline_days == down_days:
            return True

    return False


def is_kdj_gf(symbol):
    """
    if product fork of kdj
    :param symbol:
    :return:
    """
    day_bars = his_quo(symbol)

    date, open, high, low, close = [], [], [], [], []
    for bar in day_bars:
        date.append(bar['date'])
        open.append(bar['open'])
        high.append(bar['high'])
        low.append(bar['low'])
        close.append(bar['close'])

    date.reverse()
    open.reverse()
    high.reverse()
    low.reverse()
    close.reverse()

    quo_info = last_quo(symbol)
    last_date, last_open, last_high, last_low, last_close = quo_info['date'],\
                                                            quo_info['open'],\
                                                            quo_info['high'],\
                                                            quo_info['low'],\
                                                            quo_info['close']

    date.append(last_date)
    open.append(float(last_open))
    high.append(float(last_high))
    low.append(float(last_low))
    close.append(float(last_close))

    df_kdj = pd.DataFrame({'date': date, 'open': open,
                           'high': high, 'low': low, 'close': close})

    day = 9
    df_kdj['max'] = df_kdj['high'].rolling(window=day, min_periods=1).max()
    df_kdj['min'] = df_kdj['low'].rolling(window=day, min_periods=1).min()

    tmp_k = 50
    tmp_d = 50
    k_list = [tmp_k]
    d_list = [tmp_d]

    tmp_df_kdj = df_kdj[1:]

    for idx, row in tmp_df_kdj.iterrows():
        rsv = (row['close'] - row['min']) /\
              (row['max'] - row['min']) * 100
        k = rsv / 3 + tmp_k * 2 / 3
        tmp_k = k
        k_list.append(k)

        d = k / 3 + tmp_d * 2 / 3
        tmp_d = d
        d_list.append(d)

    df_kdj['k'] = k_list
    df_kdj['d'] = d_list
    df_kdj['j'] = df_kdj['k'] * 3 - df_kdj['d'] * 2
    df_kdj['k_pre'] = df_kdj['k'].shift(1)
    df_kdj['d_pre'] = df_kdj['d'].shift(1)

    def jude_buy(x):
        if x['k_pre'] < x['d_pre'] and x['k'] > x['d']:
            return 1
        return 0

    def jude_sell(x):
        if x['k_pre'] > x['d_pre'] and x['k'] < x['d']:
            return 1
        return 0

    df_kdj['buy_sig'] = df_kdj.apply(jude_buy, axis=1)
    df_kdj['sell_sig'] = df_kdj.apply(jude_sell, axis=1)

    print(f'PRE_K:{df_kdj["k"].iloc[-2]}, PRE_D:{df_kdj["d"].iloc[-2]}')
    print(f'    K:{df_kdj["k"].iloc[-1]},     D:{df_kdj["d"].iloc[-1]}')

    return df_kdj['buy_sig'].iloc[-1]


def is_last_price_gt_ma30(symbol):
    """
    if last price gt ma30
    :param symbol:
    :return:
    """
    ma_30 = ma(symbol, freq='D', ma_num=30)
    last_price = 0.0
    quo = get_realtime_quotes(symbol)
    if quo.empty is not True:
        last_price = float(quo.price.iloc[0])

    return last_price > ma_30


def is_break_through_ma5(symbol, pre_days=3):
    """
    if break through ma5
    :param symbol:
    :param pre_days
    :return:
    """
    assert pre_days >= 0

    quo = get_realtime_quotes(symbol)
    last_price = float(quo.price.iloc[0])
    last_date = str(quo.date.iloc[0])

    day_bars = his_quo(symbol, startdate=None, enddate=None, num=5+pre_days, is_index=False)

    dates, closes = [], [],
    for bar in day_bars:
        dates.append(bar['date'])
        closes.append(bar['close'])

    dates.reverse()
    closes.reverse()

    if last_date != dates[-1]:
        dates.append(last_date)
        closes.append(last_price)

    df_ma = pd.DataFrame({'date': dates, 'close': closes})

    df_ma['ma5'] = df_ma['close'].rolling(window=5, min_periods=1).mean()
    df_ma['diff'] = df_ma['close'] - df_ma['ma5']
    df_ma['pre_diff'] = df_ma['diff'].shift(1)
    df_ma['cross_up'] = df_ma.apply(lambda x: 1 if x['pre_diff'] <= 0 < x['diff'] else 0, axis=1)

    cross_up = False

    for i in range(pre_days):
        ma_info = df_ma.iloc[-pre_days]
        if ma_info.cross_up == 0:
            continue

        print(f"{symbol} {ma_info.date} last price({last_price}) cross up ma5({ma_info.ma5})")
        cross_up = True
        break

    return cross_up


def is_moderate_heavy_vol(symbol, heavy_percent=0.13):
    """
    if moderate heavy volume
    :param symbol:
    :param heavy_percent:
    :return:
    """
    quo = get_realtime_quotes(symbol)

    last_price = float(quo.price.iloc[0])
    open_price = float(quo.open.iloc[0])

    if last_price < open_price:
        return False

    day_bars = his_quo(symbol, num=1)
    yesday_bar = day_bars[0]

    yesday_close = float(yesday_bar['close'])
    yesday_open = float(yesday_bar['open'])

    if yesday_close < yesday_open:
        return False

    last_volume = float(quo.volume.iloc[0])
    yesday_volume = float(yesday_bar['volume']) * 100

    if last_volume < yesday_volume:
        return False

    volume_change = last_volume / yesday_volume - 1

    if volume_change > heavy_percent:
        return False

    return True


if __name__ == "__main__":
    rls = is_look_up_from_bottom('000960', down_days=2)
    pass
