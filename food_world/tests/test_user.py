from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import User
import logging


class userTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        u = User.objects.create(pk=1, first_name='Test', last_name='User', email='test@user.com', phone_number='123-456-7890')
        u.save()
    def test_create_user(self):
        data = {
            'pk': 2,
            'first_name': 'Bob',
            'last_name': 'Dylan',
            'email': 'bob@aol.com',
            'phone_number': '531-225-7765',
        }
        response = self.client.post(reverse('create_user'),data)
        self.assertTrue(User.objects.all().filter(pk=int(response.json()['id'])).exists(), msg="Object did not actually get created in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="Return status code is not 200! Error with create_user API!")

    def test_get_all_users(self):
        response = self.client.get(reverse('get_all_users'))
        self.assertContains(response, 'data' , msg_prefix= str(response.json()))

    def test_get_user(self):
        response = self.client.get(reverse('get_users', kwargs={'pk': 1}))
        self.assertContains(response, 'data', msg_prefix = str(response.json()))

    #Change First Name of created object in set up
    def test_update_user(self):
        data = {
            'first_name': 'Mark',
         }
        
        response = self.client.post(reverse('update_user', kwargs={'pk': 1}),data)
        self.assertTrue(User.objects.all().filter(first_name='Mark').exists(), msg="User did not actually get updated with new name!")
        self.assertEquals(response.json()['data']['first_name'], 'Mark', msg="Change did not happen! Error")

    def test_delete_user(self):
        response = self.client.post(reverse('destroy_user', kwargs={'pk': 1}))
        self.assertFalse(User.objects.all().filter(pk=7).exists(), msg="User did not actually get deleted in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="User not deleted!")

    def test_get_invalid_user(self):
        response = self.client.get(reverse('get_users', kwargs={'pk': 2}))
        self.assertNotContains(response, 'data', msg_prefix= str(response))


    def test_delete_invalid_user(self):
        response = self.client.post(reverse('destroy_user', kwargs={'pk': 5}))
        self.assertEquals(response.json()['status_code'], str(500), msg="User deleted that does not exist!")

    def test_update_invalid_user(self):
        data = {
            'first_name': 'Mark',
         }
        
        response = self.client.post(reverse('update_user', kwargs={'pk': 5}),data)
        self.assertFalse(User.objects.all().filter(first_name='Mark').exists(), msg="User did not actually get updated with new name!")
        self.assertNotContains(response, 'data' , msg_prefix="Change did not happen! Error")

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
