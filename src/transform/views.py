from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from .serializers import *
from .tasks import *


# CALL
class CallViewSet(ReadOnlyModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer


class CallMapperViewSet(ModelViewSet):
    queryset = ConvocatoriaMapper.objects.all()
    serializer_class = ConvocatoriaMapperSerializer


class CallMappingViewSet(ViewSet):
    def create(self, request):
        call_mapping_task.delay()
        return Response({'data': 'call', 'queued': True})


# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer


class ProjectMapperViewSet(ModelViewSet):
    queryset = ProyectoMapper.objects.all()
    serializer_class = ProyectoMapperSerializer


class ProjectMappingViewSet(ViewSet):
    def create(self, request):
        project_mapping_task.delay()
        return Response({'data': 'project', 'queued': True})


# ORGANIZATION
class OrganizationViewSet(ReadOnlyModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


class OrganizationMapperViewSet(ModelViewSet):
    queryset = OrganizacionMapper.objects.all()
    serializer_class = OrganizacionMapperSerializer


class OrganizationMappingViewSet(ViewSet):
    def create(self, request):
        organization_mapping_task.delay()
        return Response({'data': 'organization', 'queued': True})


# PERSON
class PersonViewSet(ReadOnlyModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonMapperViewSet(ModelViewSet):
    queryset = PersonaMapper.objects.all()
    serializer_class = PersonaMapperSerializer


class PersonMappingViewSet(ViewSet):
    def create(self, request):
        person_mapping_task.delay()
        return Response({'data': 'person', 'queued': True})


# PROJECT-CALL
class ProjectCallViewSet(ReadOnlyModelViewSet):
    queryset = ProyectoConvocatoria.objects.all()
    serializer_class = ProyectoConvocatoriaSerializer


class ProjectCallMapperViewSet(ModelViewSet):
    queryset = ProyectoConvocatoriaMapper.objects.all()
    serializer_class = ProyectoConvocatoriaMapperSerializer


class ProjectCallMappingViewSet(ViewSet):
    def create(self, request):
        project_call_mapping_task.delay()
        return Response({'data': 'project-call', 'queued': True})


# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = ProyectoOrganizacion.objects.all()
    serializer_class = ProyectoOrganizacionSerializer


class ProjectOrganizationMapperViewSet(ModelViewSet):
    queryset = ProyectoOrganizacionMapper.objects.all()
    serializer_class = ProyectoOrganizacionMapperSerializer


class ProjectOrganizationMappingViewSet(ViewSet):
    def create(self, request):
        project_organization_mapping_task.delay()
        return Response({'data': 'project-organization', 'queued': True})


# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


class PersonProjectMapperViewSet(ModelViewSet):
    queryset = PersonaProyectoMapper.objects.all()
    serializer_class = PersonaProyectoMapperSerializer


class PersonProjectMappingViewSet(ViewSet):
    def create(self, request):
        person_project_mapping_task.delay()
        return Response({'data': 'person-project', 'queued': True})


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer


class PersonOrganizationMapperViewSet(ModelViewSet):
    queryset = PersonaOrganizacionMapper.objects.all()
    serializer_class = PersonaOrganizacionMapperSerializer


class PersonOrganizationMappingViewSet(ViewSet):
    def create(self, request):
        person_organization_mapping_task.delay()
        return Response({'data': 'person-organization', 'queued': True})
