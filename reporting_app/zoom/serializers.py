from rest_framework import serializers

from .models import Zoom


class ZoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zoom
        fields = ('date', 'new_users', 'meetings', 'participants', 'meeting_minutes', )
