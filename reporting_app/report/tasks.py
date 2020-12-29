import json
import os
from datetime import timedelta, datetime
from celery import shared_task
from django.utils import timezone
from .models import Report


def extractData():
    api_client = os.getenv("API_CLIENT", "ZOOM")
    # url = api_client + "_URL".format(
    #   year=timezone.now().year,
    #   month=timezone.now().month))
    # headers = {'Authorization': api_client + "_TOKEN",
    #            'Content-Type': 'application/json'
    #            }
    # response = requests.get(url, headers=headers)
    # data = json.loads(response.text)

    """ As demo paid accounts was not available,thus mocked up a few records looking at the API schema into JSON """

    json_data = open(os.getenv(api_client + "_REPORT_JSON"))
    api_response = json.load(json_data)
    json_data.close()
    return api_response['dates']


# celery -A reporting_app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A reporting_app beat -l INFO
@shared_task
def updateRecordService(window_end=None):
    print("Update Service running!")
    if os.getenv("DEFAULT_EXTRACT_DATA", True):
        response_data = extractData()
    else:
        response_data = []

    try:
        if not window_end:
            window_end = timezone.now().date()
        usage_records = Report.objects.filter(date__gt=window_end - timedelta(days=int(os.getenv("DAYS_OF_USAGE"))),
                                              date__lte=window_end).order_by('-date')
        if usage_records.count() == int(os.getenv("DAYS_OF_USAGE")):
            print("Already up to date")
            return
        window_start = window_end - timedelta(days=int(os.getenv("DAYS_OF_USAGE")))

        data_list = []
        for data in response_data:
            record_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if window_start < record_date <= window_end:
                if not usage_records.filter(date=record_date):
                    report_usage_record = Report(date=record_date, new_users=data['new_users'], meetings=data['meetings'],
                                                 participants=data['participants'], meeting_minutes=data['meeting_minutes'], )
                    data_list.append(report_usage_record)
        Report.objects.bulk_create(data_list)
        print("Records Updated!")
    except Report.DoesNotExist:
        print('Report Record does not exist!')
