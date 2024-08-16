from behave import given, when, then
from django.urls import reverse
from rest_framework import status
from user.models import Role


@given('I am an authenticated user with a valid token')
def step_impl(context):
    set_test_user(context)
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

@when('I send a POST request to create a new role')
def step_impl(context):
    context.url = reverse('roles')
    context.data = {'description': 'PM'}
    context.response = context.client.post(context.url, context.data, format='json')

@then('the response status should be 201')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@given('I have an existing role with description "{description}"')
def step_impl(context, description):
    context.role = Role.objects.create(description=description)

@when('I send a DELETE request to delete the role')
def step_impl(context):
    context.url = reverse('roles-delete', kwargs={'pk': context.role.id})
    context.response = context.client.delete(context.url)

@then('the response status should be 204')
def step_impl(context):
    assert context.response.status_code == status.HTTP_204_NO_CONTENT

@given('there is no role with id {role_id}')
def step_impl(context, role_id):
    # Assuming role_id doesn't exist
    context.role_id = role_id

@when('I send a DELETE request to delete the role with non-existing id')
def step_impl(context):
    context.url = reverse('roles-delete', kwargs={'pk': context.role_id})
    context.response = context.client.delete(context.url)

@then('the response status should be 404')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND
