from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import Cart
import logging


class cartTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        #create an object
        #s = Cart.objects.create(pk=1, )
        pass
    def test_create_cart(self):
        pass

    def test_get_cart(self):
        #response = self.client.get(reverse('get_carts', kwargs={'pk':1}))
        #self.assertContains(response, 'data', msg_prefix= str(response.json()))
        pass
    def test_update_cart(self):
        pass

    def test_delete_cart(self):
        pass

    def test_get_invalid_cart(self):
        # response = self.client.get(reverse('get_carts', kwargs={'pk':2}))
        # self.assertContains(response, 'Data', msg_prefix= str(response))
        pass

    def test_delete_invalid_cart(self):
        pass

    def test_update_invalid_cart(self):
        pass

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
