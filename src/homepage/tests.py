from django.test import TestCase
from django.contrib.auth.models import User


class TestAuthenticatedHomepage(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_authenticated_user_home(self) -> None:
        # If someone is authenticated and they go home, go ahead and make them go to the dashboard page.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/dashboard/")

    def test_fair_is_in_page(self) -> None:
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Fairs" in response.content.decode("utf-8"))


class TestHomepage(TestCase):
    def test_unauthenticated_user_home(self) -> None:
        # First page that users should see. They'll be navigating without being authenticated.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_unauthenticated_dashboard(self) -> None:
        # Check if an unauthenticated user can visit the dashboard...
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")



