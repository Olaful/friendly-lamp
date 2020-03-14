import requests
import os
import json
import lxml.html
import re
import pypinyin


BASIC_PAGE = ''
OVERVIEW_PAGE = ''
CONFIG = {}
INDICATOR = {}


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
    rtn = float(rtn[:-1]) / 100
    INDICATOR['rtn_1y'] = round(rtn, 5)

def return_6m(tree):
    path = '//dl[@class="dataItem03"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[0].text_content()
    rtn = float(rtn[:-1]) / 100
    INDICATOR['rtn_6m'] = rtn

def return_3m(tree):
    path = '//dl[@class="dataItem02"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[1].text_content()
    rtn = float(rtn[:-1]) / 100
    INDICATOR['rtn_3m'] = rtn

def return_1m(tree):
    path = '//dl[@class="dataItem01"]/dd/span[contains(@class, "ui-font-middle")]'
    rtn_e = tree.xpath(path)
    rtn = rtn_e[0].text_content()
    rtn = float(rtn[:-1]) / 100
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
    risk_ind = float(risk_ind[:-1]) / 100
    INDICATOR['std_dt'] = round(risk_ind, 5)

def sharp_ratio(tree):
    path = '//table[@class="fxtb"]/tr/td'
    risk_e = tree.xpath(path)
    risk_ind = risk_e[5].text_content()
    risk_ind = float(risk_ind)
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
    scoreavg = float(scoreavg)

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
    pf_score = INDICATOR['perform']['avg'] * CONFIG['weight']['perform']
    std_dt_score = -INDICATOR['std_dt'] * CONFIG['weight']['std_dt']
    sharp_ratio_score = INDICATOR['sharp_ratio'] * CONFIG['weight']['sharp_ratio']

    INDICATOR['score'] = round(sum([rtn_score, pf_score, std_dt_score, sharp_ratio_score]))


def main():
    global BASIC_PAGE, OVERVIEW_PAGE, INDICATOR
    load_config()

    basic_url = 'http://fund.eastmoney.com/{0}.html?spm=search'
    overview_url = 'http://fundf10.eastmoney.com/tsdata_{0}.html'
    req_headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            + 'Chrome/71.0.3578.98 Safari/537.36'
        }

    for fund in CONFIG['f_code']:
        INDICATOR = {}
        INDICATOR['fund'] = fund

        resp = requests.get(basic_url.format(fund), headers=req_headers)
        BASIC_PAGE = resp.text
        basic_info()

        resp = requests.get(overview_url.format(fund), headers=req_headers)
        OVERVIEW_PAGE = resp.text
        overview_info()

        cal_score()

        print(INDICATOR, '\n')


if __name__ == '__main__':
    main()