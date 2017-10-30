from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^snacks/(?P<pk>\d+)', views.details),
    url(r'^sorted/', views.sort),
    url(r'^login/', views.validate_user),
    url(r'^create_snack/', views.create_snack),
]