import matplotlib
import matplotlib.pyplot as plt
import os
import platform
from matplotlib.font_manager import FontProperties
from django_newswebsite.settings import STATIC_DIR

def saveToBarh(datalist):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if platform.system() == 'Windows':
        static_dir = os.path.join(base_dir, 'static/images')
        img = os.path.join(static_dir, 'topviews.png')
        fname = STATIC_DIR + r'\fonts\wqydkzh.ttf'
        font = FontProperties(fname=fname)
    elif platform.system() == 'Linux':
        static_dir = base_dir
        img = os.path.join(static_dir, 'topviews.png')
        fname = STATIC_DIR + r'/fonts/wqydkzh.ttf'
        font = FontProperties(fname=fname)

    x = [data.name for data in datalist]
    y = [data.likes for data in datalist]
    x.reverse()
    y.reverse()

    #matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    ax = plt.subplot2grid((1, 1), (0, 0))
    # 宽度0.5
    ax.barh(x, y, 0.5, color='red')
    
    ticks = [i for i in range(0, len(x)+1)]
    ax.set_xticks(y)
    ax.set_yticks(ticks)

    # 注解
    for i, _ in enumerate(x, start=1):
        xy = (y[i-1], i)
        plt.annotate(xy[0], xy=xy, xytext=(xy[0], i-1-0.1), xycoords='data')

    ax.set_xticks([])
    ax.set_facecolor('none')
    ax.set_title('热门top 5(点赞数)', FontProperties=font)

    axes = plt.gca()
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    #axes.spines['left'].set_color('none')
    axes.spines['bottom'].set_visible(False)

    plt.setp(ax.get_yticklabels(), fontsize=15)
    plt.tight_layout()
    # 保存透明背景图像
    plt.savefig(img, facecolor='none')