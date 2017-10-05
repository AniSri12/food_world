from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import Wishlist
import logging


class wishlistTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        #s = Wishlist.objects.create(pk=1, name='Chickpeas', price=15.25, description='Dired, salted and spiced chickpeas', nutrition_info='Great for you!')
        pass
    def test_create_wishlist(self):
        pass
        
    def test_get_wishlist(self):
        #response = self.client.get(reverse('get_wishlists', kwargs={'pk':1}))
        #self.assertContains(response, 'data', msg_prefix= str(response.json()))
        pass

    def test_update_wishlist(self):
        pass

    def test_delete_wishlist(self):
        pass

    def test_get_invalid_wishlist(self):
        # response = self.client.get(reverse('get_wishlists', kwargs={'pk':2}))
        # self.assertContains(response, 'Data', msg_prefix= str(response))
        pass

    def test_delete_invalid_wishlist(self):
        pass

    def test_update_invalid_wishlist(self):
        pass

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
