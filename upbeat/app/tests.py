from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup(self):
        response = self.client.post('/signup/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone_number": "1234567890",
            "hashed_password": "yourpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        self.client.post('/signup/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone_number": "1234567890",
            "hashed_password": "yourpassword"
        })
        response = self.client.post('/login/', {
            "email": "testuser@example.com",
            "password": "yourpassword"
        })
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
