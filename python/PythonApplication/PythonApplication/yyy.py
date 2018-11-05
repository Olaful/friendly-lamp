# 新闻组信息获取模块
from nntplib import NNTP
import time
import datetime
#yesterday = time.time() - 24*60*60
#yesterday = time.localtime(yesterday)

#date = time.strftime('%y%m%d', yesterday)
#hour = time.strftime('%H%M%S', yesterday)
# 十天以前
yesterday = datetime.date.today() + datetime.timedelta(days = -4)

servername = 'web.aioe.org'
group = 'comp.lang.python.announce'
# 向NNTP服务器发送一条newnews指令
server = NNTP(servername)
# 获取全部新闻组信息
(resp, count, first, last, name) = server.group(group)
# 获取指定日期之后的新闻组信息，ids为文章ID
(resp, ids) = server.newnews(group, yesterday)
body = server.body('<mailman.355.1541073920.2799.python-announce-list@python.org>')[1].lines
print(body)

subject = []
for id in ids:
    (resp, ArticleInfoObj) = server.head(id)
    for line in ArticleInfoObj.lines:
        if line.lower().startswith(b'subject:'):
            subject = line[9:]
            break
    body = server.body(id)[1].lines

    print(subject)
    print('-'*len(subject))
    print('\n'.join([b.decode('ISO-8859-15') for b in body]))