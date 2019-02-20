import os
import sys
import lxml.html

# 设置所需模块环境变量
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(path, 'spider_component')
sys.path.append(path)

from dowloader import Downloader
from aide import get_proxy, getAgent, ProxyScheduler
from storage import CsvHtml

def download():
    """
    获取电影列表并存入csv文件
    """
    # 114个页面
    url = 'https://www.dytt8.net/html/gndy/china/list_4_{}.html'
    urls = [url.format(i) for i in range(1, 115)]

    # 获取proxy与user-agent
    proxy = [get_proxy()]
    #proxy = ['223.85.196.75:9999']
    userAgent = getAgent()
    downloader = Downloader(delay=1, user_agent=userAgent, timeout=100, proxies=proxy, num_retries=3)

    # csv存储
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(path, 'myfile')
    file = os.path.join(filepath, 'dytt.csv')
    col_head = ['名称', '日期']

    csvHtml = CsvHtml(file=file, col_head=col_head)

    for url in urls:
        html = downloader(url)
        # html charset=gb2312,使用gbk解码
        if html:
            html.decode('gbk', 'ignore')
            tree = lxml.html.fromstring(html)

            titles = tree.cssselect('div.co_content8 b')
            dates = tree.cssselect('div.co_content8 font')

            for e in zip(titles, dates):
                row = [e[0].text_content(), e[1].text_content().split('\r\n')[0]]
                csvHtml(row)

if __name__ == '__main__':
    # 代理服务
    # ps = ProxyScheduler()
    # ps.run()

    download()