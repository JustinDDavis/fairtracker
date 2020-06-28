from django.db import models

from catalog.models import Catalog

class CatalogItem(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    def __str__(self):
        return f"CatalogItem({self.name} | {self.description} | {self.catalog})"