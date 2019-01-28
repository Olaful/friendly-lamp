import matplotlib as mp
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.cbook import get_sample_data
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv
import sys
import xlrd
from xlrd import open_workbook, xldate_as_tuple
from pprint import pprint
import os
import time
from datetime import datetime
import datetime
from math import sqrt

# numpy中也会有random这个模块,重命令避免混淆
import random as std_rand
import struct
import string
import requests
import argparse
import json
import settings
try:
    import cStringIO as StringIO
except:
    from io import StringIO

import sqlite3
import aide
# pylab相当导入作图相关的库matplotlib,numpy等
from pylab import *
import pylab
from matplotlib.font_manager import FontProperties
import scipy.misc
import scipy
import scipy.signal
from PIL import Image, ImageChops, ImageFilter

def setParam():
    """
    matplotlib默认配置从rc文件中(位于当前用户目录下)读取
    可以通过两种方式手动指定属性
    """
    mp.rcParams['lines.linewidth'] = 2
    mp.rcParams['lines.color'] = 'r'
    mp.rc('lines', linewidth=2, color='r')

def sincosLine():
    """
    正弦余弦
    """
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
    """
    读取csv文件
    """
    data = []
    try:
        with open('mycsv.csv') as f:
            # dialect指定字段分隔符
            reader = csv.reader(f, dialect=csv.excel_tab)
            head = next(reader)
            data = [row for row in reader]
    except csv.Error as e:
        print('发生错误，位置:{}, 信息:{}'.format(reader.line_num, e))
        sys.exit(-1)
    
    # 使用numpy加载大文件
    #data = np.loadtxt('../myfile/mycsv.csv', dtype='string', delimiter=',')
    print(head)
    print(data)

def readXlsx():
    """
    xlrd读取xlsx文件
    """
    # on_demand=True按需加载
    wb = xlrd.open_workbook(filename=r'myxlsx.xlsx', on_demand=True)
    ws = wb.sheet_by_name('Sheet1')
    dataset = []
    for r in range(ws.nrows):
        col = []
        for c in range(ws.ncols):
            col.append(ws.cell(r, c).value)
        dataset.append(col)

    pprint(dataset)

    cell = xlrd.sheet.Cell(1, 0)
    print(cell)
    print(cell.value)
    print(cell.ctype)

    # 日期以浮点数存储，如果xlrd检测是否是日期类型
    if cell.ctype == xlrd.XL_CELL_DATE:
        date_value = xldate_as_tuple(cell.value, wb.datemode)
        print(datetime(*date_value))

def makeBigData():
    """
    制造大数据
    """
    def get_rand_len_data(len):
        data = []
        for _ in range(len):
            data.append(randint(0,9))
        string = ''.join(list(map(str, data)))
        return string

    with open('bigdata.data', 'w', encoding="utf-8") as file:
        for _ in range(1000000):
            f, s, t = get_rand_len_data(9),get_rand_len_data(13), get_rand_len_data(4)
            file.write('{} {} {}\n'.format(f, s, t))

def readJsonData():
    """
    读取json文件
    """
    url = 'https://github.com/timeline.json'

    resp = requests.get(url)
    json_data = resp.json()
    
    rls = set
    for r in json_data:
        try:
            rls.add(r['repository']['url'])
        except KeyError as e:
            print('没有数据:{}'.format(e))

def readBigData(file):
    """先读取9个宽度的字符,s表示c语言中的char[]，接着读取14个，以此类推，根据文件而定
    600833296 4937438977840 7014
    """
    mask = '9s14s5s'
    data = []
    with open(file, 'r') as f:
        for line in f:
            fields = struct.Struct(mask).unpack_from(line.encode())
            #fields = struct.unpack_from(mask, line)
            #print('fields:', [field.strip() for field in fields])
            data.append([field.decode().strip() for field in fields])
        return data

def import_data(data, export_format):
    """
    按格式导出数据
    """
    if export_format == 'csv':
        return write_csv(data)
    elif export_format == 'json':
        return write_json(data)
    elif export_format == 'xlsx':
        return write_xlsx(data)
    else:
        print('不支持的格式:{}'.format(export_format))

def write_csv(data):
    """
    导成csv数据
    """
    f = StringIO()
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
    return f.getvalue()

def write_json(data):
    """
    导成json数据
    """
    j = json.dumps(data)
    return j

def write_xlsx(data):
    """
    导成xlsx数据
    """
    from xlwt import Workbook

    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    row = 0
    for line in data:
        col = 0
        for datum in line:
            print(datum)
            sheet1.write(row, col, datum)
            col += 1
        row += 1
        
        if row > 65535:
            print('超时单个sheet页支持的最大行数65535', sys.stderr)
            break
    f = StringIO()
    book.save(f)
    return f.getvalue()

def args():
    ''

def importData():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("import_file", help="定宽文件的路径")
    # parser.add_argument("export_format", help="支持的导出格式:json, csv, xlsx")
    # args = parser.parse_args()
    args.import_file = 'bigdata.data'
    args.export_format = 'xlsx'

    if args.import_file is None:
        print('请指定要导出的定宽文件的路径', sys.stderr)
        sys.exit(1)

    if args.export_format not in ('csv', 'json', 'xlsx'):
        print('不支持的导出格式:{}'.format(args.export_format), sys.stderr)

    if not os.path.isfile(args.import_file):
        print('指定的文件不存在:{args.import_file}'.format, sys.stderr)

    data = readBigData(args.import_file)
    rls = import_data(data, args.export_format)
    print(rls)

def makeSqliteData():
    """
    大批量插入sqlite
    """
    conn = sqlite3.connect('mysqlitedb.db')
    cursor = conn.cursor()
    createSql = """
        create table population
        (
            id INTEGER primary key,
            name TEXT,
            population TEXT
        )    
    """
    insertSql = 'insert into population values(?,?,?)'
    #cursor.execute(createSql)
    
    id = 1
    population = 10000

    for _ in range(5000):
        name = 'country_' + str(id)
        data = [id, name, population]
        cursor.execute(insertSql, data)
        id += 1
        population += 100
    
    conn.commit()
    conn.close()

def readSqlite():
    """
    读取sqlite数据
    """
    conn = sqlite3.connect('mysqlitedb.db')
    try:
        with conn:
            cursor = conn.cursor()
            querySql = 'select id, name, population from population \
            order by population desc limit 1000'
            cursor.execute(querySql)

            resultset = cursor.fetchall()
            col_names = [cn[0] for cn in cursor.description]
            print('{0:10} {1:30} {2:10}'.format(col_names[0], col_names[1], col_names[2]))
            print('='*(10+1+30+1+10))
            
            for row in resultset:
                print('%10s %30s %10s' % row)
    except sqlite3.Error as e:
        print("sqlite 出错:{}".format(e))

def is_outer(points, threshold=3.5):
    """
    超出范围，异常
    """
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points, axis=0)

    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_zcore = 0.6745 * diff / med_abs_deviation
    
    return modified_z_zcore > threshold

def showCleanData():
    """
    直方图显示
    """
    # 返回产生100个0-1之间的数的array对象
    x = np.random.random(100)
    buckets = 50
    # r_按行连接矩阵: 例r_[[1,2], ]
    x = np.r_[x, -49, 95, 100, -100]

    filtered = x[~is_outer(x)]
    # figure可以划分为多个子图
    plt.figure()

    # 子图像,211表示2行1列，位置索引1
    # 也可以写成2,1,1
    plt.subplot(211)
    # 直方图,buckets指柱状条个数,个数越多，区分范围越细
    plt.hist(x, buckets)
    plt.xlabel('Raw')

    plt.subplot(212)
    plt.hist(filtered, buckets)
    plt.xlabel('Cleaned')
    plt.show()
        
def showBox():
    """
    箱型图
    """
    # rand(50)返回50个0-1之间的随机数的numpy.narray对象
    spread = rand(50) * 100
    # 返回25个50的对象
    center = ones(25) * 50
    flier_high = rand(10) * 100 + 100
    flier_low = rand(10) * -100
    # 按行连接array
    data = concatenate((spread, center, flier_high, flier_low), 0)

    subplot(311)
    # gx表示超出异常
    boxplot(data, 0, 'gx')
    
    subplot(312)

    spread_1 = concatenate((spread, flier_high, flier_low), 0)
    center_1 = ones(70) * 25
    # 两个array组成的散点图
    scatter(center_1, spread_1)
    # x轴范围
    xlim([0, 50])

    subplot(313)
    center_2 = rand(70) * 50
    scatter(center_2, spread_1)
    xlim([0, 50])

    show()

def showScatter():
    """
    散点图
    """
    x = 1e6 * rand(1000)
    y = rand(1000)

    figure()

    subplot(211)
    scatter(x, y)
    xlim(1e-6, 1e6)

    subplot(212)
    scatter(x, y)
    # x轴整数区间比例尺
    xscale('log')
    xlim(1e-6, 1e6)

    show()

def openBigdata():
    """
    按块读取大数据
    """
    with open('bigdata.data', 'r') as f:
        chunksize = 1000
        readable = ''
        done = 0
        # f不会是空
        while not done:
            # 当前读取位置
            start = f.tell()
            print("开始位置:{}".format(start))
            file_block = ''
            for _ in range(start, start + chunksize):
                # next不能与tell同时用
                #line = next(f)
                line = f.readline()
                if not line:
                    done = 1
                    break
                file_block = file_block + line
                print('逐行读取:{}-{}'.format(type(file_block), file_block))
            readable = readable + file_block
            stop = f.tell()
            print('块数据:{}-{}'.format(type(readable), readable))
            print('读取{}到{}之间的数据'.format(start, stop))
            print('总读取字节数:{}'.format(len(readable)))
            # data = input("继续:")

def readTimeChangeData():
    """
    读取变化的文件
    """
    with open('countries.txt') as f:
        # 文件大小
        filesize = os.stat('countries.txt')[6]
        f.seek(filesize)
        while True:
            where = f.tell()
            line = f.readline()
            if not line:
                time.sleep(1)
                # 重定位
                f.seek(where)
            else:
                print(line)

def showMisc():
    face = scipy.misc.face()
    plt.gray()
    plt.imshow(face)
    plt.colorbar()

    # 像素信息
    print(face.shape)
    # 最大灰度直
    print(face.max())
    # 像素点的值类型
    print(face.dtype)
    plt.show()

def openByPIL():
    img = Image.open('captcha_railway.png')
    # 图像数据类似一个二维数据
    arr = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    plt.gray()
    # 加载数组形式的图像数据
    plt.imshow(arr)
    plt.colorbar()
    plt.show()

def dealImg():
    # 把大内存图像部分加载到内存
    # img = np.memmap('captcha_railway.png', dtype=np.uint8, shape=(375,500)
    img = scipy.misc.imread('captcha_railway.png')
    # 把b通道灰度值置0
    img = img[:,:,0]
    # 指定图像实例，初始化参数
    plt.figure(num="hello")
    plt.gray()

    plt.subplot(121)
    plt.imshow(img)

    # 选择100:250, 140:350行之间的图像进行放大
    zimg = img[100:250, 140:350] 

    plt.subplot(122)
    plt.imshow(zimg)
    plt.show()

def dealArray():
    # 一维数组
    a = array([5, 1, 2, 3, 4])
    print(a[2:3])
    print(a[:2])
    print(a[3:])

    # 多维数组
    b = array([[1,1,1],[2,2,2],[3,3,3]])
    # 取第一行
    print(b[0,:])
    # 去第一列
    print(b[:,0])

def showRandData():
    """
    随机数直方图
    """
    # seed使用系统时间初始化伪随机数
    seed()

    pylab.subplot(211)
    real_rand_vals = []
    real_rand_vals = [random() for _ in range(100)]
    pylab.hist(real_rand_vals, 20)

    # 设置中文字符集
    pylab.xlabel('随机数', FontProperties=settings.FONT_SET)
    pylab.ylabel('个数', FontProperties=settings.FONT_SET)

    # 1-6随机数
    pylab.subplot(212)
    real_rand_vals = [randint(1,7) for _ in range(100)]
    pylab.hist(real_rand_vals, 20)
    pylab.xlabel('随机数', FontProperties=font_set)
    pylab.ylabel('个数', FontProperties=font_set)

    # 0-6浮点数
    # subplot最多为两个
    # pylab.subplot(213)
    # real_rand_vals = [uniform(1,7) for _ in range(100)]
    # pylab.hist(real_rand_vals, 20)
    # pylab.xlabel('随机数', FontProperties=font_set)
    # pylab.ylabel('个数', FontProperties=font_set)
    
    
    pylab.show()

def showPriceChange():
    """
    价格与时间
    """
    duration = 100
    mean_inc = 0.2
    std_dev_inc = 1.2
    x = range(duration)
    y = []
    price_today = 0
    
    for _ in x:
        # 随机正态分布数据,参数：中值，标准差
        next_delta = std_rand.normalvariate(mean_inc, std_dev_inc)
        price_today += next_delta
        y.append(price_today)

    pylab.plot(x, y)
    pylab.xlabel('时间', FontProperties=settings.FONT_SET)
    pylab.ylabel('价格', FontProperties=settings.FONT_SET)
    pylab.show()

def showDistributed():
    """
    各种随机数分布
    """
    SAMPLE_SIZE = 1000
    buckets = 100

    plt.figure()
    matplotlib.rcParams.update({'font.size': 7})
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    plt.subplot(621)
    plt.xlabel('0-1随机数分布')
    res = [std_rand.random() for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(622)
    plt.xlabel('1-1000浮点数分布')
    a = 1
    b = SAMPLE_SIZE
    res = [std_rand.uniform(a, b) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(623)
    plt.xlabel('三角形分布')
    low = 1
    height = SAMPLE_SIZE
    res = [std_rand.triangular(low, height) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(624)
    plt.xlabel('beta分布')
    alpha = 1
    beta = 10
    res = [std_rand.betavariate(alpha, beta) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(625)
    plt.xlabel('指数分布')
    lambd = 1.0 / ((SAMPLE_SIZE + 1) / 2.)
    res = [std_rand.expovariate(lambd) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(626)
    plt.xlabel('gamma分布')
    alpha = 1
    beta = 10
    res = [std_rand.gammavariate(alpha, beta) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(627)
    plt.xlabel('对数正态分布')
    mu = 1
    sigma = 0.5
    res = [std_rand.lognormvariate(mu, sigma) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(628)
    plt.xlabel('正态分布')
    mu = 1
    sigma = 0.5
    res = [std_rand.normalvariate(mu, sigma) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    plt.subplot(629)
    plt.xlabel('帕累托分布')
    alpha = 1
    res = [std_rand.paretovariate(alpha) for _ in range(1, SAMPLE_SIZE)]
    plt.hist(res, buckets)

    # 设置子图默认间距
    plt.tight_layout()
    plt.show()

def cleanNoiseData():
    """"
    convolve方法数据噪声去除
    """

    def moving_average(interval, window_size):
        window = np.ones(int(window_size)) / float(window_size)
        return np.convolve(interval, window, 'same')
    
    # 返回-4到4之间分布均匀的100个样本
    t = pylab.linspace(-4, 4, 100)
    y = sin(t) + pylab.randn(len(t)) * 0.1

    # x,y轴坐标，刻度样式
    pylab.plot(t, y, "k.")
    y_av = moving_average(y, 10)
    pylab.plot(t, y_av, "r")
    pylab.xlabel("时间", FontProperties=settings.FONT_SET)
    pylab.ylabel("值", FontProperties=settings.FONT_SET)
    pylab.grid(True)
    pylab.show()

def cleanDataByMF():
    """
    中值滤波过滤噪声
    """
    x = np.linspace(0, 1, 101)
    x[3::10] = 1.5

    pylab.plot(x)
    pylab.plot(scipy.signal.medfilt(x, 3))
    pylab.plot(scipy.signal.medfilt(x, 5))

    # 三个图例
    pylab.legend(['原始数据', '中值3过滤', '中值5过滤'])
    
    pylab.show()

def simple():
    """
    简单线形图
    """
    # y轴值，x轴赋默认值
    pylab.plot([1,2,3,4,5,6])
    # 另一条线,分别是x,y轴, x轴从左到右升序，两个列表值按下标对应
    pylab.plot([4,3,2,1], [1,2,3,4])
    pylab.show()

def showMany():
    """
    常见图集合
    """
    x = [1,2,3,4]
    y = [5,4,3,2]

    # 创建新图表
    plt.figure("多图集合")
    
    # 线性图
    s = plt.subplot(231)
    s.set_title('tutu')
    plt.plot(x, y)

    # 垂直柱状图
    plt.subplot(232)
    plt.bar(x, y)

    # 水平柱状图
    plt.subplot(233)
    plt.barh(x, y)

    # 堆叠柱状图，一个坐标轴中显示两个子图
    plt.subplot(234)
    plt.bar(x, y)
    y1 = [7,8,5,3]
    # y1以y接底
    plt.bar(x, y1, bottom=y, color='r')

    # 箱形图,最大值位于箱顶，最小值位于箱底
    # 中值位于箱体中部，箱体分8部分，上4分与下4分
    # 下4分为集合中大小较低的25%的数据
    plt.subplot(235)
    plt.boxplot(x)

    # 散点图
    plt.subplot(236)
    plt.scatter(x, y)

    plt.show()

def boxVsHist():
    """
    箱线图对比直方图
    """
    dataset = [113, 115, 119, 121, 124,
               124, 125, 126, 126, 126,
               127, 127, 128, 129, 130,
               130, 131, 132, 133, 136]

    pylab.subplot(121)
    # vert=False横向显示
    pylab.boxplot(dataset, vert=False)

    subplot(122)
    pylab.hist(dataset)

    pylab.show()

def showSinCos():
    """
    sinCos曲线
    """
    # -pi 到 pi 等分的256个数，不包含尾数
    x = np.linspace(-np.pi, np.pi, 256, endpoint=True)

    # cos数集合，随着数据的增大，cos值
    # 先减小后增大再减小
    y = np.cos(x)
    # sin数集合，随着数据的增大，sin值
    # 先增大后减小
    y1 = np.sin(x)

    # 坐标轴默认值xmin, xmax, ymin, ymax
    print(plt.axis())
    # 手动设置坐标轴刻度值范围
    # plt.axis([-1, 1, -10, 10])
    # plt.axis({'ymax': 100})
    # 根据数据设置坐标轴刻度范围
    # plt.autoscale()

    # 显示网格,显示纵向网格
    plt.grid(axis='x')

    plt.plot(x, y, linewidth=3)
    plt.plot(x, y1)

    plt.title("正余弦函数")
    plt.xlim(-3.0, 3.0)
    plt.ylim(-1.0, 1.0)
    # 给刻度值加标签显示
    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
              # $$laTex语法
              [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi/$'])
    plt.yticks([-1, 0, +1],
               [r'$-1$', r'$0$', r'$+1$'])

    # y=0水平线
    # plt.axhline()
    # # x=0垂直线
    # plt.axvline()
    # # y=0.5水平线
    # plt.axhline(0.5)

    # 0<=y<=0.5之间的水平线
    #plt.axhspan(0, 0.5)

    plt.show()

def showLine():
    """
    设置plot属性
    """
    x = [1,2,3,4,5]
    y = [5,4,3,2,1]

    #plt.plot(x, y, linewidth=3)
    #line, = plt.plot(x, y)
    #line.set_linewidth(3)
    lines = plt.plot(x, y)
    #plt.setp(lines, 'linewidth', 3)
    plt.title('下降曲线', color='#123456')
    # 坐标轴背景色
    #plt.axes(facecolor="#e5f0cf")

    plt.setp(lines, linewidth=1.5)
    plt.setp(lines, color='r')
    plt.setp(lines, label='下降直线')
    plt.setp(lines, linestyle='--')
    # 线条标记
    plt.setp(lines, marker='D')
    # 线条标记边缘色
    plt.setp(lines, markeredgecolor='b')
    plt.setp(lines, markeredgewidth=1.5)
    # 线条标记的大小
    plt.setp(lines, markersize=8)
    #plt.setp(lines, markerfacecolor='c')
    plt.setp(lines, markerfacecolor='#eeefff')
    #plt.setp(lines, markerfacecolor=(0.3, 0.3, 0.4))

    # 实线线端风格
    plt.setp(lines, solid_capstyle='round')
    plt.setp(lines, solid_joinstyle='miter')
    # 显示作者
    plt.setp(lines, visible=True)
    # x轴array值
    #plt.setp(lines, xdata=np.array([9,8,7,6,5]))
    # 为artist设置z轴位置
    plt.setp(lines, Zorder=1)
    
    plt.show()

def showTick():
    """
    设置刻度
    """
    # 获取轴对象
    ax = pylab.gca()
    # 紧凑视图, 因为数据比较多,最大刻度数20
    ax.locator_params(tight=True, nbins=10)
    # 正态分布数据曲线
    ax.plot(np.random.normal(10, .1, 100))

    # 设置主定位器x轴刻度为10的倍数
    ax.xaxis.set_major_locator(mp.ticker.MultipleLocator(10))
    
    pylab.show()

def showDate():
    """
    设置日期的显示
    """
    fig = pylab.figure()

    ax = pylab.gca()

    startdate = datetime.datetime(2013, 1, 1)
    stopdate = datetime.datetime(2013, 12, 31)
    delta = datetime.timedelta(days=1)

    # 起始到结束日期，间隔为delta
    dates = mp.dates.drange(startdate, stopdate, delta)
    values = np.random.rand(len(dates))

    ax = pylab.gca()
    # 日期形式的图例
    ax.plot_date(dates, values, linestyle='-', marker='')
    date_format = mp.dates.DateFormatter('%Y-%m-%d')
    # 格式器为日期格式
    ax.xaxis.set_major_formatter(date_format)

    # 自动格式日期
    fig.autofmt_xdate()

    pylab.show()

def showAnnotation():
    """
    添加注解
    """
    x1 = np.random.normal(30, 3, 100)
    x2 = np.random.normal(20, 2, 100)
    x3 = np.random.normal(10, 3, 100)

    plt.plot(x1, label="图1")
    plt.plot(x2, label="图2")
    plt.plot(x3, label="图3")

    # 把以上三个图例添加到图例框中,框位于2(upper_left)位置
    # 列数为3，边界框位置为(0.0, 1.02)，宽度为1.0,高度为0.102
    # 水平扩展至整个坐标轴区域，坐标轴与图例边框之间的间距为0
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
                ncol=3, mode="expand", borderaxespad=0.)

    # 在(5, 38)的位置显示"重要数据"，箭头指向(55, 30的数据)
    # xycoords='data'指定注解与数据使用相同的坐标系，箭头风格为'->'
    plt.annotate("重要数据", (55, 30), xycoords='data', xytext=(5, 38), arrowprops=dict(arrowstyle='->'))

    plt.show()

def moveAxeToCenter():
    """
    移动轴线到图中央
    """
    x = np.linspace(-np.pi, np.pi, 500, endpoint=True)
    y = np.sin(x)

    plt.plot(x, y)
    ax = plt.gca()
    # 设置color为None，隐藏轴线
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # 移动轴中心到(0,0)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))

    # 移动x,y刻度轴位置
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # 设置轴线在数据结束的地方停止延伸显示
    #ax.xaxis.set_smart_bounds(True)

    plt.show()

def showHist():
    """
    设置直方图
    """    
    mu = 100
    sigma = 15
    x = np.random.normal(mu, sigma, 10000)

    ax = plt.gca()
    # 宽度为35,类型为未填充
    plt.hist(x, bins=35, color='r', histtype='step')
    ax.set_xlabel('值')
    ax.set_ylabel('频率')
    ax.set_title(r'$Histogram mu={},sigma={}$'.format(mu, sigma))

    plt.show()

def showErrorBar():
    """
    误差条
    """
    x = np.arange(0, 10, 1)
    y = np.log(x)

    xe = 0.1 * np.abs(np.random.randn(len(y)))

    # 误差条颜色为红色，边缘为红色，内部颜色为青色,在y轴上生成误差条
    # 显示数据偏离
    plt.bar(x, y, yerr=xe, width=0.4, align='center', ecolor='r',
            edgecolor='r', color='cyan', label='试验 #1')
    plt.xlabel('尺寸')
    plt.ylabel('测量值')
    plt.title('测量数据')
    plt.legend(loc='upper left')

    plt.show()

def showPie():
    """
    饼图
    """
    pylab.figure(1, figsize=(6, 6))
    labels = '春', '夏', '秋', '冬'
    x = [15, 30, 45, 10]
    # explode元素个数为len(x)或者没有
    explode = (0.1, 0.1, 0.1, 0.2)

    # 从67度角位置升序显示，explode指定各个分裂程度
    # autopct格式化各个区块中的数据
    pylab.pie(x, explode=explode, labels=labels,
            autopct='%1.1f%%', startangle=67)
    pylab.title('季节降雨量')

    pylab.show()
    
def showFillingArea():
    """
    填充曲线区域
    """
    x = np.arange(0.0, 2, 0.01)
    y1 = np.sin(2*np.pi*x)
    y2 = 1.2*np.sin(4*np.pi*x)

    plt.figure()
    ax = plt.gca()

    # 两条曲线
    ax.plot(x, y1, x, y2, color='black')
    # 在x位置对应的y1与y2之间填充，如果y2>=y1则填充相应的颜色
    ax.fill_between(x, y1, y2, where=y2>=y1, facecolor='b',
                    interpolate=True)
    ax.fill_between(x, y1, y2, where=y2<=y1, facecolor='deeppink',
                    interpolate=True)
    ax.set_title('填充曲线')

    plt.show()

def setScatter():
    """
    彩色标记散点图
    """
    # 不相关数据
    x = np.random.randn(1000)
    y1 = np.random.randn(len(x))

    # 与x相关数据
    y2 = 1.2 + np.exp(x)

    ax1 = plt.subplot(121)
    # 透明度0.3
    plt.scatter(x, y1, color='indigo', alpha=0.3,
                edgecolors='white', label='不相关')
    plt.xlabel('不相关')
    plt.grid(True)
    plt.legend()

    # 坐标属性与ax1一致
    ax2 = plt.subplot(122, sharey=ax1, sharex=ax1)
    plt.scatter(x, y2, color='green', alpha=0.3,
                edgecolors='grey', label='相关')
    plt.xlabel('强相关')
    plt.grid(True)
    plt.legend()

    plt.show()

def setAxisAlphaAndSize():
    """
    设置坐标轴标签阴影与大小
    """
    from matplotlib import patheffects
    data = np.random.randn(70)

    fontsize = 18
    plt.plot(data)

    title = '这是一个图例的标题'
    x_label = '这是一个x轴标签'
    y_label = '这是一个y轴标签'

    title_text_obj = plt.title(title, fontsize=fontsize,
                                verticalalignment='bottom')
    # 设置标题阴影
    title_text_obj.set_path_effects([patheffects.withSimplePatchShadow()])

    offset_xy = (1, -1)
    rgbred = (1.0, 0.0, 0.0)
    alpha = 0.8
    # 阴影偏移量为(1, -1),默认为(2, -2),阴影颜色为(1.0, 0.0, 0.0)
    # 透明度为0.5
    pe = patheffects.withSimplePatchShadow(offset=offset_xy,
                                            shadow_rgbFace=rgbred,
                                            alpha=alpha)
    xlabel_obj = plt.xlabel(x_label, fontsize=fontsize, alpha=0.5)
    xlabel_obj.set_path_effects([pe])

    y_label_obj = plt.ylabel(y_label, fontsize=fontsize, alpha=0.5)
    y_label_obj.set_path_effects([pe])

    plt.show()

def setChartAlpha():
    """
    设置图表阴影效果
    """
    def setup(layout=None):
        fig = plt.figure()
        ax = fig.add_subplot(layout)
        return fig, ax
    
    def get_signal():
        t = np.arange(0., 2.5, 0.01)
        s = np.sin(5*np.pi*t)
        return t, s

    def plot_signal(t, s):
        line, = plt.plot(t, s, linewidth=5, color='magenta')
        return line
    
    def make_shadow(fig, axes, line, t, s):
        # 阴影偏移量
        delta = 2 / 72
        # 偏移转换对象，使用dpi_scale_trans转换可调用对象对delta，-delta
        # 进行比例调整，位置不会因输出设备而改变
        offset = mp.transforms.ScaledTranslation(delta, -delta, fig.dpi_scale_trans)
        # 偏移数据
        offset_transform = axes.transData + offset
        # 根据偏移数据绘制另一个图例
        axes.plot(t, s, linewidth=5, color='gray', transform=offset_transform,
                zorder=0.5 * line.get_zorder())

    fig, axes = setup(111)
    t, s = get_signal()
    line = plot_signal(t, s)
    make_shadow(fig, axes, line, t, s)
    axes.set_title('使用偏移转换设置图表阴影')
    plt.show()

def addDataSheetToChart():
    """
    往图表中添加数据表
    """
    plt.figure()
    plt.gca()
    y = np.random.randn(9)

    col_labels = ['姓名', '住址', '联系方式']
    row_labels = ['1', '2', '3']
    table_vals = [['张三', '广东广州', 15698654458],
                  ['李四', '广西南宁', 16599856648],
                  ['王五', '湖南长沙', 19865789631]]
    row_colors = ['red', 'gold', 'green']

    people_table = plt.table(cellText=table_vals,
            colWidths=[0.1]*3,
            rowLabels=row_labels,
            colLabels=col_labels,
            rowColours=row_colors,
            loc='upper right')
    # 可以通过axes对表格进行微调
    # fig = plt.figure()
    # axes = fig.add_table(people_table)

    plt.plot(y)

    plt.show()

def showSubplot():
    """
    显示子区
    """
    plt.figure(0)
    # subplot索引是0开始
    # 三行三列，从0行0列开始作图,列跨三个跨度
    plt.subplot2grid((3, 3), (0, 0), colspan=3)
    plt.subplot2grid((3, 3), (1, 0), colspan=2)
    plt.subplot2grid((3, 3), (1, 2))
    plt.subplot2grid((3, 3), (2, 0))
    plt.subplot2grid((3, 3), (2, 1), colspan=2)

    # 获取当前figure的所有轴
    all_axes = plt.gcf().axes
    for ax in all_axes:
        # 设置刻度字体大小
        for ticklabel in ax.get_xticklabels() + ax.get_yticklabels():
            ticklabel.set_fontsize(10)
    plt.suptitle('subplot2grid 示例')

    plt.show()

def setAxesbg():
    """
    设置图表背景
    """
    fig = plt.figure()
    axes = fig.add_subplot(111)
    rectangle = axes.patch
    rectangle.set_facecolor('cyan')

    # 创建一个补片，并在轴中显示这个补片
    rect = mp.patches.Rectangle((0.5, 0.5), width=6, height=12, color='red')
    axes.add_patch(rect)
    axes.figure.canvas.draw()

    plt.show()

def showSimpleGrid():
    """
    设置网格
    """
    data = [1,2,3,3,5,4,4.3,3]
    pylab.plot(data)
    pylab.grid(color='g', linestyle='--', linewidth=1)
    # 再次使用即关闭网格
    #pylab.grid()

    pylab.show()

def setGrid():
    """
    设置网格
    """
    def get_demo_image():
        f = get_sample_data('axes_grid/bivariate_normal.npy', asfileobj=False)
        Z = np.load(f)
        return Z, (-3, 4, -4, 3)
    
    def get_grid(fig=None, layout=None, nrows_ncols=None):
        assert(fig is not None)
        assert(layout is not None)
        assert(nrows_ncols is not None)
        grid = ImageGrid(fig, layout, nrows_ncols=nrows_ncols,
                        axes_pad=0.05, add_all=True, label_mode='L')
        return grid
    
    def load_image_to_grid(grid, Z, *images):
        min, max = Z.min(), Z.max()
        for i, image in enumerate(images):
            axes = grid[i]
            axes.imshow(image, origin='lower', vmin=min, vmax=max,
                        interpolation='nearest')
    fig = plt.figure(1, (8,6))
    grid = get_grid(fig, 111, (1, 3))
    Z, extent = get_demo_image()

    image1 = Z
    image2 = Z[:, :10]
    image3 = Z[:, 10:]

    load_image_to_grid(grid, Z, image1, image2, image3)

    plt.draw()
    plt.show()

def showSimpleContour():
    """
    简单等高线
    """
    data = [[1,2,3,3,5,4,4.3,3], [1,2,3,3,5,4,4.3,3]]
    # 数据必须是二维的
    cs = pylab.contour(data)
    pylab.colorbar(cs)

    pylab.show()
    

def showContour():
    """
    等高线
    """
    def process_signals(x, y):
        # exp返回e的幂次方
        return (1 - (x**2 + y**2)) * np.exp(-y ** 3 / 3)
    
    x = np.arange(-1.5, 1.5, 0.1)
    y = np.arange(-1.5, 1.5, 0.1)
    # 返回坐标矩阵
    X, Y = np.meshgrid(x, y)
    Z = process_signals(X, Y)
    N = np.arange(-1, 1.5, 0.3)
    # 绘制Z数组的等高线，水平数由N决定,颜色映射为jet
    CS = plt.contour(Z, N, linewidth=2, cmap=mp.cm.jet)
    # 为等高线添加标签
    plt.clabel(CS, inline=True, fmt='%1.1f', fontsize=10)
    plt.colorbar(CS)
    plt.title('我的函数: $z=(1-x^2+y^2) e^{-(y^3)/3}$')
   
    plt.show()

def setSimpleFill():
    """
    填充特定区域
    """
    t = range(1000)
    y = [sqrt(i) for i in t]
    plt.plot(t, y, color='red', lw=2)
    # 填充y轴值之间的区域，where=y
    plt.fill_between(t, y, color='silver')

    plt.show()

def setFill():
    """
    根据多条件填充区域
    """
    x = np.arange(0.0, 2, 0.01)
    y1 = np.sin(np.pi*x)
    y2 = 1.7 * np.sin(4*np.pi*x)

    fig = plt.figure()
    axes1 = fig.add_subplot(211)
    axes1.plot(x, y1, x, y2, color='grey')
    # where 接收长度为n的布尔数组
    axes1.fill_between(x, y1, y2, where=y2<=y1, facecolor='blue', interpolate=True)
    axes1.fill_between(x, y1, y2, where=y2>=y1, facecolor='gold', interpolate=True)
    axes1.set_title('蓝色区域表示y2<=y1, 金色区域表示y2>=y1.')
    axes1.set_ylim(-2, 2)

    # 大于1.0的数屏蔽掉
    y2 = np.ma.masked_greater(y2, 1.0)
    axes2 = fig.add_subplot(212, sharex=axes1)
    axes2.plot(x, y1, x, y2, color='black')
    axes2.fill_between(x, y1, y2, where=y2<=y1, facecolor='blue', interpolate=True)
    axes2.fill_between(x, y1, y2, where=y2<=y1, facecolor='gold', interpolate=True)
    axes2.set_title('同上, 但是有些隐藏.')
    axes2.set_ylim(-2, 2)
    axes2.grid('on')

    plt.show()

def showSimplePolar():
    """
    简单极线图
    """
    # 角度的宽度表示样本量的多少
    theta = [1, 2, 3]
    # 半径的长度表示个体样本的大小
    radii = [1.5, 2, 3]
    fig = plt.figure(figsize=(8, 8))
    # 轴原点坐标(0.1, 0.1), 坐标轴长度(0.6, 0.6)
    # 显示为极坐标
    ax = fig.add_axes([0.2, 0.2, 0.6, 0.6], polar=True)
    # 根据样本产生n个bar
    bars = ax.bar(theta, radii, tick_label=('样本1','样本2','样本3'),
                edgecolor='cyan')

    colormap = lambda r: mp.cm.Set2(r / len(theta))
    # 分别设置不同的颜色
    for r, each in zip(radii, bars):
        each.set_facecolor(colormap(r))
        each.set_alpha(0.5)

    plt.annotate("重要数据", (1, 3), xycoords='data', xytext=(10, 0.5), arrowprops=dict(arrowstyle='->'))

    plt.show()

def showPolar():
    """
    极线图
    """
    figsize = 7
    colormap = lambda r: mp.cm.Set2(r / 20.)
    N = 18
    # 正方形图表
    fig = plt.figure(figsize=(figsize, figsize))
    # 添加极坐标轴
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7], polar=True)
    # 角度集合
    theta = np.arange(0.0, 2 * np.pi, 2 * np.pi / N)
    # 极线距离集合
    radii = 20 * np.random.randn(N)
    width = np.pi / 4 * np.random.randn(N)
    # 饼图集合
    bars = ax.bar(theta, radii, width=width, bottom=0.0)
    # 逐个添加极线条
    for r, bar in zip(radii, bars):
        bar.set_facecolor(colormap(r))
        bar.set_alpha(0.6)
    
    plt.show()

def showFileSysTree():
    """
    使用极线图显示文件系统树
    """
    def build_folders(start_path):
        folders = []

        for each in get_directories(start_path):
            size = get_size(each)
            if size >= 25 * 1024 * 1024:
                folders.append({'size': size, 'path': each})
        for each in folders:
            print("路径:", os.path.basename(each['path']))
            print("大小", str(each['size'] / 1024 / 1024), "MB")
        
        return folders

    def get_size(path):
        assert(path is not None)
        total_size = 0
        total_size = os.path.getsize(path)
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    size = os.path.getsize(fp)
                    total_size += size
                except OSError as e:
                    print(str(e))
                    pass
        return total_size

    def get_directories(path):
        dirs = set()
        for dirpath, dirnames, filenames in os.walk(path):
            #dirs = set([os.path.join(dirpath, x) for x in dirnames])
            for f in filenames:
                dirs.add(os.path.join(dirpath, f))
            #只需要第一个文件
            break
        return dirs

    def draw(folders):
        figsize = (8, 8)
        ldo, rup = 0.1, 0.8
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([ldo, ldo, rup, rup], polar=True)
        
        x = [os.path.basename(x['path']) for x in folders]
        y = [y['size'] / 1024 / 1024 for y in folders]
        theta = np.arange(0.0, 2 * np.pi, 2 * np.pi / len(x))
        radii = y
        bars = ax.bar(theta, radii)
        middle = 90 / len(x)
        theta_ticks = [t * (180 / np.pi) + middle for t in theta]
        lines, labels = plt.thetagrids(theta_ticks, labels=x)

        for step, each in enumerate(labels):
            each.set_rotation(theta[step] * (180 / np.pi) + middle)
            each.set_fontsize(8)

        colormap = lambda r: mp.cm.Set2(r / len(x))
        for r, each in zip(radii, bars):
            each.set_facecolor(colormap(r))
            each.set_alpha(0.5)

        plt.show()

    start_path = r'E:\迅雷下载'
    if not os.path.exists(start_path):
        print("路径不存在:{}".format(start_path))
        sys.exit(-1)

    folders = build_folders(start_path)
    if len(folders) < 1:
        print("路径底下没有文件夹:{}".format(start_path))
        sys.exit(-1)

    draw(folders)

def show3DBar():
    """
    简单3D柱状图
    """
    fig = plt.figure()
    # 3D图例
    ax = fig.add_subplot(111, projection='3d')

    # x,y,z轴数据
    for z in [2011, 2012, 2013, 2014]:
        xs = range(1, 13)
        ys = 1000 * np.random.rand(12)
        
        # 随机颜色映射
        color = plt.cm.Set2(std_rand.choice(range(plt.cm.Set2.N)))
        # 指定y轴作为z轴的维度,其它3d图如scatter,plot等
        ax.bar(xs, ys, zs=z, zdir='y', color=color, alpha=0.8)

    ax.xaxis.set_major_locator(mp.ticker.FixedLocator(xs))
    ax.yaxis.set_major_locator(mp.ticker.FixedLocator(ys))

    ax.set_xlabel('月份')
    ax.set_ylabel('年份')
    ax.set_zlabel('数据')

    plt.show()

def showSimple3dPlot():
    """
    简单3d图
    """
    x = [1, 2, 3]
    y = [1, 2, 3]
    z = [1, 2, 3]

    dx = [0.1] * 3
    dy = [0.1] * 3
    dz = [0.1] * 3

    fig = plt.figure()
    color = plt.cm.Set2(std_rand.choice(range(plt.cm.Set2.N)))
    ax = fig.add_subplot(211, projection='3d')
    ax.scatter(x, y, zs=z, zdir='y', color=color, alpha=0.6)
    ax = fig.add_subplot(212, projection='3d')
    ax.bar(x, y, zs=z, zdir='y', color=color, alpha=0.6)
    plt.show()

def showHbPb():
    """
    三翼面图
    """
    # 角度数量
    n_angles = 36
    # 半径数量
    n_radii = 8

    radii = np.linspace(0.125, 1.0, n_radii)
    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    x = np.append(0, (radii * np.cos(angles)).flatten())
    y = np.append(0, (radii * np.sin(angles)).flatten())
    z = np.sin(-x * y)

    fig = plt.figure()
    ax = plt.gca(projection='3d')
    ax.plot_trisurf(x, y, z, cmap=mp.cm.jet, linewidth=0.2)

    plt.show()

def show3dHist():
    """
    3d直方图
    """
    samples = 25
    x = np.random.normal(5, 1, samples)
    y = np.random.normal(3, .5, samples)

    fig = plt.figure()
    ax = fig.add_subplot(211, projection='3d')
    # 计算两个空间的直方图
    hist, xedges, yedges = np.histogram2d(x, y, bins=10)
    elements = (len(xedges) - 1) * (len(yedges) - 1)
    xpos, ypos = np.meshgrid(xedges[:-1]+.25, yedges[:-1]+.25)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(elements)
    dx = .1 * np.ones_like(zpos)
    dy = dx.copy()
    dz = hist.flatten()
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', alpha='0.4')
    ax.set_xlabel('x轴')
    ax.set_ylabel('y轴')
    ax.set_zlabel('z轴')

    ax2 = fig.add_subplot(212)
    ax2.scatter(x, y)
    ax2.set_xlabel('x轴')
    ax2.set_ylabel('y轴')

    plt.show()

def showAnimation():
    """
    动图
    """
    from matplotlib import animation

    fig = plt.figure()
    ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
    line, = ax.plot([], [], lw=2)

    def init():
        """
        清空轴数据
        """
        line.set_data([], [])
        return line,

    def animate(i):
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i)) * np.cos(22 * np.pi * (x - 0.01 *1))
        line.set_data(x, y)
        return line,
    
    # 动画长度200(一次循环包含的帧数),每20ms更新一次,blit=True更新所有点(false更新变化点)
    # 每次更新调用init_func函数，使用animate(frames)作图
    animator = animation.FuncAnimation(fig, animate, init_func=init,
                                        frames=200, interval=20, blit=True)

    # 保存动图, 使用ffmepg_file编码器
    # animator.save('matplot动图.mp4', fps=30,
    #                 extra_args=['-vcodec', 'libx264'],
    #                 writer='ffmpeg')

    plt.show()

def showMayaAnimation():
    """
    maya动图
    """
    import mayavi.mlab as mmb

    n_mer, n_long = 6, 11
    pi = np.pi
    dphi = pi / 1000.0
    phi  = np.arange(0.0, 2*pi + 0.5*dphi, dphi, 'd')
    mu = phi * n_mer
    x = np.cos(mu) * (1 + np.cos(n_long*mu/n_mer)*0.5)
    y = np.sin(mu) * (1 + np.cos(n_long*mu/n_mer)*0.5)
    z = np.sin(n_long*mu/n_mer)*0.5
    l = mmb.plot3d(x, y, z, np.sin(mu), tube_radius=0.025, colormap='Spectral')
    ms = l.mlab_source
    
    for i in range(100):
        x = np.cos(mu) * (1 + np.cos(n_long*mu/n_mer + np.pi*(i+1)/5)*0.5)
        scalars = np.sin(mu + np.pi*(i+1)/5)
        ms.set(x=x, scalars=scalars)

def imgViewByPyglet():
    """
    使用pyglet察看图像
    """
    import pyglet

    window = pyglet.window.Window()
    image = pyglet.resource.image('captcha_normal.png')

    @window.event
    def on_draw():
        window.clear()
        image.blit(0, 0)

    pyglet.app.run()

def filterImage():
    """
    使用PIL滤波器过滤图像
    """
    class FilterImage():
        def __init__(self, image_file=None):
            self.fixed_filters = [ff for ff in dir(ImageFilter) if ff.isupper()]
            assert(image_file is not None)
            assert(os.path.isfile(image_file) is True)
            self.image_file = image_file
            self.image = Image.open(self.image_file)

        def _make_temp_dir(self):
            from tempfile import mkdtemp
            # 创建临时目录
            self.ff_tmpdir = mkdtemp(prefix='ff_demo')
        
        def _get_temp_name(self, filter_name):
            # 获取文件名与文件扩展名
            name, ext = os.path.splitext(os.path.basename(self.image_file))
            newimage_file = name + '-' + filter_name + ext
            path = os.path.join(self.ff_tmpdir, newimage_file)
            return path

        def _get_filter(self, filter_name):
            real_filter = eval('ImageFilter.' + filter_name)
            return real_filter

        def applyfilter(self, filter_name):
            print("正在使用滤波器:{}".format(filter_name))
            filter_callable = self._get_filter(filter_name)
            if filter_name in self.fixed_filters:
                temp_img = self.image.filter(filter_callable)
            else:
                print("不支持该滤波器:{}".format(filter_name))
            return temp_img

        def run_fixed_filter(self):
            self._make_temp_dir()
            for ffilter in self.fixed_filters:
                temp_img = self.applyfilter(ffilter)
                temp_img.save(self._get_temp_name(ffilter))
            print('过滤后的图像路径:{}'.format(self.ff_tmpdir))

    imgfilter = FilterImage('captcha_normal.png')
    imgfilter.run_fixed_filter()

def adjustImageSize():
    """
    使用PIL调整指定目录下图像大小
    """
    class Thumbnailer(object):
        def __init__(self, src_folder=None):
            self.src_folder = src_folder
            # 调整比例0.3
            self.radio = .3
            self.thumbnail_folder = 'thumbnails'

        def _create_thumbnailers_folder(self):
            thumb_path = os.path.join(self.src_folder, self.thumbnail_folder)
            if not os.path.isdir(thumb_path):
                os.makedirs(thumb_path)

        def _build_thumb_path(self, image_path):
            root = os.path.dirname(image_path)
            name, ext = os.path.splitext(os.path.basename(image_path))
            suffix = '.thumbnail'
            return os.path.join(root, self.thumbnail_folder, name + suffix + ext)

        def _load_files(self):
            files = set()
            for each in os.listdir(self.src_folder):
                each = os.path.abspath(self.src_folder + '/' + each)
                if os.path.isfile(each):
                    files.add(each)
            return files

        def _thumb_size(self, size):
            return (int(size[0] * self.radio), int(size[1] * self.radio))

        def create_thumbnails(self):
            self._create_thumbnailers_folder()
            files = self._load_files()

            for each in files:
                print("正在处理:{}".format(each))
                try:
                    img = Image.open(each)
                    thumb_size = self._thumb_size(img.size)
                    resized = img.resize(thumb_size, Image.ANTIALIAS)
                    savepath = self._build_thumb_path(each)
                    resized.save(savepath)
                except IOError as e:
                    print("发生错误:{}".format(str(e)))

    src_folder = r'E:\pictures'
    if not os.path.isdir(src_folder):
        print("路径不存在:{}".format(src_folder))
        sys.exit(-1)
    thumbs = Thumbnailer(src_folder)
    thumbs.thumbnail_folder = 'THUMBS'
    thumbs.radio = 0.1
    thumbs.create_thumbnails()

def addImgToChart():
    """
    向图表中添加图像
    """
    from matplotlib._png import read_png
    from matplotlib.offsetbox import TextArea, \
    OffsetImage, AnnotationBbox

    def load_data():
        import csv
        with open('ship.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            datarows = []
            for row in reader:
                datarows.append(row)
            return header, datarows
    
    def format_data(datarows):
        years, temps, pirates = [], [], []
        for each in datarows:
            years.append(each[0])
            temps.append(each[1])
            pirates.append(each[2])
        return years, temps, pirates

    fig = plt.figure(figsize=(16, 8))
    ax = plt.subplot(111)
    header, datarows = load_data()
    xlabel, ylabel = header[0], header[1]
    years, temps, pirates = format_data(datarows)
    years = list(map(int, years))
    title = '温度与船只的数量关系'
    plt.plot(years, temps, lw=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # 在每一个点添加图像注解框
    for x in range(len(years)):
        xy = years[x], temps[x]
        ax.plot(xy[0], xy[1], 'ok')
        ship = read_png('captcha_normal.png')
        zoomc = int(pirates[x]) * (1 / 90000.)
        imagebox = OffsetImage(ship, zoom=zoomc)
        # 注解类
        ab = AnnotationBbox(imagebox, xy,
                            xybox=(-200.*zoomc, 200.*zoomc),
                            xycoords='data',
                            boxcoords='offset points',
                            pad=0.1,
                            arrowprops=dict(arrowstyle='->',
                            connectionstyle='angle, angleA=0, angleB=-30, rad=3'))
        ax.add_artist(ab)

        no_ship = TextArea(pirates[x], minimumdescent=False)
        ab = AnnotationBbox(no_ship, xy,
                            xybox=(50., -25.),
                            xycoords='data',
                            boxcoords='offset points',
                            pad=.3,
                            arrowprops=dict(arrowstyle='->',
                            connectionstyle='angle, angleA=0, angleB=-30, rad=3'))
        ax.add_artist(ab)
    
    plt.grid(1)
    plt.xlim(2000, 2020)
    plt.ylim(0, 18)
    plt.title(title)

    plt.show()

def test():
    ''
    fig = plt.figure(figsize=(16, 8))
    # plt.plot(['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'], 
    # ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'], 
    # lw=2)
    plt.plot([1, 2, 3], ['1', '2', '3'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.grid(1)
    plt.xlim(2000, 2020)
    plt.ylim(0, 18)
    plt.title(title)

    plt.show()
    
if __name__ == "__main__":
    #---------------------------------------------------start
    tupletime = time.localtime()
    print('program start:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print()
    starttime = time.time()

    os.chdir(r'E:\git\Olaful\Olaful.github.io\python\PythonApplication\PythonApplication\myfile')

    # 能显示中文
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # 能显示负号
    matplotlib.rcParams['axes.unicode_minus'] = False

    addImgToChart()

    #---------------------------------------------------end
    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f}seconds'.format(endtime-starttime))