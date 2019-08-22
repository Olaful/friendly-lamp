import pandas as pd
import numpy as np
import time
import functools

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
    print(l)

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

def boolIndex():
    # 布尔索引
    a = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    b = pd.DataFrame(np.random.randn(6, 4), index=a, columns=list('ABCD'))
    # 根据某列条件布尔判断筛选
    c = b[b.A > 0]
    # 大于零的数据显示，否则显示NaN
    d = b[b > 0]
    e = b.copy()
    e['E'] = ['one', 'one', 'two', 'three', 'four', 'three']
    # 在指定值中过滤
    f = e[e['E'].isin(['two', 'four'])]
    print(b)
    print(c)

def setting():
    """
    设置值
    """
    a = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    b = pd.DataFrame(np.random.randn(6, 4), index=a, columns=list('ABCD'))
    c = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130102', periods=6))
    # 设置某列的的值为指定序列，按索引对应
    b['F'] = c
    # 根据修改特定位置的值
    b.at[a[0], 'A'] = 0
    # 根据数字索引修改值
    b.iat[0,1] = 0
    # 用numpy数组赋值
    b.loc[:,'D'] = np.array([5]*len(b))
    # where 条件赋值
    b[b>0] = -b
    print(b)

def missData():
    """
    处理缺失数据
    """
    a = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    b = pd.DataFrame(np.random.randn(6, 4), index=a, columns=list('ABCD'))
    c = b.reindex(index=a[0:4], columns=list(b.columns) + ['E'])
    c.loc[a[0]:a[1], 'E'] = 1
    # 如果某一行有NanN值，则删除掉该行
    d = c.dropna(how='any')
    # 以指定值填充NaN值
    e = c.fillna(value=5)
    # 返回各个元素是否NaN值的数组
    f = pd.isna(c)
    # 使用前面的值填充
    g = c.fillna(method='ffill')
    print(b)
    print(c)

def stats():
    """
    数学运算
    """
    a = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    b = pd.DataFrame(np.random.randn(6, 4), index=a, columns=list('ABCD'))
    # 针对列求中值
    c = b.mean()
    # 向下偏移两位，索引不偏移，空出的位置由NaN填充
    d = pd.Series([1,3,5,np.nan,6,8], index=a).shift(2)
    # d 会广播至与b相同的维度后再执行相减操作
    e = b.sub(d, axis='index')
    print(b)
    print(d)

def apply():
    """
    应用函数
    """
    a = pd.date_range('20130101', periods=6)
    # 为数组指定行索引，列名
    b = pd.DataFrame(np.random.randn(6, 4), index=a, columns=list('ABCD'))
    # 应用累加函数
    c = b.apply(np.cumsum)
    # 应用最大值与最小值之差函数
    d = b.apply(lambda x: x.max() - x.min())
    print(b)
    print(c)

def histogram():
    """
    类直方图统计
    """
    a = pd.Series(np.random.randint(0, 7, size=10))
    # 计算每个值出现的次数
    b = a.value_counts()
    print(a)
    print(b)

def strMethod():
    """
    字符串函数
    """
    a = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
    # 小写化
    b = a.str.lower()
    print(b)

def merge():
    """
    合并数据
    """
    a = pd.DataFrame(np.random.randn(10, 4))
    b = [a[0:3], a[3:7], a[7:]]
    # 按行合并
    c = pd.concat(b)
    d = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
    e = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
    # 类似sql的left join on, 不会出现重复的key列名
    f = pd.merge(d, e, on='key')
    g = pd.DataFrame(np.random.randn(8, 4), columns=['A', 'B', 'C', 'D'])
    h = g.iloc[3]
    # 追加行
    i = g.append(h)
    print(h)
    print(i)

def group():
    """
    分组统计
    """
    a = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                        'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                        'C': np.random.randn(8),
                        'D': np.random.randn(8)})
    # 分组统计
    b = a.groupby('A').sum()
    # 按多个字段分组
    c = a.groupby(['A', 'B']).sum()
    print(a)
    print(c)

def reshape():
    a = list(zip(*[['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
                 ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]))
    # 分组索引，一级组为fisrt, 二级组为second
    b = pd.MultiIndex.from_tuples(a, names=['first', 'second'])
    c = pd.DataFrame(np.random.randn(8, 2), index=b, columns=['A', 'B'])
    d = c[:4]
    # 垂直叠加列
    e = d.stack()
    # 叠加的逆操作, 解迭加的时候只能在不同的组间解
    f = e.unstack()
    # 按第二组索引解
    g = e.unstack(1)
    h = e.unstack(0)

    #print(b)
    #print(c)
    print(c.index.names[0])

def pivotTb():
    """
    转换表轴
    """
    a = pd.DataFrame({'A': ['one', 'one', 'two', 'three']*3,
                        'B': ['A', 'B', 'C']*4,
                        'C': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar']*2,
                        'D': np.random.randn(12),
                        'E': np.random.randn(12)})
    # 第一级索引为A列，第二级索引为B列，使用C列数值做列头，行的值由D，E列组成
    b = pd.pivot_table(a, values=['D', 'E'], index=['A', 'B'], columns=['C'])

    print(a)
    print('...............')
    print(b)

def timeSeries():
    """
    时间序列化
    """
    # 秒为step的序列
    a = pd.date_range('1/1/2012', periods=100, freq='S')
    b = pd.Series(np.random.randint(0, 500, len(a)), index=a)
    # 按5分钟的频率采样汇总
    c = b.resample('5Min').sum()
    d = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
    e = pd.Series(np.random.randn(len(d)), d)
    # UTC 时间格式
    f = e.tz_localize('UTC')
    # 转成其他时区
    g = f.tz_convert('US/Eastern')
    h = pd.date_range('1/1/2012', periods=5, freq='M')
    i = pd.Series(np.random.randn(len(h)), index=h)
    # 转换周期，默认月
    j = i.to_period()
    # 转换成年月日格式
    k = j.to_timestamp()
    # 1990季度1到2000季度4范围，周期是
    l = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV')
    m = pd.Series(np.random.randn(len(l)), l)
    m.index = (l.asfreq('M', 'e') + 1).asfreq('H', 's') + 9
    n = m.head()
    print(i)
    print(j)

def cate():
    """
    分类
    """
    a = pd.DataFrame({'id': [1,2,3,4,5,6], 'raw_grade': ['a', 'b', 'b', 'a', 'a', 'e']})
    # 设置列为分类列
    a['grade'] = a['raw_grade'].astype('category')
    b = a['grade']
    # 给分类取名
    a['grade'].cat.categories = ['very good', 'good', 'very bad']
    # 设置分类并添加缺少的分类
    a['grade'] = a['grade'].cat.set_categories(['very bad', 'bad', 'medium', 'good', 'very good'])
    c = a['grade']
    # 根据分类列进行排序
    d = a.sort_values(by='grade')
    # 按分类分组统计
    e = a.groupby('grade').size()
    print(a)
    print(e)

def plot():
    """
    matplotlib对象
    """
    a = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    b = a.cumsum()
    # matplotlib的subplot对象
    c = b.plot()
    e = pd.DataFrame(np.random.randn(1000, 4), index=a.index, columns=['A', 'B', 'C', 'D'])
    f = e.cumsum()
    print(c)

def inOut():
    """
    导入导出
    """
    a = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    #a.to_csv(r'D:\tmpfile\pdcsv.csv')
    #b = pd.read_csv(r'D:\tmpfile\pdcsv.csv')
    #a.to_hdf(r'D:\tmpfile\pdh5.h5', 'df')
    #c = pd.read_hdf(r'D:\tmpfile\pdh5.h5', 'df')
    #a.to_excel(r'D:\tmpfile\pdexcel.xlsx', sheet_name='sheet1')
    d = pd.read_excel(r'D:\tmpfile\pdexcel.xlsx', index_col=None, na_values=['NA'])
    print(d)

def other():
    """
    """
    # 不能用来做真假判断，因为取值不明确
    if pd.Series([False, True, False]):
        print('hello')

def idioms():
    a = pd.DataFrame({"AAA": [4,5,6,7], "BBB": [10,20,30,40], "CCC": [100,50,-30,-50]})
    # 如果。。则。。
    a.loc[a.AAA >= 5, 'BBB'] = -1
    a.loc[a.AAA >= 5, ['BBB', 'CCC']] = 555
    b = pd.DataFrame({"AAA": [True]*4, "BBB": [False]*4, "CCC": [True,False]*2})
    # 对应标记的位置如果为False，则设定指定值
    c = a.where(b, -1000)
    # 使用numpy的where方法筛选
    a['logic'] = np.where(a['AAA'] > 5, 'high', 'low')
    d = a.loc[(a['BBB'] < 25) & (a['CCC'] >= -40), 'AAA']
    a.loc[(a['BBB'] > 25) | (a['CCC'] >= 75), 'AAA'] = 0.1
    # 排序
    a.loc[a.CCC.abs().argsort()]
    e = pd.DataFrame({"AAA": [4,5,6,7], "BBB": [10,20,30,40], "CCC": [100,50,-30,-50]})
    f = e.AAA <= 5.5
    g = e.BBB == 10.0
    h = e.CCC > -40.0
    # 列布尔判断组合筛选
    i = f & g & h
    j = [f,g,h]
    k = functools.reduce(lambda x,y: x&y, j)
    l = e[i]
    print(e)
    print(l)

def multiIdex():
    a = pd.DataFrame({
        'row': [0, 1, 2],
        'One_X': [1.1, 1.1, 1.1],
        'One_Y': [1.2, 1.2, 1.2],
        'Two_X': [1.11, 1.11, 1.11],
        'Two_Y': [1.22, 1.22, 1.22]
    })
    b = a.set_index('row')
    a.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in a.columns])
    c = a.stack(0).reset_index(1)
    c.columns = ['Sample', 'ALL_X', 'ALL_Y']
    d = pd.MultiIndex.from_tuples([(x, y) for x in ['A', 'B', 'C'] for y in ['O', 'I']])
    e = pd.DataFrame(np.random.randn(2, 6), index=['n', 'm'], columns=d)
    # 对每个元素以C列为除数做相除操作
    f = e.div(e['C'], level=1)
    print(a)
    print(b)

def group2():
    a = pd.DataFrame({
        'code': ['foo', 'bar', 'baz'] * 2,
        'data': [0.16, -0.21, 0.33, 0.45, -0.59, 0.62],
        'flag': [False, True] * 3
    })
    b = a.groupby('code')
    c = b[['data']].transform(sum).sort_values(by='data')
    d = a.loc[c.index]
    e = pd.date_range(start='2014-10-07', periods=10, freq='2min')
    f = pd.Series(data=list(range(10)), index=e)
    def MyCust(x):
        if len(x) > 2:
            return x[1] * 1.234
        return pd.NaT
    g = {'Mean': np.mean, 'Max':np.max, 'Custom':MyCust}
    h = f.resample('5min').apply(g)
    i = pd.DataFrame({
        'Color': 'Red Red Red Blue'.split(),
        'Value': [100, 150, 50, 50]
        })
    i['Counts'] = i.groupby(['Color']).transform(len)
    print(i)

if __name__ == '__main__':
    starttime = time.time()

    reshape()

    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, \
    tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f} seconds'.format(endtime-starttime))