#/usr/bin/python
#! -*- coding:utf-8 -*-


def pattern_factory():
    """
    creative pattern
    
    instance: the same plastic can produce diff toy

    create diff obj only in one func
    easily to track the building of obj
    decoupling obj generation and obj using
    """
    import json
    import xml.etree.ElementTree as etree

    class JSONDataExtractor:
        def __init__(self, filepath):
            with open(filepath, mode='r', encoding='utf-8') as f:
                self.data = json.load(f)

        @property
        def parsed_data(self):
            return self.data

    class XMLDataExtractor:
        def __init__(self, filepath):
            self.tree = etree.parse(filepath)

        @property
        def parsed_data(self):
            return self.tree

    def dataextration_factory(filepath):
        if filepath.endswith('.json'):
            extractor = JSONDataExtractor(filepath)
        elif filepath.endswith('.xml'):
            extractor = XMLDataExtractor(filepath)
        else:
            raise ValueError(f'Cannot extract data from {filepath}')
        return extractor
    
    def extract_data_from(filepath):
        factory = None
        try:
            factory = dataextration_factory(filepath)
        except Exception as e:
            print(e)
        return factory
    
    sqlite_factory = extract_data_from('myfile/person.sq3')

    json_factory = extract_data_from('myfile/movies.json')
    json_data = json_factory.parsed_data
    print(json_data)

    xml_factory = extract_data_from('myfile/persons.xml')
    xml_data = xml_factory.parsed_data
    smiths = xml_data.findall('.//person[lastName="Smith"]')
    print(f'found: {len(smiths)} persons')


def pattern_abstract_factory():
    """
    instance in real life: 
    1. car manufacture, use the same machine to make
    diff components; 2. django support testing package to build
    django model
    
    example:
    change app behavior while runing, such as view style
    
    some factory method set, every method generate diff obj
    can improve performance of RAM
    """
    class Frog:
        def __init__(self, name):
            self.name = name
        
        def __str__(self):
            return self.name

        def interact_with(self, obstacle):
            act = obstacle.action()
            msg = f'{self} the Frog encounters {obstacle} and {act}! '
            print(msg)

    class Bug:
        def __str__(self):
            return 'a bug'

        def action(self):
            return 'eats it'

    class FrogWorld:
        """
        abstract factory
        """
        def __init__(self, name):
            print(self)
            self.player_name = name

        def __str__(self):
            return '\n\n----- Frog World -----'

        def make_character(self):
            return Frog(self.player_name)

        def make_obstacle(self):
            return Bug()

    class Wizard:
        def __init__(self, name):
            self.name = name
        
        def __str__(self):
            return self.name

        def interact_with(self, obstacle):
            act = obstacle.action()
            msg = f'{self} the Wizard battles against {obstacle} and {act}! '
            print(msg)

    class Ork:
        def __str__(self):
            return 'an evil ork'

        def action(self):
            return 'kills it'

    class WizardWorld:
        def __init__(self, name):
            print(self)
            self.player_name = name

        def __str__(self):
            return '\n\n----- Wizard World -----'

        def make_character(self):
            return Wizard(self.player_name)

        def make_obstacle(self):
            return Ork()

    class GameEnvironment:
        def __init__(self, factory):
            self.hero = factory.make_character()
            self.obstacle = factory.make_obstacle()

        def play(self):
            self.hero.interact_with(self.obstacle)

    def validate_age(name):
        try:
            age = input(f'Welcome {name}. How old are you?')
            age = int(age)
        except ValueError:
            print(f'Age {name} is invalid, please try again...')
            return (False, age)

        return (True, age)

    def main_func():
        name = input("Hello, What's your name?")
        valid_input = False
        while not valid_input:
            valid_input, age = validate_age(name)

        game = FrogWorld if age < 18 else WizardWorld
        environment = GameEnvironment(game(name))
        environment.play()

    main_func()


def pattern_builder():
    """
    creative pattern

    instance in real life: 
    fast food shop make diff hamburg, although display type is diff,
    but the process is the same, cashier is the director and staff is
    the builder who deal with order
    
    example:
    html: contain diff components such as head, head,
    every builder build diff components, and director
    can use this components to build diff html page

    the third django package: django-query-builder: build diff
    part of sql dynamic

    diff with factory-pattern: 
    factory: build obj in one process
    builder: build obj in multiple process

    introduction:
    build a obj in multiple process
    director call builder to build obj

    usage:
    1. create complex obj with diff step
    2. need diff style of obj with the same progress
    3. create obj at some time and visit it later
    """

    # factory-pattern
    MINI14 = '1.4HZ Mac mini'
    class AppleFactory:
        class MacMini14:
            def __init__(self):
                self.memory = 4
                self.hdd = 500
                self.gpu = 'Intel HD Graphics 5000'
            
            def __str__(self):
                info = (
                    f'Model: {MINI14}',
                    f'Memory: {self.memory}GB',
                    f'Hard Disk: {self.hdd}GB',
                    f'Graphics Card: {self.gpu}'
                )
                return '\n'.join(info)

        def build_computer(self, model):
            if model == MINI14:
                return self.MacMini14()
            else:
                msg = f"I don't know how to build {model}"
                print(msg)

    class Computer:
        def __init__(self, serial_number):
            self.serial = serial_number
            self.memory = None
            self.hdd = None
            self.gpu = None
        
        def __str__(self):
            info = (
                    f'Memory: {self.memory}GB',
                    f'Hard Disk: {self.hdd}GB',
                    f'Graphics Card: {self.gpu}'
                )
            return '\n'.join(info)

    class ComputerBuilder:
        def __init__(self):
            self.computer = Computer('AG28593759')

        def configure_memory(self, amount):
            self.computer.memory = amount
        
        def configure_hdd(self, amount):
            self.computer.hdd = amount

        def configure_gpu(self, gpu_model):
            self.computer.gpu = gpu_model

    class HardWareEngineer:
        def __init__(self):
            self.builder = None
        
        def construct_computer(self, memory, hdd, gpu):
            self.builder = ComputerBuilder()
            steps = (
                self.builder.configure_memory(memory),
                self.builder.configure_hdd(hdd),
                self.builder.configure_gpu(gpu)
            )
            [step for step in steps]

        @property
        def computer(self):
            return self.builder.computer

    # factory-pattern
    # afac = AppleFactory()
    # mac_mini = afac.build_computer(MINI14)  
    # print('factory:')
    # print(mac_mini)

    # builder-pattern
    # engineer = HardWareEngineer()
    # engineer.construct_computer(hdd=500, memory=8, 
    # gpu='GeForce GTX 850 Ti')
    # computer = engineer.computer
    # print('builder:')
    # print(computer)

    from enum import Enum
    import time

    # define constant
    PizzaProgress = Enum('PizzaProgress', 'queued preparation baking ready')
    PizzaDough = Enum('PizzaDough', 'thin thick')
    PizzaSauce = Enum('PizzaSauce', 'tomato creme_fraiche')
    PizzaTopping = Enum('PizaaTopping', 'mozzarella double_mozzarella bacon\
     ham mushrooms red_onion oregano')
    STEP_DELAY = 3

    class Pizza:
        def __init__(self, name):
            self.name = name
            self.dough = None
            self.sauce = None
            self.topping = []

        def __str__(self):
            return self.name

        def prepare_dough(self, dough):
            self.dough = dough
            print(f'preparing the {self.dough.name} dough of your {self}...')
            time.sleep(STEP_DELAY)
            print(f'done with the {self.dough.name} dough')

    class MargaritaBuilder:
        def __init__(self):
            self.pizza = Pizza('margarita')
            self.progress = PizzaProgress.queued
            self.baking_time = 5

        def prepare_dough(self):
            self.progress = PizzaProgress.preparation
            self.pizza.prepare_dough(PizzaDough.thin)
        
        def add_sauce(self):
            print('adding the tomato sauce to your margarita...')
            self.pizza.sauce = PizzaSauce.tomato
            time.sleep(STEP_DELAY)
            print('done with tomato sauce')

        def add_topping(self):
            topping_desc = 'double mozzarella, oregano'
            topping_items = (PizzaTopping.double_mozzarella, PizzaTopping.oregano)
            print(f'adding the topping ({topping_desc}) to your margarita')
            self.pizza.topping.append([t for t in topping_items])
            time.sleep(STEP_DELAY)
            print(f'done with the topping({topping_desc}) ')

        def bake(self):
            self.progress = PizzaProgress.baking
            print(f'baking your margarita for {self.baking_time} seconds')
            time.sleep(self.baking_time)
            self.progress = PizzaProgress.ready
            print('your margarita is ready')

    class CremyBaconBuilder:
        def __init__(self):
            self.pizza = Pizza('creamy bacon')
            self.progress = PizzaProgress.queued
            self.baking_time = 7

        def prepare_dough(self):
            self.progress = PizzaProgress.preparation
            self.pizza.prepare_dough(PizzaDough.thick)
        
        def add_sauce(self):
            print('adding the creme fraiche sauce to your creamy bacon')
            self.pizza.sauce = PizzaSauce.creme_fraiche
            time.sleep(STEP_DELAY)
            print('done with creme fraiche sauce')

        def add_topping(self):
            topping_desc = 'mozzarella, bacon, ham, mushrooms, red onion, oregano'
            topping_items = (PizzaTopping.mozzarella, PizzaTopping.bacon, 
            PizzaTopping.ham, PizzaTopping.mushrooms, PizzaTopping.red_onion,
            PizzaTopping.oregano)
            print(f'adding the topping ({topping_desc}) to your creamy bacon')
            self.pizza.topping.append([t for t in topping_items])
            time.sleep(STEP_DELAY)
            print(f'done with the topping({topping_desc}) ')

        def bake(self):
            self.progress = PizzaProgress.baking
            print(f'baking your creamy bacon for {self.baking_time} seconds')
            time.sleep(self.baking_time)
            self.progress = PizzaProgress.ready
            print('your creamy bacon is ready')

    class Waiter:
        def __init__(self):
            self.builder = None

        def construct_pizza(self, builder):
            self.builder = builder
            steps = (
                builder.prepare_dough,
                builder.add_sauce,
                builder.add_topping,
                builder.bake
            )
            [step() for step in steps]

        @property
        def pizza(self):
            return self.builder.pizza


    class Pizza2:
        def __init__(self, builder):
            self.garlic = builder.garlic
            self.extra_cheese = builder.extra_cheese

        def __str__(self):
            garlic = 'yes' if self.garlic else 'no'
            extra_cheese = 'yes' if self.extra_cheese else 'no'
            info = (
                f'Garlic: {garlic}',
                f'Extrac cheese: {extra_cheese}'
            )
            return '\n'.join(info)

        class PizzaBuilder:
            def __init__(self):
                self.extra_cheese = False
                self.garlic = False

            def add_garlic(self):
                self.garlic = True
                return self

            def add_extra_cheese(self):
                self.extra_cheese = True
                return self

            def build(self):
                return Pizza2(self)

    def validate_style(builders):
        try:
            input_msg = 'What pizza would you like, [m]argarita or [c]reamy bacon?'
            pizza_style = input(input_msg)
            builder = builders[pizza_style]()
        except KeyError:
            error_msg = 'Sorry, margarita(key m) and creamy bacon(key c)\
            are available'
            print(error_msg)
            return (False, None)
        return (True, builder)

    def main_func():
        builders = dict(m=MargaritaBuilder, c=CremyBaconBuilder)
        valid_input = False
        while not valid_input:
            valid_input, builder = validate_style(builders)
        print()

        waiter = Waiter()
        waiter.construct_pizza(builder)
        pizza = waiter.pizza
        print()
        print(f'Enjoy your {pizza}!')

    def main_func2():
        # chain call
        # smooth builder
        pizza = Pizza2.PizzaBuilder().add_garlic().add_extra_cheese().build()
        print(pizza)

    main_func()
    main_func2()


def pattern_prototype():
    """
    creative type

    instant in real life:
    1. ppt need diff language version, can copy from original
    source and just modify its language
    2. cloned sheep dory

    usage:
    1. we want another obj that keep original's most features and modify some
    attr on it
    """

    class Website:
        def __init__(self, name, domain, description, author, **kwargs):
            self.name = name
            self.domain = domain
            self.description = description
            self.author = author
            for key in kwargs:
                setattr(self, key, kwargs[key])

        def __str__(self):
            summary = [f'Website "{self.name}"\n',]
            infos = vars(self).items()
            ordered_infos = sorted(infos)
            for attr, val in ordered_infos:
                if attr == 'name':
                    continue
                summary.append(f'{attr}: {val}\n')
            return ''.join(summary)

    import copy

    class Prototype:
        def __init__(self):
            self.objects = dict()

        # order to track obj
        def register(self, identifier, obj):
            self.objects[identifier] = obj

        def unregister(self, identifier):
            del self.objects[identifier]

        def clone(self, identifier, **attrs):
            found = self.objects[identifier]
            if not found:
                raise ValueError(f'Incorrect object identifier: {identifier}')
            obj = copy.deepcopy(found)
            for key in attrs:
                setattr(obj, key, attrs[key])

            return obj

    def main_func():
        keywords = ('python', 'data', 'apis', 'automation')
        site1 = Website('ContentGardening',
        domain='contentgardening.com',
        description='Automation and data-driven apps',
        author='tbq',
        keywords=keywords)
        prototype = Prototype()
        identifier = 't-b-1'
        prototype.register(identifier, site1)
        site2 = prototype.clone(identifier,
        name='ContentGardeningPlayground',
        domain='play.contentgardening.com',
        description='Experimentation for techniques featured on the blog',
        category='Membership site',
        create_date='2021-01-24')
        
        for site in (site1, site2):
            print(site)

        print(f'ID site1: {id(site1)} != ID site2: {id(site2)}')

    main_func()


def pattern_singleton():
    """
    creative type
    instance in real life:
    Plone CMS website: every tool is singleton, such as dir tool
    you can't build another instance in any place, it is global

    usage:
    1. create only one obj or need obj that perserve app global status
    2. control visit source concurrently, such as class that connnect to db
    3. horizontal service that vist is via diff part or diff user
    """
    import urllib.parse
    import urllib.request

    class URLFetcher:
        def __init__(self):
            self.urls = []

        def fetch(self, url):
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.code == 200:
                    the_page = response.read()
                    print(the_page)
                    urls = self.urls
                    urls.append(url)
                    self.urls = urls

    # print(URLFetcher() is URLFetcher())

    # achieve singleton through meta lcass
    class SingletonType(type):
        _instances = {}
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls._instances[cls]

    class URLFetcher2(metaclass=SingletonType):
        def __init__(self):
            self.urls = []

        def fetch(self, url):
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.code == 200:
                    the_page = response.read()
                    print(len(the_page))
                    urls = self.urls
                    urls.append(url)
                    self.urls = urls
        
        def dump_url_registry(self):
            return ', '.join(self.urls)

    def main_func():
        MY_URLS = ['https://www.baidu.com/',
        'https://www.runoob.com/',
        'https://www.douban.com/',
        'https://github.com/']

        print(URLFetcher2() is URLFetcher2())

        fetcher = URLFetcher2()
        for url in MY_URLS:
            try:
                fetcher.fetch(url)
            except Exception as e:
                print(e)
        print('-'*6)
        done_urls = fetcher.dump_url_registry()
        print(f'Done urls: {done_urls}')

    main_func()


def pattern_adapter():
    """
    structure pattern
    instance in real life:
    1. usb adapter to charge your device if diff country
    2. ZCA

    usage:
    1. adapt two apis that uncompatible, cannot modify their source code
    2. use external api or old api
    """
    class Club:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return f'the club {self.name}'

        def organize_event(self):
            return 'hires a artist to perform to the people'

    def external():
        class Musician:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return f'the musician {self.name}'

            def play(self):
                return 'play music'

        class Dancer:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return f'the dancer {self.name}'

            def dance(self):
                return 'does a dance performance'

        return Musician, Dancer

    Musician, Dancer = external()

    class Adapter:
        def __init__(self, obj, adapted_methods):
            self.obj = obj
            self.__dict__.update(adapted_methods)

        def __str__(self):
            return str(self.obj)

    def main_func():
        objects = [Club('Player1'), Musician('Player2'), Dancer('Player3')]
        for obj in objects:
            if hasattr(obj, 'play') or hasattr(obj, 'dance'):
                if hasattr(obj, 'play'):
                    adapted_methods = dict(organize_event=obj.play)
                elif hasattr(obj, 'dance'):
                    adapted_methods = dict(organize_event=obj.dance)
                obj = Adapter(obj, adapted_methods)
            print(f'{obj} {obj.organize_event()}')

    main_func()


def pattern_decorator():
    """
    structure pattern
    
    instance in real life:
    1. upload silencer to gun
    2. use diff lens in camera
    3. django: limit to visit view, cache in view
    4. Pyramid: register function to subcriber

    example:
    crosscut focus point:
    1. data auth
    2. cache
    3. login
    4. monitor
    5. debug
    6. business rule
    7. encryption
    gui:
    1. add border
    2. add shadow

    usage:
    1. expand function, class
    """
    from timeit import Timer

    global number_sum

    def number_sum(n):
        assert(n >= 0), 'n must be >= 0'
        if n == 0:
            return 0
        else:
            return n + number_sum(n-1)

    # t = Timer('number_sum(30)', 'from __main__ import number_sum')
    # print('Timer: ', t.timeit())

    global number_sum2

    # use cache will more quick
    sum_cache = {0:0}
    def number_sum2(n):
        assert(n >= 0), 'n must be >= 0'
        if n in sum_cache:
            return sum_cache[n]
        res = n + number_sum2(n-1)
        sum_cache[n] = res
        return res

    # t = Timer('number_sum2(300)', 'from __main__ import number_sum2')
    # print('Timer: ', t.timeit())

    cache_fib = {0:0}
    def fibonacci(n):
        assert(n >= 0), 'n must be >= 0'
        if n in cache_fib:
            return cache_fib[n]
        res = fibonacci(n-1) + fibonacci(n-2)
        cache_fib[n] = res
        return res

    import functools

    def memoize(fn):
        cache = dict()

        @functools.wraps(fn)
        def memoizer(*args):
            if args not in cache:
                cache[args] = fn(*args)
            return cache[args]

        return memoizer

    global number_sum3

    @memoize
    def number_sum3(n):
        'return the sum of n'
        assert(n >= 0), 'n must be >= 0'
        if n == 0:
            return 0
        else:
            return n + number_sum3(n-1)

    global fibonacci2

    @memoize
    def fibonacci2(n):
        'return the n numer of fibonacci sequence'
        assert(n >= 0), 'n must be >= 0'
        if n in (0, 1):
            return n
        else:
            return fibonacci2(n-1) + fibonacci2(n-2)

    def main_func():
        to_execute = [
            (
                number_sum3, 
                Timer('number_sum3(100)', 'from __main__ import number_sum3'),

            ),
            (
                fibonacci2,
                Timer('fibonacci2(100)', 'from __main__ import fibonacci2'),
            )
        ]
        for item in to_execute:
            fn = item[0]
            print(f'Function "{fn.__name__}": {fn.__doc__}')
            t = item[1]
            print('Time:', t.timeit())
            print()

    main_func()


def pattern_bridge():
    """
    structure pattern

    instance in real life:
    1. infoproduct: support diff format product such as
    PDF, ebook, video
    2. software domain: device supplier support driver
    according to os api

    usage:
    1. share between muitiple obj
    2. diff with adapter pattern: define abstrct and implementation advance
    """
    class ResourceContent:
        def __init__(self, imp):
            self._imp = imp

        def show_content(self, path):
            self._imp.fetch(path)

    import abc
    import urllib.request

    class ResourceContentFetcher(metaclass=abc.ABCMeta):
        @abc.abstractclassmethod
        def fetch(self, path):
            pass

    class URLFetcher(ResourceContentFetcher):
        def fetch(self, path):
            req = urllib.request.Request(path)
            with urllib.request.urlopen(req) as response:
                if response.code == 200:
                    the_page = response.read()
                    print(the_page)

    class LocalFileFetcher(ResourceContentFetcher):
        def fetch(self, path):
            with open(path) as f:
                print(f.read())

    def main_func():
        url_fetcher = URLFetcher()
        iface = ResourceContent(url_fetcher)
        iface.show_content('http://python.org')

        print('='*10)

        localfs_fetcher = LocalFileFetcher()
        iface = ResourceContent(localfs_fetcher)
        iface.show_content(f'myfile/movies.json')

    main_func()


def pattern_appearance():
    """
    structure pattern

    instance in real life:
    1. customer call to server, chain between these is appearance
    2. car key
    3. start button of computer
    4. django-oscar-dataCash

    usage:
    1. show the simple api to user and hide the complex implement
    """
    from enum import Enum
    from abc import ABCMeta, abstractclassmethod

    State = Enum('State', 'new running sleeping restart zombie')
    
    class Server(metaclass=ABCMeta):
        @abstractclassmethod
        def __init__(self):
            pass

        def __str__(self):
            return self.name

        @abstractclassmethod
        def boot(self):
            pass

        @abstractclassmethod
        def kill(self, restart=True):
            pass

    class User:
        pass

    class File:
        pass

    class Process:
        pass

    class FileServer(Server):
        def __init__(self):
            self.name = 'FileServer'
            self.state = State.new

        def boot(self):
            print(f'booting the {self}')
            self.state = State.running

        def kill(self, restart=True):
            print(f'Killing {self}')
            self.state = State.restart if restart else State.zombie

        def create_file(self, user, name, permissions):
            print(f'trying to create the file "{name}" user\
             "{user}" with permissions {permissions}')
            
    class ProcessServer(Server):
        def __init__(self):
            self.name = 'ProcessServer'
            self.state = State.new

        def boot(self):
            print(f'booting the {self}')
            self.state = State.running

        def kill(self, restart=True):
            print(f'Killing {self}')
            self.state = State.restart if restart else State.zombie

        def create_process(self, user, name):
            print(f'trying to create the process "{name}" for user\
             "{user}"')

    class WindowServer:
        pass

    class NetworkServer:
        pass

    class OperatingSystem:
        def __init__(self):
            self.fs = FileServer()
            self.ps = ProcessServer()
        
        def start(self):
            [i.boot() for i in (self.fs, self.ps)]

        def create_file(self, user, name, permissions):
            return self.fs.create_file(user, name, permissions)

        def create_process(self, user, name):
            return self.ps.create_process(user, name)

    def main_func():
        os = OperatingSystem()
        os.start()
        os.create_file('foo', 'hello', '-rw-r-r')
        os.create_process('bar', 'ls /tmp')

    main_func()


def pattern_flyweight():
    """
    structure pattern

    instance in real life:
    1. fetch book from booksheft, if not found, ask seller to help you
    2. Exaile music player use flyweight reuse obj that has the same url
    3. Peppy save main mode status bar
    4. game: all soldier have the same appearance, can save this data
    use flyweight 

    usage:
    1. share obj: only contain independent, unchange data
    2. if flyweight need external data, should supply by user explicit
    3. improve performance and raw usage rate
    4. * app need many obj; * not depend on obj id and don't care that
    * too many obj, if remove variable status, should supply by app, muitiple
    group obj can replace by few share obj
    """
    
    import random
    from enum import Enum

    class Car:
        pool = dict()
        def __new__(cls, car_type):
            obj = cls.pool.get(car_type, None)
            if not obj:
                obj = object.__new__(cls)
                cls.pool[car_type] = obj
                obj.car_type = car_type
            return obj

        def render(self, color, x, y):
            type = self.car_type
            msg = f'render a car of type {type} and color \
            {color} at ({x}, {y})'
            print(msg)
    
    def main_func():
        CarType = Enum('CarType', 'subcompact compact suv')
        rnd = random.Random()
        colors = colors = 'white black silver gray red blue \
        brown beige yellow'.split(' ')
        min_point, max_point = 0, 100
        car_counter = 0

        for _ in range(10):
            cl = Car(CarType.subcompact)
            cl.render(random.choice(colors), rnd.randint(min_point, max_point),
            random.randint(min_point, max_point))
            car_counter += 1

        for _ in range(3):
            cl = Car(CarType.compact)
            cl.render(random.choice(colors), rnd.randint(min_point, max_point),
            random.randint(min_point, max_point))
            car_counter += 1

        for _ in range(5):
            cl = Car(CarType.suv)
            cl.render(random.choice(colors), rnd.randint(min_point, max_point),
            random.randint(min_point, max_point))
            car_counter += 1

        print(f'car rendered: {car_counter}')
        print(f'cars actually created: {len(Car.pool)}')

        c4 = Car(CarType.subcompact)
        c5 = Car(CarType.subcompact)
        c6 = Car(CarType.suv)
        print(f'{id(c4)} == {id(c5)}? {id(c4) == id(c5)}')
        print(f'{id(c5)} == {id(c6)}? {id(c5) == id(c6)}')

    main_func()


def pattern_mvc():
    """
    structure pattern
    
    instance in real life:
    1. waiter accept order and serve
    2. Web2py
    3. Django(MTV)

    example:
    1. Django, Rails, Symfon, iPhone SDK, Android, QT

    advantage:
    1. separate view and model
    2. modify one part and not affect other
    3. easy to maintain
    
    intelligent model:
    1. contain auth/biz rule/logic
    2. deal app status
    3. visit app data(database, cloud)
    4. independent from UI

    Slim controller:
    1. update model while interact with user
    2. update view while model modify
    3. deal data before pass data to model/view if neccessary
    4. no show data
    5. no visit app data directly
    6. no contain auth/biz rule/logic

    fool view:
    1. show data
    2. allow interact with user
    3. minimize dealing
    4. no save any data
    5. no visit app data directly
    6. no contain auth/biz rule/logic

    if mvc achieve?:
    1. if your app have gui, if it can change skin convenient
    2. if your app havn't gui, if it can add gui easily
    """
    quotes = (
        "It wasn't raining when Noah built the ark.",
        "Champions keep playing util they get it right.",
        "Genius is 1% inspiration, 99% is perspiration.",
        "You must be the change you wish to see in the world.",
        "I nerver dream of success, I worked for it."
    )

    class QuoteModel:
        def get_quo(self, n):
            try:
                value = quotes[n]
            except IndexError:
                value = 'Not found!'
            return value

    class QuoteTerminalView:
        def show(self, quote):
            print(f'And the quote is: "{quote}"')

        def errors(self, msg):
            print(f'Error: {msg}')

        def select_quote(self):
            return input('Which quote number would you like to see?')

    class QuoteTerminalController:
        def __init__(self):
            self.model = QuoteModel()
            self.view = QuoteTerminalView()

        def run(self):
            valid_input = False
            while not valid_input:
                try:
                    n = self.view.select_quote()
                    n = int(n)
                    valid_input = True
                except ValueError:
                    self.view.errors(f"Incorrect index '{n}'")
            quote = self.model.get_quo(n)
            self.view.show(quote)
            
    def main_func():
        controller = QuoteTerminalController()
        while True:
            controller.run()

    main_func()


def pattern_proxy():
    """
    struture pattern
    
    instance in real life:
    1: debit card, auth need pass

    four type proxy:
    1. remote proxy: 1.1: in distribute sys, can create a proxy
    to act the remote obj; 1.2: ORM: act as the agent of database
    2. virtual proxy
    3. protection proxy
    4. intelligent proxy: hide the complexity of thread safety
    """


def pattern_virtual_proxy():
    """
    strucure pattern

    example:
    1. graphics init

    usage:
    1. delay to init
    2. instance layer init
    3. class or module layer init
    """

    class LaxyProperty:
        def __init__(self, method):
            self.method = method
            self.method_name = method.__name__
            print(f'function overriden: {self.method}')
            print(f"function's name: {self.method_name}")

        # regard a method as a simple attr
        def __get__(self, obj, cls):
            if not obj:
                return None
            value = self.method(obj)
            print(f'value {value}')
            setattr(obj, self.method_name, value)
            return value

    class Test:
        def __init__(self):
            self.x = 'foo'
            self.y = 'bar'
            self._resource = None

        # initializing only one
        @LaxyProperty
        def resource(self):
            print(f'initializing self._resource which is {self._resource}')
            self._resource = tuple(range(5))
            return self._resource

    def main_func():
        t = Test()
        print(t.x)
        print(t.y) 
        print(t.resource)
        print(t.resource)

    main_func()


def pattern_protection_proxy():
    """
    struture pattern

    usage:
    1. visit some source that need auth
    """
    class SensitiveInfo:
        def __init__(self):
            self.users = ['nick', 'tom', 'ben', 'jane']
        
        def read(self):
            nb = len(self.users)
            print(f"There are {nb} users: {' '.join(self.users)}")

        def add(self, user):
            self.users.append(user)
            print(f'Added user {user}')

    class Info:
        def __init__(self):
            self.protected = SensitiveInfo()
            self.secret = '123'

        def read(self):
            self.protected.read()

        def add(self, user):
            sec = input('what is the secret?')
            self.protected.add(user) if sec == self.secret else \
            print("That's wrong")

    def main_func():
        info = Info()
        while True:
            print('1. read list |==| 2.add user |==| 3.quit')
            key = input('choose option: ')
            if key == '1':
                info.read()
            elif key == '2':
                name = input('choose username: ')
                info.add(name)
            elif key == '3':
                exit()
            else:
                print('unknown option: {key}')

    main_func()


def pattern_responsibility_chain():
    """
    behavioral pattern

    instance in real life:
    1. ATM: withdrawal through one slot but it distribute diff
    slot to deal
    2. java servlet: http request filter chain
    3. Apple Cocoa framework: view meet the unknown event
    and will forward to its parent's view
    4. purchase sys: diff approve institute can only approve
    specified cash amount 

    usage:
    1. send req to the first obj->is satisfied this req?
    ->forward to next obj->..>chain end
    2. if can't foresee all method that satisfy req
    """
    class Event:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return self.name

    class Widget:
        def __init__(self, parent=None):
            self.parent = parent

        def handle(self, event):
            handler = f'handle_{event}'
            if hasattr(self, handler):
                method = getattr(self, handler)
                method(event)
            elif self.parent is not None:
                self.parent.handle(event)
            elif hasattr(self, 'handle_default'):
                self.handle_default(event)
        
    class MainWindow(Widget):
        def handle_close(self, event):
            print(f'MainWindow: {event}')

        def handle_default(self, event):
            print(f'MainWindow default: {event}')

    class SendDialog(Widget):
        def handle_paint(self, event):
            print(f'SendDialog: {event}')

    class MsgText(Widget):
        def handle_down(self, event):
            print(f'MsgText: {event}')

    def main_func():
        mw = MainWindow()
        sd = SendDialog(mw)
        msg = MsgText(sd)

        for e in ('down', 'paint', 'unhandled', 'close'):
            evt = Event(e)
            print(f'Sending event -{evt}- to MainWindow')
            mw.handle(evt)
            print(f'Sending event -{evt}- to SendDialog')
            sd.handle(evt)
            print(f'Sending event -{evt}- to MsgText')
            msg.handle(evt)

    main_func()


def pattern_cmd():
    """
    instance in real life:
    1. order in restaurance, order paper is a cmd
    2. PyQt: QAction class, regard an action as a cmd
    3. Git Cola: use cmd mode to modify model

    example:
    1. undo
    2. GUI button, menu
    3. other: cut, copy, paste, restore, captalize
    4. transaction and log
    5. Macro: record and execute when need

    usage:
    1. execute cmd at any time and no need execute when create
    2. client that execute cmd no need know any detail of cmd
    3. grouping cmd and execute them in order
    """
    import os
    verbose = True

    class RenameFile:
        def __init__(self, src, dest):
            self.src = src
            self.dest = dest

        def execute(self):
            if verbose:
                print(f"renaming '{self.src}' to '{self.dest}'")
                try:
                    os.rename(self.src, self.dest)
                except FileExistsError as e:
                    os.remove(self.src)

        def undo(self):
            if verbose:
                print(f"renaming '{self.dest}' back to '{self.src}'")
            os.rename(self.dest, self.src)

    def delete_file(path):
        if verbose:
            print(f"deleting file {path}")
        os.remove(path)

    class CreateFile:
        def __init__(self, path, txt='hell world\n'):
            self.path = path
            self.txt = txt

        def execute(self):
            if verbose:
                print(f"[creating file '{self.path}']")
            with open(self.path, mode='w', encoding='utf-8') as out_file:
                out_file.write(self.txt)

        def undo(self):
            delete_file(self.path)

    class ReadFile:
        def __init__(self, path):
            self.path = path

        def execute(self):
            if verbose:
                print(f"[reading file '{self.path}']")
            with open(self.path, mode='r', encoding='utf-8') as in_file:
                print(in_file.read(), end='')

    def main_func():
        ori_name, new_name = 'myfile/file1', 'myfile/file2'
        commands = (
            CreateFile(ori_name),
            ReadFile(ori_name),
            RenameFile(ori_name, new_name)
        )
        [c.execute() for c in commands]
        answer = input('reverse the executed command? [y/n] ')
        if answer not in 'Yy':
            print(f"the result is {new_name}")
            exit()
        for c in  reversed(commands):
            try:
                c.undo()
            except AttributeError as e:
                print("Error", str(e))

    main_func()

def pattern_observer():
    """
    instance in real life:
    1. auctioneer notify newest price to bidder
    2. Kivy framework: Properties: action when property
    changed
    3. RabbitMQ: publisher->subcribers
    4. RSS, Atom, social nerwork
    5. listener listen to event

    usage:
    1. when an obj status change then notify a group obj
    """
    class Publisher:
        def __init__(self):
            self.observers = []

        def add(self, observer):
            if observer not in self.observers:
                self.observers.append(observer)
            else:
                print(f"Failed to add: {observer}")

        def remove(self, observer):
            try:
                self.observers.remove(observer)
            except ValueError:
                print(f"Failed to remove: {observer}")

        def notify(self):
            [o.notify(self) for o in self.observers]

    class DefaultFormatter(Publisher):
        def __init__(self, name):
            Publisher.__init__(self)
            self.name = name
            self._data = 0

        def __str__(self):
            return f"{type(self).__name__}: '{self.name}' \
            has data = {self._data}"

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, new_value):
            try:
                self._data = int(new_value)
            except ValueError as e:
                print(f"Error: {e}")
            else:
                self.notify()

    class HexFormatterObs:
        def notify(self, publisher):
            value = hex(publisher.data)
            print(f"{type(self).__name__}: '{publisher.name}' has now hex data = {value}")

    class BinaryFormatterObs:
        def notify(self, publisher):
            value = bin(publisher.data)
            print(f"{type(self).__name__}: '{publisher.name}' has now bin data = {value}")

    def main_func():
        df = DefaultFormatter('test1')
        print(df)

        print()
        hf = HexFormatterObs()
        df.add(hf)
        df.data = 3
        print(df)

        print()
        bf = BinaryFormatterObs()
        df.add(bf)
        df.data = 21
        print(df)

        print()
        df.remove(hf)
        df.data = 40
        print(df)

        print()
        df.remove(hf)
        df.add(bf)

        df.data = 'hello'
        print(df)

        print()
        df.data = 15.8
        print(df)

    main_func()


def pattern_state():
    """
    behavioral pattern    

    instance in real life:
    1. vending machine: response according to our selection
    and money
    2. django-fsm
    3. SMC: state machine complier

    example:
    1. os process model
    2. program languge complier
    3. event drive os: computer game: monster
    change its status when role close to them

    usage:
    1. state diagram: every node is a state,
    every line is a transition
    2. state transit when specified event happened
    """

    from state_machine import (State, Event, acts_as_state_machine,
    after, before, InvalidStateTransition)

    @acts_as_state_machine
    class Process:
        created = State(initial=True)
        waiting = State()
        running = State()
        terminated = State()
        blocked = State()
        swapped_out_waiting = State()
        swapped_out_blocked = State()

        wait = Event(from_states=(
            created,
            running,
            blocked,
            swapped_out_waiting
        ),
        to_state=waiting)
        run = Event(from_states=waiting, to_state=running)
        terminate = Event(from_states=waiting, to_state=terminated)
        block =  Event(from_states=(running, swapped_out_waiting),
        to_state=blocked)
        swap_wait = Event(from_states=waiting, to_state=swapped_out_waiting)
        swap_block = Event(from_states=blocked, to_state=swapped_out_blocked)

        def __init__(self, name):
            self.name = name

        @after('wait')
        def wait_info(self):
            print(f'{self.name} entered waiting mode')

        @after('run')
        def run_info(self):
            print(f'{self.name} is running')

        @after('terminate')
        def terminate_info(self):
            print(f'{self.name} terminated')

        @after('block')
        def block_info(self):
            print(f'{self.name} is blocked')

        @after('swap_wait')
        def swap_wait_info(self):
            print(f'{self.name} is swapped out and waiting')

        @after('swap_block')
        def swap_block_info(self):
            print(f'{self.name} is swapped out and blocked')

    def transition(process, event, event_name):
        try:
            event()
        except InvalidStateTransition as err:
            print(f'Error: transition of {process.name} \
            from {process.current_state} to {event_name} failed')

    def state_info(process):
        print(f'state of {process.name}: {process.current_state}')

    def main_func():
        RUNNING = 'running'
        WAITING = 'waiting'
        BLOCKED = 'blocked'
        TERMINATED = 'terminated'
        p1, p2 = Process('process1'), Process('process2')
        [state_info(p) for p in (p1, p2)]
        print()
        transition(p1, p1.wait, WAITING)
        transition(p2, p2.terminate, TERMINATED)
        [state_info(p) for p in (p1, p2)]
        print()
        transition(p1, p1.run, RUNNING)
        transition(p2, p2.wait, WAITING)
        [state_info(p) for p in (p1, p2)]
        print()
        transition(p2, p2.run, RUNNING)
        [state_info(p) for p in (p1, p2)]
        print()
        [transition(p, p.block, BLOCKED) for p in (p1, p2)]
        [state_info(p) for p in (p1, p2)]
        print()
        [transition(p, p.terminate, TERMINATED) for p in (p1, p2)]
        [state_info(p) for p in (p1, p2)]

    main_func()


def pattern_interpreter():
    """
    behavioral pattern

    instance in real life:
    1. musician: sheet music is music language, musician is the
    interpreter of this language
    2. C++: boot:spirit is inner DSL of parser
    3. Python: PyT

    example:
    1. suppor a simple language for expert to solve their problem

    usage:
    1. DSL: district special language
    """
    
    from pyparsing import (Word, OneOrMore, Optional, 
    Group, Suppress, alphanums)

    class Gate:
        def __init__(self):
            self.is_open = False

        def __str__(self):
            return 'open' if self.is_open else 'closed'

        def open(self):
            print('opening the gate')
            self.is_open = True

        def close(self):
            print('closing the gate')
            self.is_open = False

    class Garage:
        def __init__(self):
            self.is_open = False

        def __str__(self):
            return 'open' if self.is_open else 'closed'

        def open(self):
            print('opening the gate')
            self.is_open = True

        def close(self):
            print('closing the gate')
            self.is_open = False

    class Aircondition:
        def __init__(self):
            self.is_on = False

        def __str__(self):
            return 'on' if self.is_on else 'off'

        def turn_on(self):
            print('turning on the air condition')
            self.is_on = True

        def turn_off(self):
            print('turning off the air condition')
            self.is_on = False

    class Heating:
        def __init__(self):
            self.is_on = False

        def __str__(self):
            return 'on' if self.is_on else 'off'

        def turn_on(self):
            print('turning on the heating')
            self.is_on = True

        def turn_off(self):
            print('turning off the heating')
            self.is_on = False

    class Boiler:
        def __init__(self):
            self.temperature = 83

        def __str__(self):
            return f'boiler temperature: {self.temperature}'

        def increase_temperature(self, amount):
            print(f"increasing the boiler's temperature by {amount} degrees")
            self.temperature += amount

        def decrease_temperature(self, amount):
            print(f"decreasing the boiler's temperature by {amount} degrees")
            self.temperature -= amount

    class Fridge:
        def __init__(self):
            self.temperature = 2

        def __str__(self):
            return f'fridge temperature: {self.temperature}'

        def increase_temperature(self, amount):
            print(f"increasing the fridge's temperature by {amount} degrees")
            self.temperature += amount

        def decrease_temperature(self, amount):
            print(f"decreasing the fridge's temperature by {amount} degrees")
            self.temperature -= amount

    def main_func():
        word = Word(alphanums)
        command = Group(OneOrMore(word))
        token = Suppress('->')
        device = Group(OneOrMore(word))
        argument = Group(OneOrMore(word))
        event = command + token + device + Optional(token + argument)
        gate = Gate()
        garage = Garage()
        aircon = Aircondition()
        heating = Heating()
        boiler = Boiler()
        fridge = Fridge()

        tests = ('open -> gate',
        'close-> garage',
        'turn on -> air condition',
        'turn off -> heating',
        'increase -> boiler temperature -> 5 degrees',
        'decrease -> fridge temperature -> 2 degrees')

        open_actions = {'gate': gate.open,
        'garage': garage.open,
        'air condition': aircon.turn_on,
        'heating': heating.turn_on,
        'boiler temperature': boiler.increase_temperature,
        'fridge temperature': fridge.increase_temperature}

        close_actions = {'gate': gate.close,
        'garage': garage.close,
        'air condition': aircon.turn_off,
        'heating': heating.turn_off,
        'boiler temperature': boiler.decrease_temperature,
        'fridge temperature': fridge.decrease_temperature}

        for t in tests:
            # no arguments
            if len(event.parseString(t)) == 2:
                cmd, dev = event.parseString(t)
                cmd_str, dev_str = ' '.join(cmd), ' '.join(dev)
                if 'open' in cmd_str or 'turn on' in cmd_str:
                    open_actions[dev_str]()
                elif 'close' in cmd_str or 'turn off' in cmd_str:
                    close_actions[dev_str]()
            # has arguments
            elif len(event.parseString(t)) == 3:
                cmd, dev, arg = event.parseString(t)
                cmd_str, dev_str, arg_str = ' '.join(cmd), ' '.join(dev), ' '.join(arg)
                num_arg = 0
                try:
                    num_arg = int(arg_str.split()[0])
                except ValueError:
                    print(f"expected number but got: '{arg_str[0]}'")
                if 'increase' in cmd_str and num_arg > 0:
                    open_actions[dev_str](num_arg)
                elif 'decrease' in cmd_str and num_arg > 0:
                    close_actions[dev_str](num_arg)

    main_func()


def pattern_strategy():
    """
    behavioral pattern    

    instance in real life:
    1. catch a plane: save money: take bus, 
    have car: drive a car, other: take taxi
    2. python: sort func

    usage:
    1. use diff algorithm to achieve the same result
    2. diff formation output
    3. display data dynamically
    """

    import time

    def pairs(seq):
        n = len(seq)
        for i in range(n):
            yield seq[i], seq[(i + 1) % n]

    SLOW = 3
    LIMIT = 5
    WARNING = 'too bad, you picked the slow algorithm :('
    
    def allUniqueSort(s):
        if len(s) > LIMIT:
            print(WARNING)
            time.sleep(SLOW)

        strStr = sorted(s)
        for (c1, c2) in pairs(strStr):
            if c1 == c2:
                return False
        return True

    def allUniqueSet(s):
        if len(s) < LIMIT:
            print(WARNING)
            time.sleep(SLOW)
        return True if len(set(s)) == len(s) else False

    def allUnique(word, strategy):
        return strategy(word)

    def main_func():
        while True:
            word = None
            while not word:
                word = input('Insert word (type quit to exit)>')
                if word == 'quit':
                    print('bye')
                    return
                strategy_picked = None
                strategies = {'1': allUniqueSort, '2': allUniqueSet}
                while strategy_picked not in strategies.keys():
                    strategy_picked = input('Choose strategy: [1] Use a set, [2]\
                     Sort and pair> ')
                    try:
                        strategy = strategies[strategy_picked]
                        print(f'allUnique({word}): {allUnique(word, strategy)}')
                    except KeyError:
                        print(f'Incorrect option: {strategy_picked}')
    
    main_func()


def pattern_memorandum():
    """
    behavioral pattern

    instance in real life:
    1. language dictionary: sometime need inspect old version
    2. Zope database

    usage:
    1. supply cancal and restore function for user
    3. part: 1. memorandum; 2. sponser; 3.administrator
    """

    import pickle
    
    class Quote:
        def __init__(self, text, author):
            self.text = text
            self.author = author

        def save_state(self):
            current_state = pickle.dumps(self.__dict__)
            return current_state

        def restore_state(self, memento):
            previous_state = pickle.loads(memento)
            self.__dict__.clear()
            self.__dict__.update(previous_state)

        def __str__(self):
            return f'{self.text} - By {self.author}.'

    def main_func():
        print('Quote 1')
        q1 = Quote("A room without books is like a body without a soul.",
        'Unknown author')
        print(f'\nOriginal version:\n{q1}')
        q1_mem = q1.save_state()

        q1.author = 'Marcus Tullius Cicero'
        print(f'\nWe found the author, add did a upadted:\n{q1}')
        q1.restore_state(q1_mem)
        print(f'\nWe had to restore the previous version:\n{q1}')
        print()
        print('Quote 2')
        q2 = Quote("To be you in a word that is constantly trying to\
        make you be something else is the greatest accomplishment.",
        'Ralph Waldo Emerson')
        print(f'\nOriginal version:\n{q2}')
        q2_mem1 = q2.save_state()

        q2.text = "To be yourself in a word that is constantly trying to \
        make you something else is the greatest accomplishment."
        print(f'\nWe fixed the text:\n{q2}')
        q2_mem2 = q2.save_state()
        q2.text = "To be yourself when the world in constantly trying to\
        make you something else is the greatest accomplishment."
        print(f'\nWe fixed the text again:\n{q2}')
        q2.restore_state(q2_mem2)
        print(f'\nWe had to restore the 2nd version, the correct one:\n{q2}')

    main_func()

def pattern_iterator():
    """
    behavioral pattern

    instance in real life:
    1. fetch something from heap one by one
    2. teacher distributes book to students
    3. waiter order for every customer
    4. python iterator: list, tuple and so on

    usage:
    1. simplfy navigator of set
    2. fetch next obj of set at any point
    3. stop iter when complete
    """
    class FootballTeamIterator:
        def __init__(self, members):
            self.members = members
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.index < len(self.members):
                val = self.members[self.index]
                self.index += 1
                return val
            else:
                raise StopIteration()

    class FootballTeam:
        def __init__(self, members):
            self.members = members

        def __iter__(self):
            return FootballTeamIterator(self.members)

    def main_func():
        members = [f'player{str(x)}' for x in range(1, 23)]
        members = members + ['coach1', 'coach2']
        team = FootballTeam(members)
        team_it = iter(team)

        while True:
            print(next(team_it))

    main_func()

def pattern_template():
    """
    behavoiral pattern

    instance in real life:
    1. worker follow the same schedule, but
    diff with every part
    2. python: cmd module, asyncore module

    example:
    1. pagination
    2. graphic app

    usage:
    1. eliminate code repeat
    """

    from cowpy import cow

    def generate_banner(msg, style):
        print('-- start of banner --')
        print(style(msg))
        print('-- end of banner --nn')

    def dot_style(msg):
        msg = msg.capitalize()
        msg = '.' * 10 + msg + '.' * 10
        return msg

    def admire_style(msg):
        msg = msg.upper()
        return '!'.join(msg)

    def cow_style(msg):
        msg = cow.milk_random_cow(msg)
        return msg

    def main_func():
        styles = (dot_style, admire_style, cow_style)
        msg = 'happy coding'
        [generate_banner(msg, style) for style in styles]

    main_func()


def pattern_react_observer():
    """
    instance in real life:
    1. gather water flow
    2. behavoiral of app base in e-sheet:
    a grid changed will lead to re-evaluate relational formula
    3. ReactiveX: RxJava, RxPy, RxJS
    4. Angular framework

    usage:
    1. react for many event, event flow
    """
    from rx import Observable, Observer

    def example1():
        def get_quotes():
            import contextlib, io
            zen = io.StringIO()
            with contextlib.redirect_stdout(zen):
                import this
            quotes = zen.getvalue().split('\n')[1:]
            return quotes

        def push_quotes(obs):
            quotes = get_quotes()
            for q in quotes:
                if q:
                    obs.on_next(q)
            obs.on_completed()

        class ZenQuotesObserver(Observer):
            def on_next(self, value):
                print(f"Received: {value}")

            def on_completed(self):
                print('Done!')

            def on_error(self, error):
                print(f"Error occurred: {error}")

        source = Observable.create(push_quotes)
        source.subscribe(ZenQuotesObserver())

    def example2():
        def get_quotes():
            import contextlib, io
            zen = io.StringIO()
            with contextlib.redirect_stdout(zen):
                import this
            quotes = zen.getvalue().split('\n')[1:]
            return enumerate(quotes)

        zen_quotes = get_quotes()
        Observable.from_(zen_quotes)\
            .filter(lambda q: len(q[1]) > 0)\
            .subscribe(lambda value: print(f"Received: {value[0]} - {value[1]}"))

    def example3():
        def get_quotes():
            import contextlib, io
            zen = io.StringIO()
            with contextlib.redirect_stdout(zen):
                import this
            quotes = zen.getvalue().split('\n')[1:]
            return enumerate(quotes)

        zen_quotes = get_quotes()
        Observable.interval(5000)\
            .flat_map(lambda seq: Observable.from_(zen_quotes))\
            .flat_map(lambda q: Observable.from_(q[1].split()))\
            .filter(lambda s: len(s) > 2)\
            .map(lambda s: s.replace('.', '').replace(',', '')
            .replace('!', '').replace('-', ''))\
            .map(lambda s: s.lower())\
            .subscribe(lambda value: print(f"Received: {value}"))
        input("Stating... Press any key to quit\n")

    def peoplelist():
        from faker import Faker
        fake = Faker()

        persons = []
        for _ in range(0, 20):
            p = {'firstname': fake.first_name(),
            'lastname': fake.last_name()}
            persons.append(p)
        persons = iter(persons)
        
        new_data = [f"{p['firstname']} {p['lastname']}"
        for p in persons]
        new_data = ', '.join(new_data) + ', '

        with open('myfile/people.txt', 'a') as f:
            f.write(new_data)

    def example4():
        def firstnames_from_db(file_name):
            file = open(file_name)
            return Observable.from_(file)\
                .flat_map(lambda content: content.split(', '))\
                .filter(lambda name: name != '')\
                .map(lambda name: name.split()[0])\
                .group_by(lambda firstname: firstname)\
                .flat_map(lambda grp: grp.count().map(
                    lambda ct: (grp.key, ct)
                ))

        db_file = 'myfile/people.txt'
        Observable.interval(5000)\
            .flat_map(lambda i: firstnames_from_db(db_file))\
            .subscribe(lambda value: print(str(value)))
        input("Stating... Press any key to quit\n")

    def example5():
        def frequent_firstnames_from_db(file_name):
            file = open(file_name)
            return Observable.from_(file)\
                .flat_map(lambda content: content.split(', '))\
                .filter(lambda name: name != '')\
                .map(lambda name: name.split()[0])\
                .group_by(lambda firstname: firstname)\
                .flat_map(lambda grp: grp.count().map(
                    lambda ct: (grp.key, ct)
                ))\
                .filter(lambda name_and_ct: name_and_ct[1] > 1)

        db_file = 'myfile/people.txt'
        Observable.interval(5000)\
            .flat_map(lambda i: frequent_firstnames_from_db(db_file))\
            .subscribe(lambda value: print(str(value)))
        input("Stating... Press any key to quit\n")

    def example6():
        def frequent_firstnames_from_db(file_name):
            file = open(file_name)
            return Observable.from_(file)\
                .flat_map(lambda content: content.split(', '))\
                .filter(lambda name: name != '')\
                .map(lambda name: name.split()[0])\
                .group_by(lambda firstname: firstname)\
                .flat_map(lambda grp: grp.count().map(
                    lambda ct: (grp.key, ct)
                ))\
                .filter(lambda name_and_ct: name_and_ct[1] > 1)

        db_file = 'myfile/people.txt'
        # distinct only put when content changed
        Observable.interval(5000)\
            .flat_map(lambda i: frequent_firstnames_from_db(db_file))\
            .distinct()\
            .subscribe(lambda value: print(str(value)))
        input("Stating... Press any key to quit\n")

    def main_func():
        # example1()
        # example2()
        # example3()
        # peoplelist()
        # example4()
        # example5()
        example6()

    main_func()


import sys
import csv
from nameko.rpc import rpc, RpcProxy
from faker import Faker
faker = Faker()


class PeopleListService:
        name = 'peoplelist'

        @rpc
        def populate(self, number=20):
            names = []
            for _ in range(0, number):
                n = faker.name()
                names.append(n)
            return names


class PeopleListService2:
        name = 'peoplelist2'

        @rpc
        def populate(self, number=20):
            persons = []
            for _ in range(0, number):
                p = {'firstname': faker.first_name(),
                'lastname': faker.last_name(),
                'address': faker.address()}
                persons.append(p)
            return persons


class PeopleDataPersistenceService:
    name = 'people_data_persistence'
    peoplelist_rpc = RpcProxy('peoplelist2')

    @rpc
    def save(self, filename):
        persons = self.peoplelist_rpc.populate(number=25)
        with open(filename, 'a', newline='') as csv_file:
            filednames = ['firstname', 'lastname', 'address']
            writer = csv.DictWriter(csv_file, fieldnames=filednames,
            delimiter=';')
            for p in persons:
                writer.writerow(p)

        return f"Saved data for {len(persons)} new people"


def pattern_micro_or_cloud_service():
    """
    """
    from nameko.testing.services import worker_factory
    from nameko.standalone.rpc import ClusterRpcProxy

    """
    micro mode
    instance in real life:
    1. Eventuate
    2. eShopOnContainers
    3. AWS, GOOGLE Cloud

    usage:
    1. support diff client, contain desktop and mobile
    2. API that supply to the third partner
    3. must via message deliver to communicate other app
    4. deal request via access db, communicate other sys
    and return correct response(JSON,XML)
    5. has diff logic component of app
    """
    def test_people():
        service_woker = worker_factory(PeopleListService)
        result = service_woker.populate()
        for name in result:
            print(name)

    config = {'AMQP_URI': 'pyamqp://guest:guest@192.168.99.100:5672'}

    def test_peopledata_persist():
        with ClusterRpcProxy(config) as cluster_rpc:
            out = cluster_rpc.people_data_persistence.save.call_async('../myfile/people.csv')
            print(out.result())

    import time
    import os

    def create_file(filename, after_delay=5):
        time.sleep(after_delay)
        with open(filename, 'w') as f:
            f.write('A file creation test')

    def append_data_to_file(filename):
        if os.path.exists(filename):
            with open(filename, 'a') as f:
                f.write('... Updating the file')
        else:
            raise OSError

    FILENAME = '../myfile/file1.txt'

    """
    retry mode
    instance in real life:
    1. python: Retrying lib, Go: Pester lib, java: Spring Retry

    usage:
    1. alleviate affection because of server overload or net fault
    2. no recommend use for app inner logic error
    """
    def retry_func():
        args = sys.argv
        if args[1] == 'create':
            create_file(FILENAME)
            print(f"Created file: '{FILENAME}'")
        elif args[1] == 'update':
            while True:
                try:
                    append_data_to_file(FILENAME)
                    print("Success! We are done!")
                    break
                except OSError as e:
                    print("Error... Try again")

    from retrying import retry

    @retry
    def append_data_to_file2(filename):
        if os.path.exists(filename):
            print("got the file... let's process")
            with open(filename, 'a') as f:
                f.write('... Updating the file')
            return 'OK'
        else:
            print("Error: Missing file, so we can't proceed. Retrying...")
            raise OSError

    import tenacity

    @tenacity.retry(wait=tenacity.wait_fixed(2))
    def append_data_to_file3(filename):
        if os.path.exists(filename):
            print("got the file... let's process")
            with open(filename, 'a') as f:
                f.write('... Updating the file')
            return 'OK'
        else:
            print("Error: Missing file, so we can't proceed. Retrying...")
            raise OSError

    @tenacity.retry(wait=tenacity.wait_exponential())
    def append_data_to_file4(filename):
        if os.path.exists(filename):
            print("got the file... let's process")
            with open(filename, 'a') as f:
                f.write('... Updating the file')
            return 'OK'
        else:
            print("Error: Missing file, so we can't proceed. Retrying...")
            raise OSError

    def retry_func2():
        args = sys.argv
        if args[1] == 'create':
            create_file(FILENAME)
            print(f"Created file: '{FILENAME}'")
        elif args[1] == 'update':
            while True:
                out = append_data_to_file4(FILENAME)
                if out == 'OK':
                    print("Success! We are done!")
                    break

    import pybreaker
    import random
    import datetime

    """
    breaker mode

    instance in real life:
    1. Pybreaker: python lib
    2. Hystrix: Netflix tool
    3. Jrugged: java lib

    usage:
    1. when your component communicate with outer component
    can fault tolerance to respond long fault
    """
    
    breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5)
    @breaker
    def fragile_function():
        if not random.choice([True, False]):
            print(' /OK', end='')
        else:
            print(' /FAIL', end='')
            raise Exception('This is a sample Exception')

    # breaker
    def circuit_breaker():
        while True:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            try:
                fragile_function()
            except Exception as e:
                print('/ {} {}'.format(type(e), e), end='')
            finally:
                print('')
                time.sleep(1)

    import sqlite3
    from random import randint

    def setup_db():
        try:
            print('Creating db')
            db = sqlite3.connect('../myfile/quotes.sqlite3')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE quotes(id INTEGER PRIMARY KEY, text TEXT)
            """)
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()

    def add_quotes(quotes_list):
        quotes = []
        try:
            db = sqlite3.connect('../myfile/quotes.sqlite3')
            cursor = db.cursor()
            quotes = []
            for quote_text in quotes_list:
                quote_id = randint(1, 100)
                quote = (quote_id, quote_text)
                try:
                    cursor.execute("""INSERT INTO quotes(id, text) VALUES(
                        ?, ?)""", quote)
                    quotes.append(quote)
                except Exception as e:
                    print(f"Error with quote id {quote_id}: {e}")
            db.commit()
        except Exception as e:
            print(e)
        finally:
            db.close()

        return quotes

    """
    cache aside mode

    instance in real life:
    1. Memcached
    2. Redis
    3. ElastiCache

    usage:
    1. storage data that seldom modify
    2. no dispend consistency data of a group
    """

    # cache aside
    def cache_aside():
        args = sys.argv

        if args[1] == 'init':
            setup_db()
        elif args[1] == 'update_db_and_cache':
            quote_list = [faker.sentence() for _ in 
            range(1, 11)]
            quotes = add_quotes(quote_list)
            print("New (fake) quotes added to the database:")
            for q in quotes:
                print(f"Added to DB: {q}")
            
            with open('../myfile/quotes_cache.csv', 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=['id', 'text'],
                delimiter=';')
                for q in quotes:
                    print(f"Adding '{q[1]}' to cache")
                    writer.writerow({'id': str(q[0]), 'text': q[1]})
        elif args[1] == 'update_db_only':
            quote_list = [faker.sentence() for _ in range(1, 11)]
            quotes = add_quotes(quote_list)
            print("New (fake) quotes added to the database ONLY:")
            for q in quotes:
                print(f"Added to DB: {q}")

    cache_key_prefix = "quote"

    class QuoteCache:
        def __init__(self, filename=""):
            self.filename = filename

        def get(self, key):
            with open(self.filename) as csv_file:
                items = csv.reader(csv_file, delimiter=';')
                for item in items:
                    if item[0] == key.split('.')[1]:
                        return item[1]

        def set(self, key, quote):
            existing = []
            with open(self.filename) as csv_file:
                items = csv.reader(csv_file, delimiter=';')
                existing = [cache_key_prefix + '.' + item[0] for item in items]
                if key in existing:
                    print("This is weird. The key already exisits")
                else:
                    with open(self.filename, 'a', newline='') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=['id', 'text'],
                        delimiter=';')
                        writer.writerow({'id': key.split('.')[1], 'text': quote})

    cache = QuoteCache('../myfile/quotes_cache.csv')

    def get_quote(quote_id):
        quote = cache.get(f"quote.{quote_id}")
        out = ""

        if quote is None:
            try:
                db = sqlite3.connect('../myfile/quotes.sqlite3')
                cursor = db.cursor()
                cursor.execute(f"SELECT text FROM quotes WHERE id = {quote_id}")
                for row in cursor:
                    quote = row[0]
                print(f"Got '{quote}' FROM DB")
            except Exception as e:
                print(e)
            finally:
                db.close()
            
            key = f"{cache_key_prefix}.{quote_id}"
            cache.set(key, quote)
        
        if quote:
            out = f"{quote} (FROM CACHE, with key quote.{quote_id})"
        
        return out

    def get_quote_interactive():
        args = sys.argv

        if args[1] == 'fetch':
            while True:
                quote_id = input("Enter the ID of the quote:")
                q = get_quote(quote_id)
                if q:
                    print(q)

    from flask import Flask
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from flask import Flask

    app = Flask(__name__)

    """
    throtting mode
     
    instance in real life:
    1. Django-Rest-Framework
    2. Django-throttle-requests
    3. flask-limiter
    4. AWS API gateway

    usage:
    1. optimal usage cost of service
    2. deal outbreak event
    3. make sure continue deliver service
    """

    # throttling
    def web_limiter():
        limiter = Limiter(app,
        key_func = get_remote_address,
        default_limits=['100 per day', '10 per hour'])

        @app.route('/limited')
        def limited_api():
            return 'Welcome to our API'

        @app.route('/more_limited')
        @limiter.limit('2/minute')
        def more_limited_api():
            return 'Welcome to our expensive, thus very \
            limited, API!'

        app.run(debug=True)

    def main_func():
        # test_people()
        # test_peopledata_persist()
        # retry_func2()
        web_limiter()

    main_func()


def main():
    pattern_micro_or_cloud_service()


if __name__ == '__main__':
    main()
    # pass
