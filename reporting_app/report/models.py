from enum import IntEnum
from django.db import models


class AppName(IntEnum):
    ZOOM = 0
    DROPBOX = 1
    MEET = 2


class Report(models.Model):
    date = models.DateField(db_index=True, unique=True)
    new_users = models.PositiveIntegerField()
    meetings = models.PositiveIntegerField()
    participants = models.PositiveIntegerField()
    meeting_minutes = models.PositiveIntegerField(help_text="(in minutes)")
    type = models.IntegerField(default=AppName.ZOOM, choices=[(type.value, type.name) for type in AppName])

    def __str__(self):
        return '. '.join([str(self.pk), str(self.date)])
