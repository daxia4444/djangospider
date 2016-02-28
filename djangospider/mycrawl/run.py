#!/usr/bin/env python
#coding=utf-8
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%H:%M:%S',)
logger= logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

fh=logging.FileHandler(os.path.join(os.getcwd(),"spider.log"))
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)
logger.addHandler(fh)


import sys
from crawler.thread_urllib import Download_task
from parse.parse_response import Parse_Task
from multiprocessing import Queue
import multiprocessing


from crawler.async_tornado import download_AsyncHTTPClient
from crawler.async_twisted import Twisted_download 


sche_queue=Queue(100)
task_queue=Queue(100)
failure_queue=Queue(100)
success_queue=Queue(100)




class Start():


	def __init__(self,ulr_parse,kind,sche_queue=sche_queue,task_queue=task_queue,failure_queue=failure_queue,success_queue=success_queue):
		'''
		init the spider data

		url_parse: the url list of you will crawl
		kind:  three download ways: 1 -> multhread 
									2 -> tornado async
									3 -> twisted async
		sche_queue: this queue will store ulr_address
		task_queue: when webpage be crawled, html content and callback function will store in this queue
		'''
		logger.info("i init Start class")
		self.sche_queue=sche_queue
		self.task_queue=task_queue
		self.failure_queue=failure_queue
		self.success_queue=success_queue
		self.ulr_parse=ulr_parse
		self.kind=kind
		for item in self.ulr_parse:
			self.sche_queue.put(item)
		self.run()

	def run(self):

		parse_process = multiprocessing.Process(target=Parse_Task,args=(self.task_queue,self.failure_queue,self.success_queue))
		parse_process.start()
		if self.kind ==1:
			download_task=Download_task(self.sche_queue,self.task_queue,self.failure_queue)
			download_task.join()
		elif self.kind==2:
			download_AsyncHTTPClient(self.sche_queue,self.task_queue,self.failure_queue)
		elif self.kind==3:
			Twisted_download(self.sche_queue,self.task_queue,self.failure_queue)
		else:
			logger.error("please define the kind of download ways")
		logger.info("would exit main process")

def _crawl(url,callback):
	'''
	crawl new url

	when we parse html content, 
	we can use _crawl to add new url to crawl
	'''
	
	element=(url,callback)
	logger.info("insert to  sche_queue :  %s" %url)
	sche_queue.put(element)






