import argparse
import re
from aip import AipOcr


def imgOcr(path):
    APP_ID = '15920597'
    API_KEY = 'DDjpHGGAnMk6BBdxSZRekdPq'
    SECRET_KEY = 'Su56XKHynhNrYByAhOSfESjzuf9kqtyz'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    f = open(path, 'rb')
    img = f.read()

    msg = client.basicGeneral(img)

    wordDict = msg.get('words_result')
    print(wordDict)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--path',
                            default='',
                            type=str,
                            required=False,
                            help='the path of original img')
    args = arg_parser.parse_args()

    if args.path:
        imgOcr(args.path)


if __name__ == '__main__':
    main()
