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
    plt.barh(x, y, color='orange')
    plt.tight_layout()
    plt.savefig('topviews.png')