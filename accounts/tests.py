from distutils.log import error
from django.test import TestCase, Client
from django.urls import reverse, resolve

from .models import User
from .views import signupfunc


class TestSignUpView(TestCase):
    def setUp(self):
        self.client = Client()
        self.next_url = reverse('tweets:test')
        self.signup_url = reverse('accounts:signup')
        self.username = 'testsurutarou'
        self.password = 'watasihatestpassworddesu'
        self.corres = self.client.post(self.signup_url, {
                                       'username': self.username, 'password1': self.password, 'password2': self.password})

    def test_success_get(self):
        self.assertEqual(resolve(self.signup_url).func, signupfunc)
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'accounts.signup.html')

    def test_success_post(self):
        self.assertRedirects(self.corres, self.next_url)
        self.assertTrue(User.objects.exists())
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.corres.status_code, 302)

    def test_failure_post_with_empty_form(self):
        context = {}
        self.response = self.client.post(self.signup_url, context)
        self.assertEquals(self.response.status_code, 200)

    def test_failure_post_with_empty_username(self):
        context = {
            'username': '',
            'password1': self.password,
            'password2': self.password,
        }
        self.response = self.client.post(self.signup_url, context)

        form = self.response.context.get('form')
        self.assertTrue(form.errors)

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


class TestHomeView(TestCase):
    def test_success_get(self):
        pass


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


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
