
import urllib2
import logging
import logging.config

import threading
import time
from selenium import webdriver


logger= logging.getLogger()
from djangospider.util import record_failure
ISOTIMEFORMAT='%Y-%m-%d %X'


class Phantomjs_thread(threading.Thread):
	'''
	custom thread to download html

	'''
	def __init__(self, sche_queue,failure_queue):
		super(DownloadThread, self).__init__()
		self.sche_queue = sche_queue
		self.failure_queue=failure_queue

	def run(self):
		count=0
		while True:            
			try:
				element = self.sche_queue.get_nowait()
				self.download_url(element[0],element[1])
				count=0

			except Exception as e:
				#logger1.warning(e)	

				time.sleep(1)
				count=count+1
				if count>60:
					break
		logger.info(" i have exit run downloadThread")

	def download_url(self, url,callback):
	# change it to a different way if you require
		try:
			
			with closing(webdriver.PhantomJS()) as browser:
				browser.set_page_load_timeout(120)	
				browser.get(url)
				callback(browser)
				

		except Exception as e:
			logger.exception("%s  : %s"  %(e,url))
			record_failure("%s   url: %s    callback: %s \n" %(time.strftime(ISOTIMEFORMAT,time.localtime()),url,callback.__name__))
	



class phantomjs_task():
	def __init__(self,sche_queue,failure_queue):
		'''
		init queue

		sche_queue : the start_url we need crawl
		failure_queue :  ready to store the fail url when crawl url 


		'''  

		self.threads=[]
		self.sche_queue=sche_queue
		self.failure_queue=failure_queue
		self.run_threads(4)
		

	def run_threads(self,i):
		
		for i in range(i):
			t=Phantomjs_thread(self.sche_queue,self.failure_queue)
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

				time.sleep(2)
			except KeyboardInterrupt:
				break
		logger.info("******exit Download_task*********")



