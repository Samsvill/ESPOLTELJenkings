from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from solicitud.models import Factura

@given('I am an authenticated user with a valid token for factura management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@when('I send a POST request to create a factura with valid data')
def step_impl(context):
    context.url = reverse('crear-detalle-factura', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "estado": "Estado de prueba",
        "monto": 1000.00000
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201 for factura')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@when('I send a POST request to create a factura with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('crear-detalle-factura', kwargs={'pk_s': 100})
    context.data = {
        "estado": "Estado de prueba",
        "monto": 1000.00000
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 404 for factura')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a POST request to create a factura without a token')
def step_impl(context):
    context.url = reverse('crear-detalle-factura', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "estado": "Estado de prueba",
        "monto": 1000.00000
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401 for factura')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED

@when('I send a PUT request to update a factura with valid data')
def step_impl(context):
    context.url = reverse('crear-detalle-factura', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "estado": "Estado de prueba",
        "monto": 1000.00000
    }
    context.response = context.client.put(context.url, context.data, format='json')

@then('the response status should be 200 for factura')
def step_impl(context):
    assert context.response.status_code == status.HTTP_200_OK

@when('I send a PUT request to update a factura with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('crear-detalle-factura', kwargs={'pk_s': 100})
    context.data = {
        "estado": "Estado de prueba",
        "monto": 1000.00000
    }
    context.response = context.client.put(context.url, context.data, format='json')

@then('the response status should be 404 for factura')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a PUT request to update a factura without a token')
def step_impl(context):
    context.url = reverse('crear-detalle-factura', kwargs={'pk_s': context.solicitud.id})
    context.data = {
        "estado": "Estado de prueba",
        "monto": 1000.00000
    }
    context.response = context.client.put(context.url, context.data, format='json')

@then('the response status should be 401 for factura')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
