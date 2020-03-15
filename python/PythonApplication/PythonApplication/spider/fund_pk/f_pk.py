import requests
import os
import json
import lxml.html
import re
import pypinyin
import pprint
from selenium import webdriver


BASIC_PAGE = ''
OVERVIEW_PAGE = ''
CONFIG = {}
INDICATOR = {}
RANGE = []


def load_config():
    global CONFIG
    filepath = os.path.dirname(__file__)
    filename = os.path.join(filepath, 'setting.json')
    with open(filename, 'r', encoding='utf8') as f:
        CONFIG = json.load(f)

def return_1y(tree):
    path = '//dl[@class="dataItem01"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[1].text_content()
    try:
        rtn = float(rtn[:-1]) / 100
    except Exception:
        rtn = 0
        print(f"{INDICATOR['fund']} return_1y is None")
    INDICATOR['rtn_1y'] = round(rtn, 5)

def return_6m(tree):
    path = '//dl[@class="dataItem03"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[0].text_content()
    try:
        rtn = float(rtn[:-1]) / 100
    except Exception:
        rtn = 0
        print(f"{INDICATOR['fund']} return_6m is None")
    INDICATOR['rtn_6m'] = rtn

def return_3m(tree):
    path = '//dl[@class="dataItem02"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[1].text_content()
    try:
        rtn = float(rtn[:-1]) / 100
    except Exception:
        rtn = 0
        print(f"{INDICATOR['fund']} return_3m is None")
    INDICATOR['rtn_3m'] = rtn

def return_1m(tree):
    path = '//dl[@class="dataItem01"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[0].text_content()
    try:
        rtn = float(rtn[:-1]) / 100
    except Exception:
        rtn = 0
        print(f"{INDICATOR['fund']} return_1m is None")
    INDICATOR['rtn_1m'] = rtn

def basic_info():
    tree = lxml.html.fromstring(BASIC_PAGE)
    return_1y(tree)
    return_6m(tree)
    return_3m(tree)
    return_1m(tree)

def std_dt(tree):
    path = '//table[@class="fxtb"]/tr/td'
    risk_e = tree.xpath(path)
    risk_ind = risk_e[1].text_content()
    try:
        risk_ind = float(risk_ind[:-1]) / 100
    except Exception:
        risk_ind = 0
        print(f"{INDICATOR['fund']} std_dt is None")
    INDICATOR['std_dt'] = round(risk_ind, 5)

def sharp_ratio(tree):
    path = '//table[@class="fxtb"]/tr/td'
    risk_e = tree.xpath(path)
    risk_ind = risk_e[5].text_content()
    try:
        risk_ind = float(risk_ind)
    except Exception:
        risk_ind = 0
        print(f"{INDICATOR['fund']} sharp_ratio is None")
    INDICATOR['sharp_ratio'] = risk_ind

def perform(page):
    score = re.search(r'var Scores = \[(.*?)\]', page)[1]
    score_list = score.split(',')
    score_list = list(map(float, score_list))

    scorename = re.search(r'var ScoresName = \[(.*?)\]', page)[1]
    scorename_list = scorename.split(',')
    scorename_list = [sl.replace("'", '').replace(' ', '') for sl in scorename_list]
    scorename_list = [pypinyin.pinyin(sn) for sn in scorename_list]
    scorename_list = [''.join(map(lambda x: x[0][0], sl)) for sl in scorename_list]

    score_map = dict(zip(scorename_list, score_list))

    scoreavg = re.search('var avg = "(.*?)"', page)[1]
    if scoreavg:
        scoreavg = float(scoreavg)
    else:
        scoreavg = 0
        print(f"{INDICATOR['fund']} pf is None")

    score_map['avg'] = scoreavg

    INDICATOR['perform'] = score_map

def overview_info():
    tree = lxml.html.fromstring(OVERVIEW_PAGE)
    std_dt(tree)
    sharp_ratio(tree)
    perform(OVERVIEW_PAGE)

def cal_score():
    rtn_w = CONFIG['weight']['return']
    rtn_score = sum([INDICATOR[rn] * w for rn, w in rtn_w.items()
     if INDICATOR.get(rn)]) * rtn_w['total']
    pf_score = INDICATOR['perform']['avg'] / 100 * CONFIG['weight']['perform']
    std_dt_score = -INDICATOR['std_dt'] * CONFIG['weight']['std_dt']
    sharp_ratio_score = INDICATOR['sharp_ratio'] * CONFIG['weight']['sharp_ratio']

    INDICATOR['score'] = round(sum([rtn_score, pf_score, std_dt_score, sharp_ratio_score]), 5)

def get_fcode_with_theme():
    f_theme_url = 'http://fund.eastmoney.com/api/FundTopicInterface.ashx? \
    callbackname=topicFundData&sort=SYL_6Y&sorttype=DESC&ft=&pageindex=1 \
    &pagesize={0}&dt=10&tp={1}&isbuy=1'
    req_headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            + 'Chrome/71.0.3578.98 Safari/537.36'
        }
    
    f_code = []
    for theme, data in CONFIG['f_theme'].items():
        if not data['enabled']:
            continue
        print(f"{theme}")

        resp = requests.get(f_theme_url.format(data['num'], data['tp']), headers=req_headers)
        rls = re.search(r'"Datas":(.*?),"PageSize"', resp.text)
        json_rls = json.loads(rls[1])
        f_code_list = [r['FCODE'] for r in json_rls]
        f_code.extend(f_code_list)

    return f_code

def get_fcode_with_rating():
    f_rating_url = 'http://fund.eastmoney.com/data/fundrating.html#{0}'
    f_rating_url = f_rating_url.format(CONFIG['f_rating']['type'])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(f_rating_url)

    tree = lxml.html.fromstring(driver.page_source)
    path = '//table[@id="lbtable"]/tbody/tr/td[@class="dm"]/a'
    f_e = tree.xpath(path)
    f_e = f_e[:CONFIG['f_rating']['num']]

    f_code = [e.text_content() for e in f_e]

    return f_code

def fetch_f_code():
    if CONFIG['f_code']:
        return CONFIG['f_code']

    theme_code = get_fcode_with_theme()
    if theme_code:
        return theme_code

    rating_code = get_fcode_with_rating()
    return rating_code

def main():
    global BASIC_PAGE, OVERVIEW_PAGE, INDICATOR, RANGE
    load_config()

    basic_url = 'http://fund.eastmoney.com/{0}.html?spm=search'
    overview_url = 'http://fundf10.eastmoney.com/tsdata_{0}.html'
    req_headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            + 'Chrome/71.0.3578.98 Safari/537.36'
        }
    
    f_code = fetch_f_code()

    for fund in f_code:
        INDICATOR = {}
        INDICATOR['fund'] = fund

        resp = requests.get(basic_url.format(fund), headers=req_headers)
        BASIC_PAGE = resp.text
        basic_info()

        resp = requests.get(overview_url.format(fund), headers=req_headers)
        OVERVIEW_PAGE = resp.text
        overview_info()

        cal_score()

        RANGE.append(INDICATOR)

        print(INDICATOR, '\n')
    
    RANGE.sort(key=lambda x: x['score'], reverse=True)
    pprint.pprint(RANGE)


if __name__ == '__main__':
    main()
