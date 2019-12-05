import time
listNum = [6, 4, 8, 9, 2, 5, 7, 676, 33, 334, 22222]
'''
site-packages\pip\compat\__init__.py", line 75, in console_to_str
    return s.decode('utf_8')
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd1 in position 3: invalid continuation byte

'''
# -------------------------------------------------------------------------------------------------------------------------------------------------------
"""
print(time.time())
listNum.sort()
print(time.time())
print(listNum)

# 注意代码缩放的重要性，同级别的放在同一列，语法要求
# 以下以冒泡排序算法示例
nLen = len(listNum)
i = 0
j = 0
temp = 0
print(time.time())
while i < nLen:
    swap = False
    while j < nLen - i - 1:
        if listNum[j] > listNum[j+1]:
            temp = listNum[j+1]
            listNum[j+1] = listNum[j]
            listNum[j] = temp
            swap = True
        j = j + 1
    if !swap: break
    i = i + 1
print(time.time())
print(listNum)

def myFunc():
    print("hello, myFunc")

# 函数也可以添加属性
myFunc.name = 'myFunc'

# 函数参数类型注释，返回值类型注释
def hello(sno:int, name:str)->list:
    return [1,2,3]

def func(y=[]):
    y.append(1)
func()
# 由于没有传入实际参数，函数使用默认参数y
# 这时因为第一次调用已经使得默认参数y改变了，
# 所以第二次调用会使得y在第一次的基础上改变
# 而不像预期的两次结果都一样
func()
    

# 获取数字对应的ascii码
chr(98)

def func(x):
    return x*x

# 对列表中的每一个元素应用func并返回新的列表
l = map(func, [1,2,3])

def func2(x,y):
    return x+y
# 依次提取两个列表中元素并应用函数
l = map(func2, [1,2,3], [1,5,7])

# 返回(10 // 5, 10 % 5)
divmod(10, 5)

# 返回局部作用域的字典
vars()

x=[1,2,3,3]
# 返回列表中值为3的最小索引
x.index(3)

# 在列表第二个位置插入3
x.insert(1,3)

# 在列表第二个位置删除元素并返回该元素
x.pop(1)

# 原地反转列表
x.reverse()

x={'h':1}
# 返回x的副本，这样改变y就不会影响到x了
y=x.copy()

# 返回{'n':1, 'm':1}
dict.fromkeys(['n', 'm'], 1)

# 删除指定的key并返回该key值对应的value
x.pop('h')

# 返回x中(key,value)值组成的可迭代对象
x.items()

# 删除x中任意项并返回(key,value)值
x.popitem()

# 返回x中key值组成的可迭代对象
x.keys()

# 返回x中value值组成的可迭代对象
x.values()

# 使用另一个dict更新现有的项，有就覆盖，没有就新增
x.update({'s':1})

# __metaclass__=type表示以下定义的类都是新式类，如没有，则class class():为新式类，class class:为老式类
# class创建的类可以理解为也是一种对象，所以也可以在函数中建立
# type('myclass', (parenclass), {'name':setValua})可以创建父类为parenclass的类，并具有属性setValue()
# 所以type其实就是所有类的父类，此外，python中的整数，字符串，函数，类都是对象，所以如"hello".count('e')
# 的使用是正确的，这些对象都是由type创建的
# 也可以指定元类__metaclass__=mytype，mytype从type继承而来，可以在其中增加一些属性，这样通过mytype创建的类
# 也就拥有了这些属性，可以单独在某个class中定义__metaclass__属性，这样这个属性就只影响到这个类
__metaclass__=type
# myClass中代码被定义在类命名空间内
class myclass:
    # 构造函数
    def __init__(seft):
        seft.nMember = 0
    # 析构函数
    def __del__(): pass
    # 方法中有seft参数，而函数中没有，这就是方法与函数的区别，seft会绑定到实例上
    def setValue(seft):
        pass
    def getValue(seft):
        return seft.name
    # __双下划线开头的方法外部无法访问
    # 仅能被类对象访问(不包括子类对象)
    def  __privateFunc(seft):
        print("this is private func")
        type("type")
    def getSomeMsg(seft):
        seft. __privateFunc()
    # 单下划线开头的函数不会被import导入
    # 仅能被类对象及子类对象访问
    def  _noImportFunc():
        print("this func can't imported")

x = myclass()
x.name = 'hello'
print (x.name)
print (x.getValue())
print (myclass.getValue(x))
# 调用其特殊方法__str__()
print(x)

y = myFunc
y()
z = x.getValue
print(z())

# x._privateFunc()
x.getSomeMsg()
# 但通过以下这种隐秘的方式却是可以访问私有方法
x._myclass__privateFunc()

class LimitClass():
    # 规定类实例只能绑定哪些属性
    # 但不会限制子类实例的绑定，如果
    # 子类中也有__slots__，那么限制的
    # 返回包括子类中的slots与父类中的slots
    # 范围之合
    __slots__ = ('name', 'age')
l = LimitClass()
l.name = 'jack'
l.age = 23
# 绑定限制外的属性会报错
l.address = 'shenzhen'

def myfunc2(*args):
    return [1, 2, 3, 4]

# 可以先对函数的返回值进行操作后再赋值给变量
y = myfunc2()[0:2]
# 组装成元组形式的入参
# 补充：由于python中函数的参数是可变的
# 并且能接收不同类型的实参，所以函数重载没有
# 必要，需要函数重载的情况就是同一个函数接口，
# 参数类型，个数不一样，但却实现相同的功能
# 这点python函数的可变形参就可以做到
y = myfunc2(*(1,2,3))
# 组装成字典形式的入参
y = myfunc2(**{'a':1, 'b':2})

# 特性的改变只会体现在实例的成员上面
x.nMember = 1
x1 = myclass()
print(repr(x.nMember)+";"+repr(x1.nMember))

# 指定myClass为超类
class subClass(myclass):
    # 新式类构造函数中调用super方法，可以使用超类中的特性__init__
    def __init__(seft):
        super(myclass, seft).__init__()

    # 直接调用父类的构造函数初始化，支持老式类
    #def __init__():
    #    myclass.__init__()
    # 重写超类中的方法
    def setValue(seft):
        ""
x2 = subClass()
# 使用超类中的方法
print(x2.setValue())
# 查看是否为该子类的超类
print(issubclass(subClass, myclass))
# 查看所有基类
print(subClass.__bases__)
# 查看所属的直接类
print(subClass.__class__)
print(isinstance(x2, myclass))

class myClass1:
    def __init__(self):
        self.width = 0
        self.height = 0
    def talk():
        ""
    def setValue(self, size):
        # 这种赋值方式为元组赋值，与width, height单独赋值是不一样的
        self.width, self.height = size
    def getValue(self):
        return self.width, self.height

    # property如果没有参数，那么size将不可以读写，property是隐藏方法的一种方式
    size = property(getValue, setValue)

x = myClass1()
x.width = 1
x.height = 2
print("get size:")

# 其实是调用property对象中的getValue函数
print(x.size)

# 其实是调用property对象中的setValue函数
print("set size:")
x.size = 3, 4
print(x.width)

class myClass11:
    def __init__(self):
        self.width = 0
        self.height = 0

    # 特殊方法中实现特性的赋值，所以类似于x.name = value
    # 这样的特性操作就得先经过__setattr__方法，而不是直接的赋值
    # 特殊方法就是在特定操作下自动被调用的方法，如=赋值操作
    # 其他常用特殊方法还有__sub__（调用-减号时调用，加号则是__add__，__iadd__为实地相加）
    # __lt(<号)，等等使用这些方法，能实现类似于C++中的运算符重载机制
    def __setattr__(self, name, value):
        if name == 'size':
            self.width, self.height = value
        else:
            # 如果使用self.name = value,将会再次调用__setattr__，这样会
            # 出现死循环
            self.__dict__[name] = value

    # 这个也会拦截对象的__dict__特性，这时可以使用super函数使用超类
    # 中的__getattr__方法
    def __getattr__(self, name):
        if name == 'size':
            return self.width, self.height
        else:
            raise AttributeError

    def __delattr__(self, name): pass

x = myClass11()
# 其实是调用特殊方法__setattr__
print("set size by __setattr__:")
x.size = 3, 4
print(x.width)

print("get size by __getattr__:")
# 其实是调用特殊方法__getattr__
print(x.size)

# 可用于with的特殊方法, 常用于资源的上下文管理
class withClass():
    def __init__(self, filename):
        self.filename = filename
    # with 进入后调用
    def __enter__(self):
        self.f = open(self.filename)
        # 返回的值会赋值给as后面的变量
        return self.f
    # with结束后调用
    def __exit__(self)：
        self.f.close()
with withClass('hello.txt') as w:
    pass

# 同时继承于两个类
class ssubClass(myclass, myClass1):
    ""
x3 = ssubClass()
# 使用的是第一个继承的myclass类中方法
x3.setValue()
# 检查对象是否有指定特性
print(hasattr(x3, 'setValue'))
# 获取特性
print(getattr(x3, "setValue", ''))
# 设置对象的特性并赋值
setattr(x3, 'name', 'Mike')
# 查看对象有哪些特性
print(x3.__dict__)

# 抛出了异常类的实例
#raise Exception

# 导入异常模块， 找不到模块。。。内建异常有SyntaxError等
#import exceptions

# 自定义继承于Exception的异常类
class myException(Exception):
    pass

class myclass3:
    def func():
        # 发生异常并自定义捕捉异常类型
        try :
            1/0
       # 捕捉并打印异常对象，如果没有捕捉异常，则异常传播至函数被调用的地方
       # 如果都没有捕捉异常的地方，则会传播至全局区域，这时如果也没有捕捉，
       # 则程序中止，相比if判断，效率高些，因为判断条件中要执行完语句才知道结果
        except (ZeroDivisionError) as e:
            print("catch the Exeption")
            print(e)

            # 重新抛出异常
            raise
        except TypeError: pass

        # 捕捉两种类型的异常
        except(ZeroDivisionError, TypeError): pass

        # 捕捉所有Exception异常,但不建议那么做，无法预知具体的异常错误
        except Exception as e: pass

        # 如果没捕捉到异常，则可以执行一些自定义操作
        else: pass

        # 不管是否抛出异常，都会执行finally中的语句，但在finally中引发的异常却是无法被捕捉到的
        finally: pass

# myclass3.func()

def checkIndex(key):
    if not isinstance(key, (int)): raise TypeError
    if key < 0 : raise IndexError

# __双下划线开头的为特殊函数
class myList:
    def __init__(self, start = 0, step = 1):
        self.start = start
        self.step = step
        self.changed = {}

    def __getitem__(seft, key):
        checkIndex(key)

        try: return seft.changed[key]
        except KeyError:
            return seft.start + key*seft.step

    def __setitem__(seft, key, value):
        checkIndex(key)

        seft.changed[key] = value

s = myList(1,2)

# s[4]调用了类中的特殊函数__getitem__
print(s[4])

# 继承list类并重写__init__与__getitem__方法，带有计数功能
class myList2(list):
    def __init__(seft, *args):
        super(myList2, seft).__init__(*args)
        seft.counter = 0
    def __getitem__(seft, index):
        seft.counter += 1
        return super(myList2, seft).__getitem__(index)

# 这样对象的用法就如同调用普通的函数一样，如x = list("hello")
x = myList2("hello")
print(x)
print(x[2])

class myClass4:
    # 指定该方法为静态方法，可以直接使用类调用
    # @staticmethod装饰器返回staticmethod对象，不是
    # callable对象，所以只能在它下面使用别的装饰器
    # 不需要传入cls参数，对外部可以像普通方法一样调用
    @staticmethod
    def staticFunc(): print("this is a static func")

    # 指定该方法为类方法，且cls参数会自动绑定到当前类上，
    # 所以可以直接只用类调用，当然也可以使用类实例调用
    # 方法内部可以返回cls()，这样就像实例一样了，做到通过
    # 函数很好地封装对象
    @classmethod
    def classFunc(cls): print("this is a class func")

myClass4.staticFunc()
myClass4.classFunc()
x = myClass4()
x.staticFunc()

# 由于对象中实现了__next__与__iter__方法，所以
# 该对象可像列表那样在for循环中迭代使用，该对象
# 也可称为迭代器，当__next__无返回值时，将引发StopIteration异常
# 迭代器就是使用__next__函数时才会计算值并返回，这就是迭代器的优势，
# 只有迭代时才会计算生成值
class myIter:
    def __init__(self):
        self.a = 0
        self.b = 1
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a
    def __iter__(self):
        return self

iter1 = myIter()

# in iter时，对象实例调用了__iter__方法，返回对象实例本身
# 继而再调用__next__函数，把返回的结果赋值于i
for i in iter1:
    if i > 100:
        print(i)
        break

# 获取list对象的迭代器
iter2 = iter([1, 2, 3])
next(iter2)

class myIter2:
    value = 0
    def __next__(self):
        self.value += 1
        if self.value > 10: raise StopIteration
        return self.value
        return self.value
    def __iter__(self):
        return self

iter3 = myIter2()

# list对象的构造函数可以将迭代器转换成列表
print(list(iter3))

nested = [[1,2], [3,4], [5,6,7]]

# 函数中包含有yield语句的则该函数称为生成器，
# yield语句会使函数冻结暂停，返回一个迭代器等待被激活后从暂停
# 点开始继续执行，生成器每遍历一次才把数据放入内存中，所以可以
# 处理很大的数据
def myGenerator(listParam):
    for sublist in listParam:
        for element in sublist:
            # 第一次被挂起后，再次激活运行后yield才会返回值，其实是外部通过
            # send方法发送给生成器的值
            yield element

for element in myGenerator(nested):
    print(element)

# 生成器推导式，返回一个生成器
creator = (i for i in range(5, 10))
print(next(creator))

# 可以这样使用生成器，无需多一对圆括号
sum(i for i in range(5, 10))

nested = [[1,2], [3,4,[33,44]], [5,6,7]]

# 使用递归生成器能处理嵌套层数不固定的序列，但要是被迭代元素为
# 字符串时，将导致无限递归，因为字符串就是队列，for i in永远不会引发
# 异常
def myGenerator2(listParam):
    try:
        for sublist in listParam:
            # 以上for in试图迭代一个非序列对象时，引发异常，捕捉并返回迭代器，
            # 进而给element赋值，然后被使用于yield语句中
            for element in myGenerator2(sublist):
                yield element
    except TypeError:
        yield listParam

for element in myGenerator2(nested):
    print(element)


nested = ['h', ['e', 'llo']]
def myGenerator3(listParam):
    try:
        # 迭代字符串时，加入检查机制，如果为字符串，则直接产生元素
        # 这样不会导致无穷递归
        try: listParam + ''
        except TypeError: pass
        else: raise TypeError
        for sublist in listParam:
            # 试图迭代一个非序列对象时，引发异常，捕捉并产生元素
            for element in myGenerator3(sublist):
                yield element
    except TypeError:
        yield listParam

for element in myGenerator3(nested):
    print(element)
print(list(myGenerator3(nested)))

def myGenerator4(value):
    while(True):
        new = (yield value)
        if new is not None: value = new

x = myGenerator4(1)
# next方法被调用后，yield返回None
print(next(x))

# 再次使用时，传给生成器的参数变成了None，
# send方法会在生成器挂起后发送数据给生成器的yield表达式
# 激活生成器，生成器挂起后才能使用send方法
print(x.send('hello'))

# 以下并不是真正的生成器，由于可以像访问生成器那样
# 对其迭代进行访问，所以也叫模拟生成器
def myGenerator4(listParam):
    result = []
    try:
        try: listParam + ''
        except TypeError: pass
        else: raise TypeError
        for sublist in listParam:
            for element in myGenerator3(sublist):
                result.append(element)
    except TypeError:
        result.append(listParam)
    return result

for element in myGenerator4(nested):
    print(element)

# n*n棋盘，同行同列同对角线不能放置同一*符号，已知前n-1位置，求第n个可能的位置
# ------------
# |   | * |   |   |
# ------------
# |   |   |   | * |
# ------------
# | * |   |   |   |
# ------------
# |   |   |    |   |   pos:?
# ------------

def conflict(state, nextX):
    nextY = len(state)
    for i in range(nextY):
        if abs(state[i] - nextX) in (0, nextY - i):
            return True
    return False

def symbols(num, state):
    if len(state) == num -1:
        for pos in range(num):
            if not conflict(state, pos):
                yield pos
pos = list(symbols(4, (1,3,0)))
print(pos)

# 递归实现符号位置摆放方案，可针对任意n*n棋盘
def symbols2(num, state = ()):
    for pos in range(num):
        if not conflict(state, pos):
            if len(state) == num -1:
                yield (pos,)
            else:
                    for result in symbols2(num, state + (pos,)):
                        yield (pos,) + result
allPos = list(symbols2(4))
print(allPos)

# 整理下输出结果
def formatPrint(solution):
    def line(pos, length = len(solution)):
        return '. ' * (pos) + 'X' + '. ' * (length - pos - 1)
    for pos in solution:
        print (line(pos))

import random
print(formatPrint(random.choice(list(symbols2(4)))))
print(formatPrint(random.choice(list(symbols2(8)))))

# 只返回单个实例的类
# type与object都属于type object类型对象，其实是同一个东西
# python3.x可以省略不明显继承于object
class c(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        time.sleep(1)
        name = 'kk'
    
    # 通过类方法返回实例
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(c, '_instance'):
            # 加锁是因为如果类的实例化是在线程中实行的
            # 那么由于一些io操作，资源混乱，导致每个
            # 实例初始化都不一样
            with c._instance_lock:
                if not hasattr(c, '_instance'):
                    c._instance = c(*args, **kwargs)
        return c._instance

    # 通过__new__返回实例，通过类创建对象时自动调用
    # *args默认收集三个参数(name类名称, bases父类集合, 类实例字典__dic__)
    # 其不会收集创建实例时传入的参数，这些参数传给__init__函数
    # 可以对args的第三个参数参数进行扩展，动态添加属性
    def __new__(cls, *args, **kwargs):
        if not hasattr(c, '_instance'):
            with c._instance_lock:
                if not hasattr(c, '_instance'):
                    c._instance = object.__new__(cls)
        return c._instance
    
        
def task(arg):
    obj = c.instance()
    print(obj)

for i in range(5):
    t = threading.Thread(target=task, args=[i,])
    t.start()

class SingletonParent(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonParent._instance_lock:
                if not hasattr(cls, "_instance"):
                    # type的__call__方法中会执行__init__与__new__方法
                    cls._instance = super(SingletonParent,cls).__call__(*args, **kwargs)
        return cls._instance

class Singleton(metaclass=SingletonType):
    def __init__(self,name):
        self.name = name

# Singleton()会调用元类的__call__方法，
# 可以在其中返回实例对象
obj1 = Singleton()
obj2 = Singleton()

def Singleton(cls):
    _instance = {}
    # 多次实例化时，只返回相同的实例对象
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@decorSingle
class A:
    name = 'kk'

# 闭包=函数+引用环境，内部返回函数引用
def exFunc(arg):
    n = arg
    a = 1
    b = 1
    def innerFunc(inArg=1):
        # 这里的a其实是本函数内部定义的，并不是
        # 外部定义的，所以这里并没有改变外部的a
        a = 123
        # 这里认为b已经在本函数内定义了, 所以找
        # 不到报错，但使用nonlocal声明其为非局部
        # 量可以使用
        # b = b + 1
        # 对非全局的外部作用域变量进行引用，由此产生闭包
        return n + 1 + inArg
    # 由于内部函数引用了外部变量，因此会把所引用的对象
    # 与环境打包成一个整体返回
    return innerFunc
# 会产生两个不同的函数实例
f1 = exFunc(1)
f2 = exFunc(2)
print(f1())
print(f2())
# 参数3会和函数打包进一个环境变量中返回给f3
# 因此闭包可以保持所需的环境变量
f3 = exFunc(3)
print(f3(3))

flist = []
for i in range(3):
    # i只有在func执行时才会去赋值
    # 所以所有的func都会取到最后一个迭代的i值
    # 可以改成func(x, y=i)形式
    def func(x): print(x + i)
    flist.append(func)

for f in flist:
    f(2)

from functools import wraps

# 装饰器
# 装饰器要求接收一个callable对象作为入参
def mydecorate(func):
    # 经过wraps装饰后func能保留函数原始的信息如__name__,不然属性
    # 就全部变成innerFunc的属性了
    @wraps(func)
    def innerFunc(*args, **kwargs):
        print('enter {}'.format(func.__name__))
        return func(*args, **kwargs)
    return innerFunc

def mydecorate2(level):
    # 参数会延级接受，第一装饰器参数，第二函数对象参数
    # 第三函数对象自己的参数
    def wrapper(func):
        def inner_wrapper(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return wrapper

@mydecorate
def testFunc(arg)
    return arg + 1

import inspect
print(inspect.getargspec(func))
print(inspect.getsource(func))

@mydecorate2(level="LOG")
def testFunc(arg)
    return arg + 1

from decorator import decorate

def wrapper(fun, *args, **kwargs):
    return func(*args, **kwargs)

def logging(func):
    # decorate使用wrapper装饰func
    return decorate(func, wrapper)

@logging
def testFunc(arg)
    return arg + 1

import wrapt

# 使用wrapt实现的装饰器
@wrapt.decorator
# instance在装饰器装饰类的实例方法时可以得到类实例
def logging(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)

def logging2(level):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)
    return wrapper

@logging
def testFunc(arg)
    return arg + 1

@logging2(level="INFO")
def testFunc(arg)
    return arg + 1


import sys

# os也是标准库中常用的模块
import os

from os import *

# 结合生成器与os模块与递归实现列出指定目录下所有文件
def getFileList(dir):
    try:
        files = os.listdir(dir)
        # path.join使用的路径分隔符根据系统类型而定
        fullfile = [os.path.join(dir, name) for name in files]
        for d in fullfile:
            for dd in getFileList(d):
                yield dd
    except Exception:
        yield dir

# environ获取环境变量
print(os.environ["USERNAME"])

# system用于执行外部程序，注意目录是""引起来的，这样不会被当作程序来运行
# 而使用startfile不用双引号
# os.system(r'D:\"Program Files (x86)"\"KuGou"\"KGMusic"\KuGou.exe')
# os.startfile(r'D:\Program Files (x86)\KuGou\KGMusic\KuGou.exe')
print(os.pathsep)

import webbrowser
# 可以这样打开网址
# webbrowser.open("http://www.baidu.com")

# 加载模块所在路径后，就可以直接导入该路径下的模块了，
# 模块名就是文件名
sys.path.append('../..')

# sys模块还有其他有用的特性，如exit，可以退出当前程序
# argv获取运行脚本时附带在脚本名称后面的参数
print(sys.path)
import pprint
# 智能打印，包括对list对象的换行打印
pprint.pprint(sys.path)
import test1
 # 使用模块的特性
print(test1.test)

# 查找模块所在位置
print(test1.__file__)

# 在交互器中使用help函数可以查看模块的特性信息
# help(test1.test)

# 重复导入的效果与一次导入的效果是相同的，
# 所以两个模块可以互相导入
import test1

# 内置的dir函数可以查看模块中有哪些特性
print([n for n in dir(test1) if not n.startswith('__')])


# 表示当前.py程序要是在主程序中运行，则执行相应的操作
if __name__ == '__main__': print('hello main')

# 可以将模块放在编译器默认查找模块路径的目录下，这样可以直接导入，如site-packages目录
# 也可以设定系统环境变量并设置路径，编译器会去该路径下寻找模块
import easy_install

# 导入包，包名其实就是目录名，该目录下必须包含__init__.py文件
import mypacket
# 可以直接使用包中__init__模块的特性
print(mypacket.x)

# 导入包中其他模块
import mypacket.test

import fileinput

# fileinput模块的input函数可以在解释器中读取.py脚本名称后的参数指定的文件，读取完一个文件后
# 继续读取下一个文件，也可以nextfile自动切换到下一个文件
# inplace=True原地替换模式，所以请慎用
#for line in fileinput.input(inplace=True):
#    print(line)

# 集合{1,2,4...}，有数学中常见的操作，如求并集，比较大小等
a = set([1,2,3])
b = set([3,4])
print(a >= b)
# union与|运算符等效
print(a.union(b))
print(a|b)
c = a & b
print(c.issubset(a))
print(a.union(b))
print(a-b)

# 集合不能添加可变值，但可以使用frozenset添加其他集合
# 已有的元素不会被添加进去
a.add(6)
a.add(frozenset(b))
print(sorted(a))

from functools import reduce
# 可以求多个集合的并集
x = reduce(set.union, [{1,2,3},{3,4}, {3,4,5}])
print(x)

from heapq import *
from random import shuffle
data = [1,2,3,4,5]
# 打乱队列元素顺序
shuffle(data)
heap = []
for n in data:
    # heappush建立了堆，也可以使用heapify建立
    heappush(heap, n)
print(heap)

# 入堆时，堆算法内部会自动把最小的数排序在第一位
heappush(heap, 0.1)
print(heap)

# heappop弹出最小的元素
print(heappop(heap))
print(heappop(heap))

# 弹出最小的元素后插入新的元素
x=[0,1,2]
heapreplace(x, 0.5)
print(x)
heapreplace(x, 3)
print(x)

y=[3,1,2]
# 升序排序后返回堆前三个元素，比sorted函数效率更高
n = nlargest(3, y)
print(n)

# 降序排序后返回堆前两个元素
n = nsmallest(2, y)
print(n)

# 字典排序
d = {'k5':5, 'k6':6, 'k1':1}
newD = sorted(d.items(), key=lambda d: d[1], reverse=True)
print(newD)
print(dict(newD))

from collections import deque
# 建立一个双端队列，可在列头或列尾增减元素
q = deque(range(5))
q.append(5)
q.appendleft(6)
print(q)
print(q[0])
q.pop()
q.popleft()
# 整体往右移动三位
q.rotate(3)
print(q)
# 在右侧扩展队列
q.extend([6,7])
print(q)


# 时间模块
import time

# (2018, 9, 20, 21, 31, 0, 30, 0) 对应年月日时分秒周天夏令时
print(time.mktime((2018, 9, 20, 21, 31, 30, 3, 30, 0)))

# 时间元组转换成字符串
print(time.asctime())

# 将秒数转换为日期元组
print(time.localtime())

# 等待三秒钟后继续执行
# time.sleep(3)

# 获取全球统一标准时间
uniTime = time.gmtime()
print(uniTime)
print(uniTime[0])

from timeit import timeit
# 计算代码运行所需时间
timeit('x=range(10)')

# 随机数模块
import random

# 返回三位二进制后转换成长整型
print(random.getrandbits(3))

# 获取0-1之间的伪随机数
print(random.random())

# 获取1到5之间的随机实数
print(random.uniform(1,5))

# 返回range中的随意数
print(random.randrange(1,10))

# 返回序列中的的随意元素
print(random.choice([1,2,3,4,5]))

# 打乱序列
a = [1,2,3,4,5]
random.shuffle(a)
print(a)

# 从序列中随机返回n个元素
print(random.sample([1, 1, 2, 2, 3, 3, 4, 5], 2))


# 例子，可以这样来理解，抛三枚骰子后，求骰子朝上的面的点数的总和
sum = 0
for i in range(3): sum += random.randrange(6) + 1
print(sum)

# 建立 一副扑克牌并随机打乱顺序
digital = list(range(2,11)) + 'J Q K A'.split()
shape = "♠ ♥ ♣ ♦".split()

poker = ['%s%s' % (s, d) for s in shape for d in digital]
#poker.append('♔ ♕'.split())
poker.extend('♔ ♕'.split())
random.shuffle(poker)

from pprint import pprint
pprint(poker[:12])

#while poker:
#    tmp = input("get poker:")
#    x = poker.pop();
#    print(x)

# shelve模块提供一种简单的数据存储方案，可以把数据存储在dat二进制文件中
import shelve
# open方法:如果文件不存在，会创建test1.py.dat文件，返回一个shelf对象
f = shelve.open('mypacket/test1.py')
# 返回的对象可以当做字典一样使用，这里把数据存储到了dat文件中
f['x'] = [1,2]
# 这里的对象与普通字典不一样，append方法其实是把数据添加到副本中
# 所以f['x']并没有被改变
f['x'].append(3)
print(f['x'])

# 可以通过重新赋值达到append的效果
temp = f['x']
temp.append(3)
f['x'] = temp
print(f['x'])

# 存取完数据后close对象，不然之后的操作可能会损坏已经存取的数据，下次读取的
# 时候可能读取不了
f.close()

f = shelve.open('mypacket/test1.py')
# 再次打开存储文件的时候，可以访问到之前存储过的内容
print(f['x'])
# 试图访问对象不存在的key时，会出错
# print(f['y'])
f.close()

# 正则表达式模块
import re
# 会在开头匹配，匹配到则返回match对象，否则返回None
# 首先会把'h'转换成re匹配对象，再去匹配，search也会经过这样的
# 的转换
print(re.match('h', 'hello'))
# 转换成re匹配对象，使用其匹配效率会更高
x = re.compile('he')
print(x.match('hello'))

print(re.match('e', 'hello'))
# ? 可选项，匹配有的或是没有的
print(re.match('e?', 'hello'))
# 会从开始到结尾匹配，找到第一个符合的就返回
print(re.search('e', 'hello'))

text = "hello... wo-rld! are you ok"
# 以指定模式分割字符串，[]集合匹配，+匹配1到多个，匹配集合中的单个字符，'.'为通配符
x = re.split('[. ]+', text)
print(x)
# 位于集合匹配中的^符号是非的意思,re.S表示匹配.，所以也可以匹配\n,
x = re.findall('[^h]+', text, re.S)
print(x)
# ()子模式匹配，'wo'两边会被分割开来，但'o'会出现在分割后的列表中
x = re.split('w(o)', text)
print(x)
# 返回的是()组中的内容，| 管道可以匹配两个
print(re.findall('a(rr|re)', text))

# 以列表形式返回所有匹配到的项，返回组0，即所有匹配到的项
print(re.findall('[a-z]+', text))
# \反斜杠转义了正则表达式中的'-'符号，使其不会当作范围字符来处理
print(re.findall('[.\-!]+', text))

# 字符串中把匹配模式的pat替换成指定字符
pat = 'ok'
print(re.sub(pat, 'sure', text))

# 把字符串中的所有正则表达式字符进行转义，如. ? - 等
print(re.escape(text))
x = re.search('(ar.)', text)
# 返回匹配模式对象中的第1个匹配组
# 位于匹配模式中()内的内容就是匹配组的内容
# 如果没有()，默认匹配到的所有字符就是组的内容，即组0
# 返回第一个匹配组匹配项的开始索引
print(x.start(1))
# 返回第一个匹配组匹配项的结束索引
print(x.end(1))
# (?P<groupname>he) ?P<name>可以指定组名,之后
# 可以通过gourp(name)进行访问
print(re.search('(?P<name>he)', 'hello'))
# 有了re.VERBOSE参数，就可以在匹配模式中添加注释了，这样不会当作
# 匹配模式的一部分去匹配
print(re.search('\- # 转义"-"符号', text, re.VERBOSE))

# \1将使用匹配组1([^\*]+)匹配到的内容进行替换
print(re.sub('\*([^\*]+)\*', r'<html>\1</html>', 'hello *world*!'))
# .+把中间的星号也当作任意字符来对待了，直到遇到最后的*为止，这是贪婪匹配
print(re.sub('\*(.+)\*', r'<html>\1</html>', 'hello *wo**rld*!'))
# .+? 加个?，只要遇到符合匹配的就匹配一个，接着再继续匹配，这是非贪婪匹配
print(re.sub('\*(.+?)\*', r'<html>\1</html>', 'hello *wo**rld*!'))

import fileinput
# 例子，查找文件中所有type的值，使用.*?非贪婪匹配
# 这样找到第一个符合匹配的就返回，而不是忽略中间的'type'继续匹配到最后一个'type'
pat = re.compile('.*?type="(.*?)"( |>)')
for line in fileinput.input():
    result = pat.search(line)
    if result: print(result.group(1))

# 查找获取不重复的数据
pat = re.compile('.*?type="(.*?)"')
typeset = set()
for line in fileinput.input():
    for result in pat.findall(line):
        typeset.add(result)
print(sorted(typeset))

# 模板填充变量，定义:[name="Mike"]， 模板:hello, [name]->hello, Mike
# 可以接收两个文件，一个是模板变量定义文件，一个是模板文件
pat = re.compile('\[(.+?)\]')
# 把变量收集到该作用域
scope = {}
def replacement(match):
    code = match.group(1)
    try:
        # 如果作用域中定义了变量，则计算值并返回
        return str(eval(code, scope))
    except SyntaxError:
        # python 2.0写法
        # exec(code) in scope
        # python 3.0写法
        # 在作用域中计算如"name='mike'",
        exec(code, scope)
        return ''

# 文件内容全部存于一个字符串中
lines = []
for line in fileinput.input():
    lines.append(line)
# 转换成字符串
text = ''.join(lines)

# 每匹配到一个，就把匹配到的内容作为参数调用replacement函数，
# 用函数返回的值替换匹配到的项
print(pat.sub(replacement, text))

# open方法返回一个文件流对象，此方法不会自动创建文件，参数默认是'r'
f = open(r'myfile\template.txt')
# 从文件开头读取三个字节长度的内容，并记录读取到的位置
f.read(3)
# 从上一次读取到的位置继续读取
f.read(2)
# 移动到文件流第二个字节
f.seek(2)
# 确定不再使用文件流的时候应该手动调用close方法关闭文件
# close后才会解除其他程序对文件的访问限制
# 虽然程序退出的时候也会自动关闭，但可能因为某些情况
# 如程序崩溃可能会导致无法正确地保存文件，
f.close()
f = open(r'myfile\template.txt')
# 读取文件所有内容，读到文件尾时，返回空字符串
print(f.read())
f.close()
f = open(r'myfile\template.txt')
# 读取一行
f.readline()
# 从上次读取到的行后位置继续读取新行
f.readline()
f.close()
f = open(r'myfile\template.txt')
# 返回一个列表，列表中的每一项对应文件每一行的内容,
# 包括行尾的换行符\n
f.readlines()
f.close()
# 指定w参数可以向文件中写入内容
f = open(r'myfile\template.txt', 'w')
# \n是换行符
f.write('how are you\nfine, thanks\n')
f.close()
f = open(r'myfile\template.txt', 'w')
# 按行写入，接受列表传参
f.writelines(['so late!\n', 'maybe we can walk faster'])
f.close()

# 以二进制方式读取文件，读取声音等二进制文件的时候需要，而且不会把文件中
# 换行解释成换行符
f = open(r'myfile\template.txt', 'rb')
print(f.read())

# with语句结束后会自动关闭文件，即使发生异常也会关闭
with open(r'myfile\template.txt') as f:
    f.read()

def process(str):
    print("process...."+str)

f = open(r'myfile\template.txt')
# 在循环读取文件的过程中，可以针对读取到的每一项内容进行自定义处理
#while True:
#    char = f.read(1)
#    if not char: break
#    process(char)
#f.close()
while True:
    line = f.readline()
    if not line: break
    process(line)
f.close()

#f = open(r'myfile\template.txt')
#for char in f.read():
#    process(char)
#f.close()

# 每次只读取一行如readline函数，这种叫做懒惰行迭代，只读取需要的行
import fileinput
for line in fileinput.input(r'myfile\template.txt'):
    process(line)

# 可以直接对文件流进行迭代，但在程序关闭的时候才能close文件
for line in open(r'myfile\template.txt'):
    process(line)

# 对标准输入进行迭代
#import sys
#for line in sys.stdin:
#	print("new line"+line)

# 把文件流转换成列表
lines = list(open(r'myfile\template.txt'))
print(lines)

# 文件流赋值给多变量时，就相当于把文件每一行赋值给单独的变量
f, s = open(r'myfile\template.txt')
print(f)
print(s)

# 流行GUI库wxPython，还有其他GUI库如Tkinter(python标准库自带)，AWT、Swing(两者都是在Jython环境中使用)
import wx
app = wx.App()
# None 表示不需要父部件作为构造函数的参数来创建窗口(Frame)
win = wx.Frame(None, title = '文本编辑器', pos = (660, 390), size = (435, 500))
# 在Frame上增加控件
# 可以设置每个按钮的大小，风格
# 如果只有一个按钮，设置位置及大小将无效，以下是固定设置控件的尺寸，
# 并不会随窗口大小而变化
#btnOpen = wx.Button(win, label = '打开', pos = (255, 5), size = (80,25))
#btnSave = wx.Button(win, label = '保存', pos = (335, 5), size = (80,25))
#textInput = wx.TextCtrl(win, pos = (5,5), size = (250, 25))
## 指定了style风格后，文本框转换成文本区
#contextText = wx.TextCtrl(win, pos = (5, 35), size = (410, 425), style = wx.TE_MULTILINE | wx.HSCROLL)

def load(event):
     f = open(textInput.GetValue())
     contextText.SetValue(f.read())
     f.close()

def save(event):
    f = open(textInput.GetValue(), 'w')
    f.write(contextText.GetValue())
    f.close

def eraseBackground(event):
     dc = event.GetDC()
     if not dc:
         dc = wx.ClientDC(contextText)
         rect = contextText.GetUpdateRegion().GetBox()
         dc.SetClippingRect(rect)
     dc.Clear()
     bmp = wx.Bitmap(r"E:\picture\fire.jpg")
     dc.DrawBitmap(bmp, 0, 0)

# 以下以相对大小设置控件尺寸
# 控件都放在一个面板上
bkg = wx.Panel(win)
btnOpen = wx.Button(bkg, label = '打开')
# 把打开文件函数绑定到点击按钮事件上
btnOpen.Bind(wx.EVT_BUTTON, load)
btnSave = wx.Button(bkg, label = '保存')
btnSave.Bind(wx.EVT_BUTTON, save)
textInput = wx.TextCtrl(bkg)
contextText = wx.TextCtrl(bkg, style = wx.TE_MULTILINE | wx.HSCROLL)
contextText.SetBackgroundColour("LIGHT GREY")
#contextText.Bind(wx.EVT_ERASE_BACKGROUND, eraseBackground)

# 尺寸控制器，默认水平布局
hbox = wx.BoxSizer()
# 以下控件设置的水平空间占用比例为1:0:0，当然比例也调整成其他如3:2:1
hbox.Add(textInput, proportion = 1, flag = wx.EXPAND)
# 设置左边距为5
hbox.Add(btnOpen, proportion = 0, flag = wx.LEFT, border = 5)
hbox.Add(btnSave, proportion = 0, flag = wx.LEFT, border = 5)

# 垂直布局尺寸器，尺寸器中也可以把其他的尺寸器添加进来，形成多层次布局
vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
vbox.Add(contextText, proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)

# 设置面板尺寸控制器
bkg.SetSizer(vbox)

# 窗口只有Show才会展示，不然会隐藏
win.Show()
app.MainLoop()

# sqlite数据库模块
import sqlite3
# 会创建一个数据库db文件
conn = sqlite3.connect('myfile/mysqlitedb.db')
# 游标
curs = conn.cursor()
#curs.execute(
#    CREATE TABLE fruit
#    (
#        id INTEGER primary key,
#        name TEXT,
#        desc TEXT
#    )
#
#    )

insertSql = "insert into fruit values(?,?,?)"
querySql = "select id, name, desc from fruit"
# 从文件中读取数据并插入数据库文件中
#for line in open('myfile/fruit.txt'):
# fields = line.split(',')
# vals = [v for v in fields]
# curs.execute(insertSql, vals)
#curs.execute(insertSql, [2, 'watermelon', 'contain a lot of moisture'])
# 插入不同的数据类型，如Time,Date等
#curs.execute(insertSql, [sqlite3.Time(1,2,3), '', 'contain a lot of moisture'])
curs.execute(querySql)
# fetchall获取所有行，还有rowcount，description等操作
for row in curs.fetchall():
    print(row)
conn.commit()
conn.close()

# 网络编程套接字模块
import socket
# 建立一个服务端套接字，建立套接字->绑定地址->监听连接->等待连接
server = socket.socket()
host  = socket.gethostname()
port = 1025
# 绑定的地址格式为元组
server.bind((host, port))
# 最多同时监听5个连接
server.listen(5)
while True:
    # accept接收连接请求之前会阻塞
    client, addrClt = server.accept()
    print('Got connection from ',addrClt)
    client.send(b'Thanks for connecting')
    client.close()

#client = socket.socket()
#host  = socket.gethostname()
#port = 1025
#client.connect((host, port))
## 一次最多可接收1024个字节的内容
#print(client.recv(1024))

# python3中urllib是一个包，urlopen位于包的request模块中
from urllib.request import urlopen
# 也可以open本地文件
# 返回类文件对象
webpage = urlopen('https://www.python.org/')
# 可以把返回的页面当作文件一样读取
text = webpage.read()
# 如果存在中文，则按utf-8格式解码
text = text.decode('utf-8')

import re
#s = '<a href="http://map.baidu.com" name="tj_trmap" class="mnav">地图</a>'
rerult = re.search('<a href="(.*?)" .*?>about</a>', text, re.IGNORECASE)
print(rerult.group(1))

from urllib.request import urlretrieve
from urllib.request import quote
# 获取网页文件并保存到本地，没有指定文件名时，保存在临时目录，使用
# urlcleanup可以清除临时目录中的文件
urlretrieve('https://www.python.org/', 'myfile/python.html')
# quote会把url中的特殊字符转换成对url友好的字符后再返回url
# 如会把~转换成%7E，unquote功能则相反
webpage = urlopen(quote('https://www.~myurl.org/'))

from urllib.parse import urlencode, parse_qs
# 返回param1=test&amp;param2=%c%de类似的字符串
# 这些字符串可以在url中当作参数，如服务器cgi脚本是用
# python编写的，则可通过cgi模块的getvalue方法获取到参数
print(urlencode({'param1':'test', 'param2':'你好'}))
# 与urlencode相反
print(parse_qs('name=hello&value=22'))
# 返回元组
print(parse_qsl('name=hello&value=22'))

# 导入基础网络服务器框架socketserver，包含TCP,UDP类等
from socketserver import TCPServer, StreamRequestHandler, ThreadingMixIn

# 使用线程处理，每来自一个请求，开启一个线程来处理，
# 也可以采用分叉进程来处理，就是开启多个进程，但在windows中不支持
class Server(ThreadingMixIn, TCPServer): pass

# 继承于StreamRequestHandler类
class Handler(StreamRequestHandler):
    # 重写StreamRequestHandler类中handle处理函数
    def handle(self):
        addr = self.request.getpeername()
        print('the connection from ', addr)
        self.wfile.write(b'hello')

#server = TCPServer(('', 1025), Handler)
# 把端口号与自定义处理类作为构造函数的参数
server = Server(('', 1025), Handler)
server.serve_forever()

import socket, select
s = socket.socket()
s.bind((socket.gethostname(), 1025))
s.listen(5)
inputs = [s]
# 结合select 模块实现响应多个连接
while True:
    # 找出准备好读写的套接字，这样就是处理多个连接了，实现异步socket，select的第四个参数为等待连接的超时时间，为0则不会阻塞
    # 返回的元组的第一个元素是输入文件描述符序列
    # select会监听inputs的状态
    # 给每一个连接分配一个时间片段，这点不同于多线程的同时处理，不会出现多线程中的同步问题
    rs, ws, es = select.select(inputs, [], [], 0)
    for r in rs:
        # 有新客户端请求连接
        if r is s:
            c, addr = s.accept()
            print('connection from ', addr)
            inputs.append(c)
        else:
             try:
                 data = r.recv(1024)
                 disconnected = not data
             except socket.error:
                 disconnected = True
             if disconnected:
                 print(r.getpeername(), 'disconnected')
                 inputs.remove(r)
             else:
                print(data)

import socket, select
s = socket.socket()
s.bind((socket.gethostname(), 1025))

fmap = {s.fileno():s}

s.listen(5)
# 使用poll方法实现接收多个请求连接
# 返回一个poll对象
p = select.poll()
# 注册一个对象得到其文件描述符
p.register(s)
while True:
    events = p.poll()
    # 获取对象的状态，包括其文件描述符，在对象上发生的事件
    for fd, event in events:
        # 有新客户端请求连接
        if fd in fmap:
            c, addr = s.accept()
            print('connection from ', addr)
            p.register(c)
            # 把客户端的socket对象也注册
            fmap[c.fileno()] = c
        elif event & select.POLLINT:
            data = fmap[fd].recv(1024)
            if not data:
                print(fmap[fd].getpeername(), 'disconnected')
                p.unregister(fd)
                del fmap[fd]
        else:
            print(data)

# 使用twisted的简单网络服务器， 这是基于事件处理的网络编程框架
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver

# 继承于Protocol类
class MyLogger(Protocol):
    # 重写Protocol类的函数，有客户端连接时自动被调用
    def connectionMade(self):
        print ('connection from ', self.transport.client)
    # 客户端断开连接时自动被调用
    def connectionLost(self, reason):
        print(self.transport.client, 'disconnected')
    # 接收到客户端数据自动被调用，可能一行只显示一个字符
    def dataReceived(self, data):
        print(data)

# 协议对象工厂
factory = Factory()
# 自定义处理协议，但也可以默认使用工厂中默认的协议
factory.protocol = MyLogger
reactor.listenTCP(1025, factory)
# 启动服务器
reactor.run()

# 继承于LineReceiver类
class MyLogger(LineReceiver):
    def connectionMade(self):
        print ('connection from ', self.transport.client)

    def connectionLost(self, reason):
        print(self.transport.client, 'disconnected')

    # 可以接收到完整的行，而不是每一个字符占一行
    def lineReceived(self, line):
        print(line)

factory = Factory()
factory.protocol = MyLogger
reactor.listenTCP(1025, factory)
reactor.run()

from subprocess import Popen, PIPE
text = open('myfile/test.html', 'rb').read()
# 使用subprocess打开tidy,tidy可以用来修复不规范的html文件(如标签没有正确结束)，以便利于解析
tidy = Popen('tidy', stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
tidy.stdin.write(text)
# 以下实际中不会输出数据
tidy.stdout.read()

# 异步协程函数
async def hello(value):
    # 挂起该协程去执行其他协程，直到其他协程挂起或者完毕
    await asyncio.sleep(10)
    print(str(value),time.time())

def callback(future):
    print(future.result())

# 嵌套协程
async def main():
    task1 = asyncio.ensure_future(hello(1))
    task2 = asyncio.ensure_future(hello(2))
    task3 = asyncio.ensure_future(hello(3))
    tasks = [task1, task2, task3]

    # 完成与等待的协程
    # 此外还有Running,Cacelled状态
    dones, pendings = await asyncio.wait(tasks)
    # 返回结果列表
    #retults = await asyncio.gather(*tasks)
    
loop = asyncio.get_event_loop()
# 创建任务
#task = loop.create_task(hello())
task1 = asyncio.ensure_future(hello(1))
task2 = asyncio.ensure_future(hello(2))
task3 = asyncio.ensure_future(hello(3))
tasks = [task1, task2, task3]
# 任务完成后调用相应的回调函数.传入参数future
task1.add_done_callback(callback)
#loop.run_until_complete(task)
# 并发执行多个任务
#loop.run_until_complete(asyncio.wait(tasks))
loop.run_until_complete(main())

# 取消任务
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt as e:
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()
    loop.run_forever()
finally:
    loop.close()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def work(x):
    print(x)
    await asyncio.sleep(x)

# 新建循环
new_loop = asyncio.new_event_loop()
# 子线程中开启事件循环
t = Thread(target = start_loop, args=(new_loop,))
t.start()
# 在主进程中注册协程对象
asyncio.run_coroutine_threadsafe(work(3), new_loop)
asyncio.run_coroutine_threadsafe(work(4), new_loop)

#new_loop.call_soon_threadsafe(work, 3)
#new_loop.call_soon_threadsafe(work, 4)

# 协程原理
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    # 启动生成器
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        # 切换到consumer执行，consumer会返回yield的内容
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    # 生成器关闭
    c.close()

c = consumer()
produce(c)

from urllib.request import urlopen
from HTMLParser import HTMLParser

class Scraper(HTMLParser):
    in_li =False
    in_data = False
    # 找到开始标签时自动调用
    # attr由（键，值）组成的列表
    def handle_startstag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'li':
            self.in_li = True
        if tag == 'li' and 'data-title' in attrs:
            self.in_data = True
            self.chuncks = []

    # 使用文本数据时自动调用
    def handle_data(self, data):
        if self.in_data:
            self.chuncks.append(data)

    # 找到结束标签时自动调用
    def handle_endtag(self, tag):
        if tag == 'li':
            self.in_li = False
        if tag == 'li':
            if self.in_li and self.in_data:
                print('%s' % ''.join(self.chuncks))

text = urlopen('https://movie.douban.com/').read()
parser = Scraper()
parser.feed(repr(text))
parser.close()
from urllib.request import urlopen
import re
exp1 = re.compile(r'<li class="ui-slide-item"  data-title="(.*?)" data-release=".*?"')
exp2 = re.compile(r'<li class="title">.*?<a.*?>(.*?)</a>.*?</li>')
text = urlopen('https://movie.douban.com/').read()
text = text.decode('utf-8')
movie = set()
for name in exp1.findall(text):
    movie.add(name)

for name in exp2.findall(text):
    movie.add(name)

print(movie)

from urllib.request import urlopen
from bs4 import BeautifulSoup

text = urlopen('https://movie.douban.com/').read()
# Beautiful Soup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码，所以不需要手动转换格式
#text = text.decode('utf-8')
movie = set()
# 使用html.parser解析器，此外还有lxml解析器，xml解析器，html5lib解析器
soup = BeautifulSoup(text, 'html.parser')
# 获取li标签
print(soup.li)
# 获取标签属性
print(soup.li.attrs)
# for tag in soup('li'):
#     nameall = tag('a', 'reference')
#     if not nameall: continue
#     name = nameall[0]
#     movie.add(name)
# 查找类为title的li标签
lill = soup.find_all('li', class_ = 'title')
for nameall in lill:
    for name in nameall.find_all('a'):
        # 获取标签的文本域内容
        content = name.get_text()
        movie.add(content)
print(movie)

import webbrowser
from urllib.parse import urlencode
urlparam = urlencode({'name':'tbq'})
# 访问cgi脚本编写的服务器并自定义传入参数
# 构建较大型复杂网站服务器可以使用django，zope等框架
webbrowser.open('http://localhost/cgi-bin/test.cgi?'+urlparam)
# doctest测试工具，检测模块中的文档字符串
import doctest, test
# 会检查模块中所有的文档字符串，如文档字符串
# 包含'>>> func(x)'，则会检查这个例子在解释器中运行是否得到正确的结果
doctest.testmod(test)

# 单元测试工具unittest，还有专门针对unittest的GUI界面模块
import unittest, test

# 继承于TestCase
class myunitest(unittest.TestCase):
    def testone(self):
        for x in range(-10, 10):
            for y in range(-10, 10):
                result = test.func3(x,y)
                # 如果result == x*y不成立，则抛错
                # 此外还有其他错误抛出方法如failIf,assertEqual等
                self.failUnless(result == x*y, '失败1')

    def testtwo(self):
        for x in range(-10, 10):
            for y in range(-10, 10):
                x = x/10.0
                y = y/10.0
                result = test.func3(x,y)
                self.failUnless(result == x*y, '失败2')

# main函数运行的时候会把TestCase的子类实例化，之后执行'test'开头的的所有方法
unittest.main()

# 代码规范检查工具pychecker, pylint会检查代码的语法，命名规范等
# 如定义x变量则会提示短变量，不是规范的命名
# 可以这样在命令行下使用pylint module，还可以在子进程中调用命令并输出检查结果
import unittest, test
from subprocess import Popen, PIPE
class myunitest2(unittest.TestCase):
    def testone(self):
        # -rn关闭其他报告信息，只显示错误与警告信息
        cmd = 'pylint', '-rn', 'test'
        pylint = Popen(cmd, stdout = PIPE, stderr = PIPE)
        # 如果检查结果为空，证明代码规范检查通过
        self.assertEqual(pylint.stdout.read(), '')

unittest.main()

# 代码运行分析工具，如分析运行次数，时间
import profile, test
# 检查某个函数运行所花时间
#profile.run('test.func3(1, 2)')
# 将检查结果保存至文件中
#profile.run('test.func3(1, 2)', 'test.profile')

import pstats
# pstats工具可以查看保存后的代码分析文件
p = pstats.Stats('test.profile')
print(p.print_stats())

# 以下为导入C++编写的模块，中间需要用到的工具为swig，gcc(或者vs)编译
# 以swig+vs为例：1.编写module.i接口说明文件 2.swig处理.i文件产生包装代码
# 3.源代码与包装代码一起编译产生dll文件 4.把产生的.dll文件改后缀为.pyd,前缀
# 加上_，之后把swig产生的.py与所改的.pyd文件放在python能访问到的目录下，如
# python36/Lib
# 还有其他工具可以使用，这些工具有的将C或者C++代码嵌入python代码中，或者
# 直接导入已经存在的C语言库等，一般需要频繁使用且速度要求高的部分模块可以
# 通过这些方法来使用外部语言编写的模块
from mylib import mydll
isHw = mydll.is_huiwen('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
print(isHw)
#print(dir(testCmodule))

import profile, test
# 遍历1到一亿的数字，python:c++耗时比为69:1
profile.run('test.func6(100000001)')
print('--------------------------------------')
profile.run('test.func7(100000000)')
print(test.func6(100000001))
print(mydll.vistData(100000000))

# 创建python安装包,使用distutil工具，首先编写setup.py文件，里面指定安装的内容，包括
# 包括模块名或者包名，作者等信息，之后运行setup文件，会生成.tar.gz格式(也可以通过命令行参数指定格式)
# 的安装包，里面包含setup.py脚本，运行这个脚本就可以安装模块了，python setup.py bdist --formats=wininst
# 会创建基于window系统.exe文件，运行其也可以安装模块，此外还有其他专业的安装程序可以使用,如Inno setup，
# McMilan installer，py2exe模块能用py脚本生成exe文件，当然也可以使用pyinstaller工具

from distutils.core import setup, Extension
import py2exe

#setup(
#	name='mymodule',
#	version='2.0',
#	description='test module',
#	author='tbq',
#	py_modules=['mymodule']
#)

#setup(
#    name='mymodule',
#	version='2.0',
# 使用源文件与.i文件生成python包
#    ext_modules = [Extension('mymodule', ['mymodule.c', 'mymodule.i'])]
#    )

setup(console=['mymodule.py'])

from configparser import ConfigParser
# 获取配置文件的信息
file = "E:/hexo/source.Olaful.github.io/Olaful.github.io/python/PythonApplication/PythonApplication/myfile/myconfig.ini"
config = ConfigParser()
config.read(file)
# 获取区段
print(config.sections())
print(config.get('num', 'PI'))
# 获取后转换为float类型
print(config.getfloat('num', 'PI'))

# 发送微信消息
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot()

# 搜索名称含有 "助教-Abby2" 的女性深圳好友
my_friend = bot.friends().search('助教-Abby2', sex=FEMALE)[0]

# 发送文本给好友
my_friend.send('Hello WeChat!')

# 发送图片
#my_friend.send_image('my_picture.jpg')

# 打印来自其他好友、群聊和公众号的消息
@bot.register()
def print_others(msg):
    print(msg)

# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('我自动接受了你的好友请求')


# 进入 Python 命令行、让程序保持运行
embed()

# 或者仅仅堵塞线程
# bot.join()

# 单链表
# 定义一个节点，包含本身自定义数据与指向下一个节点的指针
class Node():
    def __init__(self, data):
        self.data = data
        self.next = None

# 定义一个链表，包括初始化链表，打印链表，插入，删除节点
# 求链表长度，这些操作都是通过移动指针遍历链表完成的
class LinkList():
    def __init__(self, node):
        self.head = node

    def printList(self):
        p = self.head
        while p:
            print(p.data)
            p = p.next

    def insertList(self, pos, node):
        p = self.head
        index = 1
        while index < pos:
            p = p.next
            index += 1
            # python不支持自增或自减操作
            #++index

        node.next = p.next
        p.next = node

    def delList(self, pos):
        p = self.head
        index = 1
        while index < pos:
            pre = p
            p = p.next
            index += 1

        pre.next = p.next
        p = None

    def getListLength(self):
        cnt = 0
        p = self.head
        while p:
            p = p.next
            cnt += 1

        return  cnt

ll = LinkList(Node(1))
print(ll.printList())

# 在链表第一个位置后插入节点
ll.insertList(1, Node(2))
print(ll.printList())
# 删除第二个位置的节点
ll.delList(2)
print(ll.printList())

# but python can deal the largest num that depend on the ram, so func below is  a addtional implement
def addBigNum(num1=999999999, num2=99999998):
    result = []
    # 数字切割成列表
    listNum1 = list(reversed(list(map(int, re.findall('\w{1}', str(num1))))))
    listNum2 = list(reversed(list(map(int, re.findall('\w{1}', str(num2))))))
    listNum1.append(0)
    listNum1.append(0)

    maxlen = len(listNum1) if len(listNum1) > len(listNum2) else len(listNum2)

    if len(listNum1) > len(listNum2):
        listNum2.extend([0 for i in  range(maxlen - len(listNum2))])
    else:
        listNum1.extend([0 for i in  range(maxlen - len(listNum1))])

    for i in range(maxlen):
       tmpNum = listNum1[i] + listNum2[i]

       if tmpNum >= 10:
           tmpNum = tmpNum - 10
           listNum1[i+1] += 1

       result.append(tmpNum)

    return int(''.join(list(map(str,reversed(result)))))

sum = addBigNum(9999993495693493495695, 98934994589569569435783459345)
print(sum)

import logging
# 指定输出日志信息的文件，输入提示信息级别
logging.basicConfig(level=logging.INFO, filename='myfile/mylog.log')
logging.info('start the program')
logging.info('begin the func')
1/0
# 上面导致程序中途退出，以下内容不会写入文件
# 这样就可以通过日志查看程序执行到大概哪个地方出错了
logging.info('func end')
logging.info('endind  program')

# 捕捉警告信息
logging.captureWarning(True)

file = open('myfile/template.txt').readlines()
def filegrt(file):
    for line in file:
        yield line
        # 增加空行
        yield '\n'

# 把文本的每一个段落格式化成一个个块
def blocks(file):
    block = []
    for line in filegrt(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []

#for i  in block(file):
#    print(i)

import re, sys

#print('<html><head><head/><title></title><body>')
#title = True

# 对文本进行html转换
# 从命令行的标准输入 < 中读取内容
#for block in block(sys.stdin):
#for block in block(file):
#    # 单独处理每一个块
#    block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
#    if title:
#        print('<h1>')
#        print(block)
#        print('</h1>')
#        title = False
#    else:
#        print('<p>')
#        print(block)
#        print('</p>')

#print('</body></html>')

#from subprocess import Popen, PIPE
#file = open('myfile/out.html', 'w')
#cmd = 'python PythonApplication.py'
#p = Popen(cmd, stdout = file, stderr = PIPE, shell=True)

# 自定义处理类超类，可以通过统一的形式调用各种方法
class Handler:
    def callback(self, pre, name, *args):
        method = getattr(self, pre+name, None)
        if callable(method): return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
       self.callback('end_', name)

    def sub(self, name):
        # match对象由re.sub函数传入
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: return match.group(0)
            return result
        return substitution

class HTMLRenderer(Handler):
  #
  #给文本添加html标记的处理类，可通过超类中的
  #start,end,sub方法进行调用
  #
  def start_document(self):
      print('<html><head></head><title></title><body>')

  def end_document(self):
      print('</body></html>')

  def start_paragraph(self):
      print('<p>')

  def end_paragraph(self):
      print('</p>')

  def start_heading(self):
      print('<h2>')

  def end_heading(self):
      print('</h2>')

  def start_title(self):
      print('<h1>')

  def end_title(self):
      print('</h1>')

  def start_list(self):
      print('<ul>')

  def end_list(self):
      print('</ul>')

  def start_listitem(self):
      print('<li>')

  def end_listitem(self):
      print('</li>')

  def sub_emphasis(self, match):
      return '<em>%s</em>' % match.group(1)

  def sub_url(self, match):
      return '<a href="%s">%s</a>' % (match.group(1), match.group(1))

  def sub_mail(self, match):
      return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))

  def sub_caps(self, match):
      return '<em>%s</em>' % match.group(1)

  def feed(self, data):
        print(data)

import re, sys
# 文本解析器，一个文本可能由标题，段落，列表等组成，可把这些单独分成快
# 针对每个快制定规则并处理，过滤信息,虽然实现这个在一个类中也可以完成
# 但不利于扩展，把文本解析器分成过滤器，规则器，执行器来实现，利于功能
# 的扩展
class Parser:
    def __init__(self, handler):
        self.handler = handler
        self.filters = []
        self.rules = []

    def addFilter(self, pattern, name):
        def filter(block, handler):
            # sub函数可以把匹配到的结果对象传给第二个参数使用
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def addRules(self, rule):
        self.rules.append(rule)

    def parser(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filer in self.filters:
                block = filer(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    if rule.action(block, self.handler): break
        self.handler.end('document')

# 规则的超类，包含一个action方法
class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


# 标题规则
class HeadingRule(Rule):
    #标题最多由70个字符组成，不以冒号结尾
    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ';'

# 题目规则，继承于标题规则类，因为标题规则依然适用于题目规则
class TitleRule(HeadingRule):
    #文本第一个标题当作题目来对待

    type = 'title'
    first = True
    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)

# 列表项规则
class ListItemRule(Rule):
    #以'-'开头的段落为列表项

    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'

    # 不需要列表开头的'-'字符，由自定义的标记替换
    # 所以重写超类中的action方法实现个性化处理
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    #列表是非列表与最后一个列表之间的区段

    type = 'list'
    inside = False

    # 列表可能存在于整个文件中，所以不能遇到列表开头就停止检查
    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and  not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False

# 段落规则
class ParagraphRule(Rule):
    #默认规则，处理不被其他规则处理的块，放在规则列表的最后一位

    type = 'paragraph'
    def condition(self, block):
        return True

# 过滤器的正则表达式
# 强调内容
emphasis = r'\*(.+?)\*'
# url
url = r'(http://[\.a-zA-Z/]+)'
# e-mail
mail = r'([a-zA-Z0-9]+@[\.a-zA-Z]+[a-zA-Z]+)'
# 大写强调
caps = r'([A-Z]+)'

class BasicTextParser(Parser):
    #增加需要的规则器与过滤器

    def __init__(self, handler):
        Parser.__init__(self, handler)
        # 规则判断的顺序很重要，先判断列表，后题目，标题，段落
        self.addRules(ListRule())
        self.addRules(ListItemRule())
        self.addRules(TitleRule())
        self.addRules(HeadingRule())
        self.addRules(ParagraphRule())

        self.addFilter(emphasis, 'emphasis')
        self.addFilter(url, 'url')
        self.addFilter(mail, 'mail')
        self.addFilter(caps, 'caps')

handler = HTMLRenderer()
parser = BasicTextParser(handler)
f=open('myfile/template.txt').readlines()
#parser.parser(sys.stdin)
parser.parser(f)

# reportlab是规则数据的包，还有其他功能丰富的包如PYX
from reportlab.graphics.shapes import Drawing, String, PolyLine
from reportlab.graphics import renderPDF
from reportlab.lib import colors

# d = Drawing(100, 100)
# s = String(50, 50, 'My firest PDF', textAnchor='middle')
# d.add(s)
# renderPDF.drawToFile(d, 'myfile/mypdf.pdf', 'hello PDF')

data = [
    # year mon pre high low
    (2007, 8, 113.2, 114.2, 112.2),
    (2007, 9, 112.2, 115.2, 109.8),
    (2007, 10, 111.0, 116.0, 106.0),
    (2007, 11, 109.8, 116.8, 102.8),
    (2007, 12, 107.3, 115.3, 99.3),
    (2008, 1, 105.2, 114.2, 96.2),
    (2008, 2, 104.1, 114.1, 94.1),
    (2008, 3, 99.9, 110.9, 88.9),
    (2009, 4, 94.8, 106.8, 82.8),
    (2009, 5, 91.2, 104.2, 78.2)
]

# 时间等数据
# 由于画图区域空间不够，所以对数据进行修剪
times = [100*((row[0]+row[1]/12.0) - 2007) for row in data]
pre = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]

# 坐标点数据
preposdata = list(zip(times, pre))
highposdata = list(zip(times, high))
lowposdata = list(zip(times, low))

d = Drawing(300, 300)
# 往绘图对象中添加坐标曲线，结合数据创建矢量图
d.add(PolyLine(preposdata, strokeColor = colors.blue))
d.add(PolyLine(highposdata, strokeColor = colors.red))
d.add(PolyLine(lowposdata, strokeColor = colors.green))
d.add(String(150, 150, 'Sunspots', fillColor = colors.red))

# 写入pdf文件
renderPDF.drawToFile(d, 'myfile/mypdf.pdf', 'sunspots data')

from reportlab.graphics.shapes import Drawing, String, PolyLine
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from urllib.request import urlopen

data = []
comment = '#'
lines = urlopen('http://127.0.0.1:8080/data.txt').readlines()

# 提取数据
for line in lines:
    # 读取到的数据是bytes格式，需要decode转换成string格式
    if not line.isspace() and not str(line.decode()[0]) in comment:
        data.append([float(n.decode()) for n in line.split()])

print(data)
times = [row[0]+row[1]/12.0 for row in data]
pre = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]

preposdata = list(zip(times, pre))
highposdata = list(zip(times, high))
lowposdata = list(zip(times, low))

lp = LinePlot()
# 曲线的开始坐标，x,y轴长度
lp.x = 50
lp.y = 50
lp.width = 300
lp.height = 150
# 给曲线添加数据(x,y),根据列表元素的格数决定曲线的条数
lp.data = [preposdata, highposdata, lowposdata]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

d = Drawing(400, 300)
d.add(lp)
d.add(String(150, 150, 'Sunspots', fillColor = colors.red, fontSize = 15))

# 一般产生的图形对象都可以添加到renderPDF中来产生pdf文件，如wxpython对象
renderPDF.drawToFile(d, 'myfile/mypdf.pdf', 'sunspots data')

# sax不会一次就把xml文档内容读入到内存中, 但dom文件数对象会
# sax对xml使用的是unicode的处理方式
from xml.sax import parse
from xml.sax.handler import ContentHandler

class myXMlHandler(ContentHandler):
    # 标记是否位于某个标签内
    in_headline = False
    def __init__(self, headlines):
        ContentHandler.__init__(self)
        self.headlines = headlines
        self.data = []

    # 遇到开始标签时自动被调用
    def startElement(self, name, attrs):
        #print(name, attrs.keys())
        if name == 'h1':
            self.in_headline = True

    def endElement(self, name):
        if name == 'h1':
            text = ''.join(self.data)
            self.headlines.append(text)
            self.data = []
            self.in_headline = False

    # 进入标签时自动被调用，提取xml文档中所有h1标签中的文本内容
    def characters(self, content):
        if self.in_headline == True:
            self.data.append(content)

headlines = []

# 由于传headlines是可变的对象，相当于传引用，
# 传不可变对象时，如数字，字符串，相当于传值
# a = 1, b = 1刚开始两者指向同一个内存，但如果
# a += 1 后，a就会指向不同的内存，可通过id(a)
# 进行查看
parse('myfile/myxml.xml', myXMlHandler(headlines))
print(headlines)

from xml.sax import parse
from xml.sax.handler import ContentHandler
class myXMlHandler(ContentHandler):
    passthrough = False

    def startElement(self, name, attrs):
        if name == 'page':
            self.passthrough = True
            self.out = open('myfile/'+attrs['name']+'.html', 'w')
            self.out.write('<html><head>\n')
            self.out.write('<title>%s</title>' % attrs['title'])
            self.out.write('\n</head><body>\n')
        elif self.passthrough:
            self.out.write('<'+name)
            for key, val in attrs.items():
                self.out.write(' %s="%s" ' % (key, val))
            self.out.write('>')


    def endElement(self, name):
        if name == 'page':
            self.passthrough = False
            self.out.write('\n</body></html>')
            self.out.close()
        elif self.passthrough:
            self.out.write('</%s>' % name)

    def characters(self, content):
        if self.passthrough:
            self.out.write(content)

parse('myfile/myxml.xml', myXMlHandler())

from xml.sax import parse
from xml.sax.handler import ContentHandler
import os

# 分三个层次解析xml，ContentHandler->Dispatcher->myXMlHandler
# 按抽象程度开始写

# 分发功能类
class Dispatcher:
    def dispatch(self, prefix, name, attrs=None):
        # capitalize首字母大写
        dname = 'default' + prefix.capitalize()
        method = getattr(self, prefix+name.capitalize(), None)
        if callable(method): args = ()
        else:
            method = getattr(self, dname, None)
            # 定义一个元组入参，结束标签不需要attrs入参
            args = name,
        if prefix == 'start': args += attrs,
        if callable(method): method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    def endElement(self, name):
       self.dispatch('end', name)

# 具体实现类
# 先继承于Dispatcher，因为要使用的是Dispatcher类中的start与end方法
class myXMlHandler(Dispatcher, ContentHandler):
    # 是否位于page标签内
    passthrough = False
    def __init__(self, *args):
        self.directory = [args[0]]
        self.ensureDirectory()

    def ensureDirectory(self):
        # 以路径符把路径连接起来，如*['path', 'subpath']->path//subpath
        path = os.path.join(*self.directory)
        if not os.path.isdir(path): os.makedirs(path)

    def startDirectory(self, attrs):
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    def endDirectory(self):
        # 弹出进入的目录，相当于返回上一层目录
        self.directory.pop()

    def startPage(self, attrs):
        self.passthrough = True
        self.out = open(os.path.join(*self.directory + [attrs['name'] + '.html']), 'w')
        self.writeHeader(attrs)

    def endPage(self):
       self.wriFooter()
       self.out.close()
       self.passthrough = False

    def writeHeader(self, attrs):
         self.out.write('<html>\n<head>\n')
         self.out.write('当前位置:'+'/'.join(self.directory))
         self.out.write('<title>%s</title>' % attrs['title'])
         self.out.write('\n</head>\n<body>\n')

    def wriFooter(self):
        self.out.write('\n</body>\n</html>')

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<'+name)
            for key, val in attrs.items():
                self.out.write(' %s="%s" ' % (key, val))
            self.out.write('>')

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write('</%s>' % name)

    def characters(self, content):
        if self.passthrough: self.out.write(content)

parse('myfile/myxml.xml', myXMlHandler('myfile/html'))

#from nntplib import *
#s = NNTP('web.aioe.org')
#(resp, count, first, last, name) = s.group('comp.lang.python')
#(resp, subs) = s.xhdr('subject', (str(first)+'-'+str(last)))
#for subject in subs[-10:]:
#  print(subject)
#number = input('Which article do you want to read? ')
#(reply, num, id, list) = s.body(str(number))
#for line in list:
#  print(line)

# 新闻组信息获取模块
from nntplib import NNTP
import time
import datetime
#yesterday = time.time() - 24*60*60
#yesterday = time.localtime(yesterday)

#date = time.strftime('%y%m%d', yesterday)
#hour = time.strftime('%H%M%S', yesterday)
# 十天以前
yesterday = datetime.date.today() + datetime.timedelta(days = -4)

servername = 'web.aioe.org'
group = 'comp.lang.python.announce'
# 向NNTP服务器发送一条newnews指令
server = NNTP(servername)
# 获取全部新闻组信息
(resp, count, first, last, name) = server.group(group)
# 获取指定日期之后的新闻组信息，ids为文章ID
(resp, ids) = server.newnews(group, yesterday)
body = server.body('<mailman.355.1541073920.2799.python-announce-list@python.org>')[1].lines
print(body)

subject = []
for id in ids:
    (resp, ArticleInfoObj) = server.head(id)
    for line in ArticleInfoObj.lines:
        if line.lower().startswith(b'subject:'):
            subject = line[9:]
            break
    body = server.body(id)[1].lines

    print(subject)
    print('-'*len(subject))
    print('\n'.join([b.decode() for b in body]))

from nntplib import NNTP
import datetime
import re
from email import message_from_string
from urllib.request import urlopen

# 新闻获取：多个新闻发布源->新闻代理：1.获取所有发布源的新闻信息并统一格式化(title:body) 2.新闻信息发布到多个目标文件(纯文本,html文件等)

# 新闻代理
class NewsAgent:
    def __init__(self):
        self.sources = []
        self.destinations = []

    # 添加新闻源
    def addSource(self, source):
        self.sources.append(source)

    # 添加发布目标
    def adddes(self, des):
        self.destinations.append(des)

    # 发布到文件
    def distribute(self):
        items = []
        for source in self.sources:
            items.extend(source.getItems())

        for des in self.destinations:
            des.releaseItems(items)

# 定义新闻信息结构(title:body)
class NewItems:
    def __init__(self, title, body):
        self.title = title
        self.body = body

# nntp服务器获取新闻
class NNTPSource:
    def __init__(self, servername, group, newstime):
        self.servername = servername
        self.group = group
        self.newstime = newstime

    # 获取新闻title与Body信息
    def getItems(self):
        server = NNTP(self.servername)
        (resp, ids) = server.newnews(self.group, self.newstime)

        for id in ids:
            (resp, artitle) = server.article(id)
            # 欧洲语言大多使用此编码方式
            msg = message_from_string('\n'.join([n.decode('ISO-8859-15') for n in artitle.lines]))
            # 根据subject关键字获取title
            title = msg['subject']
            body = msg.get_payload()
            # bdoy信息包含多个部分时，只取第一部分
            if msg.is_multipart():
                body = body[0]

            # 保存获取的信息
            yield NewItems(title, body)
        # 释放连接
        server.quit()

# 其他新闻网站获取新闻
class OtherWebSource:
    def __init__(self, url, titleExp, bodyExp):
        self.url = url
        self.titleExp = titleExp
        self.hrefExp = bodyExp

    def getItems(self):
        file = urlopen(self.url).read().decode('utf-8')
        titles = self.titleExp.findall(file)
        hrefs= self.hrefExp.findall(file)

        bodyExp = re.compile(r'(?s)<!--mainContent begin-->.*?<p>(.*)</p>.*?<!--mainContent end-->')
        f = urlopen('http://culture.ifeng.com/a/20181104/60143811_0.shtml').read().decode('utf-8')

        bodys = []

        for href in hrefs:
            f = urlopen(href).read().decode('utf-8')
            f = bodyExp.findall(f)
            bodys.append(''.join([str(n) for n in f]))

        for title, body in list(zip(titles, bodys)):
            yield NewItems(title, body)

# 发布为纯文本格式
class TextDes:
    def __init__(self, filename):
        self.filename = filename
    def releaseItems(self, items):
        f = open(self.filename, 'w')
        for item in items:
            print(item.title, file=f)
            print('-'*len(item.title)*3, file=f)
            print(item.body, file=f)
        #f.close()


# 发布为Html格式
class HtmlDes:
    def __init__(self, filename):
        self.filename = filename

    def releaseItems(self, items):
        # 以utf-8方式打开，否则报''gbk'' codec can't decode byte，因为文件是以gbk方式保存的
        f = open(self.filename, 'w', encoding='utf-8')
        print('<html>\n<head>\n<title>News</title>\n</head>\n<body>', file=f)
        print('<h2>\n', file=f)
        print('<ul>', file=f)

        # 新闻标题列表
        id = 0;
        for item in items:
            id += 1
            print('<li><a href="#%d">%s</a></li>' % (id, item.title), file=f)

        print('</ul>', file=f)
        print('</h2>', file=f)

        # 标题及正文
        id = 0;
        for item in items:
            id += 1
            print('<h2 id="%d">%s</h2><p>%s</p>' % (id, item.title, item.body), file=f)
            #f.write('<h2 id="%d">%s</h2><p>%s</p>' % (id, item.title, item.body))

        print('\n</body>\n</html>', file=f)

        #f.close()

# 主函数
def runDefaultSetup():

    newsAgent = NewsAgent()

    # 添加以nntp方式获取的新闻源
    newstime = datetime.date.today() + datetime.timedelta(days=-4)
    nntp = NNTPSource(servername='web.aioe.org', group='comp.lang.python.announce', newstime=newstime)

    newsAgent.addSource(nntp)

    # 添加以url方式获取的新闻源
    url = 'http://culture.ifeng.com/'
    # 前瞻：
    # exp1(?=exp2) 查找exp2前面的exp1
    # 后顾：
    # (?<=exp2)exp1 查找exp2后面的exp1
    # 负前瞻：
    # exp1(?!exp2) 查找后面不是exp2的exp1
    # 负后顾：
    # (?<!=exp2)exp1 查找前面不是exp2的exp1
    # (?:)分组不会被保存起来
    titleExp = re.compile(r'(?<=<h2>)\s*<a href=".*?shtml" target="_blank">(.*?)</a>\s*(?=</h2>)')
    bodyExp = re.compile('(?<=<h2>)\s*<a href="(.*?shtml)" target="_blank">.*?</a>\s*(?=</h2>)')

    otherWeb = OtherWebSource(url, titleExp, bodyExp)

    newsAgent.addSource(otherWeb)

    # 添加目标处理对象
    newsAgent.adddes(HtmlDes('myfile/news.html'))

    newsAgent.distribute()

runDefaultSetup()
# 待扩充1.使用smtplib模块把新闻当作邮件来发送；2.根据命令行参数(getopt,optparse模块)决定新闻格式
3.发布新闻为xml文件；4.发布为cgi脚本

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

port = 1025
# 会话服务器
class Chatserver(dispatcher):
    def __init__(self, port):
        dispatcher.__init__(self)
        # 创建套接字
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置重用地址机制，服务器重启后能快速绑定到之前的端口上
        self.set_reuse_addr()
        # ''默认绑定本机IP
        self.bind(('', port))
        self.listen(5)
        # 初始化回话列表
        self.sessions = []
        self.name = 'Chatserver'
        self.users = {}
        self.mainroom = ChatRoom(self)

    def handle_accept(self):
        conn, clientaddr = self.accept()
        #self.sessions.append(Chatsession(self, conn))
        Chatsession(self, conn)

    # 一个会话断开连接后将其从会话列表中删除
    def disconnect(self, session):
        self.sessions.remove(session)

    # 将一个会话用户发送给服务器的内容广播给其他会话用户
    def broadcast(self, line):
        for session in self.sessions:
            session.push(line+'\r\n')

# 新建一个会话对象
class Chatsession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        # 设定读取数据中止字符
        self.set_terminator('\r\n')
        self.server = server
        self.data = []
        self.name = None
        # push方法用于向会话用户推送消息
        #self.push(bytes('welcome to %s\r\n' % server.name, encoding='utf-8'))
        self.enter(LogingRoom(server))

    def enter(self, room):
        # 登录后把登录会话移动到主会话列表中
        # 因为登录成功后已经不需要保存登录的会话了
        try: cur = self.room
        except AttributeError: pass
        else: cur.remove(self)
        self.room = room
        room.add(self)

    # 接收到的数据数量到一定程度时，会自动被调用
    def collect_incoming_data(self, data):
        self.data.append(data)

    # 读到设定的换行符时自动被调用
    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        #self.server.broadcast(line)
        try: self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        #self.server.disconnect(self)
        self.enter(LogoutRoom(self.server))

# 用户命令处理
class CommandHandler:
    def unknown(self, session, cmd):
        session.push(bytes('Unknown command: %s' % cmd, encoding='utf-8'))

    def handle(self, session, line):
        if not line.strip(): return
        # 命令格式为 cmd msg，所以使用一个分隔符来区分
        parts = line.split(' ', 1)
        cmd = parts[0]
        try: line = parts[1].strip()
        except IndexError: line = ''
        method = getattr(self, 'do_'+cmd, None)
        try: method(session, line)
        except TypeError: self.unknown(session, cmd)

# 自定义处理登出
class EndSession(Exception): pass

# 会话处理 超类
class Room(CommandHandler):
    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def brocast(self, line):
        for session in self.sessions:
            session.push(bytes(line, encoding='utf-8'))

    def do_logout(self, session, line):
        raise EndSession

# 主会话列表
class ChatRoom(Room):
    def add(self, session):
        # 广播给会话列表中的所有用户，告知当前登录用户
        self.brocast(bytes(session.name + 'has entered the room.\r\n', encoding='utf-8'))
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, sesssion):
        Room.remove(self, sesssion)
        self.brocast(bytes(sesssion.name + 'has left the room.\r\n', encoding='utf-8'))

    def do_say(self, session, line):
        self.brocast(bytes(session.name + ':' + line + '\r\n', encoding='utf-8'))

    def do_look(self, session):
        for other in self.sessions:
            session.push(other.name + '\r\n')

    def do_who(self, session):
        for name in self.server.users:
            session.push(bytes(name + '\r\n', encoding='utf-8'))

# 登录处理
class LogingRoom(Room):
    def add(self, session):
        Room.add(self, session)
        session.push(bytes('Welcom to %s\r\n' % self.server.name, encoding='utf-8'))

    def unknown(self, session, cmd):
        session.push(bytes('Please login\nUse "login <nick>"\r\n', encoding='utf-8'))

    def remove(self, sesssion):
        Room.remove(self, sesssion)

    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.push(bytes('Pleases input your name' + '\r\n', encoding='utf-8'))
        elif name in self.server.users:
            session.push(bytes('The name "%s" is taken' % name, encoding='utf-8'))
        else:
            # 登录成功后将其加入主会话列表
            session.name = name
            session.enter(self.server.mainroom)

# 登出处理
class LogoutRoom(Room):
    def add(self, session):
        try: del self.server.users[session.name]
        except KeyError: pass

server = Chatserver(port)

try: asyncore.loop()
# 在命令行按住强制停止键(如ctrl+c)时，会产生异常，在这里手动捕捉，
# 回收堆栈跟踪垃圾
except KeyboardInterrupt: pass

import psycopg2
conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()
cursor.execute('select * from messages')
names = [d[0] for d in cursor.description]
rows = [dict(zip(names, row)) for row in cursor.fetchall()]
print(rows)

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
from os.path import isfile, join
from urllib.parse import urlparse

# 自定义一些返回值
OK = 1
FAIL = 2
# 由于ServerProxy请求的SimpleXMLRPCServer不能返回None
EMPTY = ''
# 定义最多寻找多少个节点，节点中间的联系点一般不超过6个
MAX_FIND_NODE = 6

# 从命令行参数中提取port
def getPort(url):
    ipPort = urlparse(url)[1]
    ll = ipPort.split(':')
    return int(ll[-1])


# 定义一个P2P网络中的节点，功提供给对外查询的功能并返回数据
class Node:
    # 一个节点包含文件存放目录，节点地址，查询文件方法，将请求广播至其它节点的基本要素
    def __init__(self, url, dirname, secret):
        self.url = url
        self.secret = secret
        self.dirname = dirname
        self.known = set()

    # 查询文件主功能，查询顺序为本地->网络中的其它已知节点
    def query(self, query, history = []):
        # 先从本机开始查询文件
        code, data = self._handle(query)
        if code == OK:
            return OK, data
        else:
            history = history + [self.url]
            # 如果寻找超过最大寻找节点数，则停止查找
            if len(history) > MAX_FIND_NODE:
                return FAIL, EMPTY
            # 请求发送到其它节点
            return self._brocast(query, history)

    # 把已知节点传播其它节点
    def hello(self, other):
        self.known.add(other)
        return OK

    # 寻找节点文件并写入本地文件
    def fetch(self, query, secret):
        # 校验节点密语
        if secret != self.secret: return FAIL
        code, data = self.query(query)
        if code == OK:
            f = open(join(self.dirname, query), 'w')
            f.write(data)
            f.close()
            return OK
        else:
            return FAIL


    # 将自身注册为服务器的特性,并开启服务器
    def _start(self):
        server = SimpleXMLRPCServer(('', getPort(self.url)))
        # 注册特性
        server.register_instance(self)
        # 注册方法
        #server.register_function(func)
        server.serve_forever()

    # 提取内部文件,该方法不对其它节点开放
    def _handle(self, query):
        file = join(self.dirname, query)
        if not isfile(file): return FAIL, EMPTY
        return OK, open(file).read()

    def _brocast(self, query, history):
        # 遍历拷贝的副本，由于遍历真实的节点可能会对节点产生不必要的操作
        for other in self.known.copy():
            if other in history: continue
            try:
                # 获取服务器的实例，这样也就获取了服务器中注册的实例或者方法
                server = ServerProxy(other)
                code, data = server.query(query, history)
                if code == OK:
                    return code, data
            # 如果节点不能访问，则不必要记录该节点，避免下一个节点重复该节点
            except:
                self.known.remove(other)
        return FAIL, EMPTY

url, directory, secret = sys.argv[1:]
node = Node(url, directory, secret)
node._start()

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy, Fault
import sys
from os.path import isfile, join, abspath
from urllib.parse import urlparse

# 服务器重启后可以立即使用断开前的端口
SimpleXMLRPCServer.allow_reuse_address = True

# 自定义一些返回异常
UNHANDLE = 100
ACCESS_DENIED = 200

# 无法查询异常
class UnhandledQuery(Fault):
    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLE, message)

# 访问不在指定的目录中的文件时返回的异常，
# 因为客户端可能指定../filename之类的文件名去访问非指定的目录下的文件
class AccessDenied(Fault):
    def __init__(self, message="Access Denied"):
        Fault.__init__(self, ACCESS_DENIED, message)

# 判断指定文件夹中是否有指定文件，文件名包含完整路径的文件名
def inside(dir, fullfilename):
    dir = abspath(dir)
    filename = abspath(fullfilename)
    return filename.startswith(join(dir, ''))

# 定义最多寻找多少个节点，节点中间的联系点一般不超过6个
MAX_FIND_NODE = 6

# 从命令行参数中提取port
def getPort(url):
    ipPort = urlparse(url)[1]
    ll = ipPort.split(':')
    return int(ll[-1])


# 定义一个P2P网络中的节点，功提供给对外查询的功能并返回数据
class Node:
    # 一个节点包含文件存放目录，节点地址，查询文件方法，将请求广播至其它节点的基本要素
    def __init__(self, url, dirname, secret):
        self.url = url
        self.secret = secret
        self.dirname = dirname
        self.known = set()

    # 查询文件主功能，查询顺序为本地->网络中的其它已知节点
    def query(self, query, history = []):
        # 先从本机开始查询文件
        try: return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            # 如果寻找超过最大寻找节点数，则停止查找
            if len(history) >= MAX_FIND_NODE:
                # 重抛异常
                raise
            # 请求发送到其它节点
            return self._brocast(query, history)

    # 把其它节点添加到已知节点，可能会遍历这些节点寻找文件
    def hello(self, other):
        self.known.add(other)
        return 0

    # 寻找节点文件并写入本地文件
    def fetch(self, query, secret):
        # 校验节点密语
        if secret != self.secret: return ACCESS_DENIED
        result = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    # 将自身注册为服务器的特性,并开启服务器
    def _start(self):
        server = SimpleXMLRPCServer(('', getPort(self.url)), logRequests=False)
        # 注册特性
        server.register_instance(self)
        # 注册方法
        #server.register_function(func)
        server.serve_forever()

    # 提取内部文件,该方法不对其它节点开放
    def _handle(self, query):
        file = join(self.dirname, query)
        if not isfile(file): raise UnhandledQuery
        if not inside(self.dirname, file): raise ACCESS_DENIED
        return open(file).read()

    def _brocast(self, query, history):
        # 遍历拷贝的副本，由于遍历真实的节点可能会对节点产生不必要的操作
        for other in self.known.copy():
            if other in history: continue
            try:
                # 获取服务器的实例，这样也就获取了服务器中注册的实例或者方法
                server = ServerProxy(other)
                return server.query(query, history)
            # 如果节点不能访问，则不必要记录该节点，避免下一个节点重复访问该节点
            except Fault as f:
                if f.faultCode == UNHANDLE: pass
                else:
                    self.known.remove(other)
            except:
                # 如果不能访问该节点，下一次就不再遍历该节点了
                self.known.remove(other)
        raise UnhandledQuery
#---------------------------------------------------------------------------
# 基于cmd界面的node控制器界面
from xmlrpc.client import ServerProxy, Fault
import string
from random import choice
from myfile.p2pServer import Node, UNHANDLE
from threading import Thread
from time import sleep
import sys
from cmd import Cmd

HEAD_START = 0.1
SECRET_LENGTH = 100

# 获取指定长度的随机字母
def randomStr(length):
    chars = []
    while length > 0:
        length -= 1
        chars.append(choice(string.ascii_lowercase))
    return ''.join(chars)

class Client(Cmd):
    # 自定义命令提示符
    prompt = '>'

    def __init__(self, url, dirname, urlfile):
        # 自身初始化Cmd超类，包括初始化其prompt特性
        Cmd.__init__(self)
        self.secret = randomStr(SECRET_LENGTH)
        node = Node(url, dirname, self.secret)
        # 放入线程中
        thread_node = Thread(target=node._start)
        # 创建守护进程(不受终端控制的进程，ctrl+c强制停止不会对之生效，只有调用sys.exit)
        thread_node.setDaemon(1)
        # 启动线程
        thread_node.start()
        # 让服务起来后再启动客户端程序
        sleep(HEAD_START)
        self.server = ServerProxy(url)

        # 取节点列表并发送到下一节点
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)

    # 在命令行输入fetch filename(arg)的时候会被调用
    def do_fetch(self, arg):
        try:
            self.server.fetch(arg, self.secret)
        except Fault as f:
            if f.faultCode != UNHANDLE: raise
            print("Couldn't find the file: ",arg)
        except ConnectionRefusedError:
            print("")

    def do_query(self, arg):
        try:
            result = self.server.query(arg)
            print(result)
        except Fault as f:
            if f.faultCode != UNHANDLE: raise
            print("Couldn't find the file: ",arg)

    def do_exit(self, arg):
        print()
        sys.exit()

    do_EOF = do_exit

def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.cmdloop()

if __name__ == '__main__': main()

# 基于wxPython界面的node控制器界面
from xmlrpc.client import ServerProxy, Fault
import string
from random import choice
from myfile.p2pServer import Node, UNHANDLE
from threading import Thread
from time import sleep
from os import listdir
import sys
import wx

HEAD_START = 0.1
SECRET_LENGTH = 100

def randomStr(length):
    chars = []
    while length > 0:
        length -= 1
        chars.append(choice(string.ascii_lowercase))
    return ''.join(chars)

# 扩展Node，增加一个列出共享目录下文件列表的方法
class ListTableNode(Node):
    def list(self):
        return listdir(self.dirname)
    def listKnownNode(self):
        return list(self.known)

class Client(wx.App):
    def __init__(self, url, dirname, urlfile):
        # 不能在开头就创建GUI，因为创建过程中调用的updateList使用到self.server
        # 而这个特性是在后面添加的
        #super(Client, self).__init__()

        self.secret = randomStr(SECRET_LENGTH)
        #node = Node(url, dirname, self.secret)
        node = ListTableNode(url, dirname, self.secret)
        # 放入线程中
        thread_node = Thread(target=node._start)
        # 创建守护进程(不受终端控制的进程，ctrl+c强制停止不会对之生效，只有调用sys.exit)
        thread_node.setDaemon(1)
        # 启动线程
        thread_node.start()
        # 让服务起来后再启动客户端程序
        sleep(HEAD_START)
        self.server = ServerProxy(url)

        # 取节点列表并发送到下一节点
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)

        super(Client, self).__init__()

    # 用服务器的数据更新文件列表框
    def updateList(self):
        self.files.Set(self.server.list())

    def updateNodelist(self):
        self.nodes.Set(self.server.listKnownNode())

    # 在对象被创建后自动执行
    def OnInit(self):
        win = wx.Frame(None, title="p2p Client", pos = (500, 200), size=(400,300))
        bkg = wx.Panel(win)

        self.input = input = wx.TextCtrl(bkg)
        self.submit = submit = wx.Button(bkg, label="获取", size=(80,25))
        submit.Bind(wx.EVT_BUTTON, self.fetchHandler)

        hbox = wx.BoxSizer()
        hbox.Add(input, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
        hbox.Add(submit, flag=wx.TOP|wx.BOTTOM|wx.RIGHT, border=10)

        self.files = files = wx.ListBox(bkg)
        self.updateList()

        self.nodes = nodes = wx.ListBox(bkg)
        self.updateNodelist()

        hboxlist = wx.BoxSizer()
        hboxlist.Add(files, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
        hboxlist.Add(nodes, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND)
        vbox.Add(hboxlist, proportion=1, flag=wx.EXPAND)

        bkg.SetSizer(vbox)

        win.Show()

        return True

    def fetchHandler(self, event):
        query = self.input.GetValue()

        try:
            self.submit.SetLabelText('下载中...')
            self.server.fetch(query, self.secret)
            self.submit.SetLabelText('获取')
            self.updateList()
        except Fault as f:
            if f.faultCode != UNHANDLE: raise
            print("Couldn't find the file: ", query)

def main():
    #urlfile, directory, url = sys.argv[1:]
    url = 'http://127.0.0.1:1025'
    directory = 'myfile'
    urlfile = 'myfile/urlfile.txt'
    client = Client(url, directory, urlfile)
    client.MainLoop()

#if __name__ == '__main__': main()
main()

# SimplePygame
# 模块内置的其他功能参考https://www.pygame.org/docs
import sys, pygame
from pygame.locals import *
from random import randrange

class Weight(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 获取图片的矩形区域
        self.image = weight_image
        self.rect = self.image.get_rect()
        self.reset()

    # 移动到屏幕顶部的随机位置
    def reset(self):
        self.rect.top = -self.rect.height
        self.rect.centerx = randrange(screen_size[0])

    # 使图像移动往下移动
    def update(self):
        self.rect.top += 1
        # 图像的上部分移动到底部后继续从顶部开始移动
        if self.rect.top > screen_size[1]:
            self.reset()

pygame.init()
screen_size = (800, 600)
pygame.display.set_mode(screen_size, RESIZABLE)
pygame.mouse.set_visible(0)

# 载入图像(Surface对象)
weight_image = pygame.image.load('E:/picture/16tt.png')
# 转换成适应屏幕显示的类型
weight_image = weight_image.convert()

# 创建一个图像对象组，可以包含多个图像对象
sprites = pygame.sprite.RenderUpdates()
sprites.add(Weight())

# 获取屏幕表面并填充自定义颜色
screen = pygame.display.get_surface()
bg = (255, 255, 255)
screen.fill(bg)
pygame.display.flip()

# 从屏幕上清除图像，以便显示下一帧(用白色填充)
def clear_callback(surf, rect):
    surf.fill(bg, rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

    # 清除前面的位置
    sprites.clear(screen, clear_callback)

    # 更新并显示下一帧的图像，会调用组中所有对象的update方法
    sprites.update()

    # 获取图形对象组中的绘图信息，以矩形列表返回
    updates = sprites.draw(screen)

    # 更新部分屏幕内容
    pygame.display.update(updates)

import pygame, os
from pygame.locals import *
from random import randrange
import sys
sys.path.append('E:\hexo\source.Olaful.github.io\Olaful.github.io\python\PythonApplication\PythonApplication\myfile')
import config

# 游戏从开始到结束状态
# 欢迎界面->游戏信息界面->游戏中界面->静止界面->游戏界面->静止界面

# 所有图形对象的超类
class SquishSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        shrink = -config.margin * 2
        # 获取填充后的区域，负数表示缩小矩形
        self.area = screen.get_rect().inflate(shrink, shrink)

# 秤砣对象
class Weight(SquishSprite):
    def __init__(self, speed):
        super().__init__(config.weight_image)
        self.speed = speed
        self.reset()

    def reset(self):
        x = randrange(self.area.left, self.area.right)
        self.rect.midbottom = x, 0

    def update(self):
        self.rect.top += self.speed
        self.landed = self.rect.top > self.area.bottom

# 香蕉对象
class Banana(SquishSprite):
    def __init__(self):
        SquishSprite.__init__(self, config.banana_image)
        self.rect.bottom = self.area.bottom
        self.pad_top = config.banana_pad_top
        self.pad_size = config.banana_pad_size

    def update(self):
        # 中心点定位到鼠标指针的坐标
        self.rect.centerx = pygame.mouse.get_pos()[0]
        # clamp方法能将一个矩形区域限定在另一个矩形里面，这样图像就不会
        # 溢出边界
        self.rect = self.rect.clamp(self.area)

    def touches(self, other):
            # 判断图形对象是否与其他图形对象有重叠
            bounds = self.rect.inflate(-self.pad_size, -self.pad_top)
            bounds.bottom = self.rect.bottom
            return bounds.colliderect(other.rect)

# 游戏的主要逻辑

# 游戏状态操作
class State:
    # 响应事件
    def handle(self, event):
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

    def firstDisplay(self, screen):
        # 第一次的显示状态
        screen.fill(config.bg_color)
        # 更新surface到屏幕
        pygame.display.flip()

    # 用于子类重写
    def display(self, screen):
        pass

# 游戏等级，显示游戏图像，及图像的位置变化
class Level(State):
    def __init__(self, number = 1):
        self.number = number
        self.remaining = config.weights_per_level
        speed = config.drop_speed
        # 等级的增加意味着速度的增加
        speed += (self.number - 1) * config.speed_increase
        self.weight = Weight(speed)
        self.banana = Banana()
        both = self.weight, self.banana
        self.sprites = pygame.sprite.RenderUpdates(both)

    def update(self, game):
        # 从前一帧更新游戏对象位置(向下移动)
        self.sprites.update()
        # 如果两个游戏对象有重叠，则游戏结束
        if self.banana.touches(self.weight):
            game.nextState = GameOver()
        # 如果秤砣对象落地，则重置状态，剩余要落下的秤砣数量减1
        # 落完后进入下一等级
        elif self.weight.landed:
            self.weight.reset()
            self.remaining -= 1
            if self.remaining == 0:
                game.nextState = LevelCleared(self.number)

    # 根据提供矩形信息列表更新画面(达到更新部分画面的目的
    def display(self, screen):
        screen.fill(config.bg_color)
        updates = self.sprites.draw(screen)
        pygame.display.update(updates)

# 静止界面
class Paused(State):
    finished = 0
    imge = 'E:/picture/jiaohuang.jpg'
    text = 'continue(keydown, mousebuttondown)\ngameover(esc)'

    def handle(self, event):
        # 响应事件，以及设置当前状态是否结束
        State.handle(self, event)
        if event.type in [MOUSEBUTTONDOWN, KEYDOWN]:
            self.finished = 1

    def update(self, game):
        # 当前状态结束，则切换到下一个状态
        if self.finished:
            game.nextState = self.nextState()

    def firstDisplay(self, screen):
        # 绘制暂停状态的页面
        # 先使用背景色清空屏幕
        screen.fill(config.bg_color)

        # 获取字体对象
        font = pygame.font.Font(None, config.font_size)
        lines = self.text.strip().splitlines()
        # 获取文本占用的高度
        height = len(lines) * font.get_linesize()

        # 放置文本的位置
        center, top = screen.get_rect().center
        top -= height // 2

        # 绘制图片
        if self.imge:
            image = pygame.image.load(self.imge).convert()

            r = image.get_rect()
            top += r.height // 2
            r.midbottom = center, top - 20
            # 将图片放置在屏幕上确定的位置
            screen.blit(image, r)

        # 光滑的黑色字体
        antialias = 1
        fontcolor = 0, 0, 0

        # 绘制文本
        for line in lines:
            tt = font.render(line.strip(), antialias, fontcolor)
            r = tt.get_rect()
            r.midtop = center, top
            screen.blit(tt, r)
            top += font.get_linesize()

        pygame.display.flip()

# 暂停状态显示的游戏信息
class Info(Paused):
    nextState = Level
    text = 'your should aviod the falling weights '

# 欢迎界面信息
class Startup(Paused):
    nextState = Info
    imge = config.splash_image
    text = 'Welcome to Game\nthe game of Self-Defense'

# 过关提示信息并切换到下一等级
class LevelCleared(Paused):
    def __init__(self, number):
        self.number = number
        self.text = 'Level %i Cleared, Click to start next level' % self.number

    def nextState(self):
        return Level(self.number+1)

# 游戏结束提示信息
class  GameOver(Paused):
    # 结束后从第一等级开始
    nextState = Level
    text = 'Game Over\nClick to Restart, Esc to Quit'

# 游戏主对象，负责切换游戏状态
class Game:
    def __init__(self, *args):
        #path = os.path.abspath(args[0])
        #dir = os.path.split(path)[0]
        # 切换工作环境目录
        #os.chdir(dir)
        self.state = None
        self.nextState = Startup()

    def run(self):
        # 初始化pygame模块
        pygame.init()
        # 窗口模式
        flag = 0

        if config.full_screen:
            flag = FULLSCREEN

        screen_size = config.screen_size
        screen = pygame.display.set_mode(screen_size, flag)

        pygame.display.set_caption('Hello Game')
        pygame.mouse.set_visible(False)

        while True:
            # 在不同的状态间进行切换并显示当前状态页面
            # 各个状态对象是以链表的形式关联在一起的
            if self.state != self.nextState:
                self.state = self.nextState
                self.state.firstDisplay(screen)

            # 监控鼠标键盘事件，用于状态的切换
            for event in pygame.event.get():
                self.state.handle(event)

            # 更新显示当前状态
            self.state.update(self)
            self.state.display(screen)

Game().run()

s = '*Hel Lo*2 world'
# 返回max(len(s), with)长度使用给定字符(单字符)填充两边的字符串
ss = s.center(10, '*')

# 搜索指定范围内子字符串出现的次数
cnt = s.count('ll', 0, len(s))

# 以gbk方式进行编码，错误处理方式为strict
# 以之对应的是decode
ss = s.encode('gbk', errors='strict')
# 指定范围内字符串是否以指定字符结尾，范围不含end，startswith则是是否以以指定字符开头
b = s.endswith('e', 0, 2)

# 返回子字符串出现的位置，找不到返回-1, index方法则引发ValueError异常
i = s.find('el', 0, 3)
# 检查字符串是否由数字或字母构成
c = s.isalnum()
# 检查字符串是否全部由字母组成
c = s.isalpha()
# 检查字符串是否全部由数字组成
c = s.isdigit()
# 检查字符串是否全部由小写组成
c = s.islower()
# 检查字符串是否全部由大写组成
c = s.isupper()
# 检查字符串是否全部由空格组成
c = s.isspace()
# 检查字符串中的单词是否全部由大写字母开头组成
c = s.istitle()
# 返回max(len(s), with)长度使用给定字符(单字符)填充右边的字符串, rjust则填充左边
ss = s.ljust(10, '*')
# 字符串全部变成小写后返回，upper则相反
ss = s.lower()
# 返回删除左边的所有指定字符后的字符串，rstrip则是删除右边，strip则删除两边
ss = s.lstrip('*')
# 搜索指定子字符串并且返回指定字符串与其左边与其右边组成的列表，rpartition则从左边开始搜索
ss = s.partition('Lo')
# 替换指定内容后返回
ss = s.replace(r'*', '!')
# 返回子字符串出现的位置，找不到返回-1, rindex方法则引发ValueError异常
f = s.rfind('*', 0, len(s))
# 从右边开始以指定字符分割max个部分并以列表返回
l = s.rsplit('*', 1)
# 以行分隔符分割字符串并以列表返回
l = s.splitlines()
# 字符串中所有字母大小写反转后返回
ss = s.swapcase()
# 字符串中所有单词首字母变成大写后返回
ss = s.title()
# 左边填充width - len(s)个0
ss = s.zfill(20)

# 断言，为假则抛错
#assert 1 > 2,'error info'

x=2
y=3
# 三元表达式，如果条件成立则'hello', 否则'world'
z = 'hello' if x > y else 'world'

# 实现抽象类的模块
import abc

# 抽象类：所有子类中必须全部实现超类中@abc.abstractmethod修饰的方法，
# 只要在所有子类中找到全部被修饰的方法就可以了，不要其中任何一个子类
# 全部重写,否则抛NotImplementedError异常
class parClass(abc.ABC):
    # 声明元类为ABCMeta类,
    #__metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def func1(self):
        return

    @abc.abstractmethod
    def func2(self):
        return

class subcls1(parClass):
    def func1(self):
        return '1'

    def func2(self):
        return '2'

class subcls2(parClass):
    def func1(self):
        return '1'

c1 = subcls1()
# 由于subcls2没有实现func2方法，无法实例化
#c2 = subcls2()

g = 1
def func():
    # 指出其为全局变量后方可修改，访问则不需要指出
    global g
    # 定义全局变量，函数退出后不销毁
    global gg
    g += 1
    print(g)

    l = 0
    ll = 0

    def funcc():
        # 指出引用外层变量，前提是外层变量存在，否则不可以引用
        nonlocal l
        # 指出为全局变量的话外层必需有定义
        global ll

        l += 1
#func()

# *b会收集剩下的内容
a,*b,c,d = [1,2,3,4,5]
# 字典推导式
d = {i:i for i in range(5)}

# 按key来升序排序，key也可以是自定义外部函数
l = [(4,'a'), (4,'b'), (8,'b')]
l.sort(key = lambda l: l[0], reverse = False)

from operator import itemgetter
# 多级排序
l.sort(key = itemgetter(0,1))

s = 'hello\n world'
# 字符串原样表示
repr(s)
# 对特殊字符会进行转义，如\n转义为换行符
str(s)

# 字符串缓存，操作方法基本和open一样，有read,readlines等
from io import StringIO
s = StringIO()
s.write('hello world')
s = s.getvalue()
print(s)
"""
#---------------------------------------------------------------------------
# web scrap
# robots.txt可以察看网站允许的访问方式
# sitemap可以察看网站地图
import builtwith
# 解析网站使用的框架等
result = ''
#result = builtwith.parse('http://example.webscraping.com/')

import whois
# 察看网站所有者
#result = whois.whois('http://example.webscraping.com/')

from urllib.request import urlopen
import urllib.request
from urllib.request import build_opener
from urllib.request import urlparse
from urllib.request import ProxyHandler

# 下载html数据
def download(url, user_agent = 'wswp', proxy = None, num_retries=3):
    print('Downloading:',url)
    # 设置用户代理,伪装成浏览器访问
    header = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers = header)
    # 这个支持代理
    opener = build_opener()

    if proxy:
        # 设置代理服务器，通过该代理IP进行访问
        proxy_params = {urlparse(url).scheme: proxy}
        opener.add_handler(ProxyHandler(proxy_params))

    try:
        # 由于服务器等原因可能会返回不同的错误信息
        # urlopen使用的是Python-urllib的用户代理
        # 有些网站可能会封禁这个代理
        #html = urlopen(url).read()
        #html = urlopen(request).read()

        html = opener.open(request).read()
    except urllib.request.URLError as e:
        print('Download error:',e.reason)

        if num_retries > 0:
            # 5xx为服务器错误码，4xx为客户端错误码
            if hasattr(e, 'code') and 500 <= e.code < 600:
                download(url, user_agent, num_retries - 1)
        html = None
    return html

#html = download('http://httpstat.us/500')
#html = download('http://www.meetup.com')

import socket
# downloadler类，先读取缓存的内容，没有再从网络上获取后再写入缓存
# ps: 避免爬取被禁方法: 1.设置UA;2.设置proxy代理;3.下载之间延迟;4.禁止cookie
# 5.如果可能，访问cache获取;6.分布式下载
class Downloader:
    def __init__(self, delay=1, user_agent='wswp', timeout=1000, proxies=None, num_retries=3, cache=None):
        # 对整个socket设置连接的超时时间, urlopen的read会调用socket接口
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                try:
                    if self.num_retries > 0 and 500 <= result['code'] < 600:
                        result = None
                except TypeError:
                    pass
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data = None):
        print('Downloading:',url)
        request = urllib.request.Request(url, data, headers = headers)
        opener = build_opener()

        if proxy:
            proxy_params = {urlparse(url).scheme: proxy}
            opener.add_handler(ProxyHandler(proxy_params))

        try:
            html = None
            code =None
            html = opener.open(request, timeout=20).read()
            code = opener.open(request, timeout=20).code
        except urllib.request.URLError as e:
            print('Download error:',e.reason)

            if hasattr(e, 'code') > 0:
                print(e.code)
                if num_retries > 0 and 500 <= e.code < 600:
                    code = e.code
                    self.download(url, headers, proxy, num_retries - 1, data = None)
                else:
                    code =None
        except Exception:
            ''

        return {'html': html, 'code': code}

import re
# 获取站点地图链接的内容
def craw_sitemap(url):
    sitemap = download(url).decode('utf-8')

    # 链接存在于<loc>标签内
    links = re.findall(r'<loc>(.*?)</loc>', sitemap)

    for link in links:
        html = download(link)

#craw_sitemap('http://example.webscraping.com/sitemap.xml')

import itertools

#error_nunm = 0
#max_error = 5
# for page in itertools.count(1):
#
#     # 如url中的Aland-Islands-2 可以使用 2来 代替，Aland-Islands只是为搜索优化的，数字2
#     # 才是网站查询数据库所需要的，这种靠ID来访问只是针对简单的id情况，有些id很长则不适用
#     url = 'http://example.webscraping.com/places/default/view/{}'.format(page)
#
#     html = download(url)
#
#     if html is None:
#         error_nunm += 1
#         # ID 可能不连续，连接不成功后尝试指定次数
#         if error_nunm > max_error:
#             break
#     else:
#         error_nunm = 0

import datetime
from time import sleep

# 较短间隔时间连续获取某个网站的信息可能会被禁IP，所以限时访问
class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domain = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domain.get(domain)

        if self.delay > 0 and last_accessed is not None:
            # 访问时间间隔如果小于指定间隔，则取差值进行休眠
            sleep_secs = self.delay - (datetime.datetime.now() - self.domain[domain]).seconds
            if sleep_secs > 0:
                sleep(sleep_secs)
        self.domain[domain] = datetime.datetime.now()

from urllib.parse import urljoin
from urllib.request import urlsplit

import zlib,os
import shutil
try:
    # cPickle为C语言写的版本，速度会更快
    import cPickle as pickle
except ImportError:
    import pickle

# 磁盘缓存读取类
class DiskCache:
    # compress选择是否压缩文件以节省磁盘空间，但读写文件时速度会变慢点
    def __init__(self, cache_dir='myfile\cache', expires=datetime.timedelta(days=30), compress=False):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    # 设置文件内容
    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        # 获取父目录路径
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 序列化数据与存取的时间,
        # 将数据通过特殊的形式转换为只有python语言认识的字符串
        data = pickle.dumps((result, datetime.datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as f:
            f.write(data)

    # 获取文件内容
    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            print('get from:',path)
            with open(path, 'rb') as f:
                data = f.read()
                if self.compress:
                    data = zlib.decompress(data)
                    # 序列化数据后获取
                    # 将pickle数据转换为python的数据结构
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    self.clear()
                    raise KeyError(url + 'has expired')
                return result
        else:
            raise KeyError(url + 'dose not exist')

    def __delitem__(self, url):
        path = self.url_to_path(url)
        try:
            # 删除文件与目录
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    # 把url字符串转换成路径格式的字符串
    # 但在处理相似的url路径时可能会出现问题
    # 如/a*b与/a!b在实际中指向不同路径，
    # 但处理后就指向同一个磁盘路径了，而且文件名很多时
    # 会受到存储的限制，如ext4系统只允许同一个目录建立
    # 65535个文件
    def url_to_path(self, url):
        compents = urlsplit(url)
        path = compents.path
        # url目录路径如.com/后面可能是空的
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'

        filename = compents.netloc + path + compents.query
        # 文件名可能包含系统不支持的字符，如* >等符号，需替换掉
        filename = re.sub('[^0-9a-zA-Z\-.,;_]', '_', filename)
        return os.path.join(self.cache_dir, filename)

    # 判断文件数据是否过期
    def has_expired(self, timestamp):
        return datetime.datetime.utcnow() > timestamp + self.expires

    def clear(self):
        if os.path.exists(self.cache_dir):
            # 删除当前底下的所有子目录
            shutil.rmtree(self.cache_dir)

from pymongo import MongoClient
from bson.binary import Binary

# 使用mongo数据库实现的缓存
class MongoCache:
    def __init__(self, client=None, expires=datetime.timedelta(days=30), compress=False):
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache
        # 在某字段上建立索引(字段类型为date)，记录会在指定的时间后过期,过期后会被删除
        # 只能在单个字段上建立索引
        #self.db.webpage.create_index('timestamp', expiresAfterSeconds=expires.total_seconds())
        self.compress = compress

    def __setitem__(self, url, result):
        if self.compress:
            # pickle序列化后压缩
            result = Binary(zlib.compress(pickle.dumps(result)))
        else:
            result = Binary(pickle.dumps(result))
        record = {'result': result, 'timestamp': datetime.datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set':record}, upsert=True)

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id':url})
        if record:
            print('get from mongodb:',url)
            if self.compress:
                return pickle.loads(zlib.decompress(record['result']))
            return pickle.loads(record['result'])
        else:
            raise KeyError(url + 'dose not exist')

    # 特殊方法，使用 in 迭代类实例时，会自动调用
    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def clear(self):
        self.db.webpage.drop()

#cache = MongoCache(expires = datetime.timedelta())
#cache['url'] = {'j':1, 'k':2}
## mongodb会每分钟检查一次过期记录, 所以即使设置过期时间为0，也要等到一分钟后才能看到效果
#print(cache['url'])
#cache.clear()

# 获取html页面中的所有链接
def get_links(html):
    links_regex = re.compile(r'<a[^>]+href=["\'](.*?)["\']')
    return links_regex.findall(html)

# 获取网站中所有符合要求的链接信息
def link_crawler(seed_url, link_regex, delay=3, timeout=1000, max_urls=10, max_depth=3, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = None, cache=None):
    'max_depth：最多爬取多少网页链接，scrape_callback自定义处理函数，如把'
    '网站数据保存至本地文件'
    craw_queue = [seed_url]
    #seen = set(craw_queue)
    seen = {seed_url:0}
    #throttle = Throttle(0)
    # 最大爬取网页数目
    num_urls = 0
    downloader = Downloader(delay=delay, user_agent=user_agent, timeout=timeout, proxies=proxies, num_retries=num_retries, cache=cache)

    while craw_queue:
        url = craw_queue.pop()

        #throttle.wait(url)

        html = downloader(url)

        if html is not None: html = html.decode('utf-8')

        if scrape_callback:
            scrape_callback(url, html)

        depth = seen[url]
        # 判断是否爬取到了最大深度，有些网站其中的链接会无限循环，
        # 导致爬取出现死循环
        if depth != max_depth:
            for link in get_links(html):
                # 只获取特定网页的链接
                if re.search(link_regex, link):
                    # 获取网页绝对路径，link中可能含有/page/类似的相对路径
                    link = urljoin(url, link)
                    # 已经抓取过的不再抓取，也可以避免在互相有各自连接的两个页面之间反复跳跃
                    if link not in seen:
                        seen[link] = depth + 1
                        # 只抓取同一domain的链接
                        if urlparse(seed_url).netloc == urlparse(link).netloc:
                            craw_queue.append(link)
        num_urls += 1
        if num_urls == max_urls:
            break

# 缓存加载时间比大约为2:1
# 加入缓存机制(磁盘缓存)
#link_crawler('http://example.webscraping.com', '/(index|view)/', delay=0, max_depth=3, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = None, cache=DiskCache())
# 加入缓存机制(Mongodb缓存)
#link_crawler('http://example.webscraping.com/places/default/view/Albania-3', '/(index|view)/', delay=3, max_depth=3, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = None, cache=MongoCache())

# 过滤链接
#link_crawler('http://example.webscraping.com', '/(index|view)/')

from urllib import robotparser

rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
user_agent = 'BadCrawler'
user_agent = 'GooddCrawler'
# 检查是否可以指定代理访问网站
r = rp.can_fetch(user_agent, 'http://example.webscraping.com/')

# 正则可以很快提取html页面所需数据，但页面发生改变时，正则可能失效
#html = download('http://example.webscraping.com/places/default/view/American-Samoa-5')
html = None
if html is not None:
    html = html.decode('utf-8')
    area_regex = re.compile('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>')
    result = area_regex.findall(html)
    print(result)

# BeautifulSoup能根据标签提取内容，即使标签中的属性发生变化，只需改下
# 匹配的属性就可以了
from bs4 import BeautifulSoup

broken_html = '<ul class=country><li>Area<li>Population</ul>'
# html.parser可能无法正常修复html标签
soup = BeautifulSoup(broken_html, 'html.parser')
# 修复不规整的html内容
fixed_html = soup.prettify()
# 查找指定标签
ul = soup.find('ul', attrs={'class':'country'})
# 查找所有指定内容并以列表返回
li = soup.find_all('li')

#html = download('http://example.webscraping.com/places/default/view/American-Samoa-5')
html = 'hello'.encode()
soup = BeautifulSoup(html, 'html.parser')
tr = soup.find(attrs={'id':'places_area__row'})
if tr is not None:
    td = tr.find(attrs={'class':'w2p_fw'})
    # 获取标签文本内容
    text = td.text

# lxml由C语言编程，解析速度更快
import lxml.html

tree = lxml.html.fromstring(broken_html)
# 修复后的html
fixed_html = lxml.html.tostring(tree, pretty_print=True)

tree = lxml.html.fromstring(html)
# 先根据指定标签的id再根据另一个标签的class属性(css选择)去查找
if len(tree) != 0:
    td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    text = td.text_content()

    # 查询父标签为tr的td标签
    td = tree.cssselect('tr > td')[0]
    text = td.text_content()

    # 查询标签tr中所有的td标签
    td = tree.cssselect('tr td')[0]
    text = td.text_content()

    # 查询class为w2p_fl的所有标签
    td = tree.cssselect('.w2p_fl')[0]
    text = td.text_content()

    # 查询指定标签
    td = tree.cssselect('tr')[0]
    text = td.text_content()

    # 查询拥有指定属性的标签
    td = tree.cssselect('label[for=places_population]')[0]
    text = td.text_content()

id_regex = re.compile('<tr id=["\']places_(.*?)__row["\']>.*?</tr>')
l = id_regex.findall(html.decode('utf-8'))

# 需要获取的信息
FIELDS = tuple(l)

# 正则爬取
def re_scraper(html):
    html = html.decode('utf-8')
    result = {}
    for field in FIELDS:
        result[field] = re.findall('<tr id=["\']places_{0}__row["\']>.*?<td class="w2p_fw">(.*?)</td>'.format(field), html)[0]

    return result

# bs4爬取
def bs_scraper(html):
    result = {}
    soup = BeautifulSoup(html, 'html.parser')
    for field in FIELDS:
        result[field] = soup.find('table').find('tr', id='places_{0}__row'.format(field)).find('td', class_='w2p_fw').text

    return result

# lxml爬取
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    result = {}
    for field in FIELDS:
        result[field] = tree.cssselect('table > tr#places_{0}__row > td.w2p_fw'.format(field))[0].text_content()

    return result

NUM_ITERATIONS = 1000

ll = [('Regular_expressions', re_scraper), ('BeautifulSoup', bs_scraper), ('Lxml', lxml_scraper)]

# 对比正则，bs4,lxml的速度，时间对比大约为1:7:1.2
# 由于正则与lxml都是由C语言写的，所以比由python写的bs速度会快很多
# lxml会把数据解析为内部格式，花费一定开销，所以较正则慢点
# 总的来说，正则语法难但速度快，bs速度慢但语法简单，lxml综合两者优点
import time
if 1 > 2:
    for name, scraper in ll:
        start = time.time()
        for i in range(NUM_ITERATIONS):
            if name == 'Regular_expressions':
                # 由于正则会把结果缓存，速度会更快(大约14倍)，所以为了公平对比，先清缓存
                re.purge()
                ''
            result = scraper(html)

            assert result['area'] == '199 square kilometres'
        end = time.time()

        print('{0}:{1:.2f}'.format(name, start-end))

import csv
class ScrapeCallback:
    def __init__(self):
        # 写数据入csv文件
        self.writer = csv.writer(open('myfile/mycsv.csv', 'w'))
        self.fields = FIELDS
        self.writer.writerow(self.fields)

    # 特殊方法，scrape_callback() 的时候会被自动调用,其中scrape_callback是实例化的对象
    def __call__(self, url, html):
        if re.search('/view/', url):
            row = []
            tree = lxml.html.fromstring(html)
            for field in self.fields:
                try:
                    row.append(tree.cssselect('table > tr#places_{0}__row > td.w2p_fw'.format(field))[0].text_content())
                except IndexError: pass
            self.writer.writerow(row)

#link_crawler('http://example.webscraping.com/places/default/view/American-Samoa-5', '/(index|view)/', scrape_callback=ScrapeCallback())

from pymongo import MongoClient
# 端口需与mongodb启动时显示的端口号一致
if 1 > 2:
    client = MongoClient('localhost', 27017)
    db = client.cache
    html = 'hello American-Samoa'
    url = 'http://example.webscraping.com/places/default/view/American-Samoa-5'
    #db.webpage.insert({'url':url, 'html':html})

    # 即使插入相同的数据，但在数据实际上是另插入了一条新的记录
    #db.webpage.insert({'url':url, 'html':'hello American-Samoa'})
    result = db.webpage.find_one({'url':url})
    result = db.webpage.find({'url':url}).count()
    # 正则模糊查询
    result = db.webpage.find({'url':{'$regex':'xx'}}).count()

    # 查询_id字段值为url，如果不存在则插入$set
    db.webpage.update({'_id': url}, {'$set':{'html':'old_html'}}, upsert=True)
    db.webpage.update({'_id': url}, {'$set':{'html':'new_html'}}, upsert=True)
    result = db.webpage.find_one({'_id':url})

# ^((?!gov).)*$ 会匹配不含gov字符串的字符串，*代表匹配多次，?!为否定式查找，
# 类似gov的网站禁止爬取
# 也可以写成^(?!.*gov)
# 不包含pdf和gov和javascript等的链接(^(?!.*gov))(^(?!.*pdf))(^(?!.*javascript))
regstr = '(^(?!.*gov))(^(?!.*pdf))(^(?!.*javascript))(^(?!.*site.baidu.com))(^(?!.*mailto))'

# 写数据入csv文件
class MyScrapeCallback:
    def __init__(self):
        #os.chdir(r'E:\hexo\source.Olaful.github.io\Olaful.github.io\python\PythonApplication\PythonApplication')
        self.writer = csv.writer(open('myfile/mysites.csv', 'w'))
        self.fields = ('id', 'site')
        self.writer.writerow(self.fields)
        self.href_regex = re.compile(r'<li>.*?<a.*?href="(.*?)".*?</a></li>')
        self.siteid = 1

    # 特殊方法，scrape_callback() 的时候会被自动调用,其中scrape_callback是实例化的对象
    def __call__(self, url, html):
        try:
            tmplist = self.href_regex.findall(html)
        except TypeError:
            tmplist = self.href_regex.findall(str(html))
        sitelist = []
        for link in tmplist:
            if re.search(regstr, link):
                link = urljoin(url, link)
                sitelist.append(link)

        if len(sitelist) > 0 :
            ids = [id for id in range(self.siteid, self.siteid + len(sitelist))]
            self.siteid = self.siteid + len(sitelist)

            rowinfo = zip(ids,sitelist)

            for row in rowinfo:
                self.writer.writerow(row)

#link_crawler('http://site.baidu.com/', link_regex=regstr, delay=0, max_urls=200, max_depth=5, timeout=20, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = MyScrapeCallback(), cache=MongoCache())
#import timeit
#t = timeit.Timer("link_crawler('http://site.baidu.com/', link_regex=regstr, delay=0, max_urls=200, max_depth=5, timeout=20000, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = MyScrapeCallback(), cache=MongoCache())",
#                      setup="from __main__ import link_crawler, regstr, MyScrapeCallback, MongoCache")
#ti = t.timeit(1)
#import profile
#profile.run("link_crawler('http://site.baidu.com/', link_regex=regstr, delay=0, max_urls=200, max_depth=5, timeout=20000, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = MyScrapeCallback(), cache=MongoCache())")


#data = []
#os.chdir(r'E:\hexo\source.Olaful.github.io\Olaful.github.io\python\PythonApplication\PythonApplication')
#with open('myfile/mysites.csv', 'r') as f:
#    render = csv.reader(f)
#    for row in render:
#        print(row)
#        data.append(data)
#print(data)

from zipfile import ZipFile
from io import StringIO

downloader = Downloader()

#ZipFile需要一个类似文件的接口
#with ZipFile(zipdata) as zf:
#    name = zf.namelist()[0]
#    print(name)

#zipdata = downloader('http://localhost/html/myzip.zip')
# 保存zipdata文件至本地
#with open('myfile/myzip.zip', 'wb') as zf:
#    zf.write(zipdata)

# 从zip文件中获取url列表
class GetUrlCallback:
    def __call__(self, url):
        if url == 'http://localhost/html/myzip.zip':
            urls = []
            zipdata = downloader(url)
            # 保存zipdata文件至本地
            #os.chdir(r'E:\hexo\source.Olaful.github.io\Olaful.github.io\python\PythonApplication\PythonApplication')
            with open('myfile/myzip.zip', 'wb') as zf:
                zf.write(zipdata)
            with ZipFile('myfile/myzip.zip') as zf:
                # 获取zip文件中的文件列表
                filelist = zf.namelist()
                csv_file = filelist[0]

                # 由于读取到的是而bytes形式，需要转换成unicode的形式
                sitelist = list(map(lambda x: x.decode(), zf.open(csv_file, mode="r").readlines()))
                # csv.reader会处理掉空行\r\r\n
                data = csv.reader(sitelist)
                # 去掉表头
                next(data)
                for _,site in data:
                    urls.append(site)
                    #for site in sitelist:
                    #    urls.append(site.split(',')[1])

                    #with zf.open(csv_file, mode='r') as cf:
                    #    data = cf.readlines()
                    #    print(data)
                    #    for _,line in data:
                    #        urls.append(line)
            return urls

from threading import Thread

TIME_SLEEP = 1
# 多线程同时爬取网站信息
def thread_link_crawler_tmp(seed_url, delay=3, timeout=1000, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback = None, cache=None):
    craw_queue = scrape_callback()
    downloader = Downloader(delay=delay, user_agent=user_agent, timeout=timeout, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        while craw_queue:
            url = craw_queue.pop()
            html = downloader(url)

    threads = []
    while threads or craw_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and craw_queue:
            # 将爬取函数放在线程中执行
            thread = Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
            sleep(TIME_SLEEP)

# 单线程
def simple_link_crawler(seed_url, delay=3, timeout=1000, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback = None, cache=None):
    craw_queue = scrape_callback()
    downloader = Downloader(delay=delay, user_agent=user_agent, timeout=timeout, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        while craw_queue:
            url = craw_queue.pop()
            html = downloader(url)

    process_queue()

#thread_link_crawler('', delay=0, timeout=1000, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback = GetUrlCallback(), cache=None)

import timeit
# 时间比大约为1:max_threads
# 112sec
#t = timeit.Timer("thread_link_crawler('', delay=0, timeout=20, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback = GetUrlCallback(), cache=None)",
#                 setup="from __main__ import thread_link_crawler, GetUrlCallback").timeit(1)
# 368sec
#t = timeit.Timer("simple_link_crawler('', delay=0, timeout=20, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback = GetUrlCallback(), cache=None)",
#                 setup="from __main__ import simple_link_crawler, GetUrlCallback").timeit(1)

# 从MongoDB获取数据队列的类
from pymongo import errors
class MongoQueue:
    # url记录状态 0|待处理 1|处理中 2|已完成
    OUTSTANDING, PROCESSING, COMELETE = range(3)

    def __init__(self, client=None, timeout=300):
        self.client = MongoClient() if client is None else client
        self.db = self.client.cache
        self.timeout = timeout

    # 特殊方法，当用类实例进行判断时(如 if MongoQueue() bool(MongoQueue()))
    # 会自动调用，python2.x中的写法为__nonzero__
    # 判断是否所有url都已完成处理
    def __bool__(self):
        try:
            record = None
            record =  self.db.crawl_queue.find_one({'status': {'$ne': self.COMELETE}})
        except Exception as e:
            print(e)
        return True if record else False

    # 把一条url入库，把置状态为待处理
    def push(self, url):
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        # 重复记录处理
        except errors.DuplicateKeyError as e:
            print(url, 'already exist in the database')

    # 取一条处于待处理状态的url，并置其状态为处理中，并加上开始处理的时间
    # 补充'set'待设置的集合，相当于一条记录，'$lt'小于，'$ne'不等于，还有'gt'大于
    def pop(self):
        record =  self.db.crawl_queue.find_and_modify(
                query = {'status': self.OUTSTANDING},
                update = {'$set':{'status': self.PROCESSING, 'timestamp': datetime.datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    # 取一条处于待获取状态的url，但不改变其状态
    def peek(self):
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    # 把已经处理过的url状态置为已完成
    def complete(self, url):
        self.db.crawl_queue.update({'_id': url}, {'$set': {'status': self.COMELETE}})

    # 当一条url处理超时并且其状态没有被置为已完成时，
    # 这条url应该当作还没有处理，此时修改其状态为待处理
    def repair(self):
        record = self.db.crawl_queue.find_and_modify(
                query = {'timestamp': {'$lt': datetime.datetime.now()-datetime.timedelta(seconds=-self.timeout)}, 'status': {'$ne': self.COMELETE}},
                update = {'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('Released', record['_id'])

    # 清空队列
    def clear(self):
        self.db.crawl_queue.drop()

# 多线程同时爬取网站信息，爬取队列从mongodb中获取
def thread_link_crawler(seed_url, delay=3, timeout=1000, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback=None, cache=None):
    print('pid is : {}'.format(os.getpid()))
    craw_queue = MongoQueue()
    craw_queue.clear()
    # 存入mongodb中
    craw_queue.push(seed_url)
    downloader = Downloader(delay=delay, user_agent=user_agent, timeout=timeout, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        # 首先从从网址大全中获取所有url,依次存入mongodb中，再逐个url抓取
        while True:
            try:
                url = craw_queue.pop()
            except KeyError:
                break
            else:
                html = downloader(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url) or []
                    except Exception as e:
                        print('Error in Callback for {}:{}'.format(url, e))
                    else:
                        for link in links:
                            craw_queue.push(link)
            craw_queue.complete(url)

    threads = []
    # craw_queue用于判断时会调用其特殊方法__bool__
    while threads or craw_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and craw_queue:
            # 将爬取函数放在线程中执行
            thread = Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
            # 等待上一个进程开启完后再开启下一个进程
            sleep(TIME_SLEEP)

import multiprocessing
# 多进程爬取，每个进程中包含了多线程爬取函数
# 本机为四个进程，每个进程开始五个线程，相当于
# 总共开启20个线程，但进程的的线性增加并不意味着速度
# 的线性增加，因为一部分时间得花在线程的切换上，此外还会
# 受到网络宽带的限制
def process_crawler(args, **kwargs):
    # cpu核数决定能开多少个相同的进程
    nums_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(nums_cpus))
    processes = []
    for i in range(nums_cpus):
        # args参数会传递给没有赋初始值的thread_link_crawler函数的形参
        # kwargs参数会传递给赋了初始值的thread_link_crawler函数的形参
        p = multiprocessing.Process(target=thread_link_crawler, args=[args], kwargs=kwargs)
        # 开启进程
        p.start()
        processes.append(p)
    # join方法调用的时候会阻塞当前进程(main)，直到调用join方法的进程(p)执行
    # 完，才会继续往下执行，如果某个进程没有执行join方法，主进程则不会等待其
    # 执行完，会继续往下执行，而遇到了join方法的进程后，又会继续阻塞，
    # 如进程1先start,再join,而进程2等待进程1join之后才start,则主进程会等待
    # 进程1执行完后再执行完自身，最后才执行进程2
    for p in processes:
        p.join()

# 当要开启子进程时，一定要在__main__最高命名空间内执行
# 不然当子进程会重复读取不在__main__空间内的代码，读取到
# Process时又再次开启进程，这相当于开启自己的子进程，而在Process
# 的处理中这是不可以的
if __name__ == '__main__':
    ''
#    process_crawler('http://localhost/html/myzip.zip', delay=3, timeout=20, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback=GetUrlCallback(), cache=None)
# 子进程会首先打印出这句话，因为其不在__main__命令空间中
#print('enter pro')

from multiprocessing import Queue, Lock, Pipe, Manager

def putf(q, arg):
    # 队列满时阻塞等待,为False则抛出full异常，
    q.put(arg)

def getf(q):
    print('.....')
    print(q.get())

def sendf(pipe):
    pipe.send('hello, this is pro1')

def recvf(pipe):
    while True:
        print('pro2 recv:', pipe.recv())

# 在某段执行阶段加锁，使得该进程执行到这个
# 地方得时候不会切换到其他进程
lock = Lock()
def lockf():
    print('next need lock')
    global lock
    # 申请锁
    lock.acquire()
    print('enter locked to exec')
    # 释放锁
    lock.release()
    print('lock release')

def setData(dt, lt):
    dt['key'] = 'value'
    lt.append(1)

# 进程可通过Queue，Pipe进行通信
# 队列长度为10
# q = Queue(block=True, maxsize=10)
# 创建单向管道，默认为双向(管道两边都可以进行数据的读写)
# pipe = Pipe(duplex)
# Queue与Pipe分别只支持Array与Value操作，
# 而Manager则支持dict, list, value, Lock等多种对象
# manager = Manager()
# dt = manager.dict()
# lt = manager.list()
# p1 = multiprocessing.Process(target=putf, args=(q, 'hello'))
# pipe[0]为发送端
# p1 = multiprocessing.Process(target=sendf, args=(pipe[0],))
# p1 = multiprocessing.Process(target=setData, args=(dt, lt))
# p1.start()
# 执行时间最多为2秒
# p1.join(2)
# p2 = multiprocessing.Process(target=getf, args=(q, ))
# pipe[0]为接收端
# p2 = multiprocessing.Process(target=recvf, args=(pipe[1],))
# p2.start()
# p2.join()

import json, string
countries = set()
def getInfoByJson(max_urls = 50):
    downloader = Downloader(timeout=20)
    valid_urls = 0
    def getCountry():
        nonlocal max_urls
        nonlocal valid_urls
        for letter in string.ascii_lowercase:
            if valid_urls >= max_urls:
                break
            page = 0
            while True:
                # 会返回json格式的内容，该url的请求相当于点击界面某个按钮后会通过javascript的ajax方法请求数据，因此html界面的数据是动态生成的
                # 构造不同的search_term与page参数获取不同的结果
                # 模拟点击某个按钮时发生的js调用过程也称为js逆向工程
                html = downloader('http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size=10&page={}'.format(letter, page))
                try:
                    ajax = json.loads(html)
                # 类似'{"key1":"values", "key2":"values2"}'这样的包含字典的字符串才能解析成字典返回
                # key,value以双引号包围
                except json.decoder.JSONDecodeError as e:
                    print(e)
                    ajax = None
                except TypeError as e:
                    print(e)
                    ajax = None
                else:
                    for record in ajax['records']:
                        countries.add(record['country'])
                    valid_urls += 1
                page += 1
                if ajax is None or page >= ajax['num_pages']:
                    break
    for i in range(10):
        thread = Thread(target=getCountry)
        thread.setDaemon(True)
        thread.start()
        sleep(2)

if 1 > 2:
    # getInfoByJson()
    #FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currencyname', 'phone', 'postal_code_format', 'postal_c', 'de_regex', 'languages', 'neighbours')
    FIELDS = ('country',)
    downloader = Downloader(timeout=20)
    # .用作search_term参数的通配符，page_size设置为查找1000页，page_size参数网站一般不会检查
    html = downloader('http://example.webscraping.com/places/ajax/search.json?&search_term=.&page_size=1000&page=0')
    ajax = json.loads(html)

    os.chdir(r'E:\hexo\source.Olaful.github.io\Olaful.github.io\python\PythonApplication\PythonApplication')
    f = open('myfile/countries.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(FIELDS)

    for record in ajax['records']:
        row = (record['country'],)
        writer.writerow(row)

    f.close()

# 可以解析html，并生成类似于浏览器的桌面APP
#from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtCore import QUrl, QEventLoop
#from PyQt5.QtGui import  *

#class Page(QWebEngineView):
#    def __init__(self, url, mode='normal'):
#        self.app = QApplication([])
#        QWebEngineView.__init__(self)
#        # 本地事件循环
#        loop = QEventLoop()
#        # html页面加载完成后调用的方法
#        # 网页视图加载完成后调用loop.quit方法，停止事件循环
#        self.loadFinished.connect(loop.quit)
#        # 该方法为异步加载，因此需要在事件循环中等待网页的内容加载完毕
#        # 打开url并获得其html内容，如果html中有js，会被执行
#        self.load(QUrl(url))
#        # 启动事件循环
#        loop.exec_()
#        if mode == 'normal':
#            self.execJsAndGetHtml()
#        else:
#            self.execActionAndGetHtml()

#        # 显示窗口
#        self.show()
#        self.app.exec_()

#    def execJsAndGetHtml(self):
#        # toHtml位于超类中，因此该方法只能在类中使用，会把html的内容作为getHtml方法的入参
#        # page返回QWebEnginePage
#        self.page().toHtml(self.getHtml)

#    def execActionAndGetHtml(self):
#        self.page().toHtml(self.getHtml)

#    def getHtml(self, html_str):
#        self.html = html_str
#        #self.app.quit()

# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from PyQt4.QtWebKit import QWebView

# QWebKit实现的浏览器
# class BrowserRender(QWebView):
#     def __init__(self, show=True):
#         self.app = QApplication([])
#         QWebView.__init__(self)
#         if show:
#             self.show()

#     def download(self, url, timeout=60):
#         loop = QEventLoop()
#         timer = QTimer()
#         # 设置定时器超时会执行函数
#         timer.setSingleShot(True)
#         # 定时器超时或者页面加载完成都会触发事件循环退出
#         # 如果页面一直没有响应则用定时器终止循环
#         timer.timeout.connect(loop.quit)
#         self.loadFinished.connect(loop.quit)
#         self.load(QUrl(url))
#         timer.start(timeout*1000)
#         # 一直循环直到loop.quit被调用，之后才继续后面的部分
#         loop.exec_()

#         # 如果循环结束后，定时器还没有超时，则页面下载完成
#         if timer.isActive():
#             timer.stop()
#             return self.getHtml()
#         else:
#             print('Request time out:', url)

#     def getHtml(self):
#         return self.page().mainFrame().toHtml()

#     def find(self, pattern):
#         # css选择器，通过标签名或者class等选择
#         return self.page().mainFrame().findAllElements(pattern)

#     # 设置html页面元素的值
#     def attr(self, pattern, name, value):
#         for e in self.find(pattern):
#             e.setAttribute(name, value)

#     def text(self, pattern, value):
#         for e in self.find(pattern):
#             e.setPlainText(value)

#     # 模拟html页面元素的点击事件，调用相关javascript方法
#     def click(self, pattern):
#         for e in self.find(pattern):
#             e.evaluateJavaScript('this.click()')

#     # 在定时内反复查找页面返回的信息，因为ajax调用在规定时间内可能不能及时返回数据
#     def wait_load(self, pattern, timeout=60):
#         dealine = time.time() + timeout
#         while time.time() < dealine:
#             # processEvents调用之后就能响应后面的页面事件，app.exec_内部就是调用这个方法
#             self.app.processEvents()
#             matches = self.find(pattern)
#             if matches:
#                 return matches
#         print('Wait load time out')

#     # 保持当前窗口
#     def keepWindow(self):
#         self.app.exec_()

from selenium import webdriver
def webDeriver():
    # webdriver能使用响应浏览器的驱动打开浏览器
    chrome_options = webdriver.ChromeOptions()
    # 隐藏浏览器窗口
    chrome_options.add_argument('--headless')
    # 设置代理
    # proxy = '127.0.0.1:1025'
    # chrome_options.add_argument('--proxy-server=http://' + proxy)
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', chrome_options=chrome_options)
    driver.get('http://example.webscraping.com/places/default/search')
    # 向页面中的元素填充内容7
    driver.find_element_by_id('search_term').send_keys('.')
    # 自定义js语句
    js = 'document.getElementById("page_size").options[1].text="1000"'
    # 执行自定义js语句
    driver.execute_script(js);

    driver.find_element_by_id('search').click()

    # 查找的元素如果超过这个时间出现，则抛出异常
    driver.implicitly_wait(30)

    # 通过css选择器查找元素，其他匹配模式例如，通过属性匹配：div[name="value"]，正则匹配div[name^="value"]
    links = driver.find_elements_by_css_selector('#results a')
    countries = [link.text for link in links]
    hrefs = [link.get_attribute('href') for link in links]
    print(countries)
    # 关闭浏览器驱动器，关闭后，对象的session状态也会被取消
    driver.close()


def main_webkit(url):
    br = BrowserRender(show=True)
    br.download('http://example.webscraping.com/places/default/search')
    # 模拟界面点击过程: 填写值->点击按钮
    br.attr( '#search_term', 'value', '.')
    br.text( '#page_size option', '1000')
    br.click('#search')
    elements = br.wait_load('#results a')
    countries = [e.toPlainText().strip() for e in elements]
    print(countries)
    br.keepWindow()

# 获取需要提交的表单的元素
def getFormData(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

# 基于cookie实现的表单登录
def autoLogin():
    from urllib.parse import urlencode
    import http.cookiejar
    import ssl
    from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler

    url = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'
    email = 'test123@test.com'
    pwd = 'test'

    # 处理一些界面需要的认证登陆
    username = '123'
    pwd = '123'
    p = HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, 'http://xxx', username, pwd)
    auth_handler = HTTPBasicAuthHandler(p)
    opener = build_opener(auth_handler)

    # 处理与cookie的交互
    cj = http.cookiejar.CookieJar()
    opener = build_opener(urllib.request.HTTPCookieProcessor(cj))

    # 可以保存cookies
    # fn = 'cookies.txt'
    # cjj = http.cookiejar.MozillaCookieJar(fn)
    # cjj.save(ignore_discard=True, ignore_expires=True)
    #cjj.load(fn, ignore_discard=True, ignore_expires=True)

    # 如果访问https页面，可能会进行ssl认证，这时可以手动取消认证
    #cxt = ssl._create_unverified_context()
    #opener = build_opener(urllib.request.HTTPCookieProcessor(cj)，urllib.request.HTTPSHandler(context=cxt))

    # 服务器会获取表单元素中name所指的字段的值
    html = opener.open(url).read()
    data = getFormData(html)
    data['email'] = email
    data['password'] = pwd
    encode_data = urlencode(data).encode(encoding='utf-8')

    # 构造请求数据
    # 经过编码后的表单数据，通过post方式进行提交，但表单中可能还有其他隐藏的input输入框
    # 这些input的值可能也得获取并随其他可见input值一起提交
    # _formkey表单元素用来检查是否重复提交，刷新页面重新进去后会发生改变
    # _formkey的ID值会存储在浏览器cookie中，登录的时候会拿出来与提交的登录的表单的_formkey进行对比
    # 在http的响应头中会包含Set-Cookie类似的字段，用以保存设置的数据，如果后续再次访问该网站时会从浏览器
    # 中获取到这些cookie数据，就不用重复登录了，保持了会话的持久性
    # 这个表单action是'#'，表示提交表单到当前页面
    request = urllib.request.Request(url, data=encode_data, headers = {'User-agent': 'wswp'})

    response = opener.open(request)
    # 获取返回的url信息，获取到主页信息证明登录成功
    rls = response.geturl()
    print(rls)

    # 该url需要登录后才能访问，所以得调用设置了登录信息的opener
    urlEdit = 'http://example.webscraping.com/places/default/edit/Afghanistan-1#'
    requestEdit = urllib.request.Request(urlEdit, data=encode_data, headers = {'User-agent': 'wswp'})

    html = opener.open(requestEdit).read()
    tree = lxml.html.fromstring(html)

    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')

    # 修改数据后并向网站提交数据
    data['population'] = int(data['population']) + 1
    encode_data_upd = urlencode(data).encode()

    requestCommit = urllib.request.Request(urlEdit, data=encode_data_upd, headers = {'User-agent': 'wswp'})
    #resp = opener.open(requestCommit)
    #print(resp.geturl())

    # 获取存在在本地的cookie
    # requests与标准库urllib一样是一个同步请求库，会等待网页响应
    import requests, sqlite3
    from win32.win32crypt import CryptUnprotectData
    def getCookieFromChrome(host_key):
        cookiepath = os.environ['LOCALAPPDATA'] +r'\Google\Chrome\User Data\Default\Cookies'
        print(cookiepath)
        # Chrome的cookie存储在sqlite数据库中，name:value 其中的value值是经过CryptprotectData加密的
        # 需要使用windows的CryptUnprotectData解密函数进行解密
        with sqlite3.connect(cookiepath) as conn:
            cursor = conn.cursor()
            querySql = 'select host_key, name, encrypted_value from cookies where host_key="{}"'.format(host_key)
            cookieData = {name:CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in cursor.execute(querySql).fetchall()}
            print(cookieData)
            return cookieData
    print(encode_data_upd)
    # 该方法没有成功修改网站数据，所以用来登录, cookies也可以在headers中指定
    # proxies设置代理,可以设置socks代理,如{'http':'socks5://user:pwd:host:port'
    resp = requests.post(urlEdit, headers = {'User-agent': 'wswp'}, data=encode_data_upd, cookies=getCookieFromChrome('example.webscraping.com'))
    # 获取cookies
    print(resp.cookies)
    file = {'file': open('myfile/test.txt', 'rb')}
    # 指定files可以上传文件
    resp = requests.post(urlEdit, files=file)

    # 忽视ssl认证
    resp = requests.get('https://www.12306.cn', verify=False)

    # 认证访问
    resp = requests.get('https://www.12306.cn', auth=('username', 'pwd'))

    # 保持会话持久性
    s = requests.Session()
    s.get(urlEdit)
    s.get(urlEdit)

# 使用mechanize获取表单内容自动登录
def useMechLogin():
    import mechanicalsoup
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})
    urlLogin = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'
    browser.open(urlLogin)
    # nr=0选择匹配到的第一个form
    browser.select_form(nr=0)
    browser['email'] = 'test123@test.com'
    browser['password'] = 'test'
    # 提交所选择的表单的内容
    browser.submit_selected()
    browser.close()

from PIL import Image
from io import BytesIO
import base64
import pytesseract
from urllib.parse import urlencode
import http.cookiejar
import time

def get_captchaImg(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    img_data = img_data.partition(',')[-1]
    # 由于该图片使用base64编码二进制格式的文件(转换成ascii字符)，所以相应的使用base64解码
    binary_data = base64.b64decode(img_data)
    # 把二进制文件封装成类文件接口,普通的图片文件如.jpg,png文件可以直接用Image打开
    file_like = BytesIO(binary_data)
    img = Image.open(file_like)
    # 保存原始图像
    img.save('myfile/captcha_ori.png')
    # 保存灰度图像
    gray = img.convert('L')
    gray.save('myfile/captcha_gray.png')
    # (0~1：由白至黑过度)，对每一个像素阈值化处理，只保留纯黑纯白部分
    # 这样背景与前景就能很好地区分开来
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    bw.save('myfile/captcha_thresholded.png')
    return bw

REGISTER_URL = 'http://example.webscraping.com/places/default/user/register?_next=/places/default/index'
def register(first_name, last_name, email, pwd, captcha_fn=None):
    cj = http.cookiejar.CookieJar()
    opener = build_opener(urllib.request.HTTPCookieProcessor(cj))
    html = opener.open(REGISTER_URL).read()

    img = get_captchaImg(html)

    # 从其他API中获取验证码文字
    if captcha_fn is not None:
        captcha = captcha_fn()
    else:
        # 从图像文件中抽取文字，其中用到tesseract光学字符识别工具及其训练数据集
        # 但抽取的准确度跟图片背景纯度有关
        captcha = pytesseract.image_to_string(img)
        # 由于填写验证码都是小写，再次刷选
        captcha = ''.join(c for c in captcha if c in string.ascii_letters).lower()

    form = getFormData(html)

    # 表单处理
    form['first_name'] = first_name
    form['last_name'] = last_name
    form['email'] = email
    form['password'] = form['password_two'] = pwd
    form['recaptcha_response_field'] = captcha

    encoded_data = urlencode(form).encode()
    request = urllib.request.Request(url=REGISTER_URL, data=encoded_data)
    resp = opener.open(request)
    # 判断是否注册成功
    success = 'user/register' not in resp.geturl()
    return success

class CaptChaAPI:
    "根据已知的apikey和本地的验证码图像数据发送请求到9kw，获取返回的captchaid，根据captchaid"
    "请求9kw，获取验证码处理的结果文字"
    "9kw其实是由各个用户进行人工检查验证码的"
    "如果发送相同的图像数据，9kw服务器会从缓存读取数据"
    "可以帮别人验证验证码，获取积分"
    "注：9kw帐户:...@qq.com/6ZJ34BHNXT8P6XT"

    def __init__(self, api_key=None, timeout=60):
        self.api_key = api_key if api_key is not None else 'X8BOZF05VI5GZGCGH1'
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'

    # 获取9kw的API处理后的图片验证码的结果
    def solve(self, imgdata):
        # 数据编码为base64
        byte_buffer = BytesIO()
        imgdata.save(byte_buffer, format='PNG')
        data = byte_buffer.getvalue()
        base64Data = base64.b64encode(data)

        captcha_id = self.send(base64Data)
        start_time = time.time()

        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id)
            except CaptchaError:
                pass
            else:
                if text != 'NO DATA':
                    if text == 'ERROR NO USER':
                        raise CaptchaError('Error: no user avalible to solve CAPTCHA')
                    else:
                        print('CAPTCHA solved!')
                    return text
            print('Waiting for Captcha...')
        print('Error: API timeout!')

    def send(self, imgdata):
        print("Submmiting Captcha...")
        data = {
            "apikey": self.api_key,
            "action": "usercaptchaupload",
            "file-upload-01": imgdata,
            "base64": "1",
            "maxtimeout": str(self.timeout),
            # 如果为1表示自己处理，为0让他人处理，不过会消耗积分
            "selfsolve": "0"
        }
        encoded_data = urlencode(data).encode()
        request = urllib.request.Request(self.url, data=encoded_data)
        resp = urlopen(request)
        rls = resp.read().decode()
        self.check(rls)
        return rls

    def get(self, captcha_id):
        data = {
            "apikey": self.api_key,
            "action": "usercaptchacorrectdata",
            "id": captcha_id,
            # 没有得到结果时返回NO DATA
            "info": 1
        }
        encoded_data = urlencode(data)
        resp = urlopen(self.url + '?' + encoded_data)
        rls = resp.read().decode()
        self.check(rls)
        return rls

    def check(self, result):
        # apikey错误
        if re.match('00\d\d \w+', result):
            raise CaptchaError('API error:', result)

class CaptchaError(Exception):
    pass

# 使用渲染引擎获取百度搜索页面链接
def getBaiduData(*args):
    "args[0]搜索的关键字 args[1]获取的页数"
    def parseHref(x):
        if not x.startswith('http'):
            x = 'http://' + x
        else:
            x = x
        return x

    pn = [i*10 for i in range(args[1])]
    br = BrowserRender(show=True)

    for page in pn:
        html = br.download(url='https://www.baidu.com/s?wd={0}&pn={1}'.format(args[0], page))

        tree = lxml.html.fromstring(html)
        elements_url = tree.cssselect('a.c-showurl')
        hrefs = [element.text_content() for element in elements_url]
        hrefs = list(map(parseHref, hrefs))
        domains = [urlparse(href).scheme+'://'+urlparse(href).netloc for href in hrefs]
        
        print(domains)

    br.keepWindow()

def runCrwal():
    from subprocess import Popen, PIPE
    from scrapy.cmdline import execute
    os.chdir(r'srppro')

    # scrapy命令
    crawl_check = 'scrapy check -l'
    crawl_check2 = 'scrapy check'
    crawl_list = 'scrapy list'
    crawl_edit = 'scrapy edit dmoz'
    # 下载页面
    crawl_fetch = 'scrapy fetch --nolog https://www.csdn.net'
    crawl_fetch2 = 'scrapy fetch --nolog --headers https://www.csdn.net'
    # 在浏览器中打开url
    crawl_view = 'scrapy view https://www.csdn.net'
    # 使用给定的spider的parse函数进行处理
    crawl_parse = 'scrapy parse https://www.csdn.net --spider=dmoz'
    # 指定spider的函数
    crawl_parse1 = 'scrapy parse https://www.csdn.net --spider=dmoz -c parse'
    crawl_parse2 = 'scrapy parse https://www.csdn.net --spider=dmoz --noitems'
    crawl_parse3 = 'scrapy parse https://www.csdn.net --spider=dmoz --nolinks'
    crawl_parse4 = 'scrapy parse https://www.csdn.net --spider=dmoz -v'
    crawl_settings = 'scrapy settings --get BOT_NAME'
    crawl_runspider = 'scrapy runspider PythonApplication.py'
    crawl_v = 'scrapy version -v'
    crawl_benchmark = 'scrapy bench'
    create_crawler_pro = 'scrapy startproject test'
    create_spider = 'scrapy genspider myspider XX.com'
    run_crawl_dmoz = 'scrapy crawl csdnarticle'
    run_crawl_csimage = 'scrapy crawl csimage'
    run_crawl_example = 'scrapy crawl example.com'
    run_crawl_shell = 'scrapy shell "https://www.csdn.net"'
    # 导出item, 导出为jsonline格式，即[{'k1':'v1'},{'k2','v2'}]=>{'k1':'v1'}\n{'k2','v2'}
    # 所以支持大量数据导入，[]形式的话会把整个对象写入内存，内存压力较大
    run_crawl_o_json = 'scrapy crawl dmoz -o myfile/item.json'
    run_crawl_o_csv = 'scrapy crawl dmoz -o myfile/item.csv'
    run_crawl_o_xml = 'scrapy crawl dmoz -o myfile/item.xml'
    run_crawl_o_localfile = 'scrapy crawl dmoz -o file:///e:/git/Olaful/Olaful.github.io/python/PythonApplication/PythonApplication/srppro/myfile/file.csv'
    
    auth_info = ('ta', 'qweasd', '192.168.123.175')
    run_crawl_o_ftp = 'scrapy crawl dmoz -o ftp://{0}:{1}@{2}/ftpitem.csv'.format(*auth_info)
    # name会被spider名称所覆盖,time被timestamp覆盖
    run_crawl_o_ftp_autoname = 'scrapy crawl dmoz -o ftp://{0}:{1}@{2}/%(name)s_%(time)s.csv'.format(*auth_info)
    # file_name会被spider的属性file_name所覆盖
    run_crawl_o_ftp_autoproname = 'scrapy crawl dmoz -o ftp://{0}:{1}@{2}/%(file_name)s.csv'.format(*auth_info)

    run_crawl_other = 'scrapy crawl proxy_youdaili'

    Popen('dir', stdout=None, stderr=None)
    #execute(['scrapy', 'crawl', 'csdnarticle'])


from twisted.internet import reactor,defer
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

class Myspider(Spider):
    name = 'csimage'
    allowed_domains = ['csdn.net']
    start_urls = ["https://www.csdn.net"]

    def parse(self, response):
        item = {}
        for sel in response.xpath('//img'):
            item['image_urls'] = sel.xpath('@src').extract()
            yield item

# 在Twisted reactor中运行spider,使用自定义设置或者通用设置
def runSpider1():
    settings = Settings({'USER_AGENT':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    #runner = CrawlerRunner(settings)
    runner = CrawlerRunner(get_project_settings())
    # 自定义spider或者在scrapy已存在的spider
    d = runner.crawl(Myspider)
    d.addBoth(lambda _:reactor.stop())
    # 阻塞，直到spider运行完毕
    reactor.run()

# 执行多个spider
def runSpider2():
    os.chdir(r'srppro')
    runner = CrawlerRunner(get_project_settings())
    dfs = set()
    for domain in ['csdn.net']:
        # domain会覆盖spider原来的domain
        d = runner.crawl('csdnarticle', domain=domain)
        dfs.add(d)

    # 延迟加载
    defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
    reactor.run()

# 通过链接(chaining) deferred来线性运行spider
def runSpider3():
    os.chdir(r'srppro')
    runner = CrawlerRunner(get_project_settings())
    @defer.inlineCallbacks
    def crawl():
        for domain in ['www.douban.com', 'csdn.net']:
            yield runner.crawl('csimage', domain=domain)
        reactor.stop()

    crawl()
    reactor.run()

def pySpiderRun():
    from subprocess import Popen
    Popen('pyspider all', stdout=None, stderr=None)

import json
import requests
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            + 'Chrome/71.0.3578.98 Safari/537.36'
        }
        resp = requests.get(url, headers=header)
        if resp.status_code == 200:
            return resp.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # 表达式太复杂，陷入死循环
    pattern = """
      <dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
     '.*?>(.*?)</a>.*?start">(.*?)</p>.*?releasetime">(.*?)</p>'
     '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>
     """

    items = re.findall(pattern, html, re.S)
    for item in items:  
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5] + item[6]
        }

def write_to_file(content):
    with open(r'myfile/maoyantop.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def maoyanMain(offset=0):
    url = 'http://maoyan.com/board/4?offset={}'.format(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

# 京东某商品图片url

img_urls = []
def get_Img_urls():
    url = 'https://list.jd.com/list.html?cat=9987,653,655&ev=exprice%5FM500L999&sort=sort_rank_asc&trans=1&JL=3_%E4%BB%B7%E6%A0%BC_500-999#J_crumbsBar'
    header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    }
    rsp = requests.get(url, headers=header)
    tree = lxml.html.fromstring(rsp.text)
    data = tree.xpath(r'//li[contains(@class, "gl-item")]/div/div[contains(@class, "p-img")]/a/img/@data-lazy-img')
    for d in data:
        if d is not None:
            img_urls.append(urljoin(url, d))

def write_to_file():
    md = hashlib.md5()
    get_Img_urls()

    for url in img_urls:
        resp = requests.get(url, headers=header)
        md.update(resp.content)
        suffix_name = url.split('/')[-1].split('.')[-1]
        data = BytesIO(resp.content)
        try:
            img = Image.open(data)
            img.save('{0}.{1}'.format(md.hexdigest(), suffix_name))
        except OSError:
            pass


def pyQuery():
    from pyquery import PyQuery as pq

    html = """
    <div class="wrap">
        Hello World
        <p>This is a paragraph</p>
    <div id="container">
    <ul class="list">
    <li class="item-0">first item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html"><span class="bold"></span>third item</a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
    </div>
    </div>
    """
    doc = pq(html)
    rls = doc('li')

    doc = pq(url="https://maoyan.com/")
    rls = doc('title')

    doc = pq(filename='myfile/index.html')
    rls = doc('title')

    doc = pq(html)
    rls = doc('#container .list li')

    doc = pq(html)
    rls = doc('.list')
    rls = rls.find('li')
    rls = rls.children()

    rls = doc('.list')
    rls = rls.parent()

    rls = doc('.list')
    rls = rls.parents()

    rls = doc('.list .item-0.active')
    #rls = rls.siblings()
    rls = rls.siblings('.active')

    rls = doc('li').items()
    # for li in rls:
    #     print(li)

    rls = doc('.item-0.active a')
    # 只返回第一个节点的属性
    #rls = rls.attr('href')
    # 查找所有节点的text并以逗号隔开
    #rls = rls.text()
    rls = rls.html()

    # rls = doc('.item-0.active')
    # print(rls)
    # rls = rls.removeClass('active')
    # print(rls)
    # rls = rls.addClass('active')
    # print(rls)

    # rls = doc('.item-0.active')
    # print(rls)
    # rls.attr('name', 'link')
    # print(rls)
    # rls.text('changed item')
    # print(rls)
    # rls.html('<span>changed item</span>')
    # print(rls)

    rls = doc('.wrap')
    rls.find('p').remove()

    rls = doc('li:first-child')
    rls = doc('li:last-child')
    # 第二个li节点
    rls = doc('li:nth-child(2)')
    # 第三个节点之后的节点
    rls = doc('li:gt(2)')
    # 偶数位置节点
    rls = doc('li:nth-child(2n)')
    # 包含指定内容的节点
    rls = doc('li:contains("second")')
    print(rls)

# 通过splash渲染页面
def renderUseSplash():
    from urllib.parse import quote
    # 通过splash渲染页面
    url = 'http://192.168.99.100:8050/render.html?url=https://www.baidu.com'
    # 指定长宽参数可以返回页面截图
    png_data = '&wait=5&width=1000&height=700'
    png_url = url + png_data
    # 返回页面加载参数，如时间，header等
    rar_url = 'http://192.168.99.100:8050/render.har?url=https://www.baidu.com'
    # 以json格式返回
    json_url = 'http://192.168.99.100:8050/render.har?url=https://www.baidu.com'
    # 返回数据中带html内容
    html_data = 'html=1'
    json_url = json_url + html_data

    lua = """
        function main(splash)
            return 'hello'
        end
        """
    # 执行lua脚本
    exec_url = 'http://192.168.99.100:8050/execute?lua_source=' + quote(lua)
    rsp = requests.get(exec_url)
    print(rsp.text)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import random
# 处理拖动验证码
class BiliBiliest():
    # 调整偏移量
    ADJ = 15
    RETRY = 0
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.br = webdriver.Chrome()
        self.wait = WebDriverWait(self.br, 10)
        self.phone = ''
        self.pwd = ''
    
    # 对象被销毁时触发
    def __del__(self):
        self.br.close()

    # 打开页面并输入用户名与密码
    def open(self):
        self.br.get(self.url)
        self.br.implicitly_wait(30)
        self.br.find_element_by_id('login-username').send_keys(self.phone)
        self.br.find_element_by_id('login-passwd').send_keys(self.pwd)

    def login(self):
        submmit = self.br.find_element_by_xpath('//a[contains(@class, "btn btn-login")]')
        submmit.click()
        sleep(10)
        print('登录成功')

    # 获取拖动按钮
    def get_slider_btn(self):
        # 界面加载等待期间,界面按钮可点击的时候获取该按钮
        #btn = self.wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob gt_show')))
        self.br.implicitly_wait(10)
        btn = self.br.find_element_by_xpath('//div[contains(@class, "gt_slider_knob gt_show")]')
        return btn

    # 获取验证码图片的位置
    def get_pos(self):
        self.br.implicitly_wait(10)
        # 由于验证码图片是拼接起来的，先获取图片区域左上角
        # 图片的左上角位置，再获取图片区域的右下角图片的右
        # 下角位置
        img = self.br.find_element_by_xpath('//div[contains(@style, "background-position: -157px -58px")]')
        sleep(2)
        location = img.location
        size = img.size
        top, left = location['y'], location['x']

        img = self.br.find_element_by_xpath('//div[contains(@style, "background-position: -205px 0px")]')
        location = img.location
        size = img.size
        bottom, right = location['y'] + size['height'], location['x'] + size['width']

        return (left, top, right, bottom)

    def get_screenshot(self):
        screenshot = self.br.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    # 获取指定区域的屏幕截图
    def get_image(self, name):
        left, top, right, bottom = self.get_pos()
        print('图片验证码位置:', left, top, right, bottom)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('myfile/{}'.format(name))
        return captcha

    # 判断两张图片的像素是否相同
    def is_pixel_equal(self, img1, img2, x, y):
        # 获取图片指定位置像素
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        # 自定义阈值差
        threshold = 40
        # 判断RGB值是否相等
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold \
            and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    # 获取带缺口图片的缺口像素位置
    def get_gap(self, img1, img2):
        # 默认偏移量, 由于待拼合的模块在左边，占用一定位置
        left = 60
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    # 获取按钮拖动所需位移量信息，尽量模拟人拖动的速度
    def get_track(self, distance):
        track = []
        current = 0
        # 减速位置
        mid = distance * 4 / 5
        # 加速度时间单位
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            # 前段加速，后段减速
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 根据物理公式s = v0 * t + a * t^2 / 2计算每段时间移动距离
            move = v0 * t + (a * t * t) / 2 + random.random()
            current += move
            track.append(move)

        return track

    # 根据移动轨迹模拟按钮拖动
    def move_to_gap(self, slider, tracks):
        # 按钮按下
        ActionChains(self.br).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.br).move_by_offset(xoffset=x, yoffset=0).perform()
        sleep(0.5)
        # 释放按钮按下动作
        ActionChains(self.br).release().perform()

    def crack(self):
        self.open()
        btn = self.get_slider_btn()
        # 鼠标移动到拖动按钮上
        ActionChains(self.br).move_to_element(btn).perform()
        sleep(1)
        img1 = self.get_image('captcha_normal.png')

        ActionChains(self.br).click_and_hold(btn).perform()
        img2 = self.get_image('captcha_gaps.png')
        # ActionChains(self.br).release().perform()

        gap = self.get_gap(img1, img2)
        print('图片缺口位置:', gap)

        gap += self.ADJ
        track = self.get_track(gap)
        self.move_to_gap(btn, track)

        self.br.implicitly_wait(5)
        success = False
        # 计算缺口的位置可能有所偏差，所以多重复几次
        try:
            #success = self.wait.unit(expected_conditions.presence_of_element_located(By.ClASS_NAME, 'gt_ajax_tip gt_success'))
            success = self.br.find_element_by_xpath('//div[contains(@class, "gt_ajax_tip gt_success")]')
            print(success)
        except NoSuchElementException:
            pass
        
        if not success and self.RETRY < 5:
            self.RETRY += 1
            self.crack()
        else:
            self.login()

    
import requests
from hashlib import md5

# 通过向chaojiying验证码服务提供网站请求图片数据
class Chaojiying(object):
    def __init__(self, username, pwd, soft_id):
        self.username = username
        self.pwd = pwd
        self.soft_id = soft_id
        self.base_params = {
            'user':self.username,
            'pass2':self.pwd,
            'softid':self.soft_id,
        }
        self.header = {
            'Connection':'Keep-Alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.upload_url = 'http://upload.chaojiying.net/Upload/Processing.php'
        self.uperror_url = 'http://upload.chaojiying.net/Upload/ReportError.php'
    
    # 上传图片
    def post_pic(self, im, codetype):
        params = {'codetype': codetype,}
        params.update(self.base_params)
        files = {'userfile':('hello.jpg', im)}
        r = requests.post(self.upload_url, data=params, files=files, headers=self.header)
        # 结果示例{"err_no":0,"err_str":"OK","pic_id":"1662228516102","pic_str":"1,2|3,4","md5":"35d5c7f6f53223fbdc5b72783db0c2c0"}
        return r.json()

    # 获取上传错误信息
    def report_error(self, im_id):
        params = {'id':im_id}
        params.update(self.base_params)
        r = requests.post(self.uperror_url, data=params, headers=self.header)
        # 结果示例{"err_no":0,"err_str":"OK"}
        return r.json()

CHAOJIYING_USER = ''
CHAOJIYING_PWD = ''
CHAOJIYING_SOFTID = 898312
# 选取1-4个坐标
CHAOJIYING_KIND = 9004 
RAILWAY_12306_USER = ''
RAILWAY_12306_PWD = ''

class Railway_12306():
    RETRY = 0
    def __init__(self, username=RAILWAY_12306_USER, pwd=RAILWAY_12306_PWD):
        self.url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.br = webdriver.Chrome()
        # 等待界面出现元素的时间
        self.wait = WebDriverWait(self.br, 10)
        self.username = username
        self.pwd = pwd
        self.captSerive = Chaojiying(CHAOJIYING_USER, CHAOJIYING_PWD, CHAOJIYING_SOFTID)

    def open(self):
        self.br.get(self.url)
        login_with_acct = self.wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'login-hd-account')))
        login_with_acct.click()
        username = self.wait.until(expected_conditions.presence_of_element_located((By.ID, 'J-userName')))
        pwd = self.wait.until(expected_conditions.presence_of_element_located((By.ID, 'J-password')))
        username.send_keys(self.username)
        pwd.send_keys(self.pwd)

    def login(self):
        submmit = self.wait.until(expected_conditions.presence_of_element_located((By.ID, 'J-login')))
        submmit.click()
        sleep(5)
        print('登录成功')

    def get_click_element(self):
        em_img = self.wait.until(expected_conditions.presence_of_element_located((By.ID, 'J-loginImg')))
        return em_img

    def get_login_image(self, name):
        em_img = self.get_click_element()
        img_base64data = em_img.get_property('src').split(',')[-1]
        img_base64data = re.sub(r'[\s]+', '', img_base64data)
        binary_data = base64.b64decode(img_base64data)
        img = Image.open(BytesIO(binary_data))
        img.save('myfile/{}'.format(name))
        return img
        
    # 获取点击图像的坐标
    def get_pos(self, captcha_rls):
        groups = captcha_rls.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations
    
    # 根据坐标点击图像
    def touch_click_pic(self, locations):
        for location in locations:
            ActionChains(self.br).move_to_element_with_offset(self.get_click_element(), location[0], location[1]).click().perform()
        sleep(1)

    def get_cookies(self):
        return self.br.get_cookies()

    def crack(self):
        self.open()
        image = self.get_login_image('captcha_railway.png')
        byteData = BytesIO()
        image.save(byteData, format='PNG')
        rls = self.captSerive.post_pic(byteData.getvalue(), CHAOJIYING_KIND)
        print('坐标信息:', rls)
        locations = self.get_pos(rls)
        self.touch_click_pic(locations)
        self.login()

        success = not re.search('login', self.br.current_url)

        if not success and self.RETRY < 5:
            self.RETRY += 1
            self.crack()

        if success:
            return {'status': 1, 'content': self.get_cookies()}
        else:
            return {'status': 3, 'content': '登录失败'}

from selenium.common.exceptions import TimeoutException

USERNAME = ''
PWD = ''
class CrackWeiboSlide():
    "把模板保存到本地，对比验证码与模板匹配"
    def __init__(self):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.br = webdriver.Chrome()
        self.wait = WebDriverWait(self.br, 10)
        self.username = USERNAME
        self.pwd = PWD
    
    def __del__(self):
        self.br.close()

    def open(self):
        self.br.get(self.url)
        username = self.wait.until(expected_conditions.presence_of_element_located((By.ID, "loginName")))
        pwd = self.wait.until(expected_conditions.presence_of_element_located((By.ID, "loginPassword")))
        submit = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "loginAction")))
        username.send_keys(self.username)
        pwd.send_keys(self.pwd)
        submit.click()

    def get_pos(self):
        img = None
        try:
            img = self.wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "patt-shadow")))
        except TimeoutException:
            print('验证码没有出现')
            self.open()
        sleep(2)
        if img is not None:
            location = img.location
            size = img.size
            top, left, bottom, right = location['y'], location['x'], location['y'] + size['height'],\
            location['x'] + size['width']
            return (top, left, bottom, right)
        return (0, 0, 0, 0)

    def get_screenshot(self):
        screenshot = self.br.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_img(self, name):
        top, left, bottom, right = self.get_pos()
        print('宫格码位置信息:', top, left, bottom, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save('myfile/Palace/{}'.format(name))

    # 获取带有箭头的宫格图像
    def main(self):
        cnt = 0
        while True:
            self.open()
            self.get_img(str(cnt) + '.png')
            cnt += 1

    def detect_img(self, img):
        for tmp_name in os.listdir('myfile/Palace'):
            print('正在匹配:', tmp_name)
            tmp = Image.open('myfile/Palace/{}'.format(tmp_name))
            if self.same_img(img, tmp):
                num = [int(number) for number in list(tmp_name.split('.')[0])]
                print('拖动顺序为:', num)
                return num

    def is_pixel_equal(self, img1, img2, x, y):
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 20
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold \
            and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def same_img(self, img, tmp):
        threshold = 0.99
        cnt = 0
        for x in range(img.width):
            for y in range(img.height):
                if self.is_pixel_equal(img, tmp, x, y):
                    cnt += 1
        # 误差
        rls = float(cnt) / (img.width * img.height)
        if rls > threshold:
            print('匹配成功')
            return True
        return False

    # 按照路径在宫格上拖动鼠标
    def move(self, num):
        circles = self.br.find_element_by_css_selector('.patt-wrap .patt-circ')
        dx = dy = 0
        for idx in range(4):
            circle = circles[num[idx] - 1]
            if idx == 0:
                ActionChains(self.br).move_to_element_with_offset(circle, circle.size['width'] / 2,\
                circle.size['height'] / 2).click_and_hold().perform()
            else:
                times = 30
                for i in range(times):
                    ActionChains(self.br).move_by_offset(dx / times, dy / times).perform()
                    sleep(1 / times)
            if idx == 3:
                ActionChains(self.br).release().perform()
            else:
                dx = circles[num[idx + 1] - 1].location['x'] - circle.location['x']
                dy = circles[num[idx + 1] - 1].location['y'] - circle.location['y']

    def crack(self):
        self.open()
        img = self.get_img('Palace.png')
        num = self.detect_img(img)
        self.move(num)
        sleep(10)

import redis
from redis.exceptions import DataError

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PWD = '123456'
REDIS_ZSET_KEY = 'proxies'

# 使用redis存储代理
class RedisCli():
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PWD):
        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        if not self.db.zscore(REDIS_ZSET_KEY, proxy):
            self.db.zadd(REDIS_ZSET_KEY, {proxy:score,})
    
    def random(self):
        rls = self.db.zrangebyscore(REDIS_ZSET_KEY, MAX_SCORE, MAX_SCORE)
        if len(rls):
            return random.choice(rls)
        else:
            rls = self.db.zrevrange(REDIS_ZSET_KEY, 0, 100)
            if len(rls):
                return random.choice(rls)
            else:
                 raise DataError
    
    def decrease(self, proxy):
        score = self.db.zscore(REDIS_ZSET_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理{}分数{}减1'.format(proxy, score))
            self.db.zincrby(REDIS_ZSET_KEY, -1, proxy)
        else:
            print('移除代理{}:{}'.format(proxy, score))
            self.db.zrem(REDIS_ZSET_KEY, proxy)

    def exist(self, proxy):
        return not zscore(REDIS_ZSET_KEY, proxy) == None
    
    def add_max(self, proxy):
        print('代理{}可用，分数设置为{}'.format(proxy, MAX_SCORE))
        return self.db.zadd(REDIS_ZSET_KEY, {proxy:MAX_SCORE})

    def count(self):
        return self.db.zcard(REDIS_ZSET_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_ZSET_KEY, MIN_SCORE, MAX_SCORE)

# 代理元类
class ProxyMetaclass(type):
    # 参数：1.当前准备创建的类的对象 2.类的名字 3.类继承的父类集合 4.类的方法集合
    def __new__(cls, name, bases, attrs):
        cnt = 0
        attrs['_CrawlFunc_'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['_CrawlFunc_'].append(k)
                cnt += 1
        attrs['_CrawlFuncCount_'] = cnt
        return type.__new__(cls, name, bases, attrs)

from pyquery import PyQuery as pq

# 获取代理
class CrawlProxy(object, metaclass=ProxyMetaclass):
    def __init__(self):
        self.header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        }

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('获取代理:', proxy)
            proxies.append(proxy)
        return proxies

    # 获取有代理网站免费代理IP
    def crawl_youdaili(self):
        start_url = 'https://www.youdaili.net/Daili/http/368{:02d}.html'
        urls = [start_url.format(page) for page in range(13, 0, -1)]
        for url in urls:
            print('下载有代理数据:', url)
            html = requests.get(url, headers=self.header).content.decode()
            doc = pq(html)
            rls = doc('.content p')
            for p in rls:
                ipports = p.text_content()
                for ipport in re.findall(r'([\d.:]+)#', ipports):
                    yield ipport

    # 获取快代理网站免费代理IP
    def crawl_kuaidaili(self, page_cnt=20):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_cnt + 1)]
        for url in urls:
            print('下载块代理数据:', url)
            html = requests.get(url, headers=self.header).content.decode()
            doc = pq(html)
            rls = doc('table tr')
            # 去掉表头
            rls = rls[1:0]
            # tr类型为lxml.html.HtmlElement
            for tr in rls:
                ip = tr.getchildren()[0].text
                port = tr.getchildren()[1].text
                yield ':'.join([ip, port])
            

POOL_UPPER__THRESHOLD = 10000
# 存储代理
class StorageProxy():
    def __init__(self):
        self.redis = RedisCli()
        self.crawler = CrawlProxy()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER__THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('开始入库--------')
        for callback_label in range(self.crawler._CrawlFuncCount_):
            callback_func = self.crawler._CrawlFunc_[callback_label]
            proxies = self.crawler.get_proxies(callback_func)
            for proxy in proxies:
                self.redis.add(proxy)

import aiohttp
import asyncio
from aiohttp.client_exceptions import ClientError, ClientConnectionError

VALID_STATUS_CODE = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100

# 测试代理
class TestProxy(object):
        def __init__(self):
            self.redis = RedisCli()
        # 异步协程函数，不会导致阻塞
        async def test_single_proxy(self, proxy):
            conn = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.ClientSession(connector=conn) as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode()
                    real_proxy = 'http://' + proxy
                    print('正在测试:',proxy)
                    # 异步请求，get方法类似于reuqests的get方法
                    async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                        if response.status in VALID_STATUS_CODE:
                            self.redis.add_max(proxy)
                            print('代理可用:', proxy)
                        else:
                            self.redis.decrease(proxy)
                            print('响应码不正确，代理可能不可用:', proxy)
                except (ClientError, ClientConnectionError, TimeoutError, AttributeError):
                    self.redis.decrease(proxy)
                    print('代理请求失败:', proxy)

        def run(self):
            print('代理测试器开始运行')
            try:
                proxies = self.redis.all()
                for i in range(0, len(proxies), BATCH_TEST_SIZE):
                    test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                    loop = asyncio.get_event_loop()
                    tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                    # 同时并发BATCH_TEST_SIZE个协程
                    loop.run_until_complete(asyncio.wait(tasks))
                    sleep(5)
            except Exception as e:
                print('测试器运行错误:', e.args)

# 通过web接口访问代理
def FlaskWebApiProxy(host, port):
    from flask import Flask, g
    __all__ = ['app']
    app = Flask(__name__)
    
    def get_conn():
        if not hasattr(g, 'redis'):
            g.redis = RedisCli()
        return g.redis
    
    @app.route('/')
    def index():
        return '<h2>Welcome To Visit The Proxy Pool</h2>'

    @app.route('/random')
    def get_proxy():
        conn = get_conn()
        return conn.random()
    
    @app.route('/count')
    def get_cnt():
        conn = get_conn()
        return str(conn.count())

    app.run(host, port)

TEST_CYCLE = 1
GET_CYCLE = 1
TEST_ENABLED = False
GET_ENABLED = False
API_ENABLED = False
API_IP = '127.0.0.1'
API_PORT = 1025
from multiprocessing import Process
# 调度代理：获取，存储，测试，调用
class Scheduler():
    def scheduler_test(self, cycle=TEST_CYCLE):
        test = TestProxy()
        while cycle:
            print('测试器开始执行')
            test.run()
            cycle -= 1
            sleep(5)

    def scheduler_get(self, cycle=GET_CYCLE):
        get = StorageProxy()
        while cycle:
            print('抓取器开始执行')
            get.run()
            cycle -= 1
            sleep(5)

    def scheduler_api(self):
        print('代理API开启:',API_IP,API_PORT)
        FlaskWebApiProxy(API_IP, API_PORT)

    def run(self):
        print('代理调度器开始执行')
        if TEST_ENABLED:
            test_process = Process(target=self.scheduler_test)
            test_process.start()

        if GET_ENABLED:
            get_process = Process(target=self.scheduler_get)
            get_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

# 随机获取一个可用代理
def get_proxy(API_IP, API_PORT):
    proxy_url = 'http://' + API_IP + str(API_PORT) + '/random'
    try:
        return requests.get(proxy_url).text
    except ConnectionError:
        return None

# cookie池: 1.获取 2.存储 3.检测 4.接口

# cookie存储模块
class RedisCookieCli(object):
    def __init__(self, type, website, host = REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PWD):
        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return '{type}:{website}.'.format(type=self.type, website=self.website)

    # 存储格式usrname:hashvalue
    def set(self, usrname, value):
        return self.db.hset(self.name(), usrname, value)

    def get(self, usrname):
        return self.db.hget(self.name(), usrname)

    def delete(self, usrname):
        return self.db.hdel(self.name(), usrname)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def username(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())

# cookie生成模块父类, 在数据库先存储站点用户名与密码,之后根据
# 用户名与密码登录站点，之后通过webdriver获取到cookie,账户信息
# 存储在名为account:website(自定站点名)的hash表中, 根据账户登录浏览器获取
# 的cookie存储在名为cookies:website的hash表中
class CookieGenerator(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisCookieCli('cookies', self.website)
        self.accounts_db = RedisCookieCli('accounts', self, website)
        self.init_br()

    def __del__(self):
        self.close()

    def init_br(self):
        self.br = webdriver.Chrome()

    def new_cookies(self, username, pwd):
        raise NotImplementedError

    def process_cookies(self, cookies):
        dicts = {}
        for cookie in cookies:
            dicts[cookie['name']] = cookie['value']
        return dicts

    def run(self):
        accounts_usernames = self.accounts_db.username()
        cookies_usernames = self.cookies_db.username()

        for username in accounts_usernames:
            if not username in cookies_usernames:
                pwd = self.accounts_db.get(username)
                print('正在生成cookie:账户 {}, 密码 {}'.format(username, pwd))
                rls = self.new_cookies(username, pwd)
                if rls.get('status') == 1:
                    cookies = self.process_cookies(rls.get('content'))
                    print('成功获取cookie:{}'.format(cookies))
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存cookie')
                elif rls.get('status') == 2:
                    print('cookie获取失败:{}'.format(rls.get('content')))
                    if self.accounts_db.delete(username):
                        print('删除账户成功')
                else:
                    print('cookie获取失败:{}'.format(rls.get('content')))

    def close(self):
        try:
            print('Closing Browser')
            self.br.close()
            del self.br
        except TypeError:
            print('Browser not opened')

# 12306cookie生成器
class CookieGenerator12306(CookieGenerator):
    def __init__(self, website='12306'):
        CookieGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, pwd):
        return Railway_12306(username, pwd).crack()

# cookie检测模块
class TestCookie(object):
    def __init__(self, website='default'):
        self.website = website
        self.accounts_db = RedisCookieCli('accounts', self.website)
        self.cookies_db = RedisCookieCli('cookies', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookie_groups = self.cookies_db.all()
        for username, cookie in cookie_groups.items():
            self.test(username, cookie)

TEST_URL_MAP = {'12306':'https://www.12306.cn/index/'}

# 检测12306网站cookie
class Test12306(TestCookie):
    def __init__(self, website='12306'):
        TestCookie.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试用户{}的cookie'.format(username))
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('cookies不合法')
            self.cookies_db.delete(username)
            print('删除cookie')
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            resp = requests.get(test_url, cookies=cookies, timeout=10, allow_redirects=False)
            if resp.status_code == 200:
                print('cookie有效'.format(username))
                print('请求返回结果部分展示:{}'.format(resp.text[0:50]))
            else:
                print('请求失败:{} {}'.format(resp.status_code, resp.headers))
                print('cookie失效')
                self.cookies_db.delete(username)
                print('删除cookie')
        except ConnectionError as e:
            print('发生异常:{}'.format(e.args))

GENERATOR_MAP = {'12306', 'CookieGenerator12306'}

# cookie池访问API
def FlaskWebApiCookie(host, port):
    from flask import Flask, g                 
    app = Flask(__name__)
    @app.route('/')
    def index():
        return '<h2>Welcome To Visit The Cookie Pool</h2>'

    def get_conn():
        for website in GENERATOR_MAP:
            if not hasattr(g, website):
                setattr(g, website + '_cookies', eval('RedisCookieCli' + '("cookies", "' + website + '")'))
            return g
    
    @app.route('/<website>/random')
    def random(website):
        g = get_conn()
        cookies = getattr(g, website + '_cookies').random()
        return cookies

    app.run(host, port)

TESTER_MAP = {'12306':'Test12306'}
COOKIEGENERATOR_ENABLED = True
COOKIETESTER_ENABLED = False

# 调度cookie池模块
class SchedulerCookie(object):
    @staticmethod
    def test_cookie(cycle=5):
        while True:
            print('cookie测试器开始运行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('cookie测试完成')
                    del tester
                    sleep(cycle)
            except Exception as e:
                print('发生异常:{}'.format(e.args))

    def generator_cookie(cycle=1):
        while cycle:
            print('cookie生成器开始运行')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('cookie生成完成')
                    generator.close()
                    sleep(cycle)
            except Exception as e:
                print('发生异常:{}'.format(e.args))

            cycle -= 1

    @staticmethod
    def api():
        print('cookie池API接口开始运行')
        FlaskWebApiCookie(API_IP, API_PORT)
    
    def run(self):
        if API_ENABLED:
            api_process = Process(target=SchedulerCookie.api)
            api_process.start()
        if COOKIEGENERATOR_ENABLED:
            generator_process = Process(target=SchedulerCookie.generator_cookie)
            generator_process.start()
        if COOKIETESTER_ENABLED:
            tester_process = Process(target=SchedulerCookie.test_cookie)
            tester_process.start()


# spider运行管理 1.scrapyrt http接口, 2.scrapyd http接口与部署 3.gerapy可视化界面管理
# 环境问题解决: 制作docker spider项目镜像 scrapyd镜像
# 使用云主机快速克隆环境部署

# 通过scrapyrt启动爬虫
def StartSpiderWithSrprt():
    # 可选参数spider_name, url(start_requests为False则必填),max_requests,callback
    # get请求
    os.chdir('srppro')
    cmd = 'scrapyrt'
    url = 'http://localhost:9080/crawl.json?spider_name=csimage&start_requests=true&callback=parse'
    # 返回json格式
    resp = requests.get(url)
    data = resp.json()

# 制作scrapy项目docker镜像
def MkDockerImage():
    cmd = 'docker build -t srppro .'

# scrapyd部署scrapy项目
def Scrapyd():
    cmd = 'scrapyd'

    # 查看scrapy任务
    status_cmd = 'curl http://127.0.0.1:6800/daemonstatus.json'
    # 把项目打包成egg
    egg_cmd= 'curl http://127.0.0.1:6800/addversion.json -F project=srppro -F version=first -F egg=@srppro.egg'
    # 调度已部署的项目spider
    scheduler_cmd= 'curl http://127.0.0.1:6800/scheduler.json -d project=srppro -d spider=csimage'
    # 取消spider的运行
    cacel_cmd = 'curl http://127.0.0.1:6800/cancel.json -d project=srppro -d job=spiderid'
    # 列出已部署的项目
    list_cmd = 'curl http://127.0.0.1:6800/listprojects.json'
    # 列出项目版本号
    version_cmd = 'curl http://127.0.0.1:6800/listversions.json'
    # 列出项目的spider
    spider_cmd = 'curl http://127.0.0.1:6800/listspiders.json?project=srppro'
    # 列出项目spider的任务详情
    spidertask_cmd = 'curl http://127.0.0.1:6800/listjobs.json?project=srppro'
    # 删除某版本的项目
    delversion_cmd = 'curl http://127.0.0.1:6800/delversion.json -d project=srppro -d version=v1'
    # 删除项目
    delpro_cmd = 'curl http://127.0.0.1:6800/delversion.json -d project=srppro'
    # 返回json格式
    #resp = requests.get(status_cmd)
    #data = resp.json()

    # 通过scrapyd_api部署
    from scrapyd_api import ScrapydAPI
    url = 'http://127.0.0.1:6800'
    scrapyd = ScrapydAPI(url)
    # 运行爬虫
    scrapyd.schedule('srppro', 'csimage')
    # 列出srppro状态
    scrapyd.list_jobs('srppro')
    # 列出项目版本
    scrapyd.list_versions('srppro')
    # 列出项目spider
    scrapyd.list_spiders('srppro')
    # 列出所有项目
    scrapyd.list_projects()
    # 删除项目指定版本
    scrapyd.delete_version('srppro', '123')
    # 删除项目
    scrapyd.delete_project('srppro')
    # 取消项目制定任务
    scrapyd.cancel('srppro', '123')
    # 添加项目
    # with open('myfile/srppro.egg', 'rb') as egg:
    #     scrapyd.add_version('srppro', 'v1', egg)

    scrapyd_cli_cmd = 'scrapyd-deploy'

# 通过gerapy进行界面化管理scrapy项目
def Gerapy():
    # 新建gerapy项目
    cmd_init = 'gerapy init'
    # 通过sqlite保存gerapy信息
    cmd_db = 'gerapy migrate'
    # 启动gerapy项目
    cmd_run = 'gerapy runserver'

def main():
    runCrwal()

if __name__ == '__main__':
    #---------------------------------------------------start
    tupletime = time.localtime()
    print('program start:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print()
    starttime = time.time()

    #main()
    print('hello')

    #---------------------------------------------------end
    endtime = time.time()
    tupletime = time.localtime()
    print()
    print('program   end:', '{0}/{1}/{2} {3}:{4}:{5}'.format(tupletime.tm_year, tupletime.tm_mon, tupletime.tm_mday, tupletime.tm_hour, tupletime.tm_min, tupletime.tm_sec))
    print('total time: {0:5.2f}seconds'.format(endtime-starttime))

