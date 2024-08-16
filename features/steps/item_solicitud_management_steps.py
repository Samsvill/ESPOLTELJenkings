from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from solicitud.models import Estado, Solicitud, ItemSolicitud
from proyecto.models import Proyecto
from base_cases import set_test_user

# Given steps
@given('I am an itemsolicitud test client')
def itemsolicitud_test_client(context):
    context.client = APIClient()

@given('I have an itemsolicitud setup with valid solicitud and project')
def itemsolicitud_setup_with_valid_solicitud_and_project(context):
    set_test_user(context)
    context.estado = Estado.objects.create(nombre='En revisión')
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba', project_budget=10000)
    context.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba', tema='Probando', tipo='Compra',
                                                 estado=context.estado, proyecto=context.project,
                                                 usuario_creacion=context.user_profile, usuario_modificacion=context.user_profile)
    context.itemsolicitud_url = reverse('crear-items-solicitud', kwargs={'pk_s': context.solicitud.id})

@given('I have an itemsolicitud setup with an invalid solicitud ID')
def itemsolicitud_setup_with_invalid_solicitud_id(context):
    context.invalid_itemsolicitud_url = reverse('crear-items-solicitud', kwargs={'pk_s': 100})

# When steps
@when('I send a POST request to create an itemsolicitud with {validity} data')
def itemsolicitud_create_with_validity(context, validity):
    if validity == "valid":
        context.data = {
            "nombre": "Item de prueba",
            "descripcion": "Descripción de prueba",
            "cantidad": 20,
            "valor": 1000.0,
            "solicitud": context.solicitud.id
        }
        context.response = context.client.post(context.itemsolicitud_url, context.data, format='json')
    elif validity == "invalid":
        context.data = {
            "nombre": "Item de prueba",
            "descripcion": "Descripción de prueba",
            "cantidad": 20,
            "valor": 1000.0,
            "solicitud": 100
        }
        context.response = context.client.post(context.invalid_itemsolicitud_url, context.data, format='json')

@when('I send a POST request to the itemsolicitud endpoint without a token')
def itemsolicitud_request_without_token(context):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.data = {
        "nombre": "Item de prueba",
        "descripcion": "Descripción de prueba",
        "cantidad": 20,
        "valor": 1000.0,
        "solicitud": context.solicitud.id
    }
    context.response = context.client.post(context.itemsolicitud_url, context.data, format='json')

# Then steps
@then('the response status should be {status_code} for itemsolicitud creation')
def itemsolicitud_verify_status_code(context, status_code):
    expected_status = {
        "201": status.HTTP_201_CREATED,
        "404": status.HTTP_404_NOT_FOUND,
        "401": status.HTTP_401_UNAUTHORIZED
    }
    assert context.response.status_code == expected_status[status_code]
