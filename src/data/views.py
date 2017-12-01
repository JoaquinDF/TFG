from bson.objectid import ObjectId
from rest_framework import filters
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import requests
import pprint
from .serializers import *


# CALL
class CallViewSet(ReadOnlyModelViewSet):

    serializer_class = ConvocatoriaSerializer
    queryset = Convocatoria.objects.all();
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tituloConvocatoria',)

    def get_queryset(self):
        queryset = Convocatoria.objects.all();
        org = self.request.query_params.get('id', None)
        if org is not None:
            queryset = Convocatoria.objects(id=org)
            return queryset
        username = self.request.query_params.get('name', None)
        if username is not None:
            queryset = queryset.filter(tituloConvocatoria__icontains=username)
        return queryset







# PROJECT
class ProjectViewSet(ReadOnlyModelViewSet , generics.ListAPIView):
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tituloProyecto',)
    def get_queryset(self):

        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Proyecto.objects.all()
        username = self.request.query_params.get('id', None)
        if username is not None:
            queryset = queryset.filter(id=ObjectId(username))
            return queryset
        username = self.request.query_params.get('name', None)
        if username is not None:
            queryset = queryset.filter(tituloProyecto__icontains=username)
        return queryset

# ORGANIZATION
class OrganizationViewSet(ReadOnlyModelViewSet):
    serializer_class = OrganizacionSerializer
    queryset = Organizacion.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('nombre',)


    def get_queryset(self):

        queryset = Organizacion.objects.all()
        query_params = self.request.query_params.get('id', None)
        if query_params is not None:
            queryset = queryset.filter(id=ObjectId(query_params))
            return queryset


        query_params = self.request.query_params.get('nation', None)
        if query_params is not None and query_params == 'ESP':
            queryset = queryset.filter(direccion__pais__icontains='pain')
            return queryset
        if query_params is not None and query_params == 'EU':
            queryset = queryset.filter(direccion__european=True)
            return queryset


        query_params = self.request.query_params.get('name', None)
        if query_params is not None:
            queryset = queryset.filter(nombre__icontains=query_params)
        return queryset




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
        username = self.request.query_params.get('project', None)
        if username is not None:
            print(username)
            queryset = queryset.filter(proyecto=ObjectId(username))
            return queryset

        username = self.request.query_params.get('call', None)
        if username is not None:
            print(username)
            queryset = queryset.filter(convocatoria=ObjectId(username))
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
        username = self.request.query_params.get('project', None)
        if username is not None:
            print(username)
            queryset = queryset.filter(proyecto=ObjectId(username))
            return queryset

        username = self.request.query_params.get('organization', None)
        if username is not None:
            print(username)
            queryset = queryset.filter(organizacion=ObjectId(username))
        return queryset


class RegionMetricViewSet(ReadOnlyModelViewSet):
    queryset = RegionMetric.objects.all()
    serializer_class = RegionMetricSerializer


# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer


class RegionMetricViewSet(ReadOnlyModelViewSet):
    serializer_class = RegionMetricSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = RegionMetric.objects.all()
        region = self.request.query_params.get('region', None)
        if region is not None:
            print(region)
            queryset = queryset.filter(country=region)

        return queryset


class RegionMetricToPairDictViewSet(ViewSet):
    def create(self, request):
        queryset = RegionMetric.objects.all()
        organizations = request.data.get('organization', '*')
        dictionary = []

        for regionmetric in queryset:
            url = 'https://restcountries.eu/rest/v2/name/' + regionmetric.country

            data = requests.get(url)
            json = data.json()
            ISO = json[0]['alpha2Code']
            add = (ISO, regionmetric.numeroEmpresas)
            dictionary.append(add)
            pprint.pprint(dictionary)
        return Response(dictionary)


class OrganizationMetricViewSet(ReadOnlyModelViewSet):
    serializer_class = OrganizationMetricSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OrganizationMetric.objects.all()
        org = self.request.query_params.get('organization', None)
        if org is not None:
            queryset = queryset.filter(organization=ObjectId(org))

        return queryset
