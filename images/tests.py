from django.test import TestCase
from .models import Repo, Image, User
from django.urls import reverse

# Create your tests here.


class RepoTestCase(TestCase):
    def setUp(self):
        Repo.objects.create(title="test1")

    def test_object_made(self):
        self.assertEqual(Repo.objects.filter(title="test1").exists(), True)


class ImageTestCase(TestCase):
    def setUp(self):
        Image.objects.create(title="test1")

    def test_image_made(self):
        self.assertEqual(Image.objects.filter(title="test1").exists(), True)


class HomePageTestCase(TestCase):
    def test_home_url(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_home_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_correct_template(self):
        resp = self.client.get(reverse('index'))
        self.assertTemplateUsed(resp, 'images/index.html')


class AuthPageTestCase(TestCase):
    def test_login_url(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_register_url(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    def test_register_name(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_login_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_logout_url(self):
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 302)  # 302 redirected

    def test_logout_name(self):
        resp = self.client.get(reverse("logout"))
        self.assertEqual(resp.status_code, 302)
