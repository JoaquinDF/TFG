from bson.objectid import ObjectId
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from .serializers import *
from .tasks import *


# CALL
class CallMapperViewSet(ModelViewSet):
    queryset = ConvocatoriaMapper.objects.all()
    serializer_class = ConvocatoriaMapperSerializer


class DeleteCallMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in ConvocatoriaMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class CallMappingViewSet(ViewSet):
    def create(self, request):
        call_mapping_task.delay()
        return Response({'data': 'call', 'queued': True})


# PROJECT
class ProjectMapperViewSet(ModelViewSet):
    queryset = ProyectoMapper.objects.all()
    serializer_class = ProyectoMapperSerializer


class DeleteProjectMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in ProyectoMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class ProjectMappingViewSet(ViewSet):
    def create(self, request):
        project_mapping_task.delay()
        return Response({'data': 'project', 'queued': True})


# ORGANIZATION
class OrganizationMapperViewSet(ModelViewSet):
    queryset = OrganizacionMapper.objects.all()
    serializer_class = OrganizacionMapperSerializer


class DeleteOrganizationMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in OrganizacionMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class OrganizationMappingViewSet(ViewSet):
    def create(self, request):
        organization_mapping_task.delay()
        return Response({'data': 'organization', 'queued': True})


# PERSON
class PersonMapperViewSet(ModelViewSet):
    queryset = PersonaMapper.objects.all()
    serializer_class = PersonaMapperSerializer


class PersonMappingViewSet(ViewSet):
    def create(self, request):
        person_mapping_task.delay()
        return Response({'data': 'person', 'queued': True})


# PROJECT-CALL
class ProjectCallMapperViewSet(ModelViewSet):
    queryset = ProyectoConvocatoriaMapper.objects.all()
    serializer_class = ProyectoConvocatoriaMapperSerializer


class DeleteProjectCallMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in ProyectoConvocatoriaMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class ProjectCallMappingViewSet(ViewSet):
    def create(self, request):
        project_call_mapping_task.delay()
        return Response({'data': 'project-call', 'queued': True})


# PROJECT-ORGANIZATION
class ProjectOrganizationMapperViewSet(ModelViewSet):
    queryset = ProyectoOrganizacionMapper.objects.all()
    serializer_class = ProyectoOrganizacionMapperSerializer


class DeleteProjectOrganizationMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in ProyectoOrganizacionMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class ProjectOrganizationMappingViewSet(ViewSet):
    def create(self, request):
        project_organization_mapping_task.delay()
        return Response({'data': 'project-organization', 'queued': True})


# PERSON-PROJECT
class PersonProjectMapperViewSet(ModelViewSet):
    queryset = PersonaProyectoMapper.objects.all()
    serializer_class = PersonaProyectoMapperSerializer


class DeletePersonProjectMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in PersonaProyectoMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class PersonProjectMappingViewSet(ViewSet):
    def create(self, request):
        person_project_mapping_task.delay()
        return Response({'data': 'person-project', 'queued': True})


# PERSON-ORGANIZATION
class PersonOrganizationMapperViewSet(ModelViewSet):
    queryset = PersonaOrganizacionMapper.objects.all()
    serializer_class = PersonaOrganizacionMapperSerializer


class DeletePersonOrganizationMapperViewSet(ViewSet):
    def create(self, request):
        id = request.data.get('id', '*')
        print(id)
        a = [k for k in PersonaOrganizacionMapper.objects.all()]
        b = []
        for k in a:
            if ObjectId(id) == k.id:
                b.append(k)
        b[0].delete()
        return Response(True)


class PersonOrganizationMappingViewSet(ViewSet):
    def create(self, request):
        person_organization_mapping_task.delay()
        return Response({'data': 'person-organization', 'queued': True})
