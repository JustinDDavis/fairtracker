from django.test import TestCase

from fair.forms import FairForm
from .utils import standard_fair, get_dummy_user


class TestFairPage(TestCase):
    def setUp(self) -> None:
        self.client.force_login(get_dummy_user())

    def test_fairs_form_is_valid(self):
        fair = standard_fair()
        data = {
            'name': fair.name,
            'city': fair.city,
            'state': fair.state,
            'active': fair.active,
            'owner': fair.owner
        }
        form = FairForm(data=data)
        self.assertTrue(form.is_valid())