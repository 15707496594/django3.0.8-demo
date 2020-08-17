from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'v1/orders$', views.SaleOrderView.as_view()),
    url(r'v1/orders/(?P<pk>[0-9]+)$', views.SaleOrderView.as_view()),
    url(r'celery/test$', views.celery_test)
]
