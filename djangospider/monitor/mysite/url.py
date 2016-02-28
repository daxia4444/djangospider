from . import views 
from django.conf.urls import include, url

urlpatterns = [

    #those is my test ,not production
    url(r'^sysinfo/$', views.index),
    url(r'^info/sys/$', views.sysinfo),

]
