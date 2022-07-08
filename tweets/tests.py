from traceback import print_tb
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from mysite.settings import BASE_DIR
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver

from tweets.models import LikeModel, TweetModel
from accounts.models import User


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('tweets:create')
        self.redirect_url = reverse('tweets:list')
        self.tweet_text = 'this is a test tweet.'
        self.overlength_tweet_text = 'this is a looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong tweet.'
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(self.username, '', self.password)
        self.client.login(username = self.username, password = self.password)
        self.author = User.objects.get(username=self.username)

    def test_success_get(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertRedirects(response, '/login/?next=/tweets/create/')
        self.client.login(username = self.username, password = self.password)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweets/create.html')

    def test_success_post(self):
        response = self.client.post(
            self.create_url, {'text': self.tweet_text, 'author': self.author})
        self.assertTrue(TweetModel.objects.exists())
        self.assertEqual(response.status_code, 302)

    def test_failure_post_with_empty_content(self):
        response = self.client.post(
            self.create_url, {'text': '', 'author': self.author})
        self.assertFalse(TweetModel.objects.exists())
        form = response.context.get('form')
        self.assertIsNotNone(form.errors.get('text'))

    def test_failure_post_with_too_long_content(self):
        response = self.client.post(
            self.create_url, {'text': self.overlength_tweet_text, 'author': self.author})
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
        self.test_tweet = TweetModel.objects.create(text = 'test1', author = User.objects.get(username=self.username))
    
    def test_success_get(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, '/login/?next=/tweets/detail/1')
        self.client.login(username = self.username, password = self.password)
        response = self.client.get(self.detail_url)
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
        self.client.logout()
        self.user = User.objects.create_user('waruihito', '', 'iambadman')
        self.client.login(username = 'waruihito', password = 'iambadman')
        
        response = self.client.get(self.delete_confirm_rul)
        self.assertRedirects(response, reverse('tweets:list'), 302, 200)
        self.assertTrue(TweetModel.objects.exists())
        
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(TweetModel.objects.exists())
        


class TestFavoriteView(TestCase):
    def setUp(self):
        self.client = Client()
        # self.selenium = WebDriver(executable_path='../geckodriver/chromedriver')
        # driver = webdriver.Chrome(executable_path='../geckodriver/chromedriver')
        
        # self.driver = webdriver.Firefox([str(BASE_DIR / 'geckodriver' / 'geckodriver')])
        self.username = 'testuser'
        self.password = 'testpassword'
        
        User.objects.create_user(self.username, '', self.password)
        self.user = User.objects.get(username = self.username)
        self.client.login(username = self.username, password = self.password)
        TweetModel.objects.create(text = 'test', author = User.objects.get(username = self.username))
        self.tweet = TweetModel.objects.get(author = self.user)

        self.list_url = reverse('tweets:list')
        
    def test_success_post(self):
        # self.driver.get(self.list_url)
        # self.driver.find_element_by_id('like').click()
        # self.assertFalse(LikeModel.objects.exists())
        # self.client.post(self.list_url, {})
        # print(LikeModel.objects.exists())
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
