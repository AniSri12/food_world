from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^users/create', views.createUser, name = "create_user"),
    url(r'^snacks/create', views.createSnack, name = "create_snack"),
    url(r'^carts/create', views.createCart, name = "create_cart"),
    url(r'^wishlists/create', views.createWishlist, name = "create_wishlist"),
    url(r'^users/destroy/(?P<pk>\d+)', views.destroyUser, name = "destroy_user"),
    url(r'^snacks/destroy/(?P<pk>\d+)', views.destroySnack, name = "destroy_snack"),
    url(r'^carts/destroy/(?P<pk>\d+)', views.destroyCart, name = "destroy_cart"),
    url(r'^wishlists/destroy/(?P<pk>\d+)', views.destroyWishlist, name = "destroy_wishlist"),
    url(r'^users/update/(?P<pk>\d+)', views.updateUser, name = "update_user"),
    url(r'^snacks/update/(?P<pk>\d+)', views.updateSnack, name = "update_snack"),
    url(r'^carts/update/(?P<pk>\d+)', views.updateCart, name = "update_cart"),
    url(r'^wishlists/update/(?P<pk>\d+)', views.updateWishlist, name = "update_wishlist"),
    url(r'^users/(?P<pk>\d+)', views.getUsers, name = "get_users"),
    url(r'^snacks/(?P<pk>\d+)', views.getSnacks, name = "get_snacks"),
    url(r'^wishlists/(?P<pk>\d+)', views.getWishlists, name = "get_wishlists"),
    url(r'^carts/(?P<pk>\d+)', views.getCarts, name = "get_carts"),
    url(r'^snacks/', views.get_all_snacks, name = "get_all_snacks"),
    url(r'^users/', views.get_all_users, name = "get_all_users"),
    url(r'^users/check_login', views.check_user_login, name = "check_login"),
    url(r'^create_auth/(?P<pk>\d+)', views.generate_authenticator, name = "create_auth"),
]