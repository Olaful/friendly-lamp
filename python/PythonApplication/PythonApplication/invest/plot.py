import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.lines import Line2D
from matplotlib.pylab import date2num


def _get_martrix(bars):
    """
    get martrix
    :param bars:
    :return:
    """
    bar_df = pd.DataFrame(bars)

    bar_df.date = pd.to_datetime(bar_df.date)
    bar_df.date = bar_df.date.apply(lambda x: date2num(x))

    bar_df.sort_values(by=['date'], inplace=True)
    bar_df = bar_df[['date', 'open', 'high', 'low', 'close']]

    martrix_data = bar_df.values

    return martrix_data


def key_line(bars, point: list = None):
    """
    draw key line
    :param bars:
    :param point:
    :return:
    """
    plt.figure(figsize=(18, 18))
    ax = plt.gca()

    ax.set_facecolor('#000000')
    ax.grid(axis='y', linestyle='--', color='r', alpha=0.5)
    ax.xaxis_date()

    martrix_bar_data = _get_martrix(bars)

    candlestick_ohlc(ax, martrix_bar_data, width=0.7, colorup='#ff1717', colordown='#53c156',
                     alpha=1.0)

    x_dates = martrix_bar_data[..., 0]
    x_dates_len = len(x_dates)
    lines = []

    for pos in point:
        line = Line2D(xdata=x_dates, ydata=[pos] * x_dates_len, color='#FF9933', linewidth=0.7)
        lines.append(line)

    for line in lines:
        ax.add_line(line)

    plt.show()


