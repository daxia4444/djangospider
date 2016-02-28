#!/usr/bin/env python
#coding=utf-8

import threading
import tornado.ioloop
from tornado.curl_httpclient import CurlAsyncHTTPClient
import time

import logging
logger= logging.getLogger()

from djangospider.utils.util import record_failure
ISOTIMEFORMAT='%Y-%m-%d %X'


class MyCurlAsyncHTTPClient(CurlAsyncHTTPClient):

    def free_size(self):
        return len(self._free_list)

    def size(self):
        return len(self._curls) - self.free_size()

class download_AsyncHTTPClient():

    def __init__(self,sche_queue,task_queue,failure_queue):
        '''
        init three queue

        sche_queue : the start_url we need crawl
        task_queue : ready to store the html content and callback function when success crawl
        failure_queue :  ready to store the fail url when crawl url 


        '''
        self.sche_queue=sche_queue
        self.task_queue=task_queue
        self.failure_queue=failure_queue        
        self.ioloop = tornado.ioloop.IOLoop()
        self.http_client = MyCurlAsyncHTTPClient(max_clients=100,io_loop=self.ioloop)
        self.times=0
        self.times_two=0
        self.fail_times=0
        self.i=0       
        self.run()

    def __del__(self):
        logger.info("HTTPRequest  times=================%d" %self.times)
        logger.info("HTTPResponse times=================%d" %self.times_two)
        logger.info("HTTP Fail    times=================%d " %self.fail_times)


    def run(self):
        '''
        we will start a thread to excute AsyncHTTPClient fetch url

        '''
        def download_url():
   
            try:
                if self.sche_queue.empty():
                    time.sleep(1)
                    self.i=self.i+1
                    if self.i>60:
                        print " download_url stop i= %d " %self.i
                        self.ioloop.stop()
                else:
                    element = self.sche_queue.get_nowait()
                    http_header   = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
             'Referer':"http://www.baidu.com/" }
                    http_request  = tornado.httpclient.HTTPRequest(url=element[0],method='GET',headers=http_header,
                                            use_gzip=True, request_timeout=60)
                    
                    self.http_client.fetch(http_request,callback = lambda response : self.insert_taskqueue(response,element[1]))
                    self.times=self.times+1
                    self.i=0

            except Exception as e:
                time.sleep(1)
                logger.exception(e)

        tornado.ioloop.PeriodicCallback(download_url, 100, io_loop=self.ioloop).start()
  
        try:
            # main thread will be block here
            self.ioloop.start()

        except KeyboardInterrupt:
            pass


    def insert_taskqueue(self,response,func):
        '''
        put url log to task_queue when success download
        put url log to failure_queue when fail download

        '''
        self.times_two=self.times_two+1

        if response.error:
            self.fail_times=self.fail_times+1
            logger.error(  "response.error: %s  url: %s"         %(response.error,response.effective_url))
            self.failure_queue.put(response.effective_url)
            record_failure("%s   url: %s    callback: %s \n" %(time.strftime(ISOTIMEFORMAT,time.localtime()),response.effective_url,func.__name__))

        else:
            element=(response.body,func,response.effective_url)
            logger.info("add element into taskqueue")
            self.task_queue.put(element)

    def loop_stop(self):
        self.ioloop.IOLoop.instance().stop()


