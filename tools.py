#!/usr/bin/env python
# coding: utf-8

__author__ = 'iceke'

import re

def emoji_dealer(name):
    regex = re.compile('<span class="emoji (.*?)"></span>')
    match = regex.findall(name)
    if len(match) > 0:
        print name
        for i in match:
            strOri = '<span class="emoji {0}"></span>'.format(i)
            try:
                flag = re.search('emoji([\da-z]{5})', i).groups()[0]
            except:
                flag = i[5:]
            flag = flag.zfill(8)
            name = name.replace(strOri, ('\\U%s'%flag).decode('unicode-escape'))
    return name


def check_file(fileDir):
    try:
        with open(fileDir):
            pass
        return True
    except:
        return False


def to_unicode(string, encoding='utf-8'):
        """
        将字符串转换为Unicode
        :param string: 待转换字符串
        :param encoding: 字符串解码方式
        :return: 转换后的Unicode字符串
        """
        if isinstance(string, str):
            return string.decode(encoding)
        elif isinstance(string, unicode):
            return string
        else:
            raise Exception('Unknown Type')
        
if __name__ == '__main__':
    name = u'<span class="emoji emoji1f463"></span>黑白幻影<span class="emoji emoji1f49e"></span>'
    print emoji_dealer(name)
    name = u'ʚ<span class="emoji emoji2764"></span>ɞ'
    print emoji_dealer(name)


#print emoji_dealer("Ivory<span class=\"emoji emoji1f338\"></span>adsa")
#a= emoji_dealer("dads<span class=\"emoji emoji1f338\"></span>dad<span class=\"emoji emoji200\"></span>5sds")

#a = ('2005',)
#print '@'+"member"+('\\u2005').decode('unicode-escape')

