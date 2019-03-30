import numpy as np

def array():
    a = np.array([1, 2, 3])
    b = np.array([[1, 2], [3, 4]])
    # 指定最小维度，2生成[[]]，3则生成[[[]]]
    c = np.array([1, 2, 3], ndmin=2)
    # 指定数据类型
    d = np.array([1, 2, 3], dtype=float)
    e = np.array([1, 2, 3], dtype=uint8)
    print(e)

def dtype():
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
    f = e.reshape(2, 4, 3)
    g = f.shape
    # 通过shape属性改变维度
    e.shape=(6,4)
    h = e.itemsize
    i = e.dtype
    # 数组元素总个数
    j = e.size
    print(j)

def main():
    property()  

if __name__ == '__main__':
    main()