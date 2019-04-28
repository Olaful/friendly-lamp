import pandas as pd
import numpy as np
import time

def createData():
    """
    创建数据
    """
    a = pd.Series([1, 3, 5, np.nan, 6, 8])
    # 以起始日期建立数据日期序列
    b = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    c = pd.DataFrame(np.random.randn(6, 4), index=b, columns=list('ABCD'))
    # 根据字典建立二维数组，元素少的列会自动扩充至元素个数最多的列的数量
    d = pd.DataFrame({'A': 1., 'B': pd.Timestamp('20130101'), 'C': pd.Series(1, index=list(range(4)), dtype='float32'), \
                    'D': np.array([3]*4, dtype='int32'), 'E': pd.Categorical(['test', 'train', 'test', 'train']), \
                    'F': 'foo'})
    # 获取头部或尾部指定数量的行数
    e = c.head(2)
    f = c.tail(3)
    g = c.index
    h = c.columns
    i = c.values
    # 针对每一列的常见数学统计，如max, std
    j = c.describe()
    # 倒置行列
    k = c.T
    # 根据索引降序排序，axis=1即列索引
    l = c.sort_index(axis=1, ascending=False)
    # 根据B列的值进行排序
    m = c.sort_values(by='B')
    print(c)
    print(m)

def selData():
    """
    选择数据
    """
    a = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    b = pd.DataFrame(np.random.randn(6, 4), index=a, columns=list('ABCD'))
    # 根据列名获取数据
    c = b['B']
    # 索引范围切片
    d = b[0:3]
    # 值范围切片
    e = b['20130102':'20130104']
    # 按索引名选择
    f = b.loc['2013-01-01']
    # 先筛选出行，再筛选出列
    g = b.loc['2013-01-01', ['A', 'B']]
    h = b.loc['2013-01-01', 'A']
    # 比loc更快速度定位到某个元素
    i = b.at[a[0], 'A']
    # 获取每一列的第四个数
    j = b.iloc[3]
    # 数字分片索引
    k = b.iloc[3:5, 0:2]
    # 与numpy一样用法的数组索引
    l = b.iloc[[1,2,4], [0,2]]
    m = b.iloc[1:3,:]
    n = b.iloc[1,1]
    # 比loc更快速度定位到某个元素
    o = b.iat[1,1]
    print(b)
    print(o)

if __name__ == '__main__':
    starttime = time.time()

    selData()

    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, \
    tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f} seconds'.format(endtime-starttime))