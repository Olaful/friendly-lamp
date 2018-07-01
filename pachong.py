import requests
from bs4 import BeautifulSoup
import re

def getHtmlPage(url):
    html_data = requests.get(url)
    html_data.encoding = html_data.apparent_encoding
    if html_data.status_code == 200:
        return  html_data.text
    else:
        return None

def pasePage(HtmlText):
    soup = BeautifulSoup( HtmlText,'html5lib')
    data = soup.select('div.ranklist-wrapper.clearfix div.bd ul.song-list li')
    pattern1 = re.compile(r'<li.*?<div class="index">(.*?)</div>.*?title="(.*?)".*?title="(.*?)".*?</li>',re.S)
    pattern2 = re.compile(r'<li.*?<div class="index">(.*?)</div>.*?title="(.*?)".*?target="_blank">(.*?)</a>', re.S)

    dataWant = [];

    for item in data:
        findResult = re.findall(pattern1,str(item))
        if len(findResult) == 1:
            dataWant.append(findResult[0])
        else:
            otherWayData = re.findall(pattern2, str(item))
            dataWant.append(otherWayData[0])
    return dataWant

if __name__ == '__main__':
    url = 'http://music.taihe.com/'
    html = getHtmlPage(url)
    data = pasePage(html)
    for item in data:
        dict = {
            '序号':item[0],
            '歌名':item[1],
            '歌手':item[2]
        }

        print(dict)