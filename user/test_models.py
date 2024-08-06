from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import UserProfile, Role, UserRole


class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user_profile = UserProfile.objects.create(user=user,
                                        email='test@test.com',
                                        name='Test User',
                                        cedula='12345',
                                        is_active=True)
        self.assertEqual(user_profile.user.username, 'testuser')
        self.assertEqual(user_profile.email, "test@test.com")
        self.assertEqual(user_profile.name, "Test User")
        self.assertEqual(user_profile.cedula, "12345")
        self.assertEqual(user_profile.is_active, True)

class RoleModelTest(TestCase):
    def test_role_creation(self):
        role = Role.objects.create(description="Test Role")
        self.assertEqual(role.description, "Test Role")

class UserRoleModelTest(TestCase):
    def test_user_role_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        role = Role.objects.create(description="Test Role")
        user_role = UserRole.objects.create(user=user, role=role)
        self.assertEqual(user_role.user.username, 'testuser')
        self.assertEqual(user_role.role.description, "Test Role")

