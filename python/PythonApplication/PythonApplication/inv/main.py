from invest import common, util


def _init_config():
    util.init_config('database')


def _init_db_config():
    util.init_config('strategy', from_db=True)
    util.init_config('market', from_db=True)
    util.init_config('mail', from_db=True)


def _init_db():
    util.create_mysql('test')


def _init_logger():
    util.init_logger()


def _init_common_data():
    common.init_data()


def _init():
    _init_config()
    _init_db()
    _init_db_config()
    _init_logger()
    _init_common_data()


def run():
    _init()

    from invest import strategy_my

    ms = strategy_my.MyStrategy()
    is_str_completed = False

    while not is_str_completed:
        is_str_completed = ms.run()


if __name__ == '__main__':
    run()
