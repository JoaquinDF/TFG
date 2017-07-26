from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .tasks import *


class CallLinkageViewSet(ViewSet):
    def create(self, request):
        call_linkage_task.delay()
        return Response({'name': 'call_linkage_task', 'queued': True})


class OrganizationLinkageViewSet(ViewSet):
    def create(self, request):
        organization_linkage_task.delay()
        return Response({'name': 'organization_linkage_task', 'queued': True})


class ProjectLinkageViewSet(ViewSet):
    def create(self, request):
        project_linkage_task.delay()
        return Response({'name': 'project_linkage_task', 'queued': True})


class PersonLinkageViewSet(ViewSet):
    def create(self, request):
        person_linkage_task.delay()
        return Response({'name': 'person_linkage_task', 'queued': True})
