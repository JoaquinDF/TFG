from django.shortcuts import render
import json
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from bson.json_util import dumps
import pprint
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

# Create your views here.
class CrontabsViewSet(ViewSet):
    def create(self,request):
        minute = request.data.get('minute', '*')
        hour = request.data.get('hour', '*')
        day_of_week = request.data.get('day-week', '*')
        day_of_month = request.data.get('day-month', '*')
        month_of_year = request.data.get('month-year', '*')

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute = '30',
            hour = '*',
            day_of_week = '*',
            day_of_month = '*',
            month_of_year = '*',
        )

        PeriodicTask.objects.create(
            crontab=schedule,
            name='Crontab',
            task=None,
                )
        PeriodicTask.save()

        return Response(PeriodicTask)
