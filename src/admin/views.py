from django.shortcuts import render
import json
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from bson.json_util import dumps
import pprint
from random import randint

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from celery import current_app
import os


# Create your views here.
class PeriodicTaskViewSet(ViewSet):

    def create(self,request):

# cd ENV/lib/python3.4/site-packages/django_celery_beat

        task = request.data.get('task', '*')
        args = request.data.get('args', '*')

        minute = request.data.get('minute', '*')
        hour = request.data.get('hour', '*')
        day_of_week = request.data.get('day-week', '*')
        day_of_month = request.data.get('day-month', '*')
        month_of_year = request.data.get('month-year', '*')

        print(1)
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute = minute,
            hour = hour,
            day_of_week = day_of_week,
            day_of_month = day_of_month,
            month_of_year = month_of_year,
        )
        print(2)



        PeriodicTask.objects.create(
            crontab=schedule,
            name=task + args + str((randint(0, 999))),
            task=task,
            args=json.dumps([args])
                )

        print(3)
        return Response(PeriodicTask.objects.name)



class ListTasksViewSet(ViewSet):

    def list(self, request):
        celery_app = current_app
        tasks = list(sorted(name for name in celery_app.tasks
                            if not name.startswith('celery.')))



        return Response(tasks)


class ListBotsViewSet(ViewSet):
    def list(self, request):

        a = os.listdir('extract/bots')
        b = [k for k in a if '.py' in k if not '__' in k]
        c = [k.split('.')[0] for k in b]
        return Response(c)


class ListCrawlersViewSet(ViewSet):
    def list(self, request):
        a = os.listdir('extract/crawlers')
        b = [k for k in a if '.py' in k if not '__' in k]
        c = [k.split('.')[0] for k in b]
        return Response(c)
