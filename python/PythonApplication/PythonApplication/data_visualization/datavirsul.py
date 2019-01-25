import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import xlrd
from xlrd import open_workbook, xldate_as_tuple
from pprint import pprint
import os
import time
from datetime import datetime

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
from PIL import Image

os.chdir(r'E:\git\Olaful\Olaful.github.io\python\PythonApplication\PythonApplication\myfile')

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

def sinCos():
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

    plt.plot(x, y)
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
    

if __name__ == "__main__":
    #---------------------------------------------------start
    tupletime = time.localtime()
    print('program start:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print()
    starttime = time.time()

    # 能显示中文
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # 能显示负号
    matplotlib.rcParams['axes.unicode_minus'] = False

    sinCos()

    #---------------------------------------------------end
    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f}seconds'.format(endtime-starttime))