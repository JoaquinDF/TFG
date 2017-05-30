from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import OrganizationMapper, Organization
from .serializers import OrganizationMapperSerializer, OrganizationSerializer
from .tasks import organization_mapping_task, organization_find_task


class OrganizationMapperViewSet(viewsets.ModelViewSet):
    queryset = OrganizationMapper.objects.all()
    serializer_class = OrganizationMapperSerializer


class OrganizationViewSet(ViewSet):
    def create(self, request):
        organization_mapping_task.delay()
        return Response({'data': 'organization', 'queued': True})

    def list(self, request):
        queryset = Organization.objects.all()
        paginator = Paginator(queryset, 100)
        page = request.query_params.get('page')
        try:
            organizations = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            organizations = paginator.page(page)
        except EmptyPage:
            organizations = paginator.page(paginator.num_pages)
        serializer = OrganizationSerializer(organizations, many=True)
        nxt = None
        prv = None
        if int(page) + 1 <= paginator.num_pages:
            nxt = request.build_absolute_uri(request.path_info + '?page=' + str(int(page) + 1))
        if int(page) - 1 > 0:
            prv = request.build_absolute_uri(request.path_info + '?page=' + str(int(page) - 1))
        response = dict()
        response['count'] = Organization.objects.count()
        response['next'] = nxt
        response['previous'] = prv
        response['results'] = serializer.data
        return Response(response)

    def retrieve(self, request, pk=None):
        result = organization_find_task.delay(field='name', key=pk, limit=100).get()
        return Response(result)
