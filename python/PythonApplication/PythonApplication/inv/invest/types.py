import enum


class ExeAction(enum.IntEnum):
    Buy = 0
    Sell = 1


class CaptchaWay:
    Local = 'local'
    BaiduApi = 'baidu_api'
    NineKwApi = '9kw_api'
    ChaoJiYingApi = 'chaojiying_api'
