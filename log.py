# coding=utf-8

#日志模块:参见教程 http://python.jobbole.com/82221/


import logging
import config

def logToFile(content):
    """将log日志保存到文件
        content:记录信息

        python logging 重复写日志问题：http://blog.csdn.net/huilan_same/article/details/51858817
    """
    """
    logger = logging.getLogger(config.LOGNAME) #根据名称获取日志对象
    logger.setLevel(logging.DEBUG) #DEBUG以上的日志级别会被此logger处理
    logfile = logging.FileHandler(config.LOGFILEPATH)#创建一个handler，用于将日志输出到文件中
    logfile.setLevel(logging.DEBUG) #handler对象也需要设置日志级别，由于一个logger可以包含多个handler，所以每个handler设置日志级别是有必要的
    formatter = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')
    logfile.setFormatter(formatter) #设置handler的日志输出格式
    logger.addHandler(logfile)  #logger是通过getLogger得到的Logger对象;将handlers绑定到logger上，一个logger对象可以绑定多个handler。
    logger.debug(content) #使用logger真正写日志

    #  添加下面一句，在记录日志之后移除句柄，否则会重复记录多条
    logger.removeHandler(logfile)
    """

    logger = logging.getLogger(config.LOGNAME) #根据名称获取日志对象
    #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        logger.setLevel(logging.DEBUG) #DEBUG以上的日志级别会被此logger处理
        logfile = logging.FileHandler(config.LOGFILEPATH)#创建一个handler，用于将日志输出到文件中
        logfile.setLevel(logging.DEBUG) #handler对象也需要设置日志级别，由于一个logger可以包含多个handler，所以每个handler设置日志级别是有必要的
        formatter = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')
        logfile.setFormatter(formatter) #设置handler的日志输出格式
        logger.addHandler(logfile)  #logger是通过getLogger得到的Logger对象;将handlers绑定到logger上，一个logger对象可以绑定多个handler。

    logger.debug(content) #使用logger真正写日志

if __name__=="__main__":
    pass
    #logToFile("出错了：www.baidu.com")
    #logToFile('hi')
    #logToFile('hi too')
    #logToFile('hi three')