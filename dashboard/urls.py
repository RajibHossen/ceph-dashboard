from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^dashboard/home/$',views.ajax_dashboard,name='ajax_dashboard'),
    url(r'^osd/tree/$',views.ceph_osd_tree,name='ceph_osd_tree'),
    url(r'^osd/utilization/$',views.ceph_osd_utilization,name='ceph_osd_utilization'),
    url(r'^osd/dumps/$',views.ceph_osd_dump,name='ceph_osd_dumps'),
    url(r'^osd/search/$',views.ceph_osd_search,name='ceph_osd_search'),
    url(r'^osd/dir/$',views.ceph_osd_path,name='ceph_osd_path'),
    url(r'^osd/ip/$',views.ceph_osd_ips,name='ceph_osd_ips'),
    url(r'^mon/quorum/$',views.mon_quorum,name='mon_quorum'),
    url(r'^mon/metadata/$',views.mon_metadata,name='mon_metadata')
]
