from tushare import get_realtime_quotes, get_index
from stk_data import day_bars


def is_index_in_down_trend(index='000001', down_days=3):
    """
    if index is in the down trend
    """
    day_line_bars = day_bars(index, num=down_days+2, is_index=True)

    begin_down_day_bar = day_line_bars[down_days]
    first_down_day_bar = day_line_bars[down_days - 1]

    if begin_down_day_bar['close'] < first_down_day_bar['close']:
        return False

    closes = [bar['close'] for bar in day_line_bars]
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


def is_index_ma5_turn_down_in_high_position(index, rise_days=7):
    """
    if ma5 turn down in high position
    """
    day_line_bars = day_bars(index, num=1+rise_days+5+1, is_index=True)

    closes = [bar['close'] for bar in day_line_bars]
    
    last_5_bars = closes[:5]
    pre_5_bars = closes[1:6]

    last_ma5 = sum(last_5_bars) / len(last_5_bars)
    pre_ma5 = sum(pre_5_bars) / len(pre_5_bars)

    if last_ma5 > pre_ma5:
        return False

    pre_closes = closes[1:]
    ma5_list = []

    for i in range(0, rise_days+1):
        five_closes = pre_closes[i:i+5]
        day_ma5 = sum(five_closes) / len(five_closes)
        ma5_list.append(day_ma5)

    shift_ma5_list = ma5_list[1:]
    pair_ma5 = list(zip(ma5_list, shift_ma5_list))

    gain_days = 0
    for p_m in pair_ma5:
        day_ma_rtn = p_m[0] / p_m[1] - 1
        if day_ma_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False
    

def is_dead_fork_vol_ma5_ma10(symbol):
    """
    if ma5 of volume product dead fork from ma10
    """
    day_line_bars = day_bars(symbol, num=11)

    volumes = [bar['volume'] * 100 for bar in day_line_bars]

    vol_5_days = volumes[:5]
    vol_10_days = volumes[:10]

    pre_vol_5_days = volumes[1:6]
    pre_vol_10_days = volumes[1:11]

    vol_ma5 = sum(vol_5_days) / len(vol_5_days)
    vol_ma10 = sum(vol_10_days) / len(vol_10_days)

    pre_vol_ma5 = sum(pre_vol_5_days) / len(pre_vol_5_days)
    pre_vol_ma10 = sum(pre_vol_10_days) / len(pre_vol_10_days)

    if pre_vol_ma5 > pre_vol_ma10 and vol_ma5 < vol_ma10:
        return True

    return False


def is_reach_rtn_3_days(symbol, rtn=0.08):
    """
    if the cumulate return of 
    three days reach the specified range
    """
    day_line_bars = day_bars(symbol, num=5)

    closes = [bar['close'] for bar in day_line_bars]

    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))
    three_days_pair_closes = pair_closes[:3]

    cum_rtn = 0
    for p_c in three_days_pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        cum_rtn += day_rtn

    if cum_rtn >= rtn:
        return True

    return False


def is_yin_line_after_rise(symbol, rise_days=3):
    """
    if product a yin line after rising
    """
    last_quo = get_realtime_quotes(symbol)
    last_price = float(last_quo.price.iloc[0])
    last_open = float(last_quo.open.iloc[0])

    if last_price > last_open:
        return False

    day_line_bars = day_bars(symbol, num=4+rise_days)

    pre_bars = day_line_bars[1:]

    closes = [bar['close'] for bar in pre_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))

    gain_days = 0
    for p_c in pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        if day_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False


def is_vol_decrease_after_rise(symbol, rise_days=3):
    """
    if volume decrease after rising
    """
    last_quo = get_realtime_quotes(symbol)
    last_price = float(last_quo.price.iloc[0])
    last_open = float(last_quo.open.iloc[0])

    if last_price < last_open:
        return False

    day_line_bars = day_bars(symbol, num=4+rise_days)

    if day_line_bars[0]['volume'] > day_line_bars[1]['volume']:
        return False

    pre_bars = day_line_bars[1:]

    closes = [bar['close'] for bar in pre_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))

    gain_days = 0
    for p_c in pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        if day_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False


def is_begin_dead_triangle(symbol, days=30):
    day_line_bars = day_bars(symbol, num=days+1)

    closes = [bar['close'] for bar in day_line_bars]

    last_5_bars = closes[:5]
    last_10_bars = closes[:10]
    last_ma5 = sum(last_5_bars) / len(last_5_bars)
    last_ma10 = sum(last_10_bars) / len(last_10_bars)

    if last_ma5 > last_ma10:
        return False

    last_20_bars = closes[:20]
    last_ma20 = sum(last_20_bars) / len(last_20_bars)

    if last_ma20 > last_ma5:
        return False

    pre_5_bars = closes[1:6]
    pre_10_bars = closes[1:11]
    pre_ma5 = sum(pre_5_bars) / len(pre_5_bars)
    pre_ma10 = sum(pre_10_bars) / len(pre_10_bars)

    if pre_ma5 > pre_ma10:
        return True

    return False


def is_rise_close_to_ma180(symbol, percent=0.015):
    day_line_bars = day_bars(symbol, num=180+1)

    closes = [bar['close'] for bar in day_line_bars]
    last_price = closes[0]
    closes_180 = closes[:180]

    ma180 = sum(closes_180) / len(closes_180)
    
    if last_price > ma180:
        return False

    distance = ma180 / last_price - 1

    if distance < percent:
        return True

    return False


def is_down_ma5_after_rise(symbol, rise_days=3):
    """
    if cross down ma5 after rising
    """
    last_quo = get_realtime_quotes(symbol)
    last_price = float(last_quo.price.iloc[0])

    day_line_bars = day_bars(symbol, num=4+rise_days)
    last_5_bars = day_line_bars[:5]
    closes = [bar['close'] for bar in last_5_bars]
    ma5 = sum(closes) / len(closes)

    if last_price > ma5:
        return False

    pre_bars = day_line_bars[1:]

    closes = [bar['close'] for bar in pre_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))

    gain_days = 0
    for p_c in pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        if day_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False


def is_gain_limit_after_rise(symbol, rise_days=3):
    """
    if gain to limited after rise
    """
    day_line_bars = day_bars(symbol, num=rise_days+2)

    last_close = day_line_bars[0]['close']
    pre_close = day_line_bars[1]['close']

    day_rtn = last_close / pre_close - 1
    if day_rtn < 0.099:
        return False

    pre_bars = day_line_bars[1:]

    closes = [bar['close'] for bar in pre_bars]
    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))

    gain_days = 0
    for p_c in pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        if day_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False


def is_ma5_turn_down_in_high_position(symbol, rise_days=9):
    """
    if ma5 turn down in high position
    """
    day_line_bars = day_bars(symbol, num=1+rise_days+5+1)

    closes = [bar['close'] for bar in day_line_bars]
    
    last_5_bars = closes[:5]
    pre_5_bars = closes[1:6]

    last_ma5 = sum(last_5_bars) / len(last_5_bars)
    pre_ma5 = sum(pre_5_bars) / len(pre_5_bars)

    if last_ma5 > pre_ma5:
        return False

    pre_closes = closes[1:]
    ma5_list = []

    for i in range(0, rise_days+1):
        five_closes = pre_closes[i:i+5]
        day_ma5 = sum(five_closes) / len(five_closes)
        ma5_list.append(day_ma5)

    shift_ma5_list = ma5_list[1:]
    pair_ma5 = list(zip(ma5_list, shift_ma5_list))

    gain_days = 0
    for p_m in pair_ma5:
        day_ma_rtn = p_m[0] / p_m[1] - 1
        if day_ma_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False


def is_product_cross_star_in_high_position(symbol, rise_days=6, open_close_change=0.0025, high_low_change=0.025):
    """
    if product a cross star in high position
    """
    day_line_bars = day_bars(symbol, num=1+rise_days+5+1)

    last_day_bar = day_line_bars[0]

    openclose_change = last_day_bar['open'] / last_day_bar['close'] - 1
    if abs(openclose_change) > open_close_change:
        return False

    highlow_change = last_day_bar['high'] / last_day_bar['low'] - 1
    if highlow_change < high_low_change:
        return False

    closes = [bar['close'] for bar in day_line_bars]

    pre_closes = closes[1:]
    ma5_list = []

    for i in range(0, rise_days+1):
        five_closes = pre_closes[i:i+5]
        day_ma5 = sum(five_closes) / len(five_closes)
        ma5_list.append(day_ma5)

    shift_ma5_list = ma5_list[1:]
    pair_ma5 = list(zip(ma5_list, shift_ma5_list))

    gain_days = 0
    for p_m in pair_ma5:
        day_ma_rtn = p_m[0] / p_m[1] - 1
        if day_ma_rtn < 0:
            return False

        gain_days += 1
        if gain_days == rise_days:
            return True

    return False
    


if __name__ == "__main__":
    rls = is_index_in_down_trend('000001')
    pass
