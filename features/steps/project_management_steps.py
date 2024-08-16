from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from proyecto.models import Proyecto
from user.models import Role, UserRole
from base_cases import set_test_user

# Given steps
@given('I am a proyecto test client')
def proyecto_test_client(context):
    context.client = APIClient()

@given('I have a valid user setup with project role')
def proyecto_setup_with_user_and_role(context):
    set_test_user(context)
    context.role = Role.objects.create(description='PM')
    context.user_role = UserRole.objects.create(user=context.user, role=context.role)

@given('I have a project setup with an existing name')
def proyecto_setup_with_existing_name(context):
    Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba', project_budget=10000)

# When steps
@when('I send a POST request to create a project with {validity} data')
def proyecto_create_with_validity(context, validity):
    if validity == "valid":
        context.data = {
            'nombre': 'Proyecto prueba nuevo',
            'project_budget': 12000,
            'budget_items': []
        }
        context.response = context.client.post(reverse('proyecto-list-create'), context.data, format='json')
    elif validity == "existing_name":
        context.data = {
            'nombre': 'Proyecto prueba',
            'project_budget': 10000,
            'budget_items': []
        }
        context.response = context.client.post(reverse('proyecto-list-create'), context.data, format='json')

@when('I send a POST request to create a project without a token')
def proyecto_create_without_token(context):
    context.client.credentials()  # Elimina el token para simular una solicitud no autenticada
    context.data = {
        'nombre': 'Proyecto prueba nuevo',
        'project_budget': 12000,
        'budget_items': []
    }
    context.response = context.client.post(reverse('proyecto-list-create'), context.data, format='json')

@when('I send a PUT request to update a project with {validity} data')
def proyecto_update_with_validity(context, validity):
    if validity == "valid":
        context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre='Proyecto prueba', project_budget=10000)
        context.data = {
            'nombre': 'Proyecto prueba actualizado',
            'project_budget': 15000,
            'budget_items': []
        }
        context.response = context.client.put(reverse('proyecto-detail', kwargs={'pk': context.project.id}), context.data, format='json')
    elif validity == "invalid_id":
        context.data = {
            'nombre': 'Proyecto prueba actualizado',
            'project_budget': 15000,
            'budget_items': []
        }
        context.response = context.client.put(reverse('proyecto-detail', kwargs={'pk': 999}), context.data, format='json')

# Then steps
@then('the response status should be {status_code} for project {action}')
def proyecto_verify_status_code(context, status_code, action):
    expected_status = {
        "creation": {
            "201": status.HTTP_201_CREATED,
            "400": status.HTTP_400_BAD_REQUEST,
            "401": status.HTTP_401_UNAUTHORIZED
        },
        "update": {
            "200": status.HTTP_200_OK,
            "404": status.HTTP_404_NOT_FOUND
        }
    }
    assert context.response.status_code == expected_status[action][status_code]
