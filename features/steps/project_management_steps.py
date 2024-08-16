from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from proyecto.models import Proyecto

@given('I am an authenticated user with a valid token for project management')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@when('I send a POST request to create a new project with valid data')
def step_impl(context):
    context.url = reverse('proyecto-list-create')
    context.data = {
        'nombre': 'Proyecto prueba',
        'project_budget': 10000,
        'budget_items': []
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@given('I have an existing project with the name "{project_name}"')
def step_impl(context, project_name):
    context.project = Proyecto.objects.create(usuario_creacion=context.user_profile, nombre=project_name,
                                              project_budget=10000)

@when('I send a POST request to create a project with the same name')
def step_impl(context):
    context.url = reverse('proyecto-list-create')
    context.data = {
        'nombre': context.project.nombre,
        'project_budget': 10000,
        'budget_items': []
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 400')
def step_impl(context):
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST

@when('I send a POST request to create a new project')
def step_impl(context):
    context.url = reverse('proyecto-list-create')
    context.data = {
        'nombre': 'Proyecto prueba',
        'project_budget': 10000,
        'budget_items': []
    }
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED

@when('I send a PUT request to update the project')
def step_impl(context):
    context.url = reverse('proyecto-detail', kwargs={'pk': context.project.id})
    context.data = {
        'nombre': 'Proyecto prueba, nuevo',
        'project_budget': 12000,
        'budget_items': []
    }
    context.response = context.client.put(context.url, context.data, format='json')

@then('the response status should be 200')
def step_impl(context):
    assert context.response.status_code == status.HTTP_200_OK

@when('I send a PUT request to update the project with an invalid ID')
def step_impl(context):
    context.url = reverse('proyecto-detail', kwargs={'pk': 100})
    context.data = {
        'nombre': 'Proyecto prueba, nuevo',
        'project_budget': 12000,
        'budget_items': []
    }
    context.response = context.client.put(context.url, context.data, format='json')

@then('the response status should be 404')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND
