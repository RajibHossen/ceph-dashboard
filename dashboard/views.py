"""Django view file which work like controller in MVC pattern"""
#import pdb
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render
#from django.http import HttpResponseRedirect
#from django.contrib.auth import authenticate, login, logout
#from django.core.urlresolvers import reverse
#from django.shortcuts import redirect
#from django_auth_ldap.backend import LDAPBackend

# import os, sys
# lib_path = os.path.abspath(os.path.join('..', 'devopscephwrapper'))
# sys.path.append(lib_path)

from dashboard.devopscephwrapper.docephwrapper import CephWrapper
from dashboard.devopscephwrapper import cephserviceutility

API_WRAPPER = CephWrapper(endpoint='http://192.168.120.13:8090/api/v0.1/', debug=True)

# def login_user(request):
#     if request.method == "POST":
#         next_page = request.GET.get('next')
#         name = request.POST.get('username')
#         user_pass = request.POST.get('password')
#         user = authenticate(username=name,password=user_pass)
#         print user
#         if user is not None:
#             login(request,user)
#             if next_page:
#                 return HttpResponseRedirect(next_page)
#             else:
#                 print "redirecting to home"
#                 redirect_to = reverse("index")
#                 return HttpResponseRedirect(redirect_to)
#                 #return redirect('index')
#         else:
#            redirect_to = reverse("login")
#            return HttpResponseRedirect("/login")
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
    """application landing page, this function returns the main
    content"""
    template = loader.get_template('index.html')
    context = {
        'user':request.user
    }
    output = template.render(context, request)
    return HttpResponse(output)

def ajax_dashboard(request):
    """return dashboard content
    get status,report,pools,osd,mon metadata and osd performance from ceph
    cluster
    """
    _, status = API_WRAPPER.status(body='json')
    _, report = API_WRAPPER.report(body='json')
    _, pool_usage = API_WRAPPER.df(body='json')
    _, osd_metadata = API_WRAPPER.osd_metadata(body='json')
    _, mon_metadata = API_WRAPPER.mon_metadata(body='json')
    _, osd_performance = API_WRAPPER.osd_perf(body='json')

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
    output = template.render(context, request)
    return HttpResponse(output)

def section_status(request):
    """return ceph cluster status

    Dynamically call via ajax
    """
    _, status = API_WRAPPER.status(body='json')
    _, report = API_WRAPPER.report(body='json')

    context = {
        'cephstatus':status,
        'report':report
    }
    template = loader.get_template('pages/home/status_section.html')
    output = template.render(context, request)
    return HttpResponse(output)

def ceph_osd_tree(request):
    """return osd tree rendered page

    get data from cluster,format the data into tree structure
    """

    _, osd_tree = API_WRAPPER.osd_tree(body='json')

    osd_tree = cephserviceutility.build_tree_from_list(osd_tree)

    context = {
        'osd_tree':osd_tree
    }
    template = loader.get_template('pages/ceph_osd_tree.html')
    return HttpResponse(template.render(context, request))

def ceph_osd_utilization(request):
    _, osd_df = API_WRAPPER.osd_df(body='json')
    _, utilization = API_WRAPPER.osd_utilization(body='json')

    context = {
        'osd_df':osd_df,
        'osd_utilization':utilization
    }

    template = loader.get_template('pages/osd_utilization.html')
    return HttpResponse(template.render(context, request))

def ceph_osd_dump(request):
    _, osd_dump = API_WRAPPER.osd_dump(body='json')
    context = {
        'osd_dump':osd_dump
    }

    template = loader.get_template('pages/ceph_osd_dumps.html')
    return HttpResponse(template.render(context, request))


def ceph_osd_search(request):

    if request.method == "POST":
        osd_id = request.POST.get('osd_id')
        osd_id = int(osd_id)

        _, data = API_WRAPPER.osd_find(id=osd_id, body='json')
        _, metadata = API_WRAPPER.osd_metadata(id=osd_id, body='json')
        context = {
            'osd_searched':data,
            'osd_metadata':metadata
        }
        template = loader.get_template('pages/ceph_osd_search_result.html')
        return HttpResponse(template.render(context, request))
    else:
        _, osd_list = API_WRAPPER.osd_ls(body='json')
        context = {
            'osd_list':osd_list
        }

        template = loader.get_template('pages/ceph_osd_search.html')
        return HttpResponse(template.render(context, request))

def ceph_osd_path(request):

    _, metadata = API_WRAPPER.osd_metadata(body='json')

    context = {
        'osd_metadata':metadata
    }
    template = loader.get_template('pages/ceph_osd_path.html')
    return HttpResponse(template.render(context, request))

def ceph_osd_ips(request):
    _, metadata = API_WRAPPER.osd_metadata(body='json')

    context = {
        'osd_metadata':metadata
    }
    template = loader.get_template('pages/ceph_osd_ip.html')
    return HttpResponse(template.render(context, request))

def mon_health(request):
    _, health_status = API_WRAPPER.status(body='json')

    context = {
        'health':health_status
    }
    template = loader.get_template('pages/mon_health.html')

    return HttpResponse(template.render(context, request))

def mon_quorum(request):
    _, quorum = API_WRAPPER.quorum_status(body='json')

    context = {
        'quorum':quorum
    }
    template = loader.get_template('pages/mon_quorum.html')

    return HttpResponse(template.render(context, request))

def get_mon_metadata(request):
    _, metadata = API_WRAPPER.mon_metadata(body='json')

    context = {
        'metadata':metadata
    }
    template = loader.get_template('pages/mon_metadata.html')

    return HttpResponse(template.render(context, request))

def crush_profile(request):

    _, profile = API_WRAPPER.osd_crush_show_tunables(body='json')
    context = {
        'crush_profile':profile
    }
    template = loader.get_template('pages/crush_profile.html')
    return HttpResponse(template.render(context, request))

def crush_rules(request):
    _, rules = API_WRAPPER.osd_crush_rule_dump(body='json')
    context = {
        'crush_rules':rules
    }
    template = loader.get_template('pages/crush_rules.html')
    return HttpResponse(template.render(context, request))

def crush_buckets(request):
    _, dump = API_WRAPPER.osd_crush_dump(body='json')
    context = {
        'dump':dump
    }
    template = loader.get_template('pages/crush_buckets.html')
    return HttpResponse(template.render(context, request))

def crush_devices(request):
    _, dump = API_WRAPPER.osd_crush_dump(body='json')
    context = {
        'dump':dump
    }
    template = loader.get_template('pages/crush_devices.html')
    return HttpResponse(template.render(context, request))

def pg_stats(request):
    _, stats = API_WRAPPER.pg_stat(body='json')

    context = {
        'pg_stats':stats
    }
    template = loader.get_template('pages/pg_stats.html')
    return HttpResponse(template.render(context, request))

def pg_brief(request):
    _, stats = API_WRAPPER.pg_dump(dumpcontents='pgs_brief', body='json')

    context = {
        'pg_brief':stats
    }
    template = loader.get_template('pages/pg_brief.html')

    return HttpResponse(template.render(context, request))

def pg_summary(request):
    _, stats = API_WRAPPER.pg_dump(dumpcontents='summary', body='json')

    context = {
        'pg_summary':stats
    }
    template = loader.get_template('pages/pg_summary.html')

    return HttpResponse(template.render(context, request))

def pg_pool_summary(request):
    _, pool_summary = API_WRAPPER.pg_dump(dumpcontents='pools', body='json')

    context = {
        'pool_summary':pool_summary
    }
    template = loader.get_template('pages/pg_pool_summary.html')

    return HttpResponse(template.render(context, request))

def pg_dump_stuck(request):

    if request.method == "POST":
        stuck_value = request.POST.get('stuck_string')
        _, dump_stuck = API_WRAPPER.pg_dump_stuck(stuckops=stuck_value, body='json')

        context = {
            'dump_stuck':dump_stuck
        }
        template = loader.get_template('pages/pg_dump_stuck_result.html')
        return HttpResponse(template.render(context, request))
    else:

        context = {

        }

        template = loader.get_template('pages/pg_dump_stuck.html')
        return HttpResponse(template.render(context, request))

def pg_ls_by_pool(request):
    if request.method == "POST":
        stuck_value = request.POST.get('stuck')
        pool_id = request.POST.get('pool')

        stuck_value = stuck_value.strip()
        #pdb.set_trace()
        #return HttpResponse(pool_id)
        _, pg_pools = API_WRAPPER.pg_ls_by_pool(pool_id=pool_id, states=stuck_value, body='json')

        context = {
            'pg_pools':pg_pools
        }
        template = loader.get_template('pages/pg_ls_by_pool_result.html')
        return HttpResponse(template.render(context, request))

    else:
        _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')

        context = {
            'pool_data':pool_stats
        }

        template = loader.get_template('pages/pg_ls_by_pool.html')
        return HttpResponse(template.render(context, request))

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
        _, pg_pools = API_WRAPPER.pg_ls_by_osd(osd_id=osd_id, pool_id=pool_id,
                                               states=stuck_value, body='json')
        context = {
            'osd_pools':pg_pools
        }
        template = loader.get_template('pages/pg_ls_by_osd_result.html')
        return HttpResponse(template.render(context, request))

    else:
        _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')
        _, osd_ls = API_WRAPPER.osd_ls(body='json')

        context = {
            'pool_data':pool_stats,
            'osd_ls':osd_ls,
        }

        template = loader.get_template('pages/pg_ls_by_osd.html')
        return HttpResponse(template.render(context, request))

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
        _, pg_pools = API_WRAPPER.pg_ls_by_primary(osd_id=primary_osd_id,
                                                   pool_id=pool_id, states=stuck_value, body='json')

        context = {
            'osd_pools':pg_pools
        }
        template = loader.get_template('pages/pg_ls_by_primary_result.html')
        return HttpResponse(template.render(context, request))

    else:
        _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')
        _, osd_ls = API_WRAPPER.osd_ls(body='json')

        context = {
            'pool_data':pool_stats,
            'osd_ls':osd_ls,
        }

        template = loader.get_template('pages/pg_ls_by_primary.html')
        return HttpResponse(template.render(context, request))

def pool_basic_info(request):

    _, pool_info = API_WRAPPER.osd_pool_ls(detail='detail', body='json')

    context = {
        'pool_info':pool_info
    }

    template = loader.get_template('pages/pool_basic_info.html')
    return HttpResponse(template.render(context, request))


def pool_details(request):
    _, pool_info = API_WRAPPER.osd_pool_ls(detail='detail', body='json')

    context = {
        'pool_info':pool_info
    }

    template = loader.get_template('pages/pool_details.html')
    return HttpResponse(template.render(context, request))

def pool_parameters(request):

    if request.method == "POST":

        poolname = request.POST.get('pool')
        pool_var = request.POST.get('parameter')

        #pdb.set_trace()
        #return HttpResponse(pool_id)
        if not poolname or not pool_var:
            return HttpResponse("Pool and variable name is required")

        _, pools = API_WRAPPER.osd_pool_get(pool=poolname, var=pool_var, body='json')
        context = {
            'pool_parameters':pools
        }
        template = loader.get_template('pages/pool_parameters_result.html')
        return HttpResponse(template.render(context, request))


    else:
        _, pool_ls = API_WRAPPER.osd_pool_ls(body='json')

        context = {
            'pool_data':pool_ls,
        }

        template = loader.get_template('pages/pool_parameters.html')
        return HttpResponse(template.render(context, request))

def pool_rbps(request):
    _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_rbps.html')
    return HttpResponse(template.render(context, request))

def pool_wbps(request):
    _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_wbps.html')
    return HttpResponse(template.render(context, request))

def pool_rops(request):
    _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_rops.html')
    return HttpResponse(template.render(context, request))

def pool_wops(request):
    _, pool_stats = API_WRAPPER.osd_pool_stats(body='json')

    context = {
        'pool_stats':pool_stats
    }

    template = loader.get_template('pages/pool_wops.html')
    return HttpResponse(template.render(context, request))

def auth_user_list(request):
    _, user_list = API_WRAPPER.auth_list(body='json')

    context = {
        'user_list':user_list
    }
    template = loader.get_template('pages/auth_user_list.html')
    return HttpResponse(template.render(context, request))
