#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/7/2 17:31
#@Author :weige
#@File :hh.py

import time
import sys
import stomp
# from articles.models import ArticlePost
class Point():
    pass
a = Point()
a.x = 5
print(a)
class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        time.sleep(2)


conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MyListener())
conn.start()
conn.connect()
# 注意，官方示例这样发送消息的  $ python simple.py hello world
# conn.send(body='hello,garfield! this is '.join(sys.argv[1:]), destination='/queue/test')
# article = ArticlePost.objects.get(id = 40)

# 发送消息到队列\
conn.send(body=a, destination = '/queue/test')

# 发送消息到主题
conn.send(body='this is message', destination = '/topic/testTopic')

# 从队列接受消息
conn.subscribe(destination='/queue/test', id=1, ack='auto')

# 从主题接受消息
conn.subscribe(destination='/topic/testTopic', id=2, ack='auto')

time.sleep(2)
conn.disconnect()

