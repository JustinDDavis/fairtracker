from django.db import models

from django.conf import settings

class Fair(models.Model):
    name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30)
    active = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.city} | {self.state} | {self.owner}"

