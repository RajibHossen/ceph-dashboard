from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# import os, sys
# lib_path = os.path.abspath(os.path.join('..', 'devopscephwrapper'))
# sys.path.append(lib_path)

from devopscephwrapper.docephwrapper import *
from devopscephwrapper import cephserviceutility


wrapper = CephWrapper(endpoint='http://192.168.120.13:8090/api/v0.1/',
                      debug = True)



@login_required
def index(request):
    template = loader.get_template('index.html')
    context = {
        'user':request.user
    }
    output = template.render(context,request)
    return HttpResponse(output)

def ajax_dashboard(request):
    response,status = wrapper.status(body='json')
    response,report = wrapper.report(body='json')
    response, pool_usage = wrapper.df(body='json')
    response,osd_metadata = wrapper.osd_metadata(body='json')
    reponse,mon_metadata = wrapper.mon_metadata(body='json')
    response,osd_performance = wrapper.osd_perf(body='json')

    template = loader.get_template('dynamic/dashboard.html')

    osd_metadata = cephserviceutility.format_json(osd_metadata)
    mon_metadata = cephserviceutility.format_json(mon_metadata)
    osd_performance = cephserviceutility.data_format_for_bar_chart(osd_performance)
    context = {
        'cephstatus':status,
        'report':report,
        'pool_usage':pool_usage,
        'osd_metadata':osd_metadata,
        'mon_metadata':mon_metadata,
        'osd_perf':osd_performance
    }
    output = template.render(context,request)
    return HttpResponse(output)


#def login_user(request):
#    username = request.POST['username']
#    password = request.POST['password']
#
#    user = authenticate(username=username,password=password)
#    if user in not None:
#        login(request,user)
#        redirect_to = reverse("home")
#        return HttpResponseRedirect(redirect_to)
#    else:
#        redirect_to = reverse("login")
#        return HttpResponseRedirect(redirect_to)


