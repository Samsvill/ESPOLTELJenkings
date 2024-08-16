from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from solicitud.models import Cotizacion

@given('I am an authenticated user with a valid token for cotizacion management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@when('I send a POST request to create a cotizacion with valid data')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
    context.data = {
        "proveedor": "Proveedor de prueba",
        "monto": 1000.0,
        "fecha_coti": "2021-06-01"
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201 for cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@when('I send a POST request to create a cotizacion with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': 100})
    context.data = {
        "proveedor": "Proveedor de prueba",
        "monto": 1000.0,
        "fecha_coti": "2021-06-01"
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 404 for cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a POST request to create a cotizacion without a token')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
    context.data = {
        "proveedor": "Proveedor de prueba",
        "monto": 1000.0,
        "fecha_coti": "2021-06-01",
        "solicitud": context.solicitud.id
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401 for cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED

@when('I send a DELETE request to delete a cotizacion with a valid solicitud ID')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id })
    context.response = context.client.delete(context.url)

@then('the response status should be 200 for delete cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_200_OK

@when('I send a DELETE request to delete a cotizacion with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': 100})
    context.response = context.client.delete(context.url)

@then('the response status should be 404 for delete cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a DELETE request to delete a cotizacion without a token')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
    context.response = context.client.delete(context.url)

@then('the response status should be 401 for delete cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
