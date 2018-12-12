import requests
from bs4 import BeautifulSoup
import re
import sys, time

# 爬虫类
class Reptile():
    url = ""

    def __init__(self, url):
        self.url = url

    def getHtmlPage(self):
        html_data = requests.get(self.url)
        html_data.encoding = html_data.apparent_encoding
        if html_data.status_code == 200:
            return  html_data.text
        else:
            return None

    def pasePage(self):
        HtmlText = self.getHtmlPage()
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

# 进度条类
class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 50 #进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar) #这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()
    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0

if __name__ == '__main__':
    way = "processbar"

    if way == "pachong":
        url = 'http://music.taihe.com/'
        reptile = Reptile(url)
        #html = reptile.getHtmlPage()
        data = reptile.pasePage()
        for item in data:
            dict = {
             '序号':item[0],
             '歌名':item[1],
             '歌手':item[2]
            }

            print(dict)
    elif way == "pachong":
        max_steps = 100
        process_bar = ShowProcess(max_steps, 'OK')
        for i in range(max_steps):
            process_bar.show_process()
            time.sleep(0.01)
