from django.db import models

# Create your models here.

from django.db import models
import datetime

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=128, help_text="enter First Name here")
    last_name = models.CharField(max_length=128, help_text="enter Last Name here")
    email = models.EmailField()
    phone_number = models.CharField(max_length=128, default = "")
    password = models.CharField(max_length=128, default = "")
    authenticator = models.OneToOneField("Authenticator")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.first_name



class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cart")
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    num_items = models.IntegerField()

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"



class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlist")
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    num_items = models.IntegerField()

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"




class Snack(models.Model):
    carts = models.ManyToManyField(Cart, related_name='cart', null = True, blank = True)
    wishlists = models.ManyToManyField(Wishlist, related_name='wishlist', null = True, blank = True)
    name = models.CharField(max_length=128, help_text="name of food item")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateField(default=datetime.date.today)
    country = models.CharField(max_length = 100, default = "Country Not Specified")
    description = models.TextField()
    nutrition_info = models.TextField()

    class Meta:
        verbose_name = "Snack"
        verbose_name_plural = "Snacks"
        
    def __str__(self):

        return self.name


class Authenticator(models.Model):
    user_id = models.IntegerField(default = 0)
    authenticator = models.IntegerField(default = 0)
    date_created = models.DateField(default=datetime.date.today)

