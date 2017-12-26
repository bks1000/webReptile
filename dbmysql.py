# -*- coding: utf-8 -*-

#mysql数据库操作类
#将有效数据存入数据库


import mysql.connector
#import _mysql_connector
import config
from messagequery import *
import log


import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


#ccnx = _mysql_connector.MySQL() #它不支持charset
# mysql连接配置
#参数参见：http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
config = {
              'user':'root', 
              'password':'111111', 
              'host':config.DBIP, #localhost
              'port':3306,
              'charset':'utf8',
              'database':'website'}

#ccnx.connect(**config)

def insert(title,content,torrentName,imgs):
    """
    title:片名
    content:简介
    torrentName:种子名
    imgs:图片名','分隔
    """
    # 打开数据库连接
    # 创建连接
    db = mysql.connector.connect(**config)
    #db = mysql.connector.connect("localhost","root","111111","website" )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    #这种方式不可取！！！
    #title = ccnx.escape_string(title.encode('utf-8')) 
    #content = ccnx.escape_string(content.encode('utf-8')) 

    sql = "insert into torrent(title,content,torrentname,imgs) VALUES('"+title+"','"+content+"','"+torrentName+"','"+imgs+"')"
    #print sql
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception,e:
        #logfile.write(e)   
        # Rollback in case there is any error
        print e
        log.logToFile(str(e)+"|"+title+'|'+content+'|'+torrentName+'|'+imgs)
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()

def insertmqimg(url):
    """将消息队列中的图片url存入数据库"""
    db= mysql.connector.connect(**config)
    cursor=db.cursor()
    sql="INSERT INTO mqimg(imgurl) VALUES('"+url+"')"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e:
        print e
        db.rollback()
    finally:
        db.close()

def insertmqtorrent(name,url):
    """将消息队列中的torrent存入数据库"""
    db=mysql.connector.connect(**config)
    cursor=db.cursor()
    sql="INSERT INTO mqtorrent(torrenturl,torrentname) VALUES('"+url+"','"+name+"')"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e:
        print e
        db.rollback()
    finally:
        db.close()

def insertmqweburl(url):
    """将消息队列中的weburl存入数据库"""
    db = mysql.connector.connect(**config)
    cursor=db.cursor()
    sql="INSERT INTO mqweburl(weburl) VALUES('"+url+"')"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e:
        print e
        db.rollback()
    finally:
        db.close()

def reloadtorror():
    """重新从数据库中读出torrent，重新插入到队列中"""
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = 'SELECT torrentname FROM torrent LIMIT 0,933' #取前933条
    data = cursor.execute(sql)
    for d in range(0,933): 
        torrentname = cursor.fetchone()[0]
        print torrentname
        enQueue2(torrentname,subject2)

def selectWeburl(start,count,handler):
    """查询出url并执行解析
        start:起始位置(从0开始，行号)
        count:条数
        handler:处理url函数
    """
    db=mysql.connector.connect(**config)
    cursor=db.cursor()
    sql="SELECT weburl FROM mqweburl LIMIT "+str(start)+","+str(count)
    cursor.execute(sql)
    data = cursor.fetchall() #返回结果是[(),(),...]
    for d in data:
        url=d[0]
        handler(url)

def selectTorrent(start,count,handler):
    """查询种子URL,并执行下载（下载函数传入）
        start:起始位置(从0开始，索引)
        count:条数
        handler:下载种子函数
    """
    db = mysql.connector.connect(**config)
    cursor=db.cursor()
    sql="SELECT torrenturl,torrentname FROM mqtorrent LIMIT "+str(start)+","+str(count)
    cursor.execute(sql)
    data=cursor.fetchall() #返回结果:[(,),(,),...]
    print data
    for d in data:
        #print d[0]
        #print d[1]
        handler(d[0],d[1])

def selectImg(start,count,handler):
    """查询图片URL，并执行下载
        start:起始位置
        count:条数
        handler:下载图片函数
    """
    db = mysql.connector.connect(**config)
    cursor=db.cursor()
    sql="SELECT imgurl FROM mqimg LIMIT "+str(start)+","+str(count)
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        imgs=d[0].split(',')
        for img in imgs:
            print img
            handler(img)

if __name__=='__main__':
    #insertmqimg('a')
    #insertmqtorrent('name','aaa')
    #insertmqweburl('a')

    selectTorrent(0,10,None)
    pass
    #
    #reloadtorror()