from django.test import TestCase
from django.contrib.auth.models import User


class UnAuthTest(TestCase):
    def unauthenticated_users_should_not_access(self) -> None:
        response = self.client.get('/fair/')
        self.assertRedirects(response, "/")


class TestFairPage(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def page_load(self):
        response = self.client.get('/fair/')
        self.assertEqual(response.status_code, 200)
