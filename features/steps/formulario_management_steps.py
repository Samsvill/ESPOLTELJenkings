from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from solicitud.models import Formulario

@given('I am an authenticated user with a valid token for formulario management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@when('I send a POST request to create a formulario with valid data')
def step_impl(context):
    context.url = reverse('crear-formulario', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "cedula_ruc": "0999999999",
        "descripcion": "Descripción de prueba",
        "solicitud": context.solicitud.id,
        "url_compra": "http://example.com/compra",
        "url_certi_banco": "http://example.com/certi_banco"
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201 for formulario')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@when('I send a POST request to create a formulario with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('crear-formulario', kwargs={'pk_s': 100})
    context.data = {
        "descripcion": "Descripción de prueba",
        "url_compra": "http://example.com/compra",
        "url_certi_banco": "http://example.com/certi_banco"
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 404 for formulario')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a POST request to create a formulario without a token')
def step_impl(context):
    context.url = reverse('crear-formulario', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "cedula_ruc": "0999999999",
        "descripcion": "Descripción de prueba",
        "solicitud": context.solicitud.id,
        "url_compra": "http://example.com/compra",
        "url_certi_banco": "http://example.com/certi_banco"
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401 for formulario')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
