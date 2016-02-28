from importlib import import_module
import os
import sys
import commands

class Command(object):

    def print_help(self):
      pass

    def run_from_argv(self,argv):
        try:
            path=os.path.split(os.path.realpath(__file__))[0]
            npos1=path.rfind("/")
            npos2=path.rfind("/",0,npos1)
            path=path[0:npos2]
            path=path+"/monitor"
            cmd=" cd  %s ; python manage.py runserver  0.0.0.0:8000  " %path
            (status, output) = commands.getstatusoutput(cmd)

        except KeyboardInterrupt:
            print "\n  you  click KeyboardInterrupt "
            sys.exit()
        except Exception as e:
            print e
            
        print output

