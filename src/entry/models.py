from django.db import models

from participant.models import Participant
from catalog_item.models import CatalogItem


class Entry(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="entry_participant")
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, related_name="entry_catalog_item")

    def __str__(self):
        return "Entry()"
