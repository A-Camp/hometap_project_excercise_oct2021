# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Home
import factory
from .factories import HomeFactory, UserFactory

class HomeViewTestCase(TestCase):
    def get_detail_url(self, home):
            return f'/homes/{home.id}/'

    def test_user_is_owner(self):
        pwd = 'test'
        self.user = UserFactory(password=pwd)
        self.home=HomeFactory(owner=self.user)
        self.assertTrue(self.client.login(username=self.user.username, password=pwd))

        with self.subTest('test_current_homes'):
            """GET current users Homes."""
            response = self.client.get('/homes/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            #Not adding anymore tests because testing Model.objects.filter would just be testing Django itself
        
        with self.subTest('test_get_detail'):
            """GET a detail page for a Home."""
            response = self.client.get(self.get_detail_url(self.home))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            for field_name in [
                'address', 'zipcode', 'city', 'state', 'has_septic', 'user_septic_info'
            ]:
                self.assertEqual(response.data[field_name], getattr(self.home, field_name))
        
        with self.subTest('test_post'):
            """POST to create a Home."""
            data = {
                "address": "123 Sesame St",
                "zipcode": '00000',
                "city": 'New York City',
                "state": 'NY',
            }
            count = Home.objects.count()
            response = self.client.post('/homes/', data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Home.objects.count(), count+1)
            home = Home.objects.get(id=response.data['id'])
            # Check that owner is set as logged in user
            self.assertEqual(getattr(home, 'owner'), self.user)
            for field_name in data.keys():
                    self.assertEqual(getattr(home, field_name), data[field_name])

        with self.subTest('test_patch'):
            """PATCH to update a Home."""
            home2 = HomeFactory(user_septic_info=None, owner=self.user)
            data = {
                'user_septic_info': 'I think it was put in around the 1950s'
            }
            response = self.client.patch(
                self.get_detail_url(home2),
                data=data,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # The object has really been updated
            self.assertEqual(getattr(home2, 'user_septic_info'), None)
            home2.refresh_from_db()
            self.assertEqual(getattr(home2, 'user_septic_info'), data['user_septic_info'])

    def test_user_is_admin_not_owner(self):
        pwd = 'test'
        self.user = UserFactory(password=pwd, is_superuser=True)
        self.home=HomeFactory()
        self.assertTrue(self.client.login(username=self.user.username, password=pwd))

        with self.subTest('test_get_detail'):
            """GET a detail page for a Home."""
            response = self.client.get(self.get_detail_url(self.home))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            for field_name in [
                'address', 'zipcode', 'city', 'state', 'has_septic', 'user_septic_info'
            ]:
                self.assertEqual(response.data[field_name], getattr(self.home, field_name))
        
        with self.subTest('test_patch'):
            """PATCH to update a Home."""
            home2 = HomeFactory(user_septic_info=None)
            data = {
                'user_septic_info': 'I think it was put in around the 1950s'
            }
            response = self.client.patch(
                self.get_detail_url(home2),
                data=data,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # The object has really been updated
            self.assertEqual(getattr(home2, 'user_septic_info'), None)
            home2.refresh_from_db()
            self.assertEqual(getattr(home2, 'user_septic_info'), data['user_septic_info'])

    def test_unauthenticated(self):
        """Unauthenticated users may not use the API."""
        self.client.logout()
        self.home=HomeFactory()

        with self.subTest('test_get_detail'):
            response = self.client.get(self.get_detail_url(self.home))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest('test_post'):
            data = {
                "address": "123 Sesame St",
                "zipcode": '00000',
                "city": 'New York City',
                "state": 'NY',
            }
            response = self.client.put('/homes/', data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest('test_patch'):
            data = {'zipcode': '99999'}
            response = self.client.patch(self.get_detail_url(self.home), data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            # The home was not updated
            self.home.refresh_from_db()
            self.assertNotEqual(self.home.zipcode, data['zipcode'])
