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

os.chdir(r'E:\hexo\source.Olaful.github.io\Olaful.github.io\python\PythonApplication\PythonApplication\myfile')

def setParam():
    """
    matplotlib默认配置从rc文件中(位于当前用户目录下)读取
    可以通过两种方式手动指定属性
    """
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
    def get_rand_len_data(len):
        data = []
        for _ in range(len):
            data.append(random.randint(0,9))
        string = ''.join(list(map(str, data)))
        return string

    with open('bigdata.data', 'w', encoding="utf-8") as file:
        for _ in range(1000000):
            f, s, t = get_rand_len_data(9),get_rand_len_data(13), get_rand_len_data(4)
            file.write('{} {} {}\n'.format(f, s, t))

def readJsonData():
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
    # 先读取9个宽度的字符,s表示c语言中的char[]，接着读取14个，以此类推，根据文件而定
    # 600833296 4937438977840 7014
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
    if export_format == 'csv':
        return write_csv(data)
    elif export_format == 'json':
        return write_json(data)
    elif export_format == 'xlsx':
        return write_xlsx(data)
    else:
        print('不支持的格式:{}'.format(export_format))

def write_csv(data):
    f = StringIO()
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
    return f.getvalue()

def write_json(data):
    j = json.dumps(data)
    return j

def write_xlsx(data):
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
        

if __name__ == "__main__":
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