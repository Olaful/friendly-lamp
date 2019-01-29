import matplotlib
import matplotlib.pyplot as plt
import os

def saveToBarh(datalist):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, 'static/images')
    os.chdir(static_dir)

    x = [data.name for data in datalist]
    y = [data.likes for data in datalist]
    x.reverse()
    y.reverse()

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    ax = plt.subplot2grid((1, 1), (0, 0))
    # 宽度0.5
    ax.barh(x, y, 0.5, color='red')
    
    ticks = [i for i in range(0, len(x)+1)]
    ax.set_xticks(y)
    ax.set_yticks(ticks)

    for i, _ in enumerate(x, start=1):
        xy = (y[i-1], i)
        plt.annotate(xy[0], xy=xy, xytext=(xy[0], i-1-0.1), xycoords='data')

    ax.set_xticks([])
    ax.set_facecolor('#eceeef')
    ax.set_title('热门top 5(点赞数)')

    axes = plt.gca()
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    #axes.spines['left'].set_color('none')
    axes.spines['bottom'].set_color('none')

    plt.setp(ax.get_yticklabels(), fontsize=15)
    plt.tight_layout()
    # 保存透明背景图像
    plt.savefig('topviews.png', facecolor='none')