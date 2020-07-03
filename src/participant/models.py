from django.db import models

from fair.models import Fair


class Participant(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    static_participant_id = models.CharField(max_length=60, default=None, null=True)

    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.email} | {self.fair}"
