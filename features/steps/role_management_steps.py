from behave import given, when, then
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from user.models import Role, UserRole
from base_cases import set_test_user

# Given steps
@given('I am a roles test client')
def roles_test_client(context):
    context.client = APIClient()

@given('I have a valid user setup for roles')
def roles_setup_with_valid_user(context):
    set_test_user(context)

@given('I have a role setup with an existing role')
def roles_setup_with_existing_role(context):
    context.role = Role.objects.create(description='PM')
    UserRole.objects.create(user=context.user, role=context.role)

# When steps
@when('I send a POST request to create a role with valid data')
def roles_create_with_valid_data(context):
    context.data = {'description': 'PM'}
    context.response = context.client.post(reverse('roles'), context.data, format='json')

@when('I send a DELETE request to delete an existing role')
def roles_delete_existing(context):
    context.response = context.client.delete(reverse('roles-delete', kwargs={'pk': context.role.id}))

@when('I send a DELETE request to delete a non-existing role')
def roles_delete_non_existing(context):
    context.response = context.client.delete(reverse('roles-delete', kwargs={'pk': 100}))

# Then steps
@then('the response status should be {status_code} for role {action}')
def roles_verify_status_code(context, status_code, action):
    expected_status = {
        "creation": {
            "201": status.HTTP_201_CREATED
        },
        "deletion": {
            "204": status.HTTP_204_NO_CONTENT,
            "404": status.HTTP_404_NOT_FOUND
        }
    }
    assert context.response.status_code == expected_status[action][status_code]
