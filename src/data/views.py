from rest_framework.viewsets import ReadOnlyModelViewSet;

import django_filters.rest_framework

from .serializers import *
from rest_framework import filters
from rest_framework import generics

# Get an instance of a logger

# CALL
class CallViewSet(ReadOnlyModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer


# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet , generics.ListAPIView):
    serializer_class = ProyectoSerializer

    def get_queryset(self):

        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Proyecto.objects.all()
        username = self.request.query_params.get('name', None)
        if username is not None:
            queryset = queryset.filter(tituloProyecto__contains=username)
            return queryset
        username = self.request.query_params.get('money', None)
        if username is not None:
            queryset = queryset.filter(subvencion=username)
        return queryset


# ORGANIZATION
class OrganizationViewSet(ReadOnlyModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


# PERSON
class PersonViewSet(ReadOnlyModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


# PROJECT-CALL
class ProjectCallViewSet(ReadOnlyModelViewSet):
    serializer_class = ProyectoConvocatoriaSerializer


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ProyectoConvocatoria.objects.all()
        username = self.request.query_params.get('call', None)
        if username is not None:
            queryset = queryset.filter(convocatoria=username)
        return queryset

# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(generics.ListAPIView, ReadOnlyModelViewSet):

    serializer_class = ProyectoOrganizacionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ProyectoOrganizacion.objects.all()
        asd = self.request.query_params.get('org', None)
        if asd is not None:
            queryset = queryset.filter(organizacion__contains=asd)
        return queryset


# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer
