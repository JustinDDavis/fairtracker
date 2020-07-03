from django.db import models

from participant.models import Participant
from prize.models import Prize
from entry.models import CatalogItem


class JudgeSheet(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="participant_judge_sheet_set")
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, related_name="catalog_item_judge_sheet_set")
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name="prize_judge_sheet_set")

    def __str__(self):
        return "JudgeSheet()"
