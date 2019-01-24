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
import random
import struct
import string
import requests
import argparse
import json
try:
    import cStringIO as StringIO
except:
    from io import StringIO

import sqlite3
import aide
from pylab import *
import pylab
import scipy.misc
import scipy
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

    # 子图像
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
    plt.figure()
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
    # seed系统时间
    seed()
    real_rand_vals = []
    real_rand_vals = [random() for _ in range(100)]
    pylab.hist(real_rand_vals, 20)
    pylab.xlabel('随机数')
    pylab.ylabel('个数')

    pylab.subplot()
    real_rand_vals = [randint(1,7) for _ in range(100)]
    pylab.hist(real_rand_vals, 20)
    pylab.xlabel('随机数')
    pylab.ylabel('个数')
    
    pylab.show()

if __name__ == "__main__":
    #---------------------------------------------------start
    tupletime = time.localtime()
    print('program start:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print()
    starttime = time.time()

    showRandData()

    #---------------------------------------------------end
    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f}seconds'.format(endtime-starttime))