from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from fair.models import Fair
from fair.forms import FairForm

class TestFairPage(TestCase):
    def setUp(self) -> None:
        self.client.force_login(self._dummy_user())

    def test_page_load(self):
        response = self.client.get('/fair/')
        self.assertEqual(response.status_code, 200)

    def test_fairs_can_pass_to_template(self):
        """
            Test that when logged in a another user, the template will only get their template
        """
        self._create_fair()
        self.client.force_login(self._dummy_user("secondaryUser"))
        response = self.client.get('/fair/')
        self.assertTrue(isinstance(response.context.get("current_user_fairs"), QuerySet))
        self.assertEqual(len(response.context.get("current_user_fairs")), 0)

    def test_fair_exists_in_template(self):
        self._create_fair()
        response = self.client.get('/fair/')
        self.assertIn("Test Fair", response.content.decode("utf-8"))

    def test_fair_post(self):
        fair = self._standard_fair()
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
        self._create_fair("Fair1")
        self._create_fair("Fair2")

        az_order = Fair.objects.filter(owner_id=self._dummy_user()).order_by("name")
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

    def test_fairs_form_is_valid(self):
        fair = self._standard_fair()
        data = {
            'name': fair.name,
            'city': fair.city,
            'state': fair.state,
            'active': fair.active,
            'owner': fair.owner
        }
        form = FairForm(data=data)
        self.assertTrue(form.is_valid())

    def _create_fair(self, name="Fair 1"):
        fair = self._standard_fair(name)
        fair.save()

    def _standard_fair(self, name="Fair"):
        return Fair.objects.create(name=f"Test {name}",
                                   city=f"Test {name}",
                                   state=f"Test {name}",
                                   active=True,
                                   owner=self._dummy_user())

    @staticmethod
    def _dummy_user(username='testuser'):
        return User.objects.get_or_create(username=username)[0]
