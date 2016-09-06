from django.conf.urls import url
from django.http import HttpResponseRedirect

from . import views

app_name = 'work'
urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('projects/work_orders')),
    url(r'^projects/(?P<pk>[0-9]+)/pdf/$', views.PrintPdfView, name="project_pdf"),
    url(r'^projects/complete$', views.ProjectIndexView, {'status': 'CO'}, name='complete_index'), 
    url(r'^projects/work_orders$', views.ProjectIndexView, {'status': 'WO'}, name='work_order_index'), 
    url(r'^projects/quotes$', views.ProjectIndexView, {'status': 'QT'}, name='quote_index'), 
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetailView, name='project_detail'),
    url(r'^projects/create/$', views.ProjectCreateView, name='project_create'),
    url(r'^projects/(?P<pk>[0-9]+)/update/$', views.ProjectUpdateView, name='project_update'),
    url(r'^projects/(?P<pk>[0-9]+)/delete/$', views.ProjectDeleteView, name='project_delete'),
    url(r'^clients/$', views.ClientIndex, name='client_index'),
    url(r'^clients/(?P<pk>[0-9]+)/$', views.ClientDetailView, name='clients_detail'),
    url(r'^clients/create/$', views.ClientCreateView, name='client_create'),
    url(r'^clients/(?P<pk>[0-9]+)/update/$', views.ClientUpdateView, name='clients_update'),
    url(r'^clients/(?P<pk>[0-9]+)/delete/$', views.ClientDeleteView, name='clients_delete'),
    url(r'^reports/$', views.ReportView, name='report_view'),

]