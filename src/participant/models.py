from django.db import models

from fair.models import Fair


class Participant(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.email} | {self.fair}"
