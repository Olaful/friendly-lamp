import os
import sys
import json


_CONFIG = {}


def absolute_path(*args):
    caller_full_path = sys._getframe(1).f_code.co_filename
    caller_dir = os.path.dirname(os.path.abspath(caller_full_path))

    full_path = caller_dir
    for arg in args:
        full_path = os.path.join(full_path, arg)

    return full_path


def init_config():
    global _CONFIG
    with open(r'setting.json', 'r', encoding='utf8') as f:
        _CONFIG = json.load(f)


def get_config(*args):
    tmp_config = _CONFIG[args[0]]

    for i in range(1, len(args)):
        if isinstance(tmp_config, dict):
            tmp_config = tmp_config.get(args[i], None)
    return tmp_config


init_config()


if __name__ == '__main__':
    rls = absolute_path('1', '2.txt')
    test = 1


