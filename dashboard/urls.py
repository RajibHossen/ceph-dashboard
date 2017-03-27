from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^dashboard/home/$',views.ajax_dashboard,name='ajax_dashboard'),
    url(r'^dashboard/home/section_status/$',views.section_status,name='section_status'),
    url(r'^osd/tree/$',views.ceph_osd_tree,name='ceph_osd_tree'),
    url(r'^osd/utilization/$',views.ceph_osd_utilization,name='ceph_osd_utilization'),
    url(r'^osd/dumps/$',views.ceph_osd_dump,name='ceph_osd_dumps'),
    url(r'^osd/search/$',views.ceph_osd_search,name='ceph_osd_search'),
    url(r'^osd/dir/$',views.ceph_osd_path,name='ceph_osd_path'),
    url(r'^osd/ip/$',views.ceph_osd_ips,name='ceph_osd_ips'),
    url(r'^mon/quorum/$',views.mon_quorum,name='mon_quorum'),
    url(r'^mon/metadata/$',views.mon_metadata,name='mon_metadata'),
    url(r'^mon/health/$',views.mon_health,name='mon_health'),
    url(r'^osd/crush/profiles/$',views.crush_profile,name='crush_profile'),
    url(r'^osd/crush/rules/$',views.crush_rules,name='crush_rules'),
    url(r'^osd/crush/buckets/$',views.crush_buckets,name='crush_buckets'),
    url(r'^osd/crush/devices/$',views.crush_devices,name='crush_devices'),
    url(r'^pg/stats/$',views.pg_stats,name='pg_stats'),
    url(r'^pg/brief/$',views.pg_brief,name='pg_brief'),
    url(r'^pg/summary/$',views.pg_summary,name='pg_summary'),
    url(r'^pg/pools/$',views.pg_pool_summary,name='pg_pool_summary'),
    url(r'^pg/dump/stuck/$',views.pg_dump_stuck,name='pg_dump_stuck'),
    url(r'^pg/ls/by/pools/$',views.pg_ls_by_pool,name='pg_ls_by_pool'),
    url(r'^pg/ls/by/osd/$',views.pg_ls_by_osd,name='pg_ls_by_osd'),
    url(r'^pg/ls/by/primary/$',views.pg_ls_by_primary,name='pg_ls_by_primary'),
    url(r'^pool/basic/info/$',views.pool_basic_info,name='pool_basic_info'),
    url(r'^pool/details/$',views.pool_details,name='pool_details'),
    url(r'^pool/parameters/$',views.pool_parameters,name='pool_parameters'),
    url(r'^pool/read/bps/$',views.pool_rbps,name='pool_rbps'),
    url(r'^pool/write/bps/$',views.pool_wbps,name='pool_wbps'),
    url(r'^pool/read/ops/$',views.pool_rops,name='pool_rops'),
    url(r'^pool/write/ops/$',views.pool_wops,name='pool_wops'),
    url(r'^auth/list/$',views.auth_user_list,name='auth_list'),
    
]
