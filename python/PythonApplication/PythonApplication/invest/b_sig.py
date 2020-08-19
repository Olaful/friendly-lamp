import pandas as pd
from tushare import get_realtime_quotes
from stk_data import ma, pre_ma, day_bars


def is_look_up_from_bottom(symbol, down_days=4):
    """
    if look up from the bottom
    """
    last_quo = get_realtime_quotes(symbol)
    last_price = float(last_quo.price.iloc[0])
    last_open = float(last_quo.open.iloc[0])

    if last_price < last_open:
        return False

    day_line_bars = day_bars(symbol, num=4+down_days)

    last_1_bar = day_line_bars[0]
    last_2_bar = day_line_bars[1]

    if last_1_bar['close'] > last_1_bar['open'] and \
     last_2_bar['close'] > last_2_bar['open']:
        pre_bars = day_line_bars[2:]
    else:
        pre_bars = day_line_bars[1:]

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
    day_line_bars = day_bars(symbol)

    date, open, high, low, close = [], [], [], [], []
    for bar in day_line_bars:
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

    for _, row in tmp_df_kdj.iterrows():
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

    print(f'{symbol} PRE_K:{df_kdj["k"].iloc[-2]}, PRE_D:{df_kdj["d"].iloc[-2]}')
    print(f'    K:{df_kdj["k"].iloc[-1]},     D:{df_kdj["d"].iloc[-1]}')

    return True if df_kdj['buy_sig'].iloc[-1] else False


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

    day_line_bars = day_bars(symbol, num=5+pre_days)

    dates, closes = [], [],
    for bar in day_line_bars:
        dates.append(bar['date'])
        closes.append(bar['close'])

    dates.reverse()
    closes.reverse()

    df_ma = pd.DataFrame({'date': dates, 'close': closes})

    df_ma['ma5'] = df_ma['close'].rolling(window=5, min_periods=5).mean()
    df_ma['diff'] = df_ma['close'] - df_ma['ma5']
    df_ma['pre_diff'] = df_ma['diff'].shift(1)
    df_ma['cross_up'] = df_ma.apply(lambda x: 1 if x['pre_diff'] <= 0 < x['diff'] else 0, axis=1)

    cross_up = False

    for days in reversed(range(1, pre_days + 1)):
        ma_info = df_ma.iloc[-days]
        if ma_info.cross_up == 0:
            continue

        print(f"{symbol} {ma_info.date} close price({ma_info.close}) cross up ma5({ma_info.ma5})")
        cross_up = True
        break

    return cross_up


def is_break_through_ma30(symbol, pre_days=3):
    """
    if break through ma30
    :param symbol:
    :param pre_days
    :return:
    """
    assert pre_days >= 0

    day_line_bars = day_bars(symbol, num=30+pre_days)

    dates, closes = [], [],
    for bar in day_line_bars:
        dates.append(bar['date'])
        closes.append(bar['close'])

    dates.reverse()
    closes.reverse()

    df_ma = pd.DataFrame({'date': dates, 'close': closes})

    df_ma['ma30'] = df_ma['close'].rolling(window=30, min_periods=30).mean()
    df_ma['diff'] = df_ma['close'] - df_ma['ma30']
    df_ma['pre_diff'] = df_ma['diff'].shift(1)
    df_ma['cross_up'] = df_ma.apply(lambda x: 1 if x['pre_diff'] <= 0 < x['diff'] else 0, axis=1)

    cross_up = False

    for days in reversed(range(1, pre_days + 1)):
        ma_info = df_ma.iloc[-days]
        if ma_info.cross_up == 0:
            continue

        print(f"{symbol} {ma_info.date} close price({ma_info.close}) cross up ma30({ma_info.ma30})")
        cross_up = True
        break

    return cross_up


def is_moderate_heavy_vol(symbol, heavy_percent=0.27):
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

    day_line_bars = day_bars(symbol, num=2)

    yesday_bar = day_line_bars[1]

    yesday_close = float(yesday_bar['close'])
    yesday_open = float(yesday_bar['open'])

    if yesday_close < yesday_open:
        return False

    last_volume = float(day_line_bars[0]['volume'])
    yesday_volume = float(yesday_bar['volume'])

    if last_volume < yesday_volume:
        return False

    volume_change = last_volume / yesday_volume - 1

    if volume_change > heavy_percent:
        return False

    return True


def is_rise_with_sector(symbol, sectors=[], percent=0.6):
    """
    if related sectors general rise 
    """
    if not sectors:
        return False

    all_symbol = [symbol] + sectors
    rise_num = 0

    for s in all_symbol:
        day_line_bars = day_bars(s, num=3)

        last_day_bar = day_line_bars[0]
        pre_day_bar = day_line_bars[1]

        if last_day_bar['close'] > pre_day_bar['close']:
            rise_num += 1

    rise_percent = rise_num / len(all_symbol)
    
    if rise_percent >= percent:
        return True
    
    return False


def is_gap(symbol, percent=0.00):
    """
    if product a gap
    :param symbol:
    :param percent:
    :return:
    """
    day_line_bars = day_bars(symbol, num=3)
    last_day_bar = day_line_bars[0]
    pre_day_bar = day_line_bars[1]

    open_change = last_day_bar['low'] / pre_day_bar['high'] - 1

    if open_change > percent:
        return True

    return False


def is_rise_slow_with_ma5(symbol, rise_days=3, percent=0.015):
    """
    if price rise slowly follow ma5
    :param symbol:
    :param rise_days:
    :param percent:
    :return:
    """
    day_line_bars = day_bars(symbol, num=5+rise_days+1)

    tmp_ma5 = 0.0
    first_assign_ma5 = True

    gain_days = 0

    for i in range(len(day_line_bars)):
        day_change = day_line_bars[i]['close'] / day_line_bars[i]['open'] - 1

        if abs(day_change) > percent:
            return False
        if day_line_bars[i]['close'] < day_line_bars[i+1]['close']:
            return False

        ma5_closes = [bar['close'] for bar in day_line_bars[i:i+5]]
        ma5 = sum(ma5_closes) / len(ma5_closes)

        if first_assign_ma5:
            tmp_ma5 = ma5
            first_assign_ma5 = False

        if ma5 > tmp_ma5:
            return False

        tmp_ma5 = ma5

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False


def is_big_barehead_red_line_with_increase_vol(symbol, percent=0.05):
    """
    if close is the high and the gain is big
    """
    day_line_bars = day_bars(symbol, num=3)
    last_day_bar = day_line_bars[0]
    pre_day_bar = day_line_bars[1]

    if last_day_bar['volume'] < pre_day_bar['volume']:
        return False

    if last_day_bar['close'] < last_day_bar['high'] - 0.0101:
        return False

    change = last_day_bar['close'] / last_day_bar['open'] - 1

    if change >= percent:
        return True

    return False


def is_gain_limit_with_decrease_vol(symbol, percent=0.1):
    day_line_bars = day_bars(symbol, num=2)

    last_day_bar = day_line_bars[0]
    pre_day_bar = day_line_bars[1]

    if last_day_bar['volume'] > pre_day_bar['volume']:
        return False

    day_rtn = last_day_bar['close'] / pre_day_bar['close'] - 1

    if day_rtn > percent - 0.0001:
        return True

    return False


def is_new_high(symbol, days=360):
    """
    if make a new high
    """
    day_line_bars = day_bars(symbol, num=days)

    last_close = day_line_bars[0]['close']
    highest_day = max(day_line_bars[1:], key=lambda bar: bar['close'])
    his_highest = highest_day['close']

    if last_close > his_highest:
        return True

    return False


def is_shock_pos_and_break_through(symbol, shock_days=2):
    """
    if shock pos and break through shock price
    """
    day_line_bars = day_bars(symbol, num=shock_days+3)

    last_day_bar = day_line_bars[0]
    begin_shock_day_bar = day_line_bars[shock_days+1]

    if last_day_bar['close'] < begin_shock_day_bar['close']:
        return False

    pre_bars = day_line_bars[1:]

    closes = [bar['close'] for bar in pre_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))

    decline_days = 0
    for p_c in pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        if day_rtn > 0:
            return False

        decline_days += 1
        if decline_days == shock_days:
            return True


def is_ma_vol_rise_in_parallel(symbol, diff=0.055):
    """
    if double mavol rise in parallel
    """
    day_line_bars = day_bars(symbol, num=11)

    volumes = [bar['volume'] for bar in day_line_bars]

    last_5_volumes = volumes[:5]
    pre_5_volumes = volumes[1:6]

    last_vol_ma5 = sum(last_5_volumes) / len(last_5_volumes)
    pre_vol_ma5 = sum(pre_5_volumes) / len(pre_5_volumes)

    if last_vol_ma5 < pre_vol_ma5:
        return False

    last_10_volumes = volumes[:10]
    pre_10_volumes = volumes[1:11]

    last_vol_ma10 = sum(last_10_volumes) / len(last_10_volumes)
    pre_vol_ma10 = sum(pre_10_volumes) / len(pre_10_volumes)

    if last_vol_ma10 < pre_vol_ma10:
        return False

    last_vol_ma5_ma10_diff = last_vol_ma5 / last_vol_ma10 - 1
    pre_vol_ma5_ma10_diff = pre_vol_ma5 / pre_vol_ma10 - 1

    two_day_vol_ma_diff = last_vol_ma5_ma10_diff - pre_vol_ma5_ma10_diff

    if abs(two_day_vol_ma_diff) <= diff:
        return True

    return False


def is_rise_in_good_condition(symbol, days=180, step=30, percent=0.6):
    """
    if rise in good condition
    """
    day_line_bars = day_bars(symbol, num=days+step)
    
    step_day_bars = []
    for i in range(0, len(day_line_bars), step):
        step_day_bars.append(day_line_bars[i])
    
    closes = [bar['close'] for bar in step_day_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))
    
    rise_cnt = 0
    for p_c in pair_closes:
        rtn = p_c[0] / p_c[1] - 1

        if rtn > 0:
            rise_cnt += 1
    
    total_cnt = days / step

    rise_percent = rise_cnt / total_cnt

    if rise_percent >= percent:
        return True

    return False


def is_start_up_after_adj(symbol, adj_days=7, percent=0.02):
    """
    if start up after adjustment
    """
    day_line_bars = day_bars(symbol, num=1+adj_days+5)

    closes = [bar['close'] for bar in day_line_bars]

    last_5_closes = closes[:5]
    last_ma5 = sum(last_5_closes) / len(last_5_closes)
    last_close = closes[0]

    ma5_close_change = last_close / last_ma5 - 1
    if ma5_close_change < percent:
        return False

    pre_1_5_closes = closes[1:6]
    pre_1_ma5 = sum(pre_1_5_closes) / len(pre_1_5_closes)

    mid_idx = (adj_days + 1) // 2
    mid_5_closes = closes[mid_idx:mid_idx+5]
    mid_ma5 = sum(mid_5_closes) / len(mid_5_closes)

    pre_1_mid_ma5_change = pre_1_ma5 / mid_ma5 - 1
    if abs(pre_1_mid_ma5_change) > percent:
        return False

    tail_5_closes = closes[adj_days:adj_days+5]
    tail_ma5 = sum(tail_5_closes) / len(tail_5_closes)

    mid_tail_ma5_change = mid_ma5 / tail_ma5 - 1
    if abs(mid_tail_ma5_change) > percent:
        return False

    pre_1_tail_ma5_change = pre_1_ma5 / tail_ma5 - 1
    if abs(pre_1_tail_ma5_change) <= percent:
        return True

    return False


def is_gain_limit_after_yin_line(symbol, percent=0.095):
    """
    if gain limit after product a yin line
    """
    day_line_bars = day_bars(symbol, num=3)

    last_day_bar = day_line_bars[0]
    pre_day_bar = day_line_bars[1]

    day_rth = last_day_bar['close'] / pre_day_bar['close'] - 1
    if day_rth < percent:
        return False

    if pre_day_bar['close'] < pre_day_bar['open']:
        return True

    return False


if __name__ == "__main__":
    symbol = '603707'
    # rls = {
    #     'is_look_up_from_bottom': is_look_up_from_bottom(symbol),
    #     'is_kdj_gf': is_kdj_gf(symbol),
    #     'is_last_price_gt_ma30': is_last_price_gt_ma30(symbol),
    #     'is_break_through_ma5': is_break_through_ma5(symbol),
    #     'is_moderate_heavy_vol': is_moderate_heavy_vol(symbol),
    # }
    rls = is_rise_in_good_condition('001979')
    print(rls)
    pass
