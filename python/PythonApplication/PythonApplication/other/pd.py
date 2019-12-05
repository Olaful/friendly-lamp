import pandas as pd
import numpy as np
import time
import functools
import datetime
from io import StringIO

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
    print(d)

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

def selection():
    a = pd.DataFrame({"AAA": [4,5,6,7], "BBB": [10,20,30,40], "CCC":[100,50,-30,-50]})
    b = a[(a.AAA <= 6) & (a.index.isin([0,2,4]))]
    a.index = ['foo', 'bar', 'boo', 'kar']
    # 基于标签的索引
    c = a.loc['bar':'kar']
    d = a.iloc[0:3]
    a.index = [1,2,3,4]
    # 当索引为数值的时候，注意标签索引
    # 与位置索引容易产生误解
    e = a.iloc[1:3]
    f = a.loc[1:3]
    # 取反操作
    g = a[~((a.AAA <= 6) & (a.index.isin([0,2,4])))]
    print(a)
    print(g)

def selection2():
    a = np.random.randn(100, 4)
    b = pd.date_range('1/1/2013', periods=100, freq='D')
    c = ['A', 'B', 'C', 'D']
    e, f, g = pd.DataFrame(a, b, c), pd.DataFrame(a, b, c), pd.DataFrame(a, b, c)
    # 扩展维度
    h = pd.Panel({'df1': e, 'df2': f, 'df3': g})
    h.loc[:, :, 'F'] = pd.DataFrame(a, b, c)
    print(h.loc[:,:])

def selection3():
    a = pd.DataFrame({"AAA": [1,2,1,3], "BBB": [1,1,2,2], "CCC":[2,1,2,3]})
    b = {1: "Alpha", 2: "Beta", 3: "Charlie"}
    c = [c+'_cat' for c in a.columns]
    # 对列值应用映射
    a[c] = a[a.columns].applymap(b.get)
    d = pd.DataFrame({'AAA': [1,1,1,2,2,2,3,3], 'BBB': [2,1,3,4,5,1,2,3]})
    # 分组后再求某列最小值
    e = d.loc[d.groupby('AAA')['BBB'].idxmin()]
    # 
    f = d.sort_values(by='BBB').groupby('AAA', as_index=False).first()
    print(f)

def multiIndex():
    a = [('AA', 'one'), ('AA', 'six'), ('BB', 'one'), ('BB', 'two' ), ('BB', 'six')]
    b = pd.MultiIndex.from_tuples(a)
    c = pd.DataFrame([11, 22, 33, 44, 55], b, ['MyData'])
    # 获取第一级指定索引的第一轴数据
    d = c.xs('BB', level=0, axis=0)
    # 获取第二级指定索引的第一轴数据
    e = c.xs('six', level=1, axis=0)
    print(e)

def multiIndex2():
    a = list(itertools.product(['Ada', 'Quinn', 'Violet'], ['Comp', 'Math', 'Sci']))
    b = list(itertools.product(['Exams', 'Labs'], ['I', 'II']))
    c = pd.MultiIndex.from_tuples(a, names=['Student', 'Course'])
    d = pd.MultiIndex.from_tuples(b)
    e = [[70+x+y+(x+y)%3 for x in range(4)] for y in range(9)]
    f = pd.DataFrame(e, c, d)
    g = slice(None)
    h = f.loc['Violet']
    # 取第一级索引中的Math索引行
    i = f.loc[(g, 'Math'), g]
    j = f.loc[(slice('Ada', 'Quinn'), 'Math'), g]
    k = f.loc[(g, 'Math'), ('Exams')]
    l = f.loc[(g, 'Math'), (g, 'II')]
    m = f.sort_values(by=('Labs', 'II'), ascending=False)
    print(f)
    print(m)

def missData2():
    a = pd.DataFrame(np.random.randn(6, 1), index=pd.date_range('2013-08-01', periods=6, freq='B'), columns=('A',))
    a.loc[a.index[3], 'A'] = np.nan
    b = a.reindex(a.index[::-1]).ffill()
    print(b)

def group3():
    a = pd.DataFrame({
        'animal': 'cat dog cat fish dog cat cat'.split(),
        'size': list('SSMMMLL'),
        'weight': [8, 10, 11, 1, 20, 12, 12],
        'adult': [False] * 5 + [True] * 2  
    })
    # 按animao分组并根据weight列的最大索引值求出size列的最大值
    b = a.groupby('animal').apply(lambda subf: subf['size'][subf['weight'].idxmax()])
    c = a.groupby(['animal'])
    # 获取某一组
    d = c.get_group('cat')
    def GrowUp(x):
        avg_weight = sum(x[x['size'] == 'S'].weight * 1.5)
        avg_weight += sum(x[x['size'] == 'M'].weight * 1.25)
        avg_weight += sum(x[x['size'] == 'L'].weight)
        avg_weight /= len(x)
        return pd.Series(['L', avg_weight, True], index=['size', 'weight', 'adult'])
    e = c.apply(GrowUp)
    f = pd.Series([i / 100.0 for i in range(1, 11)])
    def CumRet(x, y):
        return x * (1 + y)
    def Red(x):
        return functools.reduce(CumRet, x, 1.0)
    g = f.expanding().apply(Red, raw=True)
    h = pd.DataFrame({'A': [1, 1, 2, 2], 'B': [1, -1, 1, 2]})
    i = h.groupby('A')
    def replace(g):
        mask = g < 0
        print('......')
        g.loc[mask] = g[~mask].mean()
        return g
    # transform会把结果扩散给每一行，使之相同的组中具有多个相同的
    # 的结果行
    j = i.transform(replace)
    print(j)

def group4():
    a = pd.DataFrame({
        'line_race': [10, 10, 8, 10, 10, 8],
        'beyer': [99, 102, 103, 103, 88, 100]
    }, index=[
        'Last Gunfighter', 'Last Gunfighter', 'Last Gunfighter',
        'Paynter', 'Paynter', 'Paynter'
    ])
    # 基于一级索引分组进行beyer列的往下移动一位操作
    a['beyer_shifted'] = a.groupby(level=0)['beyer'].shift(1)
    b = pd.DataFrame({
        'host': ['other', 'other', 'that', 'this', 'this'],
        'service': ['mail', 'web', 'mail', 'mail', 'web'],
        'no': [1, 2, 1, 2, 1]  
    }).set_index(['host', 'service'])
    # 基于一级索引分组并求每组的行最大序号值
    c = b.groupby(level=0).agg('idxmax')
    # 返回聚合中no列的值
    d = b.loc[c['no']].reset_index()
    e = pd.DataFrame([0, 1, 0, 1, 1, 1, 0, 1, 1], columns=['A'])
    # cumsum会把True当作0，False当作1后进行累加，之后按序列进行分组
    # groups为获取每组的值
    f = e.A.groupby((e.A != e.A.shift()).cumsum()).groups
    # 针对每组进行累加操作
    g = e.A.groupby((e.A != e.A.shift()).cumsum()).cumsum()
    print(g)

def splitting():
    a = pd.DataFrame(data={
        'Case': ['A', 'A', 'A', 'B', 'A', 'A', 'B', 'A', 'A'],
        'Data': np.random.randn(9) 
    })
    # 经过累加，移动窗口求出中值后按中值分组后进行分组的解包获取
    b = list(zip(*a.groupby((1*(a['Case']=='B')).cumsum().rolling(window=3, min_periods=1).median())))[-1]
    print(b)

def pivot():
    a = pd.DataFrame(data={
        'Province': ['ON', 'QC', 'BC', 'AL', 'AL', 'MN', 'ON'],
        'City': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Winnipeg', 'Windsor'],
        'Sales': [13, 6, 16, 8, 4, 3, 1] 
    })
    # 索引为Province列，列为City，值为Sales的透视表，margins=True显示对每行每列进行汇总
    b = pd.pivot_table(a, values=['Sales'], index=['Province'], columns=['City'], aggfunc=np.sum, margins=True)
    # 对City的非NaN数值进行堆叠
    c = b.stack('City')
    d = [48, 99, 75, 80, 42, 80, 72, 68, 36, 78]
    e = pd.DataFrame({
        'ID': ['x%d' % r for r in range(10)],
        'Gender': ['F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'M'],
        'ExamYear': ['2007', '2007', '2007', '2008', '2008', '2008', '2008', '2009', '2009', '2009'],
        'Class': ['algebra', 'status', 'bio', 'algebra', 'algebra', 'status', 'status', 'algebra', 'bio', 'bio'],
        'Participated': ['yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes'],
        'Passed': ['yes' if x > 50 else 'no' for x in d],
        'Employed': [True, True, True, False, False, False, False, True, True, True],
        'Grade': d
    })
    # 以ExamYear进行分组并进行自定义的几组计算
    f = e.groupby('ExamYear').agg({
        'Participated': lambda x: x.value_counts()['yes'],
        'Passed': lambda x: sum(x == 'yes'),
        'Employed': lambda x: sum(x),
        'Grade': lambda x: sum(x) / len(x)
    })

    g = pd.DataFrame({'values': np.random.randn(36)}, 
                index=pd.date_range('2011-01-01', freq='M', periods=36))
    h = pd.pivot_table(g, index=g.index.month, columns=g.index.year, 
                values='values')
    
    print(g)
    print(h)

def apply2():
    a = pd.DataFrame(data={
        'A': [[2, 4, 8, 16], [100, 200], [10, 20, 30]],
        'B': [['a', 'b', 'c'], ['jj', 'kk'], ['ccc']]
    }, index=['I', 'II', 'III'])

    def SeriesFromSubList(aList):
        return pd.Series(aList)
    # 基于字典的进行叠加，字典key为一级索引
    b = pd.concat(dict([(ind, row.apply(SeriesFromSubList)) for ind, row in a.iterrows()]))
    c = pd.DataFrame(data=np.random.randn(2000, 2)/10000,
                index=pd.date_range('2001-01-01', periods=2000),
                columns=['A', 'B'])
    def gm(aDF, Const):
        v = ((((aDF.A+aDF.B)+1).cumprod())-1)*Const
        return (aDF.index[0], v.iloc[-1])
    d = pd.Series(dict([gm(c.iloc[i:min(i+51, len(c)-1)], 5) for i in range(len(c)-50)]))
    e = pd.date_range(start='2014-01-01', periods=100)
    f = pd.DataFrame({
        'Open': np.random.randn(len(e)),
        'Close': np.random.randn(len(e)),
        'Volume': np.random.randint(100, 2000, len(e))
    }, index=e)

    def vwap(bars):
        return ((bars.Close*bars.Volume).sum()/bars.Volume.sum())
    
    window=5
    g = pd.concat([(pd.Series(vwap(f.iloc[i:i+window]), index=[f.index[i+window]])) for i in range(len(f)-window)])

    print(g)

def timeSeries2():
    a = pd.date_range('2000-01-01', periods=5)
    # 转换成月周期后，每一个时间会变成当前月份的第一天
    b = a.to_period(freq='M').to_timestamp()
    print(a)
    print(b)

def merge2():
    a = pd.date_range('2000-01-01', periods=6)
    b = pd.DataFrame(np.random.randn(6, 3), index=a, columns=['A', 'B', 'C'])
    c = b.copy()
    # 在一个dataframe后面追加一个dataframe，并且忽略索引
    d = b.append(c, ignore_index=True)
    e = pd.DataFrame(data={
        'Area': ['A'] * 5 + ['C'] * 2,
        'Bins': [110] * 2 + [160] * 3 + [40] *2,
        'Test_0': [0, 1, 0, 1, 2, 0, 1],
        'Data': np.random.randn(7)
    })
    e['Test_1'] = e['Test_0'] - 1
    # 类sql的on合并，相同字段的左侧以_L结尾，右侧以_R结尾
    f = pd.merge(e, e, left_on=['Bins', 'Area', 'Test_0'], right_on=['Bins', 'Area', 'Test_1'], suffixes=['_L', '_R'])
    print(e)
    print(f)

def dataio():
    import glob
    a = ['f_1.csv', 'f_2.csv', 'f_3.csv']
    # 读取多个csv文件并且合并成一个dataframe
    #b = pd.concat([pd.read_csv(f) for f in a], ignore_index=True)
    # 可以使用glob按正则匹配文件获取文件列表
    c = glob.glob('f_*.csv')
    #d = pd.concat([pd.read_csv(f) for f in c], ignore_index=True)
    e = """;;;;
   .....:  ;;;;
   .....:  ;;;;
   .....:  ;;;;
   .....:  ;;;;
   .....:  ;;;;
   .....: ;;;;
   .....:  ;;;;
   .....:  ;;;;
   .....: ;;;;
   .....: date;Param1;Param2;Param4;Param5
   .....:     ;m²;°C;m²;m
   .....: ;;;;
   .....: 01.01.1990 00:00;1;1;2;3
   .....: 01.01.1990 01:00;5;3;4;5
   .....: 01.01.1990 02:00;9;5;6;7
   .....: 01.01.1990 03:00;13;7;8;9
   .....: 01.01.1990 04:00;17;9;10;11
   .....: 01.01.1990 05:00;21;11;12;13
   .....: """
   # 从开头10行之后开始读取，指定分隔符为;
   # 不处理11与12行，以第一列为索引，解析日期，
    f = pd.read_csv(StringIO(e), sep=';', skiprows=[11, 12],
                index_col=0, parse_dates=True, header=10)
    
    # 获取10行数据
    g = pd.read_csv(StringIO(e), sep=';', header=10, nrows=10).columns
    # 使用自定义列名
    h = pd.read_csv(StringIO(e), sep=';', header=12, parse_dates=True, names=g)
    i = pd.HDFStore(r'D:\tmpfile\test.h5')
    # 类字典映射存储
    i.put('myh5', h)
    # 自定义属性
    i.get_storer('myh5').attrs.my_attr = dict(A=10)
    j = i.get_storer('myh5').attrs.my_attr
    print(j)

def timedeltas():
    a = pd.Series(pd.date_range('2012-1-1', periods=3, freq='D'))
    # 时间相减
    b = a - a.max()
    # 相当于使用max的值分别减去序列每一个元素的值后得到新的序列
    c = a.max() - a
    d = a - datetime.datetime(2011, 1, 1, 3, 5)
    e = a + datetime.timedelta(minutes=5)
    f = datetime.datetime(2011, 1, 1, 3, 5) - a
    g = datetime.timedelta(minutes=5) + a
    h = pd.Series([datetime.timedelta(days=i) for i in range(3)])
    # 使用timedelta对象作为值
    i = pd.DataFrame(dict(A=a, B=h))
    i['New Dates'] = i['A'] + i['B']
    # 日期相减得到timedelta对象
    i['Delta'] = i['A'] - i['New Dates'] 
    print(i)

def axisAlias():
    # 给轴定义别名，myaixs为别名，columns轴一定要在dataframe中存在
    pd.DataFrame._AXIS_ALIASES['myaxis'] = 'columns'
    a = pd.DataFrame(np.random.randn(3, 2), columns=['c1', 'c2'], index=['i1', 'i2', 'i3'])
    b = a.sum(axis='myaxis')
    # 去掉别名
    pd.DataFrame._AXIS_ALIASES.pop('myaxis', None)
    c = a.sum(axis='columns')
    print(a)
    print(c)

def createExampleData():
    a = pd.DataFrame.from_records([[1, 2], [3, 4]], columns=['A', 'B'])
    print(a)

if __name__ == '__main__':
    starttime = time.time()

    pivotTb()

    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, \
    tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f} seconds'.format(endtime-starttime))