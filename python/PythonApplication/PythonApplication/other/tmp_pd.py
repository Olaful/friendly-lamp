import pandas as pd
import numpy as np
import itertools
import functools

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

def missData():
    a = pd.DataFrame(np.random.randn(6, 1), index=pd.date_range('2013-08-01', periods=6, freq='B'), columns=('A',))
    a.loc[a.index[3], 'A'] = np.nan
    b = a.reindex(a.index[::-1]).ffill()
    print(b)

def group():
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

def group2():
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

def apply():
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

if __name__ == '__main__':
    apply()