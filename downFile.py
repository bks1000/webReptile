# coding=utf-8

#下载文件（包括POST和GET方式）
#对于种子，只能在linux下运行(在windows下会把回车写成\r\n ,linux下是\n)
#重新建立一个种子队列，这样可以使下载文件脚本独立在linux下运行（解耦合）


import sys,os
import httplib,urllib,urllib2
import time
from urlparse import urlparse
import config
import log

reload(sys)
sys.setdefaultencoding('utf-8')

#如果下载一直超时，请分析http请求头

#http request 报头（img下载）
headers_img={
                 'Host':'img2.showhaotu.xyz', #这个地方要改
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48',
                 'Accept':'*/*',
                 'Accept-Language':'zh-CN',
                 #'Accept-Encoding':'gzip, deflate,sdch',#，如果你之前发送http请求之前，给了accept-encoding为gzip等值的话，那么返回的是压缩后的二进制，也会导致你看起来以为得到的是乱码，所以也需要你先去解压缩，再去解码才可以。
                 #'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
                 'Connection':'Keep-Alive',
                 #'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                 #'X-Requested-With':'XMLHttpRequest',
                 #'Referer':'http://imgloop.com/Home/article/'+self.number,
                 #'Content-Length':'12'
                 }
#下载使用的HTTP请求头（torrent下载）
headers_down={
                 'Host':'www2.jsnewsupdownspaces.info', 
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                 'Accept':'*/*',
                 'Cache-Control': 'max-age=0',
                 'Pragma': 'no-cache',
                 'Accept-Language':'zh-cn,zh;q=0.8',
                 #'Accept-Encoding':'gzip, deflate,sdch',#，如果你之前发送http请求之前，给了accept-encoding为gzip等值的话，那么返回的是压缩后的二进制，也会导致你看起来以为得到的是乱码，所以也需要你先去解压缩，再去解码才可以。
                 #'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
                 'Connection':'keep-alive',
                 'Content-Type':'application/x-www-form-urlencoded',
                 #'X-Requested-With':'XMLHttpRequest',
                 'Referer':'http://imgloop.com/Home/article/',#修改这个
                 'Origin': 'http://www1.j32048downhostup9s.info',
                 'Upgrade-Insecure-Requests': '1',
                 'Content-Length':'36'
                 }


def downloadTorrent(fileid):
    """测试POST方式下载torrent
        fileid:torrent文件名
    """
    #urllib2.urlopen('http://www2.jsnewsupdownspaces.info/freeone/freeone/ad.php')
    #---
    try:
        params=urllib.urlencode({'type':'torrent','id':fileid,'name':fileid})
        downurl = 'http://www2.jsnewsupdownspaces.info/freeone/down.php'
        conn = httplib.HTTPConnection('www2.jsnewsupdownspaces.info')
        conn.request('POST',downurl,params,headers_down)
        response = conn.getresponse()
        print response.status
        if response.status==200 or response.status==302:
            fileName = fileid+'.torrent'
            #检查文件是否被下载过
            if os.path.exists(fileName):
                print '%s has been downloaded.',fileName
                conn.close()
                return
            while(True):
                try:
                    f=open(config.FILEPATH+fileName,'w')
                    data = response.read()
                    #f.write(data.decode('utf-8','replace').encode(sys.getfilesystemencoding()))
                    #f.write(data.replace(b'\r\n',b'\n'))#windows下应该这么处理，只是并没有替换(replace处理的是字符串，而这个字符串是一段二进制)
                    f.write(data) #linux下正确
                    f.close()
                except Exception:
                    print '%s has a error' ,fileName
                    #time.sleep(self.sleepTime)
                    #Redownload.
                    #continue
                finally:
                    print '%s download completed.',fileName
                    #End of the download.
                    break
        else:
            print '%s download failed.'
            conn.close()
    except Exception,e:
        print e
        log.logToFile(str(e)+'|'+fileid)


def downloadTorrent2(url,fileid):
    """ POST方式下载torrent
        url:torrent文件下载url(downurl不能写死，因为这些种子文件下载地址来自不同的域名)
        fileid:torrent文件名
    """
    #urllib2.urlopen('http://www2.jsnewsupdownspaces.info/freeone/freeone/ad.php')
    #---
    try:
        fileName = fileid+'.torrent'
        #检查文件是否被下载过
        if os.path.exists(config.FILEPATH+fileName):
            print '%s has been downloaded.',fileName
            #conn.close()
            return
        params=urllib.urlencode({'type':'torrent','id':fileid,'name':fileid})
        #这里写死，对于不同的domain就会执行不下去了
        #downurl = 'http://www2.jsnewsupdownspaces.info/freeone/down.php'
        #conn = httplib.HTTPConnection('www2.jsnewsupdownspaces.info')
        urldata = urlparse(url)
        domain = urldata.netloc
        downurl = urldata.scheme+'://'+urldata.netloc+'/'+urldata.path.split('/')[1]+'/down.php'
        conn = httplib.HTTPConnection(domain,timeout=15)
        headers_down['Host']=domain #修改请求头
        headers_down['Referer']=url #修改请求头
        headers_down['Origin']=urldata.scheme+'://'+urldata.netloc #修改请求头
        conn.request('POST',downurl,params,headers_down)
        response = conn.getresponse()
        print response.status
        if response.status==200 or response.status==302:
            #fileName = fileid+'.torrent'
            #检查文件是否被下载过
            if os.path.exists(config.FILEPATH+fileName):
                print '%s has been downloaded.' % fileName
                conn.close()
                return
            while(True):
                try:
                    f=open(config.FILEPATH+fileName,'w')
                    data = response.read()
                    #f.write(data.decode('utf-8','replace').encode(sys.getfilesystemencoding()))
                    #f.write(data.replace(b'\r\n',b'\n'))#windows下应该这么处理，只是并没有替换(replace处理的是字符串，而这个字符串是一段二进制)
                    f.write(data) #linux下正确
                    f.close()
                except Exception:
                    print '%s has a error' % fileName
                    #time.sleep(self.sleepTime)
                    #Redownload.
                    #continue
                finally:
                    print '%s download completed.' % fileName
                    #End of the download.
                    break
        else:
            print '%s download failed.'
            conn.close()
    except Exception,e:
        print e
        log.logToFile(str(e) + '|' + url + '|' +fileid)

def downloadImg(url):
    """下载图片get
        url:图片的url地址
    """
    try:
        urldata= urlparse(url)
        domain=urldata.netloc
        headers_img['Host']=domain
        fileName= url.split('/')[-1]
        if os.path.exists(config.FILEPATH+fileName):
            print '%s has been downloaded.',fileName
            return
        
        if urldata.scheme=='http':
            conn = httplib.HTTPConnection(domain,timeout=15)
            conn.request('GET', url,headers=headers_img)
            response = conn.getresponse()
            #filename= url.split('/')[-1]
            f = open(config.FILEPATH + fileName,'wb') #注意修改路径
            f.write(response.read())
            f.close()
        if urldata.scheme=="https":
            #headers_img['Host']=domain[0:-3]+"io" #通过抓包工具fiddle发现，https访问.org后，返回301，重新访问了.io
            conn = httplib.HTTPSConnection(domain,timeout=15)
            #url = url.replace('.org','.io') #通过抓包工具fiddle发现，https访问.org后，返回301，重新访问了.io
            conn.request('GET', url,headers=headers_img)
            response = conn.getresponse()
            if response.status==301: #重定向，重新发起请求
                #print response.getheaders()
                newurl = response.getheader("location")
                downloadImg(newurl)
                
            #filename= url.split('/')[-1]
            data = response.read()
            if data=="":
                return

            f = open(config.FILEPATH + fileName,'wb') #注意修改路径
            f.write(data)
            f.close()
    except Exception,e:
        print e
        log.logToFile(str(e) + '|' + url)

#测试
if __name__=='__main__':
    #downloadTorrent2('http://www1.j1gcnewsupdownspaces.info/freeone/file.php/OD2RK2b.html','OD2RK2b')
    pass
    #torrent 测试通过
    #downloadTorrent('ODAMFHe')
    #图片
    #https测试通过
    #downloadImg('https://s22.postimg.org/72fbxapg1/NATR538_B.jpg')
    #http测试通过
    downloadImg('http://cdn3.snapgram.co/imgs/2016/06/25/QQ20160625224520.jpg ')