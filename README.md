
#  djangospider

	djangospider is light web crawling framework, it have a few code, but
	can do high speed crawling, it support three modes to crawl: multithreading,
	tornado IOloop, and twisted reactor.you can understand to how to use
	async crawler easily.

## Requirement:

	Python2.7
	Works on Linux



## Install:
	you can download the zip package in github. then unpack the zip package,
	find the path of setup.py, Execute the command: 
*	`$sudo python setup.py install`

	or you can use pip:
*	`$sudo pip install djangospider`



## The entry function: Start(start_urls,mode)

	start_urls parameter: is a list, and it's element is tuple:

		the first of the tuple is url which you will crawl,
		the second of the tuple is the callback for url.

	the mode parameter: the crawler's way, it has three types:

		if mode is int 1 : multithreading ways
		if mode is int 2 : tornado  async ways
		if mode is int 3 : twisted  async ways


## For example:

	from djangospider.mycrawl.run import Start ,_crawl

	def callback(response,url):
		print "get the %s" %url
	
	if __name__ == '__main__':
		try:
			start_urls=[('http://github.com/',callback),]
			Start(start_urls,2)
		except  Exception as e:
			logger.exception(e)

	
## System monitor

	you can monitor the memory ,cpu and network in broswer

*	`$djangospider runmonitor`
*	visit `http://127.0.0.1:8000/index/sysinfo/`


![](https://github.com/daxia4444/djangospider/blob/master/doc/djangospider.jpg)
