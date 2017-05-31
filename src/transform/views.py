from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from .models import OrganizationMapper, Organization
from .serializers import OrganizationMapperSerializer, OrganizationSerializer
from .tasks import organization_mapping_task, organization_find_task


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

    def retrieve(self, request, pk=None):
        result = organization_find_task.delay(field='name', key=pk, limit=100).get()
        return Response(result)
