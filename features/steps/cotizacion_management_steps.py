from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from solicitud.models import Estado, Solicitud, Cotizacion
from proyecto.models import Proyecto
from base_cases import set_test_user

# Given steps
@given('I am an authenticated user with a valid token for cotizacion management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@given('I have a valid solicitud and project setup')
def step_impl(context):
    context.estado = Estado.objects.create(nombre='En revisión')
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba',
                                               project_budget=10000)
    context.solicitud = Solicitud.objects.create(
        nombre='Solicitud de prueba',
        tema='Probando',
        tipo='Compra',
        estado=context.estado,
        proyecto=context.project,
        usuario_creacion=context.user_profile,
        usuario_modificacion=context.user_profile
    )

# When steps
@when('I send a POST request to create a cotizacion with valid data')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
    context.data = {
        "proveedor": "Proveedor de prueba",
        "monto": 1000.0,
        "fecha_coti": "01-06-2021",
    }
    context.response = context.client.post(context.url, context.data, format='json')

# Then steps
@then('the response status should be 201 for cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@when('I send a POST request to create a cotizacion with an invalid solicitud ID')
def step_impl(context):
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': 100})
    context.data = {
        "proveedor": "Proveedor de prueba",
        "monto": 1000.0,
        "fecha_coti": "01-06-2021"
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 404 for cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a POST request to create a cotizacion without a token')
def step_impl(context):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
    context.data = {
        "proveedor": "Proveedor de prueba",
        "monto": 1000.0,
        "fecha_coti": "01-06-2021",
        "solicitud": context.solicitud.id
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401 for cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED

@when('I send a DELETE request to delete a cotizacion with a valid solicitud ID')
def step_impl(context):
    context.cotizacion = Cotizacion.objects.create(
        proveedor='Proveedor de prueba',
        monto=1000.0,
        solicitud=context.solicitud,
        fecha_coti='2021-06-01'
    )
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
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
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.cotizacion = Cotizacion.objects.create(
        proveedor='Proveedor de prueba',
        monto=1000.0,
        solicitud=context.solicitud,
        fecha_coti='2021-06-01'
    )
    context.url = reverse('cotizaciones-solicitud', kwargs={'pk': context.solicitud.id})
    context.response = context.client.delete(context.url)

@then('the response status should be 401 for delete cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
