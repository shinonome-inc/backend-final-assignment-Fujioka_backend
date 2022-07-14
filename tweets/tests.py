import json
from telnetlib import EC
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.client.login(username=self.username, password=self.password)
        self.author = User.objects.get(username=self.username)

    def test_success_get(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertRedirects(response, '/login/?next=/tweets/create/')
        self.client.login(username=self.username, password=self.password)
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
        self.client.login(username=self.username, password=self.password)
        self.test_tweet = TweetModel.objects.create(
            text='test1', author=User.objects.get(username=self.username))

    def test_success_get(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, '/login/?next=/tweets/detail/1')
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweets/detail.html')


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.delete_url = reverse('tweets:delete', kwargs={'pk': 1})
        self.delete_confirm_rul = reverse(
            'tweets:delete_confirm', kwargs={'pk': 1})
        self.create_url = reverse('tweets:create')
        self.user = User.objects.create_user(self.username, '', self.password)
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.create_url, {
                         'text': 'text_text', 'author': self.username})

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
        self.client.login(username='waruihito', password='iambadman')

        response = self.client.get(self.delete_confirm_rul)
        self.assertRedirects(response, reverse('tweets:list'), 302, 200)
        self.assertTrue(TweetModel.objects.exists())

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(TweetModel.objects.exists())


class TestFavoriteView(StaticLiveServerTestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.loginname = 'loginuser'
        self.password = 'testpassword'
        self.list_url = reverse('tweets:list')
        self.like_url = reverse('tweets:like')

        # テストユーザーとテストツイートを作る
        self.client.force_login(User.objects.create_user(
            self.username, '', self.password))
        self.user = User.objects.get(username=self.username)
        TweetModel.objects.create(
            text='test', author=User.objects.get(username=self.username))
        self.tweet = TweetModel.objects.get(author=self.user)

        # POST用のjsonデータ
        post_obj = {'tweet_pk': TweetModel.objects.get(
            author=User.objects.get(username=self.username)).pk}
        self.json = json.dumps(post_obj)
        
        # seleniumでログイン
        self.selenium = webdriver.Chrome(executable_path='./chromedriver')
        self.selenium.get(self.live_server_url +
                          str(reverse('welcome:login')))
        self.selenium.find_element(
            By.NAME, 'username').send_keys(self.username)
        self.selenium.find_element(
            By.NAME, 'password').send_keys(self.password)
        self.selenium.find_element(By.TAG_NAME, 'button').click()
        self.selenium.implicitly_wait(1)

    def tearDown(self):
        self.selenium.quit()

    def test_success_post(self):
        # いいねボタンをクリックしてボタンの変化を確認
        self.selenium.find_element(By.ID, 'like').click()
        WebDriverWait(self.selenium, 3).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'fas')))

        #　Likeが作られているか
        self.assertTrue(LikeModel.objects.exists())

        # いいねを取り消し
        self.selenium.find_element(By.ID, 'like').click()
        WebDriverWait(self.selenium, 3).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'far')))

        # 取り消されているか確認
        self.assertFalse(LikeModel.objects.exists())

        # POST送信の確認
        self.client.post(self.like_url, self.json, content_type="application/json")
        self.assertTrue(LikeModel.objects.exists())

    def test_failure_post_with_not_exist_tweet(self):
        # いいねはツイートにあるいいねボタンを押すことによる適切なPOST(適切なcsrf_token及びtweet_pkを保持)でのみ動作する。
        # 空のPOSTより送信したcsrf_tokenと存在しないtweet_pkを用いてpost送信をして、LikeModelが生成していないことを確認する。
        response = self.client.post(self.list_url)
        cookie_data = str(response.cookies).split(';')
        csrf = cookie_data[0].replace('Set-Cookie: csrftoken=', '')
        self.client.post(
            self.list_url, {'csrfmiddlewaretoken': csrf, 'tweet_pk': 9999})
        self.assertFalse(LikeModel.objects.exists())
        
        # POST送信の確認
        post_obj = {'tweet_pk': TweetModel.objects.get(
            author=User.objects.get(username=self.username)).pk + 1}
        self.client.post(self.like_url, json.dumps(post_obj), content_type="application/json")
        self.assertFalse(LikeModel.objects.exists())

    def test_failure_post_with_favorited_tweet(self):
        # 一度いいねボタンを押す
        self.selenium.find_element(By.ID, 'like').click()
        WebDriverWait(self.selenium, 3).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'fas')))
        # LikeModelが作られていることを確認
        self.assertTrue(LikeModel.objects.exists())

        # もう一度いいねボタンを押す。ボタンのスタイルが変わるのを確認
        self.selenium.find_element(By.ID, 'like').click()
        WebDriverWait(self.selenium, 3).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'far')))
        # LikeModelが消去されていることを確認
        self.assertFalse(LikeModel.objects.exists())
        
        # POST送信の確認
        # 一度いいねする
        self.client.post(self.like_url, self.json, content_type="application/json")
        self.assertTrue(LikeModel.objects.exists())

        # もう一度いいねする
        self.client.post(self.like_url, self.json, content_type="application/json")
        self.assertFalse(LikeModel.objects.exists())
        

# TestFavoriteView.test_failure_post_with_favorited_tweetにて目的は果たせているため省略
class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
