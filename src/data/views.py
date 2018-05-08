from bson.objectid import ObjectId
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from mongoengine.queryset.visitor import Q

from .serializers import *

# Imports Nuevos
import collections
import pprint
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import pandas as pd
import json
import hashlib
import matplotlib
from sklearn import ensemble
import glob

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.snowball import EnglishStemmer
import time
import networkx as nx
from networkx.readwrite import json_graph
from .serializers import *
from collections import *
from sklearn.externals import joblib
from pymongo import MongoClient
from sklearn import preprocessing

from scipy import stats

from rest_framework.renderers import JSONRenderer

# TF-IDF
DATESTARTH2020 = 1388534400
DATEENDH2020 = 1577836800
timea = time.time()

client = MongoClient('localhost', 27017)
db = client.innhome

db.authenticate(name='innhome', password='innhome00')
raw_documents = []
c = db.get_collection('bots.h2020.projects')
documents = c.find()
for d in documents:
    raw_documents.append(d['objective'])


def stemmed_words(doc):
    """

    Args:
        doc:

    Returns:

    """
    stemmer = EnglishStemmer()
    analyzer = TfidfVectorizer(
        strip_accents='unicode',
        stop_words='english',
    ).build_analyzer()
    return (stemmer.stem(w) for w in analyzer(doc))


tfidf_vectorizer = TfidfVectorizer(
    strip_accents='unicode',
    analyzer=stemmed_words,
    stop_words='english',
    norm='l1',
    sublinear_tf=True,
)
if not os.path.exists('data/models-h2020/tfidf.sav'):
    tfidf = tfidf_vectorizer.fit(raw_documents)
    joblib.dump(tfidf, 'data/models-h2020/tfidf.sav')


# CALL
class CallViewSet(ModelViewSet):
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

        field = self.request.query_params.get('field', None)
        data = self.request.query_params.get('data', None)

        if field and data:
            kwargs = {
                '{0}'.format(field): data
            }
            pprint.pprint(kwargs)
            response = response.filter(**kwargs)

        return response


# PROJECT
class ProjectViewSet(ModelViewSet):
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tituloProyecto',)

    @property
    def get_queryset(self):
        response = Proyecto.objects.all()
        org = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)

        if org is not None:
            response = response.filter(id=ObjectId(org))
        if name is not None:
            response = response.filter(tituloProyecto__icontains=name)

        field = self.request.query_params.get('field', None)
        data = self.request.query_params.get('data', None)

        if field and data:
            kwargs = {
                '{0}'.format(field): data
            }
            pprint.pprint(kwargs)
            response = response.filter(**kwargs)

        return response


# ORGANIZATION
class OrganizationViewSet(ModelViewSet):
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

        field = self.request.query_params.get('field', None)
        data = self.request.query_params.get('data', None)

        if field and data:
            kwargs = {
                '{0}'.format(field): data
            }
            pprint.pprint(kwargs)
            queryset = queryset.filter(**kwargs)

        return queryset


# PERSON
class PersonViewSet(ModelViewSet):
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
            queryset = queryset.filter(proyecto=ObjectId(username))
            return queryset

        username = self.request.query_params.get('call', None)
        if username is not None:
            queryset = queryset.filter(convocatoria=ObjectId(username))
        return queryset


# PROJECT-ORGANIZATION
class ProjectOrganizationViewSet(ReadOnlyModelViewSet):
    serializer_class = ProyectoOrganizacionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ProyectoOrganizacion.objects.all()
        username = self.request.query_params.get('project', None)
        if username is not None:
            queryset = queryset.filter(proyecto=ObjectId(username))
            return queryset

        username = self.request.query_params.get('organization', None)
        if username is not None:
            queryset = queryset.filter(organizacion=ObjectId(username))
        return queryset


# PERSON-PROJECT
class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


# PERSON-ORGANIZATION
class PersonOrganizationViewSet(ReadOnlyModelViewSet):
    queryset = PersonaOrganizacion.objects.all()
    serializer_class = PersonaOrganizacionSerializer


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

        return Response(counter)

        # PERSON-PROJECT


class PersonProjectViewSet(ReadOnlyModelViewSet):
    queryset = PersonaProyecto.objects.all()
    serializer_class = PersonaProyectoSerializer


class RegionMetricViewSet(ReadOnlyModelViewSet):
    serializer_class = RegionMetricSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `region` query parameter in the URL.


        """
        queryset = RegionMetric.objects.all()
        region = self.request.query_params.get('region', None)
        if region is not None:
            queryset = queryset.filter(country=region)

        return queryset


class RegionMetricToPairDictViewSet(ViewSet):
    def create(self, request):
        """

        Args:
            request:

        Returns:

        """

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


class GraphH2020ViewSet(ReadOnlyModelViewSet):
    serializer_class = GraphH2020ViewSetSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Graph_nodes.objects.all()

        title = self.request.query_params.get('title', None)

        if title is not None:
            queryset = queryset.filter(tituloProyecto__icontains=title)

        community = self.request.query_params.get('community', None)
        if community is not None and community is not '':
            data = community.split(" ")
            data = list(map(int, data))

            if len(data) > 0:
                queryset = queryset.filter(community__in=list(data))

            else:
                queryset = queryset.filter(community=int(community))

        country = self.request.query_params.get('country', None)
        if country is not None and country is not '':

            data = country.split(" ")
            data = list(map(str.upper, data))
            data = [d for d in data if len(d) == 2]
            print(data)
            if len(data) > 0:
                queryset = queryset.filter(country__in=list(data))

            else:
                queryset = queryset.filter(country=data)

        moreP = self.request.query_params.get('moreP', 0)
        moreP = 0 if moreP is '' else int(moreP)

        lessP = self.request.query_params.get('lessP', 0)
        lessP = 0 if lessP is '' else int(lessP)

        moreS = self.request.query_params.get('moreS', 0)
        moreS = 0 if moreS is '' else int(moreS)

        lessS = self.request.query_params.get('lessS', 0)
        lessS = 0 if lessS is '' else int(lessS)

        if moreP > 0:
            queryset = queryset.filter(presupuesto__lte=moreP)
            print('moreP' + str(moreP))

        if moreS > 0:
            queryset = queryset.filter(subvencion__lte=moreS)
            print('moreS' + str(moreS))

        if lessP > 0:
            queryset = queryset.filter(presupuesto__gte=lessP)
            print('lessP' + str(lessP))

        if lessS > 0:
            queryset = queryset.filter(subvencion__gte=lessS)
            print('lessS' + str(lessS))

        return queryset


class AllCommunityViewSet(ReadOnlyModelViewSet):
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()


class CommunityViewSet(ReadOnlyModelViewSet):
    serializer_class = CommunitySerializer

    def test_files(self, name=None):
        if name == "h2020":
            fsock = open('./www/static/js/metric-module/h2020.json', "rb")
            print(type(fsock))
            response = HttpResponse(content=fsock)
            response['Content-Type'] = 'application/json'
            response['Content-Disposition'] = 'attachment; filename="%s.json"' \
                                              % 'whatever'

            return response

        else:

            node = []
            comunity = Community.objects.all()
            comunity_filtered = comunity.filter(communityId=int(name))
            for nodes in comunity_filtered:
                node = (nodes['communityProjects'])

            edges = Graph_edges.objects.all()

            edges_filtered = edges.filter(source__in=list(node), target__in=list(node))

            nodes = Graph_nodes.objects.all()
            nodes_filtered = nodes.filter(idnode__in=list(node))
            nodes_pd = pd.read_json(nodes_filtered.to_json())

            edges_pd = pd.read_json(edges_filtered.to_json())
            Y = nx.from_pandas_edgelist(edges_pd, 'source', 'target', 'weight')

            nx.set_node_attributes(Y, dict(Y.degree()), 'size')
            for node in Y.nodes:
                Y.node[node]['idproject'] = ((nodes_pd.loc[nodes_pd['idnode'] == node]['idproject']).iloc[0])['$oid']

            HJson = json_graph.node_link_data(Y)
            print("Graph Done - Nº Nodes = " + str(len(Y.nodes)) + " Density = " + str(nx.density(Y)))

            # pprint.pprint(json.dumps(HJson))
            return HttpResponse(json.dumps(HJson), content_type="application/json")


class CommunityEstimationViewSet(ViewSet):
    def create(self, request):

        lsa_model = joblib.load(
            'data/models-h2020/lsa_model.sav')
        svd_model = joblib.load(
            'data/models-h2020/svd_model.sav')
        tfidf = joblib.load(
            'data/models-h2020/tfidf.sav')

        new_entry = []
        entry = request.data.get('entry', '*')
        new_entry.append(entry)

        entry = tfidf.transform(new_entry)

        if entry is not '*':
            lsa_entry = svd_model.transform(entry)
            sim = []
            for i, row in enumerate(lsa_model):
                rho, _ = stats.spearmanr(lsa_entry[0], row)
                sim.append({
                    'index': i,
                    'rho': rho
                })
            sorted_sim = sorted(sim, reverse=True, key=lambda x: x['rho'])
            Graph_nodes.objects.all()

            c = db.data.community
            mayority_com = []

            for entry in sorted_sim[:100]:
                com = c.find_one({'communityProjects': entry['index']})
                mayority_com.append(com['communityId'])

            c = Counter(mayority_com)
            print(c.most_common())
        return Response(dict(c.most_common()))


class ListCountriesAvailableViewSet(ViewSet):
    serializer_class = GraphH2020ViewSetSerializer

    def list(self, _):
        queryset = Graph_nodes.objects.values_list('country').order_by('country').distinct('country')
        return Response(queryset)


class GetRecommendationViewSet(ViewSet):
    def create(self, request):
        plt.clf()
        itime = time.time()
        entry = request.data.get('search', '*')
        presupuesto = request.data.get('presupuesto', '*')
        subvencion = request.data.get('subvencion', '*')
        country = request.data.get('country', '*')
        startdate = request.data.get('startdate', '*')

        if entry == '*' or presupuesto == '*' or subvencion == '*' or country == '*' or startdate == '*':
            return HttpResponse(json.dumps({"results": '0'}), content_type="application/json")
        df = joblib.load('data/models-h2020/pandas_all_SVM_data.sav')

        mins, maxs = df['subvencion'].quantile([0., 1.])
        minp, maxp = df['presupuesto'].quantile([0., 1.])

        svd_model = joblib.load(
            'data/models-h2020/svd_model.sav')
        LabelEncoder = joblib.load('data/models-h2020/LabelEncoder.sav')
        tfidf = joblib.load(
            'data/models-h2020/tfidf.sav')
        IsolationForest = joblib.load(
            'data/models-h2020/IsolationForest.sav')

        mintime, maxtime = [1388534400, 1543622000]
        if int(startdate / 1000) < mintime | int(startdate / 1000) > maxtime:
            print('startdate low or high')
            return HttpResponse(json.dumps({"results": '0'}), content_type="application/json")

        d = {'country': LabelEncoder.transform([country]), 'subvencion': [subvencion], 'presupuesto': [presupuesto],
             'startdate': [startdate]}
        pprint.pprint(d)
        dataframe_no_objetive = pd.DataFrame(data=d)
        new_entry = []
        new_entry.append(entry)
        entry = tfidf.transform(new_entry)

        if entry is not '*':

            path = 'static/images/recommendation/*'

            try:
                for f in glob.glob(path):
                    os.remove(f)
            except Exception as e:
                print(e)

            DimensionalityReduction = svd_model.transform(entry)
            DimensionalityReduction_dataframe = pd.DataFrame(DimensionalityReduction)
            result = pd.concat([dataframe_no_objetive, DimensionalityReduction_dataframe], axis=1)

            result = result.drop(axis=1, labels=['startdate'])
            Isolation = IsolationForest.predict(result)
            print(Isolation)

            predict = [int(subvencion), int(presupuesto)]
            X = df.loc[df['country'] == float(LabelEncoder.transform([country]))]
            X_train = X[['subvencion', 'presupuesto']].as_matrix()
            mins, maxs = X['subvencion'].quantile([0., 1.])
            minp, maxp = X['presupuesto'].quantile([0., 1.])

            Iso_Sub_Pres = ensemble.IsolationForest(max_samples=999999, random_state=42, contamination=0.25)
            IsolationForest_Sub_Pres = Iso_Sub_Pres.fit(X_train)
            y = IsolationForest_Sub_Pres.predict([predict])
            print(y)

            z = IsolationForest_Sub_Pres.decision_function([predict])
            print(z)
            plt.figure(figsize=(8, 8))
            plt.title("Isolation Forest with result = " + str(y))

            xx, yy = np.meshgrid(np.linspace(predict[0] / 15, predict[0] * 3, 120),
                                 np.linspace(predict[1] / 15, predict[1] * 3, 120))
            Z = IsolationForest_Sub_Pres.decision_function(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)

            plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
            pr = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
            plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

            Z[Z < .035] = -1

            plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='green')

            b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='yellow',
                             s=50, edgecolor='k')
            c1 = plt.scatter(predict[0], predict[1], c='white',
                             s=200, edgecolor='k')

            plt.xlim((predict[0] / 15, predict[0] * 3))
            plt.ylim((predict[1] / 15, predict[1] * 3))

            plt.xlabel('Subvencion')
            plt.ylabel('Presupuesto')

            plt.legend([pr.collections[0], b1, c1],
                       ["Learning Limit", "Training set", "Predicted Result"], loc="upper left")

            h = hashlib.new('ripemd160')
            key = str(time.time())
            h.update(key.encode())
            key = h.hexdigest()[:6]

            path_key = []
            path_key.append('static/images/recommendation/' + key + '_foo.png')
            plt.savefig('static/images/recommendation/' + key + '_foo.png', )

            ##LocalOutlierFactor
            from sklearn.neighbors import LocalOutlierFactor
            clf = LocalOutlierFactor()

            clf.fit_predict(X_train)
            scores_pred = clf.negative_outlier_factor_

            threshold = stats.scoreatpercentile(scores_pred, 25)

            plt.figure(figsize=(8, 8))

            xx, yy = np.meshgrid(np.linspace(predict[0] / 5, predict[0] * 2, 120),
                                 np.linspace(predict[1] / 5, predict[1] * 2, 120))
            Z = clf._decision_function(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)
            result = clf._decision_function([predict])[0]
            if result > threshold:
                y = [1]
            else:
                y = [-1]

            plt.title("Local Outlier Factor (LOF) with result = " + str(y))

            pr = plt.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors='darkred')
            plt.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors='palevioletred')

            a = plt.scatter(X_train[:, 0], X_train[:, 1], c='yellow',
                            edgecolor='k', s=75)
            b = plt.scatter(predict[0], predict[1], c='blue',
                            edgecolor='k', s=200)

            plt.xlim((predict[0] / 5, predict[0] * 2))
            plt.ylim((predict[1] / 5, predict[1] * 2))

            plt.legend([a, b, pr.collections[0]],
                       ["Training set",
                        "Predicted Result", "learned decision function"],
                       loc="upper left")

            plt.xlabel('Subvencion')
            plt.ylabel('Presupuesto')

            h = hashlib.new('ripemd160')
            key = str(time.time())
            h.update(key.encode())
            key = h.hexdigest()[:6]

            path_key.append('static/images/recommendation/' + key + '_foo.png')

            plt.savefig('static/images/recommendation/' + key + '_foo.png')

            path_key = ['/' + x for x in path_key]

            print(time.time() - itime)
        return HttpResponse(
            json.dumps({'resultGlobal': str(Isolation[0]), 'resultSubPres': str(y[0]), 'image': path_key}),
            content_type="application/json")


class SearchViewSet(ViewSet):
    def create(self, request):
        model = request.data.get('model', '*')

        if model == "project":
            what = request.data.get('what', '*')
            where = request.data.get('where', '*')

            kwargs = {
                '{0}__{1}'.format(what, 'icontains'): where,
            }
            from django.core import serializers

            response = Proyecto.objects.all()
            projets = response.filter(**kwargs)
            data = serializers.serialize("json", projets)

            serializer = ProyectoSerializer(projets[0])
            pprint.pprint(serializer.data)

            return Response(data)
