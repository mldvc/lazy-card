from django.conf.urls import url
from . import views

app_name = 'app_ribbon_inventory'

urlpatterns = [
    url(r'^$', views.ribbonStockMgr, name="stocks"),
    url(r'^add_new_stock/$', views.addNewStock, name="add_new_stock"),
    url(r'^(?P<pk>[0-9]+)/$', views.updateStock, name='update_stock'),
]
