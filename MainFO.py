# coding=utf-8

#出队列下载文件的方法

from messagequery import *
from downFile import *
import dbmysql

if __name__=="__main__":
    ##下载图片
    ##deQueue(downloadImg,subject3)
    
    ##下载torrent
    ##deQueue(downloadTorrent,subject2)

    #摒弃队列方式，采用数据库读取
    dbmysql.selectTorrent(16360,2,downloadTorrent2)

    #摒弃队列方式，采用数据库读取
    #dbmysql.selectImg(0,2,downloadImg)