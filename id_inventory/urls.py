"""id_inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

admin.site.site_url = '/overview'
admin.site.site_header = _('IDMS Administration')
admin.site.site_title = _('IDMS Admin')
admin.site.index_title = _('IDMS Database')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^overview/', include('app_overview.urls', namespace='app_overview')),
    url(r'^printid/', include('app_print_id.urls', namespace='app_print_id')),
    url(r'^cards/', include('app_cards.urls', namespace='app_cards')),
    url(r'^forms/', include('app_id_form.urls', namespace='app_id_form')),
    url(r'^ribbons/', include('app_ribbons.urls', namespace='app_ribbons')),
    url(r'^report/', include('app_print_record.urls', namespace='app_print_record')),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', auth_views.login, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
