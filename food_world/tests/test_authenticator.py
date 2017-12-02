from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import User, Authenticator
import logging


class authTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        pass
    
   	def test_generate_authenticator(self):
        u2 = User.objects.create(pk=2, first_name='Bob', last_name='Dylan', email='bob@aol.com', phone_number='531-225-7765')
        u2.save()
        user_2 = User.objects.get(pk = u2.id)
        data = {
            'User' : user_2.id,
        }
        response = self.client.post(reverse('create_authenticator'),data)

        self.assertEquals(response.json()['status_code'], str(200), msg="Return status code is not 200! Error with create_cart API!")