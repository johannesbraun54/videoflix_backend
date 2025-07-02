from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User

class RegistartionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_check_new_email_availability(self):
        url = reverse('email_availability')
        new_email = 'example@mail.de'
        response = self.client.post(url, {'email': new_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': False})
        
    def test_check_existing_email_availability(self):
        url = reverse('email_availability')
        exisisting_email = 'example@mail.de'
        User.objects.create_user(username='testuser', email=exisisting_email, password='testpassword')
        response = self.client.post(url, {'email': exisisting_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'exists': True})
        
    def test_check_bad_request(self):
        url = reverse('email_availability')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Email is required"})