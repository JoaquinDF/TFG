import collections
import pprint
from django.http import HttpResponse
from django.utils.encoding import smart_str

import os
import requests
from bson.objectid import ObjectId
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ViewSet

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
class ProjectViewSet(ReadOnlyModelViewSet, generics.ListAPIView):
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


class SectorMetricViewSet(ViewSet):
    def create(self, request):
        queryset = Organizacion.objects.all()
        region = request.data.get('region', '*')
        salida = []
        if region is not '*':

            queryset = queryset.filter(direccion__pais__iexact=region)
            for org in queryset:
                try:
                    salida.append(org.sector[0].lower())
                except Exception:
                    continue

            counter = collections.Counter(salida)
            pprint.pprint(counter)

        return Response(counter)



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
        pprint.pprint(request)
        what = request.data.get('?', '*')

        if what == 'orgnum':
            path = '/home/bisite/innhome/innhome/src/www/static/json/Orgs-Num.json'
            if os.path.getsize(path) == 0:
                file = open(path, 'w+')

                queryset = RegionMetric.objects.all()
                dictionary = []

                for regionmetric in queryset:
                    url = 'https://restcountries.eu/rest/v2/name/' + regionmetric.country

                    data = requests.get(url)
                    json = data.json()
                    ISO = json[0]['alpha3Code']
                    add = (ISO, regionmetric.numeroEmpresas)
                    dictionary.append(add)

                from json import dumps as jsdumper
                data = jsdumper(dictionary)
                file.write(data)
                file.close()
                return Response(dictionary)
            else:
                file = open(path, 'r')
                jsondata = file.read()
                from json import loads as jsload
                data = jsload(jsondata)

                pprint.pprint(data)
                return Response(data)

        elif what == 'orgper':
            path = '/home/bisite/innhome/innhome/src/www/static/json/Orgs-Per.json'
            if os.path.getsize(path) == 0:
                file = open(path, 'w+')

                queryset = RegionMetric.objects.all()
                dictionary = []

                for regionmetric in queryset:
                    url = 'https://restcountries.eu/rest/v2/name/' + regionmetric.country

                    data = requests.get(url)
                    json = data.json()
                    ISO = json[0]['alpha3Code']
                    add = (ISO, regionmetric.porcentajesubvencionado)
                    dictionary.append(add)

                from json import dumps as jsdumper
                data = jsdumper(dictionary)
                file.write(data)
                file.close()
                return Response(dictionary)
            else:
                file = open(path, 'r')
                jsondata = file.read()
                from json import loads as jsload
                data = jsload(jsondata)

                pprint.pprint(data)
                return Response(data)

        elif what == 'proynum':
            path = '/home/bisite/innhome/innhome/src/www/static/json/Proy-Num.json'
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                file = open(path, 'w+')

                queryset = RegionMetric.objects.all()
                dictionary = []

                for regionmetric in queryset:
                    url = 'https://restcountries.eu/rest/v2/name/' + regionmetric.country

                    data = requests.get(url)
                    json = data.json()
                    ISO = json[0]['alpha3Code']
                    add = (ISO, regionmetric.numeroProyectos)
                    dictionary.append(add)

                from json import dumps as jsdumper
                data = jsdumper(dictionary)
                file.write(data)
                file.close()
                return Response(dictionary)
            else:
                file = open(path, 'r')
                jsondata = file.read()
                from json import loads as jsload
                data = jsload(jsondata)

                pprint.pprint(data)
                return Response(data)
        elif what == 'avenum':
            path = '/home/bisite/innhome/innhome/src/www/static/json/Ave-Num.json'
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                file = open(path, 'w+')

                queryset = RegionMetric.objects.all()
                dictionary = []

                for regionmetric in queryset:
                    url = 'https://restcountries.eu/rest/v2/name/' + regionmetric.country

                    data = requests.get(url)
                    json = data.json()
                    ISO = json[0]['alpha3Code']
                    add = (ISO, (regionmetric.numeroProyectos / regionmetric.numeroEmpresas))
                    dictionary.append(add)

                from json import dumps as jsdumper
                data = jsdumper(dictionary)
                file.write(data)
                file.close()
                return Response(dictionary)
            else:
                file = open(path, 'r')
                jsondata = file.read()
                from json import loads as jsload
                data = jsload(jsondata)

                pprint.pprint(data)
                return Response(data)


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


class CommunityViewSet(ReadOnlyModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def test_files(self, name=None):
        if name == "gexf":
            fsock = open('/home/bisite/innhome/innhome/src/www/static/js/metric-module/test.json', "rb")
            response = HttpResponse(content=fsock)
            response['Content-Type'] = 'application/gexf'
            response['Content-Disposition'] = 'attachment; filename="%s.gexf"' \
                                              % 'whatever'
            return response
