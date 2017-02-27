from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^ajax/dashboard/$',views.ajax_dashboard,name='ajax_dashboard'),
]
