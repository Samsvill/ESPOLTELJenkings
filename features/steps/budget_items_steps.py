from behave import given, when, then
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from user.models import UserProfile
from proyecto.models import Proyecto

from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status

from base_cases import set_test_user


# Given steps
@given('I am an authenticated user with a valid token for budget item management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)


@given('I have a project with ID {project_id}')
def step_impl(context, project_id):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba',
                                              project_budget=10000)

# When steps
@when('I send a POST request to create a budget item with valid data')
def step_impl(context):
    context.url = reverse('crear-budget-items', kwargs={'proyecto_id': context.project.id})
    context.data = {
        "recurso": "Recurso Actualizado",
        "categoria": "Categoría Actualizada",
        "cantidad": 20,
        "valor": 150.0,
        "presupuesto": 3000.0
    }
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to create multiple budget items')
def step_impl(context):
    context.url = reverse('crear-budget-items', kwargs={'proyecto_id': context.project.id})
    context.data = {
        "budget_items": [
            {
                "recurso": "Recurso 1",
                "categoria": "Categoría 1",
                "cantidad": 20,
                "valor": 150.0,
                "presupuesto": 3000.0
            },
            {
                "recurso": "Recurso 2",
                "categoria": "Categoría 2",
                "cantidad": 30,
                "valor": 250.0,
                "presupuesto": 7500.0
            }
        ]
    }
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to create a budget item with an invalid project ID')
def step_impl(context):
    context.url = reverse('crear-budget-items', kwargs={'proyecto_id': 100})
    context.data = {}
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to create a budget item without a name')
def step_impl(context):
    context.url = reverse('crear-budget-items', kwargs={'proyecto_id': context.project.id})
    context.data = {
        "budget_items": [
            {
                "recurso": "",
                "categoria": "Categoría Actualizada",
                "cantidad": 20,
                "valor": 150.0,
                "presupuesto": 3000.0
            }
        ]
    }
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to create a budget item without a token')
def step_impl(context):
    # No setting token in the request
    context.client.credentials()  # Remove the token
    context.url = reverse('crear-budget-items', kwargs={'proyecto_id': context.project.id})
    context.data = {
        "budget_items": [
            {
                "recurso": "Recurso Actualizado",
                "categoria": "Categoría Actualizada",
                "cantidad": 20,
                "valor": 150.0,
                "presupuesto": 3000.0
            }
        ]
    }
    context.response = context.client.post(context.url, context.data, format='json')

# Then steps
@then('the response status should be 201 for budget item')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@then('the response status should be 404 for budget item')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@then('the response status should be 400 for budget item')
def step_impl(context):
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST

@then('the response status should be 401 for budget item')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
