from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

# Given step para inicializar el cliente de pruebas
@given('I am a test client')
def step_impl(context):
    context.client = APIClient()

# Given steps relacionados con usuarios
@given('I have the registration endpoint')
def step_impl(context):
    context.url = reverse('registro')

@given('A user already exists with the username {username}')
def step_impl(context, username):
    User.objects.filter(username=username).delete()
    User.objects.create_user(username=username, password='Jq23%aS@')

@given('A user exists with the username {username} and password {password}')
def step_impl(context, username, password):
    User.objects.filter(username=username).delete()
    User.objects.create_user(username=username, password=password)

@given('I have the token obtain endpoint')
def step_impl(context):
    context.url = reverse('get_token')

# When steps
@when('I send a POST request to create a user with valid data')
def step_impl(context):
    User.objects.filter(username='lcanarte').delete()
    context.data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to create a user with the same username')
def step_impl(context):
    User.objects.create_user(username='lcanarte', password='Jq23%aS@')
    context.data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to obtain a token with valid credentials')
def step_impl(context):
    User.objects.create_user(username='lcanarte', password='Jq23%aS@')
    context.data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
    context.response = context.client.post(context.url, context.data, format='json')

@when('I send a POST request to obtain a token with invalid credentials')
def step_impl(context):
    context.data = {'username': 'lcanarte', 'password': 'incorrect_password'}
    context.response = context.client.post(context.url, context.data, format='json')

# Then steps
@then('the response status should be 201 for user creation')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@then('the response status should be 400 for user creation')
def step_impl(context):
    print(f"Response status code: {context.response.status_code}")
    print(f"Response content: {context.response.content}")
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST

@then('the response status should be 200 for token obtainment')
def step_impl(context):
    print(f"Response status code: {context.response.status_code}")
    print(f"Response content: {context.response.content}")
    assert context.response.status_code == status.HTTP_200_OK

@then('the response status should be 401 for token obtainment')
def step_impl(context):
    print(f"Response status code: {context.response.status_code}")
    print(f"Response content: {context.response.content}")
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED

