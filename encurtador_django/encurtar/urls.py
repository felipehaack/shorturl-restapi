from django.conf.urls import url
from encurtar import views

urlpatterns = [
    url(r'^users/$', views.users_list),
	url(r'^user/$', views.user_list),
    url(r'^user/:(?P<pk>[0-9]+)$', views.user_operation),
    url(r'^users/:(?P<pk>[0-9]+)/urls$', views.url_operation),
    url(r'^stats/:(?P<pk>[0-9]+)$', views.url_stats),
    url(r'^url/:(?P<pk>[0-9]+)$', views.url_operation),
    url(r'^url/(?P<short>[0-9a-zA-Z]+)$', views.url_short),
    url(r'^user/:(?P<pk>[0-9]+)/stats$', views.user_stats),
    url(r'^stats/$', views.global_stats),
]