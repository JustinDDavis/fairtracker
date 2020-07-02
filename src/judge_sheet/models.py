from django.db import models

from participant.models import Participant
from prize.models import Prize


class JudgeSheet(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="participant_judge_sheet_set")
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name="prize_judge_sheet_set")

    def __str__(self):
        return "JudgeSheet()"
