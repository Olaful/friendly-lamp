import json
import urllib.parse
import urllib.request
import os

# 读取webhose search key
def read_webhose_key():

    web_hose_key = None

    try:
        with open('E:\hexo\source.Olaful.github.io\Olaful.github.io\python\DjangoWebProject\django_newswebsite\search.key', 'r') as f:
            web_hose_key = f.readline().strip()
    except:
        raise IOError('search key not found')

    return web_hose_key

# 根据关键字请求webhose api查询
def run_query(search_item, size=10):

    web_hose_key = read_webhose_key()

    if not web_hose_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'

    query_str = urllib.parse.quote(search_item)

    search_url = ('{root_url}?token={key}&format=json&q={query}&sort=relevancy&size={size}'.format
                 (root_url=root_url, key=web_hose_key, query=query_str, size=size))

    rls = []

    try:
        resp = urllib.request.urlopen(search_url).read().decode()
        json_resp = json.loads(resp)
        for post in json_resp['posts']:
            rls.append({'title': post['title'], 'link': post['url'], 'summary': post['text'][0:200]})
    except:
        print('通过webhose查询出错')

    return rls

def main():
    search_item = None
    search_item = input("请输入搜索关键词:")
    rls = run_query(search_item)
    for r in rls:
        print(r['title']+'\n')
        print(r['summary']+'\n')


if __name__ == '__main__':
    main()