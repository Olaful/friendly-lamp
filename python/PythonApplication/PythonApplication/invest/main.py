import util
import strategy

def _init_config():
    util.init_config('database')
    util.init_config('strategy')


def _init_db():
    util.create_mysql('pool_db')


def _init_logger():
    util.init_logger()


def _init():
    _init_config()
    _init_db()
    _init_logger()


def run():
    _init()

    ms = strategy.MyStrategy()
    ms.run()


if __name__ == '__main__':
    run()