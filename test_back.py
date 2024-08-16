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

# TC-101
class CreateUserViewTest(APITestCase):
    def test_create_user(self):
        url = reverse('registro')
        data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
        response = self.client.post('/user/registro/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# TC-102 Create a user with an existing username
class CreateUserWithExistingUsernameViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lcanarte', password='Jq23%aS@')
        self.user.save()

    def test_create_user_with_existing_username(self):
        url = reverse('registro')
        data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# TC-201 Correct credentials
class ValidTokenObtainPairViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lcanarte', password='Jq23%aS@')
        self.user.save()

    def test_token_obtain_pair(self):
        url = reverse('get_token')
        data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# TC-202 Incorrect credentials
class InvalidTokenObtainPairViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lcanarte', password='Jq23%aS@')
        self.user.save()

    def test_token_obtain_pair(self):
        url = reverse('get_token')
        data = {'username': 'lcanarte', 'password': 'lcanarte'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# TC-301 Create a role
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

# TC-302 Delete existing role
class DeleteRoleViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_delete_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('roles-delete', kwargs={'pk': self.role.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.credentials()

# TC-303 Delete non-existing role
class DeleteNonExistingRoleViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)

    def test_delete_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('roles-delete', kwargs={'pk': 100})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

# TC-501 Create a project
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

# TC-502 Create a project with an existing nombre
class CreateProjectWithExistingNameViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
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

# TC-503 Create a project without jwt token
class CreateProjectWithoutTokenViewTest(APITestCase):
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

# TC-504 PUT request to update a project
class UpdateProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_update_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-detail', kwargs={'pk': self.project.id})
        data = {'nombre': 'Proyecto prueba, nuevo',
                'project_budget': 12000,
                'budget_items': []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

# TC-505 PUT request to update a project with non-existing id
class UpdateNonExistingProjectViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_update_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('proyecto-detail', kwargs={'pk': 9})
        data = {'nombre': 'Proyecto prueba, nuevo',
                'project_budget': 12000,
                'budget_items': []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

# TC-601 POST request with valid project id and budget item name
class CreateBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-budget-items', kwargs={'proyecto_id': self.project.id})
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

# TC-602 POST request with valid project id and many budget items
class CreateMultipleBudgetItemsViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-budget-items', kwargs={'proyecto_id': self.project.id})
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

# TC-603 POST request with invalid project id
class CreateInvalidBudgetItemViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-budget-items', kwargs={'proyecto_id': 100})
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

# TC-604 POST request with no budget item name provided
class CreateBudgetItemWithoutNameViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-budget-items', kwargs={'proyecto_id': self.project.id})
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

# TC-605 POST request with no jwt token provided
class CreateBudgetItemWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_budget_item(self):
        url = reverse('crear-budget-items', kwargs={'proyecto_id': self.project.id})
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

# TC-701 POST request to create a solicitud with valid project id, all fields filled
class CreateSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_create_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-solicitud', kwargs={'pk': self.project.id})
        data = {
            "nombre": "Solicitud de prueba",
            "tema": "Probando",
            "tipo": "Compra",
            "estado": self.estado.id,
            "proyecto": self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

# TC-702 POST request to create a solicitud with invalid project id
class CreateInvalidSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_create_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-solicitud', kwargs={'pk': 100})
        data = {
            "nombre": "Solicitud de prueba",
            "tema": "Probando",
            "tipo": "Compra",
            "estado": self.estado.id,
            "proyecto": 10
        }
        response = self.client.post(url, data, format='json')
        self.client.credentials()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# TC-703 PUT request to update a solicitud with an invalid cotizacion id
class InvalidCotizacionUpdateSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile,
                                               #usuario_modificacion = self.user,
                                               nombre='Proyecto prueba',
                project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                tema='Probando',
                tipo='Compra',
                estado=self.estado,
                proyecto=self.project,
                usuario_creacion=self.user_profile,
                usuario_modificacion=self.user_profile)

    def test_update_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('detalle-solicitud', kwargs={'pk': self.solicitud.id})
        data = {
            "nombre": "Solicitud de prueba",
            "tema": "Probando",
            "tipo": "Compra",
            "estado": self.estado.id,
            "proyecto": self.project.id,
            "cotizacion_aceptada": 100
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

#TC-704 POST request to create a solicitud with no jwt token provided
class CreateSolicitudWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.role = Role.objects.create(description='PM')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion = self.user_profile, nombre='Proyecto prueba',
                project_budget=10000)

    def test_create_solicitud(self):
        url = reverse('crear-solicitud', kwargs={'pk': self.project.id})
        data = {
            "nombre": "Solicitud de prueba",
            "tema": "Probando",
            "tipo": "Compra",
            "estado": self.estado.id,
            "proyecto": self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

 #TC-801 POST request to create a cotizacion with valid solicitud id, all fields filled
class CreateCotizacionViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_cotizacion(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('cotizaciones-solicitud', kwargs={'pk': self.solicitud.id})
        data = {
            "proveedor": "Proveedor de prueba",
            "monto": 1000.0,
            "fecha_coti": "01-06-2021",
        }

        response = self.client.post(url, data, format='json')
        self.client.credentials()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

# TC-802 POST request to create a cotizacion with invalid solicitud id
class CreateInvalidCotizacionViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_create_cotizacion(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('cotizaciones-solicitud', kwargs={'pk': 100})
        data = {
            "proveedor": "Proveedor de prueba",
            "monto": 1000.0,
            "fecha_coti": "2021-06-01"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-803 POST request to create a cotizacion with no jwt token provided
class CreateCotizacionWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_cotizacion(self):
        url = reverse('cotizaciones-solicitud', kwargs={'pk': self.solicitud.id})
        data = {
            "proveedor": "Proveedor de prueba",
            "monto": 1000.0,
            "fecha_coti": "2021-06-01",
            "solicitud": self.solicitud.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# TC-804 DELETE request to delete a cotizacion with valid solicitud id
class DeleteCotizacionViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)
        self.cotizacion = Cotizacion.objects.create(
            proveedor='Proveedor de prueba',
        monto=1000.0,
        solicitud=self.solicitud,
        fecha_coti='2021-06-01'
)

    def test_delete_cotizacion(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('cotizaciones-solicitud', kwargs={'pk': self.solicitud.id })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()


# TC-805 DELETE request to delete a cotizacion with invalid solicitud id
class DeleteInvalidCotizacionViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_delete_cotizacion(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('cotizaciones-solicitud', kwargs={'pk': 100})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-806 DELETE request to delete a cotizacion with no jwt token provided
class DeleteCotizacionWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)
        self.cotizacion = Cotizacion.objects.create(
            proveedor='Proveedor de prueba',
        monto=1000.0,
        solicitud=self.solicitud,
        fecha_coti='2021-06-01'
)

    def test_delete_cotizacion(self):
        url = reverse('cotizaciones-solicitud', kwargs={'pk': self.solicitud.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# TC-901 POST request to create a formulario with valid solicitud id
class CreateFormularioViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_formulario(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-formulario', kwargs={'pk_s': self.solicitud.id})
        data = {
            "cedula_ruc": "0999999999",
            "descripcion": "Descripción de prueba",
            "solicitud": self.solicitud.id,
            "url_compra": "http://example.com/compra",
            "url_certi_banco": "http://example.com/certi_banco"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()


# TC-902 POST request to create a formulario with invalid solicitud id
class CreateInvalidFormularioViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_create_formulario(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-formulario', kwargs={'pk_s': 100})
        data = {
            "descripcion": "Descripción de prueba",
            "url_compra": "http://example.com/compra",
            "url_certi_banco": "http://example.com/certi_banco"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-903 POST request to create a formulario with no jwt token provided
class CreateFormularioWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_formulario(self):
        url = reverse('crear-formulario', kwargs={'pk_s': self.solicitud.id})
        data = {
            "cedula_ruc": "0999999999",
            "descripcion": "Descripción de prueba",
            "solicitud": self.solicitud.id,
            "url_compra": "http://example.com/compra",
            "url_certi_banco": "http://example.com/certi_banco"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# TC-1001 POST request to create a factura with valid solicitud id
class CreateFacturaViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_factura(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-detalle-factura', kwargs={'pk_s': self.solicitud.id})
        data = {
    "estado": "Estado de prueba",
    "monto": 1000.00000
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()


# TC-1002 POST request to create a factura with invalid solicitud id
class CreateInvalidFacturaViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_create_factura(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-detalle-factura', kwargs={'pk_s': 100})
        data = {
    "estado": "Estado de prueba",
    "monto": 1000.00000
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-1003 POST request to create a factura with no jwt token provided
class CreateFacturaWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_factura(self):
        url = reverse('crear-detalle-factura', kwargs={'pk_s': self.solicitud.id})
        data = {
    "estado": "Estado de prueba",
    "monto": 1000.00000
}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# TC-1004 PUT request to update a factura with a valid solicitud id
class UpdateFacturaViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)
        self.factura = Factura.objects.create(
            solicitud=self.solicitud,
            estado = "En revisión",
            monto = 1000.0,
)

    def test_update_factura(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-detalle-factura', kwargs={'pk_s': self.solicitud.id})
        data = {
    "estado": "Estado de prueba",
    "monto": 1000.00000
}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()


# TC-1005 PUT request to update a factura with an invalid solicitud id
class UpdateInvalidFacturaViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_update_factura(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-detalle-factura', kwargs={'pk_s': 100})
        data = {
    "estado": "Estado de prueba",
    "monto": 1000.00000
}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-1006 PUT request to update a factura with no jwt token provided
class UpdateFacturaWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)
        self.factura = Factura.objects.create(
            solicitud=self.solicitud,
            estado = "En revisión",
            monto = 1000.0
)

    def test_update_factura(self):
        url = reverse('crear-detalle-factura', kwargs={'pk_s': self.solicitud.id})
        data = {
    "estado": "Estado de prueba",
    "monto": 1000.00000
}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# TC-1101 POST request to create an item solicitud with valid solicitud id
class CreateItemSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_item_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-items-solicitud', kwargs={'pk_s': self.solicitud.id})
        data = {
            "nombre": "Item de prueba",
            "descripcion": "Descripción de prueba",
            "cantidad": 20,
            "valor": 1000.0,
            "solicitud": self.solicitud.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()


# TC-1102 POST request to create an item solicitud with invalid solicitud id
class CreateInvalidItemSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')

    def test_create_item_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('crear-items-solicitud', kwargs={'pk_s': 100})
        data = {
            "nombre": "Item de prueba",
            "descripcion": "Descripción de prueba",
            "cantidad": 20,
            "valor": 1000.0,
            "solicitud": 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-1103 POST request to create an item solicitud with no jwt token provided
class CreateItemSolicitudWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_create_item_solicitud(self):
        url = reverse('crear-items-solicitud', kwargs={'pk_s': self.solicitud.id})
        data = {
            "nombre": "Item de prueba",
            "descripcion": "Descripción de prueba",
            "cantidad": 20,
            "valor": 1000.0,
            "solicitud": self.solicitud.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# TC-1201 PUT request to update an estado of a solicitud with valid ids
class UpdateEstadoSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.estado2 = Estado.objects.create(nombre='Aprobada')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_update_estado_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('estado-solicitud', kwargs={'pk_p': self.project.id, 'pk_s': self.solicitud.id, 'pk_e': self.estado.id})
        data = {
            "estado": self.estado2.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()


# TC-1202 PUT request to update an estado of a solicitud with invalid solicitud id
class UpdateInvalidEstadoSolicitudViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.estado2 = Estado.objects.create(nombre='Aprobada')

    def test_update_estado_solicitud(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('estado-solicitud', kwargs={'pk_p': 100, 'pk_s': 100, 'pk_e': self.estado.id})
        data = {
            "estado": self.estado2.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()


# TC-1203 PUT request to update an estado of a solicitud with no jwt token provided
class UpdateEstadoSolicitudWithoutTokenViewTest(APITestCase):
    def setUp(self):
        set_test_user(self)
        self.estado = Estado.objects.create(nombre='En revisión')
        self.estado2 = Estado.objects.create(nombre='Aprobada')
        self.project = Proyecto.objects.create(usuario_creacion=self.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
        self.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba',
                                                  tema='Probando',
                                                  tipo='Compra',
                                                  estado=self.estado,
                                                  proyecto=self.project,
                                                  usuario_creacion=self.user_profile,
                                                  usuario_modificacion=self.user_profile)

    def test_update_estado_solicitud(self):
        url = reverse('estado-solicitud', kwargs={'pk_p': self.project.id, 'pk_s': self.solicitud.id, 'pk_e': self.estado.id})
        data = {
            "estado": self.estado2.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
