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


class ProjectCallLinkageViewSet(ViewSet):
    def create(self, request):
        project_call_linkage_task.delay()
        return Response({'name': 'project_call_linkage_task', 'queued': True})


class ProjectOrganizationLinkageViewSet(ViewSet):
    def create(self, request):
        project_organization_linkage_task.delay()
        return Response({'name': 'project_organization_linkage_task', 'queued': True})


class DatabaseLinkageViewSet(ViewSet):
    def create(self, request):
        call_linkage_task.delay()
        organization_linkage_task.delay()
        project_linkage_task.delay()
        project_call_linkage_task.delay()
        project_organization_linkage_task.delay()
        return Response({'name': 'database_linkage_task', 'queued': True})
