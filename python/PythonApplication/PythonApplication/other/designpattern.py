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

# ---------------------------------过滤器模式
class Person(object):
    def __init__(self, name, gender, maritalStatus):
        self.name = name
        self.gender = gender
        self.maritalStatus = maritalStatus

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender.lower()
    
    def getMaritalStatus(self):
        return self.maritalStatus.lower()

class Filter():
    def filter(self):
        NotImplemented

class FilterMale(Filter):
    def filter(self, persons):
        pList = []
        for p in persons:
            if p.getGender() == 'male':
                pList.append(p)
        return pList

class FilterFemale(Filter):
    def filter(self, persons):
        pList = []
        for p in persons:
            if p.getGender() == 'female':
                pList.append(p)
        return pList

class FilterMaleAndSingle(Filter):
    def filter(self, persons):
        pList = []
        for p in persons:
            if p.getGender() == 'female' and p.getMaritalStatus == 'single':
                pList.append(p)
        return pList

pList = [Person('Mike', 'Male', 'Single'), Person('Susanna', 'Female', 'Married')]
male = FilterFemale()
mList = male.filter(pList)
female = FilterFemale()
fList = female.filter(pList)

# ---------------------------------组合模式
class Menu(object):
    def __init__(self, name, level):
        self.name = name
        self.level = int(level)
        self.mList = []
    
    def add(self, objMenu):
        self.mList.append(objMenu)

    def remove(self, objectMenu):
        self.mList.remove(objectMenu)

    def getMenuGrp(self):
        return self.mList

    def __str__(self):
        return self.name + self.level

menu1 = Menu('File', 1)
menu2 = Menu('New File', 2)
menu3 = Menu('Preferences', 2)
menu4 = Menu('Settings', 3)

menu1.add(menu2)
menu1.add(menu3)
menu2.add(menu4)

    


                
