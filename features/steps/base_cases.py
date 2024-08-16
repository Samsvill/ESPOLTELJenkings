from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserProfile

def set_test_user(context):
    # Eliminar el usuario existente si ya existe
    User.objects.filter(username='testuser').delete()

    # Crear un nuevo usuario de prueba
    context.user = User.objects.create_user(username='testuser', password='12345')
    
    # Crear el perfil de usuario
    context.user_profile = UserProfile.objects.create(
        user=context.user,
        email='test@test.com',
        name='Test User',
        cedula='12345',
        is_active=True
    )
    
    # Generar un token JWT para autenticación
    refresh = RefreshToken.for_user(context.user)
    context.access_token = str(refresh.access_token)
    
    # Configurar el cliente de API con el token de autenticación
    context.client = APIClient()
    context.client.credentials(HTTP_AUTHORIZATION='Bearer ' + context.access_token)

def set_pm_user(context):
    context.user = User.objects.create_user(username='PM', password='PM')
    context.user_profile = UserProfile.objects.create(
        user=context.user,
        email='pm@pm.com',
        name='Director de Proyecto Test',
        cedula='12345',
        is_active=True
    )
    context.role = Role.objects.create(description='Director de Proyecto')
    refresh = RefreshToken.for_user(context.user)
    context.access_token = str(refresh.access_token)

def set_adq_user(context):
    context.user = User.objects.create_user(username='ADQ', password='ADQ')
    context.user_profile = UserProfile.objects.create(
        user=context.user,
        email='adq@ad.com',
        name='Director de Adquisiciones Test',
        cedula='12345',
        is_active=True
    )
    refresh = RefreshToken.for_user(context.user)
    context.access_token = str(refresh.access_token)
