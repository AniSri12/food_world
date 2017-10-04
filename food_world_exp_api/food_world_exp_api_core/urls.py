from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^snacks/(?P<pk>\d+)', views.details),
]