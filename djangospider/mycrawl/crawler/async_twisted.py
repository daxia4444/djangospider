#coding=utf-8
from twisted.internet import defer, reactor,task
from twisted.web.client import getPage
import threading
import time
import logging

logger= logging.getLogger()
from djangospider.utils.util import record_failure
ISOTIMEFORMAT='%Y-%m-%d %X'

class Twisted_download():
  
  def __init__(self,sche_queue,task_queue,failure_queue):
    self.sche_queue=sche_queue
    self.task_queue=task_queue
    self.failure_queue=failure_queue
    self.i=0
    self.RunMain()


  def handle_request(self,response,url,func):
    element=(response,func,url)      
    self.task_queue.put(element)
    logger.info("add element into task_queue")


  def handle_error(self,result,url,func):
    self.failure_queue.put(url)
    logger.error("error: %s   url: %s"  %(result,url))
    record_failure("%s   url: %s    callback: %s \n" %(time.strftime(ISOTIMEFORMAT,time.localtime()),url,func.__name__))



  def add_url(self):
    try:      
      if self.sche_queue.empty():
        #time.sleep(1)
        self.i=self.i+1
        if self.i>60:
          print "add_url stop self.i=%d" %self.i
          reactor.stop()          

      else:
        element = self.sche_queue.get_nowait()
        url=element[0]
        callback=element[1]

        http_header   = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Referer':"http://www.baidu.com/" }
        d = getPage(url,timeout=60,headers=http_header)
        d.addCallback(self.handle_request,url,callback)
        d.addErrback(self.handle_error,url,callback)
        self.i=0

    except Exception as e:
      logger.exception(e)
      time.sleep(1)



  def finish(self):
    reactor.stop()



  def RunMain(self):
    try:

      heartbeat=task.LoopingCall(self.add_url)
      heartbeat.start(1)
      reactor.run()
    except KeyboardInterrupt:
      pass






