from django.conf.urls import url
from . import views

app_name = 'app_overview'

urlpatterns = [
    url(r'^$', views.overview, name='overview'),
    url(r'^api/chart/data/total/$', views.get_total_data, name='get_total_data'),
]
