from tushare import get_realtime_quotes
from quotool import his_quo
from stk_data import day_bars


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


if __name__ == "__main__":
    rls = is_vol_decrease_after_rise('603667')
    pass
