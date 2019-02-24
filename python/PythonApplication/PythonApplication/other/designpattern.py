# ---------------------------------工厂模式
class Bird(object):
    def sing(self):
        NotImplemented

class eagle(Bird):
    def sing(self):
        print('eagle sing')

class Owl(Bird):
    def sing(self):
        print('owl sing')

class BirdFactory():
    # 根据参数实例化相应的类
    def getBird(self, BirdType='eagle'):
        if BirdType == 'eagle':
            return eagle()
        elif BirdType == 'owl':
            return Owl()

bird = BirdFactory().getBird('owl')
bird.sing()

# ---------------------------------装饰器模式
def decorate(cls):
    def innerfunc(*args, **kwargs):
        return cls(*args, **kwargs)
    return innerfunc

@decorate
class Bird(object):
    def sing(self):
        NotImplemented

bird = Bird()

# ---------------------------------桥接模式
class Bird(object):
    def sing(self):
        NotImplemented

class eagle(Bird):
    def sing(self):
        print('eagle sing')

class Owl(Bird):
    def sing(self):
        print('owl sing')

class Brige():
    def __init__(self, birType):
        self.birType = birType
    
    def sing(self):
        self.birType.sing()

bird = Brige(eagle())
bird.sing()

# ---------------------------------命令模式
class Bird(object):
    def sing(self):
        NotImplemented

class Eagle(Bird):
    def sing(self):
        print('eagle sing')

class Owl(Bird):
    def sing(self):
        print('owl sing')

import sys
birdType = sys.argv[1:2]
bird = None
if birdType == 'eagle':
    bird = Eagle()
elif birdType == 'owl':
    bird = Owl()

bird.sing()