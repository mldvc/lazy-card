from django.conf.urls import url
from . import views

app_name = 'app_print_id'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.printID, name="print-preview"),
    # url(r'^ajax/get_layout/$', views.getLayout, name='get_layout'),
]
