from quo_down import his_quo, last_quo


def get_rsi(close, day):
    import pandas as pd

    df_close = pd.DataFrame({'close': close})
    df_close['shiff_1'] = df_close['close'].shift(1)
    df_close['rtn_day'] = (df_close['close'] - df_close['shiff_1'])
    df_close['day_sma'] = df_close['rtn_day'] / day
    df_close['day_sma_gain'] = df_close['day_sma'].apply(lambda x: x if x >= 0 else 0)
    df_close['day_sma_decline'] = df_close['day_sma'].apply(lambda x: abs(x) if x <= 0 else 0)

    def get_smooth_change(change_list):
        tmp_sma_change = 0
        smooth_change_list = [0]
        for change in change_list[1:]:
            smooth_change = float(change) + tmp_sma_change * (day - 1) / day
            tmp_sma_change = smooth_change
            smooth_change_list.append(smooth_change)
        return smooth_change_list

    day_sma_gain = df_close['day_sma_gain'].tolist()
    smooth_gain_list = get_smooth_change(day_sma_gain)

    day_sma_decline = df_close['day_sma_decline'].tolist()
    smooth_decline_list = get_smooth_change(day_sma_decline)

    df_close['smooth_sma_day_gain'] = smooth_gain_list
    df_close['smooth_sma_day_decline'] = smooth_decline_list
    df_close['RS'] = df_close['smooth_sma_day_gain'] /\
                     df_close['smooth_sma_day_decline']
    df_close['RSI'] = round(df_close['RS'] / (1 + df_close['RS']) * 100, 2)

    return df_close['RSI']


def cal_rsi(symbol):
    import pandas as pd

    date, _, _, _, close = his_quo(symbol)

    df_rsi = pd.DataFrame({'date': date, 'close': close})
    rsi6 = get_rsi(close, 6)
    rsi12 = get_rsi(close, 12)
    rsi24 = get_rsi(close, 24)

    df_rsi['RSI6'] = rsi6
    df_rsi['RSI12'] = rsi12
    df_rsi['RSI24'] = rsi24
    df_rsi['RSI6_pre'] = df_rsi['RSI6'].shift(1)
    df_rsi['RSI12_pre'] = df_rsi['RSI12'].shift(1)

    use_rsi24 = False

    def jude_buy(x):
        buy_flag = False
        if x['RSI6_pre'] < x['RSI12_pre'] and x['RSI6'] > x['RSI12']:
            buy_flag = True
        if use_rsi24:
            buy_flag = buy_flag and x['RSI12'] < x['RSI24'] < x['RSI6']

        return 1 if buy_flag else 0

    df_rsi['buy_sig'] = df_rsi.apply(jude_buy, axis=1)

    buy_date = df_rsi[df_rsi['buy_sig'] == 1]['date'].tolist()
    buy_date = list(reversed(buy_date))
    print('RSI:', buy_date)


def cal_kdj(symbol):
    import pandas as pd

    date, open, high, low, close = his_quo(symbol)
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

    buy_date = df_kdj[df_kdj['buy_sig'] == 1]['date'].tolist()
    buy_date = list(reversed(buy_date))
    sell_date = df_kdj[df_kdj['sell_sig'] == 1]['date'].tolist()
    sell_date = list(reversed(sell_date))

    print("BUY_KDJ:", buy_date)
    print("SELL_KDJ:", sell_date)


if __name__ == '__main__':
    cal_rsi('600073')
    cal_kdj('600073')
