import time
import lxml
import pytesseract
import re
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlencode

from invest import util

browser = None
MAX_TRY_LOGIN = 5


def _init_config():
    util.init_config('database')


def _init_db():
    util.create_mysql('test')


def _init_db_config():
    util.init_config('chrome', from_db=True)


def _init_browser():
    global browser
    
    chrome_options = webdriver.ChromeOptions()
    for opt in util.get_config('chrome', 'options'):
        chrome_options.add_argument(opt)

    browser = webdriver.Chrome(executable_path=util.get_config('chrome', 'executable_path'),
                               chrome_options=chrome_options)


def _close_browser():
    browser.close()


def _find_elements_by_css(css):
    elements = browser.find_elements_by_css_selector(css)
    browser.implicitly_wait(30)
    return elements


def _pop_up_login_page():
    e_account = browser.find_element_by_css_selector('i[class="base-icon login-btn pointer"]')
    browser.implicitly_wait(30)

    time.sleep(1)
    e_account.click()

    e_login = browser.find_element_by_css_selector('ul.login-popup > li > a > span')
    browser.implicitly_wait(30)

    time.sleep(1)
    e_login.click()

    browser.switch_to.frame('login_iframe')


def _get_captcha_pos(e_captcha):
    captcha_location = e_captcha.location_once_scrolled_into_view
    captcha_size = e_captcha.size

    top, left = captcha_location['y'], captcha_location['x']
    right = left + captcha_size['width']
    bottom = top + captcha_size['height']

    return left, top, right, bottom


def _screenshot_captcha():
    e_captcha = _find_elements_by_css('img[class="pointer captcha_img"]')[0]
    e_captcha.click()

    screenshot = browser.get_screenshot_as_png()
    screen_img = Image.open(BytesIO(screenshot))
    screen_img.save('E:\picture\sreen.png')
    captcha_pos = _get_captcha_pos(e_captcha)
    captcha_sc = screen_img.crop(captcha_pos)

    return captcha_sc


def _captcha_rem_noise(img):
    def sum_9_scope_new(img, x, y):
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

    def collect_noise_point(img):
        noise_points = []
        for x in range(img.width):
            for y in range(img.height):
                scope_9 = sum_9_scope_new(img, x, y)
                # the isolated point
                if img.getpixel((x, y)) == 0 and 0 < scope_9 < 3:
                    noise_points.append((x, y))
        return noise_points

    def remove_noise(img, noise_poss):
        for pos in noise_poss:
            img.putpixel((pos[0], pos[1]), 1)

    gray_img = img.convert('L')
    threshold = 109
    black_white_img = gray_img.point([0 if i < threshold else 1 for i in range(256)], '1')

    noise_point_list = collect_noise_point(black_white_img)

    remove_noise(black_white_img, noise_point_list)

    return black_white_img


def _parse_captcha(try_num=0):
    captcha_img = _screenshot_captcha()
    rem_noise_img = _captcha_rem_noise(captcha_img)
    rem_noise_img.save('E:\picture\iwencai_captcha.png')
    words = pytesseract.image_to_string(image=rem_noise_img, lang='eng', config='--psm 7')
    if words:
        return words
    max_try = 5
    if try_num < max_try:
        _parse_captcha(try_num + 1)

    return ''


def _auto_login(try_num=0):
    is_record_login_info = re.search('touxiangAvatar', browser.page_source)
    if is_record_login_info:
        e_login_img = browser.find_element(by=By.CLASS_NAME, value='touxiangAvatar')
        e_login_img.click()
        time.sleep(2)
        return True

    e_switch_account_login = _find_elements_by_css('a#to_account_login')[0]
    e_switch_account_login.click()

    e_uname_input = _find_elements_by_css('input#uname')[0]
    e_uname_input.send_keys(util.get_config('chrome', 'ths_uname'))

    e_pwd_input = _find_elements_by_css('input#passwd')[0]
    pwd = ''.join([chr(int(w) - 12) for w in util.get_config('chrome', 'ths_pwd').split(',')])
    e_pwd_input.send_keys(pwd)

    captcha = _parse_captcha()
    e_captcha_input = _find_elements_by_css('input#account_captcha')[0]
    e_captcha_input.send_keys(captcha)

    time.sleep(2)

    e_login = _find_elements_by_css('div[class="b_f pointer tc submit_btn enable_submit_btn"]')[0]
    e_login.click()
    time.sleep(1)

    print(f'login...captcha: {captcha}')

    e_error_box = _find_elements_by_css('div[class="fl error_c msg_box"]')[0]
    error_msg = e_error_box.text
    print(error_msg)

    if error_msg:
        print("login retry...")
        if try_num < MAX_TRY_LOGIN:
            time.sleep(2)

            e_uname_input.send_keys("")
            e_pwd_input.send_keys("")
            e_captcha_input.send_keys("")

            _auto_login(try_num + 1)
        return False

    return True


def _get_current_html(try_num=0):
    e_page = _find_elements_by_css('ul.pcwencai-pagination > li')

    e_next = e_page[-1]
    e_next = e_next.find_element_by_css_selector('a')

    max_try = 3
    if not e_next.is_enabled() and try_num < max_try:
        time.sleep(2)
        _get_current_html(try_num + 1)

    return browser.page_source


def _get_query_url(query_param):
    url = f"http://www.iwencai.com/unifiedwap/result?{query_param}&querytype=&issugs"
    return url


def _get_page_num():
    e_page = _find_elements_by_css('ul.pcwencai-pagination > li.page-item')
    browser.implicitly_wait(30)

    e_last_page_num = e_page[-1]

    return int(e_last_page_num.text)


def _get_code(current_html):
    tree = lxml.html.fromstring(current_html)

    e_codes = tree.cssselect('div[class="iwc-table-body-inner scroll-style2"]'
                             ' > table > tbody > tr > td[style="width: 76px;"]')
    
    codes = []
    for e in e_codes:
        code = str(e.text_content())
        codes.append(code)

    codes = [code for code in codes if code.startswith('00') or code.startswith('60')]

    return codes


def _next_page(try_num=0):
    e_page = _find_elements_by_css('ul.pcwencai-pagination > li')

    e_next = e_page[-1]
    e_next = e_next.find_element_by_css_selector('a')

    max_try = 3
    if not e_next.is_enabled() and try_num < max_try:
        time.sleep(2)
        _next_page(try_num + 1)

    e_next.click()


def _to_db(pool, codes: list = None):
    db = util.get_mysql('test')
    insert_sql = "REPLACE INTO `code_pool`" \
                 "(`code`, `name`, `pool`) VALUES" \
                 "( %s, NULL, %s )"
    insert_param = [(code, pool) for code in codes]

    db.executemany(insert_sql, insert_param)


def run():
    home_page = 'http://www.iwencai.com/unifiedwap/home/index'
    browser.get(home_page)

    _pop_up_login_page()

    if not _auto_login():
        return

    for pool, query_word in util.get_config('chrome', 'pool_where').items():
        query_param = urlencode({'w': query_word})
        url = _get_query_url(query_param)
        browser.get(url)

        pool_codes = []

        current_html = _get_current_html()
        page_codes = _get_code(current_html)
        pool_codes.extend(page_codes)

        page_num = _get_page_num()

        for _ in range(page_num - 1):
            if len(pool_codes) >= util.get_config('chrome', 'pool_num'):
                break

            time.sleep(3)
            _next_page()

            current_html = _get_current_html()
            page_codes = _get_code(current_html)
            pool_codes.extend(page_codes)

        _to_db(pool, pool_codes[:util.get_config('chrome', 'pool_num')])


def fetch_pool():
    _init_config()
    _init_db()
    _init_db_config()
    _init_browser()

    try:
        run()
        _close_browser()
    except Exception as e:
        print(f"run error: {str(e)}")
        _close_browser()
        

if __name__ == '__main__':
    fetch_pool()
