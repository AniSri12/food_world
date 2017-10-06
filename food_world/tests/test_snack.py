from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from food_core.models import Snack
import logging


class snackTest(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        s = Snack.objects.create(pk=1, name='Chickpeas', price=15.25, description= 'Dired, salted and spiced chickpeas', country= 'India', nutrition_info='Great for you!')
        s.save()

    #Creating a snack (User Story)
    def test_create_snack(self):
        data = {
            'pk': 2,
            'name': 'Seaweed',
            'price': 1.25,
            'country': 'Japan',
            'description': 'Dired Crunchy Seaweed!',
            'nutrition_info': 'Great for you! Salty!',
        }
        response = self.client.post(reverse('create_snack'),data)
        self.assertTrue(Snack.objects.all().filter(pk=2).exists(), msg="Object did not actually get created in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="Return status code is not 200! Error with create_user API!")


    def test_get_all_snacks(self):
        response = self.client.get(reverse('get_all_snacks'))
        self.assertContains(response, 'data' , msg_prefix= str(response.json()))

    def test_get_snack(self):
        response = self.client.get(reverse('get_snacks', kwargs={'pk':1}))
        self.assertContains(response, 'data', msg_prefix= str(response.json()))

    #change price of item
    def test_update_snack(self):
        data = {
            'price' : 6.99,
        }
        response = self.client.post(reverse('update_snack', kwargs={'pk': 1}),data)
        self.assertTrue(Snack.objects.all().filter(price='6.99').exists(), msg="Snack did not actually get updated with new name!")
        self.assertEquals(response.json()['data']['price'], str(6.99), msg="Change did not happen! Error")


    def test_delete_snack(self):
        response = self.client.post(reverse('destroy_snack', kwargs={'pk': 1}))
        self.assertFalse(Snack.objects.all().filter(pk=1).exists(), msg="Snack did not actually get deleted in db with API!")
        self.assertEquals(response.json()['status_code'], str(200), msg="Snack not deleted!")

    def test_get_invalid_snack(self):
        response = self.client.get(reverse('get_snacks', kwargs={'pk':2}))
        self.assertNotContains(response, 'data', msg_prefix= str(response))
    

    def test_delete_invalid_snack(self):
        response = self.client.post(reverse('destroy_snack', kwargs={'pk': 7}))
        self.assertEquals(response.json()['status_code'], str(500), msg="Snack that shouldn't exists, got deleted")
        

    def test_update_invalid_snack(self):
        data = {
            'price' : 6.99,
        }
        response = self.client.post(reverse('update_snack', kwargs={'pk': 5}),data)
        self.assertFalse(Snack.objects.all().filter(price='6.99').exists(), msg="Snack that does not exist, now exists, bad!")
        self.assertEquals(response.json()['status_code'], '500', msg="Object shouln't exit yet was updated")

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
