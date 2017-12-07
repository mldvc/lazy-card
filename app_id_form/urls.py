from django.conf.urls import url
from . import views

app_name = 'app_id_form'

urlpatterns = [
    url(r'^$', views.formView, name="forms"),
    url(r'^select_form_type/$', views.selectForm, name="select_form_type"),
    url(r'^select_form_type/add_form/(?P<pk>[0-9]+)/$', views.addForm, name="add_form"),
    url(r'^(?P<pk>[0-9]+)/$', views.updateIDForm, name='update_id_form'),
    url(r'^view_form/(?P<pk>[0-9]+)/$', views.viewIDForm, name='view_id_form'),
    url(r'^(?P<pk>[0-9]+)/(?P<obj>[0-9]+)/$', views.updateIDForm, name='update_form'),
    url(r'^ajax/filter_field/$', views.filterField, name='filter_field'),
]
