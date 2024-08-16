from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from solicitud.models import Estado, Solicitud, Factura
from proyecto.models import Proyecto
from base_cases import set_test_user

# Given steps
@given('I am a factura test client')
def factura_test_client(context):
    context.client = APIClient()

@given('I have a factura setup with valid solicitud and project')
def factura_setup_with_valid_solicitud_and_project(context):
    set_test_user(context)
    context.estado = Estado.objects.create(nombre='En revisión')
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba', project_budget=10000)
    context.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba', tema='Probando', tipo='Compra',
                                                 estado=context.estado, proyecto=context.project,
                                                 usuario_creacion=context.user_profile, usuario_modificacion=context.user_profile)
    context.factura_url = reverse('crear-detalle-factura', kwargs={'pk_s': context.solicitud.id})

@given('I have an existing factura setup')
def factura_existing_factura_setup(context):
    context.factura = Factura.objects.create(solicitud=context.solicitud, estado="En revisión", monto=1000.0)

@given('I have a factura setup with an invalid solicitud ID')
def factura_setup_with_invalid_solicitud_id(context):
    context.invalid_factura_url = reverse('crear-detalle-factura', kwargs={'pk_s': 100})

# When steps
@when('I send a POST request to create a factura with {validity} data')
def factura_create_with_validity(context, validity):
    if validity == "valid":
        context.data = {"estado": "Estado de prueba", "monto": 1000.00000}
        context.response = context.client.post(context.factura_url, context.data, format='json')
    elif validity == "invalid":
        context.data = {"estado": "Estado de prueba", "monto": 1000.00000}
        context.response = context.client.post(context.invalid_factura_url, context.data, format='json')

@when('I send a PUT request to update the factura with {validity} data')
def factura_update_with_validity(context, validity):
    if validity == "valid":
        context.data = {"estado": "Estado de prueba actualizado", "monto": 1500.00000}
        context.response = context.client.put(context.factura_url, context.data, format='json')
    elif validity == "invalid":
        context.data = {"estado": "Estado de prueba actualizado", "monto": 1500.00000}
        context.response = context.client.put(context.invalid_factura_url, context.data, format='json')

@when('I send a {method} request to the factura endpoint without a token')
def factura_request_without_token(context, method):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    if method == "POST":
        context.data = {"estado": "Estado de prueba", "monto": 1000.00000}
        context.response = context.client.post(context.factura_url, context.data, format='json')
    elif method == "PUT":
        context.data = {"estado": "Estado de prueba actualizado", "monto": 1500.00000}
        context.response = context.client.put(context.factura_url, context.data, format='json')

# Then steps
@then('the response status should be {status_code} for factura {action}')
def factura_verify_status_code(context, status_code, action):
    expected_status = {
        "creation": {
            "201": status.HTTP_201_CREATED,
            "404": status.HTTP_404_NOT_FOUND,
            "401": status.HTTP_401_UNAUTHORIZED
        },
        "update": {
            "200": status.HTTP_200_OK,
            "404": status.HTTP_404_NOT_FOUND,
            "401": status.HTTP_401_UNAUTHORIZED
        }
    }
    assert context.response.status_code == expected_status[action][status_code]
