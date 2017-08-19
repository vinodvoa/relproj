from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.static import static  # for pictures
from django.conf import settings  # for accessing settings
from relapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name='home'),
    url(r'^emeasearch/', views.emeasearch, name='emeasearch'),
    url(r'^emeasumm/', views.emeasumm, name='emeasumm'),
    url(r'^emeacard/(?P<oppm>[A-Z]-[0-9]+)/$', views.emeacard, name='emeacard'),
    url(r'^emeadtls/', views.emeadtls, name='emeadtls'),
    url(r'^emeaadd/', views.emeaadd, name='emeaadd'),
    url(r'^emeacal/', views.emeacal, name='emeacal'),
    url(r'^emeacontact/', views.emeacontact, name='emeacontact'),


    # url(r'^asiacard/(?P<oppm>[A-Z]-[0-9]+)/$', views.asiacard, name='asiacard'),
    # url(r'^asiadtls/', views.asiadtls, name='asiadtls'),
    # url(r'^asiaadd/', views.asiaadd, name='asiaadd'),
    #
    # url(r'^ctscard/(?P<oppm>[A-Z]-[0-9]+)/$', views.ctscard, name='ctscard'),
    # url(r'^ctsdtls/', views.ctsdtls, name='asiadtls'),
    # url(r'^ctsadd/', views.ctsadd, name='asiaadd'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
