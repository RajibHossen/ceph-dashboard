from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import csrf_token
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import pdb
# import os, sys
# lib_path = os.path.abspath(os.path.join('..', 'devopscephwrapper'))
# sys.path.append(lib_path)

from devopscephwrapper.docephwrapper import *
from devopscephwrapper import cephserviceutility


wrapper = CephWrapper(endpoint='http://192.168.120.13:8090/api/v0.1/',
                      debug = True)

# def login_user(request):
#     if request.method == "POST":
#         next_page = request.GET.get('next')
#         name = request.POST.get('username')
#         user_pass = request.POST.get('password')
#         print name,user_pass
#         user = authenticate(username=name,password=user_pass)
#         print str(request)
#         print user.is_active
#         if user is not None and user.is_active:
#             login(request,user)
#             print request.session.session_key
#             print str(request)
#             print str(user)

           
#             if next_page:
#                 return HttpResponseRedirect(next_page)
#             else:
#                 print "redirecting to home"
#                 redirect_to = reverse("index")
#                 return HttpResponseRedirect(redirect_to)
#                 #return redirect('index')
#         else:
#            redirect_to = reverse("login")
#            return HttpResponseRedirect("fasdas")
#     else:
#         template = loader.get_template('registration/login.html')
#         context = {
#         }
#         output = template.render(context,request)
#         return HttpResponse(output)

# def logout_user(request):
#     logout(request)
#     return HttpResponse("Logged out successfully")

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
    template = loader.get_template('pages/dashboard.html')
    output = template.render(context,request)
    return HttpResponse(output)

def section_status(request):
    response,status = wrapper.status(body='json')
    response,report = wrapper.report(body='json')

    context = {
        'cephstatus':status,
        'report':report
    }
    template = loader.get_template('pages/home/status_section.html')
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

def mon_health(request):
    response,health_status = wrapper.status(body='json')

    context = {
        'health':health_status
    }
    template = loader.get_template('pages/mon_health.html')

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

def crush_profile(request):

    response,profile = wrapper.osd_crush_show_tunables(body='json')
    context={
        'crush_profile':profile
    }
    template = loader.get_template('pages/crush_profile.html')
    return HttpResponse(template.render(context,request))

def crush_rules(request):
    response,rules = wrapper.osd_crush_rule_dump(body='json')
    context={
        'crush_rules':rules
    }
    template = loader.get_template('pages/crush_rules.html')
    return HttpResponse(template.render(context,request))

def crush_buckets(request):
    response,dump = wrapper.osd_crush_dump(body='json')
    context={
        'dump':dump
    }
    template = loader.get_template('pages/crush_buckets.html')
    return HttpResponse(template.render(context,request))

def crush_devices(request):
    response,dump = wrapper.osd_crush_dump(body='json')
    context={
        'dump':dump
    }
    template = loader.get_template('pages/crush_devices.html')
    return HttpResponse(template.render(context,request))

def pg_stats(request):
    response,stats = wrapper.pg_stat(body='json')

    context= {
        'pg_stats':stats
    }
    template = loader.get_template('pages/pg_stats.html')
    return HttpResponse(template.render(context,request))

def pg_brief(request):
    response,stats = wrapper.pg_dump(dumpcontents='pgs_brief',body='json')

    context = {
        'pg_brief':stats
    }
    template = loader.get_template('pages/pg_brief.html')

    return HttpResponse(template.render(context,request))

def pg_summary(request):
    response,stats = wrapper.pg_dump(dumpcontents='summary',body='json')

    context = {
        'pg_summary':stats
    }
    template = loader.get_template('pages/pg_summary.html')

    return HttpResponse(template.render(context,request))

def pg_pool_summary(request):
    response,pool_summary = wrapper.pg_dump(dumpcontents='pools',body='json')

    context ={
        'pool_summary':pool_summary
    }
    template = loader.get_template('pages/pg_pool_summary.html')

    return HttpResponse(template.render(context,request))

def pg_dump_stuck(request):

    if request.method == "POST":
        stuck_value = request.POST.get('stuck_string')
        response,dump_stuck = wrapper.pg_dump_stuck(stuckops=stuck_value,body='json')
        
        context = {
            'dump_stuck':dump_stuck
        }
        template = loader.get_template('pages/pg_dump_stuck_result.html')
        return HttpResponse(template.render(context,request))
    else:

        context = {

        }

        template = loader.get_template('pages/pg_dump_stuck.html')
        return HttpResponse(template.render(context,request))

def pg_ls_by_pool(request):
    if request.method == "POST":
        stuck_value = request.POST.get('stuck')
        pool_id = request.POST.get('pool')

        stuck_value = stuck_value.strip()
        #pdb.set_trace()
        #return HttpResponse(pool_id)
        
        response,pg_pools = wrapper.pg_ls_by_pool(pool_id=pool_id,states=stuck_value,body='json')
        
        context = {
            'pg_pools':pg_pools
        }
        template = loader.get_template('pages/pg_ls_by_pool_result.html')
        return HttpResponse(template.render(context,request))

    else:
        response,pool_stats = wrapper.osd_pool_stats(body='json')

        context = {
            'pool_data':pool_stats
        }

        template = loader.get_template('pages/pg_ls_by_pool.html')
        return HttpResponse(template.render(context,request))

def pg_ls_by_osd(request):

    if request.method == "POST":
        osd_id = request.POST.get('osd')
        stuck_value = request.POST.get('stuck')
        pool_id = request.POST.get('pool')

        stuck_value = stuck_value.strip()
        #pdb.set_trace()
        #return HttpResponse(pool_id)
        if not osd_id:
            return HttpResponse("OSD ID is required")
        
        response,pg_pools = wrapper.pg_ls_by_osd(osd_id=osd_id,pool_id=pool_id,states=stuck_value,body='json')
        
        context = {
            'osd_pools':pg_pools
        }
        template = loader.get_template('pages/pg_ls_by_osd_result.html')
        return HttpResponse(template.render(context,request))

    else:
        response,pool_stats = wrapper.osd_pool_stats(body='json')
        response,osd_ls = wrapper.osd_ls(body='json')

        context = {
            'pool_data':pool_stats,
            'osd_ls':osd_ls,
        }

        template = loader.get_template('pages/pg_ls_by_osd.html')
        return HttpResponse(template.render(context,request))

def pg_ls_by_primary(request):
    if request.method == "POST":
        primary_osd_id = request.POST.get('primary_osd')
        stuck_value = request.POST.get('stuck')
        pool_id = request.POST.get('pool')

        stuck_value = stuck_value.strip()
        #pdb.set_trace()
        #return HttpResponse(pool_id)
        if not primary_osd_id:
            return HttpResponse("OSD ID is required")
        
        response,pg_pools = wrapper.pg_ls_by_primary(osd_id=primary_osd_id,pool_id=pool_id,states=stuck_value,body='json')
        
        context = {
            'osd_pools':pg_pools
        }
        template = loader.get_template('pages/pg_ls_by_primary_result.html')
        return HttpResponse(template.render(context,request))

    else:
        response,pool_stats = wrapper.osd_pool_stats(body='json')
        response,osd_ls = wrapper.osd_ls(body='json')

        context = {
            'pool_data':pool_stats,
            'osd_ls':osd_ls,
        }

        template = loader.get_template('pages/pg_ls_by_primary.html')
        return HttpResponse(template.render(context,request))

def pool_basic_info(request):

    response,pool_info = wrapper.osd_pool_ls(detail='detail',body='json')

    context = {
        'pool_info':pool_info
    }

    template = loader.get_template('pages/pool_basic_info.html')
    return HttpResponse(template.render(context,request))


def pool_details(request):
    response,pool_info = wrapper.osd_pool_ls(detail='detail',body='json')

    context = {
        'pool_info':pool_info
    }

    template = loader.get_template('pages/pool_details.html')
    return HttpResponse(template.render(context,request))

def pool_parameters(request):

    if request.method == "POST":
        
        poolname = request.POST.get('pool')
        pool_var = request.POST.get('parameter')
        
        #pdb.set_trace()
        #return HttpResponse(pool_id)
        if not poolname or not pool_var:
            return HttpResponse("Pool and variable name is required")
        
        response,pools = wrapper.osd_pool_get(pool=poolname,var=pool_var,body='json')
        
        context = {
            'pool_parameters':pools
        }
        template = loader.get_template('pages/pool_parameters_result.html')
        return HttpResponse(template.render(context,request))


    else:
        response,pool_ls = wrapper.osd_pool_ls(body='json')

        context = {
            'pool_data':pool_ls,
        }

        template = loader.get_template('pages/pool_parameters.html')
        return HttpResponse(template.render(context,request))

def pool_rbps(request):
    response,pool_stats = wrapper.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_rbps.html')
    return HttpResponse(template.render(context,request))
def pool_wbps(request):
    response,pool_stats = wrapper.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_wbps.html')
    return HttpResponse(template.render(context,request))
def pool_rops(request):
    response,pool_stats = wrapper.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_rops.html')
    return HttpResponse(template.render(context,request))
def pool_wops(request):
    response,pool_stats = wrapper.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_wops.html')
    return HttpResponse(template.render(context,request))


def auth_user_list(request):
    response,user_list = wrapper.auth_list(body='json')

    context = {
        'user_list':user_list
    }
    template = loader.get_template('pages/auth_user_list.html')
    return HttpResponse(template.render(context,request))

# def login_user(request):
#     next_page = request.GET.get('next')
#     name = request.POST.get('username')
#     user_pass = request.POST.get('password')

#     user = authenticate(username=name,password=user_pass)
#     if user is not None:
#        login(request,user)
#        return HttpResponseRedirect(next_page)
#     else:
#        redirect_to = reverse("login")
#        return HttpResponseRedirect("fasdas")


