import numpy as np
import numpy.matlib as nm

def createArray():
    # 创建一个空数组, 存储方式为C风格的行存储
    # F则为FORTRAN的列存储
    a = np.empty([3, 2], dtype=int, order='C')
    # 创建指定大小数组，类型默认为float
    b = np.zeros(5)
    # 创建两行两列空数组，并且对每一个元素映射到自定义类型
    c = np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'f2')])
    # 创建指定形状的数组，以1进行填充
    d = np.ones([2, 2])
    print(d)

def createWithCur():
    a = [1, 2, 3]
    # 从现有数组创建数组
    b = np.asarray(a, dtype=float)
    c = [(1, 2, 3), (4, 5)]
    d = np.asarray(c)
    # 需转换成bytestring形式，读取数据数量-1(全部)，偏移量0
    e = b'hello'
    f = np.frombuffer(e, dtype='S1', count=-1, offset=0)
    g = range(5)
    # 把可迭代对象转换成数组
    h = np.fromiter(g, dtype=float)
    print(h)

def createWithRange():
    # 从数值范围创建数组start stop step
    a = np.arange(0, 10, 2, dtype=float)
    # 生成指定区间指定数量的等差序列，retstep=True返回等差值
    # 如start与stop相等，则生成指定数量的相同的值
    b = np.linspace(0, 10, 15, endpoint=True, retstep=False, dtype=float)
    # 生成base ** start 到base ** stop之间的等比数列
    c = np.logspace(1.0, 2.0, num=10, base=10)
    print(c)

def splitAindIdx():
    a = np.arange(10)
    b = slice(2, 7, 2)
    # 根据切片对象进行切片
    c = a[b]
    # 加上:则表示要切片的返回，如果没有，则表示索引
    # 与list用法一致
    d = a[2:7:2]
    e = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 7]])
    # ...使选择元组的长度与数组的维度相同
    # 省略号位于行处理位置则说明不返回行
    # 返回第三列元素
    f = e[...,2]
    # 返回第二行元素
    g = e[1,...]
    # 返回从第二列之后的所有列元素
    h = e[...,1:]
    print(f)

def highLevelIdx():
    a = np.array([[1, 2], [3, 4], [5, 6]])
    b = a[[0, 1, 2], [0, 1, 0]]
    c = np.arange(35).reshape(5, 7)
    # 先找两行，再找三列
    d = c[1:5:2,::3]
    # 先按行索引，再在结果上进行索引
    # 抽取每一行特定值组成新数据
    # 没有切片则按数组元素为索引值
    # []也可以使用np.array替换
    e = c[[0, 2, 4], [0, 1, 2]]
    f = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
    g = np.array([[0,0], [3,3]])
    h = np.array([[0,2], [0,2]])
    i = f[g, h]
    # 先提取两组行，在根据列分别对两组行进行提取
    j = c[[[0, 2, 4], [0, 1, 2]], [0, 1, 2]]
    # 如果列索引组只有一组，则对行组的处理都使用第一组，
    # 有两组则分别对应行组进行处理
    k = c[[[0, 2, 4], [0, 1, 2]], [[0, 1, 2], [0, 2, 2]]]
    # 切片与组索引可以组合使用
    l = c[1:3, [0, 1, 2]]
    # 布尔索引，检索出大于5的元素，返回一维数组
    m = f[f > 5]
    n = np.array([np.nan, 1, 2, np.nan, 3, 4, 5])
    # 过滤掉非nan元素
    o = n[~np.isnan(n)]
    # 与普通数组索引不同，行索引有多少个元素
    # 则返回多少组
    p = c[np.ix_([0, 2, 4], [0, 1, 2])]
    print(p)

def broadcast():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    # 形状相同，则正常相加
    c = a * b
    d = np.array([[1, 2, 3], [4, 5, 6]])
    e = np.array([1, 2, 3])
    # 由于相加的数组维度不同，维度少的数组会
    # 扩展至和维度多的数组的相同的维度后再相加
    # 这就是广播
    f = d + e
    # 被扩展数组维度为1或者与较长维度数组维度相同
    # 则可以进行数学运算，否则报错
    g = np.array([1])
    h = d + g
    print(c)

def iter():
    a = np.arange(6).reshape(2, 3)
    def iterArray():
        # 使用nditer按行迭代数组
        for i in np.nditer(a):
            print(i, end=", ")
        print('\n')
        # T倒置数组，order按C风格行排序
        for i in np.nditer(a.T.copy(order='C')):
            print(i, end=", ")
        print('\n')
        # 按fortran风格列排序
        for i in np.nditer(a.copy(order='F')):
            print(i, end=", ")
        print('\n')
        # 改变为按列排序方式
        for i in np.nditer(a, order='F'):
            print(i, end=", ")
        print('\n')
        # 迭代到的元素默认是只读的，可以改变
        # 模式为读写，这样就可以修改数组中的元素
        for i in np.nditer(a, op_flags=['readwrite']):
            i[...]=2*i
        # 每一列迭代为一个数组
        for i in np.nditer(a, flags=['external_loop'], order='F'):
            print(i, end=", ")
        print('\n')
        b = np.array([1, 2, 3])
        # 两个数组可以广播的话，可以放在一起迭代
        for i,j in np.nditer([a, b]):
            print('{}:{}'.format(i,j), end=", ")
        print('\n')
    iterArray()

def dupView():
    a = np.array([[10, 10], [2, 3], [4, 5]])
    # 创建数组的拷贝
    b = a.copy()
    # copy方式的拷贝的修改不会影响到原来的数组
    b[0, 0] = 100
    print(b)

def matrix():
    # 创建空矩阵
    a = nm.empty((2, 2))
    # 创建0填充的矩阵
    b = nm.zeros((2, 2))
    # 创建1填充的矩阵
    c = nm.ones((2, 2))
    # 创建对角线元素为1，行数为3，列数为4
    # 开始的1索引从1开始
    d = nm.eye(n=3, M=4, k=1, dtype=float)
    # 创建五行五列，对角线元素为1的矩阵
    e = nm.identity(5, dtype=float)
    # 创建给定形状的，元素为随机的矩阵
    f = nm.rand((3, 3))
    # 创建len(str.split(';'))行，
    # len(str.split(';')[0].split(','))
    # 列的矩阵
    g = np.matrix('1,2;3,4')
    # 矩阵与数组可以相互切换
    h = np.asarray(g)
    i = np.asmatrix(h)
    print(i)

if __name__ == '__main__':
    matrix()
