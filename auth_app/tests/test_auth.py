from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User

class RegistartionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_check_existing_email(self):
        url = reverse('verif_email')
        new_email = 'example@mail.de'
        reponse = self.client.post(url, {'email': new_email})
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)