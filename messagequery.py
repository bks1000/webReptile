# coding=utf-8

#消息队列操作类(函数库)
#消息队列这里的缺陷在于：1：没有消息日志，2：出队列时不是一个一个出，3：并发及重复处理问题。
#目前用数据库代替消息队列

from stompySimple import Client
import time

subject = 'mq/weburl' #队列名称【即往这个队列里添加，消费的时候，也是这个名字！】
subject2 = 'torrent'
subject3 = 'img'

def enQueue(data):
    """入队列"""
    stomp = Client() #这里连接的是172.18.13.116在stompySimple.py中设置
    stomp.connect('admin','admin')
    stomp.put(data, destination=subject)
    time.sleep(2)
    stomp.disconnect()

def enQueue2(data,subj):
    """入队列2
        data:入队列的数据
        subj:队列名
    """
    stomp = Client() #这里连接的是172.18.13.116在stompySimple.py中设置
    stomp.connect('admin','admin')
    stomp.put(data, destination=subj)
    time.sleep(2)
    stomp.disconnect()


def deQueue(handler,subj):
    """出队列(传入出队列后，消息的处理函数)
       函数可以作为一个对象，进行参数传递。函数名(比如func)即该对象

       subj:队列名,表示你要读取哪个队列
    """
    stomp = Client() #这里连接的是172.18.13.116在stompySimple.py中设置
    conn = stomp.connect('admin','admin')
    stomp.subscribe(destination=subj) #订阅消息
    while True:
        message = stomp.get()	#获取消息信息
        print message.body	#消息体（这里是一个URL地址）
        #stomp.ack(message)#Acknowledge message.[确认消息]
        handler(message.body)

    stomp.unsubscribe(subject) #取消订阅
    stomp.disconnect()		#断开连接
