from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from proyecto.models import Proyecto
from solicitud.models import Solicitud, Estado

@given('I am an authenticated user with a valid token for solicitud management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@given('I have a project with ID {project_id} and an estado with ID {estado_id}')
def step_impl(context, project_id, estado_id):
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba',
                                              project_budget=10000)
    context.estado = Estado.objects.create(nombre='En revisión')

@when('I send a POST request to create a solicitud with valid data')
def step_impl(context):
    context.url = reverse('crear-solicitud', kwargs={'pk': context.project.id})
    context.data = {
        "nombre": "Solicitud de prueba",
        "tema": "Probando",
        "tipo": "Compra",
        "estado": context.estado.id,
        "proyecto": context.project.id
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@when('I send a POST request to create a solicitud with an invalid project ID')
def step_impl(context):
    context.url = reverse('crear-solicitud', kwargs={'pk': 100})
    context.data = {
        "nombre": "Solicitud de prueba",
        "tema": "Probando",
        "tipo": "Compra",
        "estado": context.estado.id,
        "proyecto": 10
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 404')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a PUT request to update the solicitud with an invalid cotizacion ID')
def step_impl(context):
    context.url = reverse('detalle-solicitud', kwargs={'pk': context.solicitud.id})
    context.data = {
        "nombre": "Solicitud de prueba",
        "tema": "Probando",
        "tipo": "Compra",
        "estado": context.estado.id,
        "proyecto": context.project.id,
        "cotizacion_aceptada": 100
    }
    context.response = context.client.put(context.url, context.data, format='json')

@then('the response status should be 404 for invalid cotizacion')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@when('I send a POST request to create a solicitud without a token')
def step_impl(context):
    context.url = reverse('crear-solicitud', kwargs={'pk': context.project.id})
    context.data = {
        "nombre": "Solicitud de prueba",
        "tema": "Probando",
        "tipo": "Compra",
        "estado": context.estado.id,
        "proyecto": context.project.id
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401 for solicitud')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
