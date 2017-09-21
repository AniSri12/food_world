from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^users/(?P<pk>\d+)', views.getUsers),
    url(r'^snacks/(?P<pk>\d+)', views.getSnacks),
    url(r'^carts/(?P<pk>\d+)', views.getCarts),
    url(r'^wishlists/(?P<pk>\d+)', views.getWishlists),
    url(r'^users/create', views.createUser),
    url(r'^snacks/create', views.createSnack),
    url(r'^carts/create', views.createCart),
    url(r'^wishlists/create', views.createWishlist),
]