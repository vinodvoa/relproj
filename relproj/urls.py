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
    url(r'^emeaadde0/', views.emeaadde0, name='emeaadde0'),
    url(r'^emeaadde1/', views.emeaadde1, name='emeaadde1'),
    url(r'^emeaeditprj/', views.emeaeditprj, name='emeaeditprj'),
    url(r'^emeaedite0/', views.emeaadde0, name='emeaedite0'),
    url(r'^emeaedite1/', views.emeaadde1, name='emeaedite1'),
    url(r'^emeacal/', views.emeacal, name='emeacal'),
    url(r'^emeacaladd/', views.emeacaladd, name='emeacaladd'),
    url(r'^emeacontact/', views.emeacontact, name='emeacontact'),
]
