from django.test import TestCase
from django.contrib.auth.models import User
from user.models import UserProfile, UserRole, Role
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTest(TestCase):
    @classmethod
    def setUp(self):
        self.PMuser = User.objects.create_user(username='testPMuser', password='12345')
        self.PMuser_profile = UserProfile.objects.create(user=self.PMuser,
                                        email='test@test.com',
                                        name='Test PM User',
                                        cedula='12345',
                                        is_active=True)
        self.PMrole = Role.objects.create(description='PM')
        self.PMuser_role = UserRole.objects.create(user=self.PMuser, role=self.PMrole)

        self.ADQuser = User.objects.create_user(username='testADQuser', password='12345')
        self.ADQuser_profile = UserProfile.objects.create(user=self.ADQuser,
                                                          email='test@test.com',
                                                          name='Test PM User',
                                                          cedula='12345',
                                                          is_active=True)
        self.ADQrole = Role.objects.create(description='ADQ')
        self.ADQuser_role = UserRole.objects.create(user=self.ADQuser, role=self.ADQrole)

    #@classmethod
    #def tearDown(self):
    #    User.objects.all().delete()
    #    UserProfile.objects.all().delete()
    #    UserRole.objects.all().delete()
    #    Role.objects.all().delete()
    #    post_save.disconnect(UserProfile.create_user_profile, sender=User)
