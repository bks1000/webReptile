# coding=utf-8

#作用是解析html，将需要下载的内容入队列（另起两个队列，一个下载torrent,一个是img）

import sys
import urllib2
from MyHtmlParser import * #或者 import MyHtmlParser.MyHtmlParser
import dbmysql
import messagequery
import chardet #chardet是一个非常优秀的编码识别模块
import log

#http request 报头（模拟网页请求）
headers={
                 'Host':'w1.vz05.bid',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                 'Accept':'*/*',
                 'Accept-Language':'zh-cn,zh;q=0.8',
                 #'Accept-Encoding':'gzip, deflate,sdch',#，如果你之前发送http请求之前，给了accept-encoding为gzip等值的话，那么返回的是压缩后的二进制，也会导致你看起来以为得到的是乱码，所以也需要你先去解压缩，再去解码才可以。
                 #'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
                 'Connection':'keep-alive',
                 #'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                 #'X-Requested-With':'XMLHttpRequest',
                 #'Referer':'http://imgloop.com/Home/article/'+self.number,
                 #'Content-Length':'12'
                 }

def parseHtml(url):
    """从给定url中，解析出想要的东西

        技术注意事项：
        有时候我们在爬取网络数据时，会因为对方网速缓慢、服务器超时等原因， 导致 urllib2.urlopen() 之后的 read()操作（下载内容）卡死
        http://blog.csdn.net/waterforest_pang/article/details/16885259
    """
    try:
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request,timeout=15) #设置超时时间为15秒
        html = response.read()
    
        """
        #html = html.decode('utf-8','replace').encode(sys.getfilesystemencoding())
        mychar = chardet.detect(html)
        bianma = mychar['encoding']
        print bianma #查看网页编码
        if bianma == 'utf-8' or bianma == 'UTF-8':
            pass
        else:
            html = html.decode('gb2312','ignore').encode('utf-8')
        """

        #print html
        parse = MyHtmlParser()
        parse.feed(html)
        #print parse.getItems()
        #pass
        #for i in parse.getItems():
        #    print i
        itemCount = len(parse.getItems()) #元素总个数
        group=[] #组一个组发送给入库程序(入库程序往队列里添加种子URL,往队列里添加图片URL)
        for i in range(0,itemCount): #注意range(0,12)只会输出 0~11 总共12个数字
            item = parse.getItems()[i]
            if i==itemCount-1:
                if '======' in item:
                    actor(group)
                elif 'freeone' in item:
                    group.append(item)
                    actor(group)
                else:
                    group.append(item)
                    actor(group)
            elif '======' in item:
                actor(group)
                group=[]#清空
                pass
            elif 'freeone' in item:
                group.append(item)
                actor(group)
                group=[]
            else:
                group.append(item)
    except Exception,e:
        print e
        log.logToFile(str(e)+"|"+url)

def actor(group):
    """
    处理解析出的内容
    group:list 类型，一组需要处理的信息
    """
    if len(group)<4:
        return
    try:
        group = list(set(group)) #去重复
        title=group[0]
        content=''
        torrent=''
        imgs='' #数据库对应字段
        imgs2=[] #图片连接地址
        count = len(group)
        for i in range(1,count):
            #print group[i]
            if 'http' in group[i] and 'html' in group[i]:
                #这是一个http链接,并且是一个html连接(torrent)
                torrent=getFileId(group[i])
                dbmysql.insertmqtorrent(torrent,group[i])#存数据库
            elif 'http' in group[i]:
                #这是一个图片链接
                imgs2.append(group[i]) #下载用
                imgs=imgs + getImgName(group[i])+','
                #dbmysql.insertmqimg(','.join(imgs2));#存数据库
            else:
                #这是内容
                content = content + group[i]+','

        #将种子名存入队列（单独队列）
        #messagequery.enQueue2(torrent,messagequery.subject2)
        #将图片数组顺序存入队列（单独的队列）
        #for i in range(len(imgs2)):
        #    messagequery.enQueue2(imgs2[i],messagequery.subject3)
        
        dbmysql.insertmqimg(','.join(imgs2));#存数据库
        dbmysql.insert(title,content,torrent,imgs)#存入数据库
    except Exception,e:
        print e
        log.logToFile(str(e)+"|"+url)

def getFileId(url):
    """获取URL中的 种子 ID
        下载种子是根据种子ID
    """
    parsed = urlparse(url)
    #print parsed
    path = parsed.path
    strs = path.split('/')
    #print strs[-1][0:-5]
    return strs[-1][0:-5]

def getImgName(url):
    """获取图片名"""
    parsed = urlparse(url)
    #print parsed
    path = parsed.path
    strs = path.split('/')
    return strs[-1][0:-4] #以.jpg结尾

if __name__=="__main__":
    #pass
    #解析html 全部测试通过
    #合集
    #parseHtml('http://c2.1024mx.trade/pw/htm_data/3/1609/426759.html')
    parseHtml('http://c2.1024mx.trade/pw/htm_data/3/1608/406185.html')
    #单个
    #parseHtml('http://c2.1024mx.trade/pw/htm_data/5/1609/430111.html ')