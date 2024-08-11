from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from user.models import UserProfile, Role, UserRole
from proyecto.models import Proyecto, BudgetItem
from solicitud.models import Solicitud, ItemSolicitud, Estado, Cotizacion, Formulario, Factura
from datetime import datetime
from base_cases import set_test_user

#TC-101
class CreateUserViewTest(APITestCase):
    def test_create_user(self):
        url = reverse('registro')
        data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
        response = self.client.post('/user/registro/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#TC-102 Create a user with an existing username
class CreateUserWithExistingusernameViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lcanarte', password='Jq23%aS@')
        self.user.save()

    def test_create_user_with_existing_username(self):
        url = reverse('registro')
        data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#TC-103 Correct credentials
class TokenObtainPairViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lcanarte', password='Jq23%aS@')
        self.user.save()

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#TC-104 Incorrect credentials
class TokenObtainPairViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lcanarte', password='Jq23%aS@')
        self.user.save()

    def test_token_obtain_pair(self):
        url = reverse('get_token')
        data = {'username': 'lcanarte', 'password': 'lcanarte'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#TC-301 Create a role
class CreateRoleViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
    
    def test_create_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('roles')
        data = {'description': 'PM'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

#TC-302 Delete existing role
class DeleteRoleViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_delete_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('roles') + str(self.role.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.credentials()

#TC-303 Delete non-existing role
class DeleteRoleViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)

    def test_delete_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('roles') + '100/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

#TC-501 Create a project
class CreateProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_create_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create')
        data = {'nombre': 'Proyecto prueba',
                'project_budget': 10000,
                'budget_items': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

#TC-502 Create a project with an existing nombre
class CreateProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create')
        data = {'nombre': 'Proyecto prueba',
                'project_budget': 10000,
                'budget_items': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials()

#TC-503 Create a project without jwt token
class CreateProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_create_project(self):
        url = reverse('proyecto-list-create')
        data = {'nombre': 'Proyecto prueba',
                'project_budget': 10000,
                'budget_items': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#TC-504 PUT request to update a project
class UpdateProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000,
                created_by=self.user_profile)

    def test_update_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create') + str(self.project.id) + '/'
        data = {'nombre': 'Proyecto prueba, nuevo',
                'project_budget': 12000,
                'budget_items': []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

#TC-505 PUT request to update a project with non-existing id
class UpdateProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000)

    def test_update_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create') + '10/'
        data = {'nombre': 'Proyecto prueba, nuevo',
                'project_budget': 12000,
                'budget_items': []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

#TC-601 POST request with valid project id and budget item name
class CreateBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create') + str(self.project.id) + '/items/'
        data = {
            "recurso": "Recurso Actualizado",
            "categoria": "Categoría Actualizada",
            "cantidad": 20,
            "valor": 150.0,
            "presupuesto": 3000.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

#TC-602 POST request with valid project id and many budget items
class CreateBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create') + str(self.project.id) + '/items/'
        data = {
            "budget_items": [
                {
                    "recurso": "Recurso 1",
                    "categoria": "Categoría 1",
                    "cantidad": 20,
                    "valor": 150.0,
                    "presupuesto": 3000.0

                },
                {
                    "recurso": "Recurso Actualizado 2",
                    "categoria": "Categoría Actualizada 2",
                    "cantidad": 30,
                    "valor": 250.0,
                    "presupuesto": 7500.0
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

#TC-603 POST request with invalid project id
class CreateBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create') + '10/items/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

#TC-604 POST request with no budget item name provided
class CreateBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-list-create') + str(self.project.id) + '/items/'
        data = {
            "budget_items": [
                {
                    "recurso": "",
                    "categoria": "Categoría Actualizada",
                    "cantidad": 20,
                    "valor": 150.0,
                    "presupuesto": 3000.0
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials()

#TC-605 POST request with no jwt token provided
class CreateBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        url = reverse('proyecto-list-create') + str(self.project.id) + '/items/'
        data = {
            "budget_items": [
                {
                    "recurso": "Recurso Actualizado",
                    "categoria": "Categoría Actualizada",
                    "cantidad": 20,
                    "valor": 150.0,
                    "presupuesto": 3000.0
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)