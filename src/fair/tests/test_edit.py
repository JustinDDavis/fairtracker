from django.test import TestCase
from django.urls import reverse

from .utils import get_dummy_user, create_fair


class TestActivateFair(TestCase):
    def setUp(self) -> None:
        self.client.force_login(get_dummy_user())

    def test_edit_get(self):
        fair = create_fair()
        response = self.client.get(reverse('fair_edit', args=[fair.id]))
        self.assertEqual(response.context.get("fair"), fair)

    def test_edit_post(self):
        fair = create_fair()

        data = {
            'name': fair.name,
            'city': fair.city,
            'state': fair.state,
            'active': fair.active,
            'owner': fair.owner
        }

        response = self.client.post(reverse('fair_edit', args=[fair.id]), data)
        self.assertRedirects(response, reverse('fair_home'))

