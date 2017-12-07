from django.conf.urls import url, include
from . import views

app_name = 'app_cards'

urlpatterns = [
    url(r'^$', views.cards, name='cards'),
    url(r'^stocks/', include('app_card_inventory.urls', namespace='app_card_inventory')),
    url(r'^reports/', include('app_print_record.urls', namespace='app_print_record')),
    url(r'^add_print_history/$', views.add_print_history, name='add_print_history'),
    url(r'^(?P<pk>[0-9]+)/$', views.update_print_history, name='update_print_history'),
    url(r'^add_print_history/(?P<pk>[0-9]+)/$', views.add_print_history, name='add_print_history_from_form'),
]
