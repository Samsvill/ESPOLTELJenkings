from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Solicitud, Estado, Cotizacion, Formulario

# Create your tests here.
class SolicitudTests(APITestCase):
    def test_create_solicitud(self):
        soli = Solicitud.objects.create(nombre='Test Solicitud', descripcion='Test Description')
        self.assertEqual(soli.nombre, 'Test Solicitud')
        self.assertEqual(soli.descripcion, 'Test Description')
        