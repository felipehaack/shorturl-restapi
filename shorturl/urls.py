from django.conf.urls import url
from shorturl import views

urlpatterns = [
    #GET
    url(r'^users/$', views.users_list),
    #POST
    url(r'^user/$', views.user_store),
    #GET/DELETE
    url(r'^user/:(?P<pk>[0-9]+)$', views.user_operations),
    #POST
    url(r'^users/:(?P<pk>[0-9]+)/urls$', views.url_operations),
    #DELETE/GET/REDIRECT
    url(r'^url/:(?P<pk>[0-9]+)$', views.url_operations),
    #REDIRECT
    url(r'^url/(?P<short>[0-9a-zA-Z]+)$', views.url_redirect_by_short_code),
    #GET
    url(r'^stats/:(?P<pk>[0-9]+)$', views.url_stats),
    #GET
    url(r'^user/:(?P<pk>[0-9]+)/stats$', views.user_stats),
    #GET
    url(r'^stats/$', views.global_stats),
]