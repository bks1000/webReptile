# coding=utf-8

#入队列的main方法

from messagequery import *
from analysisUrl import *
from parseHtml import *
import dbmysql

if __name__=="__main__":
    #先执行
    #亚洲无码系列 将侦测到的url加入队列
    #for i in range(1,239):
        #getUrlFromUrl('http://c2.1024mx.trade/pw/thread.php?fid=5&page='+str(i))
    #最新合集系列
    #for i in range(16,94):
        #getUrlFromUrl('http://c2.1024mx.trade/pw/thread.php?fid=3&page='+str(i))

    #个人专区
    #for i in range(135,323):
        #print '======第 %s 页======' % str(i)
        #getUrlFromUrl('http://c2.1024mx.trade/pw/thread.php?fid=21&page='+str(i))

    ##上面执行完成后，执行这里
    ##将网址出队列，分析网页内容，插入数据库，并且添加新队列
    ##deQueue(parseHtml,subject)

    #摒弃队列的方式了，直接读数据库，操作
    #dbmysql.selectWeburl(6800,1000,parseHtml)