from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from .serializers import *
from .tasks import *


class OrganizationViewSet(ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationMapperViewSet(ModelViewSet):
    queryset = OrganizationMapper.objects.all()
    serializer_class = OrganizationMapperSerializer


class OrganizationMappingViewSet(ViewSet):
    def create(self, request):
        organization_mapping_task.delay()
        return Response({'data': 'organization', 'queued': True})


class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectMapperViewSet(ModelViewSet):
    queryset = ProjectMapper.objects.all()
    serializer_class = ProjectMapperSerializer


class ProjectMappingViewSet(ViewSet):
    def create(self, request):
        project_mapping_task.delay()
        return Response({'data': 'project', 'queued': True})


class CallViewSet(ReadOnlyModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


class CallMapperViewSet(ModelViewSet):
    queryset = CallMapper.objects.all()
    serializer_class = CallMapperSerializer
