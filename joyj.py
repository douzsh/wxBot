'''
Created on 2017-1-10

@author: Administrator
'''
import requests
import time
import bs4

class JOYJWebCrawler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.startPage= 'http://www.joyj.com'
        self.contents={}
        self.newc={}
    
    def __get_content__(self):
        result = requests.get(self.startPage)
        soup = bs4.BeautifulSoup(result.text,"lxml")
        for item in soup.find_all('div',"media bl_block"):
            url = ''
            content = ''
            price = ''
            for i in item.contents:
                if i.name!='div':
                    continue
                if i['class'][0]=='media-body':
                    content = i.a.text
                    for j in i.find('h4','media-extra').contents:
                        if j.name is None:
                            if(len(j.strip())>2):
                                price =  j.strip()
                if i['class'][0]=='media-link':
                    url = self.startPage + i.a['href']
            if not(self.contents.has_key(url)) and not(self.newc.has_key(url)):
                self.newc[url] = content+"--"+price
        pass
    
    def GetLatestCoupon(self):
        self.__get_content__()
        res = []
        for key in self.newc:
            res.append(key+"    "+self.newc[key])
        self.contents = dict(self.contents, **self.newc)
        self.newc={}
        return res
        
if __name__ == '__main__':
    joy = JOYJWebCrawler()
    print joy.GetLatestCoupon()
    #time.sleep(60)
    #print joy.GetLatestCoupon()
    
        