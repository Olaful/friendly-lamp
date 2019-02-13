import itchat
import requests
import time

KEY = 'b6109ca7c8704a11a5d8c49205403164'

def resp_api(msg):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': '123'
    }
    
    try:
        resp = requests.post(url=url, data=data)
        reply_text = resp.json()['text']
        return reply_text
    except:
        return '有事稍忙, 等下回复!'

# 文本信息回复
def wechat_reply():
    @itchat.msg_register(itchat.content.TEXT)
    def text_reply(msg):
        reply_msg = resp_api(msg['Text'])
        print('hello......:', msg['FromUserName'])
        #itchat.send_msg(reply_msg, toUserName=msg['FromUserName'])
        #msg.user.send('你好')
        return reply_msg

    @itchat.msg_register(itchat.content.RECORDING)
    def voice_reply(msg):
        return '现在不方便听语音, 发文字吧^_^'
    
    @itchat.msg_register(itchat.content.PICTURE)
    def picture_reply(msg):
        return '再发图片手机就没流量了。。。'
    
    itchat.auto_login(hotReload=True)
    itchat.run()

if __name__ == '__main__':
    wechat_reply()
