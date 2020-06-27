from django.contrib.auth.models import User
from .forms import ParticipantForm
from django.test import TestCase

import json


class TestParticipants(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_page_load(self):
        response = self.client.get("/participant/")
        self.assertEqual(response.status_code, 200)

    def test_table_load(self):
        response = self.client.get("/participant/")
        self.assertContains(response, "Participant Name")

    def test_invalid_form(self):
        value = {
            'name': "TestParticipant"
        }
        form = ParticipantForm(value)

        self.assertFalse(form.is_valid())

    def test_invalid_POST(self):
        value = {
            'name': "TestParticipant"
        }

        response = self.client.post("/participant/", json.dumps(value), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_form(self):
        value = {
            'name': "TestParticipant",
            'email': "TestParticipant@example.com"
        }
        form = ParticipantForm(value)

        self.assertTrue(form.is_valid())

    def test_post_new_form(self):
        value = {
            'name': "TestParticipant",
            'email': "TestParticipant@example.com"
        }

        form = ParticipantForm(value)

        response = self.client.post("/participant/", form, content_type="application/json")
        self.assertEqual(response.status_code, 200)