from django.conf.urls import url, include
from . import views


app_name = 'app_ribbons'

urlpatterns = [
    url(r'^$', views.ribbons, name='ribbons'),
    url(r'^add_ribbon_usage_history/$', views.addRibbonUsageHistory, name='add_ribbon_usage_history'),
    url(r'^(?P<ribbon_number>[0-9]+)/$', views.updateRibbonUsageHistory, name='update_ribbon_usage_history'),
    url(r'^stocks/', include('app_ribbon_inventory.urls', namespace='app_ribbon_inventory')),
]
