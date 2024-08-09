from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from user.models import UserProfile, Role, UserRole

def set_test_user(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.user_profile = UserProfile.objects.create(
        user=self.user,
        email='test@test.com',
        name='Test User',
        cedula='12345',
        is_active=True
    )
    refresh = RefreshToken.for_user(self.user)
    self.access_token = str(refresh.access_token)


def set_pm_user(self):
    self.user = User.objects.create_user(username='PM', password='PM')
    self.user_profile = UserProfile.objects.create(
        user=self.user,
        email='pm@pm.com',
        name='Director de Proyecto Test',
        cedula='12345',
        is_active=True
    )
    self.role = Role.objects.create(name='Director de Proyecto')
    refresh = RefreshToken.for_user(self.user)
    self.access_token = str(refresh.access_token)

def set_adq_user(self):
    self.user = User.objects.create_user(username='ADQ', password='ADQ')
    self.user_profile = UserProfile.objects.create(
        user=self.user,
        email= 'adq@ad.com',
        name='Director de Adquisiciones Test',
        cedula='12345',
        is_active=True
    )
    refresh = RefreshToken.for_user(self.user)
    self.access_token = str(refresh.access_token)