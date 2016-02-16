from django.conf.urls import url
from encurtar import views

urlpatterns = [
#	url(r'^url/:(?P<pk>[0-9]+)/$', views.encutar_remove_or_redirect),
	url(r'^user/$', views.user_list),
#    url(r'^:(?P<pk>[0-9]+)/urls/$', views.encutar_store_url),
    url(r'^user/:(?P<pk>[0-9]+)$', views.user_operations),
#    url(r'^stats/$', views.encutar_global_statistics),
#    url(r'^:(?P<pk>[0-9]+)/stats/$', views.encurtar_user_statistics),
#    url(r'^stats/:(?P<pk>[0-9]+)/$', views.encurtar_url_statistics),
]