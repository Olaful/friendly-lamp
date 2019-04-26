import numpy as np
import numpy.matlib as nm

def array():
    """
    数组
    """
    a = np.array([1, 2, 3])
    b = np.array([[1, 2], [3, 4]])
    # 指定最小维度，2生成[[]]，3则生成[[[]]]
    c = np.array([1, 2, 3], ndmin=2)
    # 指定数据类型
    d = np.array([1, 2, 3], dtype=float)
    e = np.array([1, 2, 3], dtype=np.uint8)
    print(e)

def dtype():
    """
    数组类型
    """
    a = np.dtype(np.int32)
    # i4其实是int32，如i1表示int8
    b = np.dtype('i4')
    # >字节码存放顺序为大端法，<则为小端法
    c = np.dtype('>i4')
    # hello字段对应np.int8类型
    d = np.dtype([('hello', np.int8)])
    e = d['hello']
    # 应用自定义类型
    f = np.array([(1,), (2,), (3,)], dtype=c)
    # name字段为16位字符串，grades为2个float64的子数组
    g = np.dtype([('name', np.str_, 16), ('grades', np.float64, (2,))])
    # 'Jack'会使用name指定的类型，(9.0, 8.0)则使用grades
    h = np.array([('Jack', (9.0, 8.0)), ('Mike', (8.0, 7.0))], dtype=g)
    i = h[1]['name']
    j = h[1]['grades']
    k = np.dtype('2a3, (2,2)a2')
    # 会分别对1与2进行2个3字节字符，2*2维2个字节字符的矩阵映射
    l = np.array([1,2], dtype=k)
    print(l)

def property():
    """
    数组属性
    """
    a = np.array([(1,1), (2,2), (3,4)])
    # 数组维度
    b = a.ndim
    # 行数*列数
    c = a.shape
    # ndarray对象内存信息
    d = a.flags
    e = np.arange(24)
    # 重新分为三维数组，第二轴有2个，每第二个轴中有四个第三轴
    # [[[], [], [], []], [[], [], [], []]]
    # f与e会共用一块内存
    f = e.reshape(2, 4, 3)
    g = f.shape
    # 通过shape属性改变维度
    e.shape=(6,4)
    h = e.itemsize
    i = e.dtype
    # 数组元素总个数
    j = e.size
    # 列位置-1表示python会根据行数来判断应该写多少列
    i = e.reshape(3, -1)
    print(e)
    print(i)

def createArray():
    """
    创建数组
    """
    # 创建一个空数组, 存储方式为C风格的行存储
    # F则为FORTRAN的列存储
    a = np.empty([3, 2], dtype=int, order='C')
    # 创建指定大小数组，类型默认为float
    b = np.zeros(5)
    # 创建两行两列空数组，并且对每一个元素映射到自定义类型
    c = np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'f2')])
    # 创建指定形状的数组，以1进行填充
    d = np.ones([2, 2])
    print(c)

def createWithCur():
    """
    从现有数组创建数组
    """
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
    print(f)

def createWithRange():
    """
    从指定范围创建数组
    """
    # 从数值范围创建数组start stop step
    a = np.arange(0, 10, 2, dtype=float)
    # 生成指定区间指定数量的等差序列，retstep=True返回等差值
    # 如start与stop相等，则生成指定数量的相同的值
    b = np.linspace(0, 10, 15, endpoint=True, retstep=False, dtype=float)
    # 生成base ** start 到base ** stop之间的等比数列
    c = np.logspace(1.0, 2.0, num=10, base=10)
    print(c)

def splitAindIdx():
    """
    切片
    """
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
    """
    高级索引
    """
    a = np.array([[1, 2], [3, 4], [5, 6]])
    b = a[[0, 1, 2], [0, 1, 0]]
    c = np.arange(35).reshape(5, 7)
    # 从1-5范围内隔两行查找出所有的行，再在每一行中
    # 从0到len(col)范围内隔三列找出所有的列
    d = c[1:5:2,::3]
    # 先按行索引，再在结果上进行索引
    # 抽取每一行特定值组成新数据
    # 没有切片则按数组元素为索引值
    # []也可以使用np.array替换
    e = c[[0, 2, 4], [0, 1, 2]]
    f = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
    g = np.array([[0,0], [3,3]])
    h = np.array([[0,2], [0,2]])
    # 先提取第0行，再根据[0, 2]提取一组，再提取第3行，再
    # 根据[0, 2]提取一组
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
    # 则返回多少组，先提取0 2 4行，再在每一行提取
    # 0 1 2列
    p = c[np.ix_([0, 2, 4], [0, 1, 2])]
    # 三维数组
    q = np.reshape(np.arange(24), (2, 3, 4))
    # 先取出所有的第二维，再取出两个第三维，再在第三维中取出
    # 第一个列
    r = q[:,:2,0]
    print(c)
    print(b)

def broadcast():
    """
    广播
    """
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
    # 两者进行数学运算时，i广播至[[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    # j广播至[[4, 5, 6], [4, 5, 6], [4, 5, 6]]
    i = np.array([[1], [2], [3]])
    j = np.array([4, 5, 6])
    # 广播的结果
    k = np.broadcast(i, j)
    r, c = k.iters
    l = next(r)
    m = next(c)
    n = k.shape
    o = np.empty(k.shape)
    o.flat = [u+v for (u,v) in k]
    # 将数组广播至新形状并返回只读视图
    p = np.broadcast_to(j, (3, 3))
    print(p)

def iterArray():
    """
    迭代
    """
    a = np.arange(6).reshape(2, 3)
    def iter():
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
    iter()

def oper():
    """
    展开，维度转换
    """
    a = np.arange(8).reshape(2, 4)
    # 按行迭代数组
    for row in a:
        print(row)
    # 按元素迭代数组
    for e in a.flat:
        print(e)
    # 返回数组的拷贝，并按order顺序展开元素
    b = a.flatten(order='F')
    print(b)
    c = a.ravel(order='C')
    # 对换数组维度
    d = np.transpose(a)

    print(d)

def oper2():
    """
    按维度改变数组
    """
    a = np.array(([1, 2], [3, 4]))
    # 再0位置插入轴
    b = np.expand_dims(a, axis=0)
    # 再1位置插入轴
    c = np.expand_dims(a, axis=1)
    d = np.arange(9).reshape(1, 3, 3)
    # 减掉维度，默认0维
    e = np.squeeze(d)
    print(e)

def oper3():
    """
    连接数组
    """
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    # 沿0轴连接数组
    c = np.concatenate((a,b), axis=0)
    # 沿1轴连接数组
    d = np.concatenate((a,b), axis=1)
    # 沿0轴叠加数组
    e = np.stack((a, b), 0)
    # 沿1轴叠加数组
    f = np.stack((a, b), 1)
    # 水平叠加数组
    g = np.hstack((a, b))
    # 垂直叠加数组
    h = np.vstack((a, b))
    print(h)

def oper4():
    """
    拆分数组
    """
    a = np.arange(9)
    # 拆分成三个数组
    b = np.split(a, 3)
    # 按[0:3] [3:5] [5:]来切分
    c = np.split(a, [3, 5])
    d = np.array([[1, 2, 3], [4, 5, 6]])
    # 按水平来拆分，分割的数量要与数组的列数量相同
    e = np.hsplit(d, 3)
    # 按垂直来拆分
    f = np.vsplit(d, 2)
    print(e)

def oper5():
    """
    增删数组
    """
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.resize(a, (3, 2))
    # 修改后的数组大于原来的数组，则会重复包含原
    # 数组第一行的数据
    c = np.resize(a, (3, 3))
    # 横向追加数组元素，始终返回一维数组
    d = np.append(a, [7, 8])
    # 指定轴向时，待追加的数组维度要与原数组相同
    e = np.append(a, [[7, 8, 9]], axis=0)
    # 指定轴向时，待追加的数组维度要与原数组相同
    f = np.append(a, [[1, 1, 1], [2, 2, 2]], axis=1)
    g = np.array([[1, 2], [3, 4], [5, 6]])
    # axis未提供，则原数组被展开后再进行插入
    h = np.insert(g, 3, [11, 12])
    # 指定axis后待插入数组会被广播后再插入
    i = np.insert(g, 1, [11], axis=0)
    j = np.insert(g, 1, [11], axis=1)
    # 展开后再删除
    k = np.delete(g, 3)
    # 删除第二列元素
    l = np.delete(g, 1, axis=1)
    m = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    # 按数组删除
    n = np.delete(m, np.s_[::2])
    o = np.array([1, 1, 3, 4, 5, 6, 6, 7])
    # 去除重复元素
    p = np.unique(o)
    # 返回新数组与新数组中每个元素在原数组中的下标列表
    q = np.unique(o, return_index=True)
    # 返回新数组与旧元素在原数组中的下标列表
    r = np.unique(o, return_inverse=True)
    # 返回新数组与新数组元素在原数组中的重复数量下标列表
    s = np.unique(o, return_counts=True)
    print(s)

def oper6():
    """
    轴变换
    """
    a = np.arange(8).reshape(2, 2, 2)
    # 把轴2滚动到轴0， 如001位置的数字1滚动后
    # 位置变成100，即到达了数字2的位置
    b = np.rollaxis(a, 2)
    # 轴2滚动到轴1
    c = np.rollaxis(a, 2, 1)
    # 交换轴2与轴1
    d = np.swapaxes(a, 2, 1)
    print(d)

def bitCalc():
    """
    数值位运算
    """
    # 位与运算
    a = np.bitwise_and(13, 17)
    # 位或运算
    b = np.bitwise_or(13, 17)
    # 按位反转
    c = np.invert(1)
    # 转换成二进制
    d = np.binary_repr(13, width=8)
    # 按位左移两位
    e = np.left_shift(10, 2)
    # 按位右移两位
    f = np.right_shift(8, 2)
    print(d)

def strfunc():
    """
    字符串函数
    """
    # 连接两个字符串
    a = np.char.add(['hello'], ['world'])
    # 分别连接对应位置的字符串
    b = np.char.add(['hello', 'hi'], ['world', 'jack'])
    # 重复3次连接
    c = np.char.multiply('hello', 3)
    # 区中，两边用指定字符填充至指定长度
    d = np.char.center('hello', 20, fillchar='-')
    e = np.char.capitalize('hello')
    f = np.char.title('hello world')
    g = np.char.lower(['HEllO', 'WOrLD'])
    h = np.char.upper(['HEllO', 'WOrLD'])
    i = np.char.split('he.llo wor.ld', sep='.')
    # 以换行符进行分割
    j = np.char.splitlines('hello\nworld')
    k = np.char.strip('--hello world--', '-')
    l = np.char.strip(['--hello--', '--world--'], '-')
    m = np.char.join(['-', '*'], ['hello', 'world'])
    n = np.char.replace('hello world', 'll', 'cc')
    # cp500编码
    o = np.char.encode('hello world', 'cp500')
    p = np.char.decode(o, 'cp500')
    print(m)

def mathFunc():
    """
    数学函数
    """
    a = np.array([0, 30, 45, 60, 90])
    # 转换为弧度后再调用正弦函数
    b = np.sin(a*np.pi/180)
    c = np.cos(a*np.pi/180)
    d = np.tan(a*np.pi/180)
    # 反正弦返回弧度
    e = np.arcsin(b)
    # 弧度转换成角度
    f = np.degrees(e)
    g = np.array([1.0, 5.55, 123, 0.567, 25.532])
    h = np.around(g)
    i = np.around(g, decimals=1)
    # 往小数点左侧一位进行四舍五入
    j = np.around(g, decimals=-1)
    # 下入
    k = np.floor(g)
    # 上入
    l = np.ceil(g)
    print(i)

def ariFunc():
    """
    数学运算
    """
    a = np.arange(9, dtype=np.float_).reshape(3, 3)
    b = np.array([10, 10, 10])
    c = np.add(a, b)
    d = np.subtract(a, b)
    e = np.multiply(a, b)
    f = np.divide(a, b)
    g = np.array([0.25, 1.33, 1, 100])
    # 倒数
    h = np.reciprocal(g)
    # 幂函数
    i = np.power(b, 2)
    j = np.power(b, [1, 2, 3])
    # 取余，与remainder一致
    k = np.mod(b, [1, 2, 3])
    print(e)

def stasFunc():
    """
    统计
    """
    a = np.array([[3, 7, 5], [8, 7, 3], [2, 4, 9]])
    # 统计0轴最小值, 与argmin用法一致
    b = np.amin(a, 1)
    c = np.amin(a, 0)
    d = np.amax(a, 1)
    e = np.amax(a, 0)
    # 统计最大值与最小值的差
    f = np.ptp(a)
    # 沿1轴统计最大值与最小值的差
    g = np.ptp(a, axis=1)
    h = np.array([[10, 7, 4], [3, 2, 1]])
    # 在排序后的数列中，求处于70%这个点的数，
    # 那么这些数中(离散后)就有70%的数会比这个数低，
    # 30%的数比这个数高
    i = np.percentile(h, 70)
    j = np.percentile(h, 70, axis=0)
    # 中位数
    k = np.median(h)
    l = np.median(h, axis=0)
    # 算术平均值
    m = np.mean(h)
    n = np.array([4, 3, 2, 1])
    o = np.array([1, 2, 3, 4])
    # 求加权平均数，不指定权重则与mean一样
    p = np.average(n)
    # =(4*1+3*2+2*3+1*4)/(4+3+2+1)
    q = np.average(n, weights=o)
    r = np.average(h, axis=1, weights=[1, 2, 3])
    # 标准差
    s = np.std(n)
    # 方差
    t = np.var(n)
    print(k)

def sort():
    """
    排序
    """
    a = np.array([[3, 7], [9 ,1]])
    # 默认使用快排
    b = np.sort(a)
    #　按列排
    c = np.sort(a, axis=0)
    dt = np.dtype([('name', 'S10'), ('age', int)])
    d = np.array([('raju', 21), ('anil', 25), ('ravi', 17), ('amar', 27)], dtype=dt)
    e = np.sort(d, order='name')
    f = np.array([3, 1, 2])
    # 返回按数组元素大小排序的索引值
    # 先标索引，在按元素大小排序索引
    g = np.argsort(f)
    # 以索引对数组进行排序
    h = f[g]
    i = ('raju', 'anil', 'ravi', 'amar')
    j = ('f.y', 's.y', 's.y', 'f.y')
    # 先按j排,j相同则按i排
    k = np.lexsort((j, i))
    # 先按实部排后按虚部排
    l = np.sort_complex([1 + 2j, 2 - 1j, 3 -2j, 3 - 3j, 3 + 5j])
    m = np.array([3, 4, 2, 1, -1])
    # 按3分区，比3大的放在后面，小的放在前面
    n = np.partition(m, 3)
    # 比1小放前面，比3大放后面，1< >3的放中间
    o = np.partition(m , (1, 3))
    print(o)

def sort2():
    """
    排序
    """
    a = np.array([46, 57, 23, 39, 1, 10, 0, 120])
    # 先按第二小的元素分区，在根据下标取值
    # 这样就能取到第二小值了
    b = a[np.argpartition(a, 2)[2]]
    # 取第二大值
    c = a[np.argpartition(a, -2)[-2]]
    # 按两个元素先进行分区，再按下标取值
    d = a[np.argpartition(a, [2, 4])[2]]
    e = np.array([[30,40,0],[0,20,10],[50,0,60]])
    # 返回非零元素索引值，第一组索引值按列顺序组合，
    # 第二组索引值按行顺序组合
    f = np.nonzero(e)
    g = np.arange(9.).reshape(3,  3)
    # 根据条件返回索引，第一组索引为坐标行数据
    # 第二组为坐标列数据 
    h = np.where(g > 3)
    i = np.mod(g, 2) == 0
    # 根据自定义条件抽取符合条件的元素
    j = np.extract(i, g)
    print(f)

def swapbyte():
    """
    大小端切换
    """
    a = np.array([1, 256, 8755], dtype=np.int16)
    b = list(map(bin, a))
    # 调换元素的字节在内存中的存储顺序
    c = a.byteswap(True)
    d = list(map(bin, a))
    print(b)
    print(d)

def dupView():
    """
    副本与视图
    """
    a = np.arange(6)
    # b 引用了a
    b = a
    # b的改变影响到了a
    b.shape = 3, 2
    c = np.arange(6).reshape(3, 2)
    # 使用view创建数组的视图，视图与原数组id不同
    d = c.view()
    # view创建的视图的更改不会影响到原数组
    d.shape = 2, 3
    e = np.arange(9)
    f = e[3:]
    g = e[3:]
    # 切片创建的视图的改变会影响到原数组
    # 但是视图与原数组的id却不同
    f[0] = 4
    g[1] = 5
    h = np.array([[10, 10], [2, 3], [4, 5]])
    # 创建数组的拷贝
    i = h.copy()
    # copy方式的拷贝的修改不会影响到原来的数组
    i[0, 0] = 100
    print(e)

def matrix():
    """
    矩阵
    """
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
    print(h)

def IO():
    """
    IO操作
    """
    a = np.array([1, 2, 3, 4, 5])
    # 保存数组到npy文件中，如果没有.npy扩展名
    # 会自动加上,保存的数据为未压缩的原始二进制
    # 格式
    np.save(r'D:\tmpfile\npyfile', a)
    # 读取npy文件
    b = np.load(r'D:\tmpfile\npyfile.npy')
    c = np.arange(0, 1.0, 0.1)
    d = np.sin(c)
    # 将多个数组保存到npz文件中
    np.savez(r'D:\tmpfile\npzfile.npz', a, c, sin_array=c)
    e = np.load(r'D:\tmpfile\npzfile.npz')
    f = e.files
    # a 对应arr_0， c对应arr_1，c对应sin_array
    g = e['arr_0']
    h = e['arr_1']
    i = e['sin_array']
    # 以简单的文本格式保存数组
    np.savetxt(r'D:\tmpfile\npzfile.txt', a)
    j = np.loadtxt(r'D:\tmpfile\npzfile.txt')
    k = np.arange(0, 10, 0.5).reshape(4, -1)
    # 格式化，指定分隔符后保存
    np.savetxt(r'D:\tmpfile\npzfilefmt.txt', a, fmt='%d', delimiter=',')
    l = np.loadtxt(r'D:\tmpfile\npzfilefmt.txt', delimiter=',')
    print(l)

def linearAlgebra():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[11, 12], [13, 14]])
    # 对于二维数组，计算矩阵乘积
    # [[1*11+2*13, 1*12+2*14], [3*11+4*12+3*12+4*14]]
    c = np.dot(a, b)
    # 向量点积 1*11+2*12+3*13+4*14
    d = np.vdot(a, b)
    # 对于一维数组，返回向量点积
    e = np.inner(np.array([1, 2, 3]), np.array([0, 1, 0]))
    # 多维数组，最后一维上的乘积
    # [[1*11+2*12 1*13+2*14] [3*11+4*12 3*13 4*14]]
    f = np.inner(a, b)
    # 对于二维数组，计算方法与dot一致
    g = np.matmul(a, b)
    print(g)

def linearAlgebra2():
    a = np.array([[1, 2], [3, 4]])
    # 行列式 1*4 - 3*2
    b = np.linalg.det(a)
    c = np.array([[1, 1, 1], [0, 2, 5], [2, 5, -1]])
    d = np.linalg.inv(a)
    e = np.array([[6], [-4], [27]])
    # 求x+y+z=6; y+5z=-4; 2x+5y-z=27的解
    f = np.linalg.solve(c, e)
    print(d)

if __name__ == '__main__':
    strfunc()