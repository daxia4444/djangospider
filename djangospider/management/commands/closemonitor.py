import commands
from importlib import import_module

class Command(object):

	def print_help(self):
		pass


	def run_from_argv(self,argv):

		cmd=" sudo netstat -anp | grep 8000 | grep python | awk '{ print $7   }' | sed -n '1,2p'"
		(status, output) = commands.getstatusoutput(cmd)
		if output.find('python'):
			npos=output.rfind('/')
			output=output[:npos]
			cmd= "kill -9 %s" %output
			(status, output) = commands.getstatusoutput(cmd)
			print output
