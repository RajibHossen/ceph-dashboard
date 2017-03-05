from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import csrf_token

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

    template = loader.get_template('pages/dashboard.html')

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

def ceph_osd_tree(request):

    response,osd_tree = wrapper.osd_tree(body='json')

    osd_tree = cephserviceutility.build_tree_from_list(osd_tree)

    context = {
        'osd_tree':osd_tree
    }
    template = loader.get_template('pages/ceph_osd_tree.html')
    return HttpResponse(template.render(context,request))

def ceph_osd_utilization(request):
   
    response,osd_df = wrapper.osd_df(body='json')    
    response,utilization = wrapper.osd_utilization(body='json')

    context = {
        'osd_df':osd_df,
        'osd_utilization':utilization
    }

    template = loader.get_template('pages/osd_utilization.html')
    return HttpResponse(template.render(context,request))

def ceph_osd_dump(request):
    
    response,osd_dump = wrapper.osd_dump(body='json')

    context = {
        'osd_dump':osd_dump
    }

    template = loader.get_template('pages/ceph_osd_dumps.html')
    return HttpResponse(template.render(context,request))


def ceph_osd_search(request):

    if request.method == "POST":
        osd_id = request.POST.get('osd_id')
        osd_id = int(osd_id)
        
        response,data = wrapper.osd_find(id=osd_id,body='json')
        response,metadata = wrapper.osd_metadata(id=osd_id,body='json')
        context = {
            'osd_searched':data,
            'osd_metadata':metadata
        }
        template = loader.get_template('pages/ceph_osd_search_result.html')
        return HttpResponse(template.render(context,request))
    else:
        response,osd_list = wrapper.osd_ls(body='json')
        context = {
            'osd_list':osd_list
        }

        template = loader.get_template('pages/ceph_osd_search.html')
        return HttpResponse(template.render(context,request))

def ceph_osd_path(request):

    response,metadata = wrapper.osd_metadata(body='json')

    context = {
        'osd_metadata':metadata
    }
    template = loader.get_template('pages/ceph_osd_path.html')
    return HttpResponse(template.render(context,request))
def ceph_osd_ips(request):
    response,metadata = wrapper.osd_metadata(body='json')

    context = {
        'osd_metadata':metadata
    }
    template = loader.get_template('pages/ceph_osd_ip.html')
    return HttpResponse(template.render(context,request))


def mon_quorum(request):
    response,quorum = wrapper.quorum_status(body='json')

    context={
        'quorum':quorum
    }
    template = loader.get_template('pages/mon_quorum.html')

    return HttpResponse(template.render(context,request))

def mon_metadata(request):
    response,metadata = wrapper.mon_metadata(body='json')

    context={
        'metadata':metadata
    }
    template = loader.get_template('pages/mon_metadata.html')

    return HttpResponse(template.render(context,request))

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


