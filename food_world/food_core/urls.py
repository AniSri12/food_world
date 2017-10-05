from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^users/(?P<pk>\d+)', views.getUsers, name = "get_user"),
    url(r'^snacks/(?P<pk>\d+)', views.getSnacks, name = "get_snacks"),
    url(r'^snacks/', views.get_all_snacks, name = "get_all_snacks"),
    url(r'^users/', views.get_all_users, name = "get_all_users"),
    url(r'^users/create', views.createUser, name = "create_user"),
    url(r'^snacks/create', views.createSnack, name = "create_snack"),
    url(r'^carts/create', views.createCart, name = "create_cart"),
    url(r'^wishlists/create', views.createWishlist, name = "create_wishlist"),
    url(r'^users/destroy', views.destroyUser),
    url(r'^snacks/destroy', views.destroySnack),
    url(r'^carts/destroy', views.destroyCart),
    url(r'^wishlists/destroy', views.destroyWishlist),
    url(r'^users/update', views.updateUser),
    url(r'^snacks/update', views.updateSnack),
    url(r'^carts/update', views.updateCart),
    url(r'^wishlists/update', views.updateWishlist),

]