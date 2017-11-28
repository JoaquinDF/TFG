import json

import os
from celery import current_app
from django_celery_beat.models import *
from django_celery_beat.models import PeriodicTask
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class PeriodicTaskViewSet(ViewSet):
    def create(self, request):
        # bot/crawlers
        task = request.data.get('task', '*')
        args = request.data.get('args', '*')
        # chose interval?crontab
        crontab = request.data.get('crontab', '*')
        if crontab is not None:
            # crontabs
            minute = request.data.get('minute', '*')
            hour = request.data.get('hour', '*')
            day_of_week = request.data.get('day-week', '*')
            day_of_month = request.data.get('day_of_month', '*')
            month_of_year = request.data.get('month_of_year', '*')

            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year,
            )

            PeriodicTask.objects.create(
                crontab=schedule,
                name='Crontab' + '/' + task + '/' + args,
                task=task,
                args=json.dumps([args])
            )
        else:
            # intervals
            intervalevery = request.data.get('intervalevery', '*')
            intervalperiod = request.data.get('intervalperiod', '*')
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=intervalevery,
                period=intervalperiod, )
            PeriodicTask.objects.create(
                interval=schedule,
                name='Interval' + '/' + task + '/' + args,
                task=task,
                args=json.dumps([args])
            )
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


class ScheduleViewSet(ViewSet):
    def list(self, request):
        a = [k.name for k in PeriodicTask.objects.all()]
        return Response(a)


class DeleteTaskViewSet(ViewSet):
    def create(self, request):
        name = request.data.get('name', '*')
        a = [k for k in PeriodicTask.objects.all()]
        b = [k for k in a if name in k.name]
        b[0].delete()
        return Response(True)
