#!/usr/bin/env python
#coding=utf-8
import time
import logging
logger=logging.getLogger()
from bs4 import BeautifulSoup
from djangospider.utils.util import record_failure ,record_success
ISOTIMEFORMAT='%Y-%m-%d %X'

class Parse_Task():
	def __init__(self,task_queue,failure_queue,success_queue):
		self.task_queue=task_queue
		self.failure_queue=failure_queue
		self.success_queue=success_queue
		self.outputtime=0
		self.summary={}

		# wait for the first page be crawled
		#time.sleep(10)
		self.run()

	def __del__(self):
		for k,v in self.summary.iteritems():
			info="callback function  %s excute times =" %k,v
			logger.info(info)
		logger.info("task queue output %d"  %self.outputtime)

	def run(self):
		count=0
		while  True:
			try:
				if self.task_queue.empty():
					time.sleep(1)
					count=count+1
					if count>60:
						break

				else:
					element=self.task_queue.get_nowait()
					self.outputtime=self.outputtime+1
					count=0
					html=element[0]
					url=element[2]
					callback=element[1]
					
					if callback==None:
						logger.info("callback is none: can't find callback")
						continue
					try:
						callback(html,url)
						str_tmp="i have success parse %s" %url
						logger.info(str_tmp)
						self.success_queue.put("%s,%s" %(time.time(),url))
						record_success("%s   %s\n" %(time.strftime(ISOTIMEFORMAT,time.localtime()),url))
						if not self.summary.has_key(callback.__name__):
							self.summary[callback.__name__]=1
						else:
							self.summary[callback.__name__]=self.summary[callback.__name__]+1


					except Exception as e:
						logger.exception(e)
						self.failure_queue.put(url)
						logger.error(url)
						record_failure("%s   url: %s    callback: %s \n" %(time.strftime(ISOTIMEFORMAT,time.localtime()),url,callback.__name__))


			except Exception as e:
				time.sleep(1)
				logger.exception(e)

		logger.info("i ready to exit parse process")





