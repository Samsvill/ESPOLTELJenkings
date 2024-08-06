from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from proyecto.models import Proyecto, BudgetItem

from rest_framework_simplejwt.tokens import RefreshToken

from . import base_scenario
#aqui se testea la creacion de un proyecto, pero con el usuario PM que es el unico que puede crear proyectos
#con el usuario PM creado en base_scenario.py
class CreateProyectoViewTest(APITestCase):
    def test_create_proyecto(self):
        refresh = RefreshToken.for_user(base_scenario.PMuser)
        self.access_tokenPM = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        url = reverse('crear-proyecto')
        data = {'nombre': 'Proyecto de Prueba', 'project_budget': 100000}
        self.client.force_authenticate(user=base_scenario.PMuser)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proyecto.objects.count(), 1)
        self.assertEqual(Proyecto.objects.get().nombre, 'Proyecto de Prueba')
        self.assertEqual(Proyecto.objects.get().project_budget, 100000)

        self.client.credentials()
        

#se testea la creacion de un Budget item, con el usuario PM
class CreateBudgetItemViewTest(APITestCase):
    def test_create_budget_item(self):
        refresh = RefreshToken.for_user(base_scenario.PMuser)
        self.access_tokenPM = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        proyecto = Proyecto.objects.create(nombre='Proyecto de Prueba', project_budget=100000)
        url = reverse('crear-budget-item', kwargs={'pk': proyecto.id})
        data = {'recurso': 'Hormigon', 'categoria': 'Materiales', 'cantidad': 10, 'valor': 1000}
        self.client.force_authenticate(user=base_scenario.PMuser)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BudgetItem.objects.count(), 1)
        self.assertEqual(BudgetItem.objects.get().recurso, 'Hormigon')
        self.assertEqual(BudgetItem.objects.get().categoria, 'Materiales')
        self.assertEqual(BudgetItem.objects.get().cantidad, 10)
        self.assertEqual(BudgetItem.objects.get().valor, 1000)

        self.client.credentials()


