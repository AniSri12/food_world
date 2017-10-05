from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^users/create', views.createUser, name = "create_user"),
    url(r'^snacks/create', views.createSnack, name = "create_snack"),
    url(r'^carts/create', views.createCart, name = "create_cart"),
    url(r'^wishlists/create', views.createWishlist, name = "create_wishlist"),
    url(r'^users/destroy/(?P<pk>\d+)', views.destroyUser),
    url(r'^snacks/destroy/(?P<pk>\d+)', views.destroySnack),
    url(r'^carts/destroy/(?P<pk>\d+)', views.destroyCart),
    url(r'^wishlists/destroy/(?P<pk>\d+)', views.destroyWishlist),
    url(r'^users/update/(?P<pk>\d+)', views.updateUser),
    url(r'^snacks/update/(?P<pk>\d+)', views.updateSnack),
    url(r'^carts/update/(?P<pk>\d+)', views.updateCart),
    url(r'^wishlists/update/(?P<pk>\d+)', views.updateWishlist),
    url(r'^snacks/', views.get_all_snacks, name = "get_all_snacks"),
    url(r'^users/', views.get_all_users, name = "get_all_users"),
    url(r'^users/(?P<pk>\d+)', views.getUsers, name = "get_user"),
    url(r'^snacks/(?P<pk>\d+)', views.getSnacks, name = "get_snacks"),
    

]