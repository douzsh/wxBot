#!/usr/bin/env python
# coding: utf-8

import ConfigParser
import time
import thread
import requests
import json
from joyj import JOYJWebCrawler
from wxbot import WXBot

coupon = JOYJWebCrawler()
keywords=[u'UNIQLO',u"NIKE",u"运动",u"蓝牙",u"小米",u"迪卡侬"]

def KerWordCheck(res):
    for i in keywords:
        if res.find(i)>0:
            return True
    return False

def sendWeatherReport(bot, delay):
    weather = ''
    while True:
        weather = bot.tuling_auto_reply(u'd', u"北京天气")
        bot.send_msg_to_group(weather)
        time.sleep(delay)
      
def sendJOYJInfo(bot, delay):
    while True:
        res = coupon.GetLatestCoupon()
        for item in res:
            if KerWordCheck(item):
                bot.send_msg_to_group(item)
                print res
        time.sleep(delay)

class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        if(self.DEBUG):
            print 'tuling_key:', self.tuling_key

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " + \
                        k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')
            if(self.DEBUG):
                print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']            
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作', u'开始']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
                    return
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])
                    return
        # for add keyword
        if(msg_data.split(' ')[0]==u'添加'):
            for word in msg_data.split(' '):
                if(word != u'添加'):
                    keywords.append(word) 
                    self.send_msg_by_uid(u'[Robot]' + u'添加关键词:'+word, msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = '@' + src_name + ' '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])
                    
    def send_msg_to_group(self, content):
        if(len(content) < 2):
            return
        for group in self.group_list:
            if(group['PYQuanPin'] == 'babablacksheep') or (group['PYQuanPin'].find('douzsh')>0):
                self.send_msg_by_uid(content,group['UserName'])


def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    thread.start_new(sendJOYJInfo, (bot, 60))
    thread.start_new(sendWeatherReport, (bot, 60*60*12))
    bot.run()


if __name__ == '__main__':
    main()

