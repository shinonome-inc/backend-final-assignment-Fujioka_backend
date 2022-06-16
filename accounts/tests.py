from distutils.log import error
import turtle
from urllib import response
from webbrowser import get
from django.test import TestCase, Client
from django.urls import reverse, resolve
import pprint

from welcome.views import loginfunc

from .models import User
from .views import signupfunc


class TestSignUpView(TestCase):
    def setUp(self):
        self.client = Client()
        self.next_url = reverse('tweets:test')
        self.signup_url = reverse('accounts:signup')
        self.username = 'testsurutarou'
        self.password = 'watasihatestpassworddesu'

    def test_success_get(self):
        self.assertEqual(resolve(self.signup_url).func, signupfunc)
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_failure_post_with_empty_form(self):
        context = {}
        self.response = self.client.post(self.signup_url, context)
        self.assertEquals(self.response.status_code, 200)

        form = self.response.context.get('form')
        self.assertIsNotNone(form.errors.get('username'))
        self.assertIsNotNone(form.errors.get('password1'))
        self.assertIsNotNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_username(self):
        context = {
            'username': '',
            'password1': self.password,
            'password2': self.password,
        }
        self.response = self.client.post(self.signup_url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        self.assertIsNotNone(form.errors.get('username'))
        self.assertIsNone(form.errors.get('password1'))
        self.assertIsNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_email(self):
        pass

    def test_failure_post_with_empty_password(self):
        context = {
            'username': self.username,
            'password1': '',
            'password2': '',
        }
        self.response = self.client.post(self.signup_url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        self.assertIsNone(form.errors.get('username'))
        self.assertIsNotNone(form.errors.get('password1'))
        self.assertIsNotNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_duplicated_user(self):
        pass

    def test_failure_post_with_invalid_email(self):
        pass

    def test_failure_post_with_too_short_password(self):
        context = {
            'username': self.username,
            'password1': 'aa',
            'password2': 'aa',
        }
        self.response = self.client.post(self.signup_url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        self.assertIsNone(form.errors.get('username'))
        self.assertIsNone(form.errors.get('password1'))
        self.assertIsNotNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_password_similar_to_username(self):
        url = reverse('accounts:signup')
        context = {
            'username': self.username,
            'password1': self.username,
            'password2': self.username,
        }
        self.response = self.client.post(url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        self.assertIsNone(form.errors.get('username'))
        self.assertIsNone(form.errors.get('password1'))
        self.assertIsNotNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_only_numbers_password(self):
        url = reverse('accounts:signup')
        context = {
            'username': '11111111',
            'password1': '11111111',
            'password2': '11111111',
        }
        self.response = self.client.post(url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        self.assertIsNone(form.errors.get('username'))
        self.assertIsNone(form.errors.get('password1'))
        self.assertIsNotNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_mismatch_password(self):
        url = reverse('accounts:signup')
        context = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password+'AAA',
        }
        self.response = self.client.post(url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        self.assertIsNone(form.errors.get('username'))
        self.assertIsNone(form.errors.get('password1'))
        self.assertIsNotNone(form.errors.get('password2'))
        self.assertFalse(User.objects.exists())

    def test_success_post(self):
        corres = self.client.post(self.signup_url, {
            'username': self.username, 'password1': self.password, 'password2': self.password})
        self.assertTrue(User.objects.exists())
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(corres.status_code, 302)


class TestHomeView(TestCase):
    def test_success_get(self):
        pass


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('welcome:login')
        self.signup_url = reverse('accounts:signup')
        self.redirect_url = reverse('tweets:test')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.credentials = {
            'username': self.username,
            'password': self.password}
        self.client.post(self.signup_url, {
            'username': self.username, 'password1': self.password, 'password2': self.password})

    def test_success_get(self):
        self.assertEqual(resolve(self.login_url).func, loginfunc)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome/login.html')

    def test_success_post(self):
        login_response = self.client.post(self.login_url, self.credentials)
        self.assertEqual(login_response.status_code, 302)
        self.assertEqual(login_response.url, self.redirect_url)
        login_response = self.client.login(
            username=self.username, password=self.password)
        self.assertTrue(login_response)

    def test_failure_post_with_not_exists_user(self):
        login_response = self.client.login(
            username=self.username, password=self.password+'AAA')
        self.assertEqual(login_response, False)

        login_response = self.client.post(
            self.login_url, {'username': self.username+'A', 'password': self.password})
        self.assertEqual(login_response.context.get(
            'error'), 'This user is not exitst. Please try anothor name or passwrod.')

    def test_failure_post_with_empty_password(self):
        login_response = self.client.login(
            username=self.username, password=self.password+'AAA')
        self.assertEqual(login_response, False)

        login_response = self.client.post(
            self.login_url, {'username': self.username+'A', 'password': self.password})
        self.assertEqual(login_response.context.get(
            'error'), 'This user is not exitst. Please try anothor name or passwrod.')


class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('welcome:login')
        self.logout_url = reverse('welcome:logout')
        self.signup_url = reverse('accounts:signup')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.client.post(self.signup_url, {
            'username': self.username, 'password1': self.password, 'password2': self.password})

    def test_success_get(self):
        login_response = self.client.login(
            username=self.username, password=self.password)

        self.assertEqual(login_response, True)
        logout_response = self.client.get(self.logout_url)
        self.assertEqual(logout_response.status_code, 302)
        self.assertEqual(logout_response.url, self.login_url)


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
