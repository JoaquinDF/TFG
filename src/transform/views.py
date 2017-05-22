from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import OrganizationMapper
from .serializers import OrganizationMapperSerializer
from .tasks import organization_task


class OrganizationMapperViewSet(viewsets.ModelViewSet):
    queryset = OrganizationMapper.objects.all()
    serializer_class = OrganizationMapperSerializer


class OrganizationViewSet(ViewSet):
    def create(self, request):
        organization_task.delay()
        return Response({'data': 'organization', 'queued': True})
