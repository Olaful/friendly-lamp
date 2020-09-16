import time
import os
import importlib
from invest import common, util


def _init_config():
    util.init_config('database')


def _init_db_config():
    util.init_config('global', from_db=True)
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


def _load_strategies():
    from invest.strategy_base import StrategyBase

    strategy_switch = util.get_config('global', 'str_status')
    enable_str = [s for s, status in strategy_switch.items() if status == 1]

    all_files = os.listdir(os.path.join(util.root_path(), 'invest'))
    str_files = [f for f in all_files if f.endswith('.py') and f.startswith('strategy')]

    str_seen = set()
    str_list = []

    for f in str_files:
        if len(str_seen) >= len(enable_str):
            break

        f_name = f.split('.')[0]
        lib = importlib.import_module(f".{f_name}", 'invest')
        attrs = dir(lib)

        for attr_name in attrs:
            attr = getattr(lib, attr_name)

            if not isinstance(attr, type):
                continue
            if not issubclass(attr, StrategyBase):
                continue
            if attr is StrategyBase:
                continue

            if attr.name() in enable_str and attr.name() not in str_seen:
                str_list.append(attr())
                str_seen.add(attr.name())

    return str_list, str_seen


def run():
    _init()

    all_str, str_names = _load_strategies()

    logger = util.get_logger()
    logger.info(f"Begin to run: {str_names}")

    if not all_str:
        return

    while True:
        time.sleep(0.1)
        for strategy in all_str:
            strategy.run()


if __name__ == '__main__':
    run()
