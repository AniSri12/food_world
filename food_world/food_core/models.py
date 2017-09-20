from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=128, help_text="enter First Name here")
    last_name = models.CharField(max_length=128, help_text="enter Last Name here")
    email = models.EmailField()
    phone_number = models.CharField(max_length=128)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        pass


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cart")
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    num_items = models.IntegerField()

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        pass


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlist")
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    num_items = models.IntegerField()

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wus"

    def __str__(self):
        pass


class Snack(models.Model):
    carts = models.ManyToManyField(Cart, related_name='cart')
    wishlists = models.ManyToManyField(Wishlist, related_name='wishlist')
    name = models.CharField(max_length=128, help_text="name of food item")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    nutrition_info = models.TextField()

    class Meta:
        verbose_name = "Snack"
        verbose_name_plural = "Snacks"

    def __str__(self):
        pass



