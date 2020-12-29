from rest_framework import serializers

from .models import Report


class ZoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('date', 'new_users', 'meetings', 'participants', 'meeting_minutes', )
