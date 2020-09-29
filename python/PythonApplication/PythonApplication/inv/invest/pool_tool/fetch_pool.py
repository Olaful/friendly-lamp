import time
import lxml
import re
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
import hashlib

from invest import util
from invest.pool_tool.captcha_ident import parse_captcha
from invest.types import CaptchaWay

browser = None
MAX_TRY_LOGIN = 3
logger = None


def _init_config():
    util.init_config('database')


def _init_db():
    util.create_mysql('test')


def _init_db_config():
    util.init_config('chrome', from_db=True)
    
    
def _init_logger():
    util.init_logger()
    global logger
    logger = util.get_logger()


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

    time.sleep(1.5)

    screenshot = browser.get_screenshot_as_png()
    screen_img = Image.open(BytesIO(screenshot))
    captcha_pos = _get_captcha_pos(e_captcha)
    captcha_sc = screen_img.crop(captcha_pos)

    return captcha_sc


def _parse_captcha():
    captcha_img = _screenshot_captcha()

    if util.get_config('chrome', 'save_capt'):
        captcha_img.save(util.get_config('chrome', 'capt_path'))

    api_key = ''
    username = ''
    pwd = ''
    soft_id = 0
    code_type = 0
    secret_key = ''
    bin_thres = 0

    way = util.get_config('chrome', 'capt_way')
    if way == CaptchaWay.Local:
        bin_thres = util.get_config('chrome', 'local_capt_bin_thres')
    elif way == CaptchaWay.BaiduApi:
        api_key = util.get_config('chrome', 'baidu_capt_api_key')
        soft_id = util.get_config('chrome', 'baidu_capt_soft_id')
        secret_key = util.get_config('chrome', 'baidu_capt_api_secret_key')
    elif way == CaptchaWay.NineKwApi:
        api_key = util.get_config('chrome', '9kw_capt_api_key')
    elif way == CaptchaWay.ChaoJiYingApi:
        username = util.get_config('chrome', 'chaojiying_uname')
        ori_pwd = ''.join([chr(int(w) - 12) for w in util.get_config('chrome', 'chaojiying_upwd').split(',')])
        pwd_md5 = hashlib.md5()
        pwd_md5.update(ori_pwd.encode())
        pwd = pwd_md5.hexdigest()
        soft_id = util.get_config('chrome', 'chaojiying_soft_id')
        code_type = util.get_config('chrome', 'chaojiying_code_type')
    else:
        raise ValueError(f"not support way: {way}")

    words = parse_captcha(captcha_img, way=way,
                          api_key=api_key, username=username,
                          pwd=pwd, soft_id=soft_id,
                          code_type=code_type, secret_key=secret_key,
                          bin_thres=bin_thres)
    return words


def _auto_login(try_num=0):
    is_record_login_info = re.search('touxiangAvatar', browser.page_source)

    if is_record_login_info:
        e_login_img = browser.find_element(by=By.CLASS_NAME, value='touxiangAvatar')
        e_login_img.click()
        time.sleep(2)
        return True

    try:
        e_switch_account_login = _find_elements_by_css('a#to_account_login')[0]
        e_switch_account_login.click()
    except Exception:
        pass

    e_uname_input = _find_elements_by_css('input#uname')[0]
    e_uname_input.send_keys(util.get_config('chrome', 'ths_uname'))

    e_pwd_input = _find_elements_by_css('input#passwd')[0]
    pwd = ''.join([chr(int(w) - 12) for w in util.get_config('chrome', 'ths_pwd').split(',')])
    e_pwd_input.send_keys(pwd)

    captcha = _parse_captcha()
    captcha = captcha.replace(' ', '')
    e_captcha_input = _find_elements_by_css('input#account_captcha')[0]
    e_captcha_input.send_keys(captcha)

    time.sleep(2)

    e_login = _find_elements_by_css('div[class="b_f pointer tc submit_btn enable_submit_btn"]')[0]
    e_login.click()
    time.sleep(2)

    logger.info(f'login...captcha: {captcha}')

    login_error_info = re.search('fl error_c msg_box', browser.page_source)

    if login_error_info:
        e_error_box = _find_elements_by_css('div[class="fl error_c msg_box"]')[0]
        error_msg = e_error_box.text
        logger.info(error_msg)
        logger.info("login retry...")
        if try_num < MAX_TRY_LOGIN:
            time.sleep(2)

            e_uname_input.clear()
            e_pwd_input.clear()
            e_captcha_input.clear()

            return _auto_login(try_num + 1)
        return False

    return True


def _get_current_html(try_num=0):
    e_page = _find_elements_by_css('ul.pcwencai-pagination > li')

    e_next = e_page[-1]
    e_next = e_next.find_element_by_css_selector('a')

    max_try = 3
    if not e_next.is_enabled() and try_num < max_try:
        time.sleep(2)
        return _get_current_html(try_num + 1)

    return browser.page_source


def _get_query_url(query_param):
    url = f"http://www.iwencai.com/unifiedwap/result?{query_param}&querytype=&issugs"
    return url


def _get_page_num():
    e_page = _find_elements_by_css('ul.pcwencai-pagination > li.page-item')
    browser.implicitly_wait(30)

    e_last_page_num = e_page[-1]

    page_num = e_last_page_num.text

    return int(page_num) if page_num else 1


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
        return _next_page(try_num + 1)

    time.sleep(1)
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
        logger.info("login failed")
        return

    for pool, query_word in util.get_config('chrome', 'pool_where').items():
        logger.info(f"fetch pool: {pool}")

        query_param = urlencode({'w': query_word})
        url = _get_query_url(query_param)

        time.sleep(2)
        browser.get(url)

        pool_codes = []

        current_html = _get_current_html()
        page_codes = _get_code(current_html)
        pool_codes.extend(page_codes)

        page_num = _get_page_num()

        for _ in range(page_num - 1):
            if len(pool_codes) >= util.get_config('chrome', 'pool_num'):
                break

            _next_page()
            time.sleep(3)

            current_html = _get_current_html()
            page_codes = _get_code(current_html)
            pool_codes.extend(page_codes)

        _to_db(pool, pool_codes[:util.get_config('chrome', 'pool_num')])


def fetch_pool():
    _init_config()
    _init_db()
    _init_db_config()
    _init_logger()
    _init_browser()

    try:
        run()
        _close_browser()
    except Exception as e:
        logger.info(f"run error: {str(e)}")
        _close_browser()
        

if __name__ == '__main__':
    fetch_pool()
