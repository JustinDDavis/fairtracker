from django.test import TestCase


class UnAuthTest(TestCase):
    def test_unauthenticated_users_should_not_access(self) -> None:
        response = self.client.get('/fair/')
        self.assertRedirects(response, "/")