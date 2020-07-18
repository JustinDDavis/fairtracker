from django.test import TestCase
from django.db.models.query import QuerySet

from fair.models import Fair
from .utils import get_dummy_user, \
                    create_fair, \
                    standard_fair


class TestFairPage(TestCase):
    def setUp(self) -> None:
        self.client.force_login(get_dummy_user())

    def test_page_load(self):
        """
            Test that the page can load successfully
        """
        response = self.client.get('/fair/')
        self.assertEqual(response.status_code, 200)

    def test_fairs_can_pass_to_template(self):
        """
            Test that when logged in a another user, the template will only get their template
        """
        create_fair()
        self.client.force_login(get_dummy_user("secondaryUser"))
        response = self.client.get('/fair/')
        self.assertTrue(isinstance(response.context.get("current_user_fairs"), QuerySet))
        self.assertEqual(len(response.context.get("current_user_fairs")), 0)

    def test_fair_exists_in_template(self):
        """
            Test the template is getting rendered with some data displayed
        """
        create_fair()
        response = self.client.get('/fair/')
        self.assertIn("Test Fair", response.content.decode("utf-8"))

    def test_fair_post(self):
        """
            Test that a request can successfully be posted
        """
        fair = standard_fair()
        data = {
            'name': fair.name,
            'city': fair.city,
            'state': fair.state,
            'active': fair.active,
            'owner': fair.owner
        }
        response = self.client.post('/fair/', data)
        self.assertRedirects(response, "/fair/")

    def test_fair_default_order(self):
        """
            Test that using sorting options work
        """
        create_fair("Fair1")
        create_fair("Fair2")

        az_order = Fair.objects.filter(owner_id=get_dummy_user()).order_by("name")

        sorting_attributes = ['name', 'city', 'state']
        for sorting in sorting_attributes:

            # Check that A-Z Order works
            response = self.client.get(f'/fair/?sort={sorting}')
            self.assertEqual(
                getattr(response.context.get("current_user_fairs")[0], sorting, False),
                getattr(az_order[0], sorting, False)
            )

            # # Check that Z-A order works
            response = self.client.get(f'/fair/?sort=-{sorting}')
            self.assertEqual(
                getattr(response.context.get("current_user_fairs")[0], sorting, False),
                getattr(az_order[1], sorting, False)
            )
