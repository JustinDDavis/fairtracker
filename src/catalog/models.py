from django.db import models
from fair.models import Fair


class Catalog(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    active = models.BooleanField(default=False)
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)

    def __str__(self):
        return f"Catalog({self.name} | {self.description} | {self.active} | {self.fair})"