from django.conf.urls import url
from demo import views


urlpatterns = [
    url(r'^demos/$', views.demo_list),
    url(r'^demos/(?P<pk>[0-9]+)/$', views.demo_detail),
]
