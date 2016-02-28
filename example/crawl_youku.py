#coding=utf-8

from bs4 import BeautifulSoup
from djangospider.utils.util import debug_one
from djangospider.mycrawl.run import Start ,_crawl
import os
import logging
import time



logger= logging.getLogger()
logger.setLevel(logging.INFO)
ISOTIMEFORMAT='%Y-%m-%d %X'



def parse_youku(response,url):	
	soup=BeautifulSoup(response)
	nav=soup.find('div',attrs={"class":"cata_variety"})
	now_quarter=""
	a_list=nav.findAll("a",attrs={"href":True})

	for item in a_list:
		if (str(item).find("java") <0):
			url="http://www.soku.com" + item['href']
			_crawl(url,youku2)
			



def youku2(response,url):
	try:
		logger.warning(" i come into youku2")
		logger.warning("%d   souku :  %s" %(len(response),url) )
		soup=BeautifulSoup(response)
		div=soup.find("div",attrs={"class":"s_detail"})
		li=div.find("li",attrs={"data-type":"linkMore"})
		href=li.find("a")["href"]
		_crawl(href,youku3)
	except Exception as e:
		logger.exception(e)


def youku3(response,url):

	soup=BeautifulSoup(response)
	npos1=url.find("id_")
	tvid=url[npos1:]
	logger.info(tvid)

	str2="%s   %s"  %(time.strftime(ISOTIMEFORMAT,time.localtime()),url)	
	soup=BeautifulSoup(response)
	try:
		lis=soup.find("ul",attrs={"id":"zySeriesTab"}).findAll("li")
	except Exception as e:
		logger.exception(e)



	for li in lis:
		str1=li.find("a")["onclick"]
		npos1=str1.find("('")
		npos2=str1.find("')")	
		tvdate=str1[npos1+2:npos2]
		newurl="http://www.youku.com/show_episode/"+tvid+"?dt=json&divid="+tvdate +"&__rt=1&__ro=" +tvdate

		str2="%s   %s"  %(time.strftime(ISOTIMEFORMAT,time.localtime()),newurl)		
		logger.info(newurl)
		_crawl(newurl,youku4)



def youku4(response,url):
	logger.info("i come into youku4")



if __name__ == '__main__':

	try:
		start_urls=[('http://www.soku.com/search_video/q_今晚80后脱口秀',parse_youku),]
		Start(start_urls,2)
	except  Exception as e:
		logger.exception(e)





