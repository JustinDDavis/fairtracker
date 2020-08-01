from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from .utils import get_dummy_user, create_fair, get_fair


class TestDeleteFair(TestCase):
    def setUp(self) -> None:
        self.client.force_login(get_dummy_user())

    def test_delete(self):
        fair_id = create_fair().id
        response = self.client.get(reverse('fair_delete', args=[fair_id]))
        self.assertRaises(ObjectDoesNotExist, get_fair, fair_id)
        self.assertRedirects(response, reverse('fair_home'))

