import time
import lxml
from selenium import webdriver
from urllib.parse import urlencode

from invest import util

browser = None


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

    e_switch_account_login = browser.find_element_by_css_selector('a#to_account_login')
    browser.implicitly_wait(30)
    e_switch_account_login.click()


def _auto_login():
    _pop_up_login_page()

    e_uname_input = _find_elements_by_css('input#uname')[0]
    e_uname_input.send_keys(util.get_config('chrome', 'ths_uname'))

    e_pwd_input = _find_elements_by_css('input#passwd')[0]
    pwd = [chr(int(w) - 12) for w in util.get_config('chrome', 'ths_pwd')]
    e_pwd_input.send_keys(pwd)


def _get_current_html(try_num=0):
    e_page = browser.find_elements_by_css_selector('ul.pcwencai-pagination > li')
    browser.implicitly_wait(30)

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
    e_page = browser.find_elements_by_css_selector('ul.pcwencai-pagination > li.page-item')
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
    e_page = browser.find_elements_by_css_selector('ul.pcwencai-pagination > li')
    browser.implicitly_wait(30)

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
                 "( '{code}', NULL, '{pool}')"
    insert_param = [{'code': code, 'pool': pool} for code in codes]

    db.executemany(insert_sql, insert_param)


def run():
    for pool, query_word in util.get_config('chrome', 'pool_where').items():
        query_param = urlencode({'w': query_word})
        url = _get_query_url(query_param)
        browser.get(url)

        _auto_login()

        pool_codes = []

        current_html = _get_current_html()
        page_codes = _get_code(current_html)
        pool_codes.extend(page_codes)

        page_num = _get_page_num()

        for _ in range(page_num - 1):
            if len(pool_codes) >= util.get_config('chrome', 'pool_num'):
                break

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
