
import urllib2
import logging
import logging.config

import threading
import time

logger= logging.getLogger()
from djangospider.utils.util import record_failure
ISOTIMEFORMAT='%Y-%m-%d %X'


class DownloadThread(threading.Thread):
	'''
	custom thread to download html

	'''
	def __init__(self, sche_queue,task_queue,failure_queue):

		super(DownloadThread, self).__init__()
		self.sche_queue = sche_queue
		self.task_queue=task_queue
		self.failure_queue=failure_queue

	def run(self):
		count=0
		while True:            
			try:
				if self.sche_queue.empty():
					time.sleep(1)
					count=count+1
					if count>60:
						break

				else:
					element = self.sche_queue.get_nowait()
					self.download_url(element[0],element[1])
					count=0

			except Exception as e:
				time.sleep(1)
				logger.exception(e)

		logger.info(" i have exit run downloadThread")

	def download_url(self, url,callback):
		# change it to a different way if you require
		try:
			
			req_header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
			 'Referer':"http://www.baidu.com/" 
			}
			req = urllib2.Request(url,None,req_header)

			response = urllib2.urlopen(req,timeout=60).read()
			element=(response,callback,url)

			logger.info("add element into taskqueue  :  %s"  %url)
			#print response
			self.task_queue.put(element)
		except Exception as e:
			logger.exception("%s  : %s"  %(e,url))
			self.failure_queue.put(url)
			record_failure("%s   url: %s    callback: %s \n" %(time.strftime(ISOTIMEFORMAT,time.localtime()),url,callback.__name__))
	



class Download_task():
	def __init__(self,sche_queue,task_queue,failure_queue):
		'''
		init three queue

		sche_queue : the start_url we need crawl
		task_queue : ready to store the html content and callback function when success crawl
		failure_queue :  ready to store the fail url when crawl url 


		'''  

		self.threads=[]
		self.task_queue=task_queue
		self.sche_queue=sche_queue
		self.failure_queue=failure_queue
		self.run_threads(4)
		

	def run_threads(self,i):
		
		for i in range(i):
			t=DownloadThread(self.sche_queue,self.task_queue,self.failure_queue)
			self.threads.append(t)
			t.daemon=True
			t.start()

	def join(self):
		threads_len=len(self.threads)
		logger.info(threads_len)
		while True:
			try:
				count=0			
				for item in self.threads:
					if  not item.isAlive():
						count=count+1
					else:
						break
				if count==threads_len:
					break

				time.sleep(1)
				#logger.warning("check check check")
			except KeyboardInterrupt:
				break
		logger.info("******exit Download_task******")



