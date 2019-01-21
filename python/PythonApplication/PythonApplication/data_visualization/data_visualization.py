import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

# matplotlib默认配置从rc文件中(位于当前用户目录下)读取
# 可以通过两种方式手动指定属性
def setParam():
    mp.rcParams['lines.linewidth'] = 2
    mp.rcParams['lines.color'] = 'r'
    mp.rc('lines', linewidth=2, color='r')

def sincosLine():
    t = np.arange(0.0, 1.0, 0.01)

    s = np.sin(2 * np.pi * t)
    plt.rcParams['lines.color'] = 'r'
    plt.plot(t, s)

    c = np.cos(2 * np.pi * t)
    plt.rcParams['lines.linewidth'] = '3'
    plt.plot(t, c)

    # 重置matplotlib参数
    # mp.rcdefaults()

    plt.show()

def readCsv():
    data = []
    try:
        with open('../myfile/mycsv.csv') as f:
            reader = csv.reader(f)
        head = reader.next()
        data = [row for row in reader]
    except csv.Error as e:
        print('发生错误，位置:{}, 信息:{}'.format(reader.line_num, e))
        sys.exit(-1)
    
    # 使用numpy加载大文件
    #data = np.loadtxt('../myfile/mycsv.csv', dtype='string', delimiter=',')

if __name__ == "__main__":
    sincosLine()

