from django.test import TestCase

# Create your tests here.
from distutils.log import error
from django.test import TestCase, Client
from django.urls import reverse, resolve

from .views import signupfunc


class TestSignUpView(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'admin'
        self.password = 'admin'

    def login(self):
        self.client.login(username=self.username, password = self.password)
        
    def logout(self):
        self.client.logout(username=self.username, password = self.password)
        
        