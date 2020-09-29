from PIL import Image
import argparse
import re
import time
import base64
import pytesseract
import requests
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlencode
from io import BytesIO

from invest.types import CaptchaWay

_img_path = r'{}_captcha.png'


def save_img(name):
    path = _img_path.format(name)

    def wrapper(func):
        def inner_func(*args, **kwargs):
            img = func(*args, **kwargs)
            img.save(path)
            return img
        return inner_func

    return wrapper


@save_img('gray')
def to_gray(img):
    gray_img = img.convert('L')
    return gray_img


@save_img('binary')
def to_binary(gray_img, threshold=109):
    black_white_img = gray_img.point([0 if i < threshold
                                      else 1 for i in range(256)], '1')
    return black_white_img


def _sum_9_scope_new(img, x, y):
    cur_pixel = img.getpixel((x, y))
    width = img.width
    height = img.height
    # the white point
    if cur_pixel == 1:
        return 0
    # remove the black point of surrounding
    if y < 3:
        return 1
    # the two rows of bottom
    elif y > height - 3:
        return 1
    # y not in the border
    else:
        # two col of front
        if x < 3:
            return 1
        # not top point of right
        elif x == width - 1:
            return 1
        # meet the condition of 9 region
        else:
            sum_pixel = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum_pixel


def _collect_noise_point(black_white_img):
    noise_points = []
    for x in range(black_white_img.width):
        for y in range(black_white_img.height):
            scope_9 = _sum_9_scope_new(black_white_img, x, y)
            # the isolated point
            if black_white_img.getpixel((x, y)) == 0 and 0 < scope_9 < 3:
                noise_points.append((x, y))
    return noise_points


@save_img('clear_noise')
def remove_noise(black_white_img):
    noises = _collect_noise_point(black_white_img)

    for pos in noises:
        black_white_img.putpixel((pos[0], pos[1]), 1)

    return black_white_img


class CaptCha9KAPI:
    def __init__(self, img_data, api_key='', timeout=60):
        self.img_data = img_data
        self.api_key = api_key
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'

    # get the result of solved captcha
    def solve(self):
        # data encode to base64
        byte_buffer = BytesIO()
        self.img_data.save(byte_buffer, format='PNG')
        data = byte_buffer.getvalue()
        base64_ata = base64.b64encode(data)

        captcha_id = self.send(base64_ata)
        start_time = time.time()

        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id)
            except Exception:
                pass
            else:
                if text == 'NO DATA':
                    continue
                if text == 'ERROR NO USER':
                    raise Exception('Error: no user available to solve CAPTCHA')
                else:
                    print('CAPTCHA solved!')
                return text
            print('Waiting for Captcha...')

        print('Error: API timeout!')
        return ""

    def send(self, img_data):
        print("Submitting Captcha...")

        data = {
            "apikey": self.api_key,
            "action": "usercaptchaupload",
            "file-upload-01": img_data,
            "base64": "1",
            "maxtimeout": str(self.timeout),
            # 1 self solve; 0 other solve, but spend credits
            "selfsolve": "0"
        }
        encoded_data = urlencode(data).encode()
        request = urllib.request.Request(self.url, data=encoded_data)
        resp = urlopen(request)
        captcha_id = resp.read().decode()
        self.check(captcha_id)

        return captcha_id

    def get(self, captcha_id):
        data = {
            "apikey": self.api_key,
            "action": "usercaptchacorrectdata",
            "id": captcha_id,
            # return 'NO DATA' if no result
            "info": 1
        }
        encoded_data = urlencode(data)
        resp = urlopen(self.url + '?' + encoded_data)
        captcha = resp.read().decode()
        self.check(captcha)

        return captcha

    @staticmethod
    def check(result):
        # apikey error
        if re.match(r'00\d\d \w+', result):
            raise Exception('API error:', result)


class ChaoJiYingAPI:
    def __init__(self, img, username, pwd, soft_id, code_type=1006):
        self.img = img
        self.username = username
        self.pwd = pwd
        self.soft_id = soft_id
        self.code_type = code_type
        self.base_params = {
            'user': self.username,
            'pass2': self.pwd,
            'softid': self.soft_id,
        }
        self.header = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.upload_url = 'http://upload.chaojiying.net/Upload/Processing.php'
        self.uperror_url = 'http://upload.chaojiying.net/Upload/ReportError.php'

    # upload picture
    def solve(self):
        byte_buffer = BytesIO()
        self.img.save(byte_buffer, format='PNG')
        img_bytes = byte_buffer.getvalue()

        params = {'codetype': self.code_type}
        params.update(self.base_params)
        files = {'userfile': ('hello.jpg', img_bytes)}

        resp = requests.post(self.upload_url, data=params, files=files, headers=self.header)

        # result example {"err_no":0,"err_str":"OK","pic_id":"1662228516102","pic_str":"1,2|3,4",
        # "md5":"35d5c7f6f53223fbdc5b72783db0c2c0"}
        all_msg = resp.json()

        return all_msg['pic_str']

    # get error info of upload
    def report_error(self, img_id):
        params = {'id': img_id}
        params.update(self.base_params)
        error_info = requests.post(self.uperror_url, data=params, headers=self.header)
        # result example {"err_no":0,"err_str":"OK"}
        return error_info.json()


def parse_captcha(ori_img, way='local', api_key='',
                  username='', pwd='', soft_id=0,
                  code_type=0, secret_key='', bin_thres=0):
    if way == CaptchaWay.Local:
        gray_img = to_gray(ori_img)
        bin_img = to_binary(gray_img, bin_thres)
        rem_noise_img = remove_noise(bin_img)

        words = pytesseract.image_to_string(image=rem_noise_img, lang='eng', config='--psm 7')
    elif way == CaptchaWay.BaiduApi:
        from aip import AipOcr
        client = AipOcr(soft_id, api_key, secret_key)

        img_bytes = BytesIO()
        ori_img.save(img_bytes, format='PNG')
        msg = client.basicGeneral(img_bytes.getvalue())

        words = msg.get('words_result')
        try:
            words = words[0]['words']
        except IndexError:
            words = ''
    elif way == CaptchaWay.NineKwApi:
        cc9k = CaptCha9KAPI(ori_img, api_key=api_key)
        words = cc9k.solve()
    elif way == CaptchaWay.ChaoJiYingApi:
        cjy = ChaoJiYingAPI(ori_img, username, pwd, soft_id, code_type)
        words = cjy.solve()
    else:
        print(f"not support way: {way}")
        words = ""

    return words


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--path', default='', type=str, required=False, help='the path of original img')
    arg_parser.add_argument('--way', default='local', type=str, required=False, help='the way to parse')
    arg_parser.add_argument('--api_key', default='', type=str, required=False, help='api_key')
    arg_parser.add_argument('--username', default='', type=str, required=False, help='username')
    arg_parser.add_argument('--pwd', default='', type=str, required=False, help='password')
    arg_parser.add_argument('--soft_id', default='', type=str, required=False, help='soft_id')
    arg_parser.add_argument('--code_type', default=0, type=int, required=False, help='code_type')
    arg_parser.add_argument('--secret_key', default=0, type=str, required=False, help='secret_key')
    arg_parser.add_argument('--bin_thres', default=0, type=int, required=False, help='bin_thres, only for way: local')

    args = arg_parser.parse_args()

    if args.path:
        img = Image.open(args.path)
        words = parse_captcha(img, args.way, args.api_key,
                              args.username, args.pwd, args.soft_id,
                              args.code_type, args.secret_key, args.bin_thres)
        print(words)


if __name__ == '__main__':
    main()
