# coding=utf-8
"""
此工具用于从csv文件中读取某列(ANSI编码)
参考：https://blog.csdn.net/allyli0022/article/details/79125672
"""

import csv

"""
#UTF-8 编码的csv文件
with open('D:\\MyCode\\hack\\YJ\\SZJY\\t_yuangong.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile)
    #column = [row['yg_id'] for row in reader]
    #print column
    for row in reader:
        #print row['yg_id']
"""

#ANSI编码的csv文件(GBK)
import os
import codecs
#with open('D:\\t_file.csv','rb',encoding='GBK') as csvfile:
with codecs.open('D:\\t_file.csv','rb',encoding='GBK') as csvfile:
    reader = csv.DictReader(csvfile)
    #column = [row['yg_id'] for row in reader]
    #print column
    for row in reader:
        u = (row['f_url'])
        strGbk = u.encode('gbk')
        print strGbk
        
        dics= (strGbk).split('\\\\')
        #print dics
        cnt = len(dics)
        #print cnt
        fullpath =FILEPATH+"\\".join(dics[0:cnt-1])+"\\"
        print fullpath
        if(not os.path.exists(fullpath)):
            os.makedirs(fullpath)
        #print fullpath
        
        