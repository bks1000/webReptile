# coding=utf-8

#html解析类，对于需要在网页上提取内容时，使用。
#由于处理的网页不同，可能需要针对不同的网站，写不同的解析类
#这个解析类针对1024网站

import HTMLParser
from htmlentitydefs import entitydefs
from urlparse import urlparse

class MyHtmlParser(HTMLParser.HTMLParser):
    """参考：http://www.cnblogs.com/coser/archive/2012/01/09/2317076.html"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.items=[] #保存提取结果
        self.flag = False
        self.date_start = False
        self.isIncontent= False#在content中的img才会保存下来
        self.text =""
        self.link = ""
        

    def handle_starttag(self,tag,attrs):
        """处理开始标签"""
        #片名
        if tag=='h1':
            self.flag=True
            self.date_start=True
        #介绍
        if 'div'==tag and attrs[0][0]=='class' and attrs[0][1]=='tpc_content':
            #print attrs
            self.flag=True
            self.date_start=True
            self.isIncontent=True

        if self.isIncontent and 'img'==tag:
            #print attrs
            #for attr in attrs:
            self.items.append(attrs[0][1])
            #print attrs[0][1]
            

    def handle_data(self,data):
        """处理数据"""
        if self.flag:
            if 'nbsp'==data:
                return
            if 'br'==data:
                return
            if ' '==data:
                return

            self.text = data
            self.items.append(data)
            #print data.decode('utf-8').encode(sys.getfilesystemencoding())
            #print data #已经编码过了

    def handle_entityref(self,name):
        """处理实体引用"""
        if entitydefs.has_key(name):
            self.handle_data(name)
        else:
            self.handle_data('&'+name)

    def handle_endtag(self,tag):
        """处理结束标签"""
        if tag=='h1' and self.flag:
            self.flag=False
            self.date_start=False

        if 'div'==tag and self.flag:
            self.flag=False
            self.date_start=False
            self.isIncontent=False

    def getItems(self):
        return self.items
