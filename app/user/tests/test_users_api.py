from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status



CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API"""

    def  setUp(self):
        self.client = APIClient()

    def  test_create_valid_user_success(self):
        """Test creating user with valid payload"""
        payload = {
            'email':'test@gmail.com',
            'password':'test9000',
            'name':'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exitst(self):
        """Test creating user with valid payload"""
        payload = {
            'email':'test@gmail.com',
            'password':'test9000',
            'name':'Test name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



    def  test_password_too_short(self):
        """Test creating user with valid payload"""
        payload = {
            'email':'test@gmail.com',
            'password':'pw',
            'name':'Test name'
        }
        res =  self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Testing our token"""
        payload = {
            'email' :'jado@gmail.com',
            'password':'iradukunda',
            'name':'jadodiye'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials"""
        create_user(email='jado@gmail.com',password='jadodiye')
        payload = {
            'email' :'jado@gmail.com',
            'password':'iradukunda'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_Create_token_no_user(self):
        """Testt if token is not created"""
        payload = {
            'email' :'jado@gmail.com',
            'password':'iradukunda'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_toke_missing_field(self):
        """Testt if token is not created"""
        payload = {
            'email' :'jado@gmail.com',
            'password':''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
