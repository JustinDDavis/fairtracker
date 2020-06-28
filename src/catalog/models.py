from django.db import models
from fair.models import Fair


class Catalog(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)