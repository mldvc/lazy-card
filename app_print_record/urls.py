from django.conf.urls import url
from . import views


app_name = 'app_print_record'

urlpatterns = [
    url(r'^$', views.report, name='report'),
    url(r'^record_report/$', views.recordReport, name='record_report'),
]
