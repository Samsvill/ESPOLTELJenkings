from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from solicitud.models import Estado, Solicitud, Formulario
from proyecto.models import Proyecto
from base_cases import set_test_user

# Given steps
@given('I am a formulario test client')
def formulario_test_client(context):
    context.client = APIClient()

@given('I have a formulario setup with valid solicitud and project')
def formulario_setup_with_valid_solicitud_and_project(context):
    set_test_user(context)
    context.estado = Estado.objects.create(nombre='En revisión')
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba', project_budget=10000)
    context.solicitud = Solicitud.objects.create(nombre='Solicitud de prueba', tema='Probando', tipo='Compra',
                                                 estado=context.estado, proyecto=context.project,
                                                 usuario_creacion=context.user_profile, usuario_modificacion=context.user_profile)
    context.formulario_url = reverse('crear-formulario', kwargs={'pk_s': context.solicitud.id})

@given('I have a formulario setup with an invalid solicitud ID')
def formulario_setup_with_invalid_solicitud_id(context):
    context.invalid_formulario_url = reverse('crear-formulario', kwargs={'pk_s': 100})

# When steps
@when('I send a POST request to create a formulario with {validity} data')
def formulario_create_with_validity(context, validity):
    if validity == "valid":
        context.data = {
            "cedula_ruc": "0999999999",
            "descripcion": "Descripción de prueba",
            "solicitud": context.solicitud.id,
            "url_compra": "http://example.com/compra",
            "url_certi_banco": "http://example.com/certi_banco"
        }
        context.response = context.client.post(context.formulario_url, context.data, format='json')
    elif validity == "invalid":
        context.data = {
            "cedula_ruc": "0999999999",
            "descripcion": "Descripción de prueba",
            "url_compra": "http://example.com/compra",
            "url_certi_banco": "http://example.com/certi_banco"
        }
        context.response = context.client.post(context.invalid_formulario_url, context.data, format='json')

@when('I send a POST request to the formulario endpoint without a token')
def formulario_request_without_token(context):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.data = {
        "cedula_ruc": "0999999999",
        "descripcion": "Descripción de prueba",
        "solicitud": context.solicitud.id,
        "url_compra": "http://example.com/compra",
        "url_certi_banco": "http://example.com/certi_banco"
    }
    context.response = context.client.post(context.formulario_url, context.data, format='json')

# Then steps
@then('the response status should be {status_code} for formulario creation')
def formulario_verify_status_code(context, status_code):
    expected_status = {
        "201": status.HTTP_201_CREATED,
        "404": status.HTTP_404_NOT_FOUND,
        "401": status.HTTP_401_UNAUTHORIZED
    }
    assert context.response.status_code == expected_status[status_code]
