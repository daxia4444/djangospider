import chardet
import commands
import time



def getmemory():
	command1="top -b -n 1 | grep python | awk -F \" \" '{ print $6 }'"
	i=0
	(status, output) = commands.getstatusoutput(command1)
	b=output.split("\n")[-1]
	b=int(b)/1024
	print str(b)+":MB"
	time.sleep(1)


def record_failure(content):
	fp=open("fail.log","a")
	fp.write(content)
	fp.close()


def record_success(content):
	fp=open("success.log","a")
	fp.write(content)
	fp.close()

def debug_one(name,content):
	fp=open(name,"a")
	fp.write(content+"\n")
	fp.close()


def save_image(response,url):
	npos=url.rfind("/")
	name=url[npos+1:]
	with open(name,"w") as f:
		f.write(response)
