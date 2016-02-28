import commands
import os
import sys
import subprocess

def Run_Django():
	print "i come into Run_Django"
	path=os.path.split(os.path.realpath(__file__))[0] 
	command1=" cd  %s ; python manage.py runserver " %path
	(status, output) = commands.getstatusoutput(command1)
	print "Run_Django status is %s"  %status
	print output


if __name__ == '__main__':
	try:
		path=os.path.split(os.path.realpath(__file__))[0] 
		command1=" cd  %s ; python manage.py runserver " %path
		(status, output) = commands.getstatusoutput(command1)

	except KeyboardInterrupt:
		print "KeyboardInterrupt happen"
		sys.exit()
	except Exception as e:
		print e

	print output