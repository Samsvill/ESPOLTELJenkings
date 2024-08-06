from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from user.models import UserProfile

class CreateUserViewTest(APITestCase):
    def test_create_user(self):
        url = reverse('registro')
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserProfileRetrieveTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            email='test@test.com',
            name='Test User',
            cedula='12345',
            is_active=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_user_profile_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        url = reverse('perfil') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data['id'], self.user_profile.id)
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['email'], self.user_profile.email)
        self.assertEqual(data['name'], self.user_profile.name)
        self.assertEqual(data['cedula'], self.user_profile.cedula)
        self.assertEqual(data['is_active'], self.user_profile.is_active)

        self.client.credentials()