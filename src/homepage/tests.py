from django.test import TestCase
from django.contrib.auth.models import User


class TestHomepage(TestCase):
    def test_unauthenticated_user_home(self):
        # First page that users should see. They'll be navigating without being authenticated.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_unauthenticated_dashboard(self):
        # Check if an unauthenticated user can visit the dashboard...
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_authenticated_user_home(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/dashboard/")
