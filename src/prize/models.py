from django.db import models

from catalog.models import Catalog


class Prize(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Prize({self.name} | {self.description} | {self.amount})"
