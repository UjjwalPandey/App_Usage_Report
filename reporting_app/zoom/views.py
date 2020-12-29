import os
from datetime import timedelta, datetime

from django.db.models import Avg, Sum
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Zoom
from .serializers import ZoomSerializer
from .tasks import updateRecordService


class ZoomViewSet(viewsets.ModelViewSet):
    queryset = Zoom.objects.all()
    serializer_class = ZoomSerializer

    def list(self, request, *args, **kwargs):
        input_date = self.request.query_params.get('date', None)
        if input_date:
            try:
                window_end = datetime.strptime(input_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(data={"message": "Date query_param is not in desired format (%Y-%m-%d)"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            window_end = timezone.now().date()
        updateRecordService(window_end)

        window_start = window_end - timedelta(days=int(os.getenv("DAYS_OF_USAGE")))
        usage_avg = Zoom.objects.filter(date__gte=window_start, date__lte=window_end).\
            aggregate(Avg('new_users'), Avg('meetings'), Avg('participants'), Avg('meeting_minutes'))

        usage_sum = Zoom.objects.filter(date__gte=window_start, date__lte=window_end).\
            aggregate(Sum('new_users'), Sum('meetings'), Sum('participants'), Sum('meeting_minutes'))
        data = {
            "Start Date": window_start,
            "End Date": window_end,
            "Total avg": usage_avg,
            "Total sum": usage_sum
        }
        days = {"Sunday": 1, "Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thursday": 5, "Friday": 6, "Saturday": 7}
        for day in days:
            day_avg = Zoom.objects.filter(date__gt=window_start, date__lte=window_end).filter(date__week_day=days[day]).\
                aggregate(Avg('new_users'), Avg('meetings'), Avg('participants'), Avg('meeting_minutes'))
            data[day] = day_avg

        print(data)
        return Response(data=data, status=status.HTTP_200_OK)

