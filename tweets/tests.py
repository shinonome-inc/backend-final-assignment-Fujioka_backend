from django.test import TestCase, Client
from django.urls import reverse

from tweets.models import TweetModel
from accounts.models import User


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('tweets:create')
        self.redirect_url = reverse('tweets:list')
        self.tweet_text = 'this is a test tweet.'
        self.username = 'testuser'
        self.overlength_tweet_text = 'this is a looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong tweet.'

    def test_success_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweets/create.html')

    def test_success_post(self):
        response = self.client.post(
            self.create_url, {'text': self.tweet_text, 'author': self.username})
        self.assertTrue(TweetModel.objects.exists())
        self.assertEqual(response.status_code, 302)

    def test_failure_post_with_empty_content(self):
        response = self.client.post(
            self.create_url, {'text': '', 'author': self.username})
        self.assertFalse(TweetModel.objects.exists())
        form = response.context.get('form')
        self.assertIsNotNone(form.errors.get('text'))

    def test_failure_post_with_too_long_content(self):
        response = self.client.post(
            self.create_url, {'text': self.overlength_tweet_text, 'author': self.username})
        self.assertFalse(TweetModel.objects.exists())
        form = response.context.get('form')
        self.assertIsNotNone(form.errors.get(
            'text'), 'Ensure this value has at most 140 characters')


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.detail_url = reverse('tweets:detail', kwargs={'pk': 1})
        self.user = User.objects.create_user(self.username, '', self.password)
        self.client.login(username = self.username, password = self.password)
        self.test_tweet = TweetModel.objects.create(text = 'test1', author = self.username)
    
    def test_success_get(self):
        response = self.client.get(self.detail_url, {'author': self.username})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweets/detail.html')


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.delete_url = reverse('tweets:delete', kwargs={'pk': 1})
        self.delete_confirm_rul = reverse('tweets:delete_confirm', kwargs={'pk': 1})
        self.create_url = reverse('tweets:create')
        self.user = User.objects.create_user(self.username, '', self.password)
        self.client.login(username = self.username, password = self.password)
        self.client.post(self.create_url, {'text': 'text_text', 'author': self.username})
    
    def test_success_post(self):
        response = self.client.post(self.delete_url)
        self.assertFalse(TweetModel.objects.exists())

    def test_failure_post_with_not_exist_tweet(self):
        self.delete_url_error = reverse('tweets:delete', kwargs={'pk': 2})
        response = self.client.post(self.delete_url_error)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(TweetModel.objects.exists())

    def test_failure_post_with_incorrect_user(self):
        response = self.client.get(self.delete_confirm_rul, {'author': 'fakeuser'})
        self.assertRedirects(response, reverse('tweets:list'), 302, 200)
        self.assertTrue(TweetModel.objects.exists())


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
