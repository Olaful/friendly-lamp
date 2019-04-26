from aip import AipOcr
import re

def imgOcr():
    APP_ID = '15920597'
    API_KEY = 'DDjpHGGAnMk6BBdxSZRekdPq'
    SECRET_KEY = 'Su56XKHynhNrYByAhOSfESjzuf9kqtyz'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    f = open(r'F:\picture\11.png', 'rb')
    img = f.read()

    msg = client.basicGeneral(img)

    wordDict = msg.get('words_result')
    print(wordDict)


if __name__ == '__main__':
    imgOcr()