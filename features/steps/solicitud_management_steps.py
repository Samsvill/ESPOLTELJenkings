from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from solicitud.models import Estado, Solicitud, Cotizacion
from proyecto.models import Proyecto
from base_cases import set_test_user

# Given steps
@given('I am a solicitudes test client')
def solicitudes_test_client(context):
    context.client = APIClient()

@given('I have a valid user setup with solicitud role')
def solicitudes_setup_with_user(context):
    set_test_user(context)
    context.estado = Estado.objects.create(nombre='En revisión')
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba', project_budget=10000)

@given('I have a solicitud setup with valid project and estado')
def solicitudes_setup_with_valid_project_and_estado(context):
    context.solicitud = Solicitud.objects.create(
        nombre='Solicitud de prueba',
        tema='Probando',
        tipo='Compra',
        estado=context.estado,
        proyecto=context.project,
        usuario_creacion=context.user_profile,
        usuario_modificacion=context.user_profile
    )

@given('I have a cotizacion setup with a non-existing ID')
def solicitudes_setup_with_invalid_cotizacion_id(context):
    context.invalid_cotizacion_id = 100

@given('I have a solicitud setup with an invalid project ID')
def solicitudes_setup_with_invalid_project_id(context):
    context.invalid_project_id = 999

# When steps
@when('I send a POST request to create a solicitud with {validity} data')
def solicitudes_create_with_validity(context, validity):
    if validity == "valid":
        context.data = {
            "nombre": "Solicitud de prueba",
            "tema": "Probando",
            "tipo": "Compra",
            "estado": context.estado.id,
            "proyecto": context.project.id
        }
        context.response = context.client.post(reverse('crear-solicitud', kwargs={'pk': context.project.id}), context.data, format='json')
    elif validity == "invalid":
        context.data = {
            "nombre": "Solicitud de prueba",
            "tema": "Probando",
            "tipo": "Compra",
            "estado": context.estado.id,
            "proyecto": context.invalid_project_id
        }
        context.response = context.client.post(reverse('crear-solicitud', kwargs={'pk': context.invalid_project_id}), context.data, format='json')

@when('I send a PUT request to update the solicitud with an invalid cotizacion ID')
def solicitudes_update_with_invalid_cotizacion_id(context):
    context.data = {
        "nombre": "Solicitud de prueba actualizada",
        "tema": "Probando actualización",
        "tipo": "Compra",
        "estado": context.estado.id,
        "proyecto": context.project.id,
        "cotizacion_aceptada": context.invalid_cotizacion_id
    }
    context.response = context.client.put(reverse('detalle-solicitud', kwargs={'pk': context.solicitud.id}), context.data, format='json')

@when('I send a POST request to create a solicitud without a token')
def solicitudes_create_without_token(context):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.data = {
        "nombre": "Solicitud de prueba",
        "tema": "Probando",
        "tipo": "Compra",
        "estado": context.estado.id,
        "proyecto": context.project.id
    }
    context.response = context.client.post(reverse('crear-solicitud', kwargs={'pk': context.project.id}), context.data, format='json')

@when('I send a PUT request to update the estado of a solicitud with {validity} IDs')
def solicitudes_update_estado_with_validity(context, validity):
    if validity == "valid":
        context.data = {
            "estado": context.estado.id
        }
        context.response = context.client.put(reverse('estado-solicitud', kwargs={
            'pk_p': context.project.id,
            'pk_s': context.solicitud.id,
            'pk_e': context.estado.id
        }), context.data, format='json')
    elif validity == "invalid":
        context.data = {
            "estado": context.estado.id
        }
        context.response = context.client.put(reverse('estado-solicitud', kwargs={
            'pk_p': context.invalid_project_id,
            'pk_s': context.invalid_project_id,
            'pk_e': context.estado.id
        }), context.data, format='json')

@when('I send a PUT request to update the estado of a solicitud without a token')
def solicitudes_update_estado_without_token(context):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.data = {
        "estado": context.estado.id
    }
    context.response = context.client.put(reverse('estado-solicitud', kwargs={
        'pk_p': context.project.id,
        'pk_s': context.solicitud.id,
        'pk_e': context.estado.id
    }), context.data, format='json')

# Then steps
@then('the response status should be {status_code} for solicitud {action}')
def solicitudes_verify_status_code(context, status_code, action):
    expected_status = {
        "creation": {
            "201": status.HTTP_201_CREATED,
            "404": status.HTTP_404_NOT_FOUND,
            "401": status.HTTP_401_UNAUTHORIZED
        },
        "update_estado": {
            "200": status.HTTP_200_OK,
            "404": status.HTTP_404_NOT_FOUND,
            "401": status.HTTP_401_UNAUTHORIZED
        }
    }
    assert context.response.status_code == expected_status[action][status_code]
