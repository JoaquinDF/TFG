from bson.objectid import ObjectId
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import *


# CALL
class CallViewSet(ReadOnlyModelViewSet):
    serializer_class = ConvocatoriaSerializer
    queryset = Convocatoria.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tituloConvocatoria',)

    def get_queryset(self):
        response = Convocatoria.objects.all()
        org = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)
        if org is not None:
            response = Convocatoria.objects(id=org)
        if name is not None:
            response = response.filter(tituloConvocatoria__icontains=name)
        return response


# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet):
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tituloProyecto',)

    def get_queryset(self):
        response = Proyecto.objects.all()
        org = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)
        if org is not None:
            response = response.filter(id=ObjectId(org))
        if name is not None:
            response = response.filter(tituloProyecto__icontains=name)
        return response


# ORGANIZATION
class OrganizationViewSet(ReadOnlyModelViewSet):
    serializer_class = OrganizacionSerializer
    queryset = Organizacion.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('nombre',)

    def get_queryset(self):
        response = Organizacion.objects.all()
        org = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)
        if org is not None:
            response = response.filter(id=ObjectId(org))
        if name is not None:
            response = response.filter(nombre__icontains=name)
        return response


# PERSON
class PersonViewSet(ReadOnlyModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


# PROJECT-CALL
class ProjectCallViewSet(ReadOnlyModelViewSet):
    serializer_class = ProyectoConvocatoriaSerializer
    queryset = ProyectoConvocatoria.objects.all()

    def get_queryset(self):
        response = ProyectoConvocatoria.objects.all()
        project = self.request.query_params.get('project', None)
        call = self.request.query_params.get('call', None)
        if project is not None:
            response = response.filter(proyecto=ObjectId(project))
        if call is not None:
            response = response.filter(convocatoria=ObjectId(call))
        return response


# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(ReadOnlyModelViewSet):
    serializer_class = ProyectoOrganizacionSerializer
    queryset = ProyectoOrganizacion.objects.all()

    def get_queryset(self):
        response = ProyectoOrganizacion.objects.all()
        project = self.request.query_params.get('project', None)
        organization = self.request.query_params.get('organization', None)
        if project is not None:
            response = response.filter(proyecto=ObjectId(project))
        if organization is not None:
            response = response.filter(organizacion=ObjectId(organization))
        return response


# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer
