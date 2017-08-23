from rest_framework.viewsets import ReadOnlyModelViewSet
import django_filters.rest_framework

from .serializers import *
from rest_framework import filters
from rest_framework import generics


# CALL
class CallViewSet(ReadOnlyModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer


# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet , generics.ListAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tituloProyecto',)


    def get_queryset(self):
        queryset = Proyecto.objects.all()
        titulo = self.request.query_params.get('titulo', None)
        if titulo is not None:
            queryset = queryset.filter(tituloProyecto=titulo)
        return queryset

        queryset = Proyecto.objects.all()
        subvencion = self.request.query_params.get('subvencion', None)
        if subvencion is not None:
            queryset = queryset.filter(subvencion=subvencion)
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
    queryset = ProyectoConvocatoria.objects.all()
    serializer_class = ProyectoConvocatoriaSerializer


# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(generics.ListAPIView, ReadOnlyModelViewSet):
    queryset = ProyectoOrganizacion.objects.all()
    serializer_class = ProyectoOrganizacionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('proyecto','organizacion')





# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer
