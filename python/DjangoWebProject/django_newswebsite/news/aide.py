import matplotlib as mp
import matplotlib.pyplot as plt
import os
import platform
from matplotlib.font_manager import FontProperties
from django_newswebsite.settings import STATIC_DIR
import io
import base64

def saveToBarh(datalist):
    if not datalist:
        return base64.b64encode(io.BytesIO().getvalue()).decode()
    if platform.system() == 'Windows':
        img = STATIC_DIR + r'\images\topviews.png'
        fname = STATIC_DIR + r'\fonts\wqydkzh.ttf'
        font = FontProperties(fname=fname)
    elif platform.system() == 'Linux':
        img = STATIC_DIR + '/images/topviews.png'
        fname = STATIC_DIR + '/fonts/simheittf.ttf'
        font = FontProperties(fname=fname)

    x = [data.name for data in datalist]
    y = [data.likes for data in datalist]
    x.reverse()
    y.reverse()

    mp.rcParams['axes.unicode_minus'] = False

    fig = plt.figure()

    ax = plt.subplot2grid((1, 1), (0, 0))
    # 宽度0.5
    barhs = ax.barh(x, y, 0.5, left=5, color=plt.cm.Set2(0))

    color = ['#FFAEB9', '#FF8C69', '#FF8247', '#FF7256', '#FF6347']

    # 颜色
    for i, barh in enumerate(barhs):
        barh.set_facecolor(color[i])
    
    for i, yticklabel in enumerate(ax.get_yticklabels()):
        yticklabel.set_color(color[i])
    
    # 刻度
    ticks = [i for i in range(0, len(x)+1)]
    ax.set_xticks(y)
    ax.set_yticks(ticks)

    # 注解
    for i, _ in enumerate(x, start=1):
        xy = (y[i-1], i)
        plt.annotate(xy[0], xy=xy, xytext=(xy[0]+5, i-1-0.1), xycoords='data')

    ax.set_xticks([])
    ax.set_facecolor('none')
    ax.set_title('热门top 5(点赞数)', FontProperties=font, fontsize=15, color='#EE5C42')

    # 隐藏坐标轴
    axes = plt.gca()
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)

    axes.spines['left'].set_color('#43CD80')
    axes.spines['left'].set_lw(15)

    plt.setp(ax.get_yticklabels(), FontProperties=font)
    plt.setp(ax.get_yticklabels(), fontsize=20)

    plt.tight_layout()
    
    # 获取二进制并编码
    # 去掉母图背景色
    fig.set_facecolor('none')
    buffer = io.BytesIO()
    fig.canvas.print_png(buffer)
    data = buffer.getvalue()
    b64Data = base64.b64encode(data)

    return b64Data.decode()

    # 保存透明背景图像
    #plt.savefig(img, facecolor='none')