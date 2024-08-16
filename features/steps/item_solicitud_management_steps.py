from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from solicitud.models import ItemSolicitud

@given('I am an authenticated user with a valid token for item solicitud management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@when('I send a POST request to create an item solicitud with valid data')
def step_impl(context):
    context.url = reverse('crear-items-solicitud', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "nombre": "Item de prueba",
        "descripcion": "Descripción de prueba",
        "cantidad": 20,
        "valor": 1000.0,
        "solicitud": context.solicitud.id
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201 for item solicitud')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@when('I send a POST request to create an item solicitud with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('crear-items-solicitud', kwargs={'pk_s': 100})
    context.data = {
        "nombre": "Item de prueba",
        "descripcion": "Descripción de prueba",
        "cantidad": 20,
        "valor": 1000.0,
        "solicitud": 100
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 404 for item solicitud')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a POST request to create an item solicitud without a token')
def step_impl(context):
    context.url = reverse('crear-items-solicitud', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "nombre": "Item de prueba",
        "descripcion": "Descripción de prueba",
        "cantidad": 20,
        "valor": 1000.0,
        "solicitud": context.solicitud.id
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401 for item solicitud')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
