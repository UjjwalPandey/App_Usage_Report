import json
import os
from datetime import timedelta, datetime
from celery import shared_task
from django.db import IntegrityError
from django.utils import timezone

from .models import Report
from django.utils.module_loading import import_string


# celery -A reporting_app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A reporting_app beat -l INFO
@shared_task
def updateRecordService(window_end=None):
    print("Update Service running!")
    api_client = os.getenv("API_CLIENT", "ZOOM")
    try:
        module = import_string(os.getenv(api_client+"_INJECT_MODULE", 'report.modules.zoom.Zoom'))
    except ModuleNotFoundError:
        return False, "Error: ModuleNotFoundError "+os.getenv(api_client+"_INJECT_MODULE", 'report.modules.zoom.Zoom')
    response_data = module.extractData()
    if not response_data:
        return False, "Error: File Not Found"

    try:
        if not window_end:
            window_end = timezone.now().date()
        usage_records = Report.objects.filter(date__gt=window_end - timedelta(days=int(os.getenv("DAYS_OF_USAGE"))),
                                              date__lte=window_end).order_by('-date')
        if usage_records.count() == int(os.getenv("DAYS_OF_USAGE")):
            print("Already up to date")
            return True, ""
        window_start = window_end - timedelta(days=int(os.getenv("DAYS_OF_USAGE")))

        data_list = []
        for data in response_data:
            record_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if window_start < record_date <= window_end:
                if not usage_records.filter(date=record_date):
                    report_usage_record = Report(date=record_date, new_users=data['new_users'], meetings=data['meetings'],
                                                 participants=data['participants'], meeting_minutes=data['meeting_minutes'], )
                    data_list.append(report_usage_record)
        try:
            Report.objects.bulk_create(data_list)
        except IntegrityError:
            return False, "Error: IntegrityError"
        print("Records Updated!")
    except Report.DoesNotExist:
        print('Report Record does not exist!')

    return True, ""
