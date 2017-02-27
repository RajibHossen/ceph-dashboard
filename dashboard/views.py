from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from cephclient.wrapper import *

wrapper = CephWrapper(endpoint='http://192.168.120.13:8090/api/v0.1/',
                      debug = True)



@login_required
def index(request):
    template = loader.get_template('index.html')
    data = wrapper.health(body='json')
    context = {
        'user':request.user,
        'data':data
    }
    output = template.render(context,request)
    return HttpResponse(output)

def ajax_dashboard(request):
    response,status = wrapper.status(body='json')
    response,report = wrapper.report(body='json')
    template = loader.get_template('dynamic/dashboard.html')
    context = {
        'cephstatus':status,
        'report':report
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


