from django.shortcuts import render
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json
# Create your views here.



def index(request):
    return render_to_response("sys.html")




def sysinfo(request):
    print " i come into info sysinfo"

    mem_usage=get_mem()
    net_usage=get_netstat("eth0") 
    cpu_usage=get_cpu_usage()
    info={"mem_usage":mem_usage,"net_usage":net_usage,"cpu_usage":cpu_usage}

    data = json.dumps(info)     
    response=HttpResponse(data)
    response['Content-Type'] = "text/javascript"
    return response

def infonet(request):
    net_state=get_netstat("eth0")
    print net_state
    return HttpResponse(net_state)



def index(request):
    return render_to_response("sys.html")


def get_mem():
    """
    Get memory usage
    """
    mem_usage={}
    try:
        pipe = os.popen(
            "free -tmo | " + "grep 'Mem' | " + "awk '{print $2,$4,$6,$7}'")
        data = pipe.read().strip().split()
        pipe.close()

        allmem = int(data[0])
        freemem = int(data[1])
        buffers = int(data[2])
        cachedmem = int(data[3])

        # Memory in buffers + cached is actually available, so we count it
        # as free. See http://www.linuxatemyram.com/ for details
        freemem += buffers + cachedmem

        percent = (100 - ((freemem * 100) / allmem))
        usage = (allmem - freemem)

        mem_usage = {'usage': usage, 'buffers': buffers, 'cached': cachedmem, 'free': freemem, 'percent': percent}

    except Exception as err:
        pass
    return mem_usage



def get_cpu_usage():
    """
    Get the CPU usage and running processes
    """
    cpu_usage={}
    try:

        pipe = os.popen("  top -bn 1 | awk '{ print $9  }' | tail -n+8 | awk '{s+=$1 } END {print s}' ")
        data = pipe.read()
        pipe.close()
        cpu_usage={"cpu_usage":data}
    except Exception as err:
        pass

    return cpu_usage



def get_netstat(interface):
    """
    Get ports and applications
    """


    net_usage={}
    try:
        pipe = os.popen("cat /proc/net/dev |" + "grep " + interface + "| awk '{print $2, $10}'")
        data = pipe.read().split()
        print data

        pipe.close()

        traffic_in = int(data[0])
        traffic_out = int(data[1])
        net_usage={"traffic_in":traffic_in,"traffic_out":traffic_out}

    except Exception as err:
        pass
        
    return net_usage