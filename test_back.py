from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from user.models import UserProfile, Role, UserRole
from proyecto.models import Proyecto, BudgetItem, ItemSolicitud
from solicitud.models import Solicitud, Estado, Cotizacion, Formulario, Factura
from datetime import datetime
from base_cases import set_test_user


class CreateUserViewTest(APITestCase):
    def test_create_user(self):
        url = reverse('registro')
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserProfileRetrieveTest(APITestCase):
    def setUp(self):
        set_test_user(self)

    def test_user_profile_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('perfil') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

class CreateRoleTest(APITestCase):
    def setUp(self):
        set_test_user(self)

    def test_create_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('roles')
        data = {'description': 'Director de Proyecto'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

class 