import util
import strategy
import common


def _init_config():
    util.init_config('database')
    util.init_config('strategy', from_db=True)


def _init_db():
    util.create_mysql('test')


def _init_logger():
    util.init_logger()


def _load_pos():
    common.init_data()


def _init():
    _init_db()
    _init_config()
    _init_logger()
    _load_pos()


def run():
    _init()

    ms = strategy.MyStrategy()
    ms.run()


if __name__ == '__main__':
    run()
