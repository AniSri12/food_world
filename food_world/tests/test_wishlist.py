from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import Wishlist
import logging


class wishlistTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        #s = Wishlist.objects.create(pk=1, name='Chickpeas', price=15.25, description='Dired, salted and spiced chickpeas', nutrition_info='Great for you!')
        u = User.objects.create(first_name='Test', last_name='User', email='test@user.com', phone_number='123-456-7890')
        u.save()
        user_1 = User.objects.get(pk=1)
        u2= User.objects.create(first_name='Test2', last_name='User', email='test@user.com', phone_number='123-456-7890')
        u.save()
        user_2 = User.objects.get(pk=1)
        s = Wishlist.objects.create(user = user_1, total_price = 500.26, num_items=5)
        
    def test_create_wishlist(self):
        data = {
            'pk': 2,
            'total_price': 12.0,
            'num_items': 5,
            'user': u2,
        }
        response = self.client.post(reverse('create_wishlist'),data)
        self.assertTrue(Wishlist.objects.all().filter(pk=2).exists(), msg="Object did not actually get created in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="Return status code is not 200! Error with create_user API!")
        
    def test_get_wishlist(self):
        response = self.client.get(reverse('get_wishlists', kwargs={'pk':1}))
        self.assertContains(response, 'data', msg_prefix= str(response.json()))

    def test_update_wishlist(self):
        data = {
            'total_price': 12.0,
         }
        
        response = self.client.post(reverse('update_wishlist', kwargs={'pk': 2}),data)
        print(response.json())
        self.assertTrue(Wishlist.objects.all().filter(total_price=12.0).exists(), msg="User did not actually get updated with new name!")
        self.assertEquals(response.json()['data']['total_price'], 12.0, msg="Change did not happen! Error")

    def test_delete_wishlist(self):
        response = self.client.post(reverse('destroy_wishlist', kwargs={'pk': 1}))
        self.assertFalse(Wishlist.objects.all().filter(pk=1).exists(), msg="Wishlist did not actually get deleted in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="Wishlist not deleted!")

    def test_get_invalid_wishlist(self):
        response = self.client.get(reverse('get_wishlists', kwargs={'pk':2}))
        self.assertContains(response, 'data', msg_prefix= str(response))
       

    def test_delete_invalid_wishlist(self):
        response = self.client.post(reverse('destroy_wishlist', kwargs={'pk': 12}))
        self.assertEquals(response.json()['status_code'], str(500), msg="Wishlist that shouldn't exist, got deleted")

    def test_update_invalid_wishlist(self):
        data = {
            'total_price' : 6.99,
        }
        response = self.client.post(reverse('update_snack', kwargs={'pk': 12}),data)
        self.assertFalse(Snack.objects.all().filter(total_price='6.99').exists(), msg="Wishlist that does not exist, now exists, bad!")
        self.assertEquals(response.json()['status_code'], '500', msg="Object shouln't exist yet was updated")

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down