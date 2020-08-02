from tushare import get_realtime_quotes
from quotool import his_quo

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


if __name__ == "__main__":
    rls = is_look_up_from_bottom('000960', down_days=2)
    pass
    

    


    

    
    
    