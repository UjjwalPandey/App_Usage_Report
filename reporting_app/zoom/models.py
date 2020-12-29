from django.db import models


class Zoom(models.Model):
    date = models.DateField(db_index=True, unique=True)
    new_users = models.PositiveIntegerField()
    meetings = models.PositiveIntegerField()
    participants = models.PositiveIntegerField()
    meeting_minutes = models.PositiveIntegerField(help_text="(in minutes)")

    def __str__(self):
        return '. '.join([str(self.pk), str(self.date)])
