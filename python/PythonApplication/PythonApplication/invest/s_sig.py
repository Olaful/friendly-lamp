from tushare import get_realtime_quotes
from quotool import his_quo


def is_dead_fork_vol_ma5_ma10(symbol):
    """
    if ma5 of volume product dead fork from ma10
    """
    last_quo = get_realtime_quotes(symbol)
    last_date = last_quo.date.iloc[0]
    
    day_bars = his_quo(symbol, num=11)

    volumes = [bar['volume'] * 100 for bar in day_bars]
    first_his_date = str(day_bars[0]['date'])

    if first_his_date < last_date:
        volumes.insert(float(last_quo.volume.iloc[0]), 0)

    vol_5_days = volumes[:5]
    vol_10_days = volumes[:10]

    vol_ma5 = sum(vol_5_days) / len(vol_5_days)
    vol_ma10 = sum(vol_10_days) / len(vol_10_days)

    if vol_ma5 < vol_ma10:
        return True

    return False


def is_reach_rtn_3_days(symbol, rtn=0.08):
    """
    if the cumulate return of 
    three days reach the specified range
    """
    last_quo = get_realtime_quotes(symbol)
    last_date = last_quo.date.iloc[0]
    
    day_bars = his_quo(symbol, num=5)

    closes = [bar['close'] for bar in day_bars]
    first_his_date = str(day_bars[0]['date'])

    if first_his_date < last_date:
        closes.insert(float(last_quo.price.iloc[0]), 0)

    shift_closes = closes[1:]
    pair_closes = list(zip(closes, shift_closes))
    three_days_pair_closes = pair_closes[:3]

    cum_rtn = 0
    for p_c in three_days_pair_closes:
        day_rtn = p_c[0] / p_c[1] - 1
        cum_rtn += day_rtn

    if cum_rtn >= 0.08:
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

    last_date = last_quo.date.iloc[0] 
    day_bars = his_quo(symbol, num=4+rise_days)
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

    pre_bars = day_bars[1:]

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
    rls = is_yin_line_after_rise('002024')
    pass
