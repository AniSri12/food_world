from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import Cart, User
import logging
from django.forms.models import model_to_dict


class cartTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        pass
        
    def test_create_cart(self):
        u2 = User.objects.create(pk=2, first_name='Bob', last_name='Dylan', email='bob@aol.com', phone_number='531-225-7765')
        u2.save()
        user_2 = User.objects.get(pk = u2.id)
        data = {
            'User' : user_2.id,
            'total_price' : '657.23',
            'num_items' : '5',
        }
        response = self.client.post(reverse('create_cart'),data)

        self.assertEquals(response.json()['status_code'], str(200), msg="Return status code is not 200! Error with create_cart API!")

    def test_get_cart(self):
        u = User.objects.create(pk=1, first_name='Test', last_name='User', email='test@user.com', phone_number='123-456-7890')
        u.save()
        user_1 = User.objects.get(pk=u.id)
        s = Cart.objects.create(user = user_1, total_price = 500.26, num_items=5)
        s.save()
        cart = Cart.objects.get(pk=s.id)
        response = self.client.get(reverse('get_carts', kwargs={'pk': cart.id}))
        self.assertContains(response, 'total_price', msg_prefix = "did not work")

    def test_update_cart(self):
        u = User.objects.create(pk=1, first_name='Test', last_name='User', email='test@user.com', phone_number='123-456-7890')
        u.save()
        user_1 = User.objects.get(pk=u.id)
        s = Cart.objects.create(user = user_1, total_price = 500.26, num_items=5)
        s.save()
        data = {
            'total_price': 20.00,
         }
        
        response = self.client.post(reverse('update_cart', kwargs={'pk': s.id}),data)
        self.assertTrue(Cart.objects.all().filter(total_price=20.00).exists(), msg="Cart did not actually get updated with new price!")
        self.assertEquals(response.json()['total_price'], '20.0', msg="Change did not happen! Error")

    def test_delete_cart(self):
        u = User.objects.create(pk=1, first_name='Test', last_name='User', email='test@user.com', phone_number='123-456-7890')
        u.save()
        user_1 = User.objects.get(pk=u.id)
        s = Cart.objects.create(user = user_1, total_price = 500.26, num_items=5)
        s.save()
        response = self.client.post(reverse('destroy_cart', kwargs={'pk': s.id}))
        self.assertFalse(Cart.objects.all().filter(pk=1).exists(), msg="Cart did not actually get deleted in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="Cart not deleted!")
        pass

    def test_get_invalid_cart(self):
        response = self.client.get(reverse('get_carts', kwargs={'pk': 8}))
        self.assertNotContains(response, 'data', msg_prefix= "Got a cart that should not be in db!")


    def test_delete_invalid_cart(self):
        response = self.client.post(reverse('destroy_cart', kwargs={'pk': 5}))
        self.assertEquals(response.json()['status_code'], str(500), msg="Cart deleted that does not exist!")

    def test_update_invalid_cart(self):
        data = {
            'total_price': '20.00',
         }
        
        response = self.client.post(reverse('update_cart', kwargs={'pk': 1}),data)
        self.assertFalse(Cart.objects.all().filter(total_price=20.00).exists(), msg="Cart does get updated")
        self.assertNotContains(response, 'total_price', msg_prefix="Change did not happen on invalid data! Good!")

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
