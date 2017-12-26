# coding=utf-8

#分析URL类；将传入的url返回的html，分析出其中的可用url
#分析可用url时，采用策略模式，把算法分离，使其更通用

import urllib2,urllib
import re
from messagequery import *
import dbmysql


def getUrlFromUrl(p):
    """根据url获取网页中的url并加入消息队列中
        p：传入的url
    """
    request = urllib2.Request(p, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        response = urllib2.urlopen(request,timeout=15)
        #print response.getcode()
        #return the meta-information of the page, such as headers, in the form of an mimetools.Message instance
    
        info = response.info()
        #判断执行状态(递归出口)
        code = response.getcode()
        print code
        if code<>200:
            print "!200"
            return
        if info['Content-Type'][0:9]<>'text/html':
            print info['Content-Type'][0:9]
            return
        else:
            #sendMsg(p)#加入activemq消息队列中；另外一个进程去消费消息，注意判断getcode==200即请求成功，才处理
            pass
    
        html = response.read()

        #=======================获取网页上的url================
        #res = r'<a .*?>(.*?)</a>'               #获取链接文本内容
        #res = r'<a.*?href=.*?<\/a>'             #获取完整链接内容
        res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"  #获取链接中URL
        urls = re.findall(res_url, html, re.I|re.S|re.M)
        print '================================================================'
        urls = list(set(urls))#去除list中的重复数据
        urls = sorted(urls)
        print urls
        for url in urls:
            #print url
            if len(url)>8 and url[0:8]=="htm_data": #将真正的文章，存入消息队列
                print "++++++++"+'http://c2.1024mx.trade/pw/'+url
                #enQueue('http://c2.1024mx.trade/pw/'+url)
                dbmysql.insertmqweburl('http://c2.1024mx.trade/pw/'+url)#存队列也存数据库
                print 1
                continue
            if url == '/sign_in':
                print 2
                continue
            if url == '/sign_up':
                print 3
                continue
            if url == '/':
                print 4
                continue
            if len(url)>11 and url[0:11] == 'javascript:':
                print 5
                continue       
            if url[0]=='#':
                print 6
                continue
            if len(url)>3 and url[-3]==".": #去除js
                print 7
                continue
            if len(url)>4 and url[-4]==".": #去除 .css
                print 8
                continue
            #if url[0:8]=="htm_data":
            #    url = 'http://c2.1024mx.trade/pw/'+url
                
            #if url[0:len(p)]<>p: #去除域外地址
            #    print 9
            #    continue
            #if url==p+"/": #去除和传入地址相同的地址（否则会无限循环）
            #    print 10
            #    continue
            #if len(url)>7 and url[0:7]=="http://":
            #    if url==p:
            #        continue
            #    print "XXX---"+url+"---XXX"
            #    #递归调用
            #    #getUrlFromUrl(url)
            
            
    except urllib2.HTTPError, e:
        print '****'
        print e.getcode()  
        print e.reason  
        print e.geturl() 
        print '****'
        return

if __name__=='__main__':
    pass
    #getUrlFromUrl('http://c2.1024mx.trade/pw/thread.php?fid=3')
