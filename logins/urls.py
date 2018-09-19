from django.conf.urls import url

from logins import views  # or: from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^byLogin/$', views.byLogin),
    url(r'byLogin/(?P<login>[\w ]+)/?$', views.byLogin),
    url(r'^byIP/$', views.byIP),
    url(r'byIP/(?P<ip>[\w\.: ]+)/?$', views.byIP),
]
 
