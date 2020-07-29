from django.test import TestCase
from django.urls import reverse

from .utils import get_dummy_user, create_fair, get_fair


class TestActivateFair(TestCase):
    def setUp(self) -> None:
        self.client.force_login(get_dummy_user())

    def test_activate(self):
        fair_id = create_fair().id
        self.client.get(reverse('fair_activate', args=[fair_id]))
        self.assertEqual(get_fair(fair_id).active, True)

    def test_only_the_owner_can_activate(self):
        """
            Create a Fair, then switch to a different user and try to activate that other fair.
        """
        fair_id = create_fair().id
        self.client.force_login(get_dummy_user("secondaryUser"))
        self.client.get(reverse('fair_activate', args=[fair_id]))

        self.assertEqual(get_fair(fair_id).active, False)

