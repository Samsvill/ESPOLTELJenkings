from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

@given('I have the user registration API endpoint')
def step_impl(context):
    context.url = reverse('registro')

@when('I send a POST request to create a user with valid credentials')
def step_impl(context):
    context.data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@given('I have an existing user with the username "{username}"')
def step_impl(context, username):
    User.objects.create_user(username=username, password='Jq23%aS@')

@when('I send a POST request to create a user with the same username')
def step_impl(context):
    context.data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 400')
def step_impl(context):
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST

@given('I have valid user credentials')
def step_impl(context):
    User.objects.create_user(username='lcanarte', password='Jq23%aS@')
    context.url = reverse('get_token')

@when('I send a POST request to obtain a token')
def step_impl(context):
    context.data = {'username': 'lcanarte', 'password': 'Jq23%aS@'}
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 200')
def step_impl(context):
    assert context.response.status_code == status.HTTP_200_OK

@given('I have invalid user credentials')
def step_impl(context):
    User.objects.create_user(username='lcanarte', password='Jq23%aS@')
    context.url = reverse('get_token')

@when('I send a POST request to obtain a token with incorrect credentials')
def step_impl(context):
    context.data = {'username': 'lcanarte', 'password': 'wrongpassword'}
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 401')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED
